import cv2
import time
from PIL import Image  # optional if you need image processing
import mysql.connector
import datetime

# Database config
db_config = {
    'host': '192.168.1.4',
    'user': 'root',
    'password': '',
    'database': 'attendance_db'
}

LOCAL_MODEL = "trained_model.yml"

def run_camera():
    # Load recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(LOCAL_MODEL)

    face_cascade = cv2.CascadeClassifier(
        "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
    )

    # Try using 0 or GStreamer pipeline
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Camera failed to open")
        return

    cv2.namedWindow("Camera Preview", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Camera Preview", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    start_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            roi = gray[y:y+h, x:x+w]
            roi = cv2.resize(roi, (200, 200))
            id_, conf = recognizer.predict(roi)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
            if conf < 70:
                # Log attendance
                try:
                    conn = mysql.connector.connect(**db_config)
                    cursor = conn.cursor()
                    now = datetime.datetime.now()
                    cursor.execute(
                        "INSERT INTO attendance (student_id, subject, timestamp, status) VALUES (%s,%s,%s,%s)",
                        (str(id_), "General", now, "present")
                    )
                    conn.commit()
                    cursor.close()
                    conn.close()
                    print(f"✅ Attendance recorded for {id_}")
                except Exception as e:
                    print("⚠️ DB error:", e)

        # Show frame in OpenCV window
        cv2.imshow("Camera Preview", frame)

        # Exit after 10 seconds or on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q') or (time.time() - start_time > 10):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_camera()
