# deepin.space web sitesi

Statik site. Klasörün tamamı deepin.space kök dizinine yüklenir.

| Dosya | Adres |
|---|---|
| `index.html` | https://deepin.space |
| `risk/index.html` | https://deepin.space/risk |
| `finance/index.html` | https://deepin.space/finance |
| `security/index.html` | https://deepin.space/security |
| `energy/index.html` | https://deepin.space/energy |
| `assets/` | Ortak görseller |

## Düzenleme

HTML dosyaları `src/` içinden üretilir; doğrudan `index.html` dosyalarını düzenlemeyin.

```
python3 build.py
```

- `src/data.json`: Investigation, Space ve müşteri bilgileri (durum/olgunluk dahil). Kartlar, müşteri kanıt ızgarası ve Space bölümleri buradan üretilir.
- `src/pages/*.html`: Sayfa içerikleri. `<!--@bilesen-->` işaretleri `build.py` içindeki bileşenlerle doldurulur (investigation_catalog, proof_grid, spaces_scene, evidence_rail, enterprise_chips, data_note, copy_email).
- `src/content/risk.en.json`: deepin.risk sayfasının tüm metinleri ve demo verileri. Türkçe sürüm için `risk.tr.json` oluşturup `build.py` içindeki PAGES listesine bir satır eklemek yeterli.
- `src/risk_components.py`: deepin.risk bileşenleri: canlı şirket incelemesi, statik rapor ve canlı inceleme zaman çizelgesi, What changed? boyutları (sahiplik, yetki, ilişki grafiği, finansal bağlam), izleme ve inceleme farkı, kanıt kartı (onay, ret, derinleştirme), risk yığını, tek inceleme ile çoklu karar, talep formu (mobilde alt sayfa olarak açılır).
- `src/base.css`, `src/base.js`: Ortak tasarım sistemi ve etkileşimler.
- Müşteri logoları: `src/data.json` içinde `proof.show_logos` true yapılıp her müşteriye `logo` yolu girilirse isimler yerine logolar gösterilir.
- Talep formu şu an e-posta uygulamasını açar. Bir form servisi bağlanırsa `risk.en.json` içindeki `form.endpoint` alanına adresi yazmak yeterli.

Eski risk.deepin.space adresini https://deepin.space/risk adresine 301 ile yönlendirmek önerilir.
