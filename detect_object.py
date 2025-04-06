from ultralytics import YOLO

yolo= YOLO('yolov8n.pt')  # Load a pretrained YOLOv8 model
results = yolo("Screenshot 2025-04-04 141405.png") 

for result in results:
    result.show()  # Display the results