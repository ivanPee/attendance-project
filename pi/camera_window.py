import cv2

def run_camera():
    cap = cv2.VideoCapture("libcamerasrc ! videoconvert ! appsink", cv2.CAP_GSTREAMER)

    if not cap.isOpened():
        print("⚠️ Cannot open camera")
        return

    print("ℹ️ Press 'q' to exit camera preview")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Failed to grab frame")
            break

        cv2.imshow("Camera Preview", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_camera()
