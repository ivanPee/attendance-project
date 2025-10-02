import cv2
import numpy as np
import os

dataset_path = "uploads"
model_path = "../../pi/trained_model.yml"

recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

faces = []
ids = []

print("Starting training...")

for student_id in os.listdir(dataset_path):
    student_dir = os.path.join(dataset_path, student_id)
    if not os.path.isdir(student_dir):
        continue

    for img_name in os.listdir(student_dir):
        img_path = os.path.join(student_dir, img_name)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue

        detected = face_cascade.detectMultiScale(img, 1.2, 5)
        for (x, y, w, h) in detected:
            faces.append(img[y:y+h, x:x+w])
            try:
                ids.append(int(student_id))
            except:
                print(f"Skipped {student_id}, must be numeric.")

if len(faces) == 0:
    print("No faces found. Please upload student images first.")
else:
    recognizer.train(faces, np.array(ids))
    recognizer.save(model_path)
    print(f"Model trained and saved as {model_path}")
