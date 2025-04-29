from ultralytics import YOLO
import tempfile
import os
import uuid
import cv2

STATIC_DIR = "uploads"
model = None

def load_model():
    global model
    if model is None:
        print("📦 Loading YOLO model...")
        model = YOLO("C:\\Users\\Kristina\\smartcook\\model\\best.pt")
        print("✅ Model loaded")

def detect_ingredients_and_save(image_bytes):
    print("🔍 Running detection...")
    load_model()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(image_bytes)
        tmp_path = tmp.name

    frame = cv2.imread(tmp_path)
    results = model.predict(frame, verbose=False)

    detected = set()
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            name = result.names[class_id]
            detected.add(name)

    # Saving annotated image
    annotated_img = results[0].plot()
    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR)

    filename = f"{uuid.uuid4().hex}.jpg"
    save_path = os.path.join(STATIC_DIR, filename)
    success = cv2.imwrite(save_path, annotated_img)
    print(f"💾 Image saved: {'success' if success else 'error'} → {save_path}")

    image_url = f"/uploads/{filename}"
    return list(detected), image_url
