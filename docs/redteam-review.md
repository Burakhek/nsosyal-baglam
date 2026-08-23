# Jüri Red-Team İncelemesi — P0

| Risk | Şiddet | Mevcut durum | Düzeltme |
|---|---:|---|---|
| “BERTurk kullanıyoruz” denip aslında kullanılmaması | Kritik | Önlenmiş | UI ve model card gerçek motor adını gösteriyor |
| Sentetik F1’in gerçek performans gibi sunulması | Kritik | Önlenmiş | ACTUAL_SYNTHETIC_PROTOTYPE etiketi |
| Projenin üç ayrı dağınık fikir görünmesi | Yüksek | Azaltıldı | “Yayın öncesi–dağıtım–tüketim” tek karar katmanı anlatısı |
| Fairness küçük hesabı koşulsuz yükseltir | Yüksek | Önlenmiş | Quality gate + regression testi |
| Büyük hesaplar cezalandırılıyor | Yüksek | Azaltıldı | Relevance/quality dominant; regression testi |
| Wellbeing klinik tanıya kayar | Kritik | Önlenmiş | Tanı yok; opt-out; nötr davranış dili |
| UI yalnız mockup | Kritik | Önlenmiş | FastAPI ile bağlı çalışan statik istemci, gerçek endpointler |
| Ayrı Node/Next.js zinciri Windows demosunda ek kurulum ve port riski yaratıyordu | Orta | Giderildi | Final P0 arayüzü FastAPI ile aynı origin üzerinden servis edilen bağımlılıksız istemciye taşındı; npm gerekmiyor |
| Resmî NSosyal API erişimi varmış gibi algılanması | Kritik | Önlenmiş | Her ekranda entegrasyon prototipi etiketi |
| Gerçek kullanılabilirlik testi yok | Orta | Açık limit | 2–7 Eylül mentörlükte gerçek test yapılmalı; şimdi sonuç uydurulmamalı |
| Uzak GitHub linki yok | Yüksek | Açık limit | Takım hesabına push edilip rapora link eklenmeli |
| Model performansı düşük | Yüksek | Açık limit | Açık veri + BERTurk P1; P0 dürüst baseline kanıtı |
