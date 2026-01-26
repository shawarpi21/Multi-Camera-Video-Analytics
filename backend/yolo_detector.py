import cv2
import os
try:
    from ultralytics import YOLO
except ImportError:
    print("[ERROR] ultralytics not installed. Install with: pip install ultralytics")
    YOLO = None

import sqlite3
import time
from .database import DB_PATH_EVENTS, init_events_db

MODEL_PATH = os.path.join(os.path.dirname(__file__), "../yolov8n.pt")
if YOLO:
    model = YOLO(MODEL_PATH)
else:
    model = None

ALLOWED_CLASSES = {"person", "cell phone", "laptop", "tv", "hand", "finger", "helmet", "cap"}
init_events_db()  # Ensure DB is initialized

def log_detection(camera_id, label, confidence):
    try:
        conn = sqlite3.connect(DB_PATH_EVENTS)
        cur = conn.cursor()
        cur.execute("INSERT INTO detections (camera_id, label, confidence, timestamp) VALUES (?, ?, ?, ?)", (camera_id, label, confidence, time.time()))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[ERROR] Failed to log detection: {e}")

def run_yolo_detection(frame, camera_id=None, conf_threshold=0.5):
    if not model:
        return frame, []
    try:
        results = model(frame, stream=True, conf=conf_threshold)
        detections = []
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                label = model.names[class_id]
                confidence = float(box.conf[0])
                if label not in ALLOWED_CLASSES:
                    continue
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{label} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                if camera_id:
                    log_detection(camera_id, label, confidence)
                detections.append({"label": label, "confidence": confidence, "bbox": [x1, y1, x2, y2]})
        return frame, detections
    except Exception as e:
        print(f"[ERROR] YOLO detection failed: {e}")
        return frame, []