# Deployment Guide  
AI-ML Based Sign Language Translator Using Raspberry Pi

This document explains how to deploy and run the project on a Raspberry Pi.

---

## 1. System Requirements

- Raspberry Pi 4 (8GB recommended)
- Raspberry Pi OS (64-bit recommended)
- Python 3.9+
- Internet connection (for initial setup)
- ESP32 configured with provided firmware

---

## 2. Clone the Repository

git clone https://github.com/SaadiyaFarheen/AI_ML_SIGN_LANGUAGE_TRANSLATOR_USING_RASPBERRY_PI.git

cd ai-ml-sign-language-translator-using-raspberry-pi

---

## 3. Install Required Python Libraries

pip install -r requirements.txt

---

## 4. Enable Required Interfaces

Open Raspberry Pi Configuration:

sudo raspi-config

Enable:
- I2C
- SPI (if using MCP3008)
- Bluetooth

Reboot after enabling.

---

## 5. Set User Permissions

Add required groups:

sudo usermod -aG bluetooth pi
sudo usermod -aG dialout pi
sudo usermod -aG i2c pi

Reboot system:

sudo reboot

---

## 6. Copy Service Files

Move service files into systemd directory:

sudo cp system_services/rfcomm-glove.service /etc/systemd/system/
sudo cp system_services/gesture-glove.service /etc/systemd/system/

Reload systemd:

sudo systemctl daemon-reexec
sudo systemctl daemon-reload

Enable services:

sudo systemctl enable rfcomm-glove.service
sudo systemctl enable gesture-glove.service

---

## 7. Start Services

sudo systemctl start rfcomm-glove.service
sudo systemctl start gesture-glove.service

---

## 8. Check Service Status

sudo systemctl status gesture-glove.service

If running correctly, the system will:
- Bind Bluetooth RFCOMM
- Connect to ESP32
- Load ML model
- Display detected gesture on OLED

---

## 9. Logs & Debugging

View runtime logs:

journalctl -u gesture-glove.service -f

Common issues:
- Bluetooth not paired
- Wrong RFCOMM port
- Incorrect model path
- I2C not enabled

---

## 10. Auto-Start on Boot

Once enabled, the system will automatically:
- Bind RFCOMM
- Launch ML gesture translator
- Display output on OLED

No manual intervention required after boot.

---

## Deployment Architecture Summary

ESP32 → Bluetooth (RFCOMM) → Raspberry Pi → ML Model → OLED Output
