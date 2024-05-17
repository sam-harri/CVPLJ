import os
from roboflow import Roboflow
from dotenv import load_dotenv
from ultralytics import YOLO
import torch
import matplotlib.pyplot as plt

import os
from roboflow import Roboflow
from dotenv import load_dotenv
from ultralytics import YOLO
import torch
import matplotlib.pyplot as plt

# Load a pretrained YOLOv8 model (using a smaller model for reduced memory usage)
model = YOLO('runs/detect/train/weights/best.pt')

results = model(['134_png.rf.b7e22c1d19744b841613a07e3cf91b9b.jpg'])  # return a list of Results objects

# Process results list
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    # obb = result.obb  # Oriented boxes object for OBB outputs (Not available in your version)
    
    # Plot results
    result_image = result.plot()

    # Display the image using matplotlib
    plt.imshow(result_image)
    plt.axis('off')
    plt.show()

    # Save the result image
    result.save(filename='result.jpg')  # save to disk


# Train the model with reduced batch size, image size, and early stopping
# results = model.train(
#     data="/home/samh/CVPLJ/datasets/Computer-Vision-Powerlifting-1/data.yaml",
#     epochs=300,
#     imgsz=320,
#     batch=8,
#     patience=30  # Set patience for early stopping
# )

# # Evaluate the model on the test set
# metrics = model.val()  # no arguments needed, dataset and settings remembered


# model.export()