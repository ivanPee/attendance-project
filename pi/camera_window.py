import cv2
from PIL import Image, ImageTk
import tkinter as tk

# Target display size (adjust to your LCD)
DISPLAY_WIDTH = 320
DISPLAY_HEIGHT = 480

def run_camera():
    win = tk.Tk()
    win.attributes("-fullscreen", True)
    win.title("Camera Window")
    win.configure(bg="black")

    label = tk.Label(win, bg="black")
    label.pack(fill="both", expand=True)

    # Use V4L2 device (libcamera-friendly)
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

    # Set camera resolution lower to match small LCD
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    def update():
        ret, frame = cap.read()
        if ret and frame is not None:
            # Resize frame to LCD dimensions
            frame = cv2.resize(frame, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            label.imgtk = imgtk
            label.configure(image=imgtk)
        label.after(30, update)  # ~30 FPS

    update()
    win.mainloop()
    cap.release()

run_camera()
