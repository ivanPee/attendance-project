import tkinter as tk
from PIL import Image, ImageTk
import cv2

# -----------------------------
# Configuration
# -----------------------------
CAMERA_ID = 1  # USB webcam
PREVIEW_WIDTH = 320
PREVIEW_HEIGHT = 240
FPS = 30

# -----------------------------
# Tkinter window
# -----------------------------
root = tk.Tk()
root.title("Camera Preview")
root.attributes("-fullscreen", False)  # Windowed mode for debugging
root.config(bg="black")

label = tk.Label(root, bg="black")
label.pack(fill="both", expand=True)

# -----------------------------
# OpenCV capture
# -----------------------------
cap = cv2.VideoCapture(CAMERA_ID, cv2.CAP_V4L2)  # Use V4L2 backend explicitly
if not cap.isOpened():
    print("❌ Could not open camera")
    exit()

# Try to set low resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, PREVIEW_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, PREVIEW_HEIGHT)

def update_frame():
    ret, frame = cap.read()
    if ret:
        # Convert BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Resize to fit preview
        frame = cv2.resize(frame, (PREVIEW_WIDTH, PREVIEW_HEIGHT))

        # Convert to Tkinter image
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)

        label.imgtk = imgtk
        label.configure(image=imgtk)

    # Schedule next frame
    label.after(int(1000/FPS), update_frame)

update_frame()

# Close camera on exit
def on_close():
    cap.release()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
