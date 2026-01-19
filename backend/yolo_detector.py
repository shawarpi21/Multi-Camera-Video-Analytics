import cv2
import time
import sqlite3
import os
from ultralytics import YOLO

ALLOWED_CLASSES = {"person", "car", "bus", "truck", "bike", "bicycle", "bag"}
CONF_THRESHOLD = 0.5
LOITER_TIME = 5  # seconds
ZONE = (0, 0, 640, 480)  # full camera for testing

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "events.db")
SNAPSHOT_DIR = os.path.join(BASE_DIR, "snapshots")
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

model = YOLO("yolov8s.pt")  # path to your YOLO model

object_tracker = {}  # obj_id -> first seen time
last_event_time = {}  # obj_id -> last event time

# Initialize DB
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            camera_id TEXT,
            timestamp TEXT,
            rule TEXT,
            object_type TEXT,
            confidence REAL,
            bbox TEXT,
            zone TEXT,
            snapshot_path TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()


def save_event(camera_id, rule, obj_type, confidence, bbox, frame):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    filename = f"{camera_id}_{int(time.time())}.jpg"
    snap_path = os.path.join(SNAPSHOT_DIR, filename)
  

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
INSERT INTO events
(camera_id, timestamp, rule, object_type, confidence, bbox, zone, snapshot_path)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (
    camera_id,
    ts,
    rule,
    obj_type,
    confidence,
    str(bbox),
    "Zone-A",
    None
))
    conn.commit()
    conn.close()

def run_camera(camera_name="Camera-1", source=0):
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print(f"❌ Cannot open camera: {camera_name}")
        return

    print(f"✅ Started {camera_name}")

    while True:
        ret, frame = cap.read()
        if not ret:
            time.sleep(1)
            continue

        results = model(frame)[0]

        # Draw zone rectangle
        cv2.rectangle(frame, (ZONE[0], ZONE[1]), (ZONE[2], ZONE[3]), (255, 255, 0), 2)

        now = time.time()

        for box, cls, conf in zip(results.boxes.xyxy, results.boxes.cls, results.boxes.conf):
            class_name = model.names[int(cls)].lower()
            if class_name not in ALLOWED_CLASSES or conf < CONF_THRESHOLD:
                continue

            x1, y1, x2, y2 = map(int, box)
            bbox = (x1, y1, x2, y2)

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{class_name} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Check zone overlap
            zx1, zy1, zx2, zy2 = ZONE
            ix1 = max(x1, zx1)
            iy1 = max(y1, zy1)
            ix2 = min(x2, zx2)
            iy2 = min(y2, zy2)
            iw = max(0, ix2 - ix1)
            ih = max(0, iy2 - iy1)
            bbox_area = (x2 - x1) * (y2 - y1)
            if bbox_area == 0:
                continue
            overlap_ratio = iw * ih / bbox_area

            if overlap_ratio > 0.1:
                obj_id = f"{class_name}_{x1}_{y1}_{x2}_{y2}"

                # Intrusion
                if obj_id not in last_event_time or now - last_event_time[obj_id] > 3:
                    save_event(camera_name, "Intrusion", class_name, float(conf), bbox, frame)
                    last_event_time[obj_id] = now
                    print(f"[EVENT] {class_name} - Intrusion saved for {camera_name}")

                # Loitering
                if obj_id not in object_tracker:
                    object_tracker[obj_id] = now
                elif now - object_tracker[obj_id] >= LOITER_TIME:
                    save_event(camera_name, "Loitering", class_name, float(conf), bbox, frame)
                    object_tracker[obj_id] = now + 999
                    print(f"[EVENT] {class_name} - Loitering saved for {camera_name}")

        cv2.imshow(camera_name, frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

