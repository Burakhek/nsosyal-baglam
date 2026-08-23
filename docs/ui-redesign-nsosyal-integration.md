# NSosyal Bağlam — 2026 UI/UX Rebuild

## Hedef
Kullanıcıya “araştırma dashboard'u” değil, gerçek bir sosyal medya ürünü içinde çalışan yapay zekâ karar katmanı hissi vermek.

## Kamuya açık NSosyal anatomisinden alınan ürün kalıpları
- kompakt sosyal navigasyon,
- zaman çizelgesi / gönderi anatomisi,
- görünen ad + `@handle` + doğrulama yapısı,
- takip ve profil sayaçları,
- `Zaman Çizelgesi / Medya / Yanıtlar`,
- arama + `Trendler / Etiketler / Haberler`,
- mobil medya-öncelikli koyu yüzey ve alt navigasyon yaklaşımı.

Ayrıntılı araştırma: `docs/nsosyal-ui-research-2026.md`.

## BAĞLAM — doğal entegrasyon
BAĞLAM artık ayrı analiz laboratuvarı değildir. Gönderi oluşturucunun hemen altında yayın öncesi yardımcı katmandır. Gerçek `/api/moderation/analyze` çıktısı ile:
- karar,
- güven,
- zarar riski,
- ironi/sarkazm sinyali,
- açıklama,
- düzenleme / yine de yayınlama / itiraz
sunulur.

## ADALET — doğal entegrasyon
ADALET ayrı karşılaştırma dashboard'u değildir. Akışta `Normal / Adil Görünürlük` seçimi bulunur. Adil modda:
- sıralama gerçek `/api/ranking/rank` çıktısından gelir,
- uygun içerikte `Keşif fırsatı` etiketi görünür,
- `Neden görüyorum?` gerçek explanation endpointini çağırır.

Takipçi sayısı tek başına boost nedeni değildir; kalite ve relevans kapıları korunur.

## DENGE — doğal entegrasyon
DENGE, akış içinde kapatılabilir bir mola önerisidir. Kontrollü hızlı senaryo API üzerinden değerlendirilir. Tıbbi/psikolojik tanı dili kullanılmaz.

## Ayrı teknik yüzey
`Jüri / Araştırma` ekranı normal kullanıcı akışından ayrıdır. API'deki gerçek sentetik/kontrollü metrikleri gösterir ve BERTurk/gerçek NSosyal verisi/üretim entegrasyonu gibi yapılmamış işleri yapılmış gibi göstermez.

## Teknik sadeleştirme
Final P0 demo yolunda ayrı Next.js/npm sunucusu kaldırılmıştır. UI FastAPI ile aynı origin üzerinden çalışır:

`http://127.0.0.1:8000`

Bu, Windows jüri demosunda port ve PowerShell/npm hata yüzeyini azaltır.
