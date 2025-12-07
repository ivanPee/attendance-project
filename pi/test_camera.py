import tkinter as tk
from PIL import Image, ImageTk
import cv2

# -----------------------------
# Configuration
# -----------------------------
CAMERA_ID = 1  # /dev/video1 for your USB webcam
PREVIEW_WIDTH = 640
PREVIEW_HEIGHT = 480
FPS = 30

# -----------------------------
# Tkinter window
# -----------------------------
root = tk.Tk()
root.title("Camera Preview")
root.attributes("-fullscreen", True)
root.config(bg="black")

label = tk.Label(root, bg="black")
label.pack(fill="both", expand=True)

# -----------------------------
# OpenCV capture
# -----------------------------
cap = cv2.VideoCapture(CAMERA_ID)
if not cap.isOpened():
    print("❌ Could not open camera")
    exit()

def update_frame():
    ret, frame = cap.read()
    if ret:
        # Convert BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Resize to fit the preview area
        frame = cv2.resize(frame, (PREVIEW_WIDTH, PREVIEW_HEIGHT))

        # Convert to Tkinter Image
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)

        label.imgtk = imgtk
        label.configure(image=imgtk)

    # Schedule next frame
    label.after(int(1000/FPS), update_frame)

# Start updating frames
update_frame()

# Close camera on exit
def on_close():
    cap.release()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
