# Multi-Camera-Video-Analytics
A modular system for real-time object detection across multiple video streams using modern computer vision models.

The application processes live camera feeds, detects predefined objects on each frame, and exposes results through a web-based dashboard. The system is designed to prioritize low latency, simplicity, and extensibility.

Problem Statement-

Traditional video surveillance requires continuous manual monitoring, which does not scale with the number of camera feeds and often leads to missed events. Existing solutions are either expensive, closed-source, or difficult to customize.

Solution Overview-

This project provides an automated video analytics pipeline that:

Captures frames from multiple camera sources

Runs real-time object detection on each stream

Logs detection events for later inspection

Exposes live feeds and historical data through a simple web interface

The system reduces manual effort while remaining lightweight and easy to extend.

Key Features
Multi-Camera Stream Handling

Supports multiple simultaneous camera inputs

Works with local webcams and IP camera streams

Each camera is processed independently to avoid blocking

Real-Time Object Detection

Uses YOLOv8 for fast and accurate detection

Detects people, mobile phones, laptops, helmets, and other configurable classes

Model can be replaced or fine-tuned without changing the rest of the system

Web-Based Dashboard-

Displays live camera feeds in the browser

Allows starting and stopping individual camera streams

Shows detection logs with timestamps and object labels

Authentication and Security

Dashboard access is protected by user authentication

Passwords are stored using secure hashing

Prevents unauthorized access to camera feeds and logs

Event Logging and Persistence

Detection events are automatically stored in a database

Each record includes detected object type, time, and source camera

Enables post-analysis and audit of historical activity

Snapshot Capture-

Saves image snapshots when detections occur

Allows quick visual verification of logged events

Useful for reporting or later review

Extensibility-

New camera sources can be added through configuration

Detection classes can be modified with minimal code changes

Designed to support future alerting and analytics features

System Architecture

Video streams are captured using OpenCV

Frames are passed to a YOLO-based detection pipeline

Detection results are processed and persisted in SQLite

FastAPI handles backend routing and request handling

Jinja2 renders server-side HTML views

The architecture is intentionally simple to keep runtime overhead low and debugging straightforward.

Technology Stack-
Backend

Python – Core language for application logic

FastAPI – Backend framework for APIs and server-side rendering

Uvicorn – ASGI server for running the application

Ultralytics YOLOv8 – Real-time object detection model

OpenCV – Video capture and frame manipulation

SQLite – Lightweight storage for users and events

Passlib – Secure password hashing

Jinja2 – Template engine for HTML views

Frontend-

HTML, CSS, JavaScript – Lightweight user interface

Minimal client-side logic to reduce complexity

Tooling-

Python virtual environment for dependency isolation

Pre-trained YOLO models (e.g. yolov8n.pt)

Setup and Installation
Requirements

Python 3.8 or higher

Installation Steps
git clone https://github.com/yourusername/multi-camera-video-analysis.git
cd multi-camera-video-analysis
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt


Ensure the YOLO model file (yolov8n.pt) is present in the project root.

Running the Application
python main.py


The application will be available at:

http://127.0.0.1:8000

Configuration-

Camera sources can be configured in backend/config.py

Detection logic and classes can be updated in backend/yolo_detector.py

Database files are created automatically at runtime

Use Cases-

Small to medium-scale security monitoring

Retail and workplace surveillance

Academic projects and computer vision experiments

Prototyping real-time AI systems

Future Work -

Asynchronous processing for higher throughput

Alerting mechanisms (email or messaging services)

Role-based access control

Support for additional detection models
