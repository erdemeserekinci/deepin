# deepin.space web sitesi

Statik site. Klasörün tamamı deepin.space kök dizinine yüklenir. Varsayılan dil Türkçe; İngilizce sürüm /en/ altında.

| Dosya | Adres |
|---|---|
| `index.html` | https://deepin.space (Türkçe) |
| `risk/`, `finance/`, `security/`, `energy/` | https://deepin.space/risk vb. (Türkçe) |
| `en/index.html` | https://deepin.space/en (İngilizce) |
| `en/risk/`, `en/finance/`, `en/security/`, `en/energy/` | https://deepin.space/en/risk vb. (İngilizce) |
| `assets/` | Ortak görseller |

Her sayfanın sağ üstünde TR / EN geçişi var; aynı sayfanın diğer dildeki karşılığına gider. Sayfalarda `hreflang` bağlantıları tanımlı.

## Düzenleme

HTML dosyaları `src/` içinden üretilir; `index.html` dosyalarını doğrudan düzenlemeyin.

```
python3 build.py
```

- `src/data.tr.json`, `src/data.en.json`: Investigation, Space ve müşteri bilgileri, durum etiketleri, menüler.
- `src/i18n/ui.json`: Bileşenlerde, menüde ve alt bilgide kullanılan ortak metinler (tr ve en).
- `src/pages/tr/*.html`, `src/pages/en/*.html`: Ana sayfa, finance, security ve energy sayfalarının dile özel içerikleri.
- `src/pages/risk.html` + `src/content/risk.tr.json` / `risk.en.json`: deepin.risk sayfası tek şablon; tüm metinler ve demo verisi JSON dosyalarında.
- `src/styles/*.css`: Sayfa stilleri (iki dil için ortak). `src/base.css`, `src/base.js`: Ortak tasarım sistemi ve etkileşimler.
- `src/risk_components.py`: deepin.risk bileşenleri.
- Türkçe sayfalarda İngilizce ürün terimleri (Investigation, deepin.risk vb.) otomatik olarak `lang="en"` ile işaretlenir; büyük harfli etiketlerde "INVESTIGATION" doğru yazılır.

Terminoloji: Türkçe metinlerde Investigation, Space ve ürün adları İngilizce bırakılır.

Müşteri logoları: `src/data.*.json` içinde `proof.show_logos` true yapılıp her müşteriye `logo` yolu girilirse isimler yerine logolar gösterilir.
Talep formu şu an e-posta uygulamasını açar. Bir form servisi bağlanırsa `risk.*.json` içindeki `form.endpoint` alanına adresi yazmak yeterli.

Eski risk.deepin.space adresini https://deepin.space/risk adresine 301 ile yönlendirmek önerilir.
