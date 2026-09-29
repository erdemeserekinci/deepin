#!/usr/bin/env python3
"""Videoya seslendirme ve muzik ekler: video/<senaryo>/<dil>_sesli.mp4

    python3 kaynak/ses_yap.py --senaryo reklam --dil tr        (once video_cek.py ile <dil>.mp4 cekilmis olmali)

Seslendirme: senaryonun "seslendirme" listesi, satir satir; her satir kendi sahnesinin basinda baslar ve bir sonraki satir
baslamadan biter (sahne sinirina birebir uymasi gerekmez). Sigmazsa once okuma hizi artar (en cok %25), yine sigmazsa betik durur (metni kisalt). Ses macOS'un kendi sesiyle
uretilir (say: Yelda / Samantha). Daha iyi bir ses icin video/<senaryo>/ses_<dil>/<NN>.wav|mp3|m4a dosyalari konursa (insan
kaydi ya da bir ses servisi, NN = satir sirasi 01, 02 ...) onlar kullanilir; zamanlama ayni kalir. Kopyalanacak numarali metin:
--metin (video/<senaryo>/seslendirme_<dil>.txt; her satirin en cok kac saniye surebilecegi yazili).
ElevenLabs ile dogrudan: export ELEVENLABS_API_KEY=... ; --elevenlabs-sesler (sesleri listeler) ; --elevenlabs <ses kimligi>
(satirlari seslendirip ses_<dil>/NN.mp3 olarak indirir, sigmayan satiri biraz hizli tekrar ister, sonra karistirir). Gonderilen
yalniz seslendirme metnidir; anahtar hicbir dosyaya yazilmaz.
Muzik: kodla uretilen ozgun parca (lisans yok), sahnelere gore kurgulanir: kanca sakin, logo vurusu, urun bolumunde ritim,
hizli montajda yukselir, gizlilik cumlesinde cekilir, kapanista cozulur. Konusma sirasinda muzik kisilir.
Birlestirme: ffmpeg varsa onunla, yoksa macOS'ta afconvert + AVFoundation (kaynak/ses_ekle.swift). Video yeniden kodlanmaz.

Ciktilar: <dil>_sesli.mp4 (video + ses), <dil>_ses.wav (karisim), <dil>_muzik.wav ve <dil>_seslendirme.wav (montaj icin ayri).
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile, urllib.error, urllib.request, wave

import numpy as np
from scipy import signal

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
SES = {"tr": "Yelda", "en": "Samantha"}
HIZ = {"tr": 168, "en": 174}


def wav_oku(yol):
    with wave.open(yol, "rb") as w:
        n, kanal, gen, sr = w.getnframes(), w.getnchannels(), w.getsampwidth(), w.getframerate()
        ham = w.readframes(n)
    if gen != 2:
        sys.exit(f"yalniz 16 bit WAV okunur: {yol}")
    x = np.frombuffer(ham, dtype="<i2").astype(np.float32) / 32768
    x = x.reshape(-1, kanal).mean(axis=1)
    if sr != SR:
        x = signal.resample_poly(x, SR, sr).astype(np.float32)
    return x


def wav_yaz(yol, x):
    x = np.clip(x, -1, 1)
    if x.ndim == 1:
        x = np.stack([x, x], axis=1)
    with wave.open(yol, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())


DIS_UZANTI = (".wav", ".mp3", ".m4a", ".aiff")
OKUNUS_DIS = {"Dipin Sekyuriti": "Deepin Security", "Mayter Atak": "MITRE ATT&CK"}


def dis_dosya(ses_dir, n, tmp):
    for uz in DIS_UZANTI:
        yol = os.path.join(ses_dir, f"{n:02d}{uz}")
        if not os.path.exists(yol):
            continue
        if uz == ".wav":
            try:
                return wav_oku(yol)
            except (SystemExit, wave.Error):
                pass
        cikti = os.path.join(tmp, f"dis_{n:02d}.wav")
        if shutil.which("afconvert"):
            subprocess.run(["afconvert", yol, "-o", cikti, "-f", "WAVE", "-d", "LEI16@48000"], check=True)
        elif shutil.which("ffmpeg"):
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", yol, "-ar", "48000", "-ac", "1", "-sample_fmt", "s16", cikti], check=True)
        else:
            sys.exit(f"{yol}: donusturmek icin afconvert (macOS) ya da ffmpeg gerekir")
        x = wav_oku(cikti)
        i = np.nonzero(np.abs(x) > 0.004)[0]
        return x[i[0]:i[-1] + 1] if len(i) else x
    return None


def yuvalar(sen, sahneler, toplam, dil):
    yer = {s["ad"]: s for s in sahneler}
    gec = lambda sl: (sl.get("gecikme_ms", 260)[dil] if isinstance(sl.get("gecikme_ms"), dict) else sl.get("gecikme_ms", 260))
    bas = [yer[sl["sahne"]]["bas"] + gec(sl) for sl in sen.get("seslendirme", [])]
    return [(b, (bas[i + 1] - 150) if i + 1 < len(bas) else toplam - 300) for i, b in enumerate(bas)]


EL_API = "https://api.elevenlabs.io/v1"


def el_istek(yol, veri=None):
    anahtar = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not anahtar:
        sys.exit("ELEVENLABS_API_KEY tanimli degil. Terminalde: export ELEVENLABS_API_KEY=... (anahtar ElevenLabs > Profile > API Keys)")
    baslik = {"xi-api-key": anahtar, "accept": "audio/mpeg" if veri else "application/json"}
    if veri:
        baslik["Content-Type"] = "application/json"
    istek = urllib.request.Request(EL_API + yol, data=json.dumps(veri).encode() if veri else None, headers=baslik, method="POST" if veri else "GET")
    try:
        with urllib.request.urlopen(istek, timeout=90) as y:
            return y.read()
    except urllib.error.HTTPError as e:
        govde = e.read().decode("utf-8", "replace")[:300]
        sys.exit(f"ElevenLabs hatasi {e.code}: {govde}")


def el_sesler():
    d = json.loads(el_istek("/voices"))
    for v in d.get("voices", []):
        et = v.get("labels") or {}
        print(f"{v['voice_id']}  {v.get('name', ''):<24} {et.get('language', '') or et.get('accent', ''):<14} {et.get('gender', ''):<8} {et.get('description', '') or et.get('use_case', '')}")
    print("\nTurkce icin ElevenLabs sitesinde Voice Library'den Turkce bir ses 'My Voices'a eklenirse burada gorunur.")


def el_uret(sen, sahneler, dil, vdir, toplam, ses_kimligi, model):
    yy = yuvalar(sen, sahneler, toplam, dil)
    ses_dir = os.path.join(vdir, f"ses_{dil}")
    os.makedirs(ses_dir, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="dsec_el_")
    for n, sl in enumerate(sen.get("seslendirme", []), 1):
        hedef = os.path.join(ses_dir, f"{n:02d}.mp3")
        if os.path.exists(hedef):
            print(f"  {n:02d} var, atlandi (yeniden uretmek icin dosyayi silin)")
            continue
        m = sl[dil]
        for k, v in OKUNUS_DIS.items():
            m = m.replace(k, v)
        yuva = (yy[n - 1][1] - yy[n - 1][0]) / 1000
        hiz = 1.0
        for _ in range(3):
            ayar = {"stability": 0.45, "similarity_boost": 0.8, "style": 0.25, "use_speaker_boost": True}
            if hiz != 1.0:
                ayar["speed"] = round(hiz, 2)
            ses = el_istek(f"/text-to-speech/{ses_kimligi}?output_format=mp3_44100_128", {"text": m, "model_id": model, "voice_settings": ayar})
            open(hedef, "wb").write(ses)
            sure = len(dis_dosya(ses_dir, n, tmp)) / SR
            if sure <= yuva or hiz >= 1.15:
                break
            hiz = min(1.15, hiz * sure / yuva * 1.03)
        print(f"  {n:02d}  {sure:4.1f} / {yuva:4.1f} sn  hiz {hiz:.2f}  {m[:60]}")
    shutil.rmtree(tmp, ignore_errors=True)


def metin_yaz(sen, sahneler, dil, vdir, toplam):
    yy = yuvalar(sen, sahneler, toplam, dil)
    satir = [f"deepin security reklami, seslendirme ({dil}). Her satiri ayri bir dosya olarak kaydedin: 01.mp3, 02.mp3 ...",
             f"Dosyalari su klasore koyun: video/<senaryo>/ses_{dil}/  Sonra: python3 kaynak/ses_yap.py --senaryo <senaryo> --dil {dil}",
             "Parantezdeki sure, cumlenin en cok ne kadar surebilecegi (sahnesine sigmasi icin). Sakin, sicak, kendinden emin bir ton.", ""]
    for n, sl in enumerate(sen.get("seslendirme", []), 1):
        bas, bit = yy[n - 1]
        m = sl[dil]
        for k, v in OKUNUS_DIS.items():
            m = m.replace(k, v)
        satir.append(f"{n:02d}  (en cok {(bit - bas) / 1000:.1f} sn)  {m}")
    yol = os.path.join(vdir, f"seslendirme_{dil}.txt")
    open(yol, "w", encoding="utf-8").write("\n".join(satir) + "\n")
    return yol


def say_uret(metin, ses, hiz, yol):
    if not shutil.which("say"):
        sys.exit("say yok (macOS disi): seslendirmeyi video/<senaryo>/ses_<dil>/NN.wav dosyalari olarak verin")
    subprocess.run(["say", "-v", ses, "-r", str(int(hiz)), "--file-format=WAVE", "--data-format=LEI16@48000", "-o", yol, metin], check=True)
    x = wav_oku(yol)
    i = np.nonzero(np.abs(x) > 0.004)[0]
    return x[i[0]:i[-1] + 1] if len(i) else x


def seslendirme(sen, sahneler, dil, vdir, toplam):
    yy = yuvalar(sen, sahneler, toplam, dil)
    ses_dir = os.path.join(vdir, f"ses_{dil}")
    iz = np.zeros(int(toplam / 1000 * SR) + SR, np.float32)
    aktif = np.zeros_like(iz)
    tmp = tempfile.mkdtemp(prefix="dsec_ses_")
    rapor = []
    vtt = ["WEBVTT", ""]
    vz = lambda ms: f"{int(ms // 3600000):02d}:{int(ms // 60000 % 60):02d}:{int(ms // 1000 % 60):02d}.{int(ms % 1000):03d}"
    for n, sl in enumerate(sen.get("seslendirme", []), 1):
        bas, bit = yy[n - 1]
        yuva = (bit - bas) / 1000
        x = dis_dosya(ses_dir, n, tmp) if os.path.isdir(ses_dir) else None
        if x is not None:
            kaynak = "dosya"
        else:
            hiz = HIZ[dil]
            x = say_uret(sl[dil], SES[dil], hiz, os.path.join(tmp, f"{n}.wav"))
            for _ in range(4):
                if len(x) / SR <= yuva or hiz >= HIZ[dil] * 1.25:
                    break
                hiz = min(HIZ[dil] * 1.25, hiz * (len(x) / SR) / yuva * 1.06)
                x = say_uret(sl[dil], SES[dil], hiz, os.path.join(tmp, f"{n}.wav"))
            kaynak = f"say {SES[dil]} {int(hiz)}"
        sure = len(x) / SR
        if sure > yuva + 0.05:
            ne = "kaydi biraz daha hizli okuyun ya da cumleyi kisaltin" if kaynak == "dosya" else "metni kisaltin"
            sys.exit(f"SIGMIYOR: satir {n} ({sl['sahne']}) {sure:.1f} sn, en cok {yuva:.1f} sn olabilir; {ne}: {sl[dil]}")
        yazi = sl[dil]
        for k, v in OKUNUS_DIS.items():
            yazi = yazi.replace(k, v)
        vtt += [str(n), f"{vz(bas)} --> {vz(min(bas + sure * 1000 + 250, bit))}", yazi, ""]
        i = int(bas / 1000 * SR)
        iz[i:i + len(x)] += x
        aktif[i:i + len(x)] = 1
        rapor.append(f"  {n:02d} {bas / 1000:5.1f} sn  {sure:4.1f}/{yuva:4.1f} sn  {kaynak:<16} {sl[dil][:60]}")
    shutil.rmtree(tmp, ignore_errors=True)
    open(os.path.join(vdir, f"{dil}_seslendirme.vtt"), "w", encoding="utf-8").write("\n".join(vtt))
    tepe = np.max(np.abs(iz)) or 1
    return iz / tepe * 0.8, aktif, rapor


def lp(x, f, sira=2):
    return signal.sosfilt(signal.butter(sira, f, "low", fs=SR, output="sos"), x, axis=0)


def hp(x, f, sira=2):
    return signal.sosfilt(signal.butter(sira, f, "high", fs=SR, output="sos"), x, axis=0)


def zarf(n, atak, birak):
    e = np.ones(n, np.float32)
    a, b = min(n, int(atak * SR)), min(n, int(birak * SR))
    if a:
        e[:a] = np.linspace(0, 1, a)
    if b:
        e[n - b:] *= np.linspace(1, 0, b)
    return e


def nota(m):
    return 440 * 2 ** ((m - 69) / 12)


def fragman_vurusu(sure_s, rng):
    n = int(sure_s * SR)
    t = np.arange(n) / SR
    alt = np.sin(2 * np.pi * np.cumsum(32 + 26 * np.exp(-t * 5)) / SR) * np.exp(-t * 1.1)
    braam = np.zeros(n)
    for f, sev in ((55.0, 1.0), (55.0 * 1.004, .8), (82.41, .55), (110.0, .6), (110.0 * .997, .45)):
        braam += (2 * ((t * f) % 1) - 1) * sev
    kesim = 240 + 700 * np.clip(t / .25, 0, 1) * np.exp(-np.clip(t - .25, 0, None) * 2.6)
    out = np.zeros(n)
    zi = None
    parca = SR // 100
    for i in range(0, n, parca):
        sos = signal.butter(2, max(120.0, float(kesim[i])), "low", fs=SR, output="sos")
        if zi is None:
            zi = signal.sosfilt_zi(sos) * 0
        out[i:i + parca], zi = signal.sosfilt(sos, braam[i:i + parca], zi=zi)
    braam = np.tanh(out * 1.8) * zarf(n, .018, 1.2) * np.exp(-t * .55)
    vur = signal.sosfilt(signal.butter(2, [180, 3200], "band", fs=SR, output="sos"), rng.standard_normal(n)) * np.exp(-t * 38)
    x = alt * 1.0 + braam * .45 + vur * .3
    ir_n = int(3.0 * SR)
    ir_t = np.arange(ir_n) / SR
    L = x + signal.fftconvolve(x, rng.standard_normal(ir_n) * np.exp(-ir_t * 1.7))[:n] * .02
    R = np.roll(x, int(.007 * SR)) + signal.fftconvolve(x, rng.standard_normal(ir_n) * np.exp(-ir_t * 1.7))[:n] * .02
    v = np.stack([L, R], axis=1)
    return (v / (np.max(np.abs(v)) or 1)).astype(np.float32)


def muzik(sahneler, toplam, rng, vurus_t=None):
    N = int(toplam / 1000 * SR) + SR
    t_s = {s["ad"]: s["bas"] / 1000 for s in sahneler}
    b_s = {s["ad"]: s["bit"] / 1000 for s in sahneler}
    logo = t_s.get("logo", 3.8)
    urun = t_s.get("ana", logo + 3.4)
    montaj = t_s.get("m-kisi", toplam / 1000 * .78)
    sakin = t_s.get("gizlilik", toplam / 1000 * .89)
    kapanis = t_s.get("kapanis", toplam / 1000 - 4.6)
    son = toplam / 1000
    L, R = np.zeros(N, np.float32), np.zeros(N, np.float32)
    beat = 60 / 96
    bar = beat * 4
    akor = [(57, 60, 64), (53, 57, 60), (48, 52, 55), (55, 59, 62)]
    kok = [45, 41, 36, 43]

    def ekle(x, t, sol=1.0, sag=1.0):
        i = int(t * SR)
        if i >= N:
            return
        x = x[:N - i]
        L[i:i + len(x)] += x * sol
        R[i:i + len(x)] += x * sag

    def ped(f_list, t, sure, sev, parlak):
        n = int(sure * SR)
        tt = np.arange(n) / SR
        x = np.zeros(n, np.float32)
        for f in f_list:
            for d in (-0.07, 0.07):
                x += (2 * ((tt * f * (1 + d / 100)) % 1) - 1).astype(np.float32)
        x = lp(x, parlak) * zarf(n, min(1.2, sure * .4), min(1.5, sure * .5)) * sev / len(f_list)
        ekle(x, t, 1.0, 0.92)
        ekle(np.roll(x, int(.011 * SR)), t, 0.92, 1.0)

    def kick(t, sev):
        n = int(.42 * SR)
        tt = np.arange(n) / SR
        f = 45 + 95 * np.exp(-tt * 28)
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9) * sev
        ekle(x.astype(np.float32), t)

    def hat(t, sev, uzun=False):
        n = int((.18 if uzun else .05) * SR)
        x = hp(rng.standard_normal(n).astype(np.float32), 7500) * np.exp(-np.arange(n) / SR * (14 if uzun else 70)) * sev
        ekle(x, t, 0.8, 1.0)

    def clap(t, sev):
        n = int(.22 * SR)
        x = signal.sosfilt(signal.butter(2, [900, 3500], "band", fs=SR, output="sos"), rng.standard_normal(n)).astype(np.float32)
        x *= np.exp(-np.arange(n) / SR * 18) * sev
        ekle(x, t, 1.0, 0.9)

    def bas_ses(f, t, sure, sev):
        n = int(sure * SR)
        tt = np.arange(n) / SR
        x = np.tanh(2.2 * np.sin(2 * np.pi * f * tt)) * zarf(n, .01, .12) * sev
        ekle(lp(x.astype(np.float32), 420), t)

    def pluck(f, t, sev):
        n = int(.5 * SR)
        tt = np.arange(n) / SR
        x = (np.sin(2 * np.pi * f * tt) + .35 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt * 7) * sev
        taraf = rng.uniform(.6, 1.0)
        ekle(x.astype(np.float32), t, taraf, 1.6 - taraf)

    def darbe(t, sev):
        n = int(2.4 * SR)
        tt = np.arange(n) / SR
        x = np.sin(2 * np.pi * (38 + 40 * np.exp(-tt * 6)) * tt) * np.exp(-tt * 1.6) * sev
        g = lp(rng.standard_normal(n).astype(np.float32), 900) * np.exp(-tt * 5) * sev * .35
        ekle((x + g).astype(np.float32), t)

    def yukselen(t0, t1, sev):
        n = int((t1 - t0) * SR)
        g = rng.standard_normal(n).astype(np.float32)
        kat = np.linspace(0, 1, n) ** 2
        out = np.zeros(n, np.float32)
        parca = SR // 50
        zi = None
        for i in range(0, n, parca):
            f = 300 + 5000 * kat[min(i, n - 1)]
            sos = signal.butter(2, f, "low", fs=SR, output="sos")
            if zi is None:
                zi = signal.sosfilt_zi(sos) * 0
            out[i:i + parca], zi = signal.sosfilt(sos, g[i:i + parca], zi=zi)
        ekle(out * kat * sev, t0)

    ped([nota(45), nota(52)], 0, logo + .4, .20, 520)
    yukselen(max(0, logo - 1.3), logo, .12)
    darbe(logo, .55)
    ped([nota(m) for m in akor[0]], logo, urun - logo + 1.0, .22, 1400)
    t, i = urun, 0
    while t < kapanis - 0.05:
        k = i % 4
        yogun = 2 if t >= montaj else 1
        sakin_bolum = sakin <= t < kapanis
        ped([nota(m) for m in akor[k]], t, bar + .6, .17 if not sakin_bolum else .21, 1600 if yogun == 1 else 2400)
        if not sakin_bolum:
            bas_ses(nota(kok[k]), t, beat * 1.6, .30)
            bas_ses(nota(kok[k]), t + beat * 2, beat * 1.6, .26)
            for b in range(4):
                if b in (0, 2) or yogun == 2:
                    kick(t + b * beat, .55 if b in (0, 2) else .38)
                for h in range(2):
                    hat(t + b * beat + h * beat / 2, .06 if h else .035)
                if yogun == 2 and b in (1, 3):
                    clap(t + b * beat, .22)
            if t >= t_s.get("graf", urun + 11):
                arp = [akor[k][0] + 12, akor[k][1] + 12, akor[k][2] + 12, akor[k][1] + 24]
                for s in range(8):
                    pluck(nota(arp[s % 4]), t + s * beat / 2, .07 if yogun == 1 else .09)
        else:
            hat(t, .03, uzun=True)
        t += bar
        i += 1
    hit = vurus_t if vurus_t else kapanis
    yukselen(max(t_s.get("gizlilik", kapanis) + 1.2, hit - 1.6), hit, .10)
    if not vurus_t:
        darbe(kapanis, .6)
    ped([nota(m) for m in (48, 52, 55, 59)], kapanis, son - kapanis + 1.0, .30, 1800)
    for s, m in enumerate((72, 76, 79, 83)):
        pluck(nota(m), kapanis + .15 + s * .18, .09)
    ir_n = int(2.2 * SR)
    ir_t = np.arange(ir_n) / SR
    irL = rng.standard_normal(ir_n) * np.exp(-ir_t * 2.4)
    irR = rng.standard_normal(ir_n) * np.exp(-ir_t * 2.4)
    Lw = signal.fftconvolve(L, irL)[:N] * .012
    Rw = signal.fftconvolve(R, irR)[:N] * .012
    m = np.stack([L + Lw, R + Rw], axis=1)
    m = hp(m, 28)
    bitis = int(son * SR)
    m[bitis:] = 0
    m[max(0, bitis - int(1.2 * SR)):bitis] *= np.linspace(1, 0, min(bitis, int(1.2 * SR)))[:, None]
    return m / (np.max(np.abs(m)) or 1) * 0.9


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--senaryo", default="reklam")
    ap.add_argument("--dil", default="tr", choices=["tr", "en"])
    ap.add_argument("--muzik-seviye", type=float, default=0.42, help="konusma yokken muzik seviyesi (0-1)")
    ap.add_argument("--kisma", type=float, default=0.38, help="konusma sirasinda muzik bu oranla carpilir")
    ap.add_argument("--hedef-db", type=float, default=-17.0, help="karisimin ortalama ses duzeyi (RMS dBFS); diller arasi ayni kalsin diye")
    ap.add_argument("--metin", action="store_true", help="yalniz seslendirme metnini yaz (disarida seslendirmek icin): video/<senaryo>/seslendirme_<dil>.txt")
    ap.add_argument("--elevenlabs", metavar="SES_KIMLIGI", default="", help="satirlari ElevenLabs ile seslendir (ELEVENLABS_API_KEY ortam degiskeni gerekir), sonra karistir")
    ap.add_argument("--elevenlabs-sesler", action="store_true", help="hesaptaki ElevenLabs seslerini ve kimliklerini listele")
    ap.add_argument("--elevenlabs-model", default="eleven_multilingual_v2")
    a = ap.parse_args()
    if a.elevenlabs_sesler:
        el_sesler()
        return
    vdir = os.path.join(KOK, "video", a.senaryo)
    video = os.path.join(vdir, f"{a.dil}.mp4")
    sj = os.path.join(vdir, f"{a.dil}_sahneler.json")
    for y in (video, sj):
        if not os.path.exists(y):
            sys.exit(f"yok: {y} (once: python3 kaynak/video_cek.py --senaryo {a.senaryo} --dil {a.dil})")
    sen = json.load(open(os.path.join(KOK, "kaynak", "senaryolar", a.senaryo + ".json"), encoding="utf-8"))
    if not sen.get("seslendirme"):
        sys.exit(f"senaryoda seslendirme listesi yok: {a.senaryo}")
    bilgi = json.load(open(sj, encoding="utf-8"))
    sahneler, toplam = bilgi["sahneler"], bilgi["sure_ms"]
    rng = np.random.default_rng(7)
    if a.metin:
        print("yazildi:", metin_yaz(sen, sahneler, a.dil, vdir, toplam))
        return
    if a.elevenlabs:
        print(f"ElevenLabs ({a.elevenlabs_model}), ses {a.elevenlabs}:")
        el_uret(sen, sahneler, a.dil, vdir, toplam, a.elevenlabs, a.elevenlabs_model)

    ses, aktif, rapor = seslendirme(sen, sahneler, a.dil, vdir, toplam)
    print(f"seslendirme ({len(rapor)} satir):")
    print("\n".join(rapor))
    mc = sen.get("muzik", {})
    vurus_t = None
    if mc.get("fragman_vurusu"):
        vurus_t = yuvalar(sen, sahneler, toplam, a.dil)[int(mc["fragman_vurusu"]) - 1][0] / 1000 - 0.03
        print(f"fragman vurusu: {vurus_t:.2f} sn (seslendirme satiri {mc['fragman_vurusu']} basliyor)")
    mz = muzik(sahneler, toplam, rng, vurus_t)
    n = min(len(ses), len(mz))
    ses, aktif, mz = ses[:n], aktif[:n], mz[:n]
    vurus = np.zeros((n, 2), np.float32)
    if vurus_t:
        v = fragman_vurusu(min(4.5, n / SR - vurus_t), rng)
        i = int(vurus_t * SR)
        vurus[i:i + len(v)] = v[:n - i]
    k = int(.25 * SR)
    duz = np.convolve(aktif, np.ones(k) / k, mode="same")
    kazanc = a.muzik_seviye * (1 - (1 - a.kisma) * np.clip(duz * 1.4, 0, 1))
    karisim = mz * kazanc[:, None] + vurus * mc.get("vurus_seviye", 0.5) + np.stack([ses, ses], axis=1) * 0.92
    karisim = np.tanh(karisim * 1.1) / np.tanh(1.1)
    disari = np.ones(len(karisim), bool)
    if vurus_t:
        disari[int(vurus_t * SR):int((vurus_t + 1.6) * SR)] = False
    ref = np.max(np.abs(karisim[disari])) or 1
    karisim = karisim / ref * 0.89
    rms_db = 20 * np.log10(np.sqrt(np.mean(karisim ** 2)) or 1e-9)
    karisim = karisim * 10 ** (np.clip(a.hedef_db - rms_db, -3, 3) / 20)
    diz, pay = 0.80, 0.19
    b = np.abs(karisim)
    karisim = np.where(b > diz, np.sign(karisim) * (diz + pay * np.tanh((b - diz) / pay)), karisim)
    wav_yaz(os.path.join(vdir, f"{a.dil}_ses.wav"), karisim)
    wav_yaz(os.path.join(vdir, f"{a.dil}_muzik.wav"), mz * a.muzik_seviye)
    wav_yaz(os.path.join(vdir, f"{a.dil}_seslendirme.wav"), ses * 0.92)

    cikti = os.path.join(vdir, f"{a.dil}_sesli.mp4")
    tmp = tempfile.mkdtemp(prefix="dsec_birlestir_")
    try:
        if shutil.which("ffmpeg"):
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", os.path.join(vdir, f"{a.dil}_ses.wav"),
                            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", cikti], check=True)
        elif shutil.which("afconvert") and shutil.which("swift"):
            m4a = os.path.join(tmp, "ses.m4a")
            subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", "-b", "192000", os.path.join(vdir, f"{a.dil}_ses.wav"), m4a], check=True)
            subprocess.run(["swift", os.path.join(KOK, "kaynak", "ses_ekle.swift"), video, m4a, cikti], check=True)
        else:
            print("UYARI: ffmpeg ya da macOS araclari yok; ses dosyalari yazildi, birlestirme yapilmadi")
            return
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("yazildi:", cikti, f"{os.path.getsize(cikti) / 1e6:.1f} MB")
    print("yazildi:", os.path.join(vdir, f"{a.dil}_ses.wav"), "(karisim), _muzik.wav, _seslendirme.wav (ayri)")


if __name__ == "__main__":
    main()
