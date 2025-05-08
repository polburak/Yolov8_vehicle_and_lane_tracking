import os
from collections import defaultdict

class Loglayici:
    def __init__(self, dosya_yolu):
        self.tespit_edilen_idler = set()
        self.gelen_sayac = 0
        self.giden_sayac = 0
        self.serit_sayac = defaultdict(int)
        self.gecis_zamanlari = []  # (id, yön, şerit, zaman)
        self.dosya_yolu = dosya_yolu
        os.makedirs(os.path.dirname(dosya_yolu), exist_ok=True)

    def tespit_oldu(self, obj_id):
        self.tespit_edilen_idler.add(obj_id)

    def gelen_kontrol_et(self, obj_id, serit_id=None, zaman=None):
        if obj_id in self.tespit_edilen_idler:
            self.gelen_sayac += 1
            if zaman is not None:
                self.gecis_zamanlari.append((obj_id, "Gelen", serit_id, zaman))

    def giden_kontrol_et(self, obj_id, serit_id=None, zaman=None):
        if obj_id in self.tespit_edilen_idler:
            self.giden_sayac += 1
            if zaman is not None:
                self.gecis_zamanlari.append((obj_id, "Giden", serit_id, zaman))

    def serit_say(self, obj_id, serit_id):
        if obj_id in self.tespit_edilen_idler and serit_id is not None:
            self.serit_sayac[serit_id] += 1

    def sayac_getir(self):
        return {
            "toplam": len(self.tespit_edilen_idler),
            "gelen": self.gelen_sayac,
            "giden": self.giden_sayac,
            "seritler": dict(self.serit_sayac)
        }

    def log_yaz(self):
        # TXT log
        with open(self.dosya_yolu, 'w') as f:
            f.write(f"=>Toplam Gelen Araç Sayısı:{self.gelen_sayac}\n\n")
            f.write(f"=>Toplam Giden Araç Sayısı:{self.giden_sayac}\n\n")
        #   f.write(f"Toplam Tespit Edilen Araç Sayısı: {len(self.tespit_edilen_idler)}\n\n")

            f.write("=>Şerit Bazlı Geçişler:\n\n")
            for serit_id in sorted(self.serit_sayac.keys()):
                f.write(f"  Şerit {serit_id}: {self.serit_sayac[serit_id]} araç\n")

            f.write("\n=>Araç Geçiş Zamanları:\n\n")
            for obj_id, yon, serit_id, zaman in self.gecis_zamanlari:
                f.write(f"ID: {obj_id} | Yön: {yon} | Şerit: {serit_id} | Zaman: {zaman:.2f} saniye\n")


