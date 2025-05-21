import cv2 as cv
import numpy as np 

mouse_is_pressing = False
start_x, start_y, end_x, end_y = -1,-1,-1,-1
step = 0
track_window  = None

def mouse_callback(event,x,y,flags,param):
    global start_x, start_y, end_x, end_y
    global step, mouse_is_pressing, track_window

    if event == cv.EVENT_LBUTTONDOWN:
        step = 1
        mouse_is_pressing = True
        start_x = x
        start_y = y
 
    elif event == cv.EVENT_MOUSEMOVE:
            if mouse_is_pressing:
                end_x = x
                end_y = y
                step = 2

    elif event == cv.EVENT_LBUTTONUP:
        mouse_is_pressing = False
        end_x = x
        end_y = y
        step = 3

cap = cv.VideoCapture(0)

if cap.isOpened() == False:
    print("카메라를 열 수 없습니다.")
    exit(1)

cv.namedWindow("Color")
cv.setMouseCallback("Color", mouse_callback) 

while True:
    ret, img_color = cap.read()
    if ret == False:
        print("캡쳐 실패")
        break;

    if step == 1: 
        cv.circle(img_color, (start_x, start_y), 10, (0, 255, 0), -1)

    elif step == 2: 
        cv.rectangle(img_color, (start_x, start_y), (end_x, end_y), (0, 255, 0), 3)

    elif step == 3:  
        if start_x > end_x:
            start_x, end_x = end_x, start_x
            start_y, end_y = end_y, start_x

            track_window = (start_x, start_y, end_x-start_x, end_y-start_y)
 
            img_hsv = cv.cvtColor(img_color, cv.COLOR_BGR2HSV)
            img_ROI = img_hsv[start_y:end_y, start_x:end_x]

            cv.imshow("ROI", img_ROI)

            objectHistogram = cv.calcHist([img_ROI], [0], None, [180], (0, 180))

            cv.normalize(objectHistogram, objectHistogram, alpha=0, beta=255, norm_type=cv.NORM_MINMAX)

            step = step + 1

    elif step == 4:
        img_hsv = cv.cvtColor(img_color, cv.COLOR_BGR2HSV)
        bp = cv.calcBackProject([img_hsv], [0], objectHistogram, [0,180], 1)

        rotatedRect, track_window = cv.CamShift(bp, track_window, ( cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1 ))

        cv.ellipse(img_color, rotatedRect, (0, 0, 255), 2);

        pts = cv.boxPoints(rotatedRect)
        pts = np.int0(pts)

        for i in range(4):
            cv.line(img_color, tuple(pts[i]), tuple(pts[(i + 1) % 4]), (0, 255, 0), 2)

    cv.imshow("Color", img_color)
 
    if cv.waitKey(25) >= 0:
        break  

  