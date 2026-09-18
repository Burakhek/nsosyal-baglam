# NSosyal Bağlam - Final Audit Düzeltmeleri

Tarih: 24.08.2026

Bu paket, teknik rapor öncesindeki son tutarlılık denetiminde yapılan güvenli düzeltmeleri içerir.

- `backend/app/services/moderation.py` içindeki karar mantığını yanlış açıklayan yorum, gerçek uygulamayla eşleştirildi. Çalışan karar mantığı değiştirilmedi: yüksek zarar riski `review`; belirsizlik, düşük güven veya yüksek sarkazm sinyali `warn` üretir.
- Herhangi bir model sonucu, veri seti, kullanıcı testi veya NSosyal entegrasyonu uydurulmadı.
- Mevcut P0 modelinin sentetik veri ve doğrulama sınırlılıkları korunmuştur.
- Otomatik test paketi düzeltmeden sonra tekrar çalıştırılmıştır.

Bu dosya üretim hazır olma iddiası değildir; final rapor ile kod davranışı arasındaki tutarlılığı belgeleyen değişiklik notudur.
