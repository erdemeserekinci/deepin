# deepin.security platform demosu (bu klasör)

Kurgusal veriyle çalışan inceleme ekranı demosu ve ondan ürün videosu çeken tur modu. Klasör kendi başına durur;
sitenin `build.py`'si buraya yazmaz, buradaki komutlar sitenin geri kalanına dokunmaz.

- **Video istenirse:** önce [VIDEO_REHBERI.md](VIDEO_REHBERI.md) §7'yi uygula. Güncel hedefler, seçiciler ve sayılar için
  `python3 kaynak/senaryo_yardim.py` (belgeden daha günceldir). Önizlemeyi (`--onizleme`) kendin incelemeden tam çekime geçme.
- **Demo değişirse:** `index.html` dosyalarını elle düzenleme. Kaynak `kaynak/`; `python3 uret.py` üretir,
  `python3 denetim.py` sekmeler arası sayıları, İngilizce çeviriyi ve video altyazılarını sınar (tutmazsa çıkış kodu 1).
  Yeni bir ekran metni iki dilde yazılır: Türkçesi `tt('…')` ya da `veri.py`, İngilizcesi `kaynak/ceviri_*_en.py`.
- **Değişmezler:** veri kurgusaldır, gerçek bir kurumdan ad, adres, sayı ya da kayıt eklenmez · altyazıdaki her rakam
  veriden gelir · "yapay zekâ tespit etti" denmez · ekranda ve altyazıda uzun tire, iç kod, dosya adı yok · kapanışta
  "Kurgusal kurumla hazırlanmış demo verisi." notu kalır.
- Ayrıntı: [BENI_OKU.md](BENI_OKU.md).
