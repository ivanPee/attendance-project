import cv2
from PIL import Image, ImageTk
import tkinter as tk

def run_camera():
    # Typical 3.5" LCD resolution
    LCD_WIDTH = 480
    LCD_HEIGHT = 320

    win = tk.Tk()
    win.title("Camera Window")
    win.configure(bg="black")
    
    # Set minimum window size to LCD resolution
    win.minsize(LCD_WIDTH, LCD_HEIGHT)
    win.geometry(f"{LCD_WIDTH}x{LCD_HEIGHT}")

    label = tk.Label(win, bg="black")
    label.pack(fill="both", expand=True)

    # Use the correct camera source for Raspberry Pi Camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("⚠️ Failed to open camera")
        return

    def update():
        ret, frame = cap.read()
        if ret:
            # Resize frame to fit the window while maintaining aspect ratio
            frame_height, frame_width = frame.shape[:2]
            scale_w = LCD_WIDTH / frame_width
            scale_h = LCD_HEIGHT / frame_height
            scale = min(scale_w, scale_h)
            new_w = int(frame_width * scale)
            new_h = int(frame_height * scale)
            frame_resized = cv2.resize(frame, (new_w, new_h))

            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            label.imgtk = imgtk
            label.configure(image=imgtk)

        label.after(30, update)  # ~30 FPS

    update()
    win.mainloop()
    cap.release()


if __name__ == "__main__":
    run_camera()
