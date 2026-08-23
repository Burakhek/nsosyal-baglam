# NSosyal Bağlam 0.2.0 — 2026 Rebuild

## Amaç
Önceki dashboard benzeri kullanıcı arayüzünü kaldırıp, kamuya açık güncel NSosyal ürün anatomisine daha yakın bir sosyal medya entegrasyon prototipi oluşturmak.

## UI/UX araştırma girdileri
- Güncel NSosyal web profil anatomisi
- Güncel Keşfet/trend terminolojisi
- Güncel Google Play ürün özellikleri
- Kamuya açık mobil Medya Modu görselleri
- 2026 resmî NSosyal özellik güncellemeleri
- Lovable UI/UX tasarım ajanı ile yüksek sadakatli referans tasarım ve ilk doğrulama

UX Pilot bağlantısı da denendi; sağlayıcı çağrısı bu oturumda araç hatası verdiği için çalışmış gibi raporlanmadı.

## Mimari değişiklik
Eski ayrı Next.js geliştirme sunucusu kaldırıldı. UI artık FastAPI ile aynı origin üzerinden `backend/static` içinden servis ediliyor.

Sonuç:
- npm yok
- ikinci port yok
- PowerShell `npm.ps1` sorunu yok
- tek Windows kurulumu
- tek demo URL'si: `http://127.0.0.1:8000`

## Python 3.14
Windows launcher'lar özellikle `py -3.14` kullanır. Eski scikit-learn 1.7.1 yerine CPython 3.14 Windows wheel'i bulunan scikit-learn 1.9.0 seçildi.

## Doğrulama
Çalışma konteynerinde Python 3.14 bulunmadığından uygulama mantığı Python 3.13.5 üzerinde regresyon testinden geçirildi:
- 12/12 pytest geçti
- değerlendirme pipeline'ı tekrar üretildi
- FastAPI TestClient smoke testi geçti
- JavaScript sözdizimi kontrolü geçti

Python 3.14 gerçek Windows çalıştırma doğrulaması kullanıcı bilgisayarında yapılmalıdır.

## Bilinçli iddia sınırları
- Resmî NSosyal entegrasyonu yok
- Gerçek NSosyal kullanıcı verisi yok
- BERTurk yok
- Gerçek saha/usability testi yok
- Kamuya açık olmayan NSosyal ekranları birebir diye uydurulmadı
