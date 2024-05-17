import os
from ultralytics import YOLO
import matplotlib.pyplot as plt
import cv2

# Define the path to your trained model and the image
model_path = 'best_model.pt'
image_path = '134_png.rf.b7e22c1d19744b841613a07e3cf91b9b.jpg'  # Change this to the path of your image

# Load the trained YOLOv8 model
model = YOLO(model_path)

# Run inference on the image
results = model(image_path)

# Display the results
results.show()

# Alternatively, to save the result:
# results.save('path_to_save_output')

# If you want to display the image with detected objects using OpenCV and matplotlib
# Load the image
img = cv2.imread(image_path)

# Convert the image from BGR to RGB (OpenCV loads images in BGR format)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Plot the image with bounding boxes
plt.figure(figsize=(10, 10))
plt.imshow(img)
plt.axis('off')

# Iterate over results and draw boxes
for box in results.boxes:
    x1, y1, x2, y2 = map(int, box.xyxy[0])  # Extract box coordinates
    confidence = box.conf[0]  # Extract confidence score
    cls = box.cls[0]  # Extract class

    # Draw the bounding box and label
    plt.gca().add_patch(plt.Rectangle((x1, y1), x2 - x1, y2 - y1, fill=False, edgecolor='red', linewidth=2))
    plt.gca().text(x1, y1, f'{results.names[int(cls)]} {confidence:.2f}', bbox=dict(facecolor='yellow', alpha=0.5), fontsize=10, color='black')

# Show the plot
plt.show()
