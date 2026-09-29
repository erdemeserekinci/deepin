"""Video altyazilarinda kullanilabilecek sayilar: her biri veriden hesaplanir, elle yazilmaz.

Bir sahnenin "sayilar" listesindeki her anahtar burada cozulur; altyazidaki rakamlar bu degerlerle birebir
eslesmelidir (denetim.py sinar). Iki tur anahtar var:

  adli anahtar     uyari_sayisi, grup_uye ...  (ADLI sozlugu)
  genel anahtar    inc.<id>.<alan>             inceleme basina: uyari, kaynak, varlik, eksik, ham, grup_uye,
                                               graf.normal, graf.yalniz, graf.engel, graf.grup_engel (ilk kisi)
                   kisi.<ad>.<alan>            kisi sorgusu: istek, engel, oturum, yonetici (haftalik toplam)
                   mitre.<kod>.uyari           o teknige dusen uyari sayisi
                   gun.<YYYY-AA-GG>            o tarihin gun sayisi (ornek: 30), tarih donemde olmali

Yeni bir sayi gerekirse ADLI sozlugune veriden hesaplanan bir anahtar ekle; sayiyi dogrudan yazma.
"""


def _inc(D, i):
    for x in D["incelemeler"]:
        if x["id"] == i:
            return x
    raise KeyError(f"inceleme yok: {i}")


def adli(D):
    inc = _inc(D, "ayrilan-hesap")
    k = inc["graf"]["kisiler"][0]
    return {
        "uyari_sayisi": len(D["uyarilar"]),
        "inceleme_sayisi": len(D["incelemeler"]),
        "yuksek_sayisi": sum(1 for i in D["incelemeler"] if i["oncelik"] == "yuksek"),
        "orta_sayisi": sum(1 for i in D["incelemeler"] if i["oncelik"] == "orta"),
        "dusuk_sayisi": sum(1 for i in D["incelemeler"] if i["oncelik"] == "dusuk"),
        "gun_sayisi": len(D["gunler"]),
        "teknik_sayisi": len(D["mitre"]),
        "kisi_sorgusu_sayisi": len(D["haftalar"]),
        "ag_bolge": len(D["ag"]["kumeler"]),
        "ag_cift": len(D["ag"]["kenarlar"]),
        "kayit_kaynagi": len(D["veri_kaynaklari"]),
        "baglam_dosyasi": len(D["baglam"]),
        "dogrulayan_kaynak": len(inc["kaynaklar"]),
        "grup_uye": inc["graf"]["grup"]["uye"],
        "yalniz_ag": k["ozet"]["yalniz"],
        "engel_ag": k["ozet"]["engel"] + k["ozet"]["grup_engel"],
        "ilk_ulasma_gunu": int(min(a["gun"] for a in k["ag"] if a["sinif"] == "yalniz")[-2:]),
    }


def coz(D, anahtar):
    A = adli(D)
    if anahtar in A:
        return A[anahtar]
    p = anahtar.split(".")
    if p[0] == "inc" and len(p) >= 3:
        i = _inc(D, p[1])
        alan = ".".join(p[2:])
        tablo = {"uyari": lambda: len(i["uyarilar"]), "kaynak": lambda: len(i["kaynaklar"]),
                 "varlik": lambda: len(i["varliklar"]), "eksik": lambda: len(i["eksik"]),
                 "ham": lambda: i["ham"]["toplam"], "grup_uye": lambda: i["graf"]["grup"]["uye"]}
        if alan in tablo:
            return tablo[alan]()
        if alan.startswith("graf."):
            return i["graf"]["kisiler"][0]["ozet"][alan[5:]]
    if p[0] == "kisi" and len(p) == 3:
        return sum(g[p[2]] for g in D["haftalar"][p[1]]["gunler"])
    if p[0] == "mitre" and len(p) == 3 and p[2] == "uyari":
        return sum(1 for u in D["uyarilar"] if p[1] in u["mitre"])
    if p[0] == "gun" and len(p) == 2:
        if p[1] not in {g["tarih"] for g in D["gunler"]}:
            raise KeyError(f"tarih donemde yok: {p[1]}")
        return int(p[1][-2:])
    raise KeyError(f"bilinmeyen sayi anahtari: {anahtar}")
