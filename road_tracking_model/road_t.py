import cv2
import numpy as np
from ultralytics import YOLO
import supervision as sv

# Load the YOLOv8 model (replace with your fine-tuned road detection model if available)
model = YOLO("./yolov8n.pt")  # Use a custom model like 'road_detection.pt' if trained

# Specify the video file path
video_path = "./input/in2.mp4"  # Replace with your video file path
cap = cv2.VideoCapture(video_path)

# Check if video loaded successfully
if not cap.isOpened():
    print(f"Error: Could not open video file at {video_path}")
    exit()

# Initialize Supervision annotators
box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

# Parameters for flight path simulation
flight_height = 100  # Simulated height in meters (for visualization)
center_offset = 0    # Offset to keep the "flight" centered between road lines

# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Optional: Save output video
output_path = "./output_road_tracking2.mp4"
out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

