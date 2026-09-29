#!/usr/bin/env python3
"""Tur modunu basliksiz Chrome'da kare kare oynatip mp4 yazar.

    python3 kaynak/video_cek.py --senaryo urun_turu --dil tr             altyazili 1080p video
    python3 kaynak/video_cek.py --senaryo urun_turu --dil en --temiz     altyazisiz, cercevesiz 4K (montaj icin)
    python3 kaynak/video_cek.py --senaryo urun_turu --dil tr --onizleme  her sahneden bir kare (hizli bakis, ~1 dk)
    python3 kaynak/video_cek.py --senaryo urun_turu --dil tr --ornek     depoya konan kucuk ornek, 720p (<dil>_ornek.mp4)
    python3 kaynak/video_cek.py --senaryo urun_turu --dil tr --anlik 3000,15000   yalniz o anlarin PNG'si

Ciktilar video/<senaryo>/ altinda: <dil>.mp4, <dil>.srt, <dil>_temas.jpg (temiz surumde <dil>_temiz.*),
onizleme_<dil>.jpg, anlik/<dil>_<ms>.png.

Zaman sayfanin kendi saatinde degil, kaydedicinin verdigi saatte ilerler: her kare icin window.__tur.kare(ms) cagrilir,
imlec konumu gercek fare olayi olarak gonderilir (uzerine gelme gorunumu icin), sonra ekran goruntusu alinir.
Boylece cekim kac saniye surerse sursun video 30 kare/sn ve iki cekim ayni cikar.

Gerekenler: Google Chrome (ya da Chromium / Edge; yol bulunamazsa CHROME ortam degiskeni), Python 3.9+,
pip install -r kaynak/video_gereksinim.txt. Chrome kullanicinin profiliyle DEGIL, gecici bir klasorle acilir.
Sayfa disariya istek yapmaz (yalniz Google Fonts'tan Poppins; internet yoksa sistem yazi tipiyle cekilir, uyari basilir).
"""
import argparse, base64, json, os, pathlib, shutil, socket, subprocess, sys, tempfile, time, urllib.request

import cv2
import numpy as np
import websocket

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN, YUK = 1600, 900
OLCEK = 1.2

CHROME_ADAYLARI = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]


def chrome_bul():
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    for yol in CHROME_ADAYLARI:
        if os.path.exists(yol):
            return yol
    for ad in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge", "chrome"):
        yol = shutil.which(ad)
        if yol:
            return yol
    sys.exit("Chrome bulunamadi. Kurun ya da yolunu verin: CHROME=/yol/chrome python3 kaynak/video_cek.py ...")


def bos_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


class CDP:
    def __init__(self, ws_url):
        self.ws = websocket.create_connection(ws_url, timeout=60, suppress_origin=True)
        self.n = 0

    def __call__(self, yontem, **par):
        self.n += 1
        kimlik = self.n
        self.ws.send(json.dumps({"id": kimlik, "method": yontem, "params": par}))
        while True:
            m = json.loads(self.ws.recv())
            if m.get("id") == kimlik:
                if "error" in m:
                    raise RuntimeError(f"{yontem}: {m['error']}")
                return m.get("result", {})

    def js(self, ifade):
        r = self("Runtime.evaluate", expression=ifade, returnByValue=True, awaitPromise=True)
        if "exceptionDetails" in r:
            raise RuntimeError("sayfa hatasi: " + json.dumps(r["exceptionDetails"])[:400])
        return r["result"].get("value")


def chrome_ac(port, profil):
    arg = [chrome_bul(), "--headless=new", f"--remote-debugging-port={port}", f"--user-data-dir={profil}",
           "--no-first-run", "--no-default-browser-check", "--disable-extensions", "--hide-scrollbars",
           "--mute-audio", "--disable-background-timer-throttling", "--disable-renderer-backgrounding",
           "--force-color-profile=srgb", f"--window-size={GEN},{YUK}", "about:blank"]
    p = subprocess.Popen(arg, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(120):
        try:
            liste = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=1).read())
            sayfa = [x for x in liste if x.get("type") == "page"]
            if sayfa:
                return p, sayfa[0]["webSocketDebuggerUrl"]
        except Exception:
            pass
        time.sleep(.15)
    p.kill()
    sys.exit("Chrome acildi ama hata ayiklama baglantisi kurulamadi")


def levha(kareler, yol, sutun=5):
    if not kareler:
        return
    kg, ky = 480, 270
    satir = (len(kareler) + sutun - 1) // sutun
    lev = np.full((satir * (ky + 28), sutun * kg, 3), 255, np.uint8)
    for i, (etiket, img) in enumerate(kareler):
        r, c = divmod(i, sutun)
        k = cv2.resize(img, (kg, ky), interpolation=cv2.INTER_AREA)
        y = r * (ky + 28)
        lev[y:y + ky, c * kg:(c + 1) * kg] = k
        cv2.putText(lev, etiket, (c * kg + 8, y + ky + 20), cv2.FONT_HERSHEY_SIMPLEX, .5, (60, 60, 60), 1, cv2.LINE_AA)
    cv2.imwrite(yol, lev, [cv2.IMWRITE_JPEG_QUALITY, 85])


def srt_zaman(ms):
    ms = int(round(ms))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def srt_yaz(sahneler, yol):
    parca, n = [], 0
    for sh in sahneler:
        if not sh.get("metin"):
            continue
        n += 1
        parca.append(f"{n}\n{srt_zaman(sh['bas'] + 150)} --> {srt_zaman(sh['bit'] - 150)}\n{sh['metin']}\n")
    open(yol, "w", encoding="utf-8").write("\n".join(parca))


def h264e_cevir(yol):
    ff = shutil.which("ffmpeg")
    gecici = yol + ".h264.mp4"
    if ff:
        r = subprocess.run([ff, "-y", "-loglevel", "error", "-i", yol, "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
                            "-movflags", "+faststart", gecici])
    elif shutil.which("avconvert"):
        r = subprocess.run(["avconvert", "--source", yol, "--preset", "PresetHighestQuality", "--output", gecici, "--replace"])
    else:
        print("UYARI: video mp4v kodegiyle yazildi (tarayicilar oynatmayabilir). H.264 icin: ffmpeg -i", yol,
              "-c:v libx264 -crf 18 -pix_fmt yuv420p cikti.mp4")
        return
    if r.returncode == 0 and os.path.exists(gecici):
        os.replace(gecici, yol)
        print("H.264'e cevrildi:", yol)


def main():
    global OLCEK
    ap = argparse.ArgumentParser(description="deepin security tur modunu videoya ceker")
    ap.add_argument("--senaryo", default="urun_turu", help="kaynak/senaryolar/<ad>.json (varsayilan urun_turu)")
    ap.add_argument("--dil", default="tr", choices=["tr", "en"])
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--temiz", action="store_true", help="altyazisiz, cercevesiz, kapanissiz urun goruntusu (montaj icin), varsayilan 4K")
    ap.add_argument("--olcek", type=float, default=0, help="cihaz olcegi; varsayilan 1.2 (1080p), --temiz ile 2.4 (4K), --ornek ile 0.8 (720p)")
    ap.add_argument("--ornek", action="store_true", help="depoya konan kucuk ornek: 720p, <dil>_ornek.mp4")
    ap.add_argument("--onizleme", action="store_true", help="her sahnenin sonuna yakin bir kare; tek levha (hizli bakis)")
    ap.add_argument("--anlik", default="", help="virgulle ms listesi; yalniz o anlarin PNG'si")
    ap.add_argument("--levha", type=float, default=2.0, help="temas levhasi icin kac saniyede bir kare")
    a = ap.parse_args()
    OLCEK = a.olcek or (2.4 if a.temiz else 0.8 if a.ornek else 1.2)

    sen_dir = os.path.join(KOK, "kaynak", "senaryolar")
    sen_yol = os.path.join(sen_dir, a.senaryo + ".json")
    if not os.path.exists(sen_yol):
        var = sorted(f[:-5] for f in os.listdir(sen_dir) if f.endswith(".json"))
        sys.exit(f"senaryo yok: {a.senaryo}. Var olanlar: {', '.join(var)}")
    sayfa = os.path.join(KOK, "index.html" if a.dil == "tr" else os.path.join("en", "index.html"))
    if os.path.getmtime(sen_yol) > os.path.getmtime(sayfa):
        sys.exit("senaryo dosyasi sayfadan yeni: once uret.py ve denetim.py kosun (senaryolar sayfaya gomulur)")
    sorgu = f"?tur=1&kare=1&senaryo={a.senaryo}" + ("&temiz=1" if a.temiz else "")
    url = pathlib.Path(sayfa).resolve().as_uri() + sorgu + "#/"
    vdir = os.path.join(KOK, "video", a.senaryo)
    os.makedirs(vdir, exist_ok=True)
    ek = ("_temiz" if a.temiz else "") + ("_ornek" if a.ornek else "")
    cikti = os.path.join(vdir, f"{a.dil}{ek}.mp4")
    boyut = (round(GEN * OLCEK), round(YUK * OLCEK))

    profil = tempfile.mkdtemp(prefix="dsec_video_")
    port = bos_port()
    proc, ws = chrome_ac(port, profil)
    try:
        c = CDP(ws)
        c("Page.enable")
        c("Runtime.enable")
        c("Emulation.setDeviceMetricsOverride", width=GEN, height=YUK, deviceScaleFactor=OLCEK, mobile=False)
        c("Page.navigate", url=url)
        bas = time.time()
        while True:
            d = c.js("window.__tur ? {h: !!window.__tur.hazir, d: window.__tur.durum, e: window.__tur.hatalar} : null")
            if d and d["h"]:
                break
            if d and d["d"] == "hata":
                sys.exit("tur baslamadi: " + "; ".join(d["e"]))
            if time.time() - bas > 40:
                sys.exit("tur modu hazir olmadi (sayfa acildi mi, ?tur=1 calisti mi)")
            time.sleep(.2)
        if not c.js("document.fonts.check('600 15px Poppins')"):
            print("UYARI: Poppins yuklenmedi, sistem yazi tipiyle cekiliyor (internet baglantisi?)")
        sure = c.js("window.__tur.sure")
        sahneler = c.js("window.__tur.sahneler")
        dt = 1000 / a.fps
        n = int(round(sure / dt)) + 1
        print(f"{a.senaryo} / {a.dil}{' temiz' if a.temiz else ''}: {sure / 1000:.1f} sn, {n} kare, {boyut[0]}x{boyut[1]}", flush=True)
        for sh in sahneler:
            print(f"  {sh['bas'] / 1000:5.1f}-{sh['bit'] / 1000:5.1f}  {sh['ad']:<14} {sh['metin'][:70]}", flush=True)

        if a.onizleme:
            anlik = [(sh["bas"] + (sh["bit"] - sh["bas"]) * .8, sh["ad"]) for sh in sahneler]
        elif a.anlik:
            anlik = [(float(x), None) for x in a.anlik.split(",") if x.strip()]
        else:
            anlik = None
        if anlik is not None:
            anlik.sort(key=lambda x: x[0])
        yazici, kod = None, None
        if anlik is None:
            for kod in ("avc1", "mp4v"):
                yazici = cv2.VideoWriter(cikti, cv2.VideoWriter_fourcc(*kod), a.fps, boyut)
                if yazici.isOpened():
                    break
            if not yazici.isOpened():
                sys.exit("VideoWriter acilamadi (opencv-python kurulu mu)")
            print("kodek:", kod, flush=True)
        kareler, son_levha, hi = [], -1e9, 0
        t_bas = time.time()
        for i in range(n):
            t = min(sure, i * dt)
            r = c.js(f"window.__tur.kare({t:.3f})")
            if anlik is not None:
                if hi >= len(anlik):
                    break
                if t + dt / 2 < anlik[hi][0]:
                    continue
            c("Input.dispatchMouseEvent", type="mouseMoved", x=r["x"], y=r["y"], button="none")
            g = c("Page.captureScreenshot", format="jpeg", quality=93, fromSurface=True)
            img = cv2.imdecode(np.frombuffer(base64.b64decode(g["data"]), np.uint8), cv2.IMREAD_COLOR)
            if (img.shape[1], img.shape[0]) != boyut:
                img = cv2.resize(img, boyut, interpolation=cv2.INTER_AREA)
            if anlik is not None:
                ms, ad = anlik[hi]
                if ad is None:
                    os.makedirs(os.path.join(vdir, "anlik"), exist_ok=True)
                    yol = os.path.join(vdir, "anlik", f"{a.dil}{ek}_{int(ms):06d}.png")
                    cv2.imwrite(yol, img)
                    print("yazildi:", yol, flush=True)
                else:
                    kareler.append((f"{ms / 1000:.1f} sn  {ad}", img))
                hi += 1
                continue
            yazici.write(img)
            if t - son_levha >= a.levha * 1000 - 1:
                kareler.append((f"{t / 1000:.1f} sn", img))
                son_levha = t
            if i % 150 == 0:
                print(f"  {t / 1000:5.1f} / {sure / 1000:.1f} sn  ({time.time() - t_bas:.0f} sn gecti)", flush=True)
        hatalar = c.js("window.__tur.hatalar")
        if a.onizleme:
            yol = os.path.join(vdir, f"onizleme_{a.dil}{ek}.jpg")
            levha(kareler, yol, sutun=4)
            print("yazildi:", yol)
        if yazici is not None:
            yazici.release()
            if kod == "mp4v":
                h264e_cevir(cikti)
            temas = os.path.join(vdir, f"{a.dil}{ek}_temas.jpg")
            levha(kareler, temas)
            srt = os.path.join(vdir, f"{a.dil}{ek}.srt")
            srt_yaz(sahneler, srt)
            print("yazildi:", cikti, f"{os.path.getsize(cikti) / 1e6:.1f} MB")
            print("yazildi:", temas)
            print("yazildi:", srt)
        if hatalar:
            print("TUR HATALARI:", len(hatalar))
            for h in hatalar:
                print("  -", h)
            sys.exit(1)
        print("tur hatasi yok")
    finally:
        proc.terminate()
        try:
            proc.wait(5)
        except Exception:
            proc.kill()
        shutil.rmtree(profil, ignore_errors=True)


if __name__ == "__main__":
    main()
