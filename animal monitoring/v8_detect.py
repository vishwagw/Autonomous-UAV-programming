from ultralytics import YOLO
import cv2
import torch

# loading the yolo model:
y_model = YOLO('V8/yolov8m.pt')

# check for is CUDA is available:
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
y_model.to(device)

# video path:
vid_path = './input/in6.mp4'
cap = cv2.VideoCapture(vid_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 360))
    # run yolo:
    results = y_model(frame)

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0].item()
            cls = int(box.cls[0].item())
            label = y_model.names[cls]

            # filter only for flying objects:
            if label in ["bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "lion", "crocadile"]:
                cv2.rectangle(frame, (x1, y1), (x2, y2),  (0, 255, 0), 2)
                cv2.putText(frame, f"{label}: {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # display the frame:
    cv2.imshow("animal monitor", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# releasing
cap.release()
cv2.destroyAllWindows()