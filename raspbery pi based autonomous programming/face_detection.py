#importing libraries 
import cv2 as cv

#cap = cv.VideoCapture(0)
cap = cv.VideoCapture('[https:// your raspberry pi wifi address]:8091/?action=stream')

face_detector = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')

#face_cascade = cv.CascadeClassifier()
#face_cascade.load(r"C:\Users\BKY-LG\anaconda3\envs\aidrone\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml")

while True:
    ret, frame = cap.read()
    frame = cv.rotate(frame, cv.ROTATE_180)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.equalizeHist(gray)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for(x, y, w, h) in faces:
        cv.rectangle(frame, (x, y), (x+h, y+h), (0, 255, 0), 3, 4, 0)

    cv.imshow('Face', frame)

    if cv.waitKey(10) >= 0:
        break

cap.release()
cv.destroyAllWindows()


