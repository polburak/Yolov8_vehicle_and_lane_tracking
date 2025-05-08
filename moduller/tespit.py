from ultralytics import YOLO

model = YOLO("yolov8n.pt")
ARAC_SINIFLARI = [2, 3, 5, 7]  # araba, motosiklet, otobüs, kamyon

def tespit_et(frame):
    results = model(frame)[0]
    tespitler = []

    for sonuc in results.boxes.data.tolist():
        x1, y1, x2, y2, skor, sinif_id = sonuc[:6]
        if int(sinif_id) in ARAC_SINIFLARI and skor > 0.4:
            tespitler.append((int(x1), int(y1), int(x2), int(y2)))

    return tespitler
