# Dosya Manifestosu — 2026 Rebuild

## Çalışan uygulama
| Yol | Rol |
|---|---|
| `backend/app/main.py` | FastAPI giriş noktası, API uçları ve statik UI servisi |
| `backend/app/services/moderation.py` | BAĞLAM prototip ML motoru |
| `backend/app/services/ranking.py` | ADALET sıralama / görünürlük mantığı |
| `backend/app/services/wellbeing.py` | DENGE davranış örüntüsü mantığı |
| `backend/static/index.html` | Tek-origin UI kabuğu |
| `backend/static/styles.css` | NSosyal uyumlu sosyal ürün görsel sistemi |
| `backend/static/app.js` | UI durumları ve gerçek API entegrasyonu |
| `backend/requirements.txt` | Python 3.14 hedef bağımlılıkları |
| `backend/tests/` | API ve çekirdek davranış testleri |

## Çalıştırma
| Yol | Rol |
|---|---|
| `setup_windows.bat` | `py -3.14` ile `.venv314` oluşturur ve bağımlılıkları kurar |
| `run_windows.bat` | Python 3.14 sanal ortamından tek-port demo başlatır |
| `run_windows_dev.bat` | Uvicorn reload geliştirici modu |
| `run.sh` | Python 3.14 POSIX çalıştırma yolu |

## Değerlendirme ve kanıt
| Yol | Rol |
|---|---|
| `evaluation/run_evaluation.py` | Tekrarlanabilir sentetik değerlendirme |
| `evaluation/results/moderation_metrics.json` | BAĞLAM ölçümleri |
| `evaluation/results/ranking_metrics.json` | ADALET karşılaştırması |
| `evaluation/results/wellbeing_metrics.json` | DENGE kontrollü senaryoları |
| `evaluation/results/latency_metrics.json` | Yerel prototip gecikme ölçümü |
| `report_assets/diagrams/` | Mimari ve akış diyagramları |
| `report_assets/screenshots/README.md` | Yeni UI için final ekran görüntüsü planı |

## Dokümantasyon
| Yol | Rol |
|---|---|
| `docs/nsosyal-ui-research-2026.md` | Kamuya açık güncel NSosyal UI/UX araştırması |
| `docs/ai-architecture.md` | AI mimari dokümanı |
| `docs/data-model-ethics.md` | Veri/model/etik sınırlar |
| `docs/privacy-security.md` | Gizlilik ve güvenlik |
| `docs/accessibility.md` | Erişilebilirlik yaklaşımı |
| `docs/user-flows.md` | Kullanıcı akışları |
| `docs/usability-test-protocol.md` | Gerçek kullanıcı testi yapılırsa izlenecek protokol |
| `docs/report-evidence-map.md` | Teknik rapor kanıt eşlemesi |
| `docs/technical-report-draft.md` | Rapor taslak içeriği |
| `docs/jury-defense.md` | Jüri soru/cevap hazırlığı |
| `docs/redteam-review.md` | Eleştirel risk incelemesi |

## Bilinçli olarak bulunmayanlar
- Ayrı Node/Next.js production frontend yok; npm gerekmez.
- Resmî NSosyal SDK/API veya özel kaynak kodu yok.
- Gerçek NSosyal kullanıcı verisi yok.
- BERTurk modeli mevcut P0 motoru olarak yok.
