import tkinter as tk
from PIL import Image, ImageTk
import cv2
import time
import os
import requests
import email.utils
import datetime
import mysql.connector

# -----------------------------
# Database & Model Config
# -----------------------------
db_config = {
    'host': '192.168.1.5',
    'user': 'pi_user',
    'password': 'your_password',
    'database': 'attendance_db'
}

SERVER_MODEL_URL = "http://192.168.1.5/attendance-project/web/public/trained_model.yml"
LOCAL_MODEL = "trained_model.yml"

CAMERA_ID = 1           # USB webcam
PREVIEW_WIDTH = 320
PREVIEW_HEIGHT = 240
FPS = 30

# -----------------------------
# Functions
# -----------------------------
def update_model():
    """Download model if server version is newer"""
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

def log_attendance(student_id, subject="General"):
    """Insert attendance record into MySQL"""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        now = datetime.datetime.now()
        cursor.execute("""
            INSERT INTO attendance (student_id, subject, timestamp, status)
            VALUES (%s, %s, %s, %s)
        """, (student_id, subject, now, "present"))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print("DB error:", e)
        return False

# -----------------------------
# Recognition Flow
# -----------------------------
def start_recognition():
    btn.pack_forget()
    status_label.config(text="📷 Scanning... Please look at the camera")
    root.update()

    update_model()

    # Load face recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    try:
        recognizer.read(LOCAL_MODEL)
    except:
        status_label.config(text="⚠️ No trained model found. Please train first.")
        root.after(3000, show_button)
        return

    # Use system Haar cascade path
    # Load the Haar cascade from the local project folder
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


    cap = cv2.VideoCapture(CAMERA_ID, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, PREVIEW_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, PREVIEW_HEIGHT)

    start_time = time.time()
    recognized = False

    def update_frame():
        nonlocal recognized
        ret, frame = cap.read()
        if not ret:
            root.after(30, update_frame)
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            roi = gray[y:y+h, x:x+w]
            roi = cv2.resize(roi, (200, 200))
            id_, conf = recognizer.predict(roi)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

            if conf < 70:
                recognized = True
                if log_attendance(str(id_)):
                    status_label.config(text="✅ Attendance Recorded")
                else:
                    status_label.config(text="⚠️ DB Error Saving Attendance")
                cap.release()
                root.after(3000, show_button)
                return

        # Convert to Tkinter Image
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

        if time.time() - start_time < 10 and not recognized:
            root.after(30, update_frame)
        else:
            if not recognized:
                status_label.config(text="❌ No Face Detected")
                cap.release()
                root.after(3000, show_button)

    update_frame()

def show_button():
    status_label.config(text="")
    video_label.config(image="")
    btn.pack(pady=50)

# -----------------------------
# Tkinter UI
# -----------------------------
root = tk.Tk()
root.attributes("-fullscreen", True)
root.config(bg="white")

status_label = tk.Label(root, text="", font=("Arial", 28), bg="white")
status_label.pack(pady=20)

video_label = tk.Label(root, bg="black")
video_label.pack(pady=10)

btn = tk.Button(root, text="📷 Tap to Get Attendance",
                font=("Arial", 36), bg="#007bff", fg="white",
                width=20, height=3,
                command=start_recognition)
btn.pack(pady=50)

root.mainloop()
