#!/usr/bin/env python3
import time
import os
import subprocess
import serial
import joblib
import numpy as np
import pandas as pd
from collections import deque
import traceback

import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# ===============================
# CONFIGURATION (LOCKED)
# ===============================
PORT = "/dev/rfcomm0"
BAUD = 115200

MODEL_FILE = "/home/pi/gesture_model25.pkl"
SCALER_FILE = "/home/pi/scaler25.pkl"

WINDOW_SIZE = 5
CONFIDENCE_THRESHOLD = 0.55

FEATURES = [
    "flex1", "flex2", "flex3", "flex4", "flex5",
    "ax", "ay", "az",
    "gx", "gy", "gz"
]

# ===============================
# OLED INIT
# ===============================
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

try:
    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20
    )
except IOError:
    font = ImageFont.load_default()

def oled_text(msg):
    draw.rectangle((0, 0, oled.width, oled.height), fill=0)
    bbox = draw.textbbox((0, 0), msg, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((oled.width - w)//2, (oled.height - h)//2),
              msg, font=font, fill=255)
    oled.image(image)
    oled.show()

def fatal(msg):
    oled_text(msg)
    time.sleep(4)
    raise SystemExit(msg)

def ok(msg, t=0.8):
    oled_text(msg)
    time.sleep(t)

# ===============================
# BOOT SEQUENCE
# ===============================
oled_text("BOOTING")
time.sleep(1)
ok("OLED OK")

# Model load
oled_text("LOAD MODEL")
try:
    model = joblib.load(MODEL_FILE)
    scaler = joblib.load(SCALER_FILE)
    ok("MODEL OK")
except Exception:
    oled_text("MODEL FAIL")
    traceback.print_exc()
    time.sleep(5)
    raise

# Bluetooth ready
def wait_bt():
    oled_text("BT SERVICE")
    for _ in range(20):
        try:
            s = subprocess.check_output(
                ["systemctl", "is-active", "bluetooth"],
                stderr=subprocess.DEVNULL
            ).decode().strip()
            if s == "active":
                ok("BT ACTIVE")
                return
        except Exception:
            pass
        time.sleep(0.5)
    fatal("BT DEAD")

wait_bt()

# rfcomm device
def wait_rfcomm():
    oled_text("WAIT RFCOMM")
    for _ in range(30):
        if os.path.exists(PORT):
            ok("RFCOMM OK")
            return
        time.sleep(0.5)
    fatal("NO RFCOMM")

wait_rfcomm()

# ===============================
# SERIAL CONNECT
# ===============================
def connect_serial():
    oled_text("SERIAL OPEN")
    while True:
        try:
            ser = serial.Serial(PORT, BAUD, timeout=0.5)
            time.sleep(1)
            if ser.readline():
                ok("DATA FLOW")
                return ser
            ser.close()
            oled_text("NO DATA")
            time.sleep(1)
        except serial.SerialException:
            oled_text("SER ERR")
            time.sleep(1)

ser = connect_serial()

# ===============================
# MAIN LOOP
# ===============================
buffer = deque(maxlen=WINDOW_SIZE)
last_prediction = None
oled_text("RUNNING")

while True:
    try:
        line = ser.readline().decode(errors="ignore").strip()
        if not line:
            continue

        values = line.split(",")
        if len(values) != 11:
            continue

        frame = pd.DataFrame([values], columns=FEATURES, dtype=float)
        frame_scaled = scaler.transform(frame)

        probs = model.predict_proba(frame_scaled)[0]
        confidence = float(np.max(probs))

        if confidence < CONFIDENCE_THRESHOLD:
            continue

        pred = model.classes_[int(np.argmax(probs))]
        buffer.append(pred)

        final_pred = max(set(buffer), key=buffer.count)
        if final_pred != last_prediction:
            oled_text(final_pred)
            last_prediction = final_pred

    except serial.SerialException:
        oled_text("SER LOST")
        buffer.clear()
        last_prediction = None
        time.sleep(1)
        ser = connect_serial()

    except KeyboardInterrupt:
        oled.fill(0)
        oled.show()
        ser.close()
        break