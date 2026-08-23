# NSosyal Bağlam — 2026 Rebuild

**NSosyal entegrasyon prototipi — resmî NSosyal uygulaması, resmî NSosyal özelliği veya resmî API entegrasyonu değildir.**

Bu sürüm, eski “dashboard/laboratuvar” arayüzünden ayrılıp kamuya açık güncel NSosyal ürün anatomisine yakın bir sosyal medya deneyimi olarak baştan düzenlenmiştir.

## Üç ana modül

- **BAĞLAM:** Türkçe metinde zararlılık ile anlatım biçimini ayrı değerlendiren yayın öncesi bağlam desteği.
- **ADALET:** İlgililik/kalite kapılarını koruyan ve önceki görünürlüğe aşırı bağımlılığı azaltmayı deneyen exposure-aware yeniden sıralama.
- **DENGE:** Kaydırma hızı, dwell time, hızlı geçiş ve oturum süresini birlikte ele alan isteğe bağlı mola desteği. Tanı koymaz.

## Bu sürümde değişenler

- Tek uygulama, tek port: `http://127.0.0.1:8000`
- **Python 3.14 hedefi**
- Node/Next.js/npm gerekmez
- Frontend FastAPI tarafından `backend/static/` içinden servis edilir
- BAĞLAM gönderi oluşturucunun içine gömülüdür
- ADALET normal sosyal akışta `Normal / Adil Görünürlük` modu olarak çalışır
- DENGE akış içinde kapatılabilir öneri olarak görünür
- Profil: görünen ad, `@kullanıcıadı`, doğrulama, takip, sayaçlar, `Zaman Çizelgesi / Medya / Yanıtlar`
- Keşfet: arama + `Trendler / Etiketler / Haberler`
- Mobil Medya görünümü: koyu, medya odaklı yüzey
- İtiraz, `Neden görüyorum?`, veri tercihleri ve ayrı jüri/araştırma ekranı
- Jüri ekranı gerçek prototip metriklerini API'den okur; uydurma sonuç göstermez

## Windows — önerilen kurulum

### 1. Kurulum
Kök klasörde:

```text
setup_windows.bat
```

Bu dosya özellikle `py -3.14` kullanır ve sanal ortamı `backend/.venv314` olarak oluşturur.

### 2. Çalıştırma

```text
run_windows.bat
```

Tarayıcı:

```text
http://127.0.0.1:8000
```

Geliştirici modu gerekiyorsa:

```text
run_windows_dev.bat
```

### PowerShell ile elle kurulum

```powershell
cd backend
py -3.14 -m venv .venv314
.\.venv314\Scripts\python.exe -m pip install --upgrade pip
.\.venv314\Scripts\python.exe -m pip install -r requirements.txt
.\.venv314\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

PowerShell `Activate.ps1` kullanmak zorunda değildir.

## Python 3.14 paket stratejisi

`requirements.txt` 2026-08 itibarıyla Python 3.14 destekleyen sürümlere taşınmıştır. Özellikle eski prototipte kurulum sorunu çıkaran scikit-learn 1.7.1 yerine **scikit-learn 1.9.0** kullanılır; bu sürüm CPython 3.14 Windows x86-64 wheel yayımlar.

## Test

```powershell
cd backend
.\.venv314\Scripts\python.exe -m pytest -q
```

Beklenen mevcut test sayısı: **12**.

## Gerçek teknik durum

Moderasyon prototipinde internet gerektirmeyen gerçek ML yürütümü vardır:

- word TF-IDF
- character TF-IDF
- Logistic Regression
- küçük sentetik eğitim/test veri kümesi

**BERTurk değildir.** BERTurk/Transformer üretim adayı olarak gelecek çalışma olabilir; mevcut prototipte varmış gibi gösterilmez.

Mevcut ölçüm özeti:

- Moderasyon Macro F1: `0.4930`
- Macro Precision: `0.4924`
- Macro Recall: `0.5033`
- Sentetik test: `20` örnek
- ADALET küçük üretici Top-5 payı: `0.20 → 0.40`
- ADALET Top-5 ortalama ilgililik: `0.846 → 0.884`
- DENGE hızlı senaryo: `25.0 kaydırma/dk`, `1.33 s` ort. dwell, `%80` hızlı geçiş → mola önerisi
- DENGE intentional senaryo: `3.43 kaydırma/dk`, `11.0 s` dwell, `%15` hızlı geçiş → mola önerisi yok

Bu değerler **NSosyal üretim performansı değildir**.

## Kaynak yapısı

- `backend/app/`: FastAPI API ve servisler
- `backend/static/`: gerçek demo UI kaynakları
- `backend/tests/`: API ve çekirdek davranış testleri
- `evaluation/`: yeniden üretilebilir sentetik değerlendirme
- `docs/`: mimari, etik, güvenlik, rapor eşlemesi ve UI araştırması
- `ml/`: model/veri notları
- `report_assets/`: rapor için varlıklar
- `demo/`: jüri demo akışı

## Kamuya açık NSosyal UI araştırması

Ayrıntılı kayıt:

`docs/nsosyal-ui-research-2026.md`

UI referansında yalnızca kamuya açık/gözlemlenebilir ürün yapısı kullanılır; erişilemeyen ekranlar “resmî NSosyal tasarımı” diye uydurulmaz.
