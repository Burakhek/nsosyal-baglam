# NSosyal Bağlam — Final Demo İşlevsellik Notları

Bu paket mevcut görsel UI/UX tasarımını koruyarak final demosu için işlevsellik düzeltmeleri içerir.

## BAĞLAM
- Gönderi metni gerçek yerel TF-IDF + Logistic Regression modeliyle analiz edilir.
- Her analiz izlenebilir `MOD-xxxx` kimliği üretir.
- Düzenle eylemi metin alanına geri döndürür ve yazdıkça yeniden analiz yapılır.
- Normal "Yayınla" akışı BAĞLAM kararını sunucu tarafında yeniden doğrular.
- `warn` kararında bilinçli "Yine de Yayınla" onayı gerekir.
- `review` kararları sessizce atlanmaz; prototip inceleme akışına yönlendirilir.
- İtiraz artık sabit demo kimliği yerine gerçekten ekrandaki moderasyon sonucuna bağlanır.

## ADALET
- Normal / Adil Görünürlük geçişi gerçek sıralama uç noktasını kullanır.
- "Neden görüyorum?" her sıralanmış gönderi için gerçek açıklama verisi döndürür.
- Kalite/ilgililik kapıları korunur; takipçi sayısı tek başına boost/ceza değildir.
- Veri tercihlerinden ADALET kapatılırsa Adil Görünürlük modu uygulanmaz.
- Jüri ekranındaki rapor metrikleri sabit kontrollü 7 gönderilik veri kümesi üzerinden kalır; demo sırasında yayınlanan gönderiler rapor kanıtını değiştirmez.

## DENGE
- Kontrollü hızlı senaryo gerçek DENGE değerlendirme fonksiyonundan geçer.
- Modül tercihlerden kapatılabilir.
- Kapatma (x) eylemi `hide_today` yanıtını kaydeder ve aynı gün öneriyi yeniden göstermez.
- 5 dakikalık hatırlatıcı eylemi gerçekten zamanlayıcı kurar ve yanıtı backend'e kaydeder.
- DENGE tanı koymaz; mevcut açıklama ve eşikler korunmuştur.

## Veri tercihleri
- BAĞLAM, ADALET, DENGE ve açıklama tercihleri artık gerçekten modül davranışını etkiler.
- Görsel tasarım/CSS değiştirilmemiştir.

## Test
- `python -m pytest -q`
- Beklenen: `21 passed`
