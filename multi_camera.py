import sys
import os
from threading import Thread
# Add backend folder to path
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))
from yolo_detector import run_camera

# List of cameras
cameras = [
    {"name": "Cam1", "source": 0},  # default webcam
    # {"name": "Cam2", "source": "rtsp://username:password@camera_ip:554/stream"},
]

threads = []

for cam in cameras:
    t = Thread(target=run_camera, args=(cam["name"], cam["source"]))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
