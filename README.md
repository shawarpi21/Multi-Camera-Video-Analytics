#  Multi-Camera Video Analytics System

A real-time video analytics platform that processes multiple camera streams and performs object detection using modern computer vision models.

This project is designed as an end-to-end system that combines computer vision, backend APIs, and system-level design. The focus is on building a deployable, extensible surveillance pipeline rather than a standalone model demo.

---

## 🧠 Problem Statement

Traditional video surveillance systems require continuous human monitoring, which does not scale as the number of cameras increases. Critical events can be missed, and many existing solutions are expensive, closed-source, or difficult to customize.

---

## 🛠️ Solution Overview

This system automates video monitoring by integrating real-time object detection with a lightweight backend and web interface.

The platform:
- Connects to multiple camera sources (webcams or IP cameras)
- Performs real-time object detection using a YOLO-based pipeline
- Logs detection events with timestamps
- Stores structured data for later inspection
- Provides a web dashboard for monitoring and control

---

## ⭐ Key Features

- **Multi-camera support** for concurrent video stream processing  
- **Real-time object detection** using YOLOv8  
- **FastAPI backend** for clean API design and scalability  
- **Authentication-protected dashboard**  
- **Event logging** with persistent storage (SQLite)  
- **Modular architecture** for easy extension and maintenance  

---

## 🏗️ Architecture & Design

- Video streams are captured using **OpenCV**
- Frames are processed through a **YOLOv8 inference pipeline**
- Detection events are stored in **SQLite** using SQLAlchemy
- Backend services are implemented with **FastAPI**
- Server-side rendering is handled using **Jinja2**

The architecture prioritizes **low latency**, **clarity**, and **ease of deployment**.

---

## 📊 Performance Snapshot

- Average inference latency: ~25–40 ms per frame (CPU)
- Throughput: ~15–25 FPS per camera (single stream)
- Tested with up to 3 concurrent camera feeds on a local machine

*(Performance varies by hardware and model size)*

---

## ⚙️ Tech Stack

**Backend**
- Python
- FastAPI
- Uvicorn
- OpenCV
- YOLOv8
- SQLAlchemy
- SQLite

**Frontend**
- HTML
- CSS
- Jinja2

**Security**
- Passlib (bcrypt)

---

## 🚀 Quick Start

```bash
git clone https://github.com/yourusername/multi-camera-video-analytics.git
cd multi-camera-video-analytics
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py


## 📊 Snapshot

![Signin Page](https://raw.githubusercontent.com/shawarpi21/Multi-Camera-Video-Analytics/99ab8ebc18cd53c51dd47814c7f7711f4fa29705/signin-page.png)





