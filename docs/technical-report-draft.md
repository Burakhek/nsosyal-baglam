# NSosyal Bağlam — Proje Teknik Rapor Taslak Materyali

> Bu dosya resmî DOCX şablonuna aktarılacak içerik taslağıdır. Sayfa düzeni, kapak bilgileri ve takım kimlikleri son aşamada resmî şablon içinde tamamlanmalıdır. Prototipte ölçülen sonuçlar “ACTUAL_*” etiketiyle, gelecek hedefler ise “PLANNED/TARGET” olarak ayrılmıştır.

## 1. PROJE ÖZETİ

### 1.1. Proje Konusu ve Amacı
NSosyal Bağlam; sosyal medya platformlarında üç karar anını tek bir modüler yapay zekâ katmanında ele alan bir Sosyal Yapay Zekâ prototipidir. Proje; (i) Türkçe sosyal medya metinlerinde sarkazm, gündelik kullanım ve bağlam nedeniyle oluşabilecek moderasyon hatalarını azaltmayı, (ii) öneri sıralamasında yalnızca geçmiş popülerliğin etkisine bağlı görünürlük dengesizliğini sınırlayarak kaliteli fakat görece az görünür içerik üreticilerine kontrollü keşif fırsatı sunmayı, (iii) toplam ekran süresinden farklı olarak kaydırma hızı, içerik başına görüntüleme süresi ve hızlı geçiş oranı gibi oturum örüntülerini kullanarak isteğe bağlı dijital iyilik hâli önerileri üretmeyi amaçlamaktadır.

Ana inovasyon dikeyi **Sosyal Yapay Zekâ**dır. Kullanıcıya açıklanabilir moderasyon uyarıları, “Neden bunu görüyorum?” bilgisi ve isteğe bağlı mola önerileri nedeniyle proje aynı zamanda Kullanıcı Katılımı ve UI/UX hedefleriyle doğrudan ilişkilidir.

**Bu bölümde ne yaptık?** Projenin üç ayrı özellikten değil, yayın öncesi–dağıtım–tüketim zincirindeki üç karar anını yöneten tek bir “sağlıklı platform karar katmanı”ndan oluştuğunu tanımladık.

### 1.2. Proje Kapsamı ve Yöntemi
Prototip, resmî NSosyal uygulamasının yerine geçmez ve resmî NSosyal iç API erişimine sahip olduğunu iddia etmez. FastAPI tabanlı entegrasyon API’si, çalışan demo istemcisi, sentetik veri üzerinde eğitilen gerçek bir prototip ML moderasyon modeli, baseline ve fairness-aware sıralama motoru, davranışsal wellbeing kural motoru, testler ve ölçüm uçları içerir.

Moderasyon katmanında bağlamı koruyan Türkçe normalizasyon, kelime+karakter TF-IDF özellikleri ve Logistic Regression sınıflandırıcıları kullanılmıştır. Güvenlik sınıfı ile anlatım biçimi ayrı tahmin edilmiştir. Bu sürüm, BERTurk olarak sunulmamaktadır; Türkçe Transformer geçişi sonraki doğrulama aşamasıdır.

Adil Görünürlük katmanı; relevance, kalite proxy skoru, özgünlük, güncellik, göreli erken etkileşim ve önceki exposure sinyallerini birleştiren deterministik bir yeniden sıralayıcıdır. Küçük hesaplar otomatik olarak yükseltilmez; fairness düzeltmesi yalnızca kalite ve alaka kapısını geçen içeriklerde sınırlı biçimde devreye girer.

Denge katmanı; oturum süresi, kaydırma hızı, ortalama dwell time ve rapid-skip oranını kullanır. Tıbbi/psikolojik tanı üretmez. Yalnızca belirli davranış örüntüsü yeterli süre boyunca sürdüğünde isteğe bağlı mola önerisi üretir.

## 2. KATMA DEĞER VE YENİLİKÇİLİK

### 2.1. Problem Tanımı ve Mevcut Çözümler
Türkçe saldırgan dil tespiti üzerine SemEval-2020 kapsamında BERTurk dâhil çeşitli yaklaşımlar değerlendirilmiştir [1]. 2026 tarihli SarcasTürk çalışması, Türkçe sarkazm tespitinde başlık düzeyindeki bağlam bilgisinin yararlı olabildiğini ve bağlamlı BERTurk tabanlı yaklaşımın güçlü bir temel oluşturduğunu göstermektedir [2]. Bu sonuçlar, Türkçe sosyal medya moderasyonunda yalnızca kelime listelerine değil, bağlamsal modellere ihtiyaç olduğunu desteklemektedir.

Öneri sistemlerinde görünürlük yalnızca kullanıcının alaka ihtiyacıyla değil, sıralamadaki pozisyonların sağladığı exposure ile de ilişkilidir. Expected Exposure yaklaşımı, aynı relevans seviyesindeki öğelerin tekrarlanan sıralamalarda aldığı dikkatin ölçülebileceğini göstermektedir [3]. NSosyal Bağlam bu literatürü doğrudan “küçük hesap her zaman öne çıkar” biçiminde yorumlamamakta; relevance ve kalite korunurken aşırı geçmiş-popülerlik bağımlılığını sınırlayan bir prototip olarak kullanmaktadır.

Dijital iyilik hâli bileşeninde mevcut platformlardaki sabit zaman hatırlatıcılarından farklı olarak, oturum davranışının biçimi değerlendirilir. Bu yaklaşım ekran süresini tamamen reddetmez; ekran süresine ek bir davranış sinyali katmanı önerir.

### 2.2. Çözüm Fikri, Özgünlük ve Yerlilik
Projenin yenilik iddiası, moderasyon, adil sıralama veya mola hatırlatıcısının dünyada ilk kez geliştirilmesi değildir. Özgünlük; Türkçe bağlam farkındalığı, üretici exposure dengesini gözeten yeniden sıralama ve davranışsal dijital iyilik hâli bileşenlerinin tek bir NSosyal odaklı, açıklanabilir ve modüler mimaride birleştirilmesidir.

Yerli/yerelleştirilmiş yön, öncelikle Türkçe dil kullanımının ve NSosyal entegrasyon senaryosunun merkeze alınmasıdır. Raporda “yerli teknoloji” ifadesi yalnızca gerçekten kullanılan yerli bir model veya bileşen eklenirse kullanılmalıdır; mevcut prototipte yabancı açık kaynak kütüphaneler yerli teknoloji olarak gösterilmemektedir.

## 3. TEKNOLOJİ KULLANIMI

### 3.1. İzlenecek Yöntem, Altyapı ve Sürüm Kontrolü
Backend Python/FastAPI ile hazırlanmıştır. Kullanıcı arayüzü ayrı bir Node/Next.js sunucusu gerektirmeyen HTML/CSS/JavaScript istemcisidir ve FastAPI ile aynı origin üzerinden servis edilir. Bu sayede jüri demosunda tek kurulum ve tek port kullanılır. Testlerde pytest kullanılmaktadır. Windows hedefi Python 3.14’tür; bağımlılıklar CPython 3.14 desteği bulunan sürümlere güncellenmiştir.

Kaynak kod yerel Git deposunda sürüm kontrolü altındadır. Uzak GitHub/Bitbucket bağlantısı takım hesabına push edildikten sonra rapora eklenecektir. Uzak repo bağlantısı olmadan tam puan iddiası yapılmamalıdır.

### 3.2. Model ve Veri Doğrulama
Moderasyon prototipi, 79 sentetik ve etik amaçlı Türkçe örnekten oluşan küçük bir veri seti üzerinde çalışmaktadır. Veri eğitim/test ayrımında `random_state=42` ile %75/%25 stratified split kullanılmıştır. Kelime ve karakter n-gram TF-IDF özellikleri Logistic Regression ile sınıflandırılmıştır. Küçük veri nedeniyle sonuçlar yalnızca prototip doğrulaması olarak raporlanmaktadır.

Gerçek çalıştırmada elde edilen held-out sentetik test sonucu: **Macro-F1 = 0.4930**, weighted-F1 = 0.5693, macro precision = 0.4924 ve macro recall = 0.5033’tür. Bu değerler düşük/orta düzeyde olup modelin üretim moderasyonuna hazır olmadığını açıkça göstermektedir. Bu dürüst sonuç, teknik rapor aşamasında sentetik küçük veriyle çalışan sistemin sınırını kanıtlamaktadır; mentörlük aşamasında açık akademik Türkçe veri ve Transformer tabanlı modelle iyileştirme planlanmalıdır.

Aşırı öğrenme riskini azaltmak için train/test ayrımı, class-weight dengesi, sınırlı model karmaşıklığı ve deterministik split uygulanmıştır. Gelecekte Transformer eğitiminde validation izleme, early stopping ve weight decay gibi yöntemler planlanmaktadır; uygulanmadıkları sürece “kullanıldı” şeklinde raporlanmamalıdır.

### 3.3. Kullanıcı Deneyimi (UI/UX)
Arayüzde Akış, Gönderi/Moderasyon, Adalet Laboratuvarı, Denge, Şeffaflık Merkezi, İtiraz ve Jüri Paneli ekranları bulunmaktadır. Kullanıcı her kararın nedenini görebilir. Denge özelliği kullanıcı tarafından kapatılabilir. Form alanlarında semantik label, klavye odağı ve renk dışında metinsel durum göstergeleri kullanılmıştır.

Kullanılabilirlik testi için görev seti hazırlanmıştır; gerçek katılımcı verisi henüz mevcut değilse sonuç üretilmemelidir.

## 4. UYGULANABİLİRLİK

### 4.1. Verimlilik ve Etkinlik
Prototip moderasyon kararı yerel ortamda medyan yaklaşık **1.494 ms**, p95 yaklaşık **2.024 ms** sürede hesaplanmıştır. Bu ölçüm yalnızca yerel küçük model içindir; NSosyal üretim gecikmesi değildir.

Sıralama deneyinde baseline ilk-5 küçük üretici payı 0.20 iken fair sıralamada 0.40 olmuştur. Aynı sentetik deneyde ilk-5 ortalama relevance 0.846’dan 0.884’e yükselmiştir. Bu sonuç yalnızca deterministik sentetik aday kümesindedir ve gerçek kullanıcı davranışına genellenmemelidir.

### 4.2. Hedef Kitle
Birincil hedef kitle NSosyal kullanıcıları ve içerik üreticileridir. İkincil kullanıcı grubu platform moderasyon/ürün ekipleridir. Yeni/küçük üreticiler görünürlük katmanından, tüm kullanıcılar bağlam açıklaması ve wellbeing tercihleri üzerinden fayda görebilir.

### 4.3. Teknolojik Yenilik ve Uygulanabilirlik
Sistem modüler API servisleri biçiminde tasarlanmıştır. Üretim ölçeğinde kalıcı veritabanı, rate limit, kimlik doğrulama, dağıtık model servisleme, bot/fake-engagement savunması ve izleme altyapısı eklenebilir. Prototip bunların tamamını yapılmış gibi göstermemektedir.

## 5. YAYGIN ETKİ
NSosyal Bağlam’ın potansiyel toplumsal faydası; Türkçe içeriklerin daha bağlama duyarlı değerlendirilmesi, içerik üreticilerinin keşfedilebilirliğinde çeşitlilik, algoritmik kararların kullanıcıya açıklanması ve dijital kullanım üzerinde kullanıcı kontrolünün güçlendirilmesidir. Denge modülü özellikle “kullanıcıyı zorla uygulamadan çıkarma” yerine isteğe bağlı nudge yaklaşımını benimser.

## 6. SÜRDÜRÜLEBİLİRLİK

### 6.1. Ticarileştirme Potansiyeli ve İş Modeli
En gerçekçi model, NSosyal içinde platform yeteneği olarak kullanımdır. İkinci seçenek, Türkçe sosyal platformlara B2B API/SDK lisanslamasıdır. Tüketici aboneliği gibi projeyle uyumsuz bir gelir modeli önerilmemektedir.

### 6.2. Finansal, Teknik ve Sosyal Sürdürülebilirlik
Teknik sürdürülebilirlik; model/version kaydı, modüler servis yapısı ve veri yönetişimiyle desteklenebilir. Sosyal sürdürülebilirlik için itiraz, şeffaflık ve opt-out mekanizmaları korunmalıdır. Finansal sürdürülebilirlik üretim ölçeğinde model inference maliyeti, depolama ve moderasyon operasyonu birlikte hesaplanarak planlanmalıdır.

## 7. PROJE TAKVİMİ

| Dönem | İş paketi | Kilometre taşı |
|---|---|---|
| 22–24 Ağustos 2026 | P0 prototip, test, teknik rapor kanıtları | Teknik Rapor Teslimi — 24 Ağustos 17.00 |
| 2–7 Eylül 2026 | Veri/model iyileştirme, gerçek kullanılabilirlik testi, mentör geri bildirimi | Mentörlük çıktıları |
| 8–14 Eylül 2026 | BERTurk/alternatif Transformer karşılaştırması, demo sertleştirme, final sunumu | Final Sunumu — 14 Eylül 17.00 |
| 15–20 Eylül 2026 | Canlı demo prova, jüri savunması ve hata düzeltme | Canlı sunum — 20 Eylül |

## 8. TAKIM YAPISI
Resmî şablona uygun olarak isim/fotoğraf kullanılmadan rol bazlı tablo doldurulmalıdır. Örnek dağılım:

| Rol | Sorumluluk |
|---|---|
| Üye A — AI/NLP | Moderasyon veri/model, metrik ve etik |
| Üye B — Backend/Recommendation | API, ranking, test ve veri akışı |
| Üye C — UI/UX/Product | Arayüz, kullanıcı akışları, erişilebilirlik, demo |

Takım kişi sayısına göre roller birleştirilebilir.

## 9. KAYNAKÇA — Doğrulanmış Başlangıç Listesi
[1] Ozdemir, A., Yeniterzi, R. (2020). SU-NLP at SemEval-2020 Task 12: Offensive Language IdentifiCation in Turkish Tweets. Proceedings of the Fourteenth Workshop on Semantic Evaluation, 2171–2176. DOI: 10.18653/v1/2020.semeval-1.288.

[2] Metin, N. A., Yılmaz, S., Erdoğdu, O. E., Meydan, E. S., Sümer, O., Keküllüoğlu, D. (2026). SarcasTürk: Turkish Context-Aware Sarcasm Detection Dataset. Proceedings of SIGTURK 2026, 61–71. DOI: 10.18653/v1/2026.sigturk-1.6.

[3] Diaz, F., Mitra, B., Ekstrand, M. D., Biega, A. J., Carterette, B. (2020). Evaluating Stochastic Rankings with Expected Exposure. arXiv:2004.13157.
