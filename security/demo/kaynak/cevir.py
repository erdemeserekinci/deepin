# -*- coding: utf-8 -*-
"""Veri katmanini Ingilizceye cevirir.

Tek mantik, iki dil: veri.py Turkce uretir (sayilar, tarihler, tutarlilik orada), bu modul her metni
SABLONA indirger ve kaynak/ceviri_veri_en.json sozlugunden Ingilizcesini koyar.

Sablon: metindeki degisken parcalar yer tutucuya cevrilir, sozlukte anahtar bu sablondur.
  {N} sayi   {P} yuzde (%74)   {D} tarih (17 Eyl, 21 Ağustos, 4 Tem 2026)   {T} saat (01:10)   {K} degismeyen kimlik (adres, makine adi)
Ingilizce degerde ayni yer tutucular kullanilir; sira degisecekse {N1} {N2} gibi kaynaktaki sirasi yazilir.
Deger {"1": "...", "*": "..."} ise ilk sayi 1 iken birinci, degilse ikinci metin kullanilir (tekil/cogul).
Sozlukte olmayan Turkce metin HATA verir: sessiz gecis yok.
"""
import json
import os
import re

KOK = os.path.dirname(os.path.abspath(__file__))
AY_EN = {"Eyl": "Sep", "Eylül": "Sep", "Ağu": "Aug", "Ağustos": "Aug", "Tem": "Jul"}

RE_KIMLIK = re.compile(r"\b(?:MRD[A-Z]+\d+|\d{1,3}(?:\.\d{1,3}){3}(?:/\d+)?|[a-z0-9-]+(?:\.[a-z0-9-]+)*\.mrd\.local|[\w-]+\.zip)\b")
RE_TARIH = re.compile(r"\b(\d{1,2}) (Eylül|Eyl|Ağustos|Ağu|Tem)(?: (\d{4}))?(?![a-zçğıöşü])")
RE_SAAT = re.compile(r"\b\d{1,2}:\d{2}\b")
RE_YUZDE = re.compile(r"%\d+(?:,\d+)?")
RE_SAYI = re.compile(r"\d{1,3}(?:\.\d{3})+|\d+(?:,\d+)?")
RE_TUR = re.compile(r"[çğıöşüÇĞİÖŞÜ]")
RE_KIMLIK_TAM = re.compile(r"^[A-Za-z0-9_.\-:/\\@*#]+$")
RE_ISIM = None

import sys
sys.path.insert(0, KOK)
from ceviri_veri_en import SOZLUK  # noqa: E402

KORU_ISIM = ["Selim Yavuz", "Aslı Bayram", "Cem Tunç", "Deniz Erdem"]


def sablon(s):
    """(sablon, degerler) dondurur; degerler yer tutucu sirasiyla."""
    degerler = []

    def al(tur):
        def f(m):
            degerler.append((tur, m))
            return "\x00%s\x00" % tur
        return f

    t = RE_ISIM.sub(al("K"), s) if RE_ISIM else s
    t = RE_KIMLIK.sub(al("K"), t)
    t = RE_TARIH.sub(al("D"), t)
    t = RE_SAAT.sub(al("T"), t)
    t = RE_YUZDE.sub(al("P"), t)
    t = RE_SAYI.sub(al("N"), t)
    t = re.sub(r"\x00([KDTPN])\x00", r"{\1}", t)
    return t, degerler


def sayi_en(m):
    s = m.group(0)
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+", s):
        return s.replace(".", ",")
    return s.replace(",", ".")


def deger_en(tur, m):
    if tur == "K" or tur == "T":
        return m.group(0)
    if tur == "N":
        return sayi_en(m)
    if tur == "P":
        return sayi_en(re.match(r".*", m.group(0)[1:])) + "%"
    if tur == "D":
        g = m.groups()
        ay = AY_EN[g[1]]
        return f"{ay} {int(g[0])}" + (f", {g[2]}" if g[2] else "")


def cevir_metin(s, eksik):
    t, dg = sablon(s)
    if t in SOZLUK:
        v = SOZLUK[t]
    else:
        if RE_KIMLIK_TAM.match(s) and not RE_TUR.search(s):
            return s
        eksik.add(t)
        return s
    if isinstance(v, dict):
        ilk = next((d for d in dg if d[0] == "N"), None)
        v = v["1"] if (ilk is not None and ilk[1].group(0) == "1" and "1" in v) else v.get("*", v.get("1"))
    if "\x00" in v:
        raise ValueError(v)
    sayac = {"N": 0, "P": 0, "D": 0, "T": 0, "K": 0}
    tur_deger = {k: [d for d in dg if d[0] == k] for k in sayac}

    def yer(m):
        tur, idx = m.group(1), m.group(2)
        liste = tur_deger[tur]
        if idx:
            i = int(idx) - 1
        else:
            i = sayac[tur]
            sayac[tur] += 1
        return deger_en(tur, liste[i][1])
    return re.sub(r"\{([NPDTK])(\d?)\}", yer, v)


ATLA = {"satirlar", "dosya", "id", "inc", "kod", "sinif", "ton", "yon", "cidr", "tip", "tarih", "gun", "oncelik"}


def isimleri_ayarla(isimler):
    global RE_ISIM
    tum = set(isimler) | set(KORU_ISIM)
    RE_ISIM = re.compile("|".join(re.escape(n) for n in sorted(tum, key=len, reverse=True)))


def cevir(x, eksik, anahtar=None):
    if isinstance(x, dict):
        atla = ATLA | ({"tur"} if "tur_ad" in x else set())
        return {k: (v if k in atla else cevir(v, eksik, k)) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [cevir(v, eksik, anahtar) for v in x]
    if isinstance(x, str):
        return cevir_metin(x, eksik)
    return x
