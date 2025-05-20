import cv2 as cv
import os 
import numpy as np
import tensorflow as tf
from tf_keras.models import Sequential
from tf_keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from sklearn.model_selection import train_test_split
from tf_keras.preprocessing.image import ImageDataGenerator

# Step 1: Capture Video Footage
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240

cap = cv.VideoCapture("http://[your wifi number]:8091/?action=stream")
cap.set(3, int(SCREEN_WIDTH))
cap.set(4, int(SCREEN_HEIGHT))

fourcc = cv.VideoWriter_fourcc(*'XVID')

try:
    if not os.path.exists('./data'):
        os.makedirs('./data')
except OSError:
    pass

video_orig = cv.VideoWriter('./data/object_video.avi', fourcc, 20.0, (SCREEN_WIDTH, SCREEN_HEIGHT))

frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print("캡쳐 실패")
        break

    frame = cv.rotate(frame, cv.ROTATE_180)
    video_orig.write(frame)  # Save video frame

    if frame_count % 10 == 0:  # Save every 10th frame as an image
            image_path = f'./data/frame_{frame_count}.jpg'
            cv.imwrite(image_path, frame)

    cv.imshow('Video', frame)
    frame_count += 1

    key = cv.waitKey(1)
    if key == 27:
        break

cap.release()
video_orig.release()
cv.destroyAllWindows()

# Step 3: Label Images (Manual Step)
# Manually label the saved images in the './data' directory using a tool like LabelImg. 

# Step 4: Data Preprocessing
image_paths = [os.path.join('./data', fname) for fname in os.listdir('./data') if fname.endswith('.jpg')]
labels = []  # Assuming labels are collected after manual labeling
images = []

for image_path in image_paths:
    image = cv.imread(image_path)
    image = cv.resize(image, (150, 150))
    images.append(image)
    labels.append(0)  # Replace with actual label after manual labeling

images = np.array(images) / 255.0  # Normalize pixel values
labels = np.array(labels)

# Split the data into training, validation, and testing sets
X_train, X_temp, y_train, y_temp = train_test_split(images, labels, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Step 5: Define and Compile a Deep Learning Model
num_classes = len(set(labels))
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    MaxPooling2D(pool_size=(2, 2)),

    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),

    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),

    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(num_classes, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Step 6: Train the Model
model.fit(
    X_train, y_train,
    epochs=20,
    validation_data=(X_val, y_val)
)

# Step 7: Evaluate the Model
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f'Test Accuracy: {test_acc}')
    
# Step 8: Save and Deploy the Model
model.save('object_recognition_model.h5')


    