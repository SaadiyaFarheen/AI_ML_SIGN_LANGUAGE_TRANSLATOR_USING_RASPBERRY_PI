# AI-ML Based Sign Language Translator Using Raspberry Pi

A real-time AI-powered smart glove system that translates hand gestures into readable text using Machine Learning and Embedded Systems.

---

## Project Overview

This project presents a wearable AI-powered sign language translator built using Raspberry Pi and ESP32. The system captures finger bending and motion data through flex sensors and an MPU6050 sensor, processes it using a trained Machine Learning model, and displays recognized gestures in real time on an OLED screen.

The solution is portable, lighting-independent, and optimized for real-time performance.

---

## System Architecture

ESP32 (Sensor Node)  
→ Bluetooth RFCOMM Communication  
→ Raspberry Pi (Processing Unit)  
→ Machine Learning Model (Random Forest)  
→ OLED Display (Output)

---

## Key Features

- Real-time gesture recognition
- AI/ML-based classification (Random Forest)
- Bluetooth-based wireless communication
- Sliding window prediction smoothing
- Automatic boot execution using systemd services
- OLED live display output
- Dataset cleaning and balancing pipeline
- Confidence-based filtering for stable predictions

---

## Hardware Components

- Raspberry Pi 4 (8GB)
- ESP32 Microcontroller
- 5 Flex Sensors
- MPU6050 (Accelerometer + Gyroscope)
- MCP3008 ADC
- 128x64 OLED Display
- TP4056 Battery Charging Module

---

## Software & Technologies Used

- Python
- Arduino IDE
- Scikit-learn
- Pandas & NumPy
- Joblib
- PySerial
- Adafruit SSD1306 Library
- Linux systemd services
- Bluetooth RFCOMM

---

## Machine Learning Pipeline

1. Live sensor data collection
2. CSV dataset creation
3. Data cleaning and smoothing
4. Feature scaling using StandardScaler
5. Stratified train-test split
6. Random Forest model training
7. Model evaluation and export (.pkl)
8. Real-time deployment on Raspberry Pi

---

## Model Performance

- Accuracy: ~99%
- Balanced dataset across gesture classes
- High precision and recall
- Stable predictions using sliding window buffering

---

## Deployment

The system supports automatic startup using Linux systemd services.  
Upon boot:

- RFCOMM binds automatically
- Bluetooth connects to ESP32
- ML model loads
- OLED initializes
- Gesture detection begins

See `DEPLOYMENT.md` for full setup instructions.

---

## Applications

- Assistive communication systems
- Human-computer interaction
- IoT-based wearable interfaces
- Embedded AI systems

---

## Future Enhancements

- Text-to-Speech output
- Deep Learning-based gesture recognition
- Multi-user adaptation
- Mobile application integration
- Cloud logging and analytics

---

## 👥 Authors (Group 7)

* Saadiya Farheen
* Swayam Das
* S. Jayant Kumar
* Smruti Saurav Mishra
* Anubhab Patra
* Veetesh Sinha

---
