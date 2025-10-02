import tkinter as tk
import cv2
import time
import mysql.connector
import datetime
import os
import requests
import email.utils

# Database config (adjust to match your server)
db_config = {
    'host': '192.168.31.136',
    'user': 'root',
    'password': '',
    'database': 'attendance_db'
}

# Model file setup
SERVER_MODEL_URL = "http://192.168.31.136/attendance-project/web/public/trained_model.yml"
LOCAL_MODEL = "trained_model.yml"

def update_model():
    """Check if server's model is newer and download it if necessary."""
    try:
        r = requests.head(SERVER_MODEL_URL, timeout=5)
        if r.status_code != 200:
            print("⚠️ Could not check model on server")
            return

        server_last_modified = r.headers.get("Last-Modified")
        if not server_last_modified:
            print("⚠️ No Last-Modified header from server, skipping check")
            return

        server_ts = time.mktime(email.utils.parsedate(server_last_modified))
        local_ts = os.path.getmtime(LOCAL_MODEL) if os.path.exists(LOCAL_MODEL) else 0

        if server_ts > local_ts:  # Server file is newer
            print("⬇️ Downloading new model from server...")
            r = requests.get(SERVER_MODEL_URL, timeout=10)
            with open(LOCAL_MODEL, "wb") as f:
                f.write(r.content)
            print("✅ Model updated.")
        else:
            print("ℹ️ Local model is up to date.")
    except Exception as e:
        print("⚠️ Error updating model:", e)

def log_attendance(student_id, subject="General"):
    """Insert attendance record into MySQL directly"""
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

def start_recognition():
    btn.pack_forget()  # hide button
    status_label.config(text="📷 Scanning... Please look at the camera")
    root.update()

    # Always check for latest model before recognition
    update_model()

    # Initialize recognizer + cascade
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    try:
        recognizer.read(LOCAL_MODEL)
    except Exception as e:
        status_label.config(text="⚠️ No trained model found. Please train first.")
        root.after(3000, show_button)
        return

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    cap = cv2.VideoCapture(0)
    recognized = False
    start_time = time.time()

    while time.time() - start_time < 10:  # 10 sec timeout
        ret, frame = cap.read()
        if not ret:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            roi = gray[y:y+h, x:x+w]
            roi = cv2.resize(roi, (200, 200))
            id_, conf = recognizer.predict(roi)

            if conf < 70:  # LBPH confidence threshold
                recognized = True
                if log_attendance(str(id_)):
                    status_label.config(text="✅ Attendance Recorded")
                else:
                    status_label.config(text="⚠️ DB Error Saving Attendance")
                break

        if recognized:
            break

    cap.release()
    if not recognized:
        status_label.config(text="❌ No Face Detected")

    # After 3s go back to button
    root.after(3000, show_button)

def show_button():
    status_label.config(text="")
    btn.pack(pady=50)

# Tkinter UI
root = tk.Tk()
root.attributes("-fullscreen", True)  # fullscreen touch
root.config(bg="white")

status_label = tk.Label(root, text="", font=("Arial", 28), bg="white")
status_label.pack(pady=20)

btn = tk.Button(root, text="📷 Tap to Get Attendance",
                font=("Arial", 36), bg="#007bff", fg="white",
                width=20, height=3,
                command=start_recognition)
btn.pack(pady=50)

root.mainloop()
