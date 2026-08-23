# Jüri Savunma Notları

1. **Bu zaten Instagram'da yok mu?** Moderasyonun kendisi yeni değil; özgünlük Türkçe bağlam + exposure-aware görünürlük + davranış tabanlı wellbeing'in tek NSosyal karar katmanında birleştirilmesi.
2. **Neden üç modül?** Aynı platform yaşam döngüsünün üç karar anını çözüyor: yayın öncesi, dağıtım, tüketim.
3. **Proje fazla geniş değil mi?** Prototipte her modül küçük, ölçülebilir ve modüler; üretim kapsamı ayrı tutuldu.
4. **Gerçek veri nerede?** Teknik rapor sürümünde sentetik prototip verisi kullanıldı ve açıkça işaretlendi; resmî NSosyal verisi kullanıldığı iddia edilmiyor.
5. **BERTurk nerede?** Şu an çalışan sürüm internet bağımsız TF-IDF+LogReg. BERTurk üretim/mentörlük yol haritasıdır; varmış gibi gösterilmez.
6. **Türkçe bağlam iddianızı nasıl kanıtlıyorsunuz?** Türkçe karakter, emoji, tekrar, sarkazm ve mecaz örneklerine ayrı testler; lexical baseline ve bağlamsal sınıflandırıcı karşılaştırma altyapısı.
7. **Fairness'i kim tanımlıyor?** Mutlak eşitlik değil; relevance/quality tabanı korunurken exposure dengesizliğini sınırlayan açık bir ürün tanımı.
8. **Büyük hesapları cezalandırıyor musunuz?** Hayır. Testte yüksek alakalı kaliteli büyük hesapların bastırılmaması regression kriteridir.
9. **Küçük hesap spam üretirse?** Quality gate nedeniyle yalnızca küçük olmak boost sebebi değildir.
10. **Algoritma manipüle edilebilir mi?** Prototip riskidir; üretimde bot/fake engagement tespiti gerekir.
11. **Wellbeing kullanıcıyı profilliyor mu?** Tıbbi profil yok; oturum özet davranışları ve opt-out vardır.
12. **Neden ekran süresi yetmiyor?** Aynı süre, farklı kullanım biçimleri gösterebilir; prototip davranış örüntüsünü ayırır.
13. **Tanı koyuyor musunuz?** Hayır; tıbbi/psikolojik tanı kesin biçimde kapsam dışıdır.
14. **Model yanlışsa?** Belirsizlikte uyarı/inceleme ve itiraz akışı vardır.
15. **Gizlilik?** Veri minimizasyonu ve gereksiz sensör/özel mesaj verisi toplamama ilkesi.
16. **NSosyal'e gerçekten entegre mi?** Hayır; entegrasyona uygun API prototipidir.
17. **Bugün ne gerçekten çalışıyor?** FastAPI servisleri, aynı origin üzerinden çalışan sosyal medya UI’si, yerel ML moderasyon, fair ranker, wellbeing motoru, itiraz/açıklama akışları, testler ve metrik uçları.
18. **Üretime hazır mı?** Hayır; prototiptir. Üretimde ölçek, gerçek veri doğrulama, güvenlik ve operasyon gerekir.
19. **Lise ekibi bunu savunabilir mi?** Her modelin input-process-output'u ve her skorun formülü dokümante edilmiştir.
20. **En büyük limit?** Gerçek NSosyal verisi ve büyük ölçek kullanıcı doğrulamasının henüz bulunmaması.
