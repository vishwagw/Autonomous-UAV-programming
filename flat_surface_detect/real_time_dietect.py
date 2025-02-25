import cv2
import numpy as np

# Open video feed (0 for webcam, or replace with video file path)
cap = cv2.VideoCapture(0)  # Change to drone camera source

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # Exit if no frame is captured

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

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
