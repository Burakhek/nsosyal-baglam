# NSosyal Bağlam — Final Demo Stabilizasyonu (15.09.2026)

Bu sürümde UI/UX tasarımı değiştirilmemiştir. `backend/static/index.html` ve `backend/static/styles.css` önceki final demo ile aynıdır.

## BAĞLAM
- TF-IDF kelime+karakter n-gram + Logistic Regression istatistiksel tabanı korunmuştur.
- Üzerine çevrimdışı ve şeffaf bir Türkçe bağlam katmanı eklenmiştir.
- Selamlaşma/hâl-hatır cümlelerinin düşük veri seti güveni nedeniyle yanlış uyarı üretmesi azaltılmıştır.
- Kişiye yönelik doğrudan hakaret, açık tehdit, tekrarlayan hedef alma, nesne/fikir eleştirisi, yaygın Türkçe mecazlar ve övgü+olumsuz olay sarkazm karşıtlığı ayrı ele alınır.
- BERTurk veya harici API kullanılmaz; final bilgisayarında tamamen yerel çalışır.
- Ekrandaki “Güven” değeri final motorunun karar güvenidir; üretim doğruluğu veya saha başarı oranı değildir.

## ADALET
- Mevcut kalite kapısı, ilgililik ölçeklemesi, göreli hız ve önceki görünürlük temelli bounded fairness düzeltmesi korunmuştur.
- Düşük kaliteli küçük üreticinin otomatik yükseltilmemesi ve yüksek ilgililikte büyük üreticinin bastırılmaması regresyon testleriyle doğrulanır.

## DENGE
- Mevcut kontrollü davranış örüntüsü eşikleri korunmuştur.
- Devre dışı bırakma, hızlı/kısa oturumda uyarı göstermeme, uzun ve hızlı örüntüde mola önerisi davranışları test edilir.

## Final notu
Bu prototip gerçek NSosyal API'sine bağlı değildir. Yarışmacılara API erişimi sağlanmadığı için bağımsız entegrasyon prototipi olarak sunulur.

## Doğrulama
- Final paketinde `python -m pytest -q` ile **39/39 test geçti**.
- UI dosyaları (`index.html`, `styles.css`) önceki çalışan final demo ile byte-for-byte aynıdır.
