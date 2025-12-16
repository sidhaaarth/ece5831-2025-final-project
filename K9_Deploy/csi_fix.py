import cv2

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1280,
    capture_height=720,
    display_width=640,
    display_height=480,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def main():
    print("📸 Attempting to open CSI Camera with 'Green Screen Fix' pipeline...")
    
    # 1. Get the magic string
    pipeline = gstreamer_pipeline(flip_method=0)
    print(f"Pipeline: {pipeline}")

    # 2. Open with GStreamer backend
    cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

    if not cap.isOpened():
        print("❌ Failed to open camera. Check ribbon cable connection!")
        return

    print("✅ Camera Opened! Press 'Q' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Lost frame")
            break

        cv2.imshow("CSI Camera Fix", frame)
        
        # Press Q to quit
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()