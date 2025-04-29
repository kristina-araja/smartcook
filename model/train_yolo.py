from ultralytics import YOLO

model = YOLO("C:\\Users\\Kristina\\smartcook\\model\\best.pt")

model.train(
    data="C:\\Users\\Kristina\\smartcook\\model\\data\\food\\train_model.yaml",
    epochs=10,
    imgsz=640,
    batch=16,
    name="yolo_bestn2"
)
