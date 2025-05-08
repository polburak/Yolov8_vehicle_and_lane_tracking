import math
class Takipci:
    def __init__(self):
        self.sonraki_id = 0
        self.takip = {}
        self.gecmis = {}

    def guncelle(self, tespitler, frame_no):
        yeni_takip = {}

        for x1, y1, x2, y2 in tespitler:
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            eşleşen_id = None
            for obj_id, (px1, py1, px2, py2) in self.takip.items():
                pcx = (px1 + px2) // 2
                pcy = (py1 + py2) // 2
                uzaklik = math.hypot(cx - pcx, cy - pcy)
                if uzaklik < 50:
                    eşleşen_id = obj_id
                    break

            if eşleşen_id is None:
                eşleşen_id = self.sonraki_id
                self.sonraki_id += 1

            yeni_takip[eşleşen_id] = (x1, y1, x2, y2)

            # Geçmiş konum güncelle
            self.gecmis.setdefault(eşleşen_id, []).append((cx, cy, frame_no))

        self.takip = yeni_takip
        return self.takip, self.gecmis
