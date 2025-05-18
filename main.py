import cv2
import sys
import time


def bgr_to_ansi(b, g, r, is_bg=False):
    return f"\033[{48 if is_bg else 38};2;{r};{g};{b}m"


def frame_to_ansi_blocks(frame, width=80, height=None):
    h, w, _ = frame.shape
    aspect_ratio = h / w

    if height is None:
        # Default: calculate height to preserve aspect ratio (each block = 2 vertical pixels)
        height = int(aspect_ratio * width)
    print(
        f"Aspect ratio: {aspect_ratio:.2f}, Width: {width}, Height: {height}")
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


def main():
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Camera error.")
        sys.exit(1)

    print("\033[2J\033[?25l")  # Clear screen and hide cursor

    prev_time = 0
    target_fps = 15

    try:
        while True:
            now = time.time()
            if now - prev_time < 1.0 / target_fps:
                time.sleep((1.0 / target_fps) - (now - prev_time))
            prev_time = time.time()

            ret, frame = cap.read()
            if not ret:
                continue

            frame = cv2.flip(frame, 1)
            output = frame_to_ansi_blocks(frame, width=80)

            sys.stdout.write("\033[H" + output)
            sys.stdout.flush()
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        print("\033[0m\033[?25h")  # Reset terminal, show cursor


if __name__ == "__main__":
    main()
