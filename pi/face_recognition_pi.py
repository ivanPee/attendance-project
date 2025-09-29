"""
Simple Raspberry Pi client that uses Haar cascade + LBPH recognizer from training images
and calls the web API to log attendance.


This is a skeleton — adapt to your local trained model and data layout from the original repo.
"""
import cv2
import time
import requests


API_URL = 'https://your-server.example.com/api/log_attendance.php'
API_TOKEN = 'REPLACE_WITH_SECURE_TOKEN'


# Load pre-trained LBPH model (from training script) - path depends on your training
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trained_model.yml') # update path as needed
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


cap = cv2.VideoCapture(0)
last_logged = {}
LOG_COOLDOWN = 30 # seconds between logging same student to avoid duplicates
SUBJECT = 'General'


def log_attendance(student_id, subject=SUBJECT):
    headers = {'Authorization': f'Bearer {API_TOKEN}', 'Content-Type': 'application/json'}
    payload = {'student_id': student_id, 'subject': subject}
    try:
        r = requests.post(API_URL, json=payload, headers=headers, timeout=5)
        if r.status_code == 200:
            print('Logged', student_id)
            return True
        else:
            print('API error', r.status_code, r.text)
            return False
    except Exception as e:
        print('Request failed', e)
        return False


while True:
    ret, frame = cap.read()
    if not ret:
        time.sleep(0.5)
        continue
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 5)
    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        id