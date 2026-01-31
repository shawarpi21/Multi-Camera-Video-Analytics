# Multi-Camera-Video-Analytics
A real-time video analytics system that processes multiple camera streams and performs object detection using modern computer vision models.

The project focuses on building a practical surveillance pipeline that is easy to deploy, easy to extend, and efficient enough for continuous monitoring. It is designed as a clean, end-to-end system rather than a standalone model demo.

🧠 Problem -

Video surveillance systems often require constant human monitoring, which does not scale as the number of cameras increases. Important events can be missed, and many existing solutions are either proprietary, expensive, or difficult to adapt to specific requirements.

🛠 Solution -

This project automates video monitoring by combining real-time object detection with a lightweight web application.

The system:

Connects to multiple video sources such as webcams or IP cameras

Processes frames in real time using a YOLO-based detection pipeline

Identifies predefined objects and captures evidence at detection time

Stores structured event data for later review

Provides a web interface for live monitoring and historical inspection

⭐ Key Features -

Multi-camera support that allows simultaneous monitoring of several video streams

Real-time object detection using YOLOv8 with configurable detection classes

Web dashboard for viewing live feeds, managing cameras, and reviewing logs

Authentication and access control to protect camera feeds and data

Event logging with snapshots to enable post-event analysis

Configuration-driven design that makes the system easy to extend and maintain

🧩 Architecture -

Video streams are captured using OpenCV and processed frame by frame through a YOLO-based inference pipeline. Detection results are persisted in a lightweight SQLite database. The backend is implemented using FastAPI, which serves both API endpoints and server-rendered views through Jinja2.

The architecture is intentionally simple to minimize latency and keep the system easy to understand, debug, and extend.

⚙️ Tech Stack -

Backend: Python, FastAPI, Uvicorn, YOLOv8, OpenCV, SQLite
Frontend: HTML, CSS, JavaScript
Security & Templating: Passlib, Jinja2

🚀 Quick Start -
git clone https://github.com/yourusername/multi-camera-video-analysis.git
cd multi-camera-video-analysis
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py


Open http://127.0.0.1:8000 in your browser.

🔧 Configuration -

Camera sources can be updated in backend/config.py

Detection logic and classes can be modified in backend/yolo_detector.py

🎯 Use Cases -

This system is suitable for home or small-scale security setups, retail and office monitoring, academic computer vision projects, and prototyping real-time AI pipelines.
