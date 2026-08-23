# PROJECT STATUS — NSosyal Bağlam 2026 Rebuild

## Çalışan prototip
- FastAPI backend: mevcut
- Tek-origin statik sosyal UI: mevcut
- Moderasyon API: mevcut
- İtiraz akışı: mevcut (simüle inceleme kuyruğu)
- ADALET ranking ve açıklama API: mevcut
- DENGE davranış örüntüsü API: mevcut
- Metrik API'leri: mevcut
- Jüri/Araştırma ekranı: mevcut

## Doğrulanan testler
- `pytest`: 12/12 geçti (çalışma ortamında Python 3.13.5 ile mantıksal regresyon testi)
- `evaluation/run_evaluation.py`: başarıyla tekrar üretildi
- API smoke test: root, health, moderation ve wellbeing başarılı
- JavaScript syntax check: başarılı

## Python 3.14 hedefi
Çalışma konteynerinde Python 3.14 kurulu olmadığı için paket doğrudan 3.14 üzerinde burada koşturulamadı. Bunun yerine PyPI üzerinde CPython 3.14 Windows wheel/sınıflandırıcı desteği doğrulanmış bağımlılıklar seçildi. Windows'taki gerçek kurulum `py -3.14` ile yapılmalıdır.

## Açık sınırlar
- Resmî NSosyal API yok
- Gerçek NSosyal kullanıcı verisi yok
- Gerçek saha/usability sonucu yok
- Moderasyon modeli BERTurk değil
- Güncel NSosyal'e görsel yakınlık kamuya açık ekranlarla sınırlı; giriş gerektiren yüzeyler uydurulmadı

## Sonraki rapor işleri
1. Kullanıcının Windows Python 3.14 kurulumunu doğrulama
2. Gerçek cihazdan temiz 1366×768 ekran görüntüleri
3. GitHub remote oluşturma/push
4. Gerçek 3–5 kişilik kullanılabilirlik testi (uygunsa)
5. Teknik rapor DOCX/PDF finalizasyonu
