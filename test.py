import cv2
import sys
import time

def rgb_to_ansi(r, g, b, is_bg=False):
    return f"\033[{'48' if is_bg else '38'};2;{r};{g};{b}m"

def frame_to_ansi_blocks(frame, width=80):
    h, w, _ = frame.shape
    aspect_ratio = h / w
    new_height = int(aspect_ratio * width * 0.5 * 2)  # *2 since we stack pixels vertically
    resized = cv2.resize(frame, (width, new_height))

    output = []
    for y in range(0, resized.shape[0] - 1, 2):
        line = ""
        for x in range(resized.shape[1]):
            top = resized[y, x]
            bottom = resized[y + 1, x]
            line += (
                rgb_to_ansi(*top, is_bg=False)
                + rgb_to_ansi(*bottom, is_bg=True)
                + "▄"
            )
        line += "\033[0m"  # Reset at end of line
        output.append(line)
    return "\n".join(output)

def main():
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Failed to open camera.")
        sys.exit(1)

    print("\033[2J\033[?25l")  # Clear screen, hide cursor

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)  # Flip horizontally for a mirror effect
            output = frame_to_ansi_blocks(frame, width=80)

            print("\033[H" + output, end="")  # Move cursor to top-left
            time.sleep(0.033)
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        print("\033[0m\033[?25h")  # Reset attributes, show cursor

if __name__ == "__main__":
    main()
