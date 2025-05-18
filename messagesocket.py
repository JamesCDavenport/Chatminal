import socket
import struct


class MessageSocket:
    def __init__(self, sock: socket.socket):
        self.sock = sock

    def send(self, name: str, payload: bytes):
        name_bytes = name.encode('utf-8')
        name_len = len(name_bytes)
        payload_len = len(payload)

        header = struct.pack(">I", name_len) + name_bytes + \
            struct.pack(">I", payload_len)
        self.sock.sendall(header + payload)

    def recv(self):
        name_len_raw = self._recv_exact(4)
        name_len = struct.unpack(">I", name_len_raw)[0]

        name_bytes = self._recv_exact(name_len)
        name = name_bytes.decode('utf-8')

        payload_len_raw = self._recv_exact(4)
        payload_len = struct.unpack(">I", payload_len_raw)[0]

        payload = self._recv_exact(payload_len)
        return name, payload

    def _recv_exact(self, n):
        buf = b""
        while len(buf) < n:
            chunk = self.sock.recv(n - len(buf))
            if not chunk:
                raise ConnectionError("Socket closed before all data received")
            buf += chunk
        return buf
