import cv2
from ultralytics import YOLO

# Load trained YOLO model
model = YOLO("./models/best.pt") 

# Open drone camera feed (use actual drone stream URL)
# img = './inputs/weed test img3.png'
cap = cv2.VideoCapture(1)  # Change to RTSP URL or onboard camera

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO detection
    results = model(frame)

    # Draw bounding boxes and labels
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  
            label = model.names[int(box.cls)]  
            confidence = float(box.conf[0])  

            # Draw bounding box
            color = (0, 255, 0) if label == "crop" else (0, 0, 255)  # Green for crop, Red for weed
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f"{label} {confidence:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imshow("Weed Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
