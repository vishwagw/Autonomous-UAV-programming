import cv2
import math
from ultralytics import YOLO

# initialize camera-option1:
cap = cv2.VideoCapture(0) # default webcam
# intialize video-option2:
#vid_path = './'
#cap = cv2.VideoCapture(vid_path)
# seting parameters:
cap.set(3, 640)
cap.set(4, 480)

# load custom-built yolo models:
model = YOLO('./custom_model/animalbest.pt')

# define object classes:
classNames = ["bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "lion"]

while True:
    success, img = cap.read()
    print("Frame read successfully!")
    results = model(source=0,show=True, conf=0.6, stream=True)

    # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            # putted box in cam
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            # Add a test rectangle to the frame
            cv2.rectangle(img, (100, 100), (200, 200), (0, 255, 0), 2)

            # confidence
            confidence = math.ceil((box.conf[0]*100))/100
            print("Confidence --->",confidence)

            # class name
            cls = int(box.cls[0])
            print("Class index -->", cls)
            print("Class name -->", classNames[cls])

            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()