from ultralytics import YOLO

print("YOLO class:", YOLO)
model = YOLO("yolov8n.pt")
print("Model loaded successfully")
