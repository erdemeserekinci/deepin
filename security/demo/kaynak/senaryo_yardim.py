#!/usr/bin/env python3
"""Senaryo yazarken kullanilabilecek her seyi veriden basar: rotalar, incelemeler, graf dugumleri, kisiler,
MITRE teknikleri, asistan sorulari (hangi sozcuk hangi cevabi getirir), secici ornekleri, altyazi sayi anahtarlari.

    python3 kaynak/senaryo_yardim.py            hepsi
    python3 kaynak/senaryo_yardim.py graf       yalniz bir bolum (rota, inceleme, graf, kisi, mitre, sohbet, secici, sayi, senaryo)

Bu cikti belgeden daha gunceldir: veri ya da arayuz degisirse burasi da degisir. Senaryo yazmadan once bak.
"""
import json, os, re, sys

sys.dont_write_bytecode = True
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, "kaynak"))
import veri  # noqa: E402
import senaryo_sayilari as SS  # noqa: E402
from ceviri_js_en import TXT as TXT_EN  # noqa: E402

D = veri.uret()
JS = open(os.path.join(KOK, "kaynak", "platform.js"), encoding="utf-8").read()
SEKME = {"genel": "Genel bakış", "uyarilar": "Uyarılar", "kanit": "Kanıt", "zaman": "Zaman", "graf": "Graf", "eksik": "Eksik bilgi"}


def bolum(ad, baslik):
    istenen = sys.argv[1:] or [ad]
    if ad in istenen:
        print(f"\n## {baslik}\n")
        return True
    return False


if bolum("rota", "Rotalar (adres çubuğu, hash)"):
    print("#/                      Güncel Uyarılar (ana sayfa)")
    print("#/inc/<id>              inceleme dosyası, Genel bakış")
    print("#/inc/<id>/<sekme>      sekme: " + " ".join(SEKME))
    print("#/uyarilar              Tüm uyarılar")
    print("#/mitre                 MITRE ATT&CK")
    print("#/ag                    Ağ geçişleri (Akış, Matris)")
    print("#/kisi/<kullanici>      Kişi sorgusu (adsız #/kisi son seçilen kişiyi açar, ilk açılışta ktuncer)")
    print("#/kaynaklar             Veri kaynakları")
    print("Videoda sayfa değiştirmek için rota yerine sol raydaki düğmeye tıklamak daha doğal görünür (secici bölümüne bak).")

if bolum("inceleme", "İncelemeler (ana sayfadaki sırayla)"):
    for i in sorted(D["incelemeler"], key=lambda x: -x["puan"]):
        sek = ["genel", "uyarilar", "kanit", "zaman"] + (["graf"] if i.get("graf") else []) + ["eksik"]
        print(f"{i['id']:<22} {i['oncelik']:<7} {len(i['uyarilar']):>2} uyarı  {i['baslik']}")
        print(f"{'':22} sekmeler: {' '.join(sek)} · kaynak: {', '.join(i['kaynaklar'])} · MITRE: {', '.join(i['mitre']) or '-'}")
        print(f"{'':22} kart: {i['kart_ozet']}")

if bolum("graf", "Graf düğümleri: grafın ÇİZDİĞİ (tıklanabilir) düğümler, platform.js grafKur ile aynı kural"):
    TAVAN = {"normal": 4, "yalniz": 4, "engel": 6, "grup_engel": 1}
    SINIF_AD = {"normal": "grup da gidiyor", "yalniz": "yalnız o", "engel": "engellendi", "grup_engel": "grup da engelleniyor"}
    for i in D["incelemeler"]:
        g = i.get("graf")
        if not g:
            continue
        print(f"{i['id']}  · grup: {g['grup']['ad']} ({g['grup']['uye']} kişi) · kişi: {len(g['kisiler'])}")
        for k in g["kisiler"]:
            print(f"   kişi {k['ad']} ({k['ad_soyad']})" + (f"   seçici: .gsel button[data-p=\"{i['id']}|{k['ad']}\"]" if len(g["kisiler"]) > 1 else ""))
            n = 0
            for sn in ("normal", "yalniz", "engel", "grup_engel"):
                hepsi = sorted([a for a in k["ag"] if a["sinif"] == sn], key=lambda a: -a["istek"])
                toplam = max(k["ozet"]["engel"], len(hepsi)) if sn == "engel" else len(hepsi)
                goster = [] if sn == "grup_engel" else hepsi[:TAVAN[sn]]
                for a in goster:
                    print(f"      {SINIF_AD[sn]:<20} .gnode[data-c=\"{a['cidr']}\"]  {a['istek']:>5} istek  {a.get('ad') or '(tanımsız)'}")
                    n += 1
                if (sn == "grup_engel" and hepsi) or toplam > len(goster):
                    adet = len(hepsi) if sn == "grup_engel" else toplam - len(goster)
                    print(f"      {SINIF_AD[sn]:<20} .gnode[data-p=\"d{n}\"]  toplu kutu: {adet} ağ")
                    n += 1
    print("\nDüğüm seçilince ayrıntı grafın altındaki .gside kutusunda; grafı tam göstermek için önce #card içinde .gsvg'ye kaydır.")

if bolum("kisi", "Kişi sorgusu (#/kisi/<ad>)"):
    for ad, w in D["haftalar"].items():
        print(f"{ad:<10} {w['ad_soyad']:<20} {w['birim']}")

if bolum("mitre", "MITRE teknikleri (.tile[data-p=\"<kod>\"]) ve ortak varlığı olan ikililer"):
    uy = {}
    for u in D["uyarilar"]:
        for k in u["mitre"]:
            uy.setdefault(k, set()).add(u["varlik"])
    for k, m in D["mitre"].items():
        print(f"{k:<10} {m['taktik']:<18} {len(uy.get(k, [])):>2} varlık  {m['ad']}")
    print("\nortak varlığı olan ikililer (iki tile tıklanınca altta kutu çıkar):")
    kod = sorted(uy)
    for x in range(len(kod)):
        for y in range(x + 1, len(kod)):
            o = uy[kod[x]] & uy[kod[y]]
            if o:
                ayri = D["mitre"][kod[x]]["taktik"] != D["mitre"][kod[y]]["taktik"]
                print(f"   {kod[x]} + {kod[y]}  {'farklı aşama' if ayri else 'aynı aşama'}  {', '.join(sorted(o))[:80]}")

if bolum("sohbet", "Asistan soruları: hangi yazı hangi cevabı getirir"):
    print("Önce inceleme açılmalı (asistan bağlam mesajı ve çipler inceleme açılınca gelir).")
    print("Çip tıklamak: .chip[data-a=\"chip\"][data-p=\"soru:<id>\"]  ·  yazıp göndermek: yaz #askin + tik #ask button[type=\"submit\"]")
    print("Doğrulama adımı: [\"kontrol\", null, 0, {\"cevap\": \"<id>\"}]  (yanlış cevaba düşerse çekim hata verir)\n")
    for m in re.finditer(r"\{id:'(\w+)', et:tt\('([^']+)'\), k:(DIL === 'en' \? \[(.*?)\] : \[(.*?)\]|\[(.*?)\]),", JS):
        sid, et = m.group(1), m.group(2)
        en_k, tr_k, ortak = m.group(4), m.group(5), m.group(6)
        temiz = lambda s: ", ".join(x.strip().strip("'") for x in (s or "").split(","))
        print(f"{sid:<9} TR çip: {et}  ·  EN çip: {TXT_EN.get(et, '?')}")
        print(f"{'':9} anahtar sözcük TR: {temiz(tr_k or ortak)}")
        print(f"{'':9} anahtar sözcük EN: {temiz(en_k or ortak)}")
    print("\nEşleşme: yazıdaki anahtar sözcük sayısı en yüksek olan soru kazanır; eşitlikte listede önce gelen.")
    print("Kısa bir sözcük başka bir kelimenin içinde geçebilir (bir kez 'att', 'attack' içinde geçip yanlış cevap getirdi): kontrol adımı koy.")

if bolum("secici", "Seçici örnekleri (adım hedefi)"):
    print('''ray (sol menü)      .rail .rb[data-p=""] ana sayfa · [data-p="uyarilar"] · [data-p="graf"] · [data-p="mitre"] · [data-p="ag"] · [data-p="kisi"] · [data-p="kaynaklar"]
ana sayfa           .t4[data-p="yuksek|orta|dusuk|tum"] öncelik sekmesi · [data-a="brifing"] günlük özet düğmesi
                    .row-h[data-a="ac-inc"][data-p="<id>"] inceleme satırı · .chev[data-a="satir-ac"][data-p="<id>"] satırı aç/kapa
                    [data-a="donem-menu"] dönem menüsü · [data-a="donem"][data-p="son3"] son 3 gün
inceleme            .dtabs [data-a="tab"][data-p="<sekme>"] sekme · .dact [data-a="tab"][data-p="graf"] "Grafı aç" düğmesi
                    .verdict özet kutusu · .neden nedenler · .mets sayılar · .steps adımlar
kanıt               .logh ham kayıt başlığı (kaydırma hedefi) · .log ham kayıt kutusu
graf                .gsvg (kaydırma hedefi) · .gsvg circle[r="44"] grup halkası · .gsvg rect[fill="#143037"] kişi
                    .gnode[data-c="<CIDR>"] ağ düğümü · .gside dl düğüm ayrıntısı · .gsel button kişi seçici
sohbet              #askin soru kutusu · #ask button[type="submit"] gönder · #feed .msg.a:last-child son cevap · #handle panel tutamacı
MITRE               .tile[data-p="<kod>"] · .card .verdict ortak varlık kutusu · .card h3.sec liste başlığı
ağ geçişleri        .card .kpis3 sayaçlar · .seg [data-a="agtab"][data-p="akis|matris"] · [data-a="agmod"][data-p="ulasan|reddedilen"]
                    .card table.heat tbody tr:first-child td:nth-child(3) ilk satırın ikinci hücresi
tüm uyarılar        #uyara arama kutusu · select[data-a="uyonc"] öncelik · select[data-a="uykay"] kaynak · .card table.t tbody tr:first-child
kişi sorgusu        .card .hk hükümler · .card .tw tbody tr:nth-child(<n>) gün satırı · .chp ilk kez çipi · .chip[data-a="kisisec"][data-p="<ad>"]
veri kaynakları     .card table.t · .kcards bağlam kartları
kaydırma kabı       #card (ana kart; kaydirma adımının hedefi hemen hemen her zaman bu)''')

if bolum("sayi", "Altyazı sayı anahtarları (sahnenin \"sayilar\" listesi)"):
    for k, v in SS.adli(D).items():
        print(f"{k:<22} {v}")
    print("\ngenel anahtarlar (örnek değerlerle):")
    for k in ("inc.ayrilan-hesap.uyari", "inc.ayrilan-hesap.kaynak", "inc.tahsilat-operasyonlari.grup_uye", "inc.ayrilan-hesap.graf.yalniz",
              "kisi.ktuncer.oturum", "mitre.T1046.uyari", "gun.2026-09-17"):
        print(f"{k:<32} {SS.coz(D, k)}")
    print("\nKural: altyazıdaki her rakam bu listedeki bir değere eşit olmalı; yeni sayı gerekirse senaryo_sayilari.py'de ADLI sözlüğüne veriden hesaplayan bir satır ekle.")

if bolum("senaryo", "Var olan senaryolar"):
    sd = os.path.join(KOK, "kaynak", "senaryolar")
    for f in sorted(os.listdir(sd)):
        if f.endswith(".json"):
            s = json.load(open(os.path.join(sd, f), encoding="utf-8"))
            print(f"{f[:-5]:<16} {len(s['sahneler'])} sahne · {s.get('baslik', '')}")
