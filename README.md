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
- `src/base.css`, `src/base.js`: Ortak tasarım sistemi ve etkileşimler.

Eski risk.deepin.space adresini https://deepin.space/risk adresine 301 ile yönlendirmek önerilir.
