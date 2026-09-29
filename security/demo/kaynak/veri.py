# -*- coding: utf-8 -*-
"""deepin.security platform demosu icin SENTETIK veri uretici.

Kurgusal kurum, kurgusal kisiler, kurgusal adresler (adres plani hicbir gercek kurumun planina dayanmaz). Gercek musteri verisi yoktur.
Bicim, urunun gercek cikti bicimini taklit eder (inceleme, uyari, kanit, ham kayit, graf, zaman).
Ayni tohum ayni cikti verir (iki kosu bayt bayt ayni).

Sayilar tek yerden uretilir: kart, panel, tablo ve grafik ayni listeden okur.
"""
import random
import unicodedata

KURUM = "Meridyen Finans"
KURUM_ALT = "Güvenlik Operasyonları"
GUNLER = ["2026-04-27", "2026-04-28", "2026-04-29", "2026-04-30", "2026-05-01", "2026-05-02", "2026-05-03"]
AY = {"04": "Nis", "05": "May"}
AY_EN = {"04": "Apr", "05": "May"}
GUN_ADI = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]


def gun_et(g):
    return f"{int(g[8:])} {AY[g[5:7]]}"


def sayi(n):
    return f"{n:,}".replace(",", ".")


def paylastir(toplam, agirlik):
    s = sum(agirlik)
    ham = [toplam * a / s for a in agirlik]
    t = [int(x) for x in ham]
    for i in sorted(range(len(agirlik)), key=lambda i: -(ham[i] - t[i]))[:toplam - sum(t)]:
        t[i] += 1
    return t


def en_yogun(dizi):
    return GUNLER[max(range(len(dizi)), key=lambda i: dizi[i])]


def sade(s):
    s = s.replace("ı", "i").replace("İ", "I").replace("ş", "s").replace("Ş", "S").replace("ğ", "g").replace("Ğ", "G")
    s = s.replace("ü", "u").replace("Ü", "U").replace("ö", "o").replace("Ö", "O").replace("ç", "c").replace("Ç", "C")
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)).lower()


KAYNAK = {
    "vpn": {"ad": "VPN günlükleri", "sistem": "Palo Alto GlobalProtect"},
    "dc": {"ad": "Etki alanı denetleyicisi", "sistem": "Microsoft Windows"},
    "citrix": {"ad": "Uygulama geçidi", "sistem": "Citrix ADC"},
    "fw": {"ad": "İç güvenlik duvarı", "sistem": "Check Point"},
    "edr": {"ad": "Uç nokta koruması", "sistem": "Trend Micro Apex Central"},
}

MITRE = {
    "T1595": ("Aktif tarama", "Keşif"),
    "T1595.002": ("Zafiyet taraması", "Keşif"),
    "T1190": ("İnternete açık uygulamayı sömürme", "İlk erişim"),
    "T1133": ("Dış uzak servisler", "İlk erişim"),
    "T1078": ("Geçerli hesaplar", "İlk erişim"),
    "T1078.002": ("Alan hesapları", "Yetki yükseltme"),
    "T1098": ("Hesap manipülasyonu", "Kalıcılık"),
    "T1021": ("Uzak servisler", "Yanal hareket"),
    "T1021.002": ("SMB ve yönetici paylaşımları", "Yanal hareket"),
    "T1046": ("Ağ servisi keşfi", "İç keşif"),
    "T1018": ("Uzak sistem keşfi", "İç keşif"),
    "T1135": ("Ağ paylaşımı keşfi", "İç keşif"),
    "T1105": ("Araç aktarımı", "Komuta ve kontrol"),
}
TAKTIK_SIRASI = ["Keşif", "İlk erişim", "Kalıcılık", "Yetki yükseltme", "İç keşif", "Yanal hareket", "Komuta ve kontrol"]

SEGMENT = {
    "10.93.24.0/24": "Ödeme Sistemleri, uygulama",
    "10.93.61.0/24": "Ödeme Sistemleri, veritabanı",
    "10.93.101.0/24": "Kart Sistemleri, uygulama",
    "10.93.191.0/24": "Çekirdek Bankacılık, uygulama",
    "10.60.241.0/24": "Üretim uygulama sunucuları",
    "10.60.22.0/24": "Üretim uygulama sunucuları 2",
    "10.60.89.0/24": "Yönetim ağı",
    "10.60.9.0/24": "Güvenlik yönetim ağı",
    "10.160.127.0/24": "Genel Müdürlük kullanıcı ağı",
    "10.160.164.0/24": "Genel Müdürlük kullanıcı ağı 2",
    "10.71.24.0/24": "Felaket Merkezi, ödeme sistemleri",
    "10.82.90.0/24": "Şube ağ cihazları",
    "10.60.67.0/24": None,
}

ERKEK = ["Ahmet", "Mehmet", "Mustafa", "Emre", "Burak", "Onur", "Kaan", "Serkan", "Volkan", "Tolga", "Cem", "Barış", "Uğur", "Fatih", "Murat", "Yusuf", "Hakan", "Levent", "Orhan", "Selim", "Berk", "Deniz", "Koray", "Ozan", "Sinan"]
KADIN = ["Ayşe", "Elif", "Zeynep", "Selin", "Derya", "Ceren", "Gizem", "Pınar", "Esra", "Merve", "Buse", "Aslı", "Özlem", "Hande", "Sibel", "Ebru", "İrem", "Nilay", "Tuğba", "Dilara", "Seda", "Burcu", "Melis", "Gamze", "Yasemin"]
SOYAD = ["Yılmaz", "Kaya", "Demir", "Şahin", "Çelik", "Yıldız", "Yıldırım", "Öztürk", "Aydın", "Özdemir", "Arslan", "Doğan", "Kılıç", "Aslan", "Çetin", "Kara", "Koç", "Kurt", "Özkan", "Şimşek", "Polat", "Korkmaz", "Erdoğan", "Güneş", "Aksoy", "Avcı", "Türk", "Bulut", "Tekin", "Acar", "Güler", "Ateş", "Duman", "Akın", "Sezer", "Bozkurt", "Karakaya", "Uysal", "Taş", "Eren", "Sönmez", "Kaplan", "Yavuz", "Bayram", "Erdem", "Tunç", "Coşkun", "Işık", "Balcı", "Çakır"]

KISI = {}


def kisi_ekle(ad_soyad, unvan, birim, ik="Aktif çalışıyor", kullanici=None):
    ad, soyad = ad_soyad.split(" ", 1)
    k = kullanici or (sade(ad)[0] + sade(soyad).replace(" ", ""))
    n = 2
    taban = k
    while k in KISI:
        k = f"{taban}{n}"
        n += 1
    KISI[k] = {"ad_soyad": ad_soyad, "unvan": unvan, "birim": birim, "ik": ik}
    return k


def havuz_kisi(rng, adet, unvanlar, birim, ozel=None):
    cikti = []
    ozel = ozel or {}
    while len(cikti) < adet:
        ad = rng.choice(ERKEK + KADIN)
        soyad = rng.choice(SOYAD)
        ad_soyad = f"{ad} {soyad}"
        k = sade(ad)[0] + sade(soyad)
        if k in KISI or ad_soyad in [KISI[x]["ad_soyad"] for x in cikti]:
            continue
        unvan = unvanlar[len(cikti) % len(unvanlar)] if len(cikti) not in ozel else ozel[len(cikti)]
        cikti.append(kisi_ekle(ad_soyad, unvan, birim, kullanici=k))
    return cikti


# ---------------------------------------------------------------- ham kayit uretimi
def saat_uret(rng, gun, aralik):
    s = rng.randint(aralik[0], aralik[1])
    return f"{s:02d}:{rng.randint(0, 59):02d}:{rng.randint(0, 59):02d}"


def ay_kisa(g):
    return f"{AY[g[5:7]]} {int(g[8:]):2d}".replace("  ", " ")


def ham_satir(kaynak, rng, gun, saat, **k):
    ay = AY_EN[gun[5:7]]
    d = int(gun[8:])
    if kaynak == "vpn":
        return (f"{ay} {d:02d} {saat} mrd-vpn01 LEEF:2.0|Palo Alto Networks|PAN-OS|10.2.4|TRAFFIC|x7C|"
                f"devTime={ay} {d:02d} 2026 {saat} GMT|src={k['src']}|dst={k['dst']}|usrName=MERIDYEN\\{k['kullanici']}|"
                f"proto=tcp|dstPort={k['port']}|action={k['aksiyon']}|bytesSent={rng.randint(400, 9000)}|"
                f"bytesReceived={rng.randint(0, 120000) if k['aksiyon'] == 'allow' else 0}|RuleName={k.get('kural', 'vpn-kullanici-erisim')}")
    if kaynak == "dc":
        kod = k.get("kod", "4624")
        return (f"{ay} {d:02d} {saat} mrd-dc02 MSWinEventLog\t1\tSecurity\t{rng.randint(5100000, 5199999)}\t"
                f"{ay} {d:02d} {saat} 2026\t{kod}\tMicrosoft-Windows-Security-Auditing\tMERIDYEN\\{k['kullanici']}\tN/A\t"
                f"Success Audit\tmrd-dc02.mrd.local\tLogon\t{k.get('metin', 'An account was successfully logged on.')} "
                f"Logon Type: {k.get('tip', 10)} Account Name: {k['kullanici']} Workstation Name: {k['istasyon']} "
                f"Source Network Address: {k['src']}")
    if kaynak == "fw":
        return (f"{ay} {d:02d} {saat} mrd-cp01 CheckPoint {rng.randint(10000, 99999)} - [action:\"Accept\"; ifdir:\"inbound\"; "
                f"src:\"{k['src']}\"; dst:\"{k['dst']}\"; service:\"{k['port']}\"; proto:\"6\"; rule_name:\"{k.get('kural', 'vpn-odeme')}\"; "
                f"src_user_name:\"{k['ad_soyad']} ({k['kullanici']})\"; src_machine_name:\"{k['istasyon']}\"]")
    if kaynak == "citrix":
        return (f"<134> {ay} {d:02d} 2026 {saat} GMT mrd-adc01 0-PPE-1 : default SSLVPN HTTPREQUEST {rng.randint(100000, 999999)} 0 : "
                f"Source {k['src']}:{rng.randint(30000, 60000)} - Destination {k['dst']}:8443 - Vserver {k['host']} - Method GET - "
                f"URL {k['yol']} - Status {k['durum']}")
    if kaynak == "edr":
        return (f"CEF:0|Trend Micro|Apex Central|2019|IN:1001|{k['olay']}|6|deviceExternalId=1 rt={ay} {d:02d} 2026 {saat} GMT+03:00 "
                f"shost={k['makine']} suser=MERIDYEN\\{k['kullanici']} fname={k['dosya']} filePath={k['yol']} act={k['aksiyon']} cat={k['kategori']}")
    if kaynak == "waf":
        return (f"{ay} {d:02d} {saat} mrd-adc02 ns: APPFW {k['imza']} {rng.randint(1000, 9999)} 0 : {k['src']} "
                f"{rng.randint(20000, 60000)}-PPE0 - default_appfw {k['aciklama']} {k['url']} <{k['sonuc']}>")
    raise ValueError(kaynak)


def ham_paket(kaynak, rng, uretici, adet, toplam, dosya, gunler, saat_araligi=(0, 23)):
    satirlar = []
    for i in range(adet):
        g = gunler[i % len(gunler)] if len(gunler) < adet else gunler[i * len(gunler) // adet]
        satirlar.append((g, saat_uret(rng, g, saat_araligi), i))
    satirlar.sort()
    cikti = [ham_satir(kaynak, rng, g, s, **uretici(rng, i)) for (g, s, i) in satirlar]
    return {"dosya": dosya, "toplam": toplam, "satirlar": cikti, "kaynak": kaynak}


# ---------------------------------------------------------------- ag dugumleri (graf)
def rastgele_cidr(rng, kullanilan):
    while True:
        c = f"10.{rng.choice([137, 214, 124, 235, 212, 111, 44, 164, 195, 28, 206])}.{rng.randint(1, 254)}.0/24"
        if c not in kullanilan:
            kullanilan.add(c)
            return c


def ag_listesi(rng, normal=(), yalniz=(), engel=(), rastgele_engel=0, grup_engel=0, istek_araligi=(30, 400), gunler=None, engel_adlari=()):
    gunler = gunler or GUNLER[1:]
    erken = gunler[:3]
    gec = gunler[2:] or gunler
    kullanilan = set()
    dugum = []
    for c in normal:
        kullanilan.add(c)
        dugum.append({"cidr": c, "ad": SEGMENT.get(c), "sinif": "normal", "istek": rng.randint(*istek_araligi) * 6,
                      "gun": rng.choice(erken), "grup_pay": round(rng.uniform(0.55, 0.9), 2), "gecen": None})
    for c in yalniz:
        kullanilan.add(c)
        dugum.append({"cidr": c, "ad": SEGMENT.get(c), "sinif": "yalniz", "istek": rng.randint(*istek_araligi) * 3,
                      "gun": rng.choice(gec), "grup_pay": 0.0, "gecen": None})
    for c in engel:
        kullanilan.add(c)
        dugum.append({"cidr": c, "ad": SEGMENT.get(c), "sinif": "engel", "istek": rng.randint(*istek_araligi),
                      "gun": rng.choice(gec), "grup_pay": 0.0, "gecen": 0})
    for _ in range(rastgele_engel):
        c = rastgele_cidr(rng, kullanilan)
        dugum.append({"cidr": c, "ad": None, "sinif": "engel", "istek": rng.randint(*istek_araligi), "gun": rng.choice(gec),
                      "grup_pay": 0.0, "gecen": 0})
    for _ in range(grup_engel):
        c = rastgele_cidr(rng, kullanilan)
        dugum.append({"cidr": c, "ad": None, "sinif": "grup_engel", "istek": rng.randint(*istek_araligi), "gun": rng.choice(gec),
                      "grup_pay": round(rng.uniform(0.25, 0.6), 2), "gecen": 0})
    for x in dugum:
        x["gecen"] = x["istek"] if x["sinif"] in ("normal", "yalniz") else 0
    return dugum


def ag_ozet(ag):
    o = {"normal": 0, "yalniz": 0, "engel": 0, "grup_engel": 0}
    for x in ag:
        o[x["sinif"]] += 1
    return o


# ---------------------------------------------------------------- uretim
def uret():
    rng = random.Random(29092026)
    KISI.clear()

    uyarilar = []
    incelemeler = []
    sayac = [0]

    def uyari(inc, varlik, tip, tur, ne, kaynak, gun, onem, mitre=(), kanit=None):
        sayac[0] += 1
        u = {"id": f"u{sayac[0]:03d}", "inc": inc, "varlik": varlik, "tip": tip, "tur": tur, "ne": ne, "kaynak": kaynak,
             "gun": gun, "onem": onem, "mitre": list(mitre)}
        uyarilar.append(u)
        return u["id"]

    # -------------------------------------------------- kisiler
    im_kisileri = havuz_kisi(rng, 34, ["Müşteri Temsilcisi"] * 5 + ["Kıdemli Müşteri Temsilcisi"], "Müşteri İletişim Merkezi",
                             ozel={11: "Ekip Lideri", 23: "Ekip Lideri"})
    dk_kisileri = havuz_kisi(rng, 27, ["Yazılım Geliştirme Uzmanı", "Mobil Uygulama Geliştirici", "Test Mühendisi", "Ürün Analisti"],
                             "Dijital Kanallar")
    ktuncer = kisi_ekle("Kerem Tuncer", "Kıdemli Operasyon Uzmanı", "Ödeme Operasyonları", "İşten ayrıldı, 8 Nis", "ktuncer")
    tsahin = kisi_ekle("Tolga Şahin", "Sistem Yöneticisi", "Altyapı ve Sistem Yönetimi", kullanici="tsahin")
    ugunes = kisi_ekle("Umut Güneş", "Siber Güvenlik Uzmanı", "Bilgi Güvenliği", kullanici="ugunes")
    ecetin = kisi_ekle("Elif Çetin", "Finansal Raporlama Uzmanı", "Mali İşler", kullanici="ecetin")
    mdemir = kisi_ekle("Mert Demir", "Kredi Operasyon Uzmanı", "Kredi Operasyonları", kullanici="mdemir")
    bkoc = kisi_ekle("Burcu Koç", "İç Denetçi", "İç Denetim", kullanici="bkoc")
    sguler = kisi_ekle("Sinan Güler", "Uyum Uzmanı", "Uyum", kullanici="sguler")

    # ==================================================================
    # 1. Ayrilan calisan hesabi (coklu kaynak)
    # ==================================================================
    iid = "ayrilan-hesap"
    ag1 = ag_listesi(rng, normal=["10.160.127.0/24", "10.60.241.0/24"], yalniz=["10.93.24.0/24", "10.93.61.0/24", "10.93.101.0/24"],
                     engel=["10.60.89.0/24", "10.60.9.0/24"], istek_araligi=(60, 380), gunler=GUNLER[1:5])
    for x in ag1:
        if x["cidr"] in ("10.93.24.0/24", "10.93.61.0/24", "10.93.101.0/24"):
            x["gun"] = "2026-04-30"
    vpn_top = sum(x["istek"] for x in ag1)
    yal_top = sum(x["istek"] for x in ag1 if x["sinif"] == "yalniz")
    kt_istek = paylastir(vpn_top, [0, 10, 20, 45, 17, 8, 0])
    kt_engel = paylastir(sum(x["istek"] for x in ag1 if x["sinif"] == "engel"), [0, 5, 12, 60, 17, 6, 0])
    yal_30 = round(yal_top * 0.62)
    yal_1 = round(yal_top * 0.30)
    u1 = uyari(iid, ktuncer, "kisi", "Gece saatinde oturum", "5 gece art arda VPN oturumu (01:10 ile 03:40 arası)", "vpn", "2026-04-28", 84, ["T1078", "T1133"])
    u2 = uyari(iid, ktuncer, "kisi", "Yeni iç ağa gidiş", "3 yeni iç ağa ulaştı: ödeme ve kart sistemleri", "vpn", "2026-04-30", 90, ["T1021", "T1018"])
    u3 = uyari(iid, ktuncer, "kisi", "Ayrılan personel hesabı", "Ayrılmış personelin hesabı etkin, dönemde 9 oturum açılmış", "dc", "2026-04-29", 88, ["T1078"])
    u4 = uyari(iid, ktuncer, "kisi", "Yeni iç ağa gidiş", "Hesabın bilgisayarından ödeme ağındaki 2 sunucuya bağlantı", "fw", "2026-04-30", 82, ["T1021"])
    vpn_gece = ["2026-04-28", "2026-04-29", "2026-04-30", "2026-05-01", "2026-05-02"]

    def u_vpn_ktuncer(r, i):
        g = vpn_gece[i % 5]
        hedef = r.choice(["10.93.24.15", "10.93.24.17", "10.93.61.21", "10.93.101.9"]) if g >= "2026-04-30" else r.choice(["10.160.127.31", "10.60.241.14"])
        return {"src": "10.249.53.41", "dst": hedef, "kullanici": "ktuncer", "port": r.choice([1433, 3389, 443, 8443]),
                "aksiyon": "allow", "kural": "vpn-kullanici-erisim"}

    ham1 = ham_paket("vpn", rng, u_vpn_ktuncer, 12, vpn_top, "uyari_001_ktuncer.csv", vpn_gece, (1, 3))
    incelemeler.append({
        "id": iid, "tur": "cok_kaynak", "tur_ad": "Çoklu kaynak", "puan": 94,
        "baslik": "Kerem Tuncer", "alt": "Ödeme Operasyonları, işten ayrıldı, hesap etkin",
        "ozet": "Ayrılış kaydı 8 Nisan, hesap etkin; dönemde 5 gece VPN oturumu açılmış ve 3 ödeme ve kart ağına ulaşılmış.",
        "kart_ozet": "İşten ayrıldıktan sonra hesap etkin; gece VPN ile ödeme ağlarına ulaşıldı",
        "uyarilar": [u1, u2, u3, u4], "kaynaklar": ["vpn", "dc", "fw"], "mitre": ["T1078", "T1133", "T1021", "T1018"], "asama": "İlk erişim",
        "varliklar": [{"ad": "ktuncer", "tip": "kisi", "alt": "Kerem Tuncer, Ödeme Operasyonları"},
                      {"ad": "MRDNB0388", "tip": "bilgisayar", "alt": "kayıtlı kullanıcı: Kerem Tuncer"}],
        "alan": [("Öncelik", "Yüksek"), ("Durum", "Açık"), ("Uyarı", "4"), ("Varlık", "1 kişi, 1 bilgisayar"),
                 ("Kim olduğu", "İK kaydı ve dizin hesabı"), ("Kaynak", "3, VPN, etki alanı, güvenlik duvarı"),
                 ("Görülme sıklığı", "Ayrılan 187 hesabın 1'inde"), ("Başka açıklama", "Sorulmadı"), ("Yoğun gün", "30 Nis")],
        "nedenler": ["Ayrılış sonrası hesap etkin", "3 ayrı kaynak doğruladı", "Ödeme ağına ulaşıldı", "Gece saatlerinde"],
        "metrikler": [("5", "gece oturumu"), ("3", "ulaşılan ödeme ağı"), ("3", "doğrulayan kaynak")],
        "adimlar": [("Ayrılış sonrası hesap kapatma kaydı", "İK ve kimlik yönetimi sürecinde bu hesap için iş kaydı", "İK ve kimlik yönetimi"),
                    ("VPN oturumlarının açıldığı cihaz ve sertifika", "10.249.53.41 adresini alan istemci", "Sistem ekibi"),
                    ("Ödeme ağlarındaki erişimin yetkisi", "hesabın 10.93.24.0/24 ve 10.93.61.0/24 için erişim talebi", "Ödeme sistemleri sahibi")],
        "eksik": [("Hesabın kapatılmama nedeni", "Ayrılış sonrası hesap kapatma iş kaydı", "İK ve kimlik yönetimi"),
                  ("Oturumu açan kişi", "VPN istemcisinin zimmet kaydı ve cihaz sertifikası", "Sistem ekibi"),
                  ("Erişimin yetki kaydı", "Ödeme ağları için erişim talebi ve onayı", "Ödeme sistemleri sahibi")],
        "lehine": ["ayrılıştan sonra hesap etkin", "gece saatlerinde 5 gece", "daha önce gidilmemiş ödeme ağları", "3 ayrı kaynakta iz"],
        "aleyhine": ["hesap yetkisi kalmış olabilir", "İK kaydı gecikmeli girilmiş olabilir"],
        "kanit": [
            {"baslik": "Kaynaklara göre bulgular", "kolon": ["Kaynak", "Bulgu", "Gün", "Adet"], "sayisal": [3],
             "satir": [["VPN günlükleri", "Gece saatinde oturum", "28 Nis, 2 May", "5 gece"],
                       ["VPN günlükleri", "Yeni iç ağa ulaşıldı", "30 Nis", "3 ağ"],
                       ["Etki alanı denetleyicisi", "Ayrılmış personelin hesabıyla oturum", "29 Nis, 1 May", "9 oturum"],
                       ["İç güvenlik duvarı", "Bilgisayardan ödeme ağına bağlantı", "30 Nis", "2 sunucu"]]},
            {"baslik": "Ulaşılan ağlar", "kolon": ["Ağ", "Ağ tanımı", "İstek", "Geçen", "İlk görülme", "Benzerlerinden giden"], "sayisal": [2, 3, 5],
             "satir": [[x["cidr"], x["ad"] or "kayıtlarda tanımlı değil", sayi(x["istek"]), sayi(x["gecen"]), gun_et(x["gun"]),
                        f"{round(x['grup_pay'] * 22)} / 22"] for x in ag1 if x["sinif"] in ("yalniz", "normal")]},
            {"baslik": "Bağlam", "kolon": ["Alan", "Değer"], "sayisal": [],
             "satir": [["İK durumu", "İşten ayrıldı, 8 Nis 2026"], ["Dizin hesabı", "Etkin"], ["Birim", "Ödeme Operasyonları"],
                       ["Unvan", "Kıdemli Operasyon Uzmanı"], ["Son parola değişimi", "12 Mar 2026"]]}],
        "ham": ham1, "yogun_gun": "2026-04-30",
        "zaman": [
            {"gun": "2026-04-28", "saat": "01:12", "baslik": "İlk gece VPN oturumu", "ayrinti": "10.249.53.41 adresi atandı; iç kullanıcı ağı ve uygulama sunucularına 6 bağlantı", "kaynak": "vpn", "ton": "uyari"},
            {"gun": "2026-04-29", "saat": "02:14", "baslik": "Etkileşimli oturum, yeni bilgisayar", "ayrinti": "MRDNB0388 üzerinde uzak masaüstü oturumu; hesap için ilk kez görülen bilgisayar", "kaynak": "dc", "ton": "uyari"},
            {"gun": "2026-04-30", "saat": "01:47", "baslik": "Ödeme ağlarına ilk ulaşım", "ayrinti": f"10.93.24.0/24, 10.93.61.0/24 ve 10.93.101.0/24 ağlarına {sayi(yal_30)} bağlantı, hepsi izinli", "kaynak": "vpn", "ton": "kritik"},
            {"gun": "2026-04-30", "saat": "01:52", "baslik": "Yönetim ağına deneme", "ayrinti": "10.60.89.0/24 ve 10.60.9.0/24 için istek gönderildi, engellendi", "kaynak": "fw", "ton": "uyari"},
            {"gun": "2026-05-01", "saat": "02:31", "baslik": "Aynı ağlarda ikinci gece", "ayrinti": f"Ödeme ve kart ağlarına {sayi(yal_1)} bağlantı", "kaynak": "vpn", "ton": "uyari"},
            {"gun": "2026-05-02", "saat": "03:40", "baslik": "Son gece oturumu", "ayrinti": "Oturum 3 saat 40 dakika sürdü", "kaynak": "vpn", "ton": "bilgi"}],
        "graf": {"tur": "kisi", "kisiler": [{"ad": "ktuncer", "ad_soyad": "Kerem Tuncer", "alt": "Ödeme Operasyonları", "ag": ag1, "ozet": ag_ozet(ag1)}],
                 "grup": {"ad": "Ödeme Operasyonları", "uye": 22}}})

    # ==================================================================
    # 2. Musteri Iletisim Merkezi (kume)
    # ==================================================================
    iid = "iletisim-merkezi"
    uyeler = im_kisileri[:9]
    agsay = [274, 236, 228, 203, 191, 187, 162, 148, 137]
    im_uyari, im_graf, im_satir = [], [], []
    toplam_istek = 0
    im_gun = {}
    for sira, (k, n) in enumerate(zip(uyeler, agsay)):
        istek = n * rng.randint(6, 12)
        agirlik = [0, 0, 10, 58, 22, 8, 2] if sira < 7 else [0, 0, 55, 30, 10, 4, 1]
        engel_gun = paylastir(istek, agirlik)
        gun = en_yogun(engel_gun)
        toplam_istek += istek
        im_uyari.append(uyari(iid, k, "kisi", "Grup davranışı", f"{n} iç ağa istek gönderdi, hiçbiri geçmedi (grupta olağan 4)", "vpn", gun, 88, ["T1046", "T1018"]))
        ag = ag_listesi(rng, normal=["10.160.127.0/24", "10.60.241.0/24"], engel=[], rastgele_engel=14, grup_engel=3,
                        istek_araligi=(4, 40), gunler=GUNLER[2:5])
        if len(im_graf) < 3:
            for x in ag:
                if x["sinif"] == "normal":
                    x["grup_pay"] = round(rng.uniform(0.7, 0.95), 2)
        ge = sum(x["istek"] for x in ag if x["sinif"] == "grup_engel")
        normal_istek = sum(x["istek"] for x in ag if x["sinif"] == "normal")
        ozet = ag_ozet(ag)
        ozet["engel"] = n - ozet["grup_engel"]
        im_gun[k] = {"istek": paylastir(istek + normal_istek, agirlik), "engel": engel_gun}
        im_graf.append({"ad": k, "ad_soyad": KISI[k]["ad_soyad"], "alt": KISI[k]["unvan"], "ag": ag, "ozet": ozet, "engel_istek": istek - ge})
        im_satir.append([k, KISI[k]["ad_soyad"], KISI[k]["unvan"], sayi(n), "4", "0", sayi(istek), gun_et(gun)])
    im_top_gun = [sum(im_gun[k]["engel"][i] for k in uyeler) for i in range(7)]
    im_zaman = [
        {"gun": GUNLER[0], "saat": "", "baslik": "Taban günü", "ayrinti": "34 kişinin hiçbiri olağan dışı sayıda ağa istek göndermedi", "kaynak": "vpn", "ton": "bilgi"},
        {"gun": GUNLER[2], "saat": "", "baslik": "İlk engellenen istekler", "ayrinti": f"9 kişiden toplam {sayi(im_top_gun[2])} engellenen istek", "kaynak": "vpn", "ton": "uyari"},
        {"gun": GUNLER[3], "saat": "", "baslik": "En yoğun gün", "ayrinti": f"9 kişinin tamamından {sayi(im_top_gun[3])} engellenen istek", "kaynak": "vpn", "ton": "kritik"},
        {"gun": GUNLER[4], "saat": "", "baslik": "Yoğunluk düştü", "ayrinti": f"{sayi(im_top_gun[4])} engellenen istek, 30 Nisan'ın %{round(100 * im_top_gun[4] / im_top_gun[3])} kadarı", "kaynak": "vpn", "ton": "bilgi"}]
    ham2_dosya = "uyari_002_iletisim_merkezi.csv"

    def u_vpn_im(r, i):
        k = uyeler[i % 9]
        return {"src": f"10.249.{[16, 53, 90][i % 3]}.{20 + i}", "dst": f"10.{r.choice([137, 214, 212, 111, 44, 164, 195])}.{r.randint(1, 254)}.{r.randint(2, 250)}",
                "kullanici": k, "port": r.choice([445, 3389, 22, 1433, 8080, 135]), "aksiyon": "deny", "kural": "interzone-default"}

    ham2 = ham_paket("vpn", rng, u_vpn_im, 12, toplam_istek, ham2_dosya, ["2026-04-29", "2026-04-30"], (8, 17))
    incelemeler.append({
        "id": iid, "tur": "kume", "tur_ad": "Grup davranışı", "puan": 91,
        "baslik": "Müşteri İletişim Merkezi", "alt": "9 / 34 kişi, engellenen iç ağ istekleri",
        "ozet": "Grup içinde 9 kişilik alt küme: engellenen ağ sayısı grupta olağanın en az 34 katı, ulaşılan yeni ağ yok.",
        "kart_ozet": "34 kişilik gruptan 9'u yüzlerce iç ağa istek gönderdi, hiçbiri geçmedi",
        "uyarilar": im_uyari, "kaynaklar": ["vpn"], "mitre": ["T1046", "T1018"], "asama": "İç keşif",
        "varliklar": [{"ad": k, "tip": "kisi", "alt": KISI[k]["ad_soyad"]} for k in uyeler],
        "alan": [("Öncelik", "Yüksek"), ("Durum", "Açık"), ("Uyarı", "9"), ("Varlık", "9 kişi"), ("Kim olduğu", "VPN oturumundan"),
                 ("Kaynak", "1, VPN günlükleri"), ("Görülme sıklığı", "34 kişinin 9'unda"), ("Başka açıklama", "Sorulmadı"), ("Yoğun gün", "30 Nis")],
        "nedenler": ["Grupta olağanın en az 34 katı", "Aynı birimde 9 kişi", "Hiçbir istek geçmedi", "Aynı gün yoğunlaşma"],
        "metrikler": [(f"{min(agsay)}-{max(agsay)}", "engellenen ağ"), ("4", "grupta olağan"), ("0", "ulaşılan yeni ağ")],
        "adimlar": [("9 bilgisayarın ortak noktası", "lokasyon, istemci sürümü, VPN profili", "Sistem ekibi"),
                    ("Hedeflerin durumu", "engellenen ağların kaldırılmış aralıklar olup olmadığı", "Ağ ekibi"),
                    ("İstekleri gönderen program", "bu dönemde uç nokta kaydı yok", "Uç nokta koruması sahibi")],
        "eksik": [("İstekleri gönderen program", "Bu dönemde bu 9 bilgisayardan uç nokta kaydı gelmiyor", "Uç nokta koruması sahibi"),
                  ("9 bilgisayarın ortak yapılandırması", "İstemci sürümü, VPN profili ve lokasyon bilgisi", "Sistem ekibi"),
                  ("Engellenen ağların kayıt durumu", "Hedef aralıkların envanter ve topolojide karşılığı", "Ağ ekibi")],
        "lehine": ["kısa sürede çok sayıda iç ağ", "grupta olağanın 34 katı", "port çeşitliliği yüksek"],
        "aleyhine": ["aynı birimde 9 kişi, aynı gün", "hedefler kaldırılmış aralıklar olabilir", "hiçbir istek geçmedi"],
        "kanit": [
            {"baslik": "Kişiler", "kolon": ["Kullanıcı", "Ad", "Unvan", "Engellenen ağ", "Grupta olağan", "Ulaşılan yeni ağ", "Engellenen istek", "Yoğun gün"],
             "sayisal": [3, 4, 5, 6], "satir": im_satir},
            {"baslik": "Grupla kıyas", "kolon": ["Ölçü", "Bu 9 kişi", "Grubun geri kalanı (25 kişi)", "Tüm kullanıcılar"], "sayisal": [1, 2, 3],
             "satir": [["Engellenen ağ, ortanca", str(sorted(agsay)[4]), "4", "4"], ["Engellenen ağ, en yüksek", str(max(agsay)), "9", str(max(agsay))],
                       ["Engellenen istek, toplam", sayi(toplam_istek), "612", sayi(toplam_istek + 612)], ["Ulaşılan yeni ağ", "0", "1", "1"]]}],
        "ham": ham2, "yogun_gun": "2026-04-30",
        "zaman": im_zaman,
        "graf": {"tur": "grup", "kisiler": im_graf, "grup": {"ad": "Müşteri İletişim Merkezi", "uye": 34}}})

    # ==================================================================
    # 3. Uretim servisleri (tema, servis arizasi)
    # ==================================================================
    iid = "uretim-servisleri"
    servisler = [
        ("odeme-gateway.mrd.local", "/actuator/health", 503, 10080), ("kart-limit.mrd.local", "/api/v2/limit/health", 503, 10080),
        ("fx-engine.mrd.local", "/health", 503, 10080), ("swift-entegrasyon.mrd.local", "/api/letter-of-guarantee", 500, 10062),
        ("taleplerim.mrd.local", "/rest/api/latest/serverInfo", 500, 9870), ("apm.mrd.local", "/sitemap.xml", 500, 10080)]
    sv_uyari, sv_satir = [], []
    sv_toplam = sum(s[3] for s in servisler)
    sv_min = min(s[3] for s in servisler if s[3] < 10080)
    sv_503 = sum(s[3] for s in servisler if s[2] == 503)
    sv_500 = sv_toplam - sv_503
    for host, yol, kod, adet in servisler:
        sv_uyari.append(uyari(iid, host, "servis", "Servis arızası", f"Hafta boyu {kod} döndü ({sayi(adet)} istek), alarm üretilmemiş", "citrix",
                              GUNLER[0], 86 if kod == 503 else 84))
        sv_satir.append([host, yol, str(kod), sayi(adet), "7 / 7", "0"])
    sorumlu_sv = [["odeme-gateway.mrd.local", "Ödeme Platformu Ekibi", "Selim Yavuz"], ["kart-limit.mrd.local", "Kart Sistemleri Ekibi", "Aslı Bayram"],
                  ["fx-engine.mrd.local", "Hazine Uygulamaları", "Cem Tunç"], ["swift-entegrasyon.mrd.local", "Uluslararası Operasyonlar BT", "Deniz Erdem"],
                  ["taleplerim.mrd.local", "Kurumsal Uygulamalar", "kayıt yok"], ["apm.mrd.local", "Altyapı İzleme", "kayıt yok"]]

    def u_citrix(r, i):
        s = servisler[i % 6]
        return {"src": f"10.82.239.{14 + i % 5}", "dst": f"10.60.241.{21 + i % 6}", "host": s[0], "yol": s[1], "durum": s[2]}

    ham3 = ham_paket("citrix", rng, u_citrix, 12, sum(s[3] for s in servisler), "uyari_003_uretim_servisleri.csv", GUNLER, (0, 23))
    incelemeler.append({
        "id": iid, "tur": "servis", "tur_ad": "Servis arızası", "puan": 87,
        "baslik": "6 üretim servisi", "alt": "hafta boyu sunucu hatası, alarm üretilmemiş",
        "ozet": f"6 üretim servisi 7 günün 7'sinde sunucu hatası döndürüyor: üçü haftanın her dakikası ({sayi(10080)} istek), diğerleri en az {sayi(sv_min)} istek boyunca. Bu süre boyunca hiçbir alarm oluşmamış.",
        "kart_ozet": "6 üretim servisi hafta boyu 5xx döndürüyor, hiçbirinde alarm yok",
        "uyarilar": sv_uyari, "kaynaklar": ["citrix"], "mitre": [], "asama": "",
        "varliklar": [{"ad": s[0], "tip": "servis", "alt": s[1]} for s in servisler],
        "alan": [("Öncelik", "Yüksek"), ("Durum", "Açık"), ("Uyarı", "6"), ("Varlık", "6 servis"), ("Kim olduğu", "uygulama geçidi kaydı"),
                 ("Kaynak", "1, uygulama geçidi"), ("Görülme sıklığı", "312 servisin 6'sında"), ("Başka açıklama", "Arandı, bulunamadı"), ("Yoğun gün", "Her gün")],
        "nedenler": ["Haftanın her dakikası", "Üretim ortamı", "Sunucu hatası (5xx)", "Alarm üretilmemiş"],
        "metrikler": [(sayi(sv_toplam), "sunucu hatası isteği"), ("7 / 7", "gün"), ("0", "üretilen alarm")],
        "adimlar": [("Servis sahibi ekiplerin bilgilendirilmesi", "6 servis için sorumlu ekip; 2 servisin envanterde sorumlusu yok", "Uygulama sahipleri"),
                    ("İzleme tanımlarının gözden geçirilmesi", "bu servisler için sağlık kontrolü alarmı", "İzleme ekibi"),
                    ("Servislerin kullanım durumu", "hâlâ trafik alan servisler ve çağıran uygulamalar", "Servis sahibi")],
        "eksik": [("Servis sahibi", "taleplerim ve apm servisleri için envanterde sorumlu kaydı", "Envanter yöneticisi"),
                  ("İzleme kapsamı", "6 servis için tanımlı sağlık alarmı olup olmadığı", "İzleme ekibi")],
        "lehine": ["hata kodu 5xx, servis tarafı", "haftanın her dakikası", "alarm yok"], "aleyhine": ["test amaçlı çağrı olabilir", "yük dengeleyici sağlık kontrolü olabilir"],
        "kanit": [
            {"baslik": "Servisler", "kolon": ["Adres", "Yol", "Baskın kod", "İstek", "Gün", "Alarm"], "sayisal": [2, 3, 4, 5], "satir": sv_satir},
            {"baslik": "Cevap kodu dağılımı", "kolon": ["Kod", "Anlamı", "İstek", "Pay"], "sayisal": [2, 3],
             "satir": [["503", "Servis kullanılamıyor", sayi(sv_503), "%" + f"{100 * sv_503 / sv_toplam:.1f}".replace(".", ",")], ["500", "Sunucu iç hatası", sayi(sv_500), "%" + f"{100 * sv_500 / sv_toplam:.1f}".replace(".", ",")]]},
            {"baslik": "Sorumlu ekipler", "kolon": ["Adres", "Ekip", "Sorumlu"], "sayisal": [], "satir": sorumlu_sv}],
        "ham": ham3, "yogun_gun": None,
        "zaman": [{"gun": g, "saat": "", "baslik": "Sunucu hatası sürüyor", "ayrinti": "6 serviste kesintisiz 5xx; alarm yok", "kaynak": "citrix", "ton": "uyari" if i in (0, 6) else "bilgi"}
                  for i, g in enumerate(GUNLER)],
        "graf": None})

    # ==================================================================
    # 4. Yonetici hesabi istasyon sicramasi
    # ==================================================================
    iid = "yonetici-istasyon"
    ts_yet = paylastir(214, [25, 28, 27, 92, 42, 0, 0])
    ag4 = ag_listesi(rng, normal=["10.60.89.0/24", "10.60.9.0/24"], yalniz=["10.60.67.0/24", "10.71.24.0/24"], engel=["10.93.191.0/24"],
                     istek_araligi=(20, 220), gunler=GUNLER[2:5])
    for x in ag4:
        if x["sinif"] == "yalniz":
            x["gun"] = "2026-04-30"
    y1 = uyari(iid, tsahin, "kisi", "Yönetici yetkisi hareketi", "Yönetici hesabı taban haftada 2 istasyondan doğruladı, 30 Nisan'da 6 istasyondan", "dc", "2026-04-30", 85, ["T1078.002", "T1021"])
    y2 = uyari(iid, tsahin, "kisi", "Yeni iç ağa gidiş", "Aynı gün 2 yeni iç ağa ulaştı: felaket merkezi ve tanımsız yönetim bloğu", "fw", "2026-04-30", 83, ["T1021"])

    def u_dc_ts(r, i):
        return {"kullanici": "tsahin", "istasyon": r.choice(["MRDNB0211", "MRDSRV0141", "MRDSRV0142", "MRDNB0774", "MRDNB0312", "MRDSRV0208"]),
                "src": f"10.160.127.{20 + i}", "kod": "4672" if i % 3 == 0 else "4624", "tip": 3 if i % 2 else 10,
                "metin": "Special privileges assigned to new logon." if i % 3 == 0 else "An account was successfully logged on."}

    ham4 = ham_paket("dc", rng, u_dc_ts, 12, 214, "uyari_004_tsahin.csv", ["2026-04-30", "2026-05-01"], (8, 18))
    incelemeler.append({
        "id": iid, "tur": "yonetici", "tur_ad": "Yönetici yetkisi", "puan": 85,
        "baslik": "Tolga Şahin", "alt": "Sistem Yöneticisi, istasyon sıçraması ve yeni iç ağlar",
        "ozet": "Yönetici hesabı taban haftada 2 istasyondan doğruladı, 30 Nisan'da 6 istasyondan doğruladı; aynı gün 2 yeni iç ağa ulaştı.",
        "kart_ozet": "Yönetici hesabı 2 yerine 6 istasyondan doğruladı, aynı gün 2 yeni iç ağa ulaştı",
        "uyarilar": [y1, y2], "kaynaklar": ["dc", "fw"], "mitre": ["T1078.002", "T1021"], "asama": "Yanal hareket",
        "varliklar": [{"ad": "tsahin", "tip": "kisi", "alt": "Tolga Şahin, Altyapı ve Sistem Yönetimi"}],
        "alan": [("Öncelik", "Yüksek"), ("Durum", "Açık"), ("Uyarı", "2"), ("Varlık", "1 kişi"), ("Kim olduğu", "dizin hesabı"),
                 ("Kaynak", "2, etki alanı, güvenlik duvarı"), ("Görülme sıklığı", "12 yönetici hesabın 1'inde"), ("Başka açıklama", "Sorulmadı"), ("Yoğun gün", "30 Nis")],
        "nedenler": ["Yönetici yetkili hesap", "Doğrulanan istasyon 3 katına çıktı", "2 yeni iç ağ", "2 kaynak doğruladı"],
        "metrikler": [("6", "istasyon, taban 2"), ("2", "yeni iç ağ"), ("214", "yetkili oturum")],
        "adimlar": [("Değişiklik ve bakım kayıtları", "30 Nis için planlı bakım ya da değişiklik talebi", "Değişiklik yönetimi"),
                    ("Yeni istasyonların kullanım amacı", "MRDSRV0141, MRDSRV0142, MRDSRV0208", "Sistem ekibi")],
        "eksik": [("Bakım penceresi kaydı", "30 Nis için değişiklik ve bakım talepleri", "Değişiklik yönetimi"),
                  ("Yeni ağların envanter kaydı", "10.60.67.0/24 için envanter ve topoloji karşılığı", "Ağ ekibi")],
        "lehine": ["taban haftaya göre 3 kat istasyon", "yeni iç ağlara ulaşım", "yönetici yetkisi"], "aleyhine": ["planlı bakım olabilir", "yeni sunucu kurulumu olabilir"],
        "kanit": [
            {"baslik": "İstasyonlar", "kolon": ["İstasyon", "Tür", "İlk görülme", "Yetkili oturum"], "sayisal": [3],
             "satir": [["MRDNB0211", "Dizüstü", "Taban", "44"], ["MRDNB0312", "Dizüstü", "Taban", "31"], ["MRDSRV0141", "Sunucu", "30 Nis", "52"],
                       ["MRDSRV0142", "Sunucu", "30 Nis", "36"], ["MRDNB0774", "Dizüstü", "30 Nis", "29"], ["MRDSRV0208", "Sunucu", "30 Nis", "22"]]},
            {"baslik": "Ulaşılan ağlar", "kolon": ["Ağ", "Ağ tanımı", "İstek", "Geçen", "İlk görülme"], "sayisal": [2, 3],
             "satir": [[x["cidr"], x["ad"] or "kayıtlarda tanımlı değil", sayi(x["istek"]), sayi(x["gecen"]), gun_et(x["gun"])] for x in ag4 if x["sinif"] != "engel"]}],
        "ham": ham4, "yogun_gun": "2026-04-30",
        "zaman": [
            {"gun": "2026-04-27", "saat": "", "baslik": "Taban haftası", "ayrinti": f"2 istasyondan doğrulama, günde {ts_yet[0]} ile {ts_yet[2]} yetkili oturum", "kaynak": "dc", "ton": "bilgi"},
            {"gun": "2026-04-30", "saat": "08:40", "baslik": "4 yeni istasyondan ilk doğrulama", "ayrinti": "Hesap 6 istasyondan doğruladı", "kaynak": "dc", "ton": "uyari"},
            {"gun": "2026-04-30", "saat": "11:15", "baslik": "2 yeni iç ağa ulaşım", "ayrinti": "10.60.67.0/24 ve 10.71.24.0/24, izinli", "kaynak": "fw", "ton": "kritik"},
            {"gun": "2026-05-01", "saat": "", "baslik": "İstasyon sayısı taban düzeyine döndü", "ayrinti": "2 istasyon", "kaynak": "dc", "ton": "bilgi"}],
        "graf": {"tur": "kisi", "kisiler": [{"ad": "tsahin", "ad_soyad": "Tolga Şahin", "alt": "Altyapı ve Sistem Yönetimi", "ag": ag4, "ozet": ag_ozet(ag4)}],
                 "grup": {"ad": "Altyapı ve Sistem Yönetimi", "uye": 12}}})

    # ==================================================================
    # ORTA
    # ==================================================================
    # 5. Ag taramasi (bilgisayar)
    iid = "ag-taramasi"
    a1 = uyari(iid, "MRDNB0912", "bilgisayar", "Ağ taraması", "3 saatte 214 iç ağa, 37 farklı porta istek (%96 reddedildi)", "fw", "2026-05-03", 78, ["T1046", "T1018"])

    def u_fw_tarama(r, i):
        return {"src": "10.160.164.88", "dst": f"10.{r.choice([93, 60, 71])}.{r.randint(100, 230)}.{r.randint(2, 250)}", "port": r.choice([22, 23, 80, 135, 139, 443, 445, 1433, 3306, 3389, 5985, 8080]),
                "kural": "interzone-default", "ad_soyad": "bilinmiyor", "kullanici": "MRDNB0912", "istasyon": "MRDNB0912"}

    ham5 = ham_paket("fw", rng, u_fw_tarama, 12, 9_412, "uyari_005_mrdnb0912.csv", ["2026-05-03"], (9, 11))
    incelemeler.append({
        "id": iid, "tur": "tarama", "tur_ad": "Ağ taraması", "puan": 78,
        "baslik": "MRDNB0912", "alt": "bilgisayar, kişi çözümlenemedi",
        "ozet": "Bir bilgisayar 3 saatte 214 iç ağa ve 37 farklı porta istek gönderdi; isteklerin %96'sı reddedildi.",
        "kart_ozet": "3 saatte 214 iç ağ ve 37 port; benzer bilgisayarlarda olağan 6 ağ",
        "uyarilar": [a1], "kaynaklar": ["fw"], "mitre": ["T1046", "T1018"], "asama": "İç keşif",
        "varliklar": [{"ad": "MRDNB0912", "tip": "bilgisayar", "alt": "kişi çözümlenemedi"}],
        "alan": [("Öncelik", "Orta"), ("Durum", "Açık"), ("Uyarı", "1"), ("Varlık", "1 bilgisayar"), ("Kim olduğu", "çözümlenemedi"),
                 ("Kaynak", "1, iç güvenlik duvarı"), ("Görülme sıklığı", "1.106 bilgisayarın 1'inde"), ("Başka açıklama", "Arandı, bulunamadı"), ("Yoğun gün", "3 May")],
        "nedenler": ["Kısa sürede çok hedef", "37 farklı port", "Benzerlerinde olağan 6 ağ"],
        "metrikler": [("214", "3 saatte taranan ağ"), ("6", "benzerlerinde olağan"), ("37", "farklı port")],
        "adimlar": [("Bilgisayarın kullanıcısı", "MRDNB0912 zimmet kaydı", "Sistem ekibi"), ("İstekleri gönderen program", "uç nokta kaydı", "Uç nokta koruması sahibi")],
        "eksik": [("Bilgisayarın kullanıcısı", "Bilgisayar için oturum kaydı ve zimmet bilgisi", "Sistem ekibi"),
                  ("İstekleri gönderen program", "Aynı saatlerde bilgisayarda çalışan süreç kaydı", "Uç nokta koruması sahibi")],
        "lehine": ["kısa sürede çok hedef", "port çeşitliliği yüksek"], "aleyhine": ["yetkili zafiyet taraması olabilir"],
        "kanit": [{"baslik": "Tarama özeti", "kolon": ["Ölçü", "Bu bilgisayar", "Benzer bilgisayarlarda ortanca", "Tüm bilgisayarlar, ortanca"], "sayisal": [1, 2, 3],
                   "satir": [["Farklı hedef ağ", "214", "6", "4"], ["Farklı port", "37", "3", "3"], ["Reddedilen pay", "%96", "%12", "%9"], ["Süre", "3 saat", "-", "-"]]}],
        "ham": ham5, "yogun_gun": "2026-05-03",
        "zaman": [{"gun": "2026-05-03", "saat": "09:02", "baslik": "Tarama başladı", "ayrinti": "10.160.164.88 adresinden; ilk 30 dakikada 71 ağ", "kaynak": "fw", "ton": "uyari"},
                  {"gun": "2026-05-03", "saat": "11:58", "baslik": "Tarama sona erdi", "ayrinti": "Toplam 9.412 bağlantı denemesi, 214 ağ", "kaynak": "fw", "ton": "kritik"}],
        "graf": None})

    # 6. EDR saldiri araci
    iid = "saldiri-araci"
    e1 = uyari(iid, "ugunes", "kisi", "Uç noktada saldırı aracı", "İndirilenler klasöründe saldırı aracı arşivi tespit edildi: impacket-master.zip", "edr", "2026-04-29", 82, ["T1105"])

    def u_edr(r, i):
        return {"olay": "Suspicious File Detected", "makine": "MRDNB0207", "kullanici": "ugunes", "dosya": "impacket-master.zip",
                "yol": "C:\\Users\\ugunes\\Downloads", "aksiyon": "Deny", "kategori": "Known Attack Tool"}

    ham6 = ham_paket("edr", rng, u_edr, 1, 1, "uyari_006_ugunes.csv", ["2026-04-29"], (14, 14))
    incelemeler.append({
        "id": iid, "tur": "arac", "tur_ad": "Uç nokta", "puan": 82,
        "baslik": "Umut Güneş", "alt": "MRDNB0207, uç noktada saldırı aracı",
        "ozet": "Bir bilgisayarın İndirilenler klasöründe bilinen saldırı aracı arşivi tespit edildi ve engellendi.",
        "kart_ozet": "impacket-master.zip, uç nokta koruması engelledi",
        "uyarilar": [e1], "kaynaklar": ["edr"], "mitre": ["T1105"], "asama": "Komuta ve kontrol",
        "varliklar": [{"ad": "ugunes", "tip": "kisi", "alt": "Umut Güneş, Bilgi Güvenliği"}, {"ad": "MRDNB0207", "tip": "bilgisayar", "alt": "dizüstü"}],
        "alan": [("Öncelik", "Orta"), ("Durum", "Açık"), ("Uyarı", "1"), ("Varlık", "1 kişi, 1 bilgisayar"), ("Kim olduğu", "uç nokta kaydı"),
                 ("Kaynak", "1, uç nokta koruması"), ("Görülme sıklığı", "1 bilgisayar"), ("Başka açıklama", "Sorulmadı"), ("Yoğun gün", "29 Nis")],
        "nedenler": ["Bilinen saldırı aracı", "Engellendi", "Tek kaynak"],
        "metrikler": [("1", "tespit"), ("Engellendi", "uç nokta aksiyonu"), ("1", "kaynak")],
        "adimlar": [("Aracın kullanım amacı", "Bilgi Güvenliği ekibinin test görevi kaydı", "Bilgi Güvenliği")],
        "eksik": [("Aracın kullanım amacı", "Kullanıcının rolü ve görev kaydı", "Bilgi Güvenliği")],
        "lehine": ["bilinen saldırı aracı adı"], "aleyhine": ["kullanıcı güvenlik uzmanı, test amaçlı olabilir"],
        "kanit": [{"baslik": "Uç nokta olayı", "kolon": ["Gün", "Bilgisayar", "Dosya", "Konum", "Aksiyon"], "sayisal": [],
                   "satir": [["29 Nis 14:22", "MRDNB0207", "impacket-master.zip", "C:\\Users\\ugunes\\Downloads", "Engellendi"]]}],
        "ham": ham6, "yogun_gun": "2026-04-29",
        "zaman": [{"gun": "2026-04-29", "saat": "14:22", "baslik": "Arşiv indirildi ve tespit edildi", "ayrinti": "Uç nokta koruması dosyayı engelledi", "kaynak": "edr", "ton": "uyari"}],
        "graf": None})

    # 7. Dijital Kanallar (kume)
    iid = "dijital-kanallar"
    dk_uyeler = dk_kisileri[:7]
    dk_say = [19, 17, 14, 11, 9, 6, 4]
    dk_uyari, dk_graf, dk_satir = [], [], []
    dk_top = 0
    dk_gun = {}
    for sira, (k, n) in enumerate(zip(dk_uyeler, dk_say)):
        ag = ag_listesi(rng, normal=["10.60.241.0/24", "10.60.22.0/24"], rastgele_engel=n - 1, grup_engel=1, istek_araligi=(4, 40), gunler=GUNLER[2:5])
        istek = sum(x["istek"] for x in ag if x["sinif"] in ("engel", "grup_engel"))
        ge = sum(x["istek"] for x in ag if x["sinif"] == "grup_engel")
        normal_istek = sum(x["istek"] for x in ag if x["sinif"] == "normal")
        agirlik = [0, 0, 15, 60, 20, 5, 0] if sira < 5 else [0, 0, 5, 25, 55, 15, 0]
        engel_gun = paylastir(istek, agirlik)
        gun = en_yogun(engel_gun)
        dk_top += istek
        dk_uyari.append(uyari(iid, k, "kisi", "Grup davranışı", f"{n} iç ağa istek gönderdi, hiçbiri geçmedi (grupta olağan 1)", "vpn", gun, 74, ["T1046", "T1018"]))
        dk_gun[k] = {"istek": paylastir(istek + normal_istek, agirlik), "engel": engel_gun}
        dk_graf.append({"ad": k, "ad_soyad": KISI[k]["ad_soyad"], "alt": KISI[k]["unvan"], "ag": ag, "ozet": ag_ozet(ag), "engel_istek": istek - ge})
        dk_satir.append([k, KISI[k]["ad_soyad"], KISI[k]["unvan"], str(n), "1", "0", sayi(istek), gun_et(gun)])
    dk_top_gun = [sum(dk_gun[k]["engel"][i] for k in dk_uyeler) for i in range(7)]
    dk_zaman = [
        {"gun": GUNLER[2], "saat": "", "baslik": "İlk engellenen istekler", "ayrinti": f"7 kişiden toplam {sayi(dk_top_gun[2])} engellenen istek", "kaynak": "vpn", "ton": "bilgi"},
        {"gun": GUNLER[3], "saat": "", "baslik": "En yoğun gün", "ayrinti": f"{sayi(dk_top_gun[3])} engellenen istek, 5 kişi için en yoğun gün", "kaynak": "vpn", "ton": "uyari"},
        {"gun": GUNLER[4], "saat": "", "baslik": "Kalan 2 kişi için en yoğun gün", "ayrinti": f"{sayi(dk_top_gun[4])} engellenen istek", "kaynak": "vpn", "ton": "uyari"}]

    def u_vpn_dk(r, i):
        k = dk_uyeler[i % 7]
        return {"src": f"10.249.{[90, 127][i % 2]}.{40 + i}", "dst": f"10.{r.choice([137, 124, 212, 206])}.{r.randint(1, 254)}.{r.randint(2, 250)}", "kullanici": k,
                "port": r.choice([443, 8443, 8080, 22]), "aksiyon": "deny", "kural": "interzone-default"}

    ham7 = ham_paket("vpn", rng, u_vpn_dk, 12, dk_top, "uyari_007_dijital_kanallar.csv", ["2026-04-30", "2026-05-01"], (9, 18))
    incelemeler.append({
        "id": iid, "tur": "kume", "tur_ad": "Grup davranışı", "puan": 74,
        "baslik": "Dijital Kanallar", "alt": "7 / 27 kişi, engellenen iç ağ istekleri",
        "ozet": "Grup içinde 7 kişilik alt küme: engellenen ağ sayısı 4 ile 19 arasında, grupta olağan 1; ulaşılan ağ yok.",
        "kart_ozet": "27 kişilik gruptan 7'si 4 ile 19 arasında iç ağa istek gönderdi, hiçbiri geçmedi",
        "uyarilar": dk_uyari, "kaynaklar": ["vpn"], "mitre": ["T1046", "T1018"], "asama": "İç keşif",
        "varliklar": [{"ad": k, "tip": "kisi", "alt": KISI[k]["ad_soyad"]} for k in dk_uyeler],
        "alan": [("Öncelik", "Orta"), ("Durum", "Açık"), ("Uyarı", "7"), ("Varlık", "7 kişi"), ("Kim olduğu", "VPN oturumundan"),
                 ("Kaynak", "1, VPN günlükleri"), ("Görülme sıklığı", "27 kişinin 7'sinde"), ("Başka açıklama", "Sorulmadı"), ("Yoğun gün", "30 Nis")],
        "nedenler": ["Grupta olağanın 4 ile 19 katı", "Aynı birimde 7 kişi", "Hiçbir istek geçmedi"],
        "metrikler": [("4-19", "engellenen ağ"), ("1", "grupta olağan"), ("0", "ulaşılan yeni ağ")],
        "adimlar": [("7 bilgisayarın ortak noktası", "test ortamı erişimi, istemci sürümü", "Sistem ekibi"), ("Hedeflerin durumu", "kaldırılmış test aralıkları", "Ağ ekibi")],
        "eksik": [("İstekleri gönderen program", "Bu dönemde uç nokta kaydı yok", "Uç nokta koruması sahibi"), ("Test ortamı aralıkları", "Hedef ağların envanter kaydı", "Ağ ekibi")],
        "lehine": ["grupta olağanın üzerinde", "birden çok kişide aynı desen"], "aleyhine": ["test ortamları kaldırılmış olabilir", "hiçbir istek geçmedi"],
        "kanit": [{"baslik": "Kişiler", "kolon": ["Kullanıcı", "Ad", "Unvan", "Engellenen ağ", "Grupta olağan", "Ulaşılan yeni ağ", "Engellenen istek", "Yoğun gün"], "sayisal": [3, 4, 5, 6], "satir": dk_satir}],
        "ham": ham7, "yogun_gun": "2026-04-30",
        "zaman": dk_zaman,
        "graf": {"tur": "grup", "kisiler": dk_graf, "grup": {"ad": "Dijital Kanallar", "uye": 27}}})

    # 8. Dis tarama (iki blok)
    iid = "dis-tarama"
    w1 = uyari(iid, "203.0.113.0/24", "adres", "Dış web taraması", "35 adres 6 gündür web uygulamalarına saldırı imzası gönderiyor", "citrix", "2026-05-01", 66, ["T1595", "T1190"])
    w2 = uyari(iid, "198.51.100.0/24", "adres", "Dış web taraması", "22 adres 4 gündür aynı hedeflere imzalı istek gönderiyor", "citrix", "2026-04-30", 62, ["T1595", "T1190"])

    def u_waf(r, i):
        blok = "203.0.113" if i % 3 else "198.51.100"
        return {"src": f"{blok}.{r.randint(2, 250)}", "imza": r.choice(["APPFW_SQL", "APPFW_XSS", "APPFW_FIELDCONSISTENCY", "APPFW_SIGNATURE_MATCH"]),
                "aciklama": "Signature violation", "url": r.choice(["http://kampanya.mrd.local/giris.aspx", "http://mrd-web.mrd.local/api/arama", "http://sube.mrd.local/login"]),
                "sonuc": r.choice(["blocked", "blocked", "not blocked"])}

    ham8 = ham_paket("waf", rng, u_waf, 12, 4_226, "uyari_008_dis_tarama.csv", GUNLER[2:], (0, 23))
    incelemeler.append({
        "id": iid, "tur": "dis_tarama", "tur_ad": "Dış tarama", "puan": 66,
        "baslik": "2 dış adres bloğu", "alt": "web uygulamalarına saldırı imzası gönderiyor",
        "ozet": "İnternetten iki adres bloğu, birden çok gündür web uygulamalarına saldırı imzalı istek gönderiyor; isteklerin %71'i engellendi.",
        "kart_ozet": "57 dış adres, 4.226 imzalı istek; %71'i uygulama geçidinde engellendi",
        "uyarilar": [w1, w2], "kaynaklar": ["citrix"], "mitre": ["T1595", "T1190"], "asama": "Keşif",
        "varliklar": [{"ad": "203.0.113.0/24", "tip": "adres", "alt": "35 adres"}, {"ad": "198.51.100.0/24", "tip": "adres", "alt": "22 adres"}],
        "alan": [("Öncelik", "Orta"), ("Durum", "Açık"), ("Uyarı", "2"), ("Varlık", "2 dış adres bloğu"), ("Kim olduğu", "kaynak adres"),
                 ("Kaynak", "1, uygulama geçidi"), ("Görülme sıklığı", "9.812 dış bloğun 3'ünde"), ("Başka açıklama", "Sorulmadı"), ("Yoğun gün", "1 May")],
        "nedenler": ["Birden çok gün", "Birden çok imza sınıfı", "Aynı hedeflere yoğunlaşma"],
        "metrikler": [("57", "dış adres"), ("4.226", "imzalı istek"), ("%71", "engellenen")],
        "adimlar": [("Denetimli test kaydı", "bu bloklar için yetkili test ya da tarama kaydı", "Bilgi Güvenliği")],
        "eksik": [("Bloğun sahibi", "Adres bloklarının kime ait olduğu ve yetkili test kaydı", "Bilgi Güvenliği")],
        "lehine": ["birden çok imza sınıfı", "birden çok gün"], "aleyhine": ["denetimli sızma testi olabilir", "izleme hizmeti olabilir"],
        "kanit": [{"baslik": "Bloklar", "kolon": ["Blok", "Adres", "İmzalı istek", "İmza sınıfı", "Engellenen pay", "Gün"], "sayisal": [1, 2, 3, 4, 5],
                   "satir": [["203.0.113.0/24", "35", "2.611", "4", "%74", "6"], ["198.51.100.0/24", "22", "1.615", "3", "%66", "4"]]},
                  {"baslik": "Hedef uygulamalar", "kolon": ["Uygulama adresi", "İstek", "Pay"], "sayisal": [1, 2],
                   "satir": [["kampanya.mrd.local", "1.911", "%45,2"], ["sube.mrd.local", "1.402", "%33,2"], ["mrd-web.mrd.local", "913", "%21,6"]]}],
        "ham": ham8, "yogun_gun": "2026-05-01",
        "zaman": [{"gun": "2026-04-28", "saat": "", "baslik": "203.0.113.0/24 ilk imza", "ayrinti": "3 adres", "kaynak": "citrix", "ton": "bilgi"},
                  {"gun": "2026-05-01", "saat": "", "baslik": "Yoğun gün", "ayrinti": "1.012 imzalı istek, 41 adres", "kaynak": "citrix", "ton": "uyari"},
                  {"gun": "2026-04-30", "saat": "", "baslik": "198.51.100.0/24 ilk imza", "ayrinti": "22 adres", "kaynak": "citrix", "ton": "uyari"}],
        "graf": None})

    # 9. ecetin yeni ic ag
    iid = "yeni-ag-ecetin"
    ag9 = ag_listesi(rng, normal=["10.160.127.0/24"], yalniz=["10.93.191.0/24"], engel=["10.60.89.0/24"], rastgele_engel=1, istek_araligi=(10, 90), gunler=GUNLER[2:5])
    ec_yeni = sum(x["istek"] for x in ag9 if x["sinif"] != "normal")
    ec_engel = sum(x["istek"] for x in ag9 if x["sinif"] == "engel")
    e9 = uyari(iid, ecetin, "kisi", "Yeni iç ağa gidiş", "3 yeni iç ağ, 1'ine ulaştı, 2'sine istek engellendi", "vpn", "2026-05-02", 61, ["T1018"])
    ham9 = ham_paket("vpn", rng, lambda r, i: {"src": "10.249.16.55", "dst": r.choice(["10.93.191.21", "10.60.89.9", "10.214.149.4"]), "kullanici": "ecetin",
                                               "port": r.choice([443, 8443, 3389]), "aksiyon": "allow" if i % 3 == 0 else "deny"}, 12, ec_yeni,
                     "uyari_009_ecetin.csv", GUNLER[4:6], (9, 18))
    incelemeler.append({
        "id": iid, "tur": "kisi", "tur_ad": "Yeni iç ağ", "puan": 61,
        "baslik": "Elif Çetin", "alt": "Mali İşler, yeni iç ağa gidiş",
        "ozet": "Hesap dönemde ilk kez 3 iç ağa istek gönderdi; 1'ine ulaşıldı, 2'sinde istek engellendi.",
        "kart_ozet": "3 yeni iç ağ: 1 ulaşıldı, 2 engellendi",
        "uyarilar": [e9], "kaynaklar": ["vpn"], "mitre": ["T1018"], "asama": "İç keşif",
        "varliklar": [{"ad": "ecetin", "tip": "kisi", "alt": "Elif Çetin, Mali İşler"}],
        "alan": [("Öncelik", "Orta"), ("Durum", "Açık"), ("Uyarı", "1"), ("Varlık", "1 kişi"), ("Kim olduğu", "VPN oturumundan"), ("Kaynak", "1, VPN günlükleri"),
                 ("Görülme sıklığı", "498 kullanıcının 21'inde"), ("Başka açıklama", "Sorulmadı"), ("Yoğun gün", "2 May")],
        "nedenler": ["3 yeni iç ağ", "Kendi birimine göre alışılmadık"], "metrikler": [("3", "yeni iç ağ"), ("1", "ulaşıldı"), ("2", "engellendi")],
        "adimlar": [("Ağ erişim talebi", "10.93.191.0/24 için açık erişim talebi", "Ağ ekibi")],
        "eksik": [("Erişim talebi", "10.93.191.0/24 için erişim talebi ya da görev kaydı", "Ağ ekibi")],
        "lehine": ["dönemde ilk kez gidilen ağlar"], "aleyhine": ["yeni görev ya da proje olabilir", "nüfusun %4'ünde görülen bir davranış"],
        "kanit": [{"baslik": "Ağlar", "kolon": ["Ağ", "Ağ tanımı", "Sonuç", "İstek", "İlk görülme"], "sayisal": [3],
                   "satir": [[x["cidr"], x["ad"] or "kayıtlarda tanımlı değil", "Ulaşıldı" if x["gecen"] else "Engellendi", sayi(x["istek"]), gun_et(x["gun"])] for x in ag9 if x["sinif"] != "normal"]}],
        "ham": ham9, "yogun_gun": "2026-05-02",
        "zaman": [{"gun": "2026-05-02", "saat": "10:14", "baslik": "Yeni iç ağlara ilk istek", "ayrinti": "10.93.191.0/24 ulaşıldı; 2 ağ engellendi", "kaynak": "vpn", "ton": "uyari"}],
        "graf": {"tur": "kisi", "kisiler": [{"ad": "ecetin", "ad_soyad": "Elif Çetin", "alt": "Mali İşler", "ag": ag9, "ozet": ag_ozet(ag9)}], "grup": {"ad": "Mali İşler", "uye": 18}}})

    # 10. mdemir surekli engel
    iid = "surekli-engel-mdemir"
    ag10 = ag_listesi(rng, normal=["10.160.127.0/24"], engel=["10.93.191.0/24"], istek_araligi=(80, 260), gunler=GUNLER[1:5])
    for x in ag10:
        if x["sinif"] == "engel":
            x["istek"] = 152
    e10 = uyari(iid, mdemir, "kisi", "Sürekli engellenen istek", "4 gündür aynı iç ağa engelleniyor, günde ortalama 38 reddedilen istek", "vpn", "2026-05-02", 72, ["T1046"])
    ham10 = ham_paket("vpn", rng, lambda r, i: {"src": "10.249.53.77", "dst": f"10.93.191.{r.randint(10, 60)}", "kullanici": "mdemir", "port": r.choice([1521, 1433, 8080]),
                                                "aksiyon": "deny"}, 12, 152, "uyari_010_mdemir.csv", GUNLER[2:6], (8, 18))
    incelemeler.append({
        "id": iid, "tur": "kisi", "tur_ad": "Sürekli engelleme", "puan": 72,
        "baslik": "Mert Demir", "alt": "Kredi Operasyonları, sürekli engellenen istek",
        "ozet": "Hesap 4 gündür aynı iç ağa istek gönderiyor ve her seferinde engelleniyor; hiçbir istek geçmedi.",
        "kart_ozet": "4 gündür aynı iç ağa istek, günde ortalama 38 ret",
        "uyarilar": [e10], "kaynaklar": ["vpn"], "mitre": ["T1046"], "asama": "İç keşif",
        "varliklar": [{"ad": "mdemir", "tip": "kisi", "alt": "Mert Demir, Kredi Operasyonları"}],
        "alan": [("Öncelik", "Orta"), ("Durum", "Açık"), ("Uyarı", "1"), ("Varlık", "1 kişi"), ("Kim olduğu", "VPN oturumundan"), ("Kaynak", "1, VPN günlükleri"),
                 ("Görülme sıklığı", "498 kullanıcının 12'sinde"), ("Başka açıklama", "Arandı, bulunamadı"), ("Yoğun gün", "30 Nis")],
        "nedenler": ["4 gün süreklilik", "Aynı ağa tekrarlayan ret"], "metrikler": [("152", "reddedilen istek"), ("4", "gün"), ("0", "geçen istek")],
        "adimlar": [("Hedef ağın durumu", "10.93.191.0/24 için kullanıcının erişim beklentisi", "Ağ ekibi")],
        "eksik": [("Erişim beklentisi", "Kullanıcının bu ağa erişmesi gereken bir görev olup olmadığı", "Kredi Operasyonları yöneticisi")],
        "lehine": ["tekrarlayan ret"], "aleyhine": ["yapılandırma hatası olabilir", "kaldırılmış bir kaynağa ayarlanmış istemci olabilir"],
        "kanit": [{"baslik": "Günlük dağılım", "kolon": ["Gün", "İstek", "Reddedilen", "Geçen"], "sayisal": [1, 2, 3],
                   "satir": [["29 Nis", "36", "36", "0"], ["30 Nis", "41", "41", "0"], ["1 May", "39", "39", "0"], ["2 May", "36", "36", "0"]]}],
        "ham": ham10, "yogun_gun": "2026-04-30",
        "zaman": [{"gun": g, "saat": "", "baslik": "Aynı ağa reddedilen istekler", "ayrinti": "10.93.191.0/24", "kaynak": "vpn", "ton": "bilgi"} for g in GUNLER[2:6]],
        "graf": {"tur": "kisi", "kisiler": [{"ad": "mdemir", "ad_soyad": "Mert Demir", "alt": "Kredi Operasyonları", "ag": ag10, "ozet": ag_ozet(ag10)}],
                 "grup": {"ad": "Kredi Operasyonları", "uye": 41}}})

    # ==================================================================
    # DUSUK
    # ==================================================================
    def kucuk(iid, tur, tur_ad, puan, baslik, alt, ozet, kart_ozet, ulist, kaynaklar, mitre, varliklar, alan, metrikler, adimlar, eksik, kanit, ham, yogun, zaman):
        incelemeler.append({
            "id": iid, "tur": tur, "tur_ad": tur_ad, "puan": puan, "baslik": baslik, "alt": alt, "ozet": ozet, "kart_ozet": kart_ozet, "uyarilar": ulist,
            "kaynaklar": kaynaklar, "mitre": mitre, "asama": MITRE[mitre[0]][1] if mitre else "", "varliklar": varliklar, "alan": alan,
            "nedenler": [], "metrikler": metrikler, "adimlar": adimlar, "eksik": eksik, "lehine": [], "aleyhine": [], "kanit": kanit,
            "ham": ham, "yogun_gun": yogun, "zaman": zaman, "graf": None})

    # 11. olu adres
    iid = "olu-adres"
    o1 = uyari(iid, "kampanya-eski.mrd.local", "servis", "Ölü adres çağrısı", "Adres artık yok (404) ama hâlâ çağrılıyor: 11.482 istek", "citrix", "2026-04-27", 52)
    o2 = uyari(iid, "eposta-onay.mrd.local", "servis", "Ölü adres çağrısı", "Adres artık yok (404) ama hâlâ çağrılıyor: 6.204 istek", "citrix", "2026-04-27", 50)
    ham11 = ham_paket("citrix", rng, lambda r, i: {"src": f"10.82.239.{30 + i % 4}", "dst": "10.60.241.21", "host": "kampanya-eski.mrd.local" if i % 2 else "eposta-onay.mrd.local",
                                                  "yol": "/v1/ilan/liste" if i % 2 else "/onay/tetikle", "durum": 404}, 12, 17686, "uyari_011_olu_adres.csv", GUNLER, (0, 23))
    kucuk(iid, "olu", "Ölü adres", 52, "2 adres artık yok", "hâlâ çağrılmaya devam ediyor",
          "İki uygulama adresi 404 döndürüyor ama istekler kesilmemiş; çağıran uygulama ayarı güncellenmemiş olabilir.", "2 adres 404 döndürüyor, çağrılar sürüyor",
          [o1, o2], ["citrix"], [], [{"ad": "kampanya-eski.mrd.local", "tip": "servis", "alt": "/v1/ilan/liste"}, {"ad": "eposta-onay.mrd.local", "tip": "servis", "alt": "/onay/tetikle"}],
          [("Öncelik", "Düşük"), ("Durum", "Açık"), ("Uyarı", "2"), ("Varlık", "2 servis"), ("Kim olduğu", "uygulama geçidi kaydı"), ("Kaynak", "1, uygulama geçidi"),
           ("Görülme sıklığı", "312 servisin 2'sinde"), ("Başka açıklama", "Arandı, bulunamadı"), ("Yoğun gün", "Her gün")],
          [("17.686", "istek"), ("404", "baskın kod"), ("2", "servis")],
          [("Çağıran uygulama", "hangi uygulama bu adresleri çağırıyor", "Uygulama sahipleri")],
          [("Çağıran uygulama", "Bu adreslere istek gönderen uygulamanın kaydı", "Uygulama sahipleri")],
          [{"baslik": "Adresler", "kolon": ["Adres", "Yol", "Kod", "İstek"], "sayisal": [3], "satir": [["kampanya-eski.mrd.local", "/v1/ilan/liste", "404", "11.482"], ["eposta-onay.mrd.local", "/onay/tetikle", "404", "6.204"]]}],
          ham11, None, [{"gun": GUNLER[i], "saat": "", "baslik": "İstekler sürüyor", "ayrinti": "404 yanıtları", "kaynak": "citrix", "ton": "bilgi"} for i in (0, 3, 6)])

    # 12. yoklama
    iid = "yoklama"
    y_a = uyari(iid, "boaidentity.mrd.local", "servis", "Yoklama hatası", "Kök yola dakikada bir istek, sürekli 404", "citrix", "2026-04-27", 48)
    y_b = uyari(iid, "satinalma.mrd.local", "servis", "Yoklama hatası", "Kök yola dakikada bir istek, sürekli 400", "citrix", "2026-04-27", 47)
    y_c = uyari(iid, "toplu-islem.mrd.local", "servis", "Yoklama hatası", "Kök yola dakikada bir istek, sürekli 404", "citrix", "2026-04-27", 46)
    ham12 = ham_paket("citrix", rng, lambda r, i: {"src": "10.82.97.11", "dst": "10.60.241.24", "host": ["boaidentity.mrd.local", "satinalma.mrd.local", "toplu-islem.mrd.local"][i % 3],
                                                  "yol": "/", "durum": 400 if i % 3 == 1 else 404}, 12, 30240, "uyari_012_yoklama.csv", GUNLER, (0, 23))
    kucuk(iid, "yoklama", "Yoklama hatası", 48, "3 yoklama yanlış adrese gidiyor", "dakikada bir kök yol, sürekli hata",
          "Üç servis için izleme kök yola istek gönderiyor ve sürekli hata alıyor; izleme ayarı yanlış adrese bakıyor olabilir.", "3 servis için kök yola yoklama, sürekli 4xx",
          [y_a, y_b, y_c], ["citrix"], [], [{"ad": h, "tip": "servis", "alt": "/"} for h in ("boaidentity.mrd.local", "satinalma.mrd.local", "toplu-islem.mrd.local")],
          [("Öncelik", "Düşük"), ("Durum", "Açık"), ("Uyarı", "3"), ("Varlık", "3 servis"), ("Kim olduğu", "uygulama geçidi kaydı"), ("Kaynak", "1, uygulama geçidi"),
           ("Görülme sıklığı", "312 servisin 3'ünde"), ("Başka açıklama", "Arandı, bulunamadı"), ("Yoğun gün", "Her gün")],
          [("30.240", "yoklama"), ("1", "dakika aralık"), ("3", "servis")],
          [("İzleme adreslerinin düzeltilmesi", "3 servis için sağlık kontrolü adresi", "İzleme ekibi")],
          [("İzleme tanımı", "3 servis için tanımlı sağlık kontrolü adresi", "İzleme ekibi")],
          [{"baslik": "Servisler", "kolon": ["Adres", "Yol", "Baskın kod", "İstek"], "sayisal": [3], "satir": [["boaidentity.mrd.local", "/", "404", "10.080"], ["satinalma.mrd.local", "/", "400", "10.080"], ["toplu-islem.mrd.local", "/", "404", "10.080"]]}],
          ham12, None, [{"gun": GUNLER[i], "saat": "", "baslik": "Dakikada bir yoklama", "ayrinti": "404 ve 400 yanıtları", "kaynak": "citrix", "ton": "bilgi"} for i in (0, 3, 6)])

    # 13. test ortami
    iid = "test-ortami"
    t_uyari = [uyari(iid, h, "servis", "Servis arızası", "Test ortamında hafta boyu hata döndü", "citrix", "2026-05-03", 40) for h in ("jira-test.mrd.local", "apigw-uat.mrd.local", "kart-test.mrd.local")]
    ham13 = ham_paket("citrix", rng, lambda r, i: {"src": "10.82.211.9", "dst": "10.60.73.14", "host": ["jira-test.mrd.local", "apigw-uat.mrd.local", "kart-test.mrd.local"][i % 3],
                                                  "yol": "/rest/api/2/issue", "durum": 502}, 12, 8_411, "uyari_013_test_ortami.csv", GUNLER, (0, 23))
    kucuk(iid, "tema_test", "Test ortamı", 40, "Test ortamında 3 adres hata alıyor", "üretimden ayrı değerlendirilir",
          "Test ortamındaki adreslerde sunucu ve istemci hataları var; üretimle ayrı değerlendirilir.", "Test ortamında 3 adres hata alıyor",
          t_uyari, ["citrix"], [], [{"ad": h, "tip": "servis", "alt": "test ortamı"} for h in ("jira-test.mrd.local", "apigw-uat.mrd.local", "kart-test.mrd.local")],
          [("Öncelik", "Düşük"), ("Durum", "Açık"), ("Uyarı", "3"), ("Varlık", "3 servis"), ("Kim olduğu", "uygulama geçidi kaydı"), ("Kaynak", "1, uygulama geçidi"),
           ("Görülme sıklığı", "28 test adresinin 3'ünde"), ("Başka açıklama", "Arandı, bulunamadı"), ("Yoğun gün", "3 May")],
          [("8.411", "hata"), ("502", "baskın kod"), ("3", "servis")],
          [("Test ortamı sahipleri", "3 servis için sorumlu ekip", "Uygulama sahipleri")],
          [("Servis sahibi", "Test ortamı adresleri için sorumlu kaydı", "Envanter yöneticisi")],
          [{"baslik": "Servisler", "kolon": ["Adres", "Ortam", "Baskın kod", "İstek"], "sayisal": [3],
            "satir": [["jira-test.mrd.local", "Test", "502", "3.211"], ["apigw-uat.mrd.local", "Test", "502", "2.906"], ["kart-test.mrd.local", "Test", "502", "2.294"]]}],
          ham13, None, [{"gun": "2026-05-03", "saat": "", "baslik": "Hata oranı arttı", "ayrinti": "3 servis", "kaynak": "citrix", "ton": "bilgi"}])

    # 14. bkoc
    iid = "yeni-ag-bkoc"
    ag14 = ag_listesi(rng, normal=["10.160.127.0/24"], engel=["10.60.89.0/24"], istek_araligi=(8, 50), gunler=GUNLER[3:5])
    for x in ag14:
        if x["sinif"] == "engel":
            x["istek"] = 26
    b14 = uyari(iid, bkoc, "kisi", "Yeni iç ağa gidiş", "1 yeni iç ağa istek gönderdi, engellendi", "vpn", "2026-05-02", 57, ["T1018"])
    ham14 = ham_paket("vpn", rng, lambda r, i: {"src": "10.249.90.12", "dst": "10.60.89.14", "kullanici": "bkoc", "port": 22, "aksiyon": "deny"}, 6, 26, "uyari_014_bkoc.csv", GUNLER[4:6], (10, 16))
    kucuk(iid, "kisi", "Yeni iç ağ", 57, "Burcu Koç", "İç Denetim, yeni iç ağa gidiş",
          "Hesap dönemde ilk kez bir yönetim ağına istek gönderdi; istek engellendi.", "1 yeni iç ağ, istek engellendi",
          [b14], ["vpn"], ["T1018"], [{"ad": "bkoc", "tip": "kisi", "alt": "Burcu Koç, İç Denetim"}],
          [("Öncelik", "Düşük"), ("Durum", "Açık"), ("Uyarı", "1"), ("Varlık", "1 kişi"), ("Kim olduğu", "VPN oturumundan"), ("Kaynak", "1, VPN günlükleri"),
           ("Görülme sıklığı", "498 kullanıcının 21'inde"), ("Başka açıklama", "Sorulmadı"), ("Yoğun gün", "2 May")],
          [("1", "yeni iç ağ"), ("0", "ulaşıldı"), ("26", "engellenen istek")],
          [("Denetim görevi kaydı", "yönetim ağına erişimi gerektiren denetim görevi", "İç Denetim")],
          [("Görev kaydı", "İç denetim çalışması için yönetim ağı erişim gerekçesi", "İç Denetim")],
          [{"baslik": "Ağlar", "kolon": ["Ağ", "Ağ tanımı", "Sonuç", "İstek"], "sayisal": [3], "satir": [["10.60.89.0/24", "Yönetim ağı", "Engellendi", "26"]]}],
          ham14, "2026-05-02", [{"gun": "2026-05-02", "saat": "14:03", "baslik": "Yönetim ağına istek", "ayrinti": "10.60.89.0/24, engellendi", "kaynak": "vpn", "ton": "bilgi"}])
    incelemeler[-1]["graf"] = {"tur": "kisi", "kisiler": [{"ad": "bkoc", "ad_soyad": "Burcu Koç", "alt": "İç Denetim", "ag": ag14, "ozet": ag_ozet(ag14)}], "grup": {"ad": "İç Denetim", "uye": 9}}

    # 15. sguler
    iid = "surekli-engel-sguler"
    ag15 = ag_listesi(rng, normal=["10.160.127.0/24"], engel=["10.93.24.0/24"], istek_araligi=(10, 60), gunler=GUNLER[2:5])
    for x in ag15:
        if x["sinif"] == "engel":
            x["istek"] = 36
    s15 = uyari(iid, sguler, "kisi", "Sürekli engellenen istek", "3 gündür aynı iç ağa engelleniyor, günde ortalama 12 reddedilen istek", "vpn", "2026-05-02", 55, ["T1046"])
    ham15 = ham_paket("vpn", rng, lambda r, i: {"src": "10.249.16.90", "dst": f"10.93.24.{r.randint(10, 50)}", "kullanici": "sguler", "port": r.choice([1433, 8443]), "aksiyon": "deny"}, 8, 36, "uyari_015_sguler.csv", GUNLER[3:6], (9, 17))
    kucuk(iid, "kisi", "Sürekli engelleme", 55, "Sinan Güler", "Uyum, sürekli engellenen istek",
          "Hesap 3 gündür aynı iç ağa istek gönderiyor ve her seferinde engelleniyor.", "3 gündür aynı ağa istek, günde ortalama 12 ret",
          [s15], ["vpn"], ["T1046"], [{"ad": "sguler", "tip": "kisi", "alt": "Sinan Güler, Uyum"}],
          [("Öncelik", "Düşük"), ("Durum", "Açık"), ("Uyarı", "1"), ("Varlık", "1 kişi"), ("Kim olduğu", "VPN oturumundan"), ("Kaynak", "1, VPN günlükleri"),
           ("Görülme sıklığı", "498 kullanıcının 12'sinde"), ("Başka açıklama", "Arandı, bulunamadı"), ("Yoğun gün", "1 May")],
          [("36", "reddedilen istek"), ("3", "gün"), ("0", "geçen istek")],
          [("Erişim beklentisi", "kullanıcının bu ağa erişmesi gereken görev", "Uyum yöneticisi")],
          [("Erişim beklentisi", "Kullanıcının bu ağa erişmesi gereken bir görev olup olmadığı", "Uyum yöneticisi")],
          [{"baslik": "Günlük dağılım", "kolon": ["Gün", "İstek", "Reddedilen", "Geçen"], "sayisal": [1, 2, 3], "satir": [["30 Nis", "11", "11", "0"], ["1 May", "13", "13", "0"], ["2 May", "12", "12", "0"]]}],
          ham15, "2026-05-01", [{"gun": g, "saat": "", "baslik": "Aynı ağa reddedilen istekler", "ayrinti": "10.93.24.0/24", "kaynak": "vpn", "ton": "bilgi"} for g in GUNLER[3:6]])
    incelemeler[-1]["graf"] = {"tur": "kisi", "kisiler": [{"ad": "sguler", "ad_soyad": "Sinan Güler", "alt": "Uyum", "ag": ag15, "ozet": ag_ozet(ag15)}], "grup": {"ad": "Uyum", "uye": 14}}

    # 16. tek dis blok
    iid = "dis-blok-tekil"
    d16 = uyari(iid, "192.0.2.0/24", "adres", "Dış web taraması", "6 adres 2 gündür imzalı istek gönderiyor", "citrix", "2026-05-02", 44, ["T1595"])
    ham16 = ham_paket("waf", rng, lambda r, i: {"src": f"192.0.2.{r.randint(2, 250)}", "imza": "APPFW_SIGNATURE_MATCH", "aciklama": "Signature violation",
                                                 "url": "http://mrd-web.mrd.local/api/arama", "sonuc": "blocked"}, 8, 143, "uyari_016_dis_blok.csv", GUNLER[5:], (2, 6))
    kucuk(iid, "dis_tarama", "Dış tarama", 44, "192.0.2.0/24", "dış adres bloğu, imzalı istek",
          "İnternetten bir adres bloğu 2 gündür imzalı istek gönderiyor; istekler uygulama geçidinde engellendi.", "6 adres, 143 imzalı istek",
          [d16], ["citrix"], ["T1595"], [{"ad": "192.0.2.0/24", "tip": "adres", "alt": "6 adres"}],
          [("Öncelik", "Düşük"), ("Durum", "Açık"), ("Uyarı", "1"), ("Varlık", "1 dış adres bloğu"), ("Kim olduğu", "kaynak adres"), ("Kaynak", "1, uygulama geçidi"),
           ("Görülme sıklığı", "9.812 dış bloğun 1'inde"), ("Başka açıklama", "Sorulmadı"), ("Yoğun gün", "3 May")],
          [("143", "imzalı istek"), ("6", "dış adres"), ("%100", "engellenen")],
          [("Bloğun sahibi", "adres bloğunun sahibi ve test kaydı", "Bilgi Güvenliği")],
          [("Bloğun sahibi", "Adres bloğunun kime ait olduğu", "Bilgi Güvenliği")],
          [{"baslik": "Blok", "kolon": ["Blok", "Adres", "İmzalı istek", "İmza sınıfı", "Engellenen pay"], "sayisal": [1, 2, 3, 4], "satir": [["192.0.2.0/24", "6", "143", "1", "%100"]]}],
          ham16, "2026-05-03", [{"gun": "2026-05-02", "saat": "", "baslik": "İlk imzalı istek", "ayrinti": "3 adres", "kaynak": "citrix", "ton": "bilgi"}, {"gun": "2026-05-03", "saat": "", "baslik": "6 adres", "ayrinti": "143 istek", "kaynak": "citrix", "ton": "bilgi"}])

    # -------------------------------------------------- oncelik etiketi (puan)
    for inc in incelemeler:
        p = inc["puan"]
        inc["oncelik"] = "yuksek" if p >= 84 else ("orta" if p >= 60 else "dusuk")

    # -------------------------------------------------- kisi haftasi (kisi sorgusu)
    haftalar = {}

    def hafta(k, istek, engel, oturum, yonetici, ilk, hukumler):
        haftalar[k] = {"ad_soyad": KISI[k]["ad_soyad"], "unvan": KISI[k]["unvan"], "birim": KISI[k]["birim"], "ik": KISI[k]["ik"],
                       "gunler": [{"gun": GUNLER[i], "istek": istek[i], "engel": engel[i], "oturum": oturum[i], "yonetici": yonetici[i], "ilk": ilk.get(i, [])} for i in range(7)],
                       "hukumler": hukumler}

    hafta("ktuncer", kt_istek, kt_engel, [0, 1, 3, 2, 2, 1, 0], [0] * 7,
          {1: [("ag", "10.249.53.0/24 kaynak ağ", "bilgi")], 2: [("bilgisayar", "MRDNB0388", "uyari")],
           3: [("ag", "10.93.24.0/24 ulaşıldı", "kritik"), ("ag", "10.93.61.0/24 ulaşıldı", "kritik"), ("ag", "10.93.101.0/24 ulaşıldı", "kritik"), ("ag", "10.60.89.0/24 engellendi", "uyari")]},
          [("kirmizi", "İşten ayrıldı, 8 Nis; hesap etkin ve dönemde 9 oturum açmış"), ("kirmizi", "5 gece VPN oturumu, 01:10 ile 03:40 arası"),
           ("turuncu", "Ulaştığı 3 ödeme ve kart ağına birimindeki 22 kişiden hiçbiri gitmiyor"), ("turuncu", "2 yönetim ağına istek gönderdi, engellendi"), ("bilgi", "3 kaynakta iz: VPN, etki alanı, güvenlik duvarı")])
    for k, n in zip(uyeler, agsay):
        hafta(k, im_gun[k]["istek"], im_gun[k]["engel"], [0, 0, 2, 2, 2, 1, 0], [0] * 7, {2: [("ag", f"{n} iç ağ engellendi, ilk kez", "uyari")]},
              [("kirmizi", f"{n} iç ağa istek gönderdi, hiçbiri geçmedi; grupta olağan 4"), ("turuncu", "Aynı birimden 8 kişi benzer davranış gösteriyor"),
               ("yesil", "Ulaştığı ağların hepsi grubunun da gittiği yerler"), ("bilgi", "Kaynak: VPN günlükleri")])
    for k, n in zip(dk_uyeler, dk_say):
        hafta(k, dk_gun[k]["istek"], dk_gun[k]["engel"], [0, 0, 2, 2, 2, 0, 0], [0] * 7, {2: [("ag", f"{n} iç ağ engellendi, ilk kez", "uyari")]},
              [("turuncu", f"{n} iç ağa istek gönderdi, hiçbiri geçmedi; grupta olağan 1"), ("yesil", "Ulaştığı ağların hepsi grubunun da gittiği yerler"), ("bilgi", "Kaynak: VPN günlükleri")])
    hafta("tsahin", paylastir(sum(x["istek"] for x in ag4), [10, 12, 12, 40, 26, 0, 0]), paylastir(sum(x["istek"] for x in ag4 if x["sinif"] == "engel"), [0, 0, 20, 50, 30, 0, 0]), [x * 3 + 8 if x else 0 for x in ts_yet], ts_yet,
          {3: [("bilgisayar", "MRDSRV0141, MRDSRV0142, MRDNB0774, MRDSRV0208", "uyari"), ("ag", "10.60.67.0/24 ulaşıldı", "kritik"), ("ag", "10.71.24.0/24 ulaşıldı", "kritik")]},
          [("kirmizi", "Yönetici yetkisi kullanan hesap; 30 Nisan'da 6 istasyondan doğruladı (taban 2)"), ("turuncu", "Aynı gün 2 yeni iç ağa ulaştı"), ("yesil", "1 Mayıs'ta istasyon sayısı taban düzeyine döndü"), ("bilgi", "Kaynak: etki alanı, güvenlik duvarı")])
    hafta("ugunes", [18, 26, 30, 22, 24, 0, 0], [0, 0, 1, 0, 0, 0, 0], [2, 2, 3, 2, 2, 0, 0], [0] * 7, {2: [("bilgisayar", "MRDNB0207 uç nokta olayı", "uyari")]},
          [("turuncu", "29 Nisan'da bilinen saldırı aracı arşivi tespit edildi ve engellendi"), ("yesil", "VPN ve oturum davranışı olağan"), ("bilgi", "Kaynak: uç nokta koruması")])
    hafta("ecetin", [22, 30, 26, 34, 28, 30 + ec_yeni, 0], [0, 0, 0, 0, 0, ec_engel, 0], [2, 2, 2, 2, 2, 3, 0], [0] * 7, {5: [("ag", "10.93.191.0/24 ulaşıldı", "uyari"), ("ag", "2 iç ağ engellendi", "uyari")]},
          [("turuncu", "2 Mayıs'ta 3 yeni iç ağa istek gönderdi; 1'ine ulaştı"), ("yesil", "Diğer günlerde davranışı olağan"), ("bilgi", "Kaynak: VPN günlükleri")])
    hafta("mdemir", [a + b for a, b in zip([12, 44, 60, 71, 69, 61, 0], [0, 0, 36, 41, 39, 36, 0])], [0, 0, 36, 41, 39, 36, 0], [1, 2, 2, 2, 2, 1, 0], [0] * 7, {2: [("ag", "10.93.191.0/24 engellendi, ilk kez", "uyari")]},
          [("turuncu", "4 gündür aynı iç ağa istek gönderiyor; her seferinde engellendi"), ("yesil", "Ulaştığı ağlar birimiyle aynı"), ("bilgi", "Kaynak: VPN günlükleri")])
    hafta("bkoc", [10, 14, 12, 16, 15, 30, 0], [0, 0, 0, 0, 0, 26, 0], [1, 1, 1, 1, 1, 1, 0], [0] * 7, {5: [("ag", "10.60.89.0/24 engellendi, ilk kez", "bilgi")]},
          [("turuncu", "2 Mayıs'ta yönetim ağına istek gönderdi; engellendi"), ("yesil", "Diğer günlerde davranışı olağan"), ("bilgi", "Kaynak: VPN günlükleri")])
    hafta("sguler", [8, 10, 11, 24, 26, 22, 0], [0, 0, 0, 11, 13, 12, 0], [1, 1, 1, 2, 2, 2, 0], [0] * 7, {3: [("ag", "10.93.24.0/24 engellendi, ilk kez", "bilgi")]},
          [("turuncu", "3 gündür aynı iç ağa istek gönderiyor; her seferinde engellendi"), ("bilgi", "Kaynak: VPN günlükleri")])

    # -------------------------------------------------- ag gecisleri (kuzey-guney, dogu-bati)
    kumeler = ["İnternet", "VPN İstemcileri", "Üçüncü Taraflar", "İnternet DMZ", "Intranet DMZ", "Kullanıcı Ağları", "Uygulama Sunucuları", "Ödeme ve Kart Sistemleri",
               "Veritabanı Sunucuları", "Yönetim Ağı", "Felaket Merkezi"]
    kenar = [
        ("İnternet", "İnternet DMZ", "İnternet güvenlik duvarı (Palo Alto)", 812_400_000, 41_200_000, "kuzey-güney"),
        ("İnternet", "Intranet DMZ", "İnternet güvenlik duvarı (Palo Alto)", 1_204, 88_410, "kuzey-güney"),
        ("İnternet", "Uygulama Sunucuları", "İnternet güvenlik duvarı (Palo Alto)", 0, 2_306_112, "kuzey-güney"),
        ("VPN İstemcileri", "Uygulama Sunucuları", "SSL VPN (Palo Alto)", 24_810_000, 3_240_000, "kuzey-güney"),
        ("VPN İstemcileri", "Kullanıcı Ağları", "SSL VPN (Palo Alto)", 6_120_000, 490_000, "kuzey-güney"),
        ("VPN İstemcileri", "Ödeme ve Kart Sistemleri", "SSL VPN (Palo Alto)", 2_140_000, 386_000, "kuzey-güney"),
        ("VPN İstemcileri", "Yönetim Ağı", "SSL VPN (Palo Alto)", 41_800, 1_912_000, "kuzey-güney"),
        ("Üçüncü Taraflar", "Ödeme ve Kart Sistemleri", "Üçüncü taraf güvenlik duvarı (Palo Alto)", 8_920_000, 12_400, "kuzey-güney"),
        ("Üçüncü Taraflar", "Uygulama Sunucuları", "Üçüncü taraf güvenlik duvarı (Palo Alto)", 3_110_000, 41_000, "kuzey-güney"),
        ("Kullanıcı Ağları", "İnternet", "İnternet güvenlik duvarı (Palo Alto)", 611_000_000, 9_800_000, "kuzey-güney"),
        ("Kullanıcı Ağları", "Uygulama Sunucuları", "İç güvenlik duvarı (Check Point)", 142_000_000, 1_120_000, "doğu-batı"),
        ("Kullanıcı Ağları", "Veritabanı Sunucuları", "İç güvenlik duvarı (Check Point)", 1_204_000, 812_000, "doğu-batı"),
        ("Kullanıcı Ağları", "Yönetim Ağı", "İç güvenlik duvarı (Check Point)", 302_000, 88_000, "doğu-batı"),
        ("Uygulama Sunucuları", "Veritabanı Sunucuları", "İç güvenlik duvarı (Check Point)", 386_000_000, 210_000, "doğu-batı"),
        ("Uygulama Sunucuları", "Ödeme ve Kart Sistemleri", "İç güvenlik duvarı (Check Point)", 94_000_000, 61_000, "doğu-batı"),
        ("Ödeme ve Kart Sistemleri", "Veritabanı Sunucuları", "İç güvenlik duvarı (Check Point)", 61_000_000, 9_400, "doğu-batı"),
        ("Yönetim Ağı", "Uygulama Sunucuları", "İç güvenlik duvarı (Check Point)", 24_000_000, 12_000, "doğu-batı"),
        ("Yönetim Ağı", "Veritabanı Sunucuları", "İç güvenlik duvarı (Check Point)", 11_400_000, 4_100, "doğu-batı"),
        ("Intranet DMZ", "Uygulama Sunucuları", "İç güvenlik duvarı (Check Point)", 48_000_000, 220_000, "doğu-batı"),
        ("İnternet DMZ", "Uygulama Sunucuları", "İç güvenlik duvarı (Check Point)", 212_000_000, 1_900_000, "doğu-batı"),
        ("Uygulama Sunucuları", "Felaket Merkezi", "İç güvenlik duvarı (Check Point)", 74_000_000, 3_100, "doğu-batı"),
        ("Veritabanı Sunucuları", "Felaket Merkezi", "İç güvenlik duvarı (Check Point)", 51_000_000, 2_400, "doğu-batı"),
    ]
    kenar = [{"kaynak": a, "hedef": b, "cihaz": c, "ulasan": d, "reddedilen": e, "yon": f} for (a, b, c, d, e, f) in kenar]

    veri_kaynaklari = [{"kod": k, "ad": v["ad"], "sistem": v["sistem"], "aralik": "27 Nis - 3 May 2026", "durum": "Bağlı"} for k, v in KAYNAK.items()]
    baglam = [{"ad": "Sunucu envanteri", "ne": "Sunucuların adı, adresi, ortamı ve sahibi", "kayit": "812 sunucu"},
              {"ad": "Ağ topolojisi", "ne": "Ağ parçaları ve bağlantıları", "kayit": "176 ağ, 61 cihaz"},
              {"ad": "Ağ cihazları envanteri", "ne": "Güvenlik duvarı, yük dengeleyici ve anahtar kayıtları", "kayit": "64 cihaz"},
              {"ad": "Organizasyon şeması", "ne": "Kişi, birim ve bağlı olduğu yönetici", "kayit": "421 kişi"},
              {"ad": "Dizin hesapları", "ne": "Hesap durumu, grup üyelikleri, İK durumu", "kayit": "2.214 hesap"}]

    incelemeler.sort(key=lambda x: -x["puan"])
    return {
        "kurum": KURUM, "kurum_alt": KURUM_ALT,
        "donem": {"bas": GUNLER[0], "bit": GUNLER[-1], "etiket": "27 Nis - 3 May 2026", "son_kosu": "3 May 2026, 09:12", "kisa": "27 Nis - 3 May", "son3": "1 May - 3 May"},
        "gunler": [{"tarih": g, "et": gun_et(g), "ad": GUN_ADI[i]} for i, g in enumerate(GUNLER)],
        "kaynaklar": KAYNAK, "mitre": {k: {"ad": v[0], "taktik": v[1]} for k, v in MITRE.items()}, "taktik_sirasi": TAKTIK_SIRASI,
        "incelemeler": incelemeler, "uyarilar": uyarilar, "kisiler": KISI, "haftalar": haftalar,
        "ag": {"kumeler": kumeler, "kenarlar": kenar, "dis_kaynak": ["İnternet", "VPN İstemcileri", "Üçüncü Taraflar"]}, "veri_kaynaklari": veri_kaynaklari, "baglam": baglam,
    }


if __name__ == "__main__":
    import json
    d = uret()
    print("inceleme:", len(d["incelemeler"]), "uyari:", len(d["uyarilar"]))
    for i in d["incelemeler"]:
        print(f"{i['puan']:>3} {i['oncelik']:<7} {i['tur']:<12} {len(i['uyarilar']):>2} uyari  {i['baslik']}")
    print(len(json.dumps(d, ensure_ascii=False)) // 1024, "KB")
