# PROJECT STATUS — NSosyal Bağlam 2026 Final (Context Guard V4.1)

## Çalışan prototip
- FastAPI backend: çalışıyor
- Tek-origin statik sosyal UI: çalışıyor
- BAĞLAM moderasyon API ve yayın öncesi karar akışı: çalışıyor
- İtiraz akışı: çalışıyor (simüle inceleme kuyruğu)
- ADALET sıralama ve “Neden görüyorum?” açıklama API: çalışıyor
- DENGE davranış örüntüsü ve mola önerisi API: çalışıyor
- Metrik API'leri: çalışıyor
- Jüri/Araştırma ekranı: çalışıyor
- Windows ve macOS başlatma betikleri: mevcut

## Doğrulama
- Yerel final regresyon paketi: **56/56 test geçti**
- GitHub Actions CI: **Python 3.13 başarılı**
- GitHub Actions CI: **Python 3.14 başarılı**
- Final CI; bağımlılık kurulumu ve `python -m pytest -q` regresyon paketini çalıştırır.
- Context Guard V4.1; açık küfür/hakaret, hedef bağlamı, alıntı/reddetme, bazı gizlenmiş yazımlar ve düşük güvenli girdiler için ek regresyon testleri içerir.

## Teknik kapsam
- Moderasyon tabanı: word TF-IDF + character TF-IDF + Logistic Regression
- Canlı demo katmanı: şeffaf Türkçe bağlam/küfür güvenlik kuralları
- ADALET: kalite/ilgililik kapılarıyla bounded fairness yeniden sıralama
- DENGE: oturum süresi, kaydırma hızı, dwell time ve hızlı geçiş sinyalleri
- Python hedefi: **3.14**; GitHub Actions üzerinde doğrulandı

## Açık sınırlar
- Resmî NSosyal API entegrasyonu yok; proje bağımsız entegrasyon prototipidir.
- Gerçek NSosyal kullanıcı verisi kullanılmaz.
- Moderasyon modeli BERTurk değildir.
- Moderasyon metrikleri küçük sentetik test kümesine aittir; NSosyal üretim performansı değildir.
- ADALET ve DENGE sonuçları kontrollü/sentetik prototip senaryolarıdır.
- Mevcut kullanılabilirlik çalışmaları prototip ölçeğindedir; gerçek platform saha dağıtımı değildir.

## Final repository durumu
- Context Guard V4.1 kodu, final regresyon testleri ve sürüm notları `main` branch'indedir.
- `.pytest_cache`, `__pycache__` ve `*.pyc` gibi geçici dosyalar repository'ye dahil edilmez.
- CI workflow: `.github/workflows/ci.yml`
