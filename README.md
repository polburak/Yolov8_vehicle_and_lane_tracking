# Yolov8_vehicle_and_lane_tracking
Bu proje, tanımlı video üzerinde gerçek zamanlı olarak **araç tespiti**, **takibi**, **şerit belirleme** ve **geliş/gidiş yönü analizini** gerçekleştiren Python tabanlı bir görüntü işleme uygulamasıdır.

## Klasör Yapısı ##
    ├── main.py # Ana kontrol dosyası
    ├── moduller/
    │ ├── tespit.py # YOLOv8 ile araç tespiti
    │ ├── takip.py # Araç takip ve ID atama
    │ ├── loglayici.py # Geliş/gidiş/şerit loglama
    │ ├── serit_yukleyici.py # Şerit tespiti
    ├── serit_secici.py # Manuel şerit çizim aracı
    ├── serit_test_goster.py # Şeritleri doğrulama aracı
    ├── seritler/seritler.json # Çizilen şerit verisi
    ├── girdi/video1.mp4 # Test videosu
    ├── cikti/ # Log ve video çıktısı
