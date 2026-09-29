# deepin.space: yapılanlar ve kararlar

Bu belge 26–29 Eylül 2026 arasında deepin.space sitesinde yapılan işleri, alınan kararları ve açık kalan konuları özetler. Sitenin nasıl üretildiği ve düzenlendiği README.md dosyasında anlatılıyor.

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

## Alınan kararlar

- **Adres yapısı:** Alt sayfalar alt alan adı değil yol olarak yayınlanıyor, örneğin deepin.space/risk.
- **Dil:** Türkçe varsayılan dil ve kökte duruyor; İngilizce /en/ altında. Terimlerde karma yaklaşım uygulanıyor.
- **Tasarım:** Açık renkler kullanılıyor. Ana renk yeşil (#158867), vurgu rengi mint (#28DCA8). Karanlık mod da destekleniyor.
- **Müşteri referansları:** Her müşteri gerçekte ulaştığı olgunluk seviyesiyle gösteriliyor: sözleşmeli, ürüne gömülü/kurulumda ya da canlı kullanımda.
- **Veri mesajı:** Deepin müşteri verisini almıyor. Kurulumlar arasında taşınan şey Investigation şablonları, bağlantı kalıpları, iş akışları ve değerlendirmeler.

## Açık konular

- **deepin.security demosu:** `security/demo/` yayına çıkınca herkese açık olur (arama motorlarına kapalı). /security sayfasından demoya bağlantı henüz verilmedi.
- **Türkçe metinler:** Tamamı gözden geçirilmeli, özellikle risk demo metinleri ve müşteri durum etiketleri.
- **Fontlar:** Eski siteye erişilemediği için Poppins tahmini yapıldı. Eski siteyle karşılaştırılıp doğrulanmalı.
- **Müşteri logoları:** Şu an isimler gösteriliyor. Logo dosyaları gelirse `proof.show_logos` açılabilir.
- **Talep formu:** Şu an e-posta uygulamasını açıyor. Bir form servisi bağlanırsa `form.endpoint` alanına adresi yazmak yeterli.
- **Yönlendirme:** Eski risk.deepin.space adresi deepin.space/risk adresine 301 ile yönlendirilmeli.
- **Energy:** Bu sayfa "keşif aşamasında". Somut bir müşteri ya da vaka oluştuğunda içeriği güncellenmeli.
