# # we need a custom trained model in yolo:
from ultralytics import YOLO
import cv2

# Load YOLO model (use a custom-trained model)
model = YOLO("./models/best.pt")

# Open drone camera feed (replace with actual video source)
#img = './'
cap = cv2.VideoCapture(1)  # Change to drone camera stream

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO detection
    results = model(frame)

    # Display results
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box
            label = model.names[int(box.cls)]  # Class name
            confidence = float(box.conf[0])  # Confidence score

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {confidence:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("Drone Live Feed 001", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
