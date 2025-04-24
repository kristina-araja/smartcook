from ultralytics import YOLO
import tempfile
import cv2

model = None

def load_model():
    global model
    if model is None:
        print("Loading YOLO model...")
        model = YOLO("C:\\Users\\Kristina\\smartcook\\model\\best.pt")
        print("YOLO model loaded.")

def detect_ingredients(image_bytes):
    print("detect_ingredients invoked")
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

    print("Detected ingredients:", detected)
    return list(detected)
