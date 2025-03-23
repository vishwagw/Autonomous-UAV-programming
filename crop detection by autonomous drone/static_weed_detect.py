from ultralytics import YOLO
import cv2
import torch

# Load a pre-trained YOLOv8 model (COCO dataset or a custom-trained model)
model = YOLO("./models/best.pt")  # Replace with "best.pt" if using a custom-trained model

# Load an image
image_path = "./inputs/weed test img1.png"
image = cv2.imread(image_path)

# Run inference
results = model(image)

# Draw bounding boxes
for result in results:
    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Extract bounding box coordinates
        confidence = box.conf[0].item()  # Confidence score
        class_id = int(box.cls[0])  # Class ID
        
        # Draw rectangle
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"Weed {confidence:.2f}"
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Display the image
cv2.imshow("Weed Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
