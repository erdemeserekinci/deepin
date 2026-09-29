#!/usr/bin/env python3
"""deepin.security platform demosunu iki dilde uretir.

    python3 uret.py            (bu klasorden; macOS'ta klasor yolu noktali bir bilesen iceriyorsa: cd /tmp && python3 <tam yol>/uret.py)

    index.html       Turkce (kok)
    en/index.html    Ingilizce

Veri tek mantikla uretilir (kaynak/veri.py, Turkce); Ingilizce veri, cevir.py ile sozlukten cevrilir. Arayuz metinleri
platform.js icindeki tt('...') anahtarlaridir; Ingilizcesi kaynak/ceviri_js_en.py. Sozlukte olmayan anahtar ya da
cevrilmemis Turkce veri metni yapiyi DURDURUR. Tur modu (video cekimi, yalniz ?tur=1 ile calisir): kaynak/tur.js + tur.css;
kaynak/senaryolar/*.json dosyalarinin hepsi dile gore secilip window.__TURLAR olarak gomulur (?senaryo=<ad>).
"""
import json, os, re, sys

sys.dont_write_bytecode = True
KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(KOK, "kaynak"))
import veri  # noqa: E402
import cevir  # noqa: E402
from ceviri_js_en import TXT as TXT_EN  # noqa: E402

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">')

DILLER = {
    "tr": {"cikti": "index.html", "asset": "assets/", "baslik": "deepin | security",
           "aciklama": "deepin security: güvenlik kayıtlarını kanıtlı incelemelere dönüştürür. Kurgusal kurumla hazırlanmış demo verisi.",
           "noscript": "Bu demo JavaScript gerektirir."},
    "en": {"cikti": "en/index.html", "asset": "../assets/", "baslik": "deepin | security",
           "aciklama": "deepin security turns security logs into evidence-backed investigations. Demo data prepared with a fictional organization.",
           "noscript": "This demo requires JavaScript."},
}


def oku(ad):
    return open(os.path.join(KOK, "kaynak", ad), encoding="utf-8").read()


def js_anahtarlari(js):
    return {m.group(1).replace("\\'", "'") for m in re.finditer(r"\btt\('((?:[^'\\]|\\.)*)'", js)}


def json_gom(x):
    return json.dumps(x, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def veri_hazirla(dil):
    d = json.loads(json.dumps(veri.uret()))
    if dil == "tr":
        return d
    cevir.isimleri_ayarla({k["ad_soyad"] for k in d["kisiler"].values()})
    eksik = set()
    en = cevir.cevir(d, eksik)
    if eksik:
        print("CEVRILMEMIS VERI METNI:", len(eksik))
        for x in sorted(eksik):
            print("  ", repr(x))
        sys.exit(1)
    return en


def senaryo_hazirla(yol, dil):
    s = json.load(open(yol, encoding="utf-8"))
    sec = lambda x: x[dil] if isinstance(x, dict) and dil in x else x
    out = {"imlec_bas": s.get("imlec_bas"), "kapanis": {k: sec(v) for k, v in s.get("kapanis", {}).items()}, "sahneler": []}
    for sh in s["sahneler"]:
        adimlar = []
        for a in sh["adimlar"]:
            a = list(a)
            if len(a) > 3 and isinstance(a[3], dict) and "metin" in a[3]:
                a[3] = dict(a[3], metin=sec(a[3]["metin"]))
            adimlar.append(a)
        out["sahneler"].append({"ad": sh["ad"], "altyazi": sec(sh.get("altyazi", "")), "adimlar": adimlar})
    return out


def senaryolar(dil):
    k = os.path.join(KOK, "kaynak", "senaryolar")
    return {os.path.splitext(f)[0]: senaryo_hazirla(os.path.join(k, f), dil) for f in sorted(os.listdir(k)) if f.endswith(".json")}


def insa(dil, js, css, ikon, tur_js):
    ayar = DILLER[dil]
    d = veri_hazirla(dil)
    txt = {} if dil == "tr" else TXT_EN
    tur = senaryolar(dil)
    doc = f'''<!doctype html>
<html lang="{dil}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>{ayar["baslik"]}</title>
<meta name="description" content="{ayar["aciklama"]}">
<meta name="theme-color" content="#ffffff">
<link rel="icon" type="image/png" href="{ayar["asset"]}favicon-64.png">
{FONTS}
<style>
{css}
</style>
</head>
<body>
<div id="kok"></div>
<noscript><p style="padding:40px;font-family:sans-serif">{ayar["noscript"]}</p></noscript>
<!-- Icons: Font Awesome Free 6.7.2 by @fontawesome, https://fontawesome.com, icon license CC BY 4.0 -->
<script>window.__DIL={json_gom(dil)};window.__ASSET={json_gom(ayar["asset"])};window.__TXT={json_gom(txt)};window.__VERI={json_gom(d)};window.__IKON={ikon};window.__TURLAR={json_gom(tur)};</script>
<script>
{tur_js}
</script>
<script>
{js}
</script>
</body>
</html>
'''
    yol = os.path.join(KOK, ayar["cikti"])
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    open(yol, "w", encoding="utf-8").write(doc)
    print("yazildi:", yol, f"{len(doc.encode('utf-8')) // 1024} KB", dil)


def uret():
    js = oku("platform.js")
    css = oku("platform.css") + "\n" + oku("tur.css")
    tur_js = oku("tur.js")
    ikon = oku("ikonlar.json")
    anahtar = js_anahtarlari(js)
    eksik = sorted(a for a in anahtar if a not in TXT_EN)
    if eksik:
        print("INGILIZCE ARAYUZ METNI EKSIK:", len(eksik))
        for x in eksik:
            print("  ", repr(x))
        sys.exit(1)
    kullanilmayan = sorted(a for a in TXT_EN if a not in anahtar)
    if kullanilmayan:
        print("kullanilmayan sozluk girdisi:", len(kullanilmayan))
    for dil in ("tr", "en"):
        insa(dil, js, css, ikon, tur_js)


if __name__ == "__main__":
    uret()
