import cv2 as cv
import os

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240

cap = cv.VideoCapture("http://[your wifi number]:8091/?action=stream")
cap.set(3, int(SCREEN_WIDTH))
cap.set(4, int(SCREEN_HEIGHT))

fource = cv.VideoWriter_fource(*'XVID')

try:
    if not os.path.exists('./data'):
        os.makedirs('./data')
except OSError:
    pass

video_orig = cv.VideoWriter('./data/object_video.avi', fource, 20.0, (SCREEN_WIDTH, SCREEN_HEIGHT))

while True:
    ret, frame = cap.read()
    if not ret:
        print("Fail Capture")
        break

    frame = cv.rotate(frame, cv.ROTATE_180)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    video_orig.write(frame)  # Save the video's frame
    cv.imshow('Video', frame)
    key = cv.waitKey(1)
    if key == 27:
        break

cap.release()
video_orig.release()
cv.destroyAllWindows()

