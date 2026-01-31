# Multi-Camera-Video-Analytics
This project is a web-based system that analyzes video feeds from multiple cameras using advanced AI to detect objects like people, phones, and more.
Purpose: It's like having a smart security assistant that watches your cameras and alerts you to important events.
Use Cases: Perfect for home security, retail monitoring, or any setup needing automated video analysis.
Key Focus: Built for simplicity and scalability.
🚀 Tech Stack
Backend:
Python: Core language for logic and scripting.
FastAPI: For building a fast, modern web API.
Uvicorn: To run the web server efficiently.
Ultralytics YOLO: AI model for real-time object detection.
OpenCV: For video processing and frame handling.
SQLite: Lightweight database for storing user data and events.
Jinja2: For rendering dynamic web pages.
Passlib: For secure password hashing.
Frontend:
HTML, CSS, and JavaScript: Basic web technologies for a clean, responsive interface.
Font Awesome: For icons to enhance the UI.
Other Tools:
Virtual environment (venv): For isolated Python dependencies.
YOLOv8 models: Pre-trained AI for detection (e.g., yolov8n.pt).
Standard Python libraries: For file handling, threading, and logging.
Why This Stack?:
Open-source and easy to deploy.
Focuses on real-time performance.
No heavy frameworks—just reliable tools that work together.
✨ Features
Multi-Camera Support:
Connect and monitor multiple cameras (e.g., webcams or IP cameras) simultaneously.
AI-Powered Detection:
Uses YOLO AI to spot objects like people, cell phones, laptops, helmets, and more in real-time.
Web Dashboard:
A simple, GitHub-inspired interface to view feeds, start/stop cameras, and see detection logs.
Secure Login:
Password-protected access with hashed passwords for safety.
Event Logging:
Automatically saves detections to a database for review.
Snapshots:
Captures images of detected events for easy access.
Real-Time Alerts:
Basic notifications for detections (expandable for emails or SMS).
Scalable:
Easy to add more cameras or customize detection classes.
🛠 Installation
Prerequisites:
Python 3.8+ installed.
Step 1: Clone the Repository:
git clone https://github.com/yourusername/multi-camera-video-analysis.git
cd multi-camera-video-analysis
Step 2: Set Up a Virtual Environment:
python -m venv venv
venv\Scripts\activate # On Windows; use source venv/bin/activate on Mac/Linux
Step 3: Install Dependencies:
pip install -r requirements.txt
Step 4: Prepare the Database:
The app creates databases automatically.
Add a test user if needed (run in Python shell):
from passlib.hash import bcrypt
hashed_pw = bcrypt.hash("yourpassword")
import sqlite3
conn = sqlite3.connect("users.db")
cur = conn.cursor()
cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("testuser", hashed_pw))
conn.commit()
conn.close()
Step 5: Download YOLO Model (if not included):
Ensure yolov8n.pt is in the root folder (download from Ultralytics if missing).
🎯 Usage
Step 1: Start the App:
python main.py
Open http://127.0.0.1:8000 in your browser.
Step 2: Log In:
Use the test user (or create your own) to access the dashboard.
Step 3: Monitor Cameras:
View camera feeds, start/stop them, and check detection logs.
Detections are saved and displayed in real-time.
Step 4: Customize:
Edit backend/config.py to add more cameras.
Modify backend/yolo_detector.py to detect different objects.
