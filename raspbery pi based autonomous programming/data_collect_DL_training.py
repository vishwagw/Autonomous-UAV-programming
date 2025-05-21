import tensorflow as tf
from tensorflow.python.keras import models, layers, datasets
import matplotlib as plt
import numpy as np

# Load Data Image
train_images = ... # Obstacle image data to use for learning
train_labels = ... # Image labels to use for training (obstacle / non-obstacle)

# model construction
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))


 # output layer
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(1))

# model compilation
model.compile(optimizer='adam',loss=tf.keras.losses.BinaryCrossentropy(from_logits=True), metrics=['accuracy'])

# model learning
history = model.fit(train_images, train_labels, epochs=10, validation_data=(test_images, test_labels))