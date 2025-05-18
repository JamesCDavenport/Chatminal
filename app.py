from ascii_magic import AsciiArt
import cv2
import numpy

# splash = AsciiArt.from_image('logo.png')
# splash.to_terminal()
 
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    scale_percent = 5
    width = width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    small_frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

    cv2.imwrite('feed.png', small_frame)

    ascii_feed = AsciiArt.from_image('feed.png')
    ascii_feed.to_terminal()
 
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Display the resulting frame
    cv2.imshow('frame', small_frame)
    if cv2.waitKey(1) == ord('q'):
        break


    
    # ascii_frame = AsciiArt.to_terminal()
 
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()