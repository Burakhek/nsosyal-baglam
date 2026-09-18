# NSosyal Bağlam — Final Context Guard v4

Bu sürüm final canlı demo için BAĞLAM katmanını güçlendirir. Raporun TF-IDF + Logistic Regression taban modeli korunur; canlı demo motoruna şeffaf Türkçe bağlam/küfür güvenlik katmanı eklenmiştir.

- Açık küfür/argo artık hedef olmasa bile sessizce "yayınlanabilir" olmaz; en az bağlam kontrolü uyarısı üretir.
- Kişiye yöneltilmiş açık küfür/hakaret incelemeye gider.
- Alıntı, bildirim, reddetme ve "demek doğru değil" gibi üst-bağlamlar doğrudan saldırı sayılmaz.
- Bazı noktalama/boşluk/leet ile gizlenmiş yazımlar için normalizasyon eklendi.
- "malzeme", "köpeğim", "sıkıldım" gibi masum sözcüklerde kaba kök eşleşmesi yapılmaması için çakışma korumaları eklendi.
- Düşük güvenli, kural dışı yeni metinlere yapay biçimde yüksek güven verilmez; belirsizlikte "Bağlamı kontrol et" uyarısı tercih edilir.
- UI yerleşimi/CSS değiştirilmedi. Yalnızca "Güven" etiketi "Modelin kararından eminliği", "Zarar riski" ise "Zarar sinyali" olarak netleştirildi; bunlar kalibre edilmiş olasılık değildir.

Önemli: Bu prototip herhangi bir serbest Türkçe metinde %99 doğruluk garantisi vermez. Böyle bir iddia için büyük ve temsilî veri, haricî test kümesi ve kalibrasyon gerekir.
