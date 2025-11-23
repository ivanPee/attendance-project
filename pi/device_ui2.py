import tkinter as tk
import cv2
import time
import mysql.connector
import datetime
import os
import requests
import email.utils
import subprocess
from PIL import Image, ImageTk

# Database config
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'attendance_db'
}

SERVER_MODEL_URL = "http://localhost/attendance-project/web/public/trained_model.yml"
LOCAL_MODEL = "trained_model.yml"

def update_model():
    """Download model if newer on server."""
    try:
        r = requests.head(SERVER_MODEL_URL, timeout=5)
        if r.status_code != 200:
            print("⚠️ Server responded with", r.status_code)
            return

        server_last_modified = r.headers.get("Last-Modified")
        if server_last_modified:
            server_ts = time.mktime(email.utils.parsedate(server_last_modified))
            local_ts = os.path.getmtime(LOCAL_MODEL) if os.path.exists(LOCAL_MODEL) else 0
            if server_ts <= local_ts:
                print("ℹ️ Local model up to date")
                return

        print("⬇️ Downloading new model...")
        r = requests.get(SERVER_MODEL_URL, timeout=10)
        with open(LOCAL_MODEL, "wb") as f:
            f.write(r.content)
        print("✅ Model updated")
    except Exception as e:
        print("⚠️ Model update error:", e)

def start_recognition():
    """Opens a new fullscreen window for camera recognition."""
    btn.pack_forget()
    status_label.config(text="📷 Starting camera...")
    root.update()

    update_model()

    # Launch separate camera window
    subprocess.Popen([
        "python3",
        "/home/raspberrypi/attendance/attendance-project/pi/camera_window.py"
    ])

    # Restore button after delay
    root.after(2000, show_button)

def show_button():
    status_label.config(text="")
    btn.pack(pady=50)

# Tkinter UI
root = tk.Tk()
root.attributes("-fullscreen", True)
root.config(bg="white")

status_label = tk.Label(root, text="", font=("Arial", 28), bg="white")
status_label.pack(pady=20)

btn = tk.Button(root, text="📷 Tap to Get Attendance",
                font=("Arial", 36), bg="#007bff", fg="white",
                width=20, height=3,
                command=start_recognition)
btn.pack(pady=50)

root.mainloop()
