#!/usr/bin/env python3
"""Font Awesome Free 6.7.2 glyflerini SVG yoluna cevirir -> kaynak/ikonlar.json

    python3 kaynak/ikon_uret.py      (yalniz yeni ikon gerekince; cikti ikonlar.json depoda hazir)
    Gerekenler: pip install qtawesome fonttools  (QTAWESOME_FONTS ile yazi tipi klasoru ayrica verilebilir)

Kaynak: yerelde kurulu qtawesome paketindeki Font Awesome Free 6.7.2 yazi tipleri (indirme yok).
Lisans: Font Awesome Free, ikonlar CC BY 4.0, yazi tipi SIL OFL 1.1; atif index.html icinde yazilir.
Ornek ekran (platform.deepin.space) ayni ikon ailesini kullaniyor.
"""
import json, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

def _yazi_tipi_klasoru():
    if os.environ.get("QTAWESOME_FONTS"):
        return os.environ["QTAWESOME_FONTS"].rstrip("/") + "/"
    import qtawesome
    return os.path.join(os.path.dirname(qtawesome.__file__), "fonts") + "/"


D = _yazi_tipi_klasoru()
CIKTI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ikonlar.json")
ISTE = {
    "solid": ["house", "bell", "diagram-project", "shield-halved", "network-wired", "user-clock", "database", "cube", "map-pin",
              "paper-plane", "circle-xmark", "arrows-left-right-to-line", "user", "users", "laptop", "server", "globe",
              "magnifying-glass", "arrow-down-wide-short", "check", "robot", "circle-info"],
    "regular": ["newspaper"],
}


def cikar(stil, adlar):
    font = TTFont(D + f"fontawesome6-{stil}-webfont-6.7.2.ttf")
    harita = json.load(open(D + f"fontawesome6-{stil}-webfont-charmap-6.7.2.json"))
    cmap = font.getBestCmap()
    gs = font.getGlyphSet()
    ust = font["hhea"].ascent
    sonuc = {}
    for ad in adlar:
        glif = cmap[int(harita[ad], 16)]
        g = gs[glif]
        pen = SVGPathPen(gs)
        g.draw(TransformPen(pen, (1, 0, 0, -1, 0, ust)))
        sonuc[ad] = {"w": g.width, "y": ust - 448, "d": pen.getCommands()}
    return sonuc


if __name__ == "__main__":
    ikon = {}
    for stil, adlar in ISTE.items():
        ikon.update(cikar(stil, adlar))
    json.dump(ikon, open(CIKTI, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    print(len(ikon), "ikon ->", CIKTI, os.path.getsize(CIKTI) // 1024, "KB")
