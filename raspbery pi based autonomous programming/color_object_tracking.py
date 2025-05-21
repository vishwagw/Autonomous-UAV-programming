
import numpy as np 
import cv2 as cv
         
cap = cv.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
         
_, frame = cap.read()
rows, cols, _ = frame.shape
x_medium = int(cols/2)
center = int(cols /2)

position = 90

while True:
    _, frame = cap.read()
    hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    # red color
    low_red = np.array([4-5,61,0])
    high_red = np.array([4+5,255,255])
    red_mask = cv.inRange(hsv_frame, low_red, high_red)
    contours, _ = cv.findContours(red_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv.contourArea(x), reverse=True)

    for cnt in contours:
        (x,y,w,h) = cv.boundingRect(cnt)
        cv.rectangle(frame, (x,y),  (x+w, y+h), (0,255,0), 2)
        x_medium = int((x+x+w) / 2)
        break

    cv.line(frame, (x_medium, 0), (x_medium, 480), (0,255,0), 2)    
    cv.imshow('Frame', frame)
        
    key = cv.waitKey(1)
    if key == 27:
        break;

cap.release()
cv.destroyAllWindows()
