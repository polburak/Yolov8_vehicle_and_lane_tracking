from ultralytics import YOLO

model = YOLO("yolov8n.pt")
VEHICLE_CLASSES = [2, 3, 5, 7]  # car, motorcycle, bus, truck

def detect(frame):
    results = model(frame)[0]
    detections = []

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result[:6]
        if int(class_id) in VEHICLE_CLASSES and score > 0.4:
            detections.append((int(x1), int(y1), int(x2), int(y2)))

    return detections
