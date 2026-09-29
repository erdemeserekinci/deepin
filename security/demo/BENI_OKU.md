# deepin.security platform demosu

deepin.security inceleme ekranının Deepin platformunun görünümüyle, **tamamen kurgusal veriyle**, gerçek bir uygulama gibi
çalışan hâli. Klasör kendi başına durur: sitenin geri kalanına (`build.py`, `src/`) bağlı değildir, `build.py` bu klasöre yazmaz.
Video üretimi için ayrı rehber: **[VIDEO_REHBERI.md](VIDEO_REHBERI.md)**.

## Açmak

`index.html` tek dosyadır, çift tıkla açılır (sunucu gerekmez). Yazı tipi (Poppins) Deepin sitesi gibi Google Fonts'tan
gelir; internet yoksa sistem yazı tipine düşer, düzen bozulmaz. Yerel sunucuyla bakmak için bu klasörde
`python3 -m http.server 8000` → `http://localhost:8000/index.html` (İngilizcesi `/en/index.html`).

## Yeniden üretmek

```
python3 uret.py
```

Komutlar bu klasörden çalışır ve yalnız standart kütüphaneyi kullanır (video için ek paketler VIDEO_REHBERI.md'de).

| Dosya | Ne |
|---|---|
| `kaynak/veri.py` | Sentetik veri üreticisi: kurgusal kurum ("Meridyen Finans"), kişiler, adres planı, 16 inceleme, 45 uyarı, ham kayıt satırları. Aynı tohum, aynı çıktı |
| `kaynak/platform.css` | Deepin platform kabuğu: ray, sohbet paneli, ana kart, risk sekmeleri, satırlar |
| `kaynak/platform.js` | Uygulama: yönlendirme (`#/…`), sohbet, çekmeceler, graf, tablolar |
| `uret.py` | Hepsini `index.html` içine gömer |
| `denetim.py` | Sekmeler arası sayı tutarlılığı ve ekran metni taraması (tutmayan varsa çıkış kodu 1) |
| `kaynak/ikon_uret.py`, `kaynak/ikonlar.json` | Font Awesome glifleri → SVG yolu |
| `assets/` | Deepin logoları (sitenin `assets/` klasöründen kopya) ve boyanmış platform logosu |
| `kaynak/tur.js`, `tur.css`, `senaryolar/`, `video_cek.py`, `senaryo_yardim.py`, `senaryo_sayilari.py` | Video (tur modu); ayrıntı VIDEO_REHBERI.md |

## Tasarım kaynağı

Birincil: platform.deepin.space'in bir ekran görüntüsü (bu depoda değil). **Ölçüler örnekten programla alındı**, gözle değil:
yazı boyutları örnekteki metinlerin genişliği Poppins ile eşlenerek, renk ve çizgi tonları doğrudan pikselden,
yerleşim kenar kenar. Örnek MacBook ekranından, pencere yaklaşık 1468×826 CSS px; karşılaştırma bu boyutta yapılır.

| Öğe | Değer |
|---|---|
| Başlık çubuğu | 63px, alt çizgi 2px `#eef2fc`; logo 29px yüksek, nane `#00e695` çubuk, "security" 32px/300 |
| Sol ray | 72px, zemin `#f8f9fb`, sağ üst köşe 14px; düğme 44px, köşe 12px, çerçeve `#eaeff9`; ikon 15px; ipucu `#143037` 15px/600 |
| Sohbet paneli | 300px; "Geri" 16px; filigran logo %17; giriş kutusu 65px, köşe 14px, çerçeve `#54e0b0`, yer tutucu 16px `#99a0ac`; alt not 13px |
| Ana kart | sol ve üst çerçeve `#eaf0fc`, sol üst köşe 14px, iç boşluk 16px; başlık 24px/700, alt başlık 15px `#727c8a` |
| Öncelik sekmeleri | 75px, köşe 12px, çerçeve `#eaeaeb`, zemin `#f8f9fb`; sayı 27px/700, etiket 15px/600, alt satır 13px; etkin sekme beyaz + 3px çubuk |
| Satırlar | aralık 84,5px, sol çubuk 3px; başlık 15px/600 büyük harf; çip 22px, 10,5px/500; hap 28px, 13px; ok 1,8px çizgi |
| Renkler | yazı `#143037`, ikincil `#727c8a`, yüksek `#f18f80`, orta `#ca8505`, düşük `#9dca85`, nane `#13dca7` |

İkonlar Font Awesome Free 6.7.2 (örnek ekranla aynı aile): yerelde kurulu qtawesome paketindeki yazı tipinden
`kaynak/ikon_uret.py` ile SVG yoluna çevrildi, `kaynak/ikonlar.json` içinde, sayfaya gömülü (indirme yok; lisans CC BY 4.0,
atıf `index.html` içinde). Logo `assets/deepin-logo-platform.png`: sitenin nane logosunun örnekteki parlak tona boyanmış kopyası.
İkincil kaynak sitenin `src/base.css` dosyası (Poppins, JetBrains Mono, yeşil vurgu). İki kaynak çakışırsa örnek ekran kazanır.

**Örnekle karşılaştırma** (her tasarım değişikliğinden sonra): Chrome başsız modda, ayrı geçici profille, 1468×826 ve 2x çekilir,
örnekle aynı ölçeğe getirilip bölge bölge yan yana konur ve kenarlar ölçülür. Son ölçümde başlık, alt başlık, sekme kutusu, satır
çizgileri, giriş kutusu, tutamaç ve logo örnekle 0-2px içinde.

## İngilizce sürüm

`en/index.html`. Sağ üstteki TR / EN düğmesi aynı ekranı (aynı `#/…` adresini) öbür dilde açar; `uret.py` iki dosyayı birlikte üretir.

| Dosya | Ne |
|---|---|
| `kaynak/cevir.py` | Veri katmanını çevirir: her metni **şablona** indirir (`{N}` sayı, `{P}` yüzde, `{D}` tarih, `{T}` saat, `{K}` adres/makine/kişi adı), sözlükten Türkçe şablonun İngilizcesini koyar. Sayılar, tarihler ve adresler dokunulmadan taşınır; biçim çevrilir (`1.386` → `1,386`, `%74` → `74%`, `17 Eyl` → `Sep 17`) |
| `kaynak/ceviri_veri_en.py` | Veri metinleri sözlüğü (~590 girdi). Tekil/çoğul için `{"1": …, "*": …}`, sayı sırası değişirse `{N2}` gibi indeks |
| `kaynak/ceviri_js_en.py` | Arayüz metinleri sözlüğü (~245 girdi); anahtarlar `platform.js` içindeki `tt('…')` çağrılarıdır |

Kurallar: sözlükte **olmayan** Türkçe veri metni ya da `tt()` anahtarı üretimi **durdurur** (sessiz geçiş yok). Kişi adları ve adresler çevrilmez.
Terimler: inceleme = investigation, uyarı = alert, varlık = entity; MITRE teknik ve aşama adları ATT&CK'in kendi İngilizce adları;
Deepin platform ekranının kendi cümleleri korundu ("Monitor closely", "Sorted from high to low", "AI can make mistakes. Please verify the answers.").
Yeni bir metin eklenince: Türkçesini `tt('…')` ya da `veri.py` içine yaz, İngilizcesini ilgili sözlüğe ekle, `uret.py` eksiği adıyla söyler.

## Ne var

Güncel Uyarılar (dönem filtresi, satır açma) · inceleme dosyası (Genel bakış, Uyarılar, Kanıt + ham kayıt satırları, Zaman,
Graf, Eksik bilgi) · Tüm uyarılar · MITRE (iki teknik seçince ortak varlıklar) · Ağ geçişleri (Akış, Matris) · Kişi sorgusu ·
Veri kaynakları · asistan (önceden tanımlı sorular ve serbest metin eşleme; cevaplar incelemenin kendi alanlarından).

## Kurallar (ürün ekran dili, burada da geçerli)

Ekranda iç kod, dosya adı (ham kayıt yolu hariç), "bize not" cümlesi, müşteriye soru ve hüküm etiketi yok; uzun tire yok;
sayının yanına ek yalnız Türkçe doğruysa gelir. Adlar açık (kurgusal). Ekranda "Kurgusal kurumla hazırlanmış demo verisi" notu var.

## Denetimler (her değişiklikte)

```
python3 denetim.py
```

- İngilizce sürüm: her Türkçe/İngilizce metin çifti aynı sayıları taşımalı, kişi adı dışında Türkçe harf kalmamalı (`denetim.py` ikisini de sınar).
- Sekmeler arası sayı tutarlılığı: uyarı sayısı, kişi tablosu ↔ graf ↔ kişi sorgusu ↔ ham kayıt toplamı, yoğun gün,
  ortanca, servis kod dağılımı (yerelde 0 tutarsızlık).
- İki koşu bayt bayt aynı.
- Metin taraması: uzun tire, iç kod, soru işareti, maskeli ad, `undefined/NaN` (0 bulgu).

## Video (tur modu)

Sayfa `?tur=1` ile açılınca kendi kendine gezen bir tura girer (sahte imleç, altyazı şeridi, kapanış kartı); parametre yoksa hiçbir
şey değişmez. Senaryolar `kaynak/senaryolar/*.json`, kaydedici `kaynak/video_cek.py`, çıktılar `video/<senaryo>/`.
Senaryo yazmak, önizlemek, çekmek ve kurallar: **[VIDEO_REHBERI.md](VIDEO_REHBERI.md)**.

## Bilinen sınırlar

- Koyu tema yok.
- Asistan model değil: önceden tanımlı sorular ve anahtar sözcük eşleme.
- Veri kurgusaldır; gerçek müşteri verisi, adı, sayısı ya da adres planı içermez.
