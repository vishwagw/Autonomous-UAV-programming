# for Tea crop detection
from ultralytics import YOLO
import cv2

# Load trained YOLO model (replace 'best.pt' with your model)
model = YOLO("best.pt")

# Open drone camera feed (use actual drone camera URL)
cap = cv2.VideoCapture(0)  # Change to RTSP URL or onboard camera

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO detection on the frame
    results = model(frame)

    # Draw bounding boxes and labels
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get box coordinates
            label = model.names[int(box.cls)]  # Get class name
            confidence = float(box.conf[0])  # Get confidence score

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {confidence:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show the output frame
    cv2.imshow("Tea Crop Detection", frame)
    
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
