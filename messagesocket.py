import socket
import struct


class ProtocolError(Exception):
    """Custom exception for protocol errors."""


class MessageSocket:
    """
    A socket wrapper that sends and receives named binary messages.
    Each message consists of:
        - 4 bytes: length of the name (unsigned int, big-endian)
        - N bytes: name (UTF-8 encoded)
        - 4 bytes: length of payload (unsigned int, big-endian)
        - M bytes: payload (raw bytes)
    """

    def __init__(self, sock: socket.socket):
        self.sock = sock

    def send(self, name: str, payload: bytes):
        """Send a named binary message."""
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if not isinstance(payload, bytes):
            raise TypeError("Payload must be bytes")

        name_bytes = name.encode("utf-8")
        name_len = len(name_bytes)
        payload_len = len(payload)

        if name_len > 1024:
            raise ValueError("Name too long")
        if payload_len > 100 * 1024 * 1024:  # 100MB sanity cap
            raise ValueError("Payload too large")

        try:
            header = struct.pack(">I", name_len) + \
                name_bytes + struct.pack(">I", payload_len)
            self.sock.sendall(header + payload)
        except OSError as e:
            raise ConnectionError(f"Failed to send message: {e}")

    def recv(self) -> tuple[str, bytes]:
        """Receive a named binary message."""
        try:
            name_len = self._unpack_int(self._recv_exact(4))
            if name_len <= 0 or name_len > 1024:
                raise ProtocolError(f"Invalid name length: {name_len}")

            name = self._recv_exact(name_len).decode("utf-8")

            payload_len = self._unpack_int(self._recv_exact(4))
            if payload_len < 0 or payload_len > 100 * 1024 * 1024:
                raise ProtocolError(f"Invalid payload length: {payload_len}")

            payload = self._recv_exact(payload_len)
            return name, payload
        except OSError as e:
            raise ConnectionError(f"Socket error during recv: {e}")

    def _recv_exact(self, n: int) -> bytes:
        """Receive exactly n bytes or raise if connection is closed."""
        if n <= 0:
            raise ValueError(f"Invalid read size: {n}")

        buf = bytearray()
        while len(buf) < n:
            chunk = self.sock.recv(n - len(buf))
            if not chunk:
                raise ConnectionError(
                    "Socket closed unexpectedly while reading")
            buf.extend(chunk)
        return bytes(buf)

    def _unpack_int(self, b: bytes) -> int:
        return struct.unpack(">I", b)[0]
