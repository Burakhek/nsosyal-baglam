# Release notes — Context Guard v4

- UI yerleşimi ve CSS korunmuştur.
- `Güven` etiketi anlamsal netlik için `Modelin kararından eminliği` olarak değiştirilmiştir.
- `Zarar riski` -> `Zarar sinyali`; `İroni / sarkazm` -> `İroni / sarkazm sinyali`.
- Türkçe hakaret/küfür sözlüğü ve morfolojik kök eşleme genişletilmiştir.
- Kişi hedefi, nesne/fikir eleştirisi, alıntı/bildirim, olumsuzlama ve üst-bağlam ayrımı güçlendirilmiştir.
- Bazı noktalama/boşluk/leet tabanlı gizleme biçimleri yakalanır.
- Tanımsız/düşük güvenli metne otomatik olarak sahte yüksek güven verilmez; uyarı yoluna düşer.
- Raporlanan 59/20 sentetik bağımsız test metriği değiştirilmemiştir; Context Guard kuralları canlı demo katmanıdır.
- Otomatik test sonucu: 56/56 geçti (mevcut + Context Guard regresyonları).

Bu sürüm serbest Türkçe metinde %99 doğruluk garantisi iddia etmez.
