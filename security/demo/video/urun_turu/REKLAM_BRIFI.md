# deepin | security: tanıtım videosu brifi

Bu dosya, ham ürün görüntüsünden **lansman tarzı bir tanıtım videosu** kuracak kişiye ya da yapay zekâ aracına verilir.
**Bu kurgunun sessiz, ekran yazılı hâli hazır:** `kaynak/senaryolar/reklam.json` → `python3 kaynak/video_cek.py --senaryo reklam --dil tr`
(ve `--dil en`), çıktı `video/reklam/tr.mp4`, ~73 sn, 1080p. Dış araç yalnız müzik ve seslendirme eklemek için gerekir (§5).
Hedef: startup'ların ürün tanıtımları gibi, **60-75 saniye**, vurucu ekran yazıları ve anlatan bir seslendirme, 16:9.

## 1. Paket

Videolar depoda tutulmaz (büyük dosya, yeniden üretilebilir). Bu klasörün iki üst dizininden (`security/demo/`) üretmek için:
`python3 kaynak/video_cek.py --senaryo urun_turu --dil tr --temiz` (4K, ~10 dk) · `--dil en --temiz` · altyazılı referans için `--temiz`'siz.
Ayrıntı: `VIDEO_REHBERI.md`.

| Dosya | Ne |
|---|---|
| `tr_temiz.mp4` | **Montajın ham maddesi.** Türkçe arayüz, altyazısız, çerçevesiz, 3840×2160 (4K), 30 kare/sn, ~96 sn. 4K olduğu için yakınlaştırmada bile net kalır |
| `en_temiz.mp4` | Aynısı, İngilizce arayüz |
| `tr.mp4`, `en.mp4` | Referans: bizim altyazılı sürümümüz (1080p). Akışı görmek için |
| `tr_temiz.srt`, `en_temiz.srt` | Sahne sahne altyazı metni ve zamanları (temiz görüntüyle aynı zaman çizelgesi) |
| `../../assets/deepin-logo-platform.png` | Logo (nane rengi "deepin"). Yanına ince nane çizgi ve "security" yazılır |

**Marka:** yazı tipi **Poppins** (başlık 600-700, gövde 400-500, "security" 300) · nane `#13dca7` (vurgu), logo çizgisi `#00e695` ·
koyu `#143037` ve zemin `#0d2126` · açık zemin beyaz. Ton: sakin, kendinden emin, abartısız.

## 2. Değişmez kurallar (araca da aynen verin)

1. **Ürün görüntüsü yeniden üretilmez.** Yalnız kesme, yakınlaştırma/kaydırma (zoom/pan), hız değişimi, geçiş ve üstüne yazı/grafik.
   Yapay zekâyla "videoyu yeniden oluşturan" araçlar (metinden videoya, videodan videoya) ekrandaki yazıları ve sayıları bozar;
   bunlar **yalnız soyut açılış/arka plan** için kullanılabilir, ürün görüntüsüne asla uygulanmaz.
2. **Yeni sayı ya da iddia uydurulmaz.** Kullanılabilecek sayılar yalnız bunlar: 45 uyarı · 16 inceleme · 4 yüksek öncelikli ·
   3 kayıt kaynağı · 22 kişilik grup · 3 ödeme ve kart ağı · 2 engellenen yönetim ağı · 8 Nisan (ayrılış) · 11 ağ bölgesi · 5 kayıt kaynağı.
   "%90 daha hızlı", "binlerce müşteri" gibi ifade yok.
3. **"Yapay zekâ saldırıyı tespit etti" denmez.** Ürün kanıta dayalı inceleme yapar; asistan incelemenin kendi kayıtlarından cevap verir
   ve kayıt söylemiyorsa "söylemez" der. Bu dürüstlük videonun ana mesajlarından biri.
4. **Kapanış:** logo ve slogan; alt satırda not yok.
5. Metinlerde uzun tire (—) kullanılmaz; virgül ya da nokta.

## 3. Senaryo (Türkçe), ~70 sn

Zaman kodları **temiz görüntünün** zamanıdır (dakika:saniye). "Yakınlaştır" satırları önerilen kamera hareketidir.

| Video | Klip (temiz görüntüde) | Ekran yazısı (vurucu, büyük) | Seslendirme |
|---|---|---|---|
| 0-4 sn | Klip yok: koyu zemin, yazı kelime kelime gelir | **Uyarı çok.** / **Zaman az.** | Her gün yeni uyarılar. Hep aynı soru: hangisi gerçekten önemli? |
| 4-7 | Logo açılışı | **deepin \| security** | deepin security, kayıtlarınızı kanıtlı incelemelere dönüştürür. |
| 7-13 | 00:00.7-00:07.0 ana sayfa; imleç öncelik sekmelerinde, sonra günlük özet açılır. Yakınlaştır: 00:03.7'den sonra sol paneldeki özet | **45 uyarı. 16 inceleme.** / **Önce 4'ü.** | Uyarıları tek tek değil, hikâye olarak görün: 45 uyarı, 16 inceleme ve hemen bakılması gereken 4 tanesi. |
| 13-19 | 00:07.4-00:13.5 Kerem Tuncer incelemesi açılır. Yakınlaştır: özet kutusu (00:09.7) | **İşten ayrıldı.** / **Hesabı hâlâ açık.** | Bir çalışan 8 Nisan'da ayrılmış. Hesabı hâlâ açık ve 3 ayrı kayıt kaynağı aynı kişiyi gösteriyor. |
| 19-25 | 00:14.0-00:20.5 graf açılır: kişi, benzer görevdeki 22 çalışan, gidilen ağlar | **O nereye gitti,** / **grubu nereye gidiyor.** | Graf, kişiyi benzer görevdeki 22 çalışanla yan yana koyar. |
| 25-31 | 00:21.1-00:27.3 turuncu ağlar; 00:22.3'te tıklanır. Yakınlaştır: 00:24.0'dan sonra sağ alttaki "hiçbiri" | **Grubundan kimsenin gitmediği** / **3 ödeme ağı.** | Grubundan kimsenin gitmediği 3 ödeme ve kart ağına yalnız o ulaşmış. |
| 31-34 | 00:27.6-00:31.0 kırmızı kesik ağ tıklanır | **Denedi. Engellendi.** | Yönetim ağlarını da denemiş; istekler engellenmiş. |
| 34-39 | 00:34.6-00:39.5 ham kayıt kutusuna iner. Yakınlaştır: koyu kayıt satırları | **İddia değil,** / **kanıt.** | Her bulgunun altında ham kayıt satırları var. Tahmin yok, kayıt var. |
| 39-49 | 00:42.1-00:51.5 soru yazılır, cevap gelir. Yakınlaştır: sol paneldeki iki sütunlu tablo | **Sorun.** / **Cevap kayıttan gelsin.** / **Saldırı mı? Kayıt tek başına söylemez.** | Asistana sorun; cevap incelemenin kendi kayıtlarından gelir. Saldırı mı diye sorduğunuzda, kaydın bunu tek başına söyleyemeyeceğini açıkça söyler ve iki ihtimali yan yana koyar. |
| 49-55 | 00:55.0-01:02.5 MITRE: iki teknik seçilir, ortak varlık kutusu. Yakınlaştır: 00:59.6 kutu | **Tek hesap.** / **İki ATT&CK aşaması.** | MITRE ATT&CK üzerinde aynı hesap hem ilk erişim hem yanal hareket aşamasında görünüyor. |
| 55-63 | Hızlı kesitler, her biri ~2 sn: 01:05.5 kişi sorgusu · 01:15.2 ağ geçişleri matrisi · 01:23.7 uyarı araması · 01:30.6 veri kaynakları | **Kişi.** · **Ağ.** · **Uyarı.** · **Kaynak.** | Kişinin haftası, ağlar arası trafik, bütün uyarılar ve 5 kayıt kaynağı tek ekranda. |
| 63-66 | 01:31.8-01:34.8 bağlam kartları | **Kayıtlarınız kurum dışına çıkmaz.** | Ve kayıtlarınız kurumunuzdan dışarı çıkmaz. |
| 66-72 | Kapanış kartı (koyu zemin) | **deepin \| security** / Güvenlik kayıtlarını kanıtlı incelemelere dönüştürür. | deepin security. Uyarıdan kanıta. |

Müzik: sakin başlayan, 7. saniyede (logo) ve 19. saniyede (graf) yükselen elektronik/ambient. Seslendirme yoksa ekran yazıları tek başına yeter;
yazılar 1080p'de en az 60 px, bir seferde en çok 6 kelime.

## 4. Script (English), ~70 s

| Video | Clip (clean footage) | On-screen text | Voice-over |
|---|---|---|---|
| 0-4 s | No clip: dark background, words appear one by one | **Too many alerts.** / **Too little time.** | New alerts every day. Always the same question: which ones actually matter? |
| 4-7 | Logo reveal | **deepin \| security** | deepin security turns your logs into evidence-backed investigations. |
| 7-13 | 00:00.7-00:07.0 home, priority tabs, daily brief. Zoom: brief in the left panel after 00:03.7 | **45 alerts. 16 investigations.** / **4 first.** | See stories, not single alerts: 45 alerts, 16 investigations, and the 4 that need you now. |
| 13-19 | 00:07.4-00:13.5 Kerem Tuncer investigation. Zoom: summary box at 00:09.7 | **Left the company.** / **Account still active.** | An employee left on April 8. The account is still active, and 3 separate log sources point at the same person. |
| 19-25 | 00:14.0-00:20.5 graph opens: person, 22 peers, networks reached | **Where they went.** / **Where the group goes.** | The graph puts the person next to 22 peers in similar roles. |
| 25-31 | 00:21.1-00:27.3 amber networks, click at 00:22.3. Zoom: "none" at bottom right after 00:24.0 | **3 payment networks** / **no one in the group touches.** | Only this person reached 3 payment and card networks. No one in the group goes there. |
| 31-34 | 00:27.6-00:31.0 red dashed network clicked | **Tried. Blocked.** | They also tried the management networks and were blocked. |
| 34-39 | 00:34.6-00:39.5 raw log box. Zoom: the dark log lines | **Not a claim.** / **Evidence.** | Every finding sits on top of its raw log lines. No guessing, just the record. |
| 39-49 | 00:42.1-00:51.5 question typed, answer arrives. Zoom: two-column table in the left panel | **Ask.** / **Answers come from the record.** / **An attack? The logs alone can't say.** | Ask the assistant; the answer comes from the investigation's own records. Ask if it's an attack, and it says plainly that the logs alone can't tell, then lays out both possibilities side by side. |
| 49-55 | 00:55.0-01:02.5 MITRE, two techniques, shared entity. Zoom: box at 00:59.6 | **One account.** / **Two ATT&CK stages.** | On MITRE ATT&CK, the same account shows up in both initial access and lateral movement. |
| 55-63 | Quick cuts, ~2 s each: 01:05.5 user lookup · 01:15.2 network flows matrix · 01:23.7 alert search · 01:30.6 data sources | **People.** · **Networks.** · **Alerts.** · **Sources.** | A person's week, traffic between zones, every alert and 5 log sources, on one screen. |
| 63-66 | 01:31.8-01:34.8 context cards | **Your logs never leave your organization.** | And your logs never leave your organization. |
| 66-72 | Closing card | **deepin \| security** / Turns security logs into evidence-backed investigations. | deepin security. From alert to evidence. |

İngilizce videoda `en_temiz.mp4` kullanılır; zaman kodları aynıdır.

## 5. Hangi araçla (önce ücretsiz, gerekirse ücretli)

Fiyat ve lisans koşulları sık değişir; **ticari kullanımdan önce aracın güncel koşullarını kontrol edin.**

| İş | Ücretsiz yol | Gerekirse ücretli |
|---|---|---|
| Montaj, yakınlaştırma, kinetik yazı | **CapCut** (masaüstü; anahtar kareyle yakınlaştırma, hazır yazı animasyonları, otomatik altyazı; bazı efektler ücretli) · **DaVinci Resolve** (ücretsiz sürümü profesyonel düzeyde, öğrenmesi daha uzun) · **Canva** (hazır "ürün lansmanı" video şablonları, en kolayı) | CapCut Pro ya da Canva Pro (ek şablon, efekt, stok müzik) |
| Seslendirme | Taslak: macOS `say` (Yelda / Samantha), CapCut'ın metinden sese özelliği | **ElevenLabs** gibi bir ses servisi (doğal Türkçe/İngilizce ses; ticari kullanım genelde ücretli planda) |
| Müzik | YouTube Ses Kitaplığı, Pixabay Music (her parçanın lisansına bakın) | Artlist, Epidemic Sound gibi abonelikli kütüphaneler |
| Metni cilalamak | ChatGPT, Claude, Gemini: bu brifi verip "ekran yazılarını daha vurucu yap" demek yeter (video düzenlemezler) | |
| Kaçınılacak | Metinden/videodan video üreten araçlar (Runway, Sora, Veo, Kling vb.) ürün görüntüsünde kullanılmaz; yalnız soyut açılış için | |

**Önerilen yol:** Canva ya da CapCut'ta bir lansman şablonu seç → temiz 4K görüntüyü içeri al → §3'teki zaman kodlarıyla kes →
yakınlaştırmaları anahtar kareyle ver → ekran yazılarını şablonun yazı animasyonuyla koy → seslendirme (önce ücretsiz taslak,
beğenilirse ücretli ses) → müzik → 1080p ve 4K çıktı. Kısa sosyal medya kesiti (15-20 sn) için §3'ün 7-31. saniyeleri yeter.

## 6. Araca yapıştırılacak hazır istem

**Türkçe:**
> Ekteki `tr_temiz.mp4` bir güvenlik yazılımının gerçek ekran kaydı. Bundan startup lansman videosu tarzında, 60-75 saniyelik,
> 16:9 bir tanıtım videosu hazırla. Ekteki REKLAM_BRIFI.md'nin 3. bölümündeki senaryoyu, klip zaman kodlarını, ekran yazılarını ve
> seslendirmeyi kullan. Kurallar: ürün görüntüsünü yeniden üretme, yalnız kes, yakınlaştır, hızlandır, üstüne yazı koy; ekrandaki
> yazı ve sayıları değiştirme; brifte olmayan sayı ya da iddia ekleme. Yazı tipi Poppins, vurgu rengi #13dca7, koyu zemin #0d2126. Ton sakin ve kendinden emin.

**English:**
> The attached `en_temiz.mp4` is a real screen recording of a security product. Turn it into a 60-75 second, 16:9 product launch
> video in the style of startup launch videos. Use the script, clip timecodes, on-screen text and voice-over from section 4 of the
> attached REKLAM_BRIFI.md. Rules: do not regenerate the product footage, only cut, zoom, speed up and overlay text; do not change
> any text or number on screen; do not add numbers or claims that are not in the brief. Font Poppins, accent #13dca7, dark background #0d2126. Tone: calm and confident.

## 7. Bizim tarafta (araca verilmez)

- Veri tamamen kurgusal (kurum "Meridyen Finans"); müşteri verisi yok. Yine de görüntüyü bir dış servise yüklemek onu o servise vermektir.
- **Kamuya açık yayından önce Deepin ekibinin onayı** gerekir (marka onların).
