import cv2
import json
import os

video_yolu = "girdi/video1.mp4"
serit_kayit_yolu = "seritler/seritler.json"
os.makedirs("seritler", exist_ok=True)

cap = cv2.VideoCapture(video_yolu)
ret, frame = cap.read()
if not ret:
    print("Video okunamadı!")
    exit()

cizim_frame = frame.copy()
seritler = []
gecici_noktalar = []
aktif_serit = 1

def mouse_callback(event, x, y, flags, param):
    global gecici_noktalar, cizim_frame, aktif_serit

    if event == cv2.EVENT_LBUTTONDOWN:
        gecici_noktalar.append((x, y))
        cv2.circle(cizim_frame, (x, y), 4, (0, 255, 0), -1)

    elif event == cv2.EVENT_RBUTTONDOWN:
        if len(gecici_noktalar) >= 3:
            seritler.append({
                "serit_id": aktif_serit,
                "noktalar": gecici_noktalar
            })
            print(f"[OK] Şerit {aktif_serit} kaydedildi.")
            aktif_serit += 1
            gecici_noktalar = []
            cizim_frame = frame.copy()
            for serit in seritler:
                pts = serit["noktalar"]
                cv2.polylines(cizim_frame, [np.array(pts, np.int32)], isClosed=True, color=(255, 0, 0), thickness=2)

        else:
            print("En az 3 nokta ile cokgen cizmelisin!")

cv2.namedWindow("Serit Cizimi")
cv2.setMouseCallback("Serit Cizimi", mouse_callback)

import numpy as np
while True:
    gosterilecek = cizim_frame.copy()

    # geçici çizim
    if len(gecici_noktalar) >= 2:
        for i in range(1, len(gecici_noktalar)):
            cv2.line(gosterilecek, gecici_noktalar[i - 1], gecici_noktalar[i], (0, 255, 0), 1)

    cv2.putText(gosterilecek, f"Serit {aktif_serit} icin noktalari sol tikla", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.putText(gosterilecek, "Cokgeni bitirmek icin sag tikla", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

    cv2.imshow("Serit Cizimi", gosterilecek)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if aktif_serit > 6:
        print("6 serit cizildi, işlem tamamlandı.")
        break

cap.release()
cv2.destroyAllWindows()

# Kaydet
with open(serit_kayit_yolu, "w") as f:
    json.dump(seritler, f, indent=2)

print(f"Şeritler başarıyla '{serit_kayit_yolu}' dosyasına kaydedildi.")
