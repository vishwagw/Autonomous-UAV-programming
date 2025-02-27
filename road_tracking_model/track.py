# import libs:
import cv2
import supervision as sv
import numpy as np
from ultralytics import YOLO

# import pretrained model:
model = YOLO('./models/yolov8n.pt')

# vid path:
vid = './input/in1.mp4'
cap = cv2.VideoCapture(vid)
# Load YOLOv8 model
model = YOLO("yolov8n.pt")  # Replace with custom-trained model for road detection

# Start video capture
cap = cv2.VideoCapture(0)  # Change to drone camera sourc

