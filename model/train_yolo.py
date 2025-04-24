from ultralytics import YOLO

model = YOLO("yolo11n.pt")

model.train(
    data="C:\\Users\\Kristina\\cv_teaching\\data\\example.yaml",
    epochs=20,
    imgsz=640,
    batch=16,
    name="custom_yolo11n"
)
