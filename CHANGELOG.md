# deepin.space: yapılanlar ve kararlar

Bu belge 26–30 Eylül 2026 arasında deepin.space sitesinde yapılan işleri, alınan kararları ve açık kalan konuları özetler. Sitenin nasıl üretildiği ve düzenlendiği README.md dosyasında anlatılıyor.

## Özet

- Site, Deepin Commercial Strategy v0.7 belgesine göre sıfırdan yazıldı. Açık renkli, sade bir tasarım seçildi.
- Anlatım "Investigation önce" yaklaşımına göre kuruldu. Ziyaretçi önce Deepin'in hangi Investigation'ları yürüttüğünü görüyor, Space'ler ise bu Investigation'ların tekrarlanmasıyla oluşan alanlar olarak anlatılıyor.
- Sayfalar: ana sayfa, deepin.risk, deepin.finance, deepin.security, deepin.energy.
- Varsayılan dil Türkçe. İngilizce sürüm /en/ altında. Ziyaretçinin seçtiği dil sayfalar arasında korunuyor.
- Alt sayfalar alt alan adı yerine yol olarak yayınlanıyor: deepin.space/risk, deepin.space/finance vb.

## Zaman çizelgesi

### 26 Eylül

**İlk sürüm** (`1b8f805`)
- Yeni ana sayfa, /risk ve /finance sayfaları eklendi.
- Eski siteye erişilemediği için fontlar tahmin edildi: Poppins (metin) ve JetBrains Mono (etiketler).
- Alt sayfalara ana sayfaya dönüş bağlantısı eklendi.
- Ana sayfadaki Space kartları alt alan adına değil /risk ve /finance yollarına gidiyor.

**Görsel ritim** (`ef6a2a6`)
- Bölümler arasına hafif ton farkları ve noktalı geçişler eklendi.
- Süreç adımlarının üzerinden geçen animasyonlu bir sinyal çizgisi eklendi. Adım listeleri metro hattı görünümüne getirildi.

**V2: Investigation önce yapı** (`d900f7d`)
- Ana sayfa, gelen brife göre 8 bölüm olarak yeniden kuruldu:
  - hero'da canlı akan örnek Investigation,
  - Investigation kataloğu,
  - nasıl çalışır,
  - kanıt arayüzü,
  - müşteri referansları,
  - Space'lerin oluşumu,
  - kurumsal altyapı,
  - kapanış.
- İçerik veri dosyalarına taşındı: Investigation'lar, Space'ler, müşteriler ve durum etiketleri tek yerden yönetiliyor.
- /security ve /energy "keşif aşamasında" sayfaları olarak eklendi.

**deepin.risk yeniden kuruldu** (`3881c47`, `40820f9`)
- Sayfa Company Investigation'ın yaşam döngüsünü anlatan 10 bölüme ayrıldı.
- Etkileşimli demo eklendi:
  - olay zaman çizelgesi,
  - ilişki grafiği,
  - "ne değişti" karşılaştırmaları,
  - kanıt zinciri,
  - onayla, reddet ya da araştırmaya devam et adımları.
- İki adımlı talep formu eklendi. Mobilde alttan açılan panel olarak çalışıyor.

**Ana sayfa karşılaştırması: "Keep the decision. Lose the investigation work."** (`b0b76fa`)
- "Bugün" ve "Deepin ile" sütunlarından oluşan karşılaştırma eklendi.

### 27 Eylül

**Karşılaştırma dengelendi** (`8fb602d`)
- İki sütun eşit yükseklik ve genişliğe getirildi.
- İnsan tarafındaki 8 görev iki sütunlu bir ızgaraya alındı. Arka plan sadeleştirildi.

**"Düzenli kaos" karşılaştırması** (`6702511`)
- İnsan tarafı, sistemler arasında gidip gelen bir yol olarak çizildi:
  - duraklar: CRM, Ticaret Sicili, PDF, e-posta, tablo, tarayıcı, yeniden Ticaret Sicili, notlar;
  - geri dönüşler ve sürtünme notları eklendi.
- Deepin tarafında aynı sistemler tek bir kutunun içinde toplanıyor.
- Sayfanın diğer bölümlerine dokunulmadı.

**Türkçe destek** (`5f7e389`)
- Türkçe kökte (deepin.space), İngilizce /en/ altında yayınlanıyor.
- Üst menüde ve alt bilgide TR / EN düğmesi var. Düğme, aynı sayfanın diğer dildeki karşılığına götürüyor.
- Terminoloji "karma" yaklaşımla belirlendi: metin Türkçe, Investigation, Space ve ürün adları İngilizce.
- Türkçe sayfalardaki İngilizce terimler otomatik olarak işaretleniyor. Böylece büyük harfli etiketlerde "INVESTİGATİON" gibi hatalı yazımlar oluşmuyor.
- Arama motorları için hreflang ve og:locale etiketleri eklendi.
- Tüm sayfalar 360 px genişlikte taşmadan açılacak şekilde kontrol edildi.

### 28 Eylül

**Türkçe metin düzeltmeleri ve dil tercihi** (`8b85d7a`)
- TR/EN düğmesiyle seçilen dil tarayıcıda saklanıyor. Ziyaretçi sonraki sayfalarda aynı dilde kalıyor.
- Metin düzeltmeleri:

| Önce | Sonra |
|---|---|
| "sizin olarak kalır" (risk ve ana sayfa) | "her zaman sizindir" |
| "Aynı Company Investigation'ın dört boyutu…" | "Company Investigation bu dört boyuta bakar ve şirket her değiştiğinde aynı soruları yeniden sorar." |
| "Bana skoru söyleme. Nedenini göster." | "deepin.risk yalnızca skoru değil, nedenini de verir." |
| Finance hero başlığı | "Chargeback Investigation. Kanıtıyla birlikte." |
| "kart şeması sürelerine karşı yarışarak" | "kart şemasının belirlediği süreler dolmadan" |
| "Vakadan karara hazır hale" | "Vakadan karara" |
| "bir öncekine kurulan" | "bir öncekinde kurulan" |
| "bir kişiye gerek kalmadan" | "insan müdahalesi olmadan" |

### 29 Eylül

**deepin.security sayfası ilk gerçek denemeye göre yeniden yazıldı**
- Üst bölümün başlığı, giriş metni ve düğmeleri aynı kaldı. Sağdaki örnek vaka, bir bankadaki ilk denemede bulunan gerçek bir vakadan uyarlandı; kurum ve kişi bilgileri, sayılar değiştirildi.
- Örnek vakaya davranış grafiği eklendi: birimdeki her kişi bir nokta; 27 kişi "olağan" bölgede, sapan 8 bilgisayar ayrı ve hareketli. Grafik sayfanın içinde satır içi SVG; hareket kapatılmış tarayıcılarda durur.
- "Neyi inceler" listeleri sayfanın gerçekten yaptığına göre düzeltildi: tehdit istihbaratı, geçmiş olaylar ve otomatik yanıt çıkarıldı; okunan kayıtlar, birleştirilen kurum bilgileri ve sunulan çıktılar girdi → çıktı kartları olarak gösteriliyor.
- Yeni bölümler: Sorun, Farkı (kural ile / Deepin ile), Nasıl çalışır (8 adım), Neleri bulur (8 vaka türü), Mevcut sistemlerinizle, Kanıt, Güven. Menü bu bölümlere göre genişletildi.
- "Neredeyiz" bölümü ilk denemeyi anıyor (banka adı ve sayı yok); durum etiketi "Keşif aşamasında" olarak kaldı.
- Güven bölümündeki adımlar ve kurumsal özellikler sayfaya özel: `src/content/security.tr.json` ve `security.en.json`.
- Metinler jargonsuz yazıldı ("makul açıklama", "kaydın aslı" gibi). İngilizce sürüm aynı içerikle.

**deepin.security platform demosu ve video aracı** (`security/demo/`)
- deepin.security inceleme ekranının Deepin platformu görünümüyle çalışan demosu eklendi: 16 inceleme, 45 uyarı, graf, kanıt ve ham kayıt, MITRE, ağ geçişleri, kişi sorgusu, asistan. Veri tamamen kurgusal ("Meridyen Finans"); kurum, kişi, sayı ve adres planı hiçbir gerçek kuruma dayanmıyor. Türkçe ve İngilizce.
- Demo kendi kendine gezen bir tur moduyla videoya çekilebiliyor (`?tur=1`). Her video bir senaryo dosyası (`kaynak/senaryolar/`); kaydedici başlıksız Chrome ile kare kare çekiyor, Türkçe ve İngilizce ayrı video, altyazılı 1080p ya da altyazısız 4K. Altyazıdaki her sayı veriyle denetleniyor.
- Nasıl kullanılacağı: `security/demo/VIDEO_REHBERI.md`. Depoda iki küçük örnek video (720p: tam ürün turu 3,3 MB, grup davranışı kesiti 0,9 MB) ve önizleme levhaları var; 1080p/4K videolar depoya konmuyor, yeniden üretiliyor.

**deepin.security tanıtım videosu**
- /security ve /en/security sayfalarına, üst bölümle "Sorun" bölümü arasına 72 saniyelik tanıtım videosu eklendi: Türkçe sayfada Türkçe, İngilizce sayfada İngilizce. Seslendirme ElevenLabs ile, müzik özgün (kodla üretildi). Kapak görüntüsü ve seslendirmenin altyazısı (WebVTT) var; video kendiliğinden oynamaz.
- Dosyalar `assets/video/` altında (deepin-security-tr/en: .mp4, .jpg, .vtt; iki video toplam ~27 MB).
- `build.py`: `src="assets/` gibi `poster="assets/` yolları da sayfanın derinliğine göre düzeltiliyor (tek satır).

**deepin.security: örnek vaka kurgusal, tanıtım videosu yenilendi**
- Üst bölümdeki örnek vaka tamamen kurgusal hâle getirildi: sayılar değişti (aynı birimde 5 bilgisayar, 22 kişilik birim, 3 günlük kayıt, 100'den fazla iç adres, 140'tan fazla kapı, denemelerin %91'i engellendi) ve alt not "Kurgusal örnek vaka; kurum, kişiler ve sayılar temsilidir." oldu. Davranış ölçümü grafiği yeni sayılarla yeniden üretildi.
- Tanıtım videosu iki dilde yeniden çekildi. Demo verisi kurgusal bir haftaya (14-20 Eylül 2026), genel ürün adlarına ve kurgusal servis ve birim adlarına taşındı; MITRE ATT&CK sayfasında seçili teknik kutusunun alt satırının kesilmesi düzeltildi. Seslendirme, müzik, kapak ve altyazı aynı.
- `security/demo/` aynı veriyle güncellendi (demo sayfası, iki örnek video, önizlemeler, belgeler). Kendi senaryosunu yazmak isteyen için tanıtım videosunun senaryosu (`kaynak/senaryolar/reklam.json`) ve seslendirme ile müzik araçları (`kaynak/ses_yap.py`, `kaynak/ses_ekle.swift`) eklendi; kullanımı `VIDEO_REHBERI.md` içinde. Ses kayıtları depoya konmuyor.
### 30 Eylül

**deepin.security sayfasından demoya bağlantı**
- /security ve /en/security sayfalarında "Neredeyiz" bölümünün altına küçük bir not eklendi. Not, demoyu yeni sekmede açıyor: Türkçe sayfadan `security/demo/`, İngilizce sayfadan `security/demo/en/`.

**Deepin Harness sayfası ve ana sayfadaki Harness bölümü**
- Yeni sayfa: /harness ve /en/harness. Harness, Investigation ve Space'lerin altında çalışan kurumsal ortam olarak anlatılıyor; agent framework'ü olarak değil.
- Bölümler: Sorun (agent kurmak kolay, organizasyon kurmak zor), organizasyon modeli (Rol, Yetki, Politika · Kısıt, Agent, Görev, Yetenek, Araç, Servis, Bilgi), Organizational Reasoning, model çağrısından yönetilen işe, iş birliği (temsilî Company Investigation örneği), yönetişim (üç örnek talepli kapı), bilgi ve hafıza, değerlendirme, izlenebilirlik (tıklanabilir iz, kurgusal şirket), Harness ve Space'ler, kullanımdaki referanslar, Ar-Ge ("TÜBİTAK destekli Ar-Ge"), kapanış.
- Kararlar: Galactica adı hiçbir yerde geçmiyor. Organizasyon modeli kavramsal; koddaki sınıfları anlatmıyor. Yetenek ≠ Araç ve Yetki ≠ Politika ayrımı sayfada açıkça yazıyor. Müşteri referansları mevcut olgunluk etiketleriyle, veri üzerinden gösteriliyor; yeni iddia eklenmedi.
- Ana sayfada Spaces'ten sonraki "Altyapı" bölümü Harness bölümüne dönüştürüldü: "Her Investigation'ın arkasındaki organizasyon.", kompakt diyagram (Organizasyon · Bilgi · Yönetişim → yapay zekâ ile yürütülen iş → deepin.risk / deepin.finance) ve "Deepin Harness'ı keşfedin →". Sağdaki kurumsal özellikler ve "Verileriniz sizde kalır" notu aynen duruyor.
- Ana menüye "Harness" eklendi (Kurumsal'dan sonra); alt bilgideki Şirket sütununa "Deepin Harness" bağlantısı eklendi. Dil tercihi Harness sayfasında da korunuyor.
- Menü tüm sayfalarda 1160 px çerçeveye sığacak şekilde sıkılaştırıldı (bağlantı aralığı ve yazı boyutu biraz küçüldü; menü 1180 px altında gizleniyor). Önceden İngilizce risk ve security sayfalarında menü taşıyordu, o da düzeldi.
- Türkçe metinde İngilizce terimlerin etrafında düğme ve etiketlerde oluşan fazladan boşluk giderildi ("Bize bir  Investigation  getirin" gibi).

## design/organism dalı (deneysel, main'e birleştirilmedi)

**DEEPIN / ORGANISM** sanat yönetimi denemesi. Ana fikir: "Organizasyon bir fiildir." Yazı tipleri (Poppins, JetBrains Mono) ve renkler aynı; kullanım kuralları sıkılaştırıldı: nane = sinyal, yeşil = sistemin kurduğu yapı, kehribar = yalnızca insan, koyu = altta yatan (Harness).

- **Ana sayfa bir yolculuk:** sinyal (bir olay gelir) → Investigation kendini organize eder (dağınık sistemler kaynaklara, kaynaklar kanıta, kanıt bulguya dönüşür; kaydırmayla ilerler) → karar anı ("Karar sizindir": gerekçe, kanıt fişleri, Onayla / Reddet / Araştırmaya devam et) → Investigation dizini → iki Space, tek dil (deepin.risk ve deepin.finance aynı adımlarla yan yana) → müşteriler → zemin kalkar, altında Deepin Harness → başlangıç.
- **Harness sayfası:** üst bölüm koyu "altta yatan" katman, canlı organizasyon topolojisi; Organizational Reasoning artık olay seçmeli ve canlı: her olay farklı rolü, yetkiyi, yeteneği, politika sınırını ve yeni durumu gösterir. Ayrı iş birliği bölümü kaldırıldı (canlı akıl yürütme devretme ve iş birliğini zaten gösteriyor).
- **Risk ve Finance:** aynı evrene alındı (menü, tipografi, ince çizgiler); kardeş ama kopya değil: risk'te ilişki halkaları, finance'te defter çizgileri ve tek aralıklı tutarlar.
- **Menü:** tüm sayfalarda tek genel menü (Deepin · deepin.risk · deepin.finance · Harness · Müşteriler); dar ekranlarda açılır menü. Ana sayfada geniş ekranlarda sayfanın hangi aşamasında olduğunuzu gösteren ince bir "durum rayı".
- **Hareket ve erişilebilirlik:** hareket azaltma tercihinde sahneler adım düğmeleriyle, hareketsiz çalışır; JavaScript olmadan son durum görünür. Yeni bağımlılık yok; sahneler DOM + SVG ile, az sayıda öğeyle çiziliyor.

**Son hassas geçiş (yeniden tasarım yok)**
- Metin: Risk'te "Deepin bir risk skoru üretmekle yetinmez…" ve "Karar verir"; Finance'te kart şeması süreleri, "Vakadan karara.", "insan onayını koruyarak" düzeltmeleri; Harness Ar-Ge metninde "Organizational Reasoning" terimi; "Onayladınız", "Bir örneği izleyin"; Harness referans cümlesi "…Investigation'larla şekilleniyor" (daha temkinli).
- Görsel: ana sayfadaki müşteri satırı ince bir çizgiyle ayrılıp kanıt gibi okunuyor; Harness'ta Organizasyon, Organizational Reasoning ve yönetilen iş öne çıktı, bilgi/değerlendirme/izlenebilirlik ikincil katman oldu; tabletlerde Investigation sahnesi düzeldi; mobilde başlık satırı ve Finance durum etiketi taşmıyor.
- Hareket: yalnızca "Deepin onu yürütür" satırı gelir; sinyal daha seyrek atar; kaydırma ipucu üç kez oynar; hareket azaltmada Harness topolojisindeki sinyal de durur.
- Erişilebilirlik: kanıt vurgusu klavyeyle de çalışır; küçük etiketlerin kontrastı 4.0'dan 5.85'e çıktı.
- Kullanılmayan eski Harness bileşenleri ve stilleri kaldırıldı.

**Önizlemede sayfa geçişleri** (`76ca480`)
- Önizleme çerçevesinde alt sayfalar her zaman en baştan açılıyor; geri gelince tıklanan bağlantıya dönülüyor.

**deepin.risk revizyonu birleştirildi** (`risk-sayfa-revizyon` dalından, Özge Miroğlu)
- Risk sayfasının içeriği ve bileşenleri o daldan alındı: "Her şirkete daha derinden bakın." üst bölümü ve katmanlı vaka kartı, KVKK/BDDK güven şeridi, tek kurgusal vaka (Tedarikçi A.Ş.), roller şeridi ve kanıt kartı, sekmeli "Ne değişti?", katma değer zinciri, sektör kartları, müşteri yorumları, "Nasıl başlarsınız" adımları; bu sayfada Investigation yerine İstihbarat/Intelligence, deepin.risk yerine Deepin Risk.
- ORGANISM tasarımı korundu: genel menü (o daldaki dört öğeli risk menüsü yerine), tipografi, ince çizgiler ve risk üst bölümündeki ilişki halkaları.
- Önceki hassas geçişteki "Karar verir" / "Make the decision" düzeltmesi korundu.

## Alınan kararlar

- **Adres yapısı:** Alt sayfalar alt alan adı değil yol olarak yayınlanıyor, örneğin deepin.space/risk.
- **Dil:** Türkçe varsayılan dil ve kökte duruyor; İngilizce /en/ altında. Terimlerde karma yaklaşım uygulanıyor.
- **Tasarım:** Açık renkler kullanılıyor. Ana renk yeşil (#158867), vurgu rengi mint (#28DCA8). Karanlık mod da destekleniyor.
- **Müşteri referansları:** Her müşteri gerçekte ulaştığı olgunluk seviyesiyle gösteriliyor: sözleşmeli, ürüne gömülü/kurulumda ya da canlı kullanımda.
- **Veri mesajı:** Deepin müşteri verisini almıyor. Kurulumlar arasında taşınan şey Investigation şablonları, bağlantı kalıpları, iş akışları ve değerlendirmeler.

## Açık konular

- **deepin.security demosu:** `security/demo/` herkese açık (arama motorlarına kapalı). /security sayfasından küçük bir notla bağlantı veriliyor.
- **Türkçe metinler:** Tamamı gözden geçirilmeli, özellikle risk demo metinleri ve müşteri durum etiketleri.
- **Fontlar:** Eski siteye erişilemediği için Poppins tahmini yapıldı. Eski siteyle karşılaştırılıp doğrulanmalı.
- **Müşteri logoları:** Şu an isimler gösteriliyor. Logo dosyaları gelirse `proof.show_logos` açılabilir.
- **Talep formu:** Şu an e-posta uygulamasını açıyor. Bir form servisi bağlanırsa `form.endpoint` alanına adresi yazmak yeterli.
- **Yönlendirme:** Eski risk.deepin.space adresi deepin.space/risk adresine 301 ile yönlendirilmeli.
- **Harness metinleri:** Türkçe ve İngilizce metinler gözden geçirilmeli; özellikle yönetişim kontrolleri ve Ar-Ge bölümü.
- **Energy:** Bu sayfa "keşif aşamasında". Somut bir müşteri ya da vaka oluştuğunda içeriği güncellenmeli.
