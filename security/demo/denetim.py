#!/usr/bin/env python3
"""Sekmeler arasi sayi tutarliligi ve ekran metni taramasi.

    python3 denetim.py            (bu klasorden)

Kural: bir sayinin gectigi her sekme ayni listeden beslenir. Bu betik bunu veri uzerinde sinar;
tutmayan varsa neyin neye esit olmasi gerektigini yazar ve cikis kodu 1 doner.
"""
import json, os, re, sys

sys.dont_write_bytecode = True
KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(KOK, "kaynak"))
import veri  # noqa: E402

D = veri.uret()
INC = {i["id"]: i for i in D["incelemeler"]}
UY = {u["id"]: u for u in D["uyarilar"]}
H = D["haftalar"]
hata = []


def sn(s):
    return int(str(s).replace(".", ""))


def kontrol(ad, ok, ayr=""):
    if not ok:
        hata.append((ad, ayr))


def tablo(inc, baslik):
    return [k for k in INC[inc]["kanit"] if k["baslik"] == baslik][0]


for i in D["incelemeler"]:
    a = dict(i["alan"])
    kontrol(i["id"] + ": alan Uyari = uyari listesi", sn(a["Uyarı"]) == len(i["uyarilar"]), (a["Uyarı"], len(i["uyarilar"])))
    kontrol(i["id"] + ": uyarilar bu incelemeye ait", all(UY[x]["inc"] == i["id"] for x in i["uyarilar"]))
kontrol("uyari toplami", len(UY) == sum(len(i["uyarilar"]) for i in D["incelemeler"]))

for kid in ("iletisim-merkezi", "dijital-kanallar"):
    i = INC[kid]
    t = tablo(kid, "Kişiler")
    kol = t["kolon"]
    ii, jn, ka = kol.index("Engellenen istek"), kol.index("Yoğun gün"), kol.index("Engellenen ağ")
    kontrol(kid + ": ham toplam = kisiler toplami", sum(sn(r[ii]) for r in t["satir"]) == i["ham"]["toplam"])
    kontrol(kid + ": varlik sayisi = kisi satiri", len(i["varliklar"]) == len(t["satir"]) == len(i["uyarilar"]))
    for r in t["satir"]:
        w = H[r[0]]
        kontrol(kid + " " + r[0] + ": haftalik engel toplami", sum(g["engel"] for g in w["gunler"]) == sn(r[ii]))
        pk = max(w["gunler"], key=lambda g: g["engel"])["gun"]
        kontrol(kid + " " + r[0] + ": yogun gun", veri.gun_et(pk) == r[jn])
        kontrol(kid + " " + r[0] + ": uyari gunu = yogun gun", [UY[x]["gun"] for x in i["uyarilar"] if UY[x]["varlik"] == r[0]][0] == pk)
    n = [sn(r[ka]) for r in t["satir"]]
    kontrol(kid + ": metrik min-max", i["metrikler"][0][0] == f"{min(n)}-{max(n)}")
    for k in i["graf"]["kisiler"]:
        oz = k["ozet"]
        kontrol(kid + " " + k["ad"] + ": graf engel + grup engel = tablo", oz["engel"] + oz["grup_engel"] == sn([r for r in t["satir"] if r[0] == k["ad"]][0][ka]))

i = INC["uretim-servisleri"]
tp = sum(sn(r[3]) for r in tablo("uretim-servisleri", "Servisler")["satir"])
kontrol("servis: ham toplam", tp == i["ham"]["toplam"])
kontrol("servis: metrik", sn(i["metrikler"][0][0]) == tp)
kontrol("servis: kod dagilimi toplami", sum(sn(r[2]) for r in tablo("uretim-servisleri", "Cevap kodu dağılımı")["satir"]) == tp)

w, i = H["ktuncer"], INC["ayrilan-hesap"]
kontrol("ktuncer: haftalik istek = ham toplam = graf istek toplami", sum(g["istek"] for g in w["gunler"]) == i["ham"]["toplam"] == sum(x["istek"] for x in i["graf"]["kisiler"][0]["ag"]))
kontrol("ktuncer: oturum toplami", sum(g["oturum"] for g in w["gunler"]) == 9)

w, i = H["tsahin"], INC["yonetici-istasyon"]
kontrol("tsahin: yonetici oturumu = ham = istasyon tablosu", sum(g["yonetici"] for g in w["gunler"]) == i["ham"]["toplam"] == sum(sn(r[3]) for r in tablo("yonetici-istasyon", "İstasyonlar")["satir"]))

for kid, kisi in (("surekli-engel-mdemir", "mdemir"), ("yeni-ag-bkoc", "bkoc"), ("surekli-engel-sguler", "sguler")):
    i = INC[kid]
    kontrol(kid + ": haftalik engel = ham", sum(g["engel"] for g in H[kisi]["gunler"]) == i["ham"]["toplam"])
    kontrol(kid + ": graf engel istegi = ham", sum(x["istek"] for x in i["graf"]["kisiler"][0]["ag"] if x["sinif"] == "engel") == i["ham"]["toplam"])

i = INC["dis-tarama"]
kontrol("dis tarama: bloklar = ham", sum(sn(r[2]) for r in tablo("dis-tarama", "Bloklar")["satir"]) == i["ham"]["toplam"])
kontrol("dis tarama: hedefler = ham", sum(sn(r[1]) for r in tablo("dis-tarama", "Hedef uygulamalar")["satir"]) == i["ham"]["toplam"])
for kid, bas in (("olu-adres", "Adresler"), ("yoklama", "Servisler"), ("test-ortami", "Servisler")):
    kontrol(kid + ": tablo = ham", sum(sn(r[3]) for r in tablo(kid, bas)["satir"]) == INC[kid]["ham"]["toplam"])

K = D["ag"]["kenarlar"]
kumeler = {e["kaynak"] for e in K} | {e["hedef"] for e in K}
kontrol("ag: kume listesi kenarlari kapsiyor", kumeler <= set(D["ag"]["kumeler"]), kumeler - set(D["ag"]["kumeler"]))

# ekran metni: log satirlari haric her metin
KURAL = {"uzun tire": r"[—–]", "ic kod": r"\b[A-Z]-\d\b|vakalar\.json|hücre|hucre|\bV1\b|\bV2\b", "soru isareti": r"\?",
         "maskeli ad": r"\*\*\*", "sizinti": r"\b(TODO|lorem|undefined|NaN|null)\b"}
metin = []


def gez(x, yol=""):
    if isinstance(x, dict):
        for k, v in x.items():
            if k not in ("satirlar", "dosya"):
                gez(v, yol + "/" + k)
    elif isinstance(x, list):
        for v in x:
            gez(v, yol)
    elif isinstance(x, str):
        metin.append((yol, x))


gez(D)
for yol, s in metin:
    for ad, rg in KURAL.items():
        if re.search(rg, s):
            hata.append(("metin: " + ad, yol + " | " + s[:70]))


# ---- Ingilizce surum: her metin cifti ayni sayilari tasimali, Turkce harf kalmamali (kisi adlari haric)
sys.path.insert(0, KOK)
import uret as U  # noqa: E402

tr_d = U.veri_hazirla("tr")
en_d = U.veri_hazirla("en")
isimler = {k["ad_soyad"] for k in tr_d["kisiler"].values()} | set(U.cevir.KORU_ISIM)


def rakamlar(s):
    return sorted(re.findall(r"\d+", re.sub(r"(?<=\d)[.,](?=\d)", "", s)))


def ikili(a, b, yol=""):
    if isinstance(a, dict):
        for k in a:
            ikili(a[k], b[k], yol + "/" + k)
    elif isinstance(a, (list, tuple)):
        if len(a) != len(b):
            hata.append(("EN: liste uzunlugu", yol))
            return
        for x, y in zip(a, b):
            ikili(x, y, yol)
    elif isinstance(a, str) and yol.split("/")[-1] not in ("satirlar", "dosya", "yon"):
        if rakamlar(a) != rakamlar(b):
            hata.append(("EN: sayilar farkli " + yol, a[:60] + " || " + b[:60]))
        kalan = b
        for n in isimler:
            kalan = kalan.replace(n, "")
        if re.search(r"[çğıöşüÇĞİÖŞÜ]", kalan):
            hata.append(("EN: Turkce harf " + yol, b[:70]))


ikili(tr_d, en_d)

# ---- video senaryolari: altyazidaki her sayi veriden gelmeli, TR ve EN ayni sayilari tasimali, sayfa adi arayuzdekiyle ayni olmali
import senaryo_sayilari as SS  # noqa: E402

SEN_DIR = os.path.join(KOK, "kaynak", "senaryolar")
SENARYOLAR = {f[:-5]: json.load(open(os.path.join(SEN_DIR, f), encoding="utf-8")) for f in sorted(os.listdir(SEN_DIR)) if f.endswith(".json")}
kontrol("video: en az bir senaryo var", bool(SENARYOLAR))
kontrol("video: varsayilan senaryo urun_turu var", "urun_turu" in SENARYOLAR)
ADIM_TIPLERI = {"tik", "imlec", "tikla", "bekle", "kaydir", "yaz", "gonder", "git", "sec", "panel", "kapanis", "kontrol"}
kontrol("video: ilk ulasma gunu hafta tablosunda ilk kez", any(
    "ulaşıldı" in x[1] for g in H["ktuncer"]["gunler"] if int(g["gun"][-2:]) == SS.adli(D)["ilk_ulasma_gunu"] for x in g["ilk"]))
for sad, SEN in SENARYOLAR.items():
    adlar = [sh.get("ad") for sh in SEN.get("sahneler", [])]
    kontrol(f"video {sad}: sahne adlari tekil ve dolu", len(adlar) == len(set(adlar)) and all(adlar), adlar)
    for sh in SEN.get("sahneler", []):
        yer = f"video {sad}/{sh.get('ad')}"
        ay = sh.get("altyazi") or {}
        try:
            bek = sorted(str(SS.coz(D, x)) for x in sh.get("sayilar", []))
        except KeyError as e:
            hata.append((yer + ": sayi anahtari", str(e)))
            bek = []
        for dil in ("tr", "en"):
            m = ay.get(dil, "") if isinstance(ay, dict) else ""
            kontrol(f"{yer} {dil}: altyazi sayilari veriden", rakamlar(m) == bek, (rakamlar(m), bek))
            for ad, rg in (("uzun tire", r"[—–]"), ("soru isareti", r"\?"), ("ic kod", r"\b[A-Z]-\d\b|hucre|\.json")):
                if re.search(rg, m):
                    hata.append((f"{yer} {dil}: {ad}", m[:70]))
        kapanis = any(a[0] == "kapanis" for a in sh.get("adimlar", []))
        if not kapanis:
            kontrol(f"{yer}: iki dilde altyazi var", isinstance(ay, dict) and bool(ay.get("tr")) and bool(ay.get("en")))
        for ad in sh.get("arayuz_adi", []):
            kontrol(f"{yer} tr: altyazida arayuz adi '{ad}'", ad.lower() in ay.get("tr", "").lower())
            kontrol(f"{yer} en: altyazida arayuz adi '{U.TXT_EN.get(ad)}'", U.TXT_EN.get(ad, "\0").lower() in ay.get("en", "").lower())
        for a in sh.get("adimlar", []):
            kontrol(f"{yer}: bilinen adim tipi '{a[0]}'", a[0] in ADIM_TIPLERI)
            ek = a[3] if len(a) > 3 and isinstance(a[3], dict) else {}
            if a[0] == "yaz":
                mt = ek.get("metin")
                kontrol(f"{yer}: yazilacak metin iki dilde", isinstance(mt, dict) and bool(mt.get("tr")) and bool(mt.get("en")))
    if any(a[0] == "kapanis" for sh in SEN.get("sahneler", []) for a in sh["adimlar"]):
        kp = SEN.get("kapanis", {})
        kontrol(f"video {sad}: kapanista demo notu iki dilde", "Kurgusal" in kp.get("not", {}).get("tr", "") and "fictional" in kp.get("not", {}).get("en", ""))

print(f"{len(D['incelemeler'])} inceleme, {len(D['uyarilar'])} uyari, {len(metin)} metin tarandi, {len(SENARYOLAR)} video senaryosu")
if hata:
    print(f"TUTARSIZLIK: {len(hata)}")
    for h in hata:
        print(" -", h)
    sys.exit(1)
print("Tutarli: sekmeler arasi sayilar ve ekran metni temiz.")
