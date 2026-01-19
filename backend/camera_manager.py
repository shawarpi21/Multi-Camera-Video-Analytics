import threading
from backend.yolo_detector import run_camera

CAMERA_SOURCES = {
    "Cam1": 0,  # Webcam
}

threads = []

def start_cameras():
    for cam_id, source in CAMERA_SOURCES.items():
        t = threading.Thread(
            target=run_camera,
            args=(cam_id, source),
            daemon=True
        )
        t.start()
        threads.append(t)

    print("✅ Cameras started")


