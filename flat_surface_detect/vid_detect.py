import cv2
import numpy as np

# Load the video file (Replace with your video path)
video_path = "./vids/in1.mp4"
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # Exit when the video ends

    # resize output:
    frame = cv2.resize(frame, (640, 360))

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours to detect flat regions
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter large flat areas
    flat_areas = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5000:  # Adjust based on drone altitude
            flat_areas.append(cnt)

    # Draw detected flat areas
    cv2.drawContours(frame, flat_areas, -1, (0, 255, 0), 3)

    # Display the processed video
    cv2.imshow("Flat Surface Detection", frame)

    # Press 'q' to exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
