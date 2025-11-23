import cv2
from PIL import Image, ImageTk
import tkinter as tk
import time

def run_camera():
    # Create a separate Tkinter window for preview
    win = tk.Tk()
    win.attributes("-fullscreen", True)
    win.title("Camera Preview")
    win.configure(bg="black")

    label = tk.Label(win, bg="black")
    label.pack(fill="both", expand=True)

    # Use Raspberry Pi camera with GStreamer
    cap = cv2.VideoCapture("libcamerasrc ! videoconvert ! appsink", cv2.CAP_GSTREAMER)

    # Load face cascade manually
    face_cascade = cv2.CascadeClassifier(
        "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
    )

    def update():
        ret, frame = cap.read()
        if ret:
            # Convert to RGB for PIL
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect faces
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame_rgb, (x, y), (x+w, y+h), (0, 255, 0), 2)

            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            label.imgtk = imgtk
            label.configure(image=imgtk)
        else:
            print("⚠️ Failed to read frame from camera")

        # Schedule next frame
        label.after(10, update)

    update()
    win.mainloop()
    cap.release()

if __name__ == "__main__":
    run_camera()
