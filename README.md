# 🎙️ FMI-Codes-2026: AI Voice Recognition & Security Ecosystem

![Event](https://img.shields.io/badge/Event-FMI--Codes--2026-blueviolet?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Hackathon--MVP-green?style=for-the-badge)
![AI Model](https://img.shields.io/badge/AI--Model-Custom--Trained-orange?style=for-the-badge)
![Tech Stack](https://img.shields.io/badge/Stack-Python%20%7C%20React%20%7C%20React%20Native%20%7C%20Kotlin-blue?style=for-the-badge)

## 🌟 Overview
Developed during the **FMI Codes 2026** hackathon, this project is a multi-platform ecosystem designed to tackle modern challenges in voice security. 

**What makes us different?** Unlike standard solutions that use pre-made APIs, our core AI engine was **trained from scratch** using an extensive dataset of custom voice recordings to ensure high precision and specialized detection capabilities.

---

## 🏗️ Architecture & Tech Stack

Our solution features a centralized custom-trained AI backend serving multiple client applications:

### 📱 Mobile Applications
* **`CallGuard/` (React Native) – [Primary]**: Our main functional mobile application. It provides cross-platform protection, real-time call filtering, and a sleek UI.
* **`app/` (Native Kotlin)**: A secondary native implementation. A high-performance alternative for the Android ecosystem, finalized during the later stages of the sprint.

### 💻 Web & Infrastructure
* **`backend/` (Python & FastAPI)**: The heart of the project. It handles complex audio processing (supporting `wav8/16/23`) and runs our **custom-trained AI inference models**.
* **`frontend/` (React)**: A comprehensive web dashboard for monitoring voice analytics and visualizing real-time detection data.

---

## 🚀 Core Features
* **Custom AI Model (Trained from Scratch)**: Our model was built and trained using a large volume of unique voice recordings to achieve superior accuracy.
* **Dual-Mobile Implementation**: Experience the same security features across both React Native (Primary) and Native Kotlin environments.
* **Scalable Backend**: A FastAPI-driven architecture optimized for low-latency audio streaming.
* **Robust Error Handling**: Recently patched to resolve 500-series server errors and complex Gradle configuration conflicts.

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/Nikola0505stag/FMI-Codes-2026.git](https://github.com/Nikola0505stag/FMI-Codes-2026.git)
cd FMI-Codes-2026
```

### 2. Clone the Repository
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. Launch the Web Frontend (React)
```bash
cd frontend
npm install
npm start
```

### 4. Mobile Setup (CallGuard (React Native) )
```bash
cd CallGuard
npm install
npm react-native run-android
```
---

## 👥 The Team
Proudly developed by the **FMI-Codes-2026** contributors:
* **Team Members**: [Add Names Here]
* **Special Thanks**: To the FMI Codes 2026 mentors and organizers.

---
*Developed for educational purposes at Sofia University, Faculty of Mathematics and Informatics (FMI).*

