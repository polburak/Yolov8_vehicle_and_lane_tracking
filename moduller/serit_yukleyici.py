import json
import os
import cv2
import numpy as np

class SeritYukleyici:
    def __init__(self, dosya_yolu="seritler/seritler.json"):
        self.seritler = []
        if not os.path.exists(dosya_yolu):
            raise FileNotFoundError(f"Şerit dosyası bulunamadı: {dosya_yolu}")
        with open(dosya_yolu, "r") as f:
            self.seritler = json.load(f)

    def serit_bul(self, cx, cy):
        nokta = (cx, cy)
        for serit in self.seritler:
            polygon = np.array(serit["noktalar"], dtype=np.int32)
            if cv2.pointPolygonTest(polygon, nokta, False) >= 0:
                return serit["serit_id"]
        return None
