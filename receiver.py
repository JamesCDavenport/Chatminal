import cv2
import numpy as np
import socket
import struct
import sys
import time

from messagesocket import MessageSocket


def bgr_to_ansi(b, g, r, is_bg=False):
    return f"\033[{48 if is_bg else 38};2;{r};{g};{b}m"


def frame_to_ansi_blocks(frame, width=80, height=None):
    h, w, _ = frame.shape
    aspect_ratio = h / w

    if height is None:
        height = int(aspect_ratio * width)
    resized = cv2.resize(frame, (width, height))

    lines = []
    for y in range(0, resized.shape[0] - 1, 2):
        line = []
        for x in range(resized.shape[1]):
            top = resized[y, x]
            bottom = resized[y + 1, x]
            fg = bgr_to_ansi(*top, is_bg=False)
            bg = bgr_to_ansi(*bottom, is_bg=True)
            line.append(f"{fg}{bg}▄")
        lines.append("".join(line) + "\033[0m")
    return "\n".join(lines)


def recv_exact(sock, size):
    buf = b""
    while len(buf) < size:
        chunk = sock.recv(size - len(buf))
        if not chunk:
            raise ConnectionError("Socket closed")
        buf += chunk
    return buf


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9000))
    server.listen(1)

    print("Waiting for connection...")
    conn, _ = server.accept()
    msg_sock = MessageSocket(conn)
    print("\033[2J\033[?25l")  # Clear screen, hide cursor

    try:
        while True:
            # Read frame size
            name, data = msg_sock.recv()
            if name != "frame":
                continue
            np_arr = np.frombuffer(data, dtype=np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if frame is None:
                continue

            output = frame_to_ansi_blocks(frame, width=80)
            sys.stdout.write("\033[H" + output)
            sys.stdout.flush()
    except KeyboardInterrupt:
        pass
    finally:
        conn.close()
        server.close()
        print("\033[0m\033[?25h")  # Reset terminal, show cursor


if __name__ == "__main__":
    main()
