import cv2
import torch
import numpy as np
from ultralytics import YOLO
from dronekit import connect, VehicleMode, LocationGlobalRelative
import supervision as sv

# Connect to the drone
drone = connect("127.0.0.1:14550", wait_ready=True)  # Change if using real drone

def set_drone_velocity(vx, vy, vz):
    """Send velocity command to drone."""
    msg = drone.message_factory.set_position_target_local_ned_encode(
        0, 0, 0,  # Time, target, frame
        0b0000111111000111,  # Type mask
        0, 0, 0,  # Position (not used)
        vx, vy, vz,  # Velocity (m/s)
        0, 0, 0,  # Acceleration (not used)
        0, 0
    )
    drone.send_mavlink(msg)
    drone.flush()

# Load YOLOv8 model
model = YOLO("yolov8n.pt")  # Replace with custom-trained model for road detection

# Start video capture
cap = cv2.VideoCapture(0)  # Change to drone camera source

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Run YOLOv8 inference
    results = model(frame)
    
    # Process detections
    detections = results[0].boxes.xyxy.cpu().numpy()
    road_lines = []
    
    for det in detections:
        x1, y1, x2, y2 = det[:4]
        road_lines.append(((x1+x2)//2, (y1+y2)//2))  # Midpoints of detected road lines
    
    # Ensure we have at least two lines
    if len(road_lines) >= 2:
        road_lines.sort()  # Sort by x-coordinates
        left_line, right_line = road_lines[0], road_lines[-1]
        
        # Compute center of road
        road_center_x = (left_line[0] + right_line[0]) // 2
        frame_center_x = frame.shape[1] // 2
        
        # Determine drone movement
        error_x = road_center_x - frame_center_x
        
        if abs(error_x) > 20:
            vx = 0
            vy = -0.5 if error_x < 0 else 0.5  # Move left or right
            vz = 0
            set_drone_velocity(vx, vy, vz)
    
    # Display results
    sv.annotate(frame, results[0])
    cv2.imshow("Road Tracking", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
drone.close()
