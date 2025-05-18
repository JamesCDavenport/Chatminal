import cv2
import socket
import struct
import time


def main():
    cap = cv2.VideoCapture(0)
    resolution = (80, 45)
    if not cap.isOpened():
        print("Camera error.")
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("10.0.0.82", 9000))

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            resized_frame = cv2.resize(frame, resolution)

            _, buf = cv2.imencode(
                '.jpg', resized_frame)
            data = buf.tobytes()

            # Send frame size first
            sock.sendall(struct.pack(">I", len(data)))
            sock.sendall(data)

            time.sleep(1 / 15)  # Limit to ~15 FPS
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        sock.close()


if __name__ == "__main__":
    main()
