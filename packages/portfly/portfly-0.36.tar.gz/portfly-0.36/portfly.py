#!/usr/bin/env python3
"""
Local/Remote Port Forwarding by TCP/UDP in Python.

Features:
1, Non-Blocking Socket.
2, Event IO.
3, TCP/UDP Tunnel. (private prototol)
4, Multi-Connection.

Author:   xinlin-z
Github:   https://github.com/xinlin-z/portfly
Blog:     https://cs.pynote.net
License:  MIT
"""
import os
import socket
from socket import IPPROTO_TCP, TCP_NODELAY
import selectors
import logging as log
import argparse
import random
import multiprocessing as mp
import threading
import time
from typing import Iterator, Generator
from dataclasses import dataclass
from base64 import b64encode, b64decode
from functools import partial
import hashlib
import platform


# set random seed
random.seed()
# socket type alias
sk_t = socket.socket


def cx(bmsg: bytes, b64: bool = False) -> bytes:
    """ b64=True is used for exchanging protocol msg.
    When b64 is False, there's only one extra byte ahead. """
    a = random.randint(0,255)
    t = random.randint(65,90)
    b = bytes((a,)) + bytes(c^a for c in bmsg)
    return b64encode(b)+bytes((t,)) if b64 else b


def dx(bmsg: bytes, b64: bool = False) -> bytes:
    bmsg = b64decode(bmsg[:-1]) if b64 else bmsg
    a = bmsg[0]
    return bytes(c^a for c in bmsg[1:])


cxb = partial(cx, b64=True)
dxb = partial(dx, b64=True)


SK_IO_CHUNK_LEN = 4096*8
UDP_RECV_LEN    = 1472  # 1500-20-8
UDP_SEND_LEN    = 1444
MAX_STREAM_ID   = 0xFFFFFFFF
HB_BASE_INTV    = 20
BOL = 'little'  # byte order little
BOB = 'big'     # byte order big
START_IDX       = 0x0406A000
CLIENT_RECONN_INTV = 8
UDP_PKT_TYPES = set((b'A',b'D'))


"""
Message Format:

* 4 bytes, total length, little endian
* 4 bytes, stream id, big endian
* 1 byte, type:
    0x01, Heart Beat (zero payload)
    0x02, Normal Data
    0x03, New Connection (zero payload)
    0x04, Connection Down (zero payload)
* variable length payload >=0
"""
MSG_HB = b'\x01'
MSG_ND = b'\x02'
MSG_NC = b'\x03'
MSG_CD = b'\x04'


def silent_close_socket(sk: sk_t) -> None:
    """ non-raise close socket """
    try:
        sk.shutdown(socket.SHUT_RDWR)
        sk.close()
    except OSError:
        return


class trafix():
    """ traffic exchanging class """
    @dataclass
    class sk_buf:
        sk: sk_t
        buf: bytes = b''

    ################################
    # UDP Tunnel layer includes:
    # pkt_sendto
    # send_sk_gen_udp
    # recv_sk_gen_udp
    ################################
    def pkt_sendto(self, pt, pkt):
        elen = 16 if self.md5 else 0

        # the first 2 bytes is total length,
        # the last 4 bytes is packet index, if no md5 hash.
        if pt in UDP_PKT_TYPES:
            pkt = int.to_bytes(len(pkt)+3+elen,2,BOL) + pt + pkt
            if self.md5:
                pkt += hashlib.md5(pkt).digest()
            plen = len(pkt)
            if pt == b'D':
                self.noack[self.uidx] = pkt
        else:
            plen = len(pkt)
            idx = int.from_bytes(pkt[plen-4-elen:plen-elen], BOL)
            log.debug('try [%d] --> %s %d', self.port, pt, idx)

        if not self.taddr:
            log.debug('do not have udp target address yet!')
            return 0

        # [re]send! Every time the xor byte is different.
        slen = self.sk.sendto(cx(pkt) if self.x else pkt, self.taddr)
        if slen == plen+(1 if self.x else 0):
            return 1
        else:
            log.error('[%d] sendto return less! %s plen=%d slen=%d',
                                            self.port, pt, plen, slen)
            return 0

    def send_sk_gen_udp(self, sk):
        data = b''
        resend_time = time.time()
        stop = False
        while True:
            # yield includes none ack udp packets
            noack_size = 0
            for rd in self.noack.values():
                noack_size += len(rd)
            bmsg, sid = yield len(data)+noack_size
            if bmsg:
                data += (len(bmsg)+8).to_bytes(4,BOL) \
                                + sid.to_bytes(4,BOB) \
                                + bmsg
            try:
                # if noack is empty, update resend time
                if not self.noack:
                    stop = False
                    resend_time = time.time()
                else:  # try resend
                    stop = True
                    if time.time()-resend_time > 0.6:
                        for rd in self.noack.values():
                            if self.pkt_sendto(b'R',rd) == 0:
                                break
                        resend_time = time.time()
                # normal send
                while not stop and len(data):
                    self.uidx += 1
                    pkt = data[:UDP_SEND_LEN] + int.to_bytes(self.uidx,4,BOL)
                    data = data[UDP_SEND_LEN:]
                    if self.pkt_sendto(b'D',pkt) == 0:
                        break
            except BlockingIOError:
                continue

    def recv_sk_gen_udp(self, sk: sk_t):
        data = b''
        recv_max_idx = START_IDX
        recv_idxlst = []
        recv_data_flag = False
        while True:
          try:
            # recv
            rd, taddr = sk.recvfrom(UDP_RECV_LEN)
            # init target addr
            if not self.taddr:
                self.taddr = taddr
                log.warning('init udp target addr %s', str(taddr))
            # check taddr
            elif taddr != self.taddr:
                log.error('udp target addr changed, packet dropped!')
                continue
            # dx
            if self.x:
                rd = dx(rd)
            # deal packet
            plen = len(rd)
            if plen>2 and int.from_bytes(rd[:2],BOL)==plen:
                # check md5
                if self.md5:
                    rd, md5 = rd[:-16], rd[-16:]
                    if hashlib.md5(rd).digest() != md5:
                        log.error('recv illegal packet, md5 wrong!')
                        continue
                # check type
                t = rd[2:3]
                if t not in UDP_PKT_TYPES:
                    log.error('recv illegal packet, type wrong!')
                    continue
                # get recv idx
                recv_idx = int.from_bytes(rd[-4:], BOL)
                # if ack
                if t == b'A':
                    num = int.from_bytes(rd[3:7], BOL)
                    rmidx = int.from_bytes(rd[7:11], BOL)
                    for i in range(num):
                        idx = int.from_bytes(rd[11+i*4:15+i*4], BOL)
                        self.noack.pop(idx, None)
                    for i in list(self.noack.keys()):
                        if i <= rmidx:
                            self.noack.pop(i, None)
                    log.debug('[%d] A <-- n:%d max:%d noack:%d fdata:%d',
                                    self.port, num, rmidx,
                                    len(self.noack), len(self.fdata))
                # if data
                else:  # t == b'D':
                    recv_data_flag = True
                    log.debug('[%d] D <-- %d %d', self.port,recv_idx,plen)
                    recv_idxlst.append(recv_idx)
                    if recv_idx>recv_max_idx and recv_idx not in self.fdata:
                        # save data
                        self.fdata[recv_idx] = rd[3:-4]
                        # concatenate
                        while (nid:=recv_max_idx+1) in self.fdata:
                            data += self.fdata[nid]
                            self.fdata.pop(nid)
                            recv_max_idx = nid
                        # yield msg
                        while(datalen:=len(data)) > 4:
                            msglen = int.from_bytes(data[:4], BOL)
                            if datalen >= msglen:
                                sid = int.from_bytes(data[4:8], BOB)
                                msg = data[8:msglen]
                                yield sid, msg[:1], msg[1:]
                                data = data[msglen:]
                            else:
                                break
                    if len(recv_idxlst) >= 256:
                        raise BlockingIOError()
            else:
                log.error('recv illegal packet, length wrong!')
          except BlockingIOError:
            # send A packet
            if recv_data_flag:
                try:
                    n = 0
                    cont = b''
                    for i in recv_idxlst:
                        if i > recv_max_idx:
                            n += 1
                            cont += int.to_bytes(i,4,BOL)
                    assert n <= 256
                    self.pkt_sendto(b'A', int.to_bytes(n,4,BOL)
                                         +int.to_bytes(recv_max_idx,4,BOL)
                                         +cont)
                    log.debug('send A packet, n=%d' % n)
                except BlockingIOError:
                  pass
            # return
            yield None, b'\x00', b''
            # resume
            recv_idxlst = []
            recv_data_flag = False

    ################################
    # TCP Tunnel layer includes:
    # send_sk_gen
    # recv_sk_gen
    ################################
    def send_sk_gen(self, sk: sk_t) \
                    -> Generator[int, tuple[bytes|None,int], None]:
        """ socket nonblocking send generator """
        data = b''
        while True:
            bmsg, sid = yield len(data)
            if bmsg:
                if self.x:
                    bmsg = cx(bmsg)
                mlen = len(bmsg) + 8 + (16 if self.md5 else 0)
                data += mlen.to_bytes(4,BOL) + sid.to_bytes(4,BOB) + bmsg
                if self.md5:
                    data += hashlib.md5(data[-mlen+16:]).digest()
            try:
                while len(data):
                    if (i:=sk.send(data[:SK_IO_CHUNK_LEN])) == -1:
                        raise ConnectionError('send_sk_gen send -1')
                    data = data[i:]
            except BlockingIOError:
                continue

    def recv_sk_gen(self, sk: sk_t) \
                    -> Iterator[tuple[int|None,bytes,bytes]]:
        """ socket nonblocking recv generator,
            yield sid,type,msg """
        data = b''
        while True:
            try:
                d = sk.recv(SK_IO_CHUNK_LEN)
                if len(d) == 0:
                    raise ConnectionError('recv_sk_gen recv 0')
                data += d
                while (tlen:=len(data)) > 4:
                    mlen = int.from_bytes(data[:4], BOL)
                    if tlen >= mlen:
                        epos = mlen
                        if self.md5:
                            epos = mlen - 16
                            md5 = data[epos:mlen]
                            if md5 != hashlib.md5(data[:epos]).digest():
                                data = data[mlen:]
                                log.error('[%d] tcp md5 error', self.port)
                                continue
                        sid = int.from_bytes(data[4:8], BOB)
                        msg = dx(data[8:epos]) if self.x else data[8:epos]
                        yield sid, msg[:1], msg[1:]
                        data = data[mlen:]
                    else:
                        break
            except BlockingIOError:
                yield None, b'\x00', b''

    ####################################
    # __init__ as main control flow
    ####################################
    def __init__(self, config: dict) -> None:
        self.session_type = config['session_type']
        self.role = config['role']
        if self.session_type == 'udp':
            self.uidx = START_IDX
            self.noack = {}
            self.fdata = {}
            self.sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sk.setblocking(False)
            if config['is_server']:
                self.sk.bind(('',config['tunnel_udp_port']))
                self.taddr = None
            else:
                self.taddr = (config['tunnel_udp_ip'],
                              config['tunnel_udp_port'])
            self.gen_recv = self.recv_sk_gen_udp(self.sk)
            self.gen_send = self.send_sk_gen_udp(self.sk)
        elif self.session_type == 'tcp':
            self.sk = config['tunnel_tcp_sk']
            self.sk.setblocking(False)
            self.gen_recv = self.recv_sk_gen(self.sk)
            self.gen_send = self.send_sk_gen(self.sk)
        next(self.gen_send)

        # selector
        self.sel = selectors.DefaultSelector()
        self.sel.register(self.sk, selectors.EVENT_READ, self._recv_tunnel)

        #
        self.port = int(config['listen_port'])
        self.x = config['tunnel_x']
        self.md5 = config['tunnel_md5']
        if self.role == 's':
            self.pserv = config['listen_sk']
            self.pserv.setblocking(False)
            self.sid = 1          # sid, stream id
            self.sel.register(self.pserv,
                              selectors.EVENT_READ,
                              self._new_connect_role_s)
        else:
            self.target = (config['target_ip'], config['target_port'])

        self.sdict: dict[int, trafix.sk_buf] = {}
        self.kdict: dict[sk_t,int] = {}    # socket --> sid
        self.reg: int = 0
        self.unreg: int = 0

        # send one HB to make udp server know its client
        self.heartbeat_time = time.time()
        self.heartbeat_max = 0
        self.gen_send.send((MSG_HB,0))

        # event loop
        try:
            while True:
                self.try_send_heartbeat()
                bytes_left = self.flush()
                sel_wait = 0.1 if bytes_left>0 else HB_BASE_INTV
                for fd, _ in self.sel.select(sel_wait):
                    fd.data(fd)
        except Exception as e:
            log.error('[%d] exception: %s', self.port, str(e))
            log.exception(e)
            for skb in self.sdict.values():
                silent_close_socket(skb.sk)
        # the end
        silent_close_socket(self.sk)
        self.sel.unregister(self.sk)
        if self.role == 's':
            silent_close_socket(self.pserv)
        log.warning('[%d] closed', self.port)

    def send_sk_conn(self, sid: int) -> int:
        skb = self.sdict[sid]
        data = skb.buf
        try:
            while len(data):
                if (i:=skb.sk.send(data[:SK_IO_CHUNK_LEN])) == -1:
                    raise ConnectionError('send_sk_conn send -1')
                data = self.sdict[sid].buf = data[i:]
        except BlockingIOError:
            pass
        return len(data)

    def flush(self) -> int:
        """ flush all sending socket, return left bytes number """
        tunnel_left = self.gen_send.send((None,0))
        sk_left = 0
        for sid in list(self.sdict.keys()):
            try:
                sk_left += self.send_sk_conn(sid)
            except OSError as e:
                log.info('[%d] sid %d down while flush',self.port,sid,str(e))
                tunnel_left = self.gen_send.send((MSG_CD,sid))
                self.clean(sid)
        return tunnel_left + sk_left

    def try_send_heartbeat(self) -> None:
        if self.heartbeat_max > 6:
            raise ConnectionError('heartbeat max is reached')
        now = time.time()
        if now - self.heartbeat_time > HB_BASE_INTV:
            self.gen_send.send((MSG_HB,0))
            log.info('[%d] send heartbeat', self.port)
            self.heartbeat_time = now + random.randint(0,39)
            self.heartbeat_max += 1

    def clean(self, sid: int) -> None:
        """ delete sid from sdict,
            delete sk from kdict,
            close socket,
            unregister sk from selector. """
        assert len(self.sdict) == len(self.kdict)
        _skb = self.sdict.pop(sid)
        sk = _skb.sk
        if sk:
            self.kdict.pop(sk, None)
            silent_close_socket(sk)
            self.sel.unregister(sk)
            self.unreg += 1
            log.debug('[%d] unreg %d', self.port, self.unreg)

    def _new_connect_role_s(self, fd):
        assert fd.fileobj == self.pserv
        try:
            while True:
                s, addr = self.pserv.accept()
                self.gen_send.send((MSG_NC, self.sid))
                log.info('[%d] accept %s, sid %d',self.port,str(addr),self.sid)
                s.setsockopt(IPPROTO_TCP, TCP_NODELAY, True)
                s.setblocking(False)  # set nonblocking
                self.sel.register(s, selectors.EVENT_READ, self._recv_conn)
                self.reg += 1
                log.debug('[%d] reg %d', self.port, self.reg)
                self.sdict[self.sid] = trafix.sk_buf(s)
                self.kdict[s] = self.sid
                # update sid, 0 is used for heartbeat
                while True:
                    self.sid = self.sid+1 if self.sid!=MAX_STREAM_ID else 1
                    if self.sid not in self.sdict.keys():
                        break
        except BlockingIOError:
            pass

    def _recv_tunnel(self, fd):
        p = self.port
        while True:
            sid, t, bmsg = next(self.gen_recv)
            if sid is not None:  # sid==0 is legal
                log.debug('[%d] recv tunnel, type: %s, sid: %d', p,t,sid)
                # data first
                if t == MSG_ND:
                    try:
                        if sid in self.sdict.keys():
                            self.sdict[sid].buf += bmsg
                            self.send_sk_conn(sid)
                    except OSError:
                        self.gen_send.send((MSG_CD,sid))
                        self.clean(sid)
                        log.info('[%d] sid %d is closed while send', p, sid)
                # new connection in client role
                elif t == MSG_NC:
                    try:
                        s = socket.create_connection(self.target, timeout=2)
                        log.info('[%d] connect target %s ok, sid %d',
                                 p, str(self.target), sid)
                        s.setsockopt(IPPROTO_TCP, TCP_NODELAY, True)
                        s.setblocking(False)
                        self.sel.register(s,
                                          selectors.EVENT_READ,
                                          self._recv_conn)
                        self.sdict[sid] = trafix.sk_buf(s)
                        self.kdict[s] = sid
                        self.reg += 1
                        log.debug('[%d] reg %d', p, self.reg)
                    except OSError as e:
                        log.error('[%d] connect %s failed: %s',
                                  p, str(self.target), str(e))
                        self.gen_send.send((MSG_CD,sid))
                # connection down
                elif t == MSG_CD:
                    if sid in self.sdict.keys():
                        self.clean(sid)
                        log.info('[%d] close sid %d by peer', p, sid)
                # heartbeat
                else:
                    assert t == MSG_HB
                    self.heartbeat_max = 0
                    log.debug('[%d] recv heartbeat', p)
            else:
                return

    def _recv_conn(self, fd):
        try:
            sid = self.kdict[fd.fileobj]
        except KeyError:
            return
        try:
            data = fd.fileobj.recv(SK_IO_CHUNK_LEN)
            if len(data) == 0:
                raise ConnectionError('recv_sk_gen_conn recv 0')
            self.gen_send.send((MSG_ND+data,sid))  # send data
        except OSError as e:
            self.gen_send.send((MSG_CD,sid))
            self.clean(sid)
            log.info('[%d] sid %d donw when recv, %s',self.port,sid,str(e))


def zombie_reaper():
    while True:
        try:
            pid, stat = os.wait()
            log.warning('reap zombie pid %d status %s' % (pid,stat))
        except ChildProcessError:
            time.sleep(60)


def server_main(saddr: tuple[str,int], key: bytes) -> None:
    if platform.system() != 'Windows':
        threading.Thread(target=zombie_reaper,args=(),daemon=True).start()
        log.warning('init zombie reaper thread')
    serv = socket.create_server(saddr)
    log.warning('init server listen at %s', str(saddr))

    config = {}
    config['is_server'] = True
    while True:
        sk, faddr = serv.accept()
        log.warning('accept connection from %s', str(faddr))
        sk.settimeout(3)
        sk.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        rf = sk.makefile('rb')
        try:
            keyhash = hashlib.sha256(key).digest()
            if dxb(rf.readline().strip()) == keyhash:
                # recv
                forward_mode = dxb(rf.readline().strip())
                log.warning('forwarding mode %s', forward_mode)
                transprot = dxb(rf.readline().strip())
                log.warning('transport protocol %s', transprot)
                udpport = int(dxb(rf.readline().strip()))
                log.warning('udp port %d', udpport)
                if forward_mode == b'R':
                    listen_port = int(dxb(rf.readline().strip()))
                    g = eval((dxb(rf.readline().strip())).decode())
                    log.warning('listen global %d', g)
                    pserv = socket.create_server(('' if g else '127.0.0.1',
                                                  listen_port))
                    log.warning('create server at port %d', listen_port)
                else:  # forward_mode == b'L':
                    target_ip = dxb(rf.readline().strip())
                    target_port = int(dxb(rf.readline().strip()))
                    log.warning('target addr %s:%s', target_ip, target_port)
                x = eval((dxb(rf.readline().strip())).decode())
                log.warning('encryption %d', x)
                md5 = eval((dxb(rf.readline().strip())).decode())
                log.warning('md5 %d', md5)
                # reply
                sk.sendall(cxb(hashlib.sha256(keyhash[:16]).digest()) + b'\n')
                # process parameters
                config['tunnel_x'] = x
                config['tunnel_md5'] = md5
                if forward_mode == b'R':
                    config['role'] = 's'
                    config['listen_sk'] = pserv
                    config['listen_port'] = listen_port
                else:  # if forward_mode == b'L':
                    config['role'] = 'c'
                    config['listen_port'] = -1
                    config['target_ip'] = target_ip
                    config['target_port'] = target_port
                if transprot == b'tcp':
                    config['session_type'] = 'tcp'
                    config['tunnel_tcp_sk'] = sk
                else:  # if transprot == b'udp':
                    config['session_type'] = 'udp'
                    config['tunnel_udp_port'] = udpport
                    silent_close_socket(sk)
                # launching process
                mp.Process(target=trafix,args=(config,),daemon=True).start()
                log.warning('process launched...')
            else:
                raise ValueError('magic bmsg error')
        except Exception as e:
            log.error('exception %s', str(faddr))
            log.exception(e)
            silent_close_socket(sk)


def client_main(config: dict, key: bytes) -> None:
    while True:
        try:
            # if local port forwarding
            if config['forward_mode'] == 'L':
                pserv = socket.create_server(
                            ('' if config['tunnel_g'] else '127.0.0.1',
                             config['listen_port']))
                log.warning('port %d is ready here', config['listen_port'])
                config['listen_sk'] = pserv
            # connect server, send parameters
            keyhash = hashlib.sha256(key).digest()
            saddr = (config['server_ip'], config['server_port'])
            sk = socket.create_connection(saddr)
            sk.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
            sk.sendall(cxb(keyhash) + b'\n')
            sk.sendall(cxb(config['forward_mode'].encode()) + b'\n')
            sk.sendall(cxb(config['session_type'].encode()) + b'\n')
            sk.sendall(cxb(str(config['tunnel_udp_port']).encode()) + b'\n')
            if config['forward_mode'] == 'R':
                sk.sendall(cxb(str(config['listen_port']).encode()) + b'\n')
                sk.sendall(cxb(str(int(config['tunnel_g'])).encode()) + b'\n')
            else:
                sk.sendall(cxb(config['target_ip'].encode()) + b'\n')
                sk.sendall(cxb(str(config['target_port']).encode()) + b'\n')
            sk.sendall(cxb(str(int(config['tunnel_x'])).encode()) + b'\n')
            sk.sendall(cxb(str(int(config['tunnel_md5'])).encode()) + b'\n')
            # read the only reply
            rf = sk.makefile('rb')
            if dxb(rf.readline().strip()) == hashlib.sha256(keyhash[:16]).digest():
                if config['forward_mode'] == 'R':
                  log.warning('connect server %s ok, port %d is ready there',
                                            str(saddr), config['listen_port'])
                else:
                  log.warning('connect server %s ok', str(saddr))
            else:
                raise ValueError('magic_breply is not match')
            # tcp tunnel socket
            if config['session_type'] == 'tcp':
                config['tunnel_tcp_sk'] = sk
            else:
                silent_close_socket(sk)
            # go
            trafix(config)
        except Exception as e:
            log.exception(e)
        finally:
            silent_close_socket(sk)
            if config['forward_mode'] == 'L':
                silent_close_socket(pserv)
            time.sleep(CLIENT_RECONN_INTV)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-V', '--version',
                            action='version', version='portfly V0.36')
    parser.add_argument('--log', choices=('INFO','DEBUG'), default='WARNING')
    parser.add_argument('-x', action='store_true',
                        help='apply simple encryption to traffic')
    end_type = parser.add_mutually_exclusive_group(required=True)
    end_type.add_argument('-s', '--server', action='store_true')
    end_type.add_argument('-c', '--client', action='store_true')
    parser.add_argument('-L', action='store_true',
                        help='local port forwarding')
    parser.add_argument('-u', '--udpport', type=int,
                        help='specify the udp port for tunneling')
    parser.add_argument('--md5', action='store_true',
                        help='enhanced integrity check by md5')
    parser.add_argument('-g', action='store_true',
                        help='listen at 0.0.0.0, default 127.0.0.1')
    parser.add_argument('-k', '--key', required=True,
                        help='server access key string')
    parser.add_argument('settings',
                        help='example is in source code as comments')
    args = parser.parse_args()

    log.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',
                    level=eval('log.'+args.log))

    # $ python portfly.py -s [--log INFO|DEBUG] -k string server_ip:port
    if args.server:
        if args.x or args.L or args.udpport or args.md5:
            log.warning('-x, -L, -u, --md5 and -g'
                        ' are all ignored in server side')
        ip, port = args.settings.split(':')
        server_main((ip.strip(),int(port)), args.key.encode())
    # $ python portfly.py -c [-x] [-L] [-u port] [--md5] [--log INFO|DEBUG] \
    #                     -k string mapping_port:target_ip:port+server_ip:port
    else:
        config = {}
        config['is_server'] = False
        config['tunnel_x'] = args.x
        config['tunnel_md5'] = args.md5
        config['tunnel_g'] = args.g
        config['session_type'] = 'udp' if args.udpport else 'tcp'
        config['forward_mode'] = 'L' if args.L else 'R'
        config['role'] = 's' if args.L else 'c'
        mapping, saddr = args.settings.strip().split('+')
        listen_port, target_ip, target_port = mapping.split(':')
        config['listen_port'] = int(listen_port)
        config['target_ip'] = target_ip
        config['target_port'] = int(target_port)
        server_ip, server_port = saddr.strip().split(':')
        config['server_ip'] = server_ip
        config['server_port'] = int(server_port)
        config['tunnel_udp_ip'] = server_ip
        config['tunnel_udp_port'] = int(args.udpport) if args.udpport else 0
        client_main(config, args.key.encode())

