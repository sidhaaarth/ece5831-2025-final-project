import os
from ultralytics import YOLO
import torch

def train_k9_guardian():
    # --- 1. SETUP PATHS ---
    # Current folder (Project_K9_Guardian)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to your VERIFIED data.yaml (inside master_k9)
    # Adjust 'master_k9' if your folder name is different
    yaml_path = os.path.join(base_dir, 'datasets', 'master_k9', 'data.yaml')
    
    # Path to the model file (in the project root)
    model_path = os.path.join(base_dir, 'yolo11n.pt') 

    print(f"📂 Reading Data from: {yaml_path}")
    print(f"🚀 Loading Model from: {model_path}")

    # --- 2. HARDWARE CHECK ---
    device = 0 if torch.cuda.is_available() else 'cpu'
    if device == 0:
        print(f"✅ Hardware: GPU Detected ({torch.cuda.get_device_name(0)})")
    else:
        print("⚠️ Hardware: GPU not found. Training will be slow.")

    # --- 3. START TRAINING ---
    print("🐕 K9 Guardian: Initializing YOLO11n (Nano)...")
    
    # Load the model
    model = YOLO(model_path) 

    # Train
    results = model.train(
        data=yaml_path,
        
        # --- Performance Settings ---
        epochs=100,        # 100 is standard for a good result
        imgsz=640,
        batch=16,          # 16 is good for 11n on most GPUs
        patience=20,       # Stop early if no improvement
        workers=4,
        
        # --- Output ---
        project='k9_runs',
        name='v1_strict_deploy',
        device=device,
        save=True,
        verbose=True
    )
    
    print(f"🏆 DONE! Best model saved at: k9_runs/v1_strict_deploy/weights/best.pt")

if __name__ == '__main__':
    train_k9_guardian()