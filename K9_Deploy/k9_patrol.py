import cv2
import time
import os
import requests
from ultralytics import YOLO

# --- 🔐 TELEGRAM KEYS (PASTE YOURS HERE) ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")  
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")   

# --- CONFIG ---
SLEEP_LIMIT_MINUTES = 0.5
CONF_THRESHOLD = 0.4

# --- SETUP ---
project_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(project_dir, "best.engine")

print(f"🚀 Loading K9 Engine from: {model_path}")
model = YOLO(model_path, task='detect') 

def send_telegram_alert(duration_sec):
    msg = f"🚨 K9 ALERT: Dog has been lying down for {duration_sec:.0f} seconds!"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg}, timeout=5)
        print("✅ Telegram Sent!")
    except Exception as e:
        print(f"⚠️ Telegram Failed: {e}")

def open_camera():
    print("📸 Initializing Camera...")
    
    # REMOVED 'sensor-mode=2' (Letting it auto-negotiate like your terminal command)
    gst_pipeline = (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), width=(int)1920, height=(int)1080, format=(string)NV12, framerate=(fraction)30/1 ! "
        "nvvidconv ! "
        "video/x-raw, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink drop=1"
    )
    
    cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)
    
    if not cap.isOpened():
        print("❌ Failed to open GStreamer pipeline.")
        return None

    # --- THE WARMUP CHECK ---
    # We read 1 frame to ensure the camera is ACTUALLY running.
    print("🔍 Warming up camera sensor...")
    for i in range(5):
        ret, frame = cap.read()
        if ret:
            print("✅ Camera is LIVE and Flowing!")
            return cap
        time.sleep(0.5)
        
    print("❌ Camera opened, but NO VIDEO detected. (Restart nvargus-daemon)")
    return None

def main():
    cap = open_camera()
    if cap is None: return 

    global lying_start_time, alert_triggered
    lying_start_time = None
    alert_triggered = False
    
    print("🐕 K9 Guardian ACTIVE. Press 'Q' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret: 
            print("❌ Video stream lost.")
            break

        frame_small = cv2.resize(frame, (640, 360))
        results = model.predict(frame_small, verbose=False, imgsz=640, half=True)
        
        current_status = "active"
        
        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                label = model.names[cls_id] if hasattr(model, 'names') else str(cls_id)
                conf = float(box.conf[0])
                if conf < CONF_THRESHOLD: continue

                if label.lower() == 'lying': 
                    current_status = 'lying'
                    color = (0, 0, 255)
                else:
                    color = (0, 255, 0)
                
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame_small, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame_small, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        if current_status == 'lying':
            if lying_start_time is None: lying_start_time = time.time()
            elapsed = time.time() - lying_start_time
            cv2.putText(frame_small, f"Lying: {elapsed:.1f}s", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            if (elapsed / 60) > SLEEP_LIMIT_MINUTES and not alert_triggered:
                print(f"🚨 ALERT TRIGGERED: {elapsed:.0f}s")
                send_telegram_alert(elapsed)
                alert_triggered = True
        else:
            lying_start_time = None
            alert_triggered = False

        cv2.imshow("K9 Guardian", frame_small)
        if cv2.waitKey(1) == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()