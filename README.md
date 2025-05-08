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

## Dosya Açıklamaları ##
| Dosya Adı             | Açıklama                                                                               |
| ----------------------| ---------------------------------------------------------------------------------------|
| `main.py`             | Projenin ana dosyası, araç tespiti vetakibi yapar, yön analizi ve şerit eşlemesi yapar.| 
| `tespit.py`           | YOLOv8 modeli ile araç tespiti yapar. Yalnızca belirli araç sınıflarını filtreler.     |
| `takip.py`            | Her araca bir ID atayarak basit mesafe tabanlı bir algoritmayla takip işlemini yürütür.|
| `loglayici.py`        | Gelen/giden araç sayısını, şerit bazlı geçişleri ve zaman damgalı verileri loglar.     |
| `serit_yukleyici.py`  | Şerit tanımlarını yükler ve bir noktanın hangi şeride ait olduğunu tespit eder.        |
| `serit_secici.py`     | Kullanıcının video üzerinde fare ile şeritleri çizmesini sağlar.                       |
| `serit_test_goster.py`| Şerit bölgelerinin doğruluğunu test etmek için kullanılır. 
    

## [Test Videosunu İndir](https://drive.google.com/file/d/1v5Hh2fll-8pAtMIrMuP1mIsLRkn9lnN-/view?usp=sharing) ## 

## [İşlenmiş Sonuç Videosunu İndir](https://drive.google.com/file/d/1V60vCSv-gAfhNB3mM55zURU1JXkbPTVX/view?usp=sharing) ##
