# ece5831-2025-final-project

## K9 Guardian: In-Vehicle Canine Safety System 🐕🚔

**Real-Time Behavior Analysis for Police K9 Units using Edge AI**

### 📂 Project Resources
* **📺 [Pre-recorded Presentation Video](https://www.youtube.com/watch?v=KbysFqdEZc8&feature=youtu.be)**
* **📊 [Presentation Slides](https://docs.google.com/presentation/d/1WT0Pa9GUNRm10mRHwzGxZuGlrJIRh856/edit?usp=drive_link&ouid=104712273097745265499&rtpof=true&sd=true)**
* **📄 [Full Technical Report](https://drive.google.com/file/d/11HKpiK0SlTDEw-ey3vPgwS5oCZF_vmtK/view?usp=sharing)**
* **💾 [Dataset](https://drive.google.com/drive/folders/1QIxRnhG8TYsU18maZIQPwi6azJo62yi9?usp=sharing)**
* **▶️ [Live Demo Video](INSERT_DEMO_LINK_HERE)**

---

## 📝 Abstract
Police K9 units face life-threatening risks from vehicular heatstroke, often caused by HVAC failures while the handler is away. Existing sensors only monitor temperature, failing to detect physiological distress (e.g., seizures, bloat, or agitation) in a cool cabin.

**K9 Guardian** is an autonomous, edge-native computer vision system designed to bridge this "semantic gap." By deploying **YOLO11** on an **NVIDIA Jetson Orin Nano**, the system analyzes canine posture in real-time, functioning as a fail-safe redundancy that operates independently of the vehicle's internal systems.

## 🚀 Key Features
* **Edge-Native Processing:** Runs locally on NVIDIA Jetson Orin Nano; no cloud dependency required.
* **Real-Time Detection:** Classifies postural states (e.g., "Agitated" vs. "Lying/Collapsed") with >30 FPS.
* **IoT Smart Alerts:** Sends rich-media alerts (photos + timestamp) to the handler’s smartphone via Telegram.
* **False Alarm Reduction:** Implements a Temporal Logic Engine (Finite State Machine) to filter out momentary occlusions.

## 🛠️ Tech Stack & Hardware

### Hardware
* **Compute:** NVIDIA Jetson Orin Nano (8GB)
* **Sensor:** Sony IMX219 (8MP) CSI-2 Camera
* **Connectivity:** LTE Modem for IoT Dispatch

### Software
* **Model Architecture:** Ultralytics YOLO11-Nano
* **Inference Engine:** NVIDIA TensorRT (FP16 Optimization)
* **Pipeline:** DeepStream / GStreamer
* **Alerting:** Telegram Bot API

## ⚙️ Methodology



[Image of System Architecture Diagram]


1.  **Data Acquisition:** Video is captured via the CSI sensor.
2.  **Inference:** Frames are processed by YOLO11n (optimized to TensorRT FP16) to detect the K9 and classify posture.
3.  **Logic Layer:** A Finite State Machine (FSM) tracks the duration of specific states.
    * *Critical Threshold:* If `State == "Lying"` for > 5 minutes, an alert is armed.
4.  **Notification:** An HTTPS POST request triggers a Telegram alert to the handler with an image of the dog for visual verification.

## 📊 Performance Results

We benchmarked the system in a constrained vehicle environment using the "15W MAXN" power mode.

| Metric | Result | Notes |
| :--- | :--- | :--- |
| **Throughput** | **80.6 FPS** | Using TensorRT FP16 |
| **Latency** | **33.0 ms** | End-to-end (Sensor to Logic) |
| **Accuracy (mAP)** | **0.95** | mAP@0.5 |
| **Power Draw** | **9.8 W** | Safe for vehicle auxiliary power |

## 📸 Demo
*(Optional: Add a GIF here of the detection system in action)*

## 👥 Contributors
* **[Your Name]** - *Lead Developer*
* Raghu Nallapati
* Sidharth Kalyan Ram

---