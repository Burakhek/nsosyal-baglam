# Moderation Model Card — demo-tfidf-logreg-1.0

**Amaç:** Türkçe bağlam farkındalığı arayüzü ve ölçülebilir prototip akışı göstermek.

**Model:** Kelime + karakter n-gram TF-IDF, Logistic Regression.

**Veri:** Sentetik prototip veri kümesi.

**Uygun olmayan kullanım:** Üretim moderasyonu, gerçek kullanıcı yaptırımı, hukuki/klinik karar.

**Metrikler:** `evaluation/results/moderation_metrics.json` dosyasında gerçek çalıştırmadan üretilir.

**Sınırlama:** Küçük sentetik veri; performans NSosyal veya genel Türkçe sosyal medya performansı değildir.
