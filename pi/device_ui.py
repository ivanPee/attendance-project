import tkinter as tk
import cv2
import time
import mysql.connector
import datetime

# Database config (adjust to match your server)
db_config = {
    'host': '192.168.1.13',
    'user': 'root',
    'password': '',
    'database': 'attendance_db'
}

# Initialize recognizer + cascade
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trained_model.yml")   # trained model path
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

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
