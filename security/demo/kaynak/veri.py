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
GUNLER = ["2026-09-14", "2026-09-15", "2026-09-16", "2026-09-17", "2026-09-18", "2026-09-19", "2026-09-20"]
AY = {"09": "Eyl"}
AY_EN = {"09": "Sep"}
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
    "vpn": {"ad": "VPN günlükleri", "sistem": "SSL VPN geçidi"},
    "dc": {"ad": "Etki alanı denetleyicisi", "sistem": "Microsoft Windows"},
    "gecit": {"ad": "Uygulama geçidi", "sistem": "Uygulama teslim denetleyicisi"},
    "fw": {"ad": "İç güvenlik duvarı", "sistem": "Yeni nesil güvenlik duvarı"},
    "edr": {"ad": "Uç nokta koruması", "sistem": "Uç nokta algılama ve yanıt"},
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
        return (f"{ay} {d:02d} {saat} mrd-vpn01 vpngw[{rng.randint(1000, 9999)}]: type=traffic time=\"{ay} {d:02d} 2026 {saat} UTC\" "
                f"src={k['src']} dst={k['dst']} user=MERIDYEN\\{k['kullanici']} proto=tcp dport={k['port']} action={k['aksiyon']} "
                f"sent={rng.randint(400, 9000)} rcvd={rng.randint(0, 120000) if k['aksiyon'] == 'allow' else 0} policy={k.get('kural', 'vpn-kullanici-erisim')}")
    if kaynak == "dc":
        kod = k.get("kod", "4624")
        return (f"{ay} {d:02d} {saat} mrd-dc02 MSWinEventLog\t1\tSecurity\t{rng.randint(5100000, 5199999)}\t"
                f"{ay} {d:02d} {saat} 2026\t{kod}\tMicrosoft-Windows-Security-Auditing\tMERIDYEN\\{k['kullanici']}\tN/A\t"
                f"Success Audit\tmrd-dc02.mrd.local\tLogon\t{k.get('metin', 'An account was successfully logged on.')} "
                f"Logon Type: {k.get('tip', 10)} Account Name: {k['kullanici']} Workstation Name: {k['istasyon']} "
                f"Source Network Address: {k['src']}")
    if kaynak == "fw":
        return (f"{ay} {d:02d} {saat} mrd-fw01 fwlog[{rng.randint(10000, 99999)}]: action={k.get('aksiyon', 'accept')} dir=inbound "
                f"src={k['src']} dst={k['dst']} dport={k['port']} proto=6 policy=\"{k.get('kural', 'vpn-odeme')}\" "
                f"user=\"{k['ad_soyad']} ({k['kullanici']})\" host={k['istasyon']}")
    if kaynak == "gecit":
        return (f"{ay} {d:02d} 2026 {saat} UTC mrd-adc01 httplog[{rng.randint(100000, 999999)}]: vserver={k['host']} "
                f"client={k['src']}:{rng.randint(30000, 60000)} backend={k['dst']}:8443 method=GET url={k['yol']} status={k['durum']}")
    if kaynak == "edr":
        return (f"{ay} {d:02d} {saat} mrd-edr01 epp[4411]: event=\"{k['olay']}\" time=\"{ay} {d:02d} 2026 {saat} +03:00\" "
                f"host={k['makine']} user=MERIDYEN\\{k['kullanici']} file={k['dosya']} path=\"{k['yol']}\" action={k['aksiyon']} category=\"{k['kategori']}\"")
    if kaynak == "waf":
        return (f"{ay} {d:02d} {saat} mrd-waf01 waflog[{rng.randint(1000, 9999)}]: sig={k['imza']} src={k['src']}:{rng.randint(20000, 60000)} "
                f"desc=\"{k['aciklama']}\" url={k['url']} result={k['sonuc']}")
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
    GRUP_A, OLAGAN_A = 46, 3
    im_kisileri = havuz_kisi(rng, GRUP_A, ["Tahsilat Uzmanı"] * 5 + ["Kıdemli Tahsilat Uzmanı"], "Tahsilat Operasyonları",
                             ozel={11: "Ekip Lideri", 23: "Ekip Lideri", 35: "Ekip Lideri"})
    GRUP_B, OLAGAN_B = 31, 2
    dk_kisileri = havuz_kisi(rng, GRUP_B, ["Yazılım Geliştirme Uzmanı", "Uygulama Geliştirici", "Test Mühendisi", "Ürün Analisti"],
                             "Uygulama Geliştirme")
    ktuncer = kisi_ekle("Kerem Tuncer", "Kıdemli Hazine Uzmanı", "Hazine Operasyonları", "İşten ayrıldı, 21 Ağu", "ktuncer")
    tsahin = kisi_ekle("Tolga Şahin", "Sistem Yöneticisi", "Altyapı ve Sistem Yönetimi", kullanici="tsahin")
    ugunes = kisi_ekle("Umut Güneş", "Güvenlik Analisti", "Bilgi Güvenliği", kullanici="ugunes")
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
            x["gun"] = "2026-09-17"
    vpn_top = sum(x["istek"] for x in ag1)
    yal_top = sum(x["istek"] for x in ag1 if x["sinif"] == "yalniz")
    kt_istek = paylastir(vpn_top, [0, 10, 20, 45, 17, 8, 0])
    kt_engel = paylastir(sum(x["istek"] for x in ag1 if x["sinif"] == "engel"), [0, 5, 12, 60, 17, 6, 0])
    yal_30 = round(yal_top * 0.62)
    yal_1 = round(yal_top * 0.30)
    u1 = uyari(iid, ktuncer, "kisi", "Gece saatinde oturum", "5 gece art arda VPN oturumu (01:10 ile 03:40 arası)", "vpn", "2026-09-15", 84, ["T1078", "T1133"])
    u2 = uyari(iid, ktuncer, "kisi", "Yeni iç ağa gidiş", "3 yeni iç ağa ulaştı: ödeme ve kart sistemleri", "vpn", "2026-09-17", 90, ["T1021", "T1018"])
    u3 = uyari(iid, ktuncer, "kisi", "Ayrılan personel hesabı", "Ayrılmış personelin hesabı etkin, dönemde 9 oturum açılmış", "dc", "2026-09-16", 88, ["T1078"])
    u4 = uyari(iid, ktuncer, "kisi", "Yeni iç ağa gidiş", "Hesabın bilgisayarından ödeme ağındaki 2 sunucuya bağlantı", "fw", "2026-09-17", 82, ["T1021"])
    vpn_gece = ["2026-09-15", "2026-09-16", "2026-09-17", "2026-09-18", "2026-09-19"]

    def u_vpn_ktuncer(r, i):
        g = vpn_gece[i % 5]
        hedef = r.choice(["10.93.24.15", "10.93.24.17", "10.93.61.21", "10.93.101.9"]) if g >= "2026-09-17" else r.choice(["10.160.127.31", "10.60.241.14"])
        return {"src": "10.249.53.41", "dst": hedef, "kullanici": "ktuncer", "port": r.choice([1433, 3389, 443, 8443]),
                "aksiyon": "allow", "kural": "vpn-kullanici-erisim"}

    ham1 = ham_paket("vpn", rng, u_vpn_ktuncer, 12, vpn_top, "uyari_001_ktuncer.csv", vpn_gece, (1, 3))
    incelemeler.append({
        "id": iid, "tur": "cok_kaynak", "tur_ad": "Çoklu kaynak", "puan": 94,
        "baslik": "Kerem Tuncer", "alt": "Hazine Operasyonları, işten ayrıldı, hesap etkin",
        "ozet": "Ayrılış kaydı 21 Ağustos, hesap etkin; dönemde 5 gece VPN oturumu açılmış ve 3 ödeme ve kart ağına ulaşılmış.",
        "kart_ozet": "İşten ayrıldıktan sonra hesap etkin; gece VPN ile ödeme ağlarına ulaşıldı",
        "uyarilar": [u1, u2, u3, u4], "kaynaklar": ["vpn", "dc", "fw"], "mitre": ["T1078", "T1133", "T1021", "T1018"], "asama": "İlk erişim",
        "varliklar": [{"ad": "ktuncer", "tip": "kisi", "alt": "Kerem Tuncer, Hazine Operasyonları"},
                      {"ad": "MRDLT0388", "tip": "bilgisayar", "alt": "kayıtlı kullanıcı: Kerem Tuncer"}],
        "alan": [("Öncelik", "Yüksek"), ("Durum", "Açık"), ("Uyarı", "4"), ("Varlık", "1 kişi, 1 bilgisayar"),
                 ("Kim olduğu", "İK kaydı ve dizin hesabı"), ("Kaynak", "3, VPN, etki alanı, güvenlik duvarı"),
                 ("Görülme sıklığı", "Ayrılan 143 hesabın 1'inde"), ("Başka açıklama", "Sorulmadı"), ("Yoğun gün", "17 Eyl")],
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
             "satir": [["VPN günlükleri", "Gece saatinde oturum", "15 Eyl, 19 Eyl", "5 gece"],
                       ["VPN günlükleri", "Yeni iç ağa ulaşıldı", "17 Eyl", "3 ağ"],
                       ["Etki alanı denetleyicisi", "Ayrılmış personelin hesabıyla oturum", "16 Eyl, 18 Eyl", "9 oturum"],
                       ["İç güvenlik duvarı", "Bilgisayardan ödeme ağına bağlantı", "17 Eyl", "2 sunucu"]]},
            {"baslik": "Ulaşılan ağlar", "kolon": ["Ağ", "Ağ tanımı", "İstek", "Geçen", "İlk görülme", "Benzerlerinden giden"], "sayisal": [2, 3, 5],
             "satir": [[x["cidr"], x["ad"] or "kayıtlarda tanımlı değil", sayi(x["istek"]), sayi(x["gecen"]), gun_et(x["gun"]),
                        f"{round(x['grup_pay'] * 18)} / 18"] for x in ag1 if x["sinif"] in ("yalniz", "normal")]},
            {"baslik": "Bağlam", "kolon": ["Alan", "Değer"], "sayisal": [],
             "satir": [["İK durumu", "İşten ayrıldı, 21 Ağu 2026"], ["Dizin hesabı", "Etkin"], ["Birim", "Hazine Operasyonları"],
                       ["Unvan", "Kıdemli Hazine Uzmanı"], ["Son parola değişimi", "4 Tem 2026"]]}],
        "ham": ham1, "yogun_gun": "2026-09-17",
        "zaman": [
            {"gun": "2026-09-15", "saat": "01:12", "baslik": "İlk gece VPN oturumu", "ayrinti": "10.249.53.41 adresi atandı; iç kullanıcı ağı ve uygulama sunucularına 6 bağlantı", "kaynak": "vpn", "ton": "uyari"},
            {"gun": "2026-09-16", "saat": "02:14", "baslik": "Etkileşimli oturum, yeni bilgisayar", "ayrinti": "MRDLT0388 üzerinde uzak masaüstü oturumu; hesap için ilk kez görülen bilgisayar", "kaynak": "dc", "ton": "uyari"},
            {"gun": "2026-09-17", "saat": "01:47", "baslik": "Ödeme ağlarına ilk ulaşım", "ayrinti": f"10.93.24.0/24, 10.93.61.0/24 ve 10.93.101.0/24 ağlarına {sayi(yal_30)} bağlantı, hepsi izinli", "kaynak": "vpn", "ton": "kritik"},
            {"gun": "2026-09-17", "saat": "01:52", "baslik": "Yönetim ağına deneme", "ayrinti": "10.60.89.0/24 ve 10.60.9.0/24 için istek gönderildi, engellendi", "kaynak": "fw", "ton": "uyari"},
            {"gun": "2026-09-18", "saat": "02:31", "baslik": "Aynı ağlarda ikinci gece", "ayrinti": f"Ödeme ve kart ağlarına {sayi(yal_1)} bağlantı", "kaynak": "vpn", "ton": "uyari"},
            {"gun": "2026-09-19", "saat": "03:40", "baslik": "Son gece oturumu", "ayrinti": "Oturum 3 saat 40 dakika sürdü", "kaynak": "vpn", "ton": "bilgi"}],
        "graf": {"tur": "kisi", "kisiler": [{"ad": "ktuncer", "ad_soyad": "Kerem Tuncer", "alt": "Hazine Operasyonları", "ag": ag1, "ozet": ag_ozet(ag1)}],
                 "grup": {"ad": "Hazine Operasyonları", "uye": 18}}})

    # ==================================================================
    # 2. Tahsilat Operasyonlari (kume)
    # ==================================================================
    iid = "tahsilat-operasyonlari"
    uyeler = im_kisileri[:8]
    agsay = [64, 58, 51, 47, 42, 38, 33, 29]
    NA = len(uyeler)
    KAT_A = min(agsay) // OLAGAN_A
    im_uyari, im_graf, im_satir = [], [], []
    toplam_istek = 0
    im_gun = {}
    for sira, (k, n) in enumerate(zip(uyeler, agsay)):
        istek = n * rng.randint(6, 12)
        agirlik = [0, 0, 10, 58, 22, 8, 2] if sira < 6 else [0, 0, 55, 30, 10, 4, 1]
        engel_gun = paylastir(istek, agirlik)
        gun = en_yogun(engel_gun)
        toplam_istek += istek
        im_uyari.append(uyari(iid, k, "kisi", "Grup davranışı", f"{n} iç ağa istek gönderdi, hiçbiri geçmedi (grupta olağan {OLAGAN_A})", "vpn", gun, 88, ["T1046", "T1018"]))
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
        im_satir.append([k, KISI[k]["ad_soyad"], KISI[k]["unvan"], sayi(n), str(OLAGAN_A), "0", sayi(istek), gun_et(gun)])
    im_top_gun = [sum(im_gun[k]["engel"][i] for k in uyeler) for i in range(7)]
    im_zaman = [
        {"gun": GUNLER[0], "saat": "", "baslik": "Taban günü", "ayrinti": f"{GRUP_A} kişinin hiçbiri olağan dışı sayıda ağa istek göndermedi", "kaynak": "vpn", "ton": "bilgi"},
        {"gun": GUNLER[2], "saat": "", "baslik": "İlk engellenen istekler", "ayrinti": f"{NA} kişiden toplam {sayi(im_top_gun[2])} engellenen istek", "kaynak": "vpn", "ton": "uyari"},
        {"gun": GUNLER[3], "saat": "", "baslik": "En yoğun gün", "ayrinti": f"{NA} kişinin tamamından {sayi(im_top_gun[3])} engellenen istek", "kaynak": "vpn", "ton": "kritik"},
        {"gun": GUNLER[4], "saat": "", "baslik": "Yoğunluk düştü", "ayrinti": f"{sayi(im_top_gun[4])} engellenen istek, 17 Eylül'ün %{round(100 * im_top_gun[4] / im_top_gun[3])} kadarı", "kaynak": "vpn", "ton": "bilgi"}]
    ham2_dosya = "uyari_002_tahsilat_operasyonlari.csv"

    def u_vpn_im(r, i):
        k = uyeler[i % NA]
        return {"src": f"10.249.{[16, 53, 90][i % 3]}.{20 + i}", "dst": f"10.{r.choice([137, 214, 212, 111, 44, 164, 195])}.{r.randint(1, 254)}.{r.randint(2, 250)}",
                "kullanici": k, "port": r.choice([445, 3389, 22, 1433, 8080, 135]), "aksiyon": "deny", "kural": "varsayilan-red"}

    ham2 = ham_paket("vpn", rng, u_vpn_im, 12, toplam_istek, ham2_dosya, ["2026-09-16", "2026-09-17"], (8, 17))
    incelemeler.append({
        "id": iid, "tur": "kume", "tur_ad": "Grup davranışı", "puan": 91,
        "baslik": "Tahsilat Operasyonları", "alt": f"{NA} / {GRUP_A} kişi, engellenen iç ağ istekleri",
        "ozet": f"Grup içinde {NA} kişilik alt küme: engellenen ağ sayısı grupta olağanın en az {KAT_A} katı, ulaşılan yeni ağ yok.",
        "kart_ozet": f"{GRUP_A} kişilik gruptan {NA}'i onlarca iç ağa istek gönderdi, hiçbiri geçmedi",
        "uyarilar": im_uyari, "kaynaklar": ["vpn"], "mitre": ["T1046", "T1018"], "asama": "İç keşif",
        "varliklar": [{"ad": k, "tip": "kisi", "alt": KISI[k]["ad_soyad"]} for k in uyeler],
        "alan": [("Öncelik", "Yüksek"), ("Durum", "Açık"), ("Uyarı", str(NA)), ("Varlık", f"{NA} kişi"), ("Kim olduğu", "VPN oturumundan"),
                 ("Kaynak", "1, VPN günlükleri"), ("Görülme sıklığı", f"{GRUP_A} kişinin {NA}'inde"), ("Başka açıklama", "Sorulmadı"), ("Yoğun gün", "17 Eyl")],
        "nedenler": [f"Grupta olağanın en az {KAT_A} katı", f"Aynı birimde {NA} kişi", "Hiçbir istek geçmedi", "Aynı gün yoğunlaşma"],
        "metrikler": [(f"{min(agsay)}-{max(agsay)}", "engellenen ağ"), (str(OLAGAN_A), "grupta olağan"), ("0", "ulaşılan yeni ağ")],
        "adimlar": [(f"{NA} bilgisayarın ortak noktası", "lokasyon, istemci sürümü, VPN profili", "Sistem ekibi"),
                    ("Hedeflerin durumu", "engellenen ağların kaldırılmış aralıklar olup olmadığı", "Ağ ekibi"),
                    ("İstekleri gönderen program", "bu dönemde uç nokta kaydı yok", "Uç nokta koruması sahibi")],
        "eksik": [("İstekleri gönderen program", f"Bu dönemde bu {NA} bilgisayardan uç nokta kaydı gelmiyor", "Uç nokta koruması sahibi"),
                  (f"{NA} bilgisayarın ortak yapılandırması", "İstemci sürümü, VPN profili ve lokasyon bilgisi", "Sistem ekibi"),
                  ("Engellenen ağların kayıt durumu", "Hedef aralıkların envanter ve topolojide karşılığı", "Ağ ekibi")],
        "lehine": ["kısa sürede çok sayıda iç ağ", f"grupta olağanın {KAT_A} katı", "port çeşitliliği yüksek"],
        "aleyhine": [f"aynı birimde {NA} kişi, aynı gün", "hedefler kaldırılmış aralıklar olabilir", "hiçbir istek geçmedi"],
        "kanit": [
            {"baslik": "Kişiler", "kolon": ["Kullanıcı", "Ad", "Unvan", "Engellenen ağ", "Grupta olağan", "Ulaşılan yeni ağ", "Engellenen istek", "Yoğun gün"],
             "sayisal": [3, 4, 5, 6], "satir": im_satir},
            {"baslik": "Grupla kıyas", "kolon": ["Ölçü", f"Bu {NA} kişi", f"Grubun geri kalanı ({GRUP_A - NA} kişi)", "Tüm kullanıcılar"], "sayisal": [1, 2, 3],
             "satir": [["Engellenen ağ, ortanca", str(sorted(agsay)[NA // 2]), str(OLAGAN_A), str(OLAGAN_A)], ["Engellenen ağ, en yüksek", str(max(agsay)), "6", str(max(agsay))],
                       ["Engellenen istek, toplam", sayi(toplam_istek), "318", sayi(toplam_istek + 318)], ["Ulaşılan yeni ağ", "0", "1", "1"]]}],
        "ham": ham2, "yogun_gun": "2026-09-17",
        "zaman": im_zaman,
        "graf": {"tur": "grup", "kisiler": im_graf, "grup": {"ad": "Tahsilat Operasyonları", "uye": GRUP_A}}})

    # ==================================================================
    # 3. Uretim servisleri (tema, servis arizasi)
    # ==================================================================
    iid = "uretim-servisleri"
    servisler = [
        ("kredi-skor.mrd.local", "/v2/skor/hesapla", 503, 7412, 7), ("musteri-bildirim.mrd.local", "/api/bildirim/gonder", 500, 6980, 7),
        ("belge-arsiv.mrd.local", "/arsiv/ara", 502, 5236, 6), ("sube-randevu.mrd.local", "/randevu/musaitlik", 503, 4871, 7),
        ("rapor-merkezi.mrd.local", "/api/rapor/uret", 500, 3904, 6)]
    NS = len(servisler)
    sv_uyari, sv_satir = [], []
    sv_toplam = sum(s[3] for s in servisler)
    sv_min = min(s[3] for s in servisler)
    KOD_ANLAM = {500: "Sunucu iç hatası", 502: "Geçersiz ağ geçidi yanıtı", 503: "Servis kullanılamıyor"}
    sv_kod = {}
    for s in servisler:
        sv_kod[s[2]] = sv_kod.get(s[2], 0) + s[3]
    for host, yol, kod, adet, gunsay in servisler:
        sv_uyari.append(uyari(iid, host, "servis", "Servis arızası", f"Hafta boyu {kod} döndü ({sayi(adet)} istek), alarm üretilmemiş", "gecit",
                              GUNLER[0], 86 if kod == 503 else 84))
        sv_satir.append([host, yol, str(kod), sayi(adet), f"{gunsay} / 7", "0"])
    sorumlu_sv = [["kredi-skor.mrd.local", "Kredi Sistemleri Ekibi", "Selim Yavuz"], ["musteri-bildirim.mrd.local", "Kanal Uygulamaları", "Aslı Bayram"],
                  ["belge-arsiv.mrd.local", "Belge Yönetimi Ekibi", "Cem Tunç"], ["sube-randevu.mrd.local", "Şube Uygulamaları", "Deniz Erdem"],
                  ["rapor-merkezi.mrd.local", "Raporlama Ekibi", "kayıt yok"]]

    def u_gecit(r, i):
        s = servisler[i % NS]
        return {"src": f"10.82.239.{14 + i % 5}", "dst": f"10.60.241.{21 + i % 6}", "host": s[0], "yol": s[1], "durum": s[2]}

    ham3 = ham_paket("gecit", rng, u_gecit, 12, sum(s[3] for s in servisler), "uyari_003_uretim_servisleri.csv", GUNLER, (0, 23))
    incelemeler.append({
        "id": iid, "tur": "servis", "tur_ad": "Servis arızası", "puan": 87,
        "baslik": f"{NS} üretim servisi", "alt": "hafta boyu sunucu hatası, alarm üretilmemiş",
        "ozet": f"{NS} üretim servisi hafta boyunca sunucu hatası döndürüyor: toplam {sayi(sv_toplam)} istek, servis başına en az {sayi(sv_min)} istek. Bu süre boyunca hiçbir alarm oluşmamış.",
        "kart_ozet": f"{NS} üretim servisi hafta boyu 5xx döndürüyor, hiçbirinde alarm yok",
        "uyarilar": sv_uyari, "kaynaklar": ["gecit"], "mitre": [], "asama": "",
        "varliklar": [{"ad": s[0], "tip": "servis", "alt": s[1]} for s in servisler],
        "alan": [("Öncelik", "Yüksek"), ("Durum", "Açık"), ("Uyarı", str(NS)), ("Varlık", f"{NS} servis"), ("Kim olduğu", "uygulama geçidi kaydı"),
                 ("Kaynak", "1, uygulama geçidi"), ("Görülme sıklığı", f"274 servisin {NS}'inde"), ("Başka açıklama", "Arandı, bulunamadı"), ("Yoğun gün", "Her gün")],
        "nedenler": ["Hafta boyunca kesintisiz", "Üretim ortamı", "Sunucu hatası (5xx)", "Alarm üretilmemiş"],
        "metrikler": [(sayi(sv_toplam), "sunucu hatası isteği"), ("7 / 7", "gün"), ("0", "üretilen alarm")],
        "adimlar": [("Servis sahibi ekiplerin bilgilendirilmesi", f"{NS} servis için sorumlu ekip; 1 servisin envanterde sorumlusu yok", "Uygulama sahipleri"),
                    ("İzleme tanımlarının gözden geçirilmesi", "bu servisler için sağlık kontrolü alarmı", "İzleme ekibi"),
                    ("Servislerin kullanım durumu", "hâlâ trafik alan servisler ve çağıran uygulamalar", "Servis sahibi")],
        "eksik": [("Servis sahibi", "rapor-merkezi servisi için envanterde sorumlu kaydı", "Envanter yöneticisi"),
                  ("İzleme kapsamı", f"{NS} servis için tanımlı sağlık alarmı olup olmadığı", "İzleme ekibi")],
        "lehine": ["hata kodu 5xx, servis tarafı", "hafta boyunca kesintisiz", "alarm yok"], "aleyhine": ["test amaçlı çağrı olabilir", "yük dengeleyici sağlık kontrolü olabilir"],
        "kanit": [
            {"baslik": "Servisler", "kolon": ["Adres", "Yol", "Baskın kod", "İstek", "Gün", "Alarm"], "sayisal": [2, 3, 4, 5], "satir": sv_satir},
            {"baslik": "Cevap kodu dağılımı", "kolon": ["Kod", "Anlamı", "İstek", "Pay"], "sayisal": [2, 3],
             "satir": [[str(kd), KOD_ANLAM[kd], sayi(n), "%" + f"{100 * n / sv_toplam:.1f}".replace(".", ",")]
                       for kd, n in sorted(sv_kod.items(), key=lambda x: -x[1])]},
            {"baslik": "Sorumlu ekipler", "kolon": ["Adres", "Ekip", "Sorumlu"], "sayisal": [], "satir": sorumlu_sv}],
        "ham": ham3, "yogun_gun": None,
        "zaman": [{"gun": g, "saat": "", "baslik": "Sunucu hatası sürüyor", "ayrinti": f"{NS} serviste sunucu hatası; alarm yok", "kaynak": "gecit", "ton": "uyari" if i in (0, 6) else "bilgi"}
                  for i, g in enumerate(GUNLER)],
        "graf": None})

    # ==================================================================
    # 4. Yonetici hesabi istasyon sicramasi
    # ==================================================================
    iid = "yonetici-istasyon"
    ts_yet = paylastir(263, [25, 28, 27, 92, 42, 0, 0])
    ag4 = ag_listesi(rng, normal=["10.60.89.0/24", "10.60.9.0/24"], yalniz=["10.60.67.0/24", "10.71.24.0/24", "10.82.90.0/24"], engel=["10.93.191.0/24"],
                     istek_araligi=(20, 220), gunler=GUNLER[2:5])
    for x in ag4:
        if x["sinif"] == "yalniz":
            x["gun"] = "2026-09-17"
    y1 = uyari(iid, tsahin, "kisi", "Yönetici yetkisi hareketi", "Yönetici hesabı taban haftada 3 istasyondan doğruladı, 17 Eylül'de 9 istasyondan", "dc", "2026-09-17", 85, ["T1078.002", "T1021"])
    y2 = uyari(iid, tsahin, "kisi", "Yeni iç ağa gidiş", "Aynı gün 3 yeni iç ağa ulaştı: felaket merkezi, şube ağ cihazları ve tanımsız yönetim bloğu", "fw", "2026-09-17", 83, ["T1021"])

    def u_dc_ts(r, i):
        return {"kullanici": "tsahin", "istasyon": r.choice(["MRDLT0211", "MRDSRV0141", "MRDSRV0142", "MRDLT0774", "MRDLT0312", "MRDSRV0208", "MRDSRV0233", "MRDLT0690", "MRDLT0455"]),
                "src": f"10.160.127.{20 + i}", "kod": "4672" if i % 3 == 0 else "4624", "tip": 3 if i % 2 else 10,
                "metin": "Special privileges assigned to new logon." if i % 3 == 0 else "An account was successfully logged on."}

    ham4 = ham_paket("dc", rng, u_dc_ts, 12, 263, "uyari_004_tsahin.csv", ["2026-09-17", "2026-09-18"], (8, 18))
    incelemeler.append({
        "id": iid, "tur": "yonetici", "tur_ad": "Yönetici yetkisi", "puan": 85,
        "baslik": "Tolga Şahin", "alt": "Sistem Yöneticisi, istasyon sıçraması ve yeni iç ağlar",
        "ozet": "Yönetici hesabı taban haftada 3 istasyondan doğruladı, 17 Eylül'de 9 istasyondan doğruladı; aynı gün 3 yeni iç ağa ulaştı.",
        "kart_ozet": "Yönetici hesabı 3 yerine 9 istasyondan doğruladı, aynı gün 3 yeni iç ağa ulaştı",
        "uyarilar": [y1, y2], "kaynaklar": ["dc", "fw"], "mitre": ["T1078.002", "T1021"], "asama": "Yanal hareket",
        "varliklar": [{"ad": "tsahin", "tip": "kisi", "alt": "Tolga Şahin, Altyapı ve Sistem Yönetimi"}],
        "alan": [("Öncelik", "Yüksek"), ("Durum", "Açık"), ("Uyarı", "2"), ("Varlık", "1 kişi"), ("Kim olduğu", "dizin hesabı"),
                 ("Kaynak", "2, etki alanı, güvenlik duvarı"), ("Görülme sıklığı", "19 yönetici hesabın 1'inde"), ("Başka açıklama", "Sorulmadı"), ("Yoğun gün", "17 Eyl")],
        "nedenler": ["Yönetici yetkili hesap", "Doğrulanan istasyon 3 katına çıktı", "3 yeni iç ağ", "2 kaynak doğruladı"],
        "metrikler": [("9", "istasyon, taban 3"), ("3", "yeni iç ağ"), ("263", "yetkili oturum")],
        "adimlar": [("Değişiklik ve bakım kayıtları", "17 Eyl için planlı bakım ya da değişiklik talebi", "Değişiklik yönetimi"),
                    ("Yeni istasyonların kullanım amacı", "MRDSRV0141, MRDSRV0142, MRDSRV0208, MRDSRV0233", "Sistem ekibi")],
        "eksik": [("Bakım penceresi kaydı", "17 Eyl için değişiklik ve bakım talepleri", "Değişiklik yönetimi"),
                  ("Yeni ağların envanter kaydı", "10.60.67.0/24 için envanter ve topoloji karşılığı", "Ağ ekibi")],
        "lehine": ["taban haftaya göre 3 kat istasyon", "yeni iç ağlara ulaşım", "yönetici yetkisi"], "aleyhine": ["planlı bakım olabilir", "yeni sunucu kurulumu olabilir"],
        "kanit": [
            {"baslik": "İstasyonlar", "kolon": ["İstasyon", "Tür", "İlk görülme", "Yetkili oturum"], "sayisal": [3],
             "satir": [["MRDLT0211", "Dizüstü", "Taban", "38"], ["MRDLT0312", "Dizüstü", "Taban", "27"], ["MRDLT0455", "Dizüstü", "Taban", "19"],
                       ["MRDSRV0141", "Sunucu", "17 Eyl", "52"], ["MRDSRV0142", "Sunucu", "17 Eyl", "41"], ["MRDSRV0208", "Sunucu", "17 Eyl", "29"],
                       ["MRDSRV0233", "Sunucu", "17 Eyl", "24"], ["MRDLT0774", "Dizüstü", "17 Eyl", "18"], ["MRDLT0690", "Dizüstü", "17 Eyl", "15"]]},
            {"baslik": "Ulaşılan ağlar", "kolon": ["Ağ", "Ağ tanımı", "İstek", "Geçen", "İlk görülme"], "sayisal": [2, 3],
             "satir": [[x["cidr"], x["ad"] or "kayıtlarda tanımlı değil", sayi(x["istek"]), sayi(x["gecen"]), gun_et(x["gun"])] for x in ag4 if x["sinif"] != "engel"]}],
        "ham": ham4, "yogun_gun": "2026-09-17",
        "zaman": [
            {"gun": "2026-09-14", "saat": "", "baslik": "Taban haftası", "ayrinti": f"3 istasyondan doğrulama, günde {ts_yet[0]} ile {ts_yet[2]} yetkili oturum", "kaynak": "dc", "ton": "bilgi"},
            {"gun": "2026-09-17", "saat": "08:40", "baslik": "6 yeni istasyondan ilk doğrulama", "ayrinti": "Hesap 9 istasyondan doğruladı", "kaynak": "dc", "ton": "uyari"},
            {"gun": "2026-09-17", "saat": "11:15", "baslik": "3 yeni iç ağa ulaşım", "ayrinti": "10.60.67.0/24, 10.71.24.0/24 ve 10.82.90.0/24, izinli", "kaynak": "fw", "ton": "kritik"},
            {"gun": "2026-09-18", "saat": "", "baslik": "İstasyon sayısı taban düzeyine döndü", "ayrinti": "3 istasyon", "kaynak": "dc", "ton": "bilgi"}],
        "graf": {"tur": "kisi", "kisiler": [{"ad": "tsahin", "ad_soyad": "Tolga Şahin", "alt": "Altyapı ve Sistem Yönetimi", "ag": ag4, "ozet": ag_ozet(ag4)}],
                 "grup": {"ad": "Altyapı ve Sistem Yönetimi", "uye": 12}}})

    # ==================================================================
    # ORTA
    # ==================================================================
    # 5. Ag taramasi (bilgisayar)
    iid = "ag-taramasi"
    a1 = uyari(iid, "MRDLT0912", "bilgisayar", "Ağ taraması", "3 saatte 214 iç ağa, 37 farklı porta istek (%91 reddedildi)", "fw", "2026-09-20", 78, ["T1046", "T1018"])

    def u_fw_tarama(r, i):
        return {"src": "10.160.164.88", "dst": f"10.{r.choice([93, 60, 71])}.{r.randint(100, 230)}.{r.randint(2, 250)}", "port": r.choice([22, 23, 80, 135, 139, 443, 445, 1433, 3306, 3389, 5985, 8080]),
                "kural": "varsayilan-red", "ad_soyad": "bilinmiyor", "kullanici": "MRDLT0912", "istasyon": "MRDLT0912", "aksiyon": "drop" if i % 11 else "accept"}

    ham5 = ham_paket("fw", rng, u_fw_tarama, 12, 9_412, "uyari_005_mrdnb0912.csv", ["2026-09-20"], (9, 11))
    incelemeler.append({
        "id": iid, "tur": "tarama", "tur_ad": "Ağ taraması", "puan": 78,
        "baslik": "MRDLT0912", "alt": "bilgisayar, kişi çözümlenemedi",
        "ozet": "Bir bilgisayar 3 saatte 214 iç ağa ve 37 farklı porta istek gönderdi; isteklerin %91'i reddedildi.",
        "kart_ozet": "3 saatte 214 iç ağ ve 37 port; benzer bilgisayarlarda olağan 6 ağ",
        "uyarilar": [a1], "kaynaklar": ["fw"], "mitre": ["T1046", "T1018"], "asama": "İç keşif",
        "varliklar": [{"ad": "MRDLT0912", "tip": "bilgisayar", "alt": "kişi çözümlenemedi"}],
        "alan": [("Öncelik", "Orta"), ("Durum", "Açık"), ("Uyarı", "1"), ("Varlık", "1 bilgisayar"), ("Kim olduğu", "çözümlenemedi"),
                 ("Kaynak", "1, iç güvenlik duvarı"), ("Görülme sıklığı", "1.106 bilgisayarın 1'inde"), ("Başka açıklama", "Arandı, bulunamadı"), ("Yoğun gün", "20 Eyl")],
        "nedenler": ["Kısa sürede çok hedef", "37 farklı port", "Benzerlerinde olağan 6 ağ"],
        "metrikler": [("214", "3 saatte taranan ağ"), ("6", "benzerlerinde olağan"), ("37", "farklı port")],
        "adimlar": [("Bilgisayarın kullanıcısı", "MRDLT0912 zimmet kaydı", "Sistem ekibi"), ("İstekleri gönderen program", "uç nokta kaydı", "Uç nokta koruması sahibi")],
        "eksik": [("Bilgisayarın kullanıcısı", "Bilgisayar için oturum kaydı ve zimmet bilgisi", "Sistem ekibi"),
                  ("İstekleri gönderen program", "Aynı saatlerde bilgisayarda çalışan süreç kaydı", "Uç nokta koruması sahibi")],
        "lehine": ["kısa sürede çok hedef", "port çeşitliliği yüksek"], "aleyhine": ["yetkili zafiyet taraması olabilir"],
        "kanit": [{"baslik": "Tarama özeti", "kolon": ["Ölçü", "Bu bilgisayar", "Benzer bilgisayarlarda ortanca", "Tüm bilgisayarlar, ortanca"], "sayisal": [1, 2, 3],
                   "satir": [["Farklı hedef ağ", "214", "6", "4"], ["Farklı port", "37", "3", "3"], ["Reddedilen pay", "%91", "%12", "%9"], ["Süre", "3 saat", "-", "-"]]}],
        "ham": ham5, "yogun_gun": "2026-09-20",
        "zaman": [{"gun": "2026-09-20", "saat": "09:02", "baslik": "Tarama başladı", "ayrinti": "10.160.164.88 adresinden; ilk 30 dakikada 71 ağ", "kaynak": "fw", "ton": "uyari"},
                  {"gun": "2026-09-20", "saat": "11:58", "baslik": "Tarama sona erdi", "ayrinti": "Toplam 9.412 bağlantı denemesi, 214 ağ", "kaynak": "fw", "ton": "kritik"}],
        "graf": None})

    # 6. EDR saldiri araci
    iid = "saldiri-araci"
    e1 = uyari(iid, "ugunes", "kisi", "Uç noktada saldırı aracı", "İndirilenler klasöründe saldırı aracı arşivi tespit edildi: impacket-master.zip", "edr", "2026-09-16", 82, ["T1105"])

    def u_edr(r, i):
        return {"olay": "Suspicious File Detected", "makine": "MRDLT0207", "kullanici": "ugunes", "dosya": "impacket-master.zip",
                "yol": "C:\\Users\\ugunes\\Downloads", "aksiyon": "Deny", "kategori": "Known Attack Tool"}

    ham6 = ham_paket("edr", rng, u_edr, 1, 1, "uyari_006_ugunes.csv", ["2026-09-16"], (14, 14))
    incelemeler.append({
        "id": iid, "tur": "arac", "tur_ad": "Uç nokta", "puan": 82,
        "baslik": "Umut Güneş", "alt": "MRDLT0207, uç noktada saldırı aracı",
        "ozet": "Bir bilgisayarın İndirilenler klasöründe bilinen saldırı aracı arşivi tespit edildi ve engellendi.",
        "kart_ozet": "impacket-master.zip, uç nokta koruması engelledi",
        "uyarilar": [e1], "kaynaklar": ["edr"], "mitre": ["T1105"], "asama": "Komuta ve kontrol",
        "varliklar": [{"ad": "ugunes", "tip": "kisi", "alt": "Umut Güneş, Bilgi Güvenliği"}, {"ad": "MRDLT0207", "tip": "bilgisayar", "alt": "dizüstü"}],
        "alan": [("Öncelik", "Orta"), ("Durum", "Açık"), ("Uyarı", "1"), ("Varlık", "1 kişi, 1 bilgisayar"), ("Kim olduğu", "uç nokta kaydı"),
                 ("Kaynak", "1, uç nokta koruması"), ("Görülme sıklığı", "1 bilgisayar"), ("Başka açıklama", "Sorulmadı"), ("Yoğun gün", "16 Eyl")],
        "nedenler": ["Bilinen saldırı aracı", "Engellendi", "Tek kaynak"],
        "metrikler": [("1", "tespit"), ("Engellendi", "uç nokta aksiyonu"), ("1", "kaynak")],
        "adimlar": [("Aracın kullanım amacı", "Bilgi Güvenliği ekibinin test görevi kaydı", "Bilgi Güvenliği")],
        "eksik": [("Aracın kullanım amacı", "Kullanıcının rolü ve görev kaydı", "Bilgi Güvenliği")],
        "lehine": ["bilinen saldırı aracı adı"], "aleyhine": ["kullanıcı güvenlik uzmanı, test amaçlı olabilir"],
        "kanit": [{"baslik": "Uç nokta olayı", "kolon": ["Gün", "Bilgisayar", "Dosya", "Konum", "Aksiyon"], "sayisal": [],
                   "satir": [["16 Eyl 14:22", "MRDLT0207", "impacket-master.zip", "C:\\Users\\ugunes\\Downloads", "Engellendi"]]}],
        "ham": ham6, "yogun_gun": "2026-09-16",
        "zaman": [{"gun": "2026-09-16", "saat": "14:22", "baslik": "Arşiv indirildi ve tespit edildi", "ayrinti": "Uç nokta koruması dosyayı engelledi", "kaynak": "edr", "ton": "uyari"}],
        "graf": None})

    # 7. Uygulama Gelistirme (kume)
    iid = "uygulama-gelistirme"
    dk_uyeler = dk_kisileri[:8]
    dk_say = [23, 18, 15, 12, 10, 8, 6, 5]
    NB = len(dk_uyeler)
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
        dk_uyari.append(uyari(iid, k, "kisi", "Grup davranışı", f"{n} iç ağa istek gönderdi, hiçbiri geçmedi (grupta olağan {OLAGAN_B})", "vpn", gun, 74, ["T1046", "T1018"]))
        dk_gun[k] = {"istek": paylastir(istek + normal_istek, agirlik), "engel": engel_gun}
        dk_graf.append({"ad": k, "ad_soyad": KISI[k]["ad_soyad"], "alt": KISI[k]["unvan"], "ag": ag, "ozet": ag_ozet(ag), "engel_istek": istek - ge})
        dk_satir.append([k, KISI[k]["ad_soyad"], KISI[k]["unvan"], str(n), str(OLAGAN_B), "0", sayi(istek), gun_et(gun)])
    dk_top_gun = [sum(dk_gun[k]["engel"][i] for k in dk_uyeler) for i in range(7)]
    dk_zaman = [
        {"gun": GUNLER[2], "saat": "", "baslik": "İlk engellenen istekler", "ayrinti": f"{NB} kişiden toplam {sayi(dk_top_gun[2])} engellenen istek", "kaynak": "vpn", "ton": "bilgi"},
        {"gun": GUNLER[3], "saat": "", "baslik": "En yoğun gün", "ayrinti": f"{sayi(dk_top_gun[3])} engellenen istek, {min(NB, 5)} kişi için en yoğun gün", "kaynak": "vpn", "ton": "uyari"},
        {"gun": GUNLER[4], "saat": "", "baslik": f"Kalan {NB - min(NB, 5)} kişi için en yoğun gün", "ayrinti": f"{sayi(dk_top_gun[4])} engellenen istek", "kaynak": "vpn", "ton": "uyari"}]

    def u_vpn_dk(r, i):
        k = dk_uyeler[i % NB]
        return {"src": f"10.249.{[90, 127][i % 2]}.{40 + i}", "dst": f"10.{r.choice([137, 124, 212, 206])}.{r.randint(1, 254)}.{r.randint(2, 250)}", "kullanici": k,
                "port": r.choice([443, 8443, 8080, 22]), "aksiyon": "deny", "kural": "varsayilan-red"}

    ham7 = ham_paket("vpn", rng, u_vpn_dk, 12, dk_top, "uyari_007_uygulama_gelistirme.csv", ["2026-09-17", "2026-09-18"], (9, 18))
    incelemeler.append({
        "id": iid, "tur": "kume", "tur_ad": "Grup davranışı", "puan": 74,
        "baslik": "Uygulama Geliştirme", "alt": f"{NB} / {GRUP_B} kişi, engellenen iç ağ istekleri",
        "ozet": f"Grup içinde {NB} kişilik alt küme: engellenen ağ sayısı {min(dk_say)} ile {max(dk_say)} arasında, grupta olağan {OLAGAN_B}; ulaşılan ağ yok.",
        "kart_ozet": f"{GRUP_B} kişilik gruptan {NB}'i {min(dk_say)} ile {max(dk_say)} arasında iç ağa istek gönderdi, hiçbiri geçmedi",
        "uyarilar": dk_uyari, "kaynaklar": ["vpn"], "mitre": ["T1046", "T1018"], "asama": "İç keşif",
        "varliklar": [{"ad": k, "tip": "kisi", "alt": KISI[k]["ad_soyad"]} for k in dk_uyeler],
        "alan": [("Öncelik", "Orta"), ("Durum", "Açık"), ("Uyarı", str(NB)), ("Varlık", f"{NB} kişi"), ("Kim olduğu", "VPN oturumundan"),
                 ("Kaynak", "1, VPN günlükleri"), ("Görülme sıklığı", f"{GRUP_B} kişinin {NB}'inde"), ("Başka açıklama", "Sorulmadı"), ("Yoğun gün", "17 Eyl")],
        "nedenler": [f"Grupta olağanın {min(dk_say) // OLAGAN_B} ile {max(dk_say) // OLAGAN_B} katı", f"Aynı birimde {NB} kişi", "Hiçbir istek geçmedi"],
        "metrikler": [(f"{min(dk_say)}-{max(dk_say)}", "engellenen ağ"), (str(OLAGAN_B), "grupta olağan"), ("0", "ulaşılan yeni ağ")],
        "adimlar": [(f"{NB} bilgisayarın ortak noktası", "test ortamı erişimi, istemci sürümü", "Sistem ekibi"), ("Hedeflerin durumu", "kaldırılmış test aralıkları", "Ağ ekibi")],
        "eksik": [("İstekleri gönderen program", "Bu dönemde uç nokta kaydı yok", "Uç nokta koruması sahibi"), ("Test ortamı aralıkları", "Hedef ağların envanter kaydı", "Ağ ekibi")],
        "lehine": ["grupta olağanın üzerinde", "birden çok kişide aynı desen"], "aleyhine": ["test ortamları kaldırılmış olabilir", "hiçbir istek geçmedi"],
        "kanit": [{"baslik": "Kişiler", "kolon": ["Kullanıcı", "Ad", "Unvan", "Engellenen ağ", "Grupta olağan", "Ulaşılan yeni ağ", "Engellenen istek", "Yoğun gün"], "sayisal": [3, 4, 5, 6], "satir": dk_satir}],
        "ham": ham7, "yogun_gun": "2026-09-17",
        "zaman": dk_zaman,
        "graf": {"tur": "grup", "kisiler": dk_graf, "grup": {"ad": "Uygulama Geliştirme", "uye": GRUP_B}}})

    # 8. Dis tarama (iki blok)
    iid = "dis-tarama"
    w1 = uyari(iid, "203.0.113.0/24", "adres", "Dış web taraması", "27 adres 5 gündür web uygulamalarına saldırı imzası gönderiyor", "gecit", "2026-09-18", 66, ["T1595", "T1190"])
    w2 = uyari(iid, "198.51.100.0/24", "adres", "Dış web taraması", "14 adres 3 gündür aynı hedeflere imzalı istek gönderiyor", "gecit", "2026-09-17", 62, ["T1595", "T1190"])

    def u_waf(r, i):
        blok = "203.0.113" if i % 3 else "198.51.100"
        return {"src": f"{blok}.{r.randint(2, 250)}", "imza": r.choice(["sql_injection", "cross_site_scripting", "field_consistency", "signature_match"]),
                "aciklama": "Signature violation", "url": r.choice(["http://kampanya.mrd.local/giris.aspx", "http://mrd-web.mrd.local/api/arama", "http://sube.mrd.local/login"]),
                "sonuc": r.choice(["blocked", "blocked", "not blocked"])}

    ham8 = ham_paket("waf", rng, u_waf, 12, 3_035, "uyari_008_dis_tarama.csv", GUNLER[2:], (0, 23))
    incelemeler.append({
        "id": iid, "tur": "dis_tarama", "tur_ad": "Dış tarama", "puan": 66,
        "baslik": "2 dış adres bloğu", "alt": "web uygulamalarına saldırı imzası gönderiyor",
        "ozet": "İnternetten iki adres bloğu, birden çok gündür web uygulamalarına saldırı imzalı istek gönderiyor; isteklerin %74'ü engellendi.",
        "kart_ozet": "41 dış adres, 3.035 imzalı istek; %74'ü uygulama geçidinde engellendi",
        "uyarilar": [w1, w2], "kaynaklar": ["gecit"], "mitre": ["T1595", "T1190"], "asama": "Keşif",
        "varliklar": [{"ad": "203.0.113.0/24", "tip": "adres", "alt": "27 adres"}, {"ad": "198.51.100.0/24", "tip": "adres", "alt": "14 adres"}],
        "alan": [("Öncelik", "Orta"), ("Durum", "Açık"), ("Uyarı", "2"), ("Varlık", "2 dış adres bloğu"), ("Kim olduğu", "kaynak adres"),
                 ("Kaynak", "1, uygulama geçidi"), ("Görülme sıklığı", "7.406 dış bloğun 2'sinde"), ("Başka açıklama", "Sorulmadı"), ("Yoğun gün", "18 Eyl")],
        "nedenler": ["Birden çok gün", "Birden çok imza sınıfı", "Aynı hedeflere yoğunlaşma"],
        "metrikler": [("41", "dış adres"), ("3.035", "imzalı istek"), ("%74", "engellenen")],
        "adimlar": [("Denetimli test kaydı", "bu bloklar için yetkili test ya da tarama kaydı", "Bilgi Güvenliği")],
        "eksik": [("Bloğun sahibi", "Adres bloklarının kime ait olduğu ve yetkili test kaydı", "Bilgi Güvenliği")],
        "lehine": ["birden çok imza sınıfı", "birden çok gün"], "aleyhine": ["denetimli sızma testi olabilir", "izleme hizmeti olabilir"],
        "kanit": [{"baslik": "Bloklar", "kolon": ["Blok", "Adres", "İmzalı istek", "İmza sınıfı", "Engellenen pay", "Gün"], "sayisal": [1, 2, 3, 4, 5],
                   "satir": [["203.0.113.0/24", "27", "1.908", "4", "%81", "5"], ["198.51.100.0/24", "14", "1.127", "3", "%63", "3"]]},
                  {"baslik": "Hedef uygulamalar", "kolon": ["Uygulama adresi", "İstek", "Pay"], "sayisal": [1, 2],
                   "satir": [["kampanya.mrd.local", "1.366", "%45,0"], ["sube.mrd.local", "1.002", "%33,0"], ["mrd-web.mrd.local", "667", "%22,0"]]}],
        "ham": ham8, "yogun_gun": "2026-09-18",
        "zaman": [{"gun": "2026-09-15", "saat": "", "baslik": "203.0.113.0/24 ilk imza", "ayrinti": "3 adres", "kaynak": "gecit", "ton": "bilgi"},
                  {"gun": "2026-09-18", "saat": "", "baslik": "Yoğun gün", "ayrinti": "742 imzalı istek, 19 adres", "kaynak": "gecit", "ton": "uyari"},
                  {"gun": "2026-09-17", "saat": "", "baslik": "198.51.100.0/24 ilk imza", "ayrinti": "14 adres", "kaynak": "gecit", "ton": "uyari"}],
        "graf": None})

    # 9. ecetin yeni ic ag
    iid = "yeni-ag-ecetin"
    ag9 = ag_listesi(rng, normal=["10.160.127.0/24"], yalniz=["10.93.191.0/24"], engel=["10.60.89.0/24"], rastgele_engel=1, istek_araligi=(10, 90), gunler=GUNLER[2:5])
    ec_yeni = sum(x["istek"] for x in ag9 if x["sinif"] != "normal")
    ec_engel = sum(x["istek"] for x in ag9 if x["sinif"] == "engel")
    e9 = uyari(iid, ecetin, "kisi", "Yeni iç ağa gidiş", "3 yeni iç ağ, 1'ine ulaştı, 2'sine istek engellendi", "vpn", "2026-09-19", 61, ["T1018"])
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
                 ("Görülme sıklığı", "436 kullanıcının 17'sinde"), ("Başka açıklama", "Sorulmadı"), ("Yoğun gün", "19 Eyl")],
        "nedenler": ["3 yeni iç ağ", "Kendi birimine göre alışılmadık"], "metrikler": [("3", "yeni iç ağ"), ("1", "ulaşıldı"), ("2", "engellendi")],
        "adimlar": [("Ağ erişim talebi", "10.93.191.0/24 için açık erişim talebi", "Ağ ekibi")],
        "eksik": [("Erişim talebi", "10.93.191.0/24 için erişim talebi ya da görev kaydı", "Ağ ekibi")],
        "lehine": ["dönemde ilk kez gidilen ağlar"], "aleyhine": ["yeni görev ya da proje olabilir", "nüfusun %4'ünde görülen bir davranış"],
        "kanit": [{"baslik": "Ağlar", "kolon": ["Ağ", "Ağ tanımı", "Sonuç", "İstek", "İlk görülme"], "sayisal": [3],
                   "satir": [[x["cidr"], x["ad"] or "kayıtlarda tanımlı değil", "Ulaşıldı" if x["gecen"] else "Engellendi", sayi(x["istek"]), gun_et(x["gun"])] for x in ag9 if x["sinif"] != "normal"]}],
        "ham": ham9, "yogun_gun": "2026-09-19",
        "zaman": [{"gun": "2026-09-19", "saat": "10:14", "baslik": "Yeni iç ağlara ilk istek", "ayrinti": "10.93.191.0/24 ulaşıldı; 2 ağ engellendi", "kaynak": "vpn", "ton": "uyari"}],
        "graf": {"tur": "kisi", "kisiler": [{"ad": "ecetin", "ad_soyad": "Elif Çetin", "alt": "Mali İşler", "ag": ag9, "ozet": ag_ozet(ag9)}], "grup": {"ad": "Mali İşler", "uye": 24}}})

    # 10. mdemir surekli engel
    iid = "surekli-engel-mdemir"
    ag10 = ag_listesi(rng, normal=["10.160.127.0/24"], engel=["10.93.191.0/24"], istek_araligi=(80, 260), gunler=GUNLER[1:5])
    for x in ag10:
        if x["sinif"] == "engel":
            x["istek"] = 152
    e10 = uyari(iid, mdemir, "kisi", "Sürekli engellenen istek", "4 gündür aynı iç ağa engelleniyor, günde ortalama 38 reddedilen istek", "vpn", "2026-09-19", 72, ["T1046"])
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
                 ("Görülme sıklığı", "436 kullanıcının 9'unda"), ("Başka açıklama", "Arandı, bulunamadı"), ("Yoğun gün", "17 Eyl")],
        "nedenler": ["4 gün süreklilik", "Aynı ağa tekrarlayan ret"], "metrikler": [("152", "reddedilen istek"), ("4", "gün"), ("0", "geçen istek")],
        "adimlar": [("Hedef ağın durumu", "10.93.191.0/24 için kullanıcının erişim beklentisi", "Ağ ekibi")],
        "eksik": [("Erişim beklentisi", "Kullanıcının bu ağa erişmesi gereken bir görev olup olmadığı", "Kredi Operasyonları yöneticisi")],
        "lehine": ["tekrarlayan ret"], "aleyhine": ["yapılandırma hatası olabilir", "kaldırılmış bir kaynağa ayarlanmış istemci olabilir"],
        "kanit": [{"baslik": "Günlük dağılım", "kolon": ["Gün", "İstek", "Reddedilen", "Geçen"], "sayisal": [1, 2, 3],
                   "satir": [["16 Eyl", "36", "36", "0"], ["17 Eyl", "41", "41", "0"], ["18 Eyl", "39", "39", "0"], ["19 Eyl", "36", "36", "0"]]}],
        "ham": ham10, "yogun_gun": "2026-09-17",
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
    o1 = uyari(iid, "kampanya-eski.mrd.local", "servis", "Ölü adres çağrısı", "Adres artık yok (404) ama hâlâ çağrılıyor: 11.482 istek", "gecit", "2026-09-14", 52)
    o2 = uyari(iid, "eposta-onay.mrd.local", "servis", "Ölü adres çağrısı", "Adres artık yok (404) ama hâlâ çağrılıyor: 6.204 istek", "gecit", "2026-09-14", 50)
    ham11 = ham_paket("gecit", rng, lambda r, i: {"src": f"10.82.239.{30 + i % 4}", "dst": "10.60.241.21", "host": "kampanya-eski.mrd.local" if i % 2 else "eposta-onay.mrd.local",
                                                  "yol": "/v1/ilan/liste" if i % 2 else "/onay/tetikle", "durum": 404}, 12, 17686, "uyari_011_olu_adres.csv", GUNLER, (0, 23))
    kucuk(iid, "olu", "Ölü adres", 52, "2 adres artık yok", "hâlâ çağrılmaya devam ediyor",
          "İki uygulama adresi 404 döndürüyor ama istekler kesilmemiş; çağıran uygulama ayarı güncellenmemiş olabilir.", "2 adres 404 döndürüyor, çağrılar sürüyor",
          [o1, o2], ["gecit"], [], [{"ad": "kampanya-eski.mrd.local", "tip": "servis", "alt": "/v1/ilan/liste"}, {"ad": "eposta-onay.mrd.local", "tip": "servis", "alt": "/onay/tetikle"}],
          [("Öncelik", "Düşük"), ("Durum", "Açık"), ("Uyarı", "2"), ("Varlık", "2 servis"), ("Kim olduğu", "uygulama geçidi kaydı"), ("Kaynak", "1, uygulama geçidi"),
           ("Görülme sıklığı", "274 servisin 2'sinde"), ("Başka açıklama", "Arandı, bulunamadı"), ("Yoğun gün", "Her gün")],
          [("17.686", "istek"), ("404", "baskın kod"), ("2", "servis")],
          [("Çağıran uygulama", "hangi uygulama bu adresleri çağırıyor", "Uygulama sahipleri")],
          [("Çağıran uygulama", "Bu adreslere istek gönderen uygulamanın kaydı", "Uygulama sahipleri")],
          [{"baslik": "Adresler", "kolon": ["Adres", "Yol", "Kod", "İstek"], "sayisal": [3], "satir": [["kampanya-eski.mrd.local", "/v1/ilan/liste", "404", "11.482"], ["eposta-onay.mrd.local", "/onay/tetikle", "404", "6.204"]]}],
          ham11, None, [{"gun": GUNLER[i], "saat": "", "baslik": "İstekler sürüyor", "ayrinti": "404 yanıtları", "kaynak": "gecit", "ton": "bilgi"} for i in (0, 3, 6)])

    # 12. yoklama
    iid = "yoklama"
    YOKLAMA = [("belge-onay.mrd.local", 404), ("bayi-portal.mrd.local", 405), ("toplu-islem.mrd.local", 404), ("kampanya-yonetim.mrd.local", 404)]
    y_list = [uyari(iid, h, "servis", "Yoklama hatası", f"Durum adresine iki dakikada bir istek, sürekli {kd}", "gecit", "2026-09-14", 48 - n)
              for n, (h, kd) in enumerate(YOKLAMA)]
    ham12 = ham_paket("gecit", rng, lambda r, i: {"src": "10.82.97.11", "dst": "10.60.241.24", "host": YOKLAMA[i % 4][0],
                                                  "yol": "/status", "durum": YOKLAMA[i % 4][1]}, 12, 5040 * len(YOKLAMA), "uyari_012_yoklama.csv", GUNLER, (0, 23))
    kucuk(iid, "yoklama", "Yoklama hatası", 48, f"{len(YOKLAMA)} yoklama yanlış adrese gidiyor", "iki dakikada bir durum adresi, sürekli hata",
          f"{len(YOKLAMA)} servis için izleme durum adresine istek gönderiyor ve sürekli hata alıyor; izleme ayarı yanlış adrese bakıyor olabilir.",
          f"{len(YOKLAMA)} servis için durum adresine yoklama, sürekli 4xx",
          y_list, ["gecit"], [], [{"ad": h, "tip": "servis", "alt": "/status"} for h, _ in YOKLAMA],
          [("Öncelik", "Düşük"), ("Durum", "Açık"), ("Uyarı", str(len(YOKLAMA))), ("Varlık", f"{len(YOKLAMA)} servis"), ("Kim olduğu", "uygulama geçidi kaydı"), ("Kaynak", "1, uygulama geçidi"),
           ("Görülme sıklığı", f"274 servisin {len(YOKLAMA)}'ünde"), ("Başka açıklama", "Arandı, bulunamadı"), ("Yoğun gün", "Her gün")],
          [(sayi(5040 * len(YOKLAMA)), "yoklama"), ("2", "dakika aralık"), (str(len(YOKLAMA)), "servis")],
          [("İzleme adreslerinin düzeltilmesi", f"{len(YOKLAMA)} servis için sağlık kontrolü adresi", "İzleme ekibi")],
          [("İzleme tanımı", f"{len(YOKLAMA)} servis için tanımlı sağlık kontrolü adresi", "İzleme ekibi")],
          [{"baslik": "Servisler", "kolon": ["Adres", "Yol", "Baskın kod", "İstek"], "sayisal": [3], "satir": [[h, "/status", str(kd), sayi(5040)] for h, kd in YOKLAMA]}],
          ham12, None, [{"gun": GUNLER[i], "saat": "", "baslik": "İki dakikada bir yoklama", "ayrinti": "404 ve 405 yanıtları", "kaynak": "gecit", "ton": "bilgi"} for i in (0, 3, 6)])

    # 13. test ortami
    iid = "test-ortami"
    t_uyari = [uyari(iid, h, "servis", "Servis arızası", "Test ortamında hafta boyu hata döndü", "gecit", "2026-09-20", 40) for h in ("portal-test.mrd.local", "entegrasyon-uat.mrd.local", "kart-test.mrd.local")]
    ham13 = ham_paket("gecit", rng, lambda r, i: {"src": "10.82.211.9", "dst": "10.60.73.14", "host": ["portal-test.mrd.local", "entegrasyon-uat.mrd.local", "kart-test.mrd.local"][i % 3],
                                                  "yol": "/api/v1/islem", "durum": 502}, 12, 8_411, "uyari_013_test_ortami.csv", GUNLER, (0, 23))
    kucuk(iid, "tema_test", "Test ortamı", 40, "Test ortamında 3 adres hata alıyor", "üretimden ayrı değerlendirilir",
          "Test ortamındaki adreslerde sunucu ve istemci hataları var; üretimle ayrı değerlendirilir.", "Test ortamında 3 adres hata alıyor",
          t_uyari, ["gecit"], [], [{"ad": h, "tip": "servis", "alt": "test ortamı"} for h in ("portal-test.mrd.local", "entegrasyon-uat.mrd.local", "kart-test.mrd.local")],
          [("Öncelik", "Düşük"), ("Durum", "Açık"), ("Uyarı", "3"), ("Varlık", "3 servis"), ("Kim olduğu", "uygulama geçidi kaydı"), ("Kaynak", "1, uygulama geçidi"),
           ("Görülme sıklığı", "41 test adresinin 3'ünde"), ("Başka açıklama", "Arandı, bulunamadı"), ("Yoğun gün", "20 Eyl")],
          [("8.411", "hata"), ("502", "baskın kod"), ("3", "servis")],
          [("Test ortamı sahipleri", "3 servis için sorumlu ekip", "Uygulama sahipleri")],
          [("Servis sahibi", "Test ortamı adresleri için sorumlu kaydı", "Envanter yöneticisi")],
          [{"baslik": "Servisler", "kolon": ["Adres", "Ortam", "Baskın kod", "İstek"], "sayisal": [3],
            "satir": [["portal-test.mrd.local", "Test", "502", "3.211"], ["entegrasyon-uat.mrd.local", "Test", "502", "2.906"], ["kart-test.mrd.local", "Test", "502", "2.294"]]}],
          ham13, None, [{"gun": "2026-09-20", "saat": "", "baslik": "Hata oranı arttı", "ayrinti": "3 servis", "kaynak": "gecit", "ton": "bilgi"}])

    # 14. bkoc
    iid = "yeni-ag-bkoc"
    ag14 = ag_listesi(rng, normal=["10.160.127.0/24"], engel=["10.60.89.0/24"], istek_araligi=(8, 50), gunler=GUNLER[3:5])
    for x in ag14:
        if x["sinif"] == "engel":
            x["istek"] = 26
    b14 = uyari(iid, bkoc, "kisi", "Yeni iç ağa gidiş", "1 yeni iç ağa istek gönderdi, engellendi", "vpn", "2026-09-19", 57, ["T1018"])
    ham14 = ham_paket("vpn", rng, lambda r, i: {"src": "10.249.90.12", "dst": "10.60.89.14", "kullanici": "bkoc", "port": 22, "aksiyon": "deny"}, 6, 26, "uyari_014_bkoc.csv", GUNLER[4:6], (10, 16))
    kucuk(iid, "kisi", "Yeni iç ağ", 57, "Burcu Koç", "İç Denetim, yeni iç ağa gidiş",
          "Hesap dönemde ilk kez bir yönetim ağına istek gönderdi; istek engellendi.", "1 yeni iç ağ, istek engellendi",
          [b14], ["vpn"], ["T1018"], [{"ad": "bkoc", "tip": "kisi", "alt": "Burcu Koç, İç Denetim"}],
          [("Öncelik", "Düşük"), ("Durum", "Açık"), ("Uyarı", "1"), ("Varlık", "1 kişi"), ("Kim olduğu", "VPN oturumundan"), ("Kaynak", "1, VPN günlükleri"),
           ("Görülme sıklığı", "436 kullanıcının 17'sinde"), ("Başka açıklama", "Sorulmadı"), ("Yoğun gün", "19 Eyl")],
          [("1", "yeni iç ağ"), ("0", "ulaşıldı"), ("26", "engellenen istek")],
          [("Denetim görevi kaydı", "yönetim ağına erişimi gerektiren denetim görevi", "İç Denetim")],
          [("Görev kaydı", "İç denetim çalışması için yönetim ağı erişim gerekçesi", "İç Denetim")],
          [{"baslik": "Ağlar", "kolon": ["Ağ", "Ağ tanımı", "Sonuç", "İstek"], "sayisal": [3], "satir": [["10.60.89.0/24", "Yönetim ağı", "Engellendi", "26"]]}],
          ham14, "2026-09-19", [{"gun": "2026-09-19", "saat": "14:03", "baslik": "Yönetim ağına istek", "ayrinti": "10.60.89.0/24, engellendi", "kaynak": "vpn", "ton": "bilgi"}])
    incelemeler[-1]["graf"] = {"tur": "kisi", "kisiler": [{"ad": "bkoc", "ad_soyad": "Burcu Koç", "alt": "İç Denetim", "ag": ag14, "ozet": ag_ozet(ag14)}], "grup": {"ad": "İç Denetim", "uye": 9}}

    # 15. sguler
    iid = "surekli-engel-sguler"
    ag15 = ag_listesi(rng, normal=["10.160.127.0/24"], engel=["10.93.24.0/24"], istek_araligi=(10, 60), gunler=GUNLER[2:5])
    for x in ag15:
        if x["sinif"] == "engel":
            x["istek"] = 36
    s15 = uyari(iid, sguler, "kisi", "Sürekli engellenen istek", "3 gündür aynı iç ağa engelleniyor, günde ortalama 12 reddedilen istek", "vpn", "2026-09-19", 55, ["T1046"])
    ham15 = ham_paket("vpn", rng, lambda r, i: {"src": "10.249.16.90", "dst": f"10.93.24.{r.randint(10, 50)}", "kullanici": "sguler", "port": r.choice([1433, 8443]), "aksiyon": "deny"}, 8, 36, "uyari_015_sguler.csv", GUNLER[3:6], (9, 17))
    kucuk(iid, "kisi", "Sürekli engelleme", 55, "Sinan Güler", "Uyum, sürekli engellenen istek",
          "Hesap 3 gündür aynı iç ağa istek gönderiyor ve her seferinde engelleniyor.", "3 gündür aynı ağa istek, günde ortalama 12 ret",
          [s15], ["vpn"], ["T1046"], [{"ad": "sguler", "tip": "kisi", "alt": "Sinan Güler, Uyum"}],
          [("Öncelik", "Düşük"), ("Durum", "Açık"), ("Uyarı", "1"), ("Varlık", "1 kişi"), ("Kim olduğu", "VPN oturumundan"), ("Kaynak", "1, VPN günlükleri"),
           ("Görülme sıklığı", "436 kullanıcının 9'unda"), ("Başka açıklama", "Arandı, bulunamadı"), ("Yoğun gün", "18 Eyl")],
          [("36", "reddedilen istek"), ("3", "gün"), ("0", "geçen istek")],
          [("Erişim beklentisi", "kullanıcının bu ağa erişmesi gereken görev", "Uyum yöneticisi")],
          [("Erişim beklentisi", "Kullanıcının bu ağa erişmesi gereken bir görev olup olmadığı", "Uyum yöneticisi")],
          [{"baslik": "Günlük dağılım", "kolon": ["Gün", "İstek", "Reddedilen", "Geçen"], "sayisal": [1, 2, 3], "satir": [["17 Eyl", "11", "11", "0"], ["18 Eyl", "13", "13", "0"], ["19 Eyl", "12", "12", "0"]]}],
          ham15, "2026-09-18", [{"gun": g, "saat": "", "baslik": "Aynı ağa reddedilen istekler", "ayrinti": "10.93.24.0/24", "kaynak": "vpn", "ton": "bilgi"} for g in GUNLER[3:6]])
    incelemeler[-1]["graf"] = {"tur": "kisi", "kisiler": [{"ad": "sguler", "ad_soyad": "Sinan Güler", "alt": "Uyum", "ag": ag15, "ozet": ag_ozet(ag15)}], "grup": {"ad": "Uyum", "uye": 14}}

    # 16. tek dis blok
    iid = "dis-blok-tekil"
    d16 = uyari(iid, "192.0.2.0/24", "adres", "Dış web taraması", "6 adres 2 gündür imzalı istek gönderiyor", "gecit", "2026-09-19", 44, ["T1595"])
    ham16 = ham_paket("waf", rng, lambda r, i: {"src": f"192.0.2.{r.randint(2, 250)}", "imza": "signature_match", "aciklama": "Signature violation",
                                                 "url": "http://mrd-web.mrd.local/api/arama", "sonuc": "blocked"}, 8, 143, "uyari_016_dis_blok.csv", GUNLER[5:], (2, 6))
    kucuk(iid, "dis_tarama", "Dış tarama", 44, "192.0.2.0/24", "dış adres bloğu, imzalı istek",
          "İnternetten bir adres bloğu 2 gündür imzalı istek gönderiyor; istekler uygulama geçidinde engellendi.", "6 adres, 143 imzalı istek",
          [d16], ["gecit"], ["T1595"], [{"ad": "192.0.2.0/24", "tip": "adres", "alt": "6 adres"}],
          [("Öncelik", "Düşük"), ("Durum", "Açık"), ("Uyarı", "1"), ("Varlık", "1 dış adres bloğu"), ("Kim olduğu", "kaynak adres"), ("Kaynak", "1, uygulama geçidi"),
           ("Görülme sıklığı", "7.406 dış bloğun 1'inde"), ("Başka açıklama", "Sorulmadı"), ("Yoğun gün", "20 Eyl")],
          [("143", "imzalı istek"), ("6", "dış adres"), ("%100", "engellenen")],
          [("Bloğun sahibi", "adres bloğunun sahibi ve test kaydı", "Bilgi Güvenliği")],
          [("Bloğun sahibi", "Adres bloğunun kime ait olduğu", "Bilgi Güvenliği")],
          [{"baslik": "Blok", "kolon": ["Blok", "Adres", "İmzalı istek", "İmza sınıfı", "Engellenen pay"], "sayisal": [1, 2, 3, 4], "satir": [["192.0.2.0/24", "6", "143", "1", "%100"]]}],
          ham16, "2026-09-20", [{"gun": "2026-09-19", "saat": "", "baslik": "İlk imzalı istek", "ayrinti": "3 adres", "kaynak": "gecit", "ton": "bilgi"}, {"gun": "2026-09-20", "saat": "", "baslik": "6 adres", "ayrinti": "143 istek", "kaynak": "gecit", "ton": "bilgi"}])

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
          {1: [("ag", "10.249.53.0/24 kaynak ağ", "bilgi")], 2: [("bilgisayar", "MRDLT0388", "uyari")],
           3: [("ag", "10.93.24.0/24 ulaşıldı", "kritik"), ("ag", "10.93.61.0/24 ulaşıldı", "kritik"), ("ag", "10.93.101.0/24 ulaşıldı", "kritik"), ("ag", "10.60.89.0/24 engellendi", "uyari")]},
          [("kirmizi", "İşten ayrıldı, 21 Ağu; hesap etkin ve dönemde 9 oturum açmış"), ("kirmizi", "5 gece VPN oturumu, 01:10 ile 03:40 arası"),
           ("turuncu", "Ulaştığı 3 ödeme ve kart ağına birimindeki 18 kişiden hiçbiri gitmiyor"), ("turuncu", "2 yönetim ağına istek gönderdi, engellendi"), ("bilgi", "3 kaynakta iz: VPN, etki alanı, güvenlik duvarı")])
    for k, n in zip(uyeler, agsay):
        hafta(k, im_gun[k]["istek"], im_gun[k]["engel"], [0, 0, 2, 2, 2, 1, 0], [0] * 7, {2: [("ag", f"{n} iç ağ engellendi, ilk kez", "uyari")]},
              [("kirmizi", f"{n} iç ağa istek gönderdi, hiçbiri geçmedi; grupta olağan {OLAGAN_A}"), ("turuncu", f"Aynı birimden {len(uyeler) - 1} kişi benzer davranış gösteriyor"),
               ("yesil", "Ulaştığı ağların hepsi grubunun da gittiği yerler"), ("bilgi", "Kaynak: VPN günlükleri")])
    for k, n in zip(dk_uyeler, dk_say):
        hafta(k, dk_gun[k]["istek"], dk_gun[k]["engel"], [0, 0, 2, 2, 2, 0, 0], [0] * 7, {2: [("ag", f"{n} iç ağ engellendi, ilk kez", "uyari")]},
              [("turuncu", f"{n} iç ağa istek gönderdi, hiçbiri geçmedi; grupta olağan {OLAGAN_B}"), ("yesil", "Ulaştığı ağların hepsi grubunun da gittiği yerler"), ("bilgi", "Kaynak: VPN günlükleri")])
    hafta("tsahin", paylastir(sum(x["istek"] for x in ag4), [10, 12, 12, 40, 26, 0, 0]), paylastir(sum(x["istek"] for x in ag4 if x["sinif"] == "engel"), [0, 0, 20, 50, 30, 0, 0]), [x * 3 + 8 if x else 0 for x in ts_yet], ts_yet,
          {3: [("bilgisayar", "MRDSRV0141, MRDSRV0142, MRDSRV0208, MRDSRV0233, MRDLT0774, MRDLT0690", "uyari"), ("ag", "10.60.67.0/24 ulaşıldı", "kritik"), ("ag", "10.71.24.0/24 ulaşıldı", "kritik"), ("ag", "10.82.90.0/24 ulaşıldı", "kritik")]},
          [("kirmizi", "Yönetici yetkisi kullanan hesap; 17 Eylül'de 9 istasyondan doğruladı (taban 3)"), ("turuncu", "Aynı gün 3 yeni iç ağa ulaştı"), ("yesil", "18 Eylül'de istasyon sayısı taban düzeyine döndü"), ("bilgi", "Kaynak: etki alanı, güvenlik duvarı")])
    hafta("ugunes", [18, 26, 30, 22, 24, 0, 0], [0, 0, 1, 0, 0, 0, 0], [2, 2, 3, 2, 2, 0, 0], [0] * 7, {2: [("bilgisayar", "MRDLT0207 uç nokta olayı", "uyari")]},
          [("turuncu", "16 Eylül'de bilinen saldırı aracı arşivi tespit edildi ve engellendi"), ("yesil", "VPN ve oturum davranışı olağan"), ("bilgi", "Kaynak: uç nokta koruması")])
    hafta("ecetin", [22, 30, 26, 34, 28, 30 + ec_yeni, 0], [0, 0, 0, 0, 0, ec_engel, 0], [2, 2, 2, 2, 2, 3, 0], [0] * 7, {5: [("ag", "10.93.191.0/24 ulaşıldı", "uyari"), ("ag", "2 iç ağ engellendi", "uyari")]},
          [("turuncu", "19 Eylül'de 3 yeni iç ağa istek gönderdi; 1'ine ulaştı"), ("yesil", "Diğer günlerde davranışı olağan"), ("bilgi", "Kaynak: VPN günlükleri")])
    hafta("mdemir", [a + b for a, b in zip([12, 44, 60, 71, 69, 61, 0], [0, 0, 36, 41, 39, 36, 0])], [0, 0, 36, 41, 39, 36, 0], [1, 2, 2, 2, 2, 1, 0], [0] * 7, {2: [("ag", "10.93.191.0/24 engellendi, ilk kez", "uyari")]},
          [("turuncu", "4 gündür aynı iç ağa istek gönderiyor; her seferinde engellendi"), ("yesil", "Ulaştığı ağlar birimiyle aynı"), ("bilgi", "Kaynak: VPN günlükleri")])
    hafta("bkoc", [10, 14, 12, 16, 15, 30, 0], [0, 0, 0, 0, 0, 26, 0], [1, 1, 1, 1, 1, 1, 0], [0] * 7, {5: [("ag", "10.60.89.0/24 engellendi, ilk kez", "bilgi")]},
          [("turuncu", "19 Eylül'de yönetim ağına istek gönderdi; engellendi"), ("yesil", "Diğer günlerde davranışı olağan"), ("bilgi", "Kaynak: VPN günlükleri")])
    hafta("sguler", [8, 10, 11, 24, 26, 22, 0], [0, 0, 0, 11, 13, 12, 0], [1, 1, 1, 2, 2, 2, 0], [0] * 7, {3: [("ag", "10.93.24.0/24 engellendi, ilk kez", "bilgi")]},
          [("turuncu", "3 gündür aynı iç ağa istek gönderiyor; her seferinde engellendi"), ("bilgi", "Kaynak: VPN günlükleri")])

    # -------------------------------------------------- ag gecisleri (kuzey-guney, dogu-bati)
    kumeler = ["İnternet", "VPN İstemcileri", "Üçüncü Taraflar", "İnternet DMZ", "İç DMZ", "Kullanıcı Ağları", "Uygulama Sunucuları", "Ödeme ve Kart Sistemleri",
               "Veritabanı Sunucuları", "Yönetim Ağı", "Felaket Merkezi"]
    kenar = [
        ("İnternet", "İnternet DMZ", "İnternet güvenlik duvarı", 812_400_000, 41_200_000, "kuzey-güney"),
        ("İnternet", "İç DMZ", "İnternet güvenlik duvarı", 1_204, 88_410, "kuzey-güney"),
        ("İnternet", "Uygulama Sunucuları", "İnternet güvenlik duvarı", 0, 2_306_112, "kuzey-güney"),
        ("VPN İstemcileri", "Uygulama Sunucuları", "SSL VPN geçidi", 24_810_000, 3_240_000, "kuzey-güney"),
        ("VPN İstemcileri", "Kullanıcı Ağları", "SSL VPN geçidi", 6_120_000, 490_000, "kuzey-güney"),
        ("VPN İstemcileri", "Ödeme ve Kart Sistemleri", "SSL VPN geçidi", 2_140_000, 386_000, "kuzey-güney"),
        ("VPN İstemcileri", "Yönetim Ağı", "SSL VPN geçidi", 41_800, 1_912_000, "kuzey-güney"),
        ("Üçüncü Taraflar", "Ödeme ve Kart Sistemleri", "Üçüncü taraf güvenlik duvarı", 8_920_000, 12_400, "kuzey-güney"),
        ("Üçüncü Taraflar", "Uygulama Sunucuları", "Üçüncü taraf güvenlik duvarı", 3_110_000, 41_000, "kuzey-güney"),
        ("Kullanıcı Ağları", "İnternet", "İnternet güvenlik duvarı", 611_000_000, 9_800_000, "kuzey-güney"),
        ("Kullanıcı Ağları", "Uygulama Sunucuları", "İç güvenlik duvarı", 142_000_000, 1_120_000, "doğu-batı"),
        ("Kullanıcı Ağları", "Veritabanı Sunucuları", "İç güvenlik duvarı", 1_204_000, 812_000, "doğu-batı"),
        ("Kullanıcı Ağları", "Yönetim Ağı", "İç güvenlik duvarı", 302_000, 88_000, "doğu-batı"),
        ("Uygulama Sunucuları", "Veritabanı Sunucuları", "İç güvenlik duvarı", 386_000_000, 210_000, "doğu-batı"),
        ("Uygulama Sunucuları", "Ödeme ve Kart Sistemleri", "İç güvenlik duvarı", 94_000_000, 61_000, "doğu-batı"),
        ("Ödeme ve Kart Sistemleri", "Veritabanı Sunucuları", "İç güvenlik duvarı", 61_000_000, 9_400, "doğu-batı"),
        ("Yönetim Ağı", "Uygulama Sunucuları", "İç güvenlik duvarı", 24_000_000, 12_000, "doğu-batı"),
        ("Yönetim Ağı", "Veritabanı Sunucuları", "İç güvenlik duvarı", 11_400_000, 4_100, "doğu-batı"),
        ("İç DMZ", "Uygulama Sunucuları", "İç güvenlik duvarı", 48_000_000, 220_000, "doğu-batı"),
        ("İnternet DMZ", "Uygulama Sunucuları", "İç güvenlik duvarı", 212_000_000, 1_900_000, "doğu-batı"),
        ("Uygulama Sunucuları", "Felaket Merkezi", "İç güvenlik duvarı", 74_000_000, 3_100, "doğu-batı"),
        ("Veritabanı Sunucuları", "Felaket Merkezi", "İç güvenlik duvarı", 51_000_000, 2_400, "doğu-batı"),
    ]
    kenar = [{"kaynak": a, "hedef": b, "cihaz": c, "ulasan": d, "reddedilen": e, "yon": f} for (a, b, c, d, e, f) in kenar]

    ETIKET = f"{gun_et(GUNLER[0])} - {gun_et(GUNLER[-1])} 2026"
    veri_kaynaklari = [{"kod": k, "ad": v["ad"], "sistem": v["sistem"], "aralik": ETIKET, "durum": "Bağlı"} for k, v in KAYNAK.items()]
    baglam = [{"ad": "Sunucu envanteri", "ne": "Sunucuların adı, adresi, ortamı ve sahibi", "kayit": "1.460 sunucu"},
              {"ad": "Ağ topolojisi", "ne": "Ağ parçaları ve bağlantıları", "kayit": "132 ağ, 47 cihaz"},
              {"ad": "Ağ cihazları envanteri", "ne": "Güvenlik duvarı, yük dengeleyici ve anahtar kayıtları", "kayit": "118 cihaz"},
              {"ad": "Organizasyon şeması", "ne": "Kişi, birim ve bağlı olduğu yönetici", "kayit": "1.180 kişi"},
              {"ad": "Dizin hesapları", "ne": "Hesap durumu, grup üyelikleri, İK durumu", "kayit": "3.870 hesap"}]

    incelemeler.sort(key=lambda x: -x["puan"])
    return {
        "kurum": KURUM, "kurum_alt": KURUM_ALT,
        "donem": {"bas": GUNLER[0], "bit": GUNLER[-1], "etiket": ETIKET, "son_kosu": f"{gun_et(GUNLER[-1])} 2026, 08:47",
                  "kisa": f"{gun_et(GUNLER[0])} - {gun_et(GUNLER[-1])}", "son3": f"{gun_et(GUNLER[-3])} - {gun_et(GUNLER[-1])}"},
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
