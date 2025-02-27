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

#create main program loop:
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("End of video or error reading frame.")
        break

    # Run YOLOv8 inference on the frame
    results = model(frame)[0]  # Get the first result from the list
    
    # Convert YOLOv8 results to Supervision Detections
    detections = sv.Detections(
        xyxy=results.boxes.xyxy.cpu().numpy(),           # Bounding box coordinates
        confidence=results.boxes.conf.cpu().numpy(),     # Confidence scores
        class_id=results.boxes.cls.cpu().numpy().astype(int)  # Class IDs
    )
    
    # Filter for road-related detections (adjust class_id based on your model)
    road_detections = detections[detections.class_id == 0]  # Assuming 'road' is class 0
    
    if len(road_detections) > 0:
        # Get bounding box coordinates of the detected road
        boxes = road_detections.xyxy
        
        # Calculate the center of the road
        road_centers = []
        for box in boxes:
            x1, y1, x2, y2 = box
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            road_centers.append((center_x, center_y))
        
        # Average the centers if multiple road segments are detected
        if road_centers:
            avg_center_x = int(np.mean([c[0] for c in road_centers]))
            avg_center_y = int(np.mean([c[1] for c in road_centers]))
            
            # Define flight path as staying between road lines
            flight_x = avg_center_x + center_offset
            flight_y = avg_center_y
            
            # Simulate flight path constraints (stay within road boundaries)
            if boxes[0][0] <= flight_x <= boxes[0][2]:  # Check if within x-bounds
                # Annotate flight path
                cv2.circle(frame, (flight_x, flight_y), 5, (0, 255, 0), -1)  # Green dot for flight position
                cv2.putText(frame, f"Flight Path: ({flight_x}, {flight_y}, {flight_height}m)", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Out of road bounds!", (10, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    # Annotate detections on the frame
    annotated_frame = box_annotator.annotate(scene=frame, detections=road_detections)
    labels = [f"Road {conf:.2f}" for conf in road_detections.confidence]
    annotated_frame = label_annotator.annotate(scene=annotated_frame, detections=road_detections, labels=labels)
    
    # Display the frame
    cv2.imshow("Road Tracking Flight", annotated_frame)
    
    # Write the frame to the output video
    out.write(annotated_frame)
    
    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv.destroyAllWindows()
print(f"Processed video saved as {output_path}")
