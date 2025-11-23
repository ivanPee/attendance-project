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

    # Use the correct camera source for Raspberry Pi Camera
    cap = cv2.VideoCapture(0)  # fallback to VideoCapture(0) works with libcamera

    if not cap.isOpened():
        print("⚠️ Failed to open camera")
        return

    def update():
        ret, frame = cap.read()
        if ret:
            # Resize to fit window if needed
            frame = cv2.resize(frame, (win.winfo_width(), win.winfo_height()))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            label.imgtk = imgtk
            label.configure(image=imgtk)
        label.after(30, update)  # ~30 FPS

    update()
    win.mainloop()
    cap.release()


if __name__ == "__main__":
    run_camera()
