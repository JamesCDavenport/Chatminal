import cv2
import socket
import struct
import time
from messagesocket import MessageSocket
import threading
import sounddevice as sd
import numpy as np


def video_sender(msg_sock):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera error.")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            _, buf = cv2.imencode(
                '.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
            msg_sock.send("video", buf.tobytes())
            time.sleep(1 / 15)
    finally:
        cap.release()


def main():
    sock = socket.create_connection(("127.0.0.1", 9000))
    msg_sock = MessageSocket(sock)

    t_video = threading.Thread(
        target=video_sender, args=(msg_sock,), daemon=True)

    t_video.start()

    t_video.join()


if __name__ == "__main__":
    main()
