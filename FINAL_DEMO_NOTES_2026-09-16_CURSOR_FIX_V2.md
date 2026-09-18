# NSosyal Bağlam — Final Demo Cursor Fix V2

- UI/UX görünümü değiştirilmedi (`index.html` ve `styles.css` aynı).
- BAĞLAM canlı analiz kartı güncellenirken gönderi textarea odağı artık korunuyor.
- Opera/Chromium'da kardeş DOM güncellemesinin textarea focus/selection kaybına karşı çift aşamalı focus + selection restore eklendi.
- İmleç konumu, seçim yönü ve textarea scroll konumu korunuyor.
- Eski/yarışan analiz cevaplarını engelleyen sequence kontrolü korunuyor.
