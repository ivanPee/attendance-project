import tkinter as tk
from PIL import Image, ImageTk
import cv2

CAMERA_ID = 1
PREVIEW_WIDTH = 320
PREVIEW_HEIGHT = 240
FPS = 30

def run_camera():
    root = tk.Tk()
    root.title("Camera Window")
    root.attributes("-fullscreen", False)
    root.config(bg="black")

    label = tk.Label(root, bg="black")
    label.pack(fill="both", expand=True)

    cap = cv2.VideoCapture(CAMERA_ID, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, PREVIEW_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, PREVIEW_HEIGHT)

    def update():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (PREVIEW_WIDTH, PREVIEW_HEIGHT))
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            label.imgtk = imgtk
            label.configure(image=imgtk)
        label.after(int(1000/FPS), update)

    update()

    def on_close():
        cap.release()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

if __name__ == "__main__":
    run_camera()
