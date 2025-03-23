import cv2
from ultralytics import YOLO

# Load trained YOLO model
model = YOLO("./models/best.pt") 
