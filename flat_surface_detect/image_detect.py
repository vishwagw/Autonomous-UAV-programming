import cv2
import numpy as np

# Load the downward-facing camera image
image = cv2.imread("./imgs/in3.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Edge detection
edges = cv2.Canny(blurred, 50, 150)

# Find contours to detect large flat regions
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter large flat areas
flat_areas = []
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > 5000:  # Adjust threshold based on drone altitude
        flat_areas.append(cnt)

# Draw detected flat areas
cv2.drawContours(image, flat_areas, -1, (0, 255, 0), 3)

cv2.imshow("Flat Surface Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
