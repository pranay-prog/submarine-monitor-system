# 🌊 Secure Multi-Agent Underwater Environmental Monitoring System

A real-time underwater environmental monitoring system that combines IoT sensing, secure communication, multi-agent artificial intelligence, and anomaly detection to monitor critical underwater environmental conditions.

## 📌 Overview

This project deploys an underwater sensing node equipped with environmental sensors connected to an Arduino and ESP32. Sensor data is securely transmitted to a port station using LoRa communication and XChaCha20-Poly1305 authenticated encryption. At the receiver side, a multi-agent AI framework processes the incoming data, detects anomalies using Isolation Forest, evaluates system performance, and visualizes results through a real-time monitoring dashboard.

---

## 🚀 Features

* Real-time underwater environmental monitoring
* Secure LoRa communication
* XChaCha20-Poly1305 authenticated encryption
* Multi-Agent AI architecture
* Isolation Forest-based anomaly detection
* Continuous evaluation and validation
* Real-time dashboard visualization
* Alert generation for abnormal conditions
* Data integrity and replay attack protection

---

## 🛠 Hardware Components

### Underwater Submarine Node

* ESP32 Development Board
* Arduino Nano/Uno
* Dissolved Oxygen Sensor
* Pressure Sensor
* LoRa Transmitter Module
* Battery Power Supply

### Port Station

* LoRa Receiver Module
* ESP32 Gateway
* Central Processing Server

---

## 🏗 System Architecture

```text
Pressure Sensor
Dissolved Oxygen Sensor
        │
        ▼
     Arduino
        │
        ▼
      ESP32
        │
        ▼
XChaCha20-Poly1305 Encryption
        │
        ▼
   LoRa Transmission
        │
        ▼
   Port Receiver
        │
        ▼
────────────────────────────
 Multi-Agent AI Framework
────────────────────────────
        │
        ▼
Data Acquisition Agent
        │
        ▼
Data Validation Agent
        │
        ▼
Data Fusion Agent
        │
        ▼
Anomaly Detection Agent
(Isolation Forest)
        │
        ▼
Evaluation Agent
        │
        ▼
Alert & Dashboard Agent
```

---

## 🤖 Multi-Agent AI Framework

### Data Acquisition Agent

* Receives incoming LoRa packets
* Extracts environmental readings
* Stores time-stamped observations

### Data Validation Agent

* Detects corrupted packets
* Removes invalid readings
* Handles missing values

### Data Fusion Agent

* Synchronizes sensor streams
* Creates environmental feature vectors
* Maintains shared blackboard memory

### Anomaly Detection Agent

* Uses Isolation Forest
* Computes anomaly scores
* Classifies observations as Normal or Anomaly

### Evaluation Agent

Continuously evaluates:

* Task Success
* Tool Usage Quality
* Reasoning Coherence
* Cost-Performance Efficiency

### Alert & Dashboard Agent

* Updates dashboard
* Generates alerts
* Logs anomalies
* Sends notifications

---

## 🔒 Security Architecture

The communication layer uses XChaCha20-Poly1305 authenticated encryption to ensure:

### Confidentiality

Protects sensor data from unauthorized access.

### Integrity

Prevents modification of transmitted packets.

### Authentication

Verifies the origin of each packet.

### Replay Protection

Uses:

* Packet Counters
* Timestamps
* Unique Nonces

to prevent replay attacks.

---

## 📊 Data Processing Pipeline

1. Environmental data collection
2. Packet generation on ESP32
3. Secure encryption using XChaCha20-Poly1305
4. LoRa transmission to port station
5. Authentication and decryption
6. Data validation and filtering
7. Feature vector creation
8. Anomaly detection
9. Evaluation and scoring
10. Dashboard visualization and alerts

---

## 📈 Dashboard Features

### Environmental Monitoring

* Pressure
* Estimated Depth
* Dissolved Oxygen Levels
* Timestamp
* Communication Status

### AI Analytics

* Anomaly Score
* Confidence Score
* Current Status
* Historical Trends

### Multi-Agent Monitoring

* Agent Health Status
* Evaluation Scores
* Performance Metrics

### Security Monitoring

* Authentication Status
* Packet Verification Status
* Communication Health
* Rejected Packet Count

---

## 🎯 Output

For every monitoring cycle, the system generates:

* Pressure Reading
* Estimated Depth
* Dissolved Oxygen Concentration
* Anomaly Score
* Confidence Score
* Normal/Anomaly Classification
* Security Verification Status
* Evaluation Metrics

---

## 🧠 Machine Learning Model

### Isolation Forest

The anomaly detection engine uses Isolation Forest to identify abnormal environmental behavior.

Outputs:

* Binary Classification (Normal / Anomaly)
* Anomaly Score
* Confidence Score

The model supports continuous retraining and adaptation to changing underwater conditions.

---

## 📂 Project Structure

```text
final_implementation/
│
├── submarine_mas_dashboard_1.html
├── README.md
└── assets/
```

---

## 🔮 Future Enhancements

* Additional environmental sensors
* Underwater acoustic communication
* Edge AI deployment on ESP32
* Federated learning between multiple submarine nodes
* Predictive environmental forecasting
* Autonomous response agents

---

## 👨‍💻 Author

Pranay Jain, Arya Singh Vishen, Manya Sinha

Secure Multi-Agent Underwater Environmental Monitoring System using IoT, LoRa Communication, XChaCha20-Poly1305 Security, and Agentic AI.
