import cv2
from PIL import Image, ImageTk
import tkinter as tk

def run_camera():
    win = tk.Tk()
    win.attributes("-fullscreen", True)
    win.title("Camera Window")
    win.configure(bg="black")

    label = tk.Label(win, bg="black")
    label.pack(fill="both", expand=True)

    cap = cv2.VideoCapture("libcamerasrc ! videoconvert ! appsink", cv2.CAP_GSTREAMER)

    def update():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            label.imgtk = imgtk
            label.configure(image=imgtk)
        label.after(10, update)

    update()
    win.mainloop()
    cap.release()

run_camera()
