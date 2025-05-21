#importing the libraries
import cv2
import os
import time

#now lets create the folder for images
if not os.path.exists('Images') :
    os.makedirs('Images')

#then we can open the file for video capture.
video = cv2.VideoCapture('Video File')

#select the object which we want to track by the drone camera
ret, frame = video.read()
bbox = cv2.selectROI(frame, False)

#initializing the tracker
tracker = cv2.TrackerCSRT_create()
tracker.init(frame, bbox)

#Initialzing the timer + counter
timer = time.time()
counter = 0

#getting the video output
while True:
    #read frames
    ret, frame =video.read()
    if not ret:
        break

    #object traking 
    success, bbox = tracker.update(frame)

    #output trace result
    if success:
        x, y, w, h = [int(i) for i in bbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        #check if timer has expired and save object image
        current_time = time.time()
        if current_time - timer >= 1: #saving the image for 1 sec
            counter += 1
            object_img = frame[y:y+h, x:x+w]
            img_path = os.path.join('Images', f'object_img_{counter}'.jpg)
            cv2.imwrite(img_path, object_img)
            timer = current_time
        else:
            cv2.putText(frame, 'Failed to track object', (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

        #frame output :
        cv2.imshow('Object Tracking', frame)

        #Handling keyboard input :
        if cv2.waitKey(1) & 0xFF == ord('q') :
            break

    #Release the video file and close the window
    video.release()
    cv2.destroyAllWindows()



