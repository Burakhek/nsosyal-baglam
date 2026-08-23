# Gizlilik ve Güvenlik

## Veri minimizasyonu
Prototipin çalışması için gerekli olmayan GPS, mikrofon, kamera, rehber, özel mesaj ve haricî uygulama verileri toplanmaz.

## Wellbeing
Oturum süresi, kaydırma sayısı, hızlı geçiş oranı ve toplam dwell gibi özet özellikler değerlendirilir. Tasarım hedefi, mümkün olan özelliklerin cihaz tarafında hesaplanmasıdır.

## Uygulanan prototip kontrolleri
- Pydantic giriş doğrulama
- Gönderi uzunluğu sınırı
- ORM gerektirmeyen belleksel demo veri modeliyle SQL injection yüzeyi yok
- Kısıtlı CORS origin listesi
- Ham gizli anahtar bulunmaması
- `.env.example`
- Kullanıcıya ham stack trace göstermeyen API hata yapısı

## Üretim için ek gereksinimler
- kimlik doğrulama/yetkilendirme
- oran sınırlama
- audit log politikası
- şifreli kalıcı depolama
- secrets manager
- bot/fake engagement savunması
- bağımlılık ve güvenlik taraması
