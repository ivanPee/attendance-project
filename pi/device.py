import tkinter as tk
import subprocess
import time
import requests
import email.utils
import os

# -----------------------------
# Database & Model (optional)
# -----------------------------
SERVER_MODEL_URL = "http://192.168.1.4/attendance-project/web/public/trained_model.yml"
LOCAL_MODEL = "trained_model.yml"

def update_model():
    """Download the model if newer on server"""
    try:
        r = requests.head(SERVER_MODEL_URL, timeout=5)
        if r.status_code != 200:
            print("⚠️ Server responded with", r.status_code)
            return

        server_last_modified = r.headers.get("Last-Modified")
        if server_last_modified:
            server_ts = time.mktime(email.utils.parsedate(server_last_modified))
            local_ts = os.path.getmtime(LOCAL_MODEL) if os.path.exists(LOCAL_MODEL) else 0
            if server_ts <= local_ts:
                print("ℹ️ Local model up to date")
                return

        print("⬇️ Downloading new model...")
        r = requests.get(SERVER_MODEL_URL, timeout=10)
        with open(LOCAL_MODEL, "wb") as f:
            f.write(r.content)
        print("✅ Model updated")
    except Exception as e:
        print("⚠️ Model update error:", e)

# -----------------------------
# Camera Preview
# -----------------------------
def start_recognition():
    """Open camera preview using rpicam-hello in a separate window"""
    btn.pack_forget()
    status_label.config(text="📷 Opening camera preview...")
    root.update()

    # Update model (optional)
    update_model()

    # Launch rpicam-hello preview
    subprocess.Popen([
        "rpicam-hello",
        "--qt-preview"
    ])

    # Restore the button after delay (so user can tap again)
    root.after(2000, show_button)

def show_button():
    status_label.config(text="")
    btn.pack(pady=50)

# -----------------------------
# Tkinter UI
# -----------------------------
root = tk.Tk()
root.attributes("-fullscreen", True)
root.config(bg="white")

# Status label
status_label = tk.Label(root, text="", font=("Arial", 28), bg="white")
status_label.pack(pady=20)

# Button to start recognition / camera
btn = tk.Button(
    root, text="📷 Tap to Get Attendance",
    font=("Arial", 36), bg="#007bff", fg="white",
    width=20, height=3,
    command=start_recognition
)
btn.pack(pady=50)

root.mainloop()
