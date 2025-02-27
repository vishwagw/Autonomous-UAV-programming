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
        
        #if abs(error_x) > 20:
        #   vx = 0
        #    vy = -0.5 if error_x < 0 else 0.5  # Move left or right
        #    vz = 0
        #    set_drone_velocity(vx, vy, vz)
    
    # Display results
    detections = sv.Detections.from_ultralytics(results[0])
    sv.draw_detections(frame, detections)
    cv2.imshow("Road Tracking", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
#drone.close()
