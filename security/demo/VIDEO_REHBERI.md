# Video rehberi: deepin | security demosundan ürün videosu

Bu klasördeki demo, **kendi kendine gezen bir tur moduyla** videoya çekilebilir: sahte bir imleç ekranda dolaşır, tıklar, yazar;
altta altyazı akar; sonunda logo kartı gelir. Tur bir **senaryo dosyasından** okunur. Yeni bir video = yeni bir senaryo dosyası.
Çekim gerçek ekran kaydıdır (yapay zekâyla üretilmiş görüntü değil), bu yüzden ekrandaki her yazı ve sayı birebir doğrudur.

Bu rehber iki okur için yazıldı: **videoyu isteyen kişi** (§1) ve **isteği yerine getirecek Claude** (§7). Aradaki bölümler
ikisinin de başvuracağı teknik ayrıntı.

**Önce örneklere bakın.** Depoda iki küçük örnek video ve her senaryonun tek resimlik önizlemesi var; neyin nasıl gösterildiğini
görmenin en hızlı yolu bu:

| Dosya | Ne |
|---|---|
| `video/urun_turu/tr_ornek.mp4` (720p, ~100 sn, 3,3 MB) | Tam ürün turu: ana sayfa ve günlük özet → inceleme → graf (üç sahne) → kanıt ve ham kayıt → asistana "Bu bir saldırı mı?" → MITRE → kişi sorgusu → ağ geçişleri → tüm uyarılar → veri kaynakları → kapanış |
| `video/grup_davranisi/tr_ornek.mp4` (720p, ~34 sn, 0,9 MB) | Tek konulu kısa kesit: grup davranışı grafı, kişiden kişiye geçiş, asistana "Kimlere sorulur?" |
| `video/<senaryo>/onizleme_tr.jpg`, `onizleme_en.jpg` | Her sahneden bir kare, sahne adıyla (bütün akış tek resimde) |
| `video/urun_turu/REKLAM_BRIFI.md` | Ürün turundan lansman videosu montajı: senaryo, vurucu ekran yazıları, seslendirme, araçlar |

1080p, 4K ve İngilizce videolar depoda tutulmaz; §3'teki komutlarla birkaç dakikada yeniden üretilir.

---

## 1. Claude'a nasıl istenir

Bu klasörde (sitede `security/demo/`) Claude Code açıp düz Türkçeyle söyleyin. Örnekler:

- *"Graf odaklı 30 saniyelik bir video çek: Kerem Tuncer incelemesi, grafı aç, turuncu ağlara tıkla. Türkçe ve İngilizce."*
- *"MITRE sayfasıyla başlayan 45 saniyelik İngilizce bir video: iki teknik seç, ortak hesabı göster, sonra o hesabın incelemesine git."*
- *"Müşteri İletişim Merkezi grup davranışı için kısa kesit; kişiden kişiye geçsin, sonunda asistana 'Kimlere sorulur?' diye sorsun."*
- *"Ürün turunu altyazısız 4K ver, montaj yapacağım."*
- *"Var olan ürün turunda sohbet sahnesini kısalt, veri kaynakları sahnesini çıkar, yeniden çek."*
- *"LinkedIn için 20 saniyelik, sadece ana sayfa ve graf; kapanışta 'Uyarıyı değil, hikâyeyi görün' yazsın."*

İstekte şunları söylerseniz ilk seferde tutar (söylemezseniz Claude makul bir varsayılan seçer ve söyler):

| Konu | Örnek | Varsayılan |
|---|---|---|
| Dil | Türkçe, İngilizce, ikisi | ikisi (ayrı ayrı iki video) |
| Süre | 20 / 45 / 90 sn | 30-60 sn |
| Hangi sayfalar ve incelemeler | "graf", "MITRE", "Kerem Tuncer" | isteğe göre |
| Vurgulanacak tek mesaj | "grubundan kimsenin gitmediği ağ" | sahne başına bir cümle |
| Altyazı | var / yok (montaj için temiz) | var |
| Kapanış sloganı | "Uyarıdan kanıta." | "Güvenlik kayıtlarını kanıtlı incelemelere dönüştürür." |
| Çözünürlük | 1080p / 4K | 1080p; temiz sürüm 4K |

Claude şunları teslim eder: senaryo dosyası (`kaynak/senaryolar/<ad>.json`), önizleme levhası (her sahneden bir kare), video(lar),
altyazı dosyası (`.srt`) ve sahne sahne altyazı listesi.

---

## 2. Kurulum (bir kez)

| Gerek | Not |
|---|---|
| Google Chrome (ya da Chromium, Edge, Brave) | Kaydedici kendisi bulur; bulamazsa `CHROME=/yol/chrome` ortam değişkeni. Kendi profilinize dokunmaz, geçici bir profille açılır |
| Python 3.9+ | Sayfa üretimi ve denetim yalnız standart kütüphaneyle çalışır |
| `pip install -r kaynak/video_gereksinim.txt` | opencv-python, numpy, websocket-client (yalnız video için) |
| İnternet | Yalnız Poppins yazı tipi için (Google Fonts). Yoksa çekim sistem yazı tipiyle yapılır ve uyarı basılır |
| ffmpeg | **Gerekmez.** OpenCV H.264 yazamazsa kaydedici varsa ffmpeg'i (ya da macOS `avconvert`) kullanır, yoksa komutu söyler |

Komutların hepsi bu klasörden çalışır. (macOS'ta klasör yolunda noktayla biten bir bileşen varsa, örneğin kullanıcı adı `ad.`,
Python çalışma dizinini okuyamayabilir: o durumda başka bir klasörden tam yolla çağırın, `cd /tmp && python3 <tam yol>/uret.py`.)

---

## 3. Bir video, beş adım

```bash
python3 kaynak/senaryo_yardim.py                                   # 1. kullanılabilecek her şey: incelemeler, graf düğümleri, seçiciler, sayılar
#                                                                    2. kaynak/senaryolar/<ad>.json dosyasını yaz (§4)
python3 uret.py && python3 denetim.py                                # 3. senaryolar sayfaya gömülür; denetim altyazı sayılarını veriyle sınar
python3 kaynak/video_cek.py --senaryo <ad> --dil tr --onizleme       # 4. her sahneden bir kare: video/<ad>/onizleme_tr.jpg (~1 dk)
python3 kaynak/video_cek.py --senaryo <ad> --dil tr                  # 5. tam çekim; sonra --dil en, gerekirse --temiz
```

| Çıktı (`video/<ad>/`) | Ne |
|---|---|
| `tr.mp4`, `en.mp4` | Altyazılı video: 1920×1080, 30 kare/sn, H.264. Uygulama koyu zeminde pencere, altyazı pencerenin altında |
| `tr_temiz.mp4`, `en_temiz.mp4` | `--temiz`: altyazısız, çerçevesiz, kapanış kartısız, uygulama tam ekran, 3840×2160 (montaj için) |
| `tr.srt`, `en.srt` (`_temiz.srt`) | Altyazılar, sahne zamanlarıyla (montajda ya da sosyal medyada ayrı altyazı olarak) |
| `tr_temas.jpg` | İki saniyede bir kare, tek resimde (kontrol için) |
| `onizleme_tr.jpg` | `--onizleme`: her sahnenin sonuna yakın bir kare, sahne adıyla |
| `anlik/tr_<ms>.png` | `--anlik 3000,15000`: yalnız o anların tam boy karesi |
| `tr_ornek.mp4` | `--ornek`: 1280×720, depoya konacak küçük örnek (depoda yalnız bunlar ve önizleme levhaları tutulur) |

**Süreler (bu makinede ölçüldü):** önizleme ~1 dk · 1080p tam çekim, videonun her saniyesi için ~3 sn · 4K ~6-7 sn.
Zaman sanal ilerlediği için makine yavaş da olsa video akıcı ve her çekim aynıdır.

---

## 4. Senaryo dosyası

`kaynak/senaryolar/<ad>.json`. Dosya adı senaryonun adıdır (`--senaryo <ad>`, tarayıcıda `index.html?tur=1&senaryo=<ad>`).
Var olan iki örnek: `urun_turu.json` (~100 sn, bütün sayfalar) ve `grup_davranisi.json` (~34 sn, tek konu). Yenisini yazarken
onlardan birini kopyalayıp değiştirmek en hızlı yoldur.

```json
{
  "surum": 1,
  "baslik": "Kısa kesit: ...",
  "imlec_bas": [0.66, 0.78],
  "kapanis": {
    "slogan": {"tr": "Uyarıyı değil, hikâyeyi görün.", "en": "See the story, not the alert."},
    "not": {"tr": "Kurgusal kurumla hazırlanmış demo verisi.", "en": "Demo data prepared with a fictional organization."}
  },
  "sahneler": [
    {
      "ad": "graf",
      "arayuz_adi": ["Graf"],
      "altyazi": {"tr": "Graf: kişi, benzer görevdeki 22 çalışan ve gittiği ağlar.", "en": "The graph: the person, 22 peers in similar roles and the networks reached."},
      "sayilar": ["grup_uye"],
      "adimlar": [
        ["tik", ".row-h[data-a=\"ac-inc\"][data-p=\"ayrilan-hesap\"]", 1000, {"fx": 0.22}],
        ["bekle", 800],
        ["tik", ".dact [data-a=\"tab\"][data-p=\"graf\"]", 950],
        ["kaydir", "#card", 1100, {"hedef": ".gsvg", "ust": 2}],
        ["imlec", ".gsvg circle[r=\"44\"]", 800],
        ["bekle", 2000]
      ]
    },
    {"ad": "kapanis", "altyazi": {"tr": "", "en": ""}, "sayilar": [], "adimlar": [["kapanis", null, 4500]]}
  ]
}
```

**Üst alanlar:** `baslik` (yardımcının listesinde görünür) · `imlec_bas` (imlecin başlangıç yeri, ekranın oranı) · `kapanis`
(kapanış kartının sloganı ve alt satırı; alt satır demo notudur, kalır).

**Sahne alanları:** `ad` (tekil, sahne tanımı) · `altyazi` (TR ve EN; sahne boyunca görünür, sahne başında belirir, sonunda
kaybolur) · `sayilar` (altyazıdaki her rakamın veri anahtarı, §5) · `arayuz_adi` (altyazı bir sayfa ya da sekme adı geçiriyorsa
o adın arayüzdeki yazılışı; denetim İngilizce karşılığını da arar) · `adimlar`.

**Adım biçimi:** `[tip, hedef, süre_ms, ek]`. Süre verilmezse varsayılan kullanılır.

| Tip | Biçim | Varsayılan | Ne yapar |
|---|---|---|---|
| `tik` | `["tik", seçici, ms, ek]` | 850 + 380 | İmleci öğeye götürür (ms), sonra tıklar. **En çok kullanılan adım** |
| `imlec` | `["imlec", seçici, ms, ek]` | 850 | İmleci öğeye yumuşak bir yayla götürür (tıklamaz; üzerine gelme görünümü oluşur) |
| `tikla` | `["tikla", seçici veya null, ms]` | 380 | İmleç olduğu yerde tıklar (null ise imlecin altındaki öğeye) |
| `bekle` | `["bekle", ms]` | | Hiçbir şey yapmaz; okuma süresi |
| `kaydir` | `["kaydir", "#card", ms, {"hedef": seçici, "ust": 24}]` | 1000 | Kabı yumuşakça kaydırır; `hedef` seçici (öğenin üstü kabın üstünden `ust` px aşağı gelir), `"son"` ya da piksel |
| `yaz` | `["yaz", seçici, ms, {"metin": {"tr": "...", "en": "..."}}]` | 1100 | Yazı kutusuna harf harf yazar (arama kutusu her harfte süzülür) |
| `gonder` | `["gonder", form seçici]` | 0 | Formu gönderir (genelde yerine gönder düğmesine `tik`) |
| `sec` | `["sec", select seçici, 0, {"deger": "yuksek"}]` | 0 | Açılır listede değer seçer |
| `panel` | `["panel", null, ms, {"genislik": 470}]` | 900 | Sohbet panelinin genişliğini değiştirir; imleç tutamaçla birlikte gider (önce `["imlec", "#handle"]`) |
| `git` | `["git", "#/mitre"]` | 0 | Rotaya anında gider, imleçsiz. Videoda `tik` daha doğal durur; `git` yalnız zorunluysa |
| `kontrol` | `["kontrol", seçici veya null, 0, {"cevap": "saldiri", "metin": "..."}]` | 0 | **Doğrulama.** Seçici ekranda yoksa, asistan beklenen soruyu cevaplamadıysa ya da metin ekranda yoksa çekim hata verir |
| `kapanis` | `["kapanis", null, ms]` | 4500 | Kapanış kartı. `--temiz` çekimde 1 sn beklemeye dönüşür |

**`ek` alanları:** `fx`, `fy` imlecin öğe içindeki yeri, 0-1 oran (varsayılan 0,5 / 0,5; uzun satırlarda `fx: 0.25` gibi sol tarafa
götürmek daha doğal) · `dx`, `dy` piksel kaydırma.

**Zamanlama:** altyazıyı okumak için karakter başına ~65 ms + 1,5 sn bırakın. Tek satır (~60 karakter) ~5 sn, iki satır (~110
karakter) ~7 sn. Bir sahnenin süresi adımlarının toplamıdır; altyazı süresi yetmiyorsa sahnenin sonuna `bekle` ekleyin.
Sayfa geçişlerinde tıklamadan sonra 700-900 ms bekleyin (yeni sayfa çizilsin). Asistan cevabı gönderimden ~1 sn sonra gelir,
sonrasında 1,5 sn bekleyin.

**Ekran:** sanal ekran 1600×900 CSS px, ölçek 1,2 (1080p); uygulama penceresi 1480×760. `--temiz` modunda uygulama tam ekran ve
ölçek 2,4 (4K). Seçiciler iki modda da aynıdır.

**Bilmek gerekenler:**
- Uygulama her tıklamada ekranı baştan çizer. Seçiciler **tıklama anında** aranır; bu yüzden sayfa değişikliğinden hemen sonraki
  adıma kısa bir `bekle` koyun.
- Grafın tamamı ancak kaydırınca görünür: graf sekmesinden sonra `["kaydir", "#card", 1100, {"hedef": ".gsvg", "ust": 2}]`.
- Graf sınıf başına sınırlı sayıda düğüm çizer, fazlası "+N ağ daha" kutusunda toplanır. Hangi düğümün tıklanabilir olduğunu
  `senaryo_yardim.py graf` gösterir (`.gnode[data-c="<CIDR>"]` ya da toplu kutu için `.gnode[data-p="dN"]`).
- Asistan soruları: çip tıklamak en güvenlisidir (`.chip[data-a="chip"][data-p="soru:<id>"]`, inceleme açılınca gelir). Yazarak
  sorulursa cevabı anahtar sözcük eşleşmesi seçer; her yazılı sorudan sonra `kontrol` adımıyla doğru cevaba düştüğünü doğrulayın
  (bir kez İngilizce "attack" kelimesi MITRE cevabına düştü; kontrol bunu yakalar). Sözcük listesi: `senaryo_yardim.py sohbet`.
- Kişi sorgusu adsız açılırsa son seçilen kişiyi gösterir (ilk açılışta `ktuncer`). Başka kişi için önce `#/kisi/<ad>` rotası ya da
  sayfadaki kişi çipi.
- Aynı turdaki önceki adımlar durumu değiştirir (açık satır, seçili MITRE teknikleri, panel genişliği). Senaryo baştan sona tek
  oturumdur; yeni bir çekim her zaman temiz sayfadan başlar.

---

## 5. Altyazıdaki sayılar veriden gelir

Altyazıda geçen **her rakam**, sahnenin `sayilar` listesindeki bir anahtarın değerine eşit olmalı. `denetim.py` bunu hem Türkçe hem
İngilizce altyazı için sınar; tutmazsa neyin neye eşit olması gerektiğini yazar ve çıkış kodu 1 döner. Anahtarlar
`kaynak/senaryo_sayilari.py` içinde; güncel listeyi ve değerleri `python3 kaynak/senaryo_yardim.py sayi` basar.

| Anahtar türü | Örnek | Değer |
|---|---|---|
| Adlı | `uyari_sayisi`, `inceleme_sayisi`, `yuksek_sayisi`, `grup_uye`, `ag_bolge`, `kayit_kaynagi` | 45, 16, 4, 22, 11, 5 |
| İnceleme başına | `inc.<id>.uyari` · `.kaynak` · `.varlik` · `.eksik` · `.ham` · `.grup_uye` · `.graf.yalniz` | `inc.iletisim-merkezi.grup_uye` = 34 |
| Kişi başına (haftalık toplam) | `kisi.<ad>.istek` · `.engel` · `.oturum` · `.yonetici` | `kisi.ktuncer.oturum` = 9 |
| Teknik | `mitre.<kod>.uyari` | `mitre.T1046.uyari` = 19 |
| Gün | `gun.<YYYY-AA-GG>` | `gun.2026-04-30` = 30 ("30 Nisan") |

Aynı sayı altyazıda iki kez geçiyorsa anahtar da iki kez yazılır. Rakam yerine yazıyla yazılan sayılar ("üç") denetlenmez; rakam
tercih edin. Listede olmayan bir sayı gerekiyorsa `senaryo_sayilari.py` içindeki `adli()` sözlüğüne **veriden hesaplayan** bir satır
eklenir; sayı elle yazılmaz.

---

## 6. Değişmez kurallar

1. **Video yalnız ürünün yaptığını söyler.** "Yapay zekâ saldırıyı tespit etti" denmez. Ürün kanıta dayalı inceleme yapar; asistan
   incelemenin kendi kayıtlarından cevap verir, kayıt söylemiyorsa "söylemez" der. Abartı, karşılaştırma ve performans iddiası yok.
2. **Sayılar veriden** (§5). Kullanıcı bir sayı söylese bile veriden doğrulanır.
3. **İki dil ayrı çekilir:** Türkçe video Türkçe arayüzle, İngilizce video İngilizce arayüzle. Her altyazı ve yazılacak her metin
   iki dilde yazılır; altyazıdaki sayfa adı arayüzdeki adla aynıdır (`arayuz_adi`).
4. **Kapanış kartında demo notu kalır:** "Kurgusal kurumla hazırlanmış demo verisi." / "Demo data prepared with a fictional organization."
5. **Altyazı dili:** uzun tire (—) yok, soru işareti yok, iç kod ya da dosya adı yok; sade, kısa, kendinden emin cümle.
6. **Veri kurgusaldır ve öyle kalır.** Kurum, kişiler, adres planı, kayıt satırları `kaynak/veri.py`'de üretilir. Gerçek bir
   kurumdan ad, adres, sayı ya da kayıt bu dosyaya taşınmaz.
7. **Ürün görüntüsü yeniden üretilmez.** Video başka bir araçta montajlanacaksa yalnız kesilir, yakınlaştırılır, üstüne yazı konur;
   metinden/videodan video üreten yapay zekâ araçları ekrandaki yazıyı bozar. Ayrıntı ve hazır istem: `video/urun_turu/REKLAM_BRIFI.md`.
8. **Yayın:** bu klasör sitenin içinde durur. Site deepin.space'e yüklenince demo `/security/demo/` adresinde **herkese açık** olur
   (sayfa arama motorlarına kapalı: `noindex`). Depoya yalnız küçük örnekler (`*_ornek.mp4`, 720p) ve önizleme levhaları girer;
   1080p/4K videolar `.gitignore` ile dışarıda kalır, yeniden üretilir. Yeni bir senaryo eklenince örneği istenirse `--ornek` ile çekilir.

---

## 7. Claude için: bu klasörde video istendiğinde

1. Bu dosyayı ve `BENI_OKU.md`'yi oku. `python3 kaynak/senaryo_yardim.py` ile güncel hedefleri, seçicileri ve sayıları al.
   Belgedeki örnek seçiciler eskiyebilir; **yardımcının çıktısı veriden gelir, ona güven.**
2. İstekten eksik kalanları §1'deki varsayılanlarla doldur ve kullanıcıya bir satırda söyle (sormak için durma). İstenen şey mümkün
   değilse (§8) söyle ve en yakın alternatifi öner.
3. Senaryoyu yaz: var olan bir senaryoyu kopyala; sahne başına tek mesaj, tek altyazı. Altyazıdaki her rakam için `sayilar`,
   sayfa adı için `arayuz_adi`, her yazılı sorudan sonra `kontrol` ekle. Süreleri §4'teki okuma kuralıyla ayarla.
4. `python3 uret.py && python3 denetim.py`. Denetim hata verirse düzelt; denetimi susturmak için kural gevşetme.
5. Her dil için `--onizleme` çek ve levhayı **kendin incele**: her karede doğru sayfa mı, imleç doğru yerde mi, altyazı okunuyor mu,
   önemli içerik pencerenin dışında mı kaldı. Gerekirse bir sahneyi `--anlik <ms>` ile tam boy aç. Kaydedici "TUR HATALARI" basarsa
   (bulunamayan seçici, tutmayan kontrol) önce onu çöz.
6. Tam çekimi yap (`--dil tr`, `--dil en`; istenirse `--temiz`). Uzun çekimleri arka planda çalıştır; iki dil paralel çekilebilir.
7. Teslim: video yolları, süre, sahne sahne altyazı listesi (TR/EN), önizleme levhası. Hangi varsayılanı seçtiğini ve neyi
   yapamadığını açıkça yaz.
8. Ürünün kendisinde bir kusur bulursan (yanlış cevap, taşan tablo, çevrilmemiş metin) `kaynak/` içinde düzelt, `denetim.py`'yi
   tekrar koştur ve teslimde ayrıca söyle. `index.html` dosyalarını elle düzenleme; `uret.py` üretir.

---

## 8. Şu an yapamadıkları

| İstek | Durum | Alternatif |
|---|---|---|
| Dikey (9:16) ya da kare (1:1) video | Yok: uygulama dar ekranda mobil düzene geçer | Temiz 4K çekimden montajda kırpma |
| Seslendirme, müzik | Yok | `REKLAM_BRIFI.md`: araçlar (önce ücretsiz), seslendirme metni |
| Kamera yakınlaştırması (ekranın bir bölgesine zoom) | Yok | Temiz 4K çekimde montajda yakınlaştırma; 4K olduğu için net kalır |
| Demoda olmayan bir vaka ya da sayı | Senaryo yetmez, veri değişir | `kaynak/veri.py`'ye inceleme eklemek gerekir; `denetim.py` tutarlılığı sınar (büyük iş) |
| Gerçek müşteri verisiyle video | Yapılmaz | Kural 6 |

---

## 9. Dosyalar

| Dosya | Ne |
|---|---|
| `kaynak/senaryolar/*.json` | Senaryolar (her dosya bir video) |
| `kaynak/senaryo_yardim.py` | Hedefler, seçiciler, asistan soruları, sayı anahtarları (veriden) |
| `kaynak/senaryo_sayilari.py` | Altyazı sayılarının veri karşılıkları |
| `kaynak/tur.js`, `kaynak/tur.css` | Tur motoru, imleç, altyazı, kapanış kartı, pencere görünümü. Yalnız `?tur=1` ile çalışır; normal kullanımda hiçbir şey değişmez |
| `kaynak/video_cek.py` | Kaydedici (başlıksız Chrome, sanal zaman, mp4/srt/levha) |
| `kaynak/video_gereksinim.txt` | Video için Python paketleri |
| `uret.py`, `denetim.py` | Sayfayı üretir (senaryoları gömer); tutarlılığı ve altyazıları sınar |
| `video/urun_turu/REKLAM_BRIFI.md` | Ürün turundan lansman videosu montajı için brif: senaryo, ekran yazıları, seslendirme, araçlar |

Tarayıcıda önizleme (gerçek zamanda, kaydetmeden): `index.html?tur=1&senaryo=<ad>` (`&temiz=1` ile çerçevesiz). Pencere boyutu
1600×900'e yakınsa videoya en yakın görünür.
