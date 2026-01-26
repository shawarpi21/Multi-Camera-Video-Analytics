import threading
import cv2
import os
from .yolo_detector import run_yolo_detection

SNAPSHOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "snapshots")
os.makedirs(SNAPSHOTS_DIR, exist_ok=True)

active_threads = {}

def camera_worker(camera_id, source, stop_event):
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print(f"[ERROR] Camera {camera_id} could not be opened")
        return
    print(f"[INFO] Camera {camera_id} started")
    frame_count = 0
    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            print(f"[WARNING] Failed to read frame from camera {camera_id}")
            break
        processed_frame, detections = run_yolo_detection(frame, camera_id)
        snapshot_path = os.path.join(SNAPSHOTS_DIR, f"camera_{camera_id}_frame_{frame_count}.jpg")
        cv2.imwrite(snapshot_path, processed_frame)
        frame_count += 1
        stop_event.wait(0.1)
    cap.release()
    print(f"[INFO] Camera {camera_id} stopped")

def start_camera(camera_id, source):
    stop_event = threading.Event()
    thread = threading.Thread(target=camera_worker, args=(camera_id, source, stop_event), daemon=True)
    thread.start()
    active_threads[camera_id] = (thread, stop_event)
    return camera_id

def stop_camera(camera_id):
    if camera_id in active_threads:
        _, stop_event = active_threads[camera_id]
        stop_event.set()
        del active_threads[camera_id]