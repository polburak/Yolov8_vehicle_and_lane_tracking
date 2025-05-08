import cv2
import os
from moduller.tespit import tespit_et
from moduller.takip import Takipci
from moduller.loglayici import Loglayici
from moduller.serit_yukleyici import SeritYukleyici

video_yolu = "girdi/video1.mp4"
video_adi = os.path.basename(video_yolu)  # "test1.mp4"
video_adi_ismi = os.path.splitext(video_adi)[0]
cikti_video_yolu = f"cikti/{video_adi_ismi}_sonuc.mp4"
log_yolu = f"cikti/{video_adi_ismi}_log.txt"


cap = cv2.VideoCapture(video_yolu)
width, height = int(cap.get(3)), int(cap.get(4))
fps = int(cap.get(cv2.CAP_PROP_FPS))

os.makedirs("cikti", exist_ok=True)
out = cv2.VideoWriter(cikti_video_yolu, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

takipci = Takipci()
loglayici = Loglayici(log_yolu)
serit_yukleyici = SeritYukleyici("seritler/seritler.json")

cizgi_y = height // 2 + 150
frame_no = 0
gecen_idler = set()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_no += 1
    tespitler = tespit_et(frame)
    takip_edilenler, gecmis_konumlar = takipci.guncelle(tespitler, frame_no)

    for obj_id, (x1, y1, x2, y2) in takip_edilenler.items():
        loglayici.tespit_oldu(obj_id)
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)

        serit_etiket = "Serit: -"

        if obj_id in gecmis_konumlar and len(gecmis_konumlar[obj_id]) >= 2:
            onceki_cy = gecmis_konumlar[obj_id][-2][1]

            if obj_id not in gecen_idler:
                zaman = frame_no / fps
                gecis_serit = serit_yukleyici.serit_bul(cx, cy)

                if onceki_cy < cizgi_y and cy >= cizgi_y:
                    loglayici.gelen_kontrol_et(obj_id, gecis_serit, zaman)
                    loglayici.serit_say(obj_id, gecis_serit)
                    gecen_idler.add(obj_id)

                elif onceki_cy > cizgi_y and cy <= cizgi_y:
                    loglayici.giden_kontrol_et(obj_id, gecis_serit, zaman)
                    loglayici.serit_say(obj_id, gecis_serit)
                    gecen_idler.add(obj_id)
                else:
                    serit_no = serit_yukleyici.serit_bul(cx, cy)
                    serit_etiket = f"Serit: {serit_no}" if serit_no else "Serit: ?"
            else:
                serit_etiket = "Serit: -"
        else:
            serit_no = serit_yukleyici.serit_bul(cx, cy)
            serit_etiket = f"Serit: {serit_no}" if serit_no else "Serit: ?"

        # Görsel çizimler
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"ID: {obj_id}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, serit_etiket, (x1, y2 + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    # Sayaçlar
    sayaclar = loglayici.sayac_getir()
    cv2.putText(frame, f"Gelen: {sayaclar['gelen']} arac", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(frame, f"Giden: {sayaclar['giden']} arac", (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    # Şerit sayaçları
    offset = 120
    for serit_id in sorted(sayaclar["seritler"].keys()):
        adet = sayaclar["seritler"][serit_id]

        # Renk belirle
        if serit_id in [1, 2, 3]:
            renk = (0, 0, 0)
        elif serit_id in [4, 5, 6]:
            renk = (0, 0, 255)


        cv2.putText(frame, f"Serit {serit_id}: {adet} arac", (10, offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, renk, 2)
        offset += 25

    # Yatay çizgi
    cv2.line(frame, (0, cizgi_y), (width, cizgi_y), (0, 0, 255), 2)

    out.write(frame)
    cv2.imshow(video_adi, frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

loglayici.log_yaz()
cap.release()
out.release()
cv2.destroyAllWindows()
