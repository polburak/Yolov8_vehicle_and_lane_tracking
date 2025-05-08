import cv2
import json
import numpy as np

video_yolu = "girdi/video1.mp4"
serit_json_yolu = "seritler/seritler.json"

# Şeritleri yükle
with open(serit_json_yolu, "r") as f:
    seritler = json.load(f)

# İlk kareyi al
cap = cv2.VideoCapture(video_yolu)
ret, frame = cap.read()
cap.release()

if not ret:
    print("Video okunamadı.")
    exit()

# Çokgen çiz
renkler = [(255, 0, 0), (0, 255, 0), (0, 0, 255),
           (255, 255, 0), (255, 0, 255), (0, 255, 255)]

for i, serit in enumerate(seritler):
    pts = np.array(serit["noktalar"], np.int32)
    cv2.polylines(frame, [pts], isClosed=True, color=renkler[i % len(renkler)], thickness=2)

    # Etiket yaz
    merkez = np.mean(pts, axis=0).astype(int)
    cv2.putText(frame, f"Serit {serit['serit_id']}", tuple(merkez),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, renkler[i % len(renkler)], 2)

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        nokta = (x, y)
        for serit in seritler:
            polygon = np.array(serit["noktalar"], dtype=np.int32)
            if cv2.pointPolygonTest(polygon, nokta, False) >= 0:
                print(f"({x}, {y}) noktası Serit {serit['serit_id']} icinde.")
                return
        print(f"({x}, {y}) noktası hiçbir serit içinde değil!")

cv2.namedWindow("Serit Dogrulama")
cv2.setMouseCallback("Serit Dogrulama", mouse_callback)

while True:
    cv2.imshow("Serit Dogrulama", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
