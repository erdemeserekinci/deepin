#!/usr/bin/env python3
"""Build the static deepin.space site in Turkish (default) and English.

    python3 build.py

Output
  Turkish (default)  index.html, risk/, finance/, security/, energy/, harness/
  English            en/index.html, en/risk/, en/finance/, en/security/, en/energy/, en/harness/

Sources (src/)
  data.<lang>.json         investigations, spaces, customers, status labels, navigation
  i18n/ui.json             shared interface strings used by components, nav and footer
  pages/<lang>/<page>.html page body per language (front matter + markup)
  pages/<page>.html        page body shared by all languages, text from content/<page>.<lang>.json
  content/<page>.<lang>.json  text and demo data for shared pages ({{key}} placeholders)
  styles/<page>.css        page styles, shared by all languages
  base.css, base.js        design system and interactions

Pages use <!--@component:arg--> markers; components are defined below and in
src/risk_components.py and src/harness_components.py. %ROOT% in a page is the
relative path to that language's home page.
"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
sys.path.insert(0, SRC)
import risk_components  # noqa: E402
import harness_components  # noqa: E402
import organism_components  # noqa: E402

LOCALES = [("tr", ""), ("en", "en/")]          # (language, output folder); first is the default
PAGES = ["home", "risk", "finance", "security", "energy", "harness"]
PAGE_DIR = {"home": ""}                        # output folder per page inside a locale
SUB = {"home": "", "harness": " harness"}     # sub-brand after the logo (".risk"; a leading space means a word, not a Space)

BASE_CSS = open(os.path.join(SRC, "base.css"), encoding="utf-8").read() + "\n" + open(os.path.join(SRC, "organism.css"), encoding="utf-8").read()
BASE_JS = open(os.path.join(SRC, "base.js"), encoding="utf-8").read()
UI_ALL = json.load(open(os.path.join(SRC, "i18n", "ui.json"), encoding="utf-8"))
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">')
EMAIL = "info@deepin.space"
ADDRESS = "Erzene Mah. Ankara Cad. EBİLTEM No: 172/14, Bornova / İzmir"
e = html.escape

# Set per locale in build()
DATA, INV, SPACE, STATUS, UI = {}, {}, {}, {}, {}


def set_locale(lang):
    global DATA, INV, SPACE, STATUS, UI
    DATA = json.load(open(os.path.join(SRC, f"data.{lang}.json"), encoding="utf-8"))
    INV = {i["id"]: i for i in DATA["investigations"]}
    SPACE = {s["id"]: s for s in DATA["spaces"]}
    STATUS = DATA["status"]
    UI = UI_ALL[lang]


# ---------------------------------------------------------------- primitives
def wordmark(space_id, cls="nm"):
    return f'<span class="{cls}">deep<b>in</b>.{e(space_id)}</span>'


def status_chip(status):
    return f'<span class="chip st-{status}">{e(STATUS[status]["label"])}</span>'


def maturity(status):
    lvl = STATUS[status]["level"]
    pips = "".join(f'<i class="{"on" if n < lvl else ""}"></i>' for n in range(3))
    return f'<span class="pips" aria-hidden="true">{pips}</span>'


ICONS = {
    "lock": '<rect x="3" y="8" width="12" height="8" rx="2"/><path d="M6 8V6a3 3 0 016 0v2"/>',
    "air": '<path d="M3 6h9a2 2 0 100-4M3 12h11a2 2 0 110 4M3 9h6"/>',
    "user": '<circle cx="9" cy="6" r="3"/><path d="M3 16c1-3 3.5-4.5 6-4.5s5 1.5 6 4.5"/>',
    "doc": '<path d="M4 3h10v12H4z"/><path d="M7 7h4M7 10h4"/>',
    "net": '<circle cx="4" cy="9" r="2"/><circle cx="14" cy="4" r="2"/><circle cx="14" cy="14" r="2"/><path d="M6 8l6-3M6 10l6 3"/>',
    "shield": '<path d="M9 2l6 3v4c0 4-3 6-6 7-3-1-6-3-6-7V5z"/>',
    "check": '<path d="M3 9.5l3.5 3.5L15 5"/>',
    "hand": '<path d="M6 9V4a1.2 1.2 0 012.4 0v4M8.4 8V3a1.2 1.2 0 012.4 0v5M10.8 8V4.5a1.2 1.2 0 012.4 0V11c0 3-2 5-4.5 5S4 14.5 3.5 12L2.8 9.6a1.1 1.1 0 012-.8L6 11"/>',
}


# ---------------------------------------------------------------- components
def c_investigation_card(inv_id, ctx):
    i = INV[inv_id]
    href = i["href"]
    if i["weight"] == "primary":
        src = "".join(f"<li>{e(x)}</li>" for x in i["sources"])
        out = "".join(f"<li>{e(x)}</li>" for x in i["outputs"])
        return f'''<article class="inv inv-primary" id="inv-{i["id"]}">
  <header class="inv-head">
    <div><h3>{e(i["name"])}</h3><p class="inv-space">{wordmark(i["space"], "nm-sm")}</p></div>
    {status_chip(i["status"])}
  </header>
  <p class="inv-lede">{e(i["headline"])}</p>
  <div class="inv-cols">
    <div><div class="lbl">{e(UI["investigates"])}</div><ul class="inv-list in">{src}</ul></div>
    <div><div class="lbl">{e(UI["delivers"])}</div><ul class="inv-list out">{out}</ul></div>
  </div>
  <a class="inv-cta" href="{href}">{e(i["cta"])} →</a>
</article>'''
    return f'''<article class="inv inv-secondary" id="inv-{i["id"]}">
  <header class="inv-head"><h3>{e(i["name"])}</h3>{status_chip(i["status"])}</header>
  <p class="inv-lede">{e(i["headline"])}</p>
  <a class="inv-cta" href="{href}">{e(i["cta"])} →</a>
</article>'''


def c_investigation_catalog(arg, ctx):
    prim = "".join(c_investigation_card(i["id"], ctx) for i in DATA["investigations"] if i["weight"] == "primary")
    sec = "".join(c_investigation_card(i["id"], ctx) for i in DATA["investigations"] if i["weight"] == "secondary")
    return f'''<div class="catalog">
  <div class="catalog-primary">{prim}</div>
  <div class="catalog-secondary">{sec}
    <a class="catalog-more" href="#contact"><strong>{e(UI["more_title"])}</strong><span>{e(UI["more_text"])}</span><span class="go">{e(UI["more_cta"])}</span></a>
  </div>
</div>'''


def c_proof_grid(arg, ctx):
    show_logos = DATA.get("proof", {}).get("show_logos", False)
    cards = []
    for c in DATA["customers"]:
        if arg and arg not in c.get("spaces", []):
            continue
        name = (f'<img class="proof-logo" src="{ctx["assets"]}{c["logo"]}" alt="{e(c["name"])}">'
                if show_logos and c.get("logo") else f'<strong>{e(c["name"])}</strong>')
        extra = f'<span class="proof-ctx">{e(c["context"][arg])}</span>' if arg and c.get("context", {}).get(arg) else ""
        cards.append(f'''<li class="proof-card">
  {name}
  <span class="proof-inv">{e(c["investigation"])}</span>{extra}
  <span class="proof-st">{maturity(c["status"])}{status_chip(c["status"])}</span>
</li>''')
    cls = " n4" if len(cards) == 4 else ""
    return f'<ul class="proof-grid{cls}">{"".join(cards)}</ul>'


def c_proof_space(space_id, ctx):
    """Customers whose first Space is space_id, grouped under that Space and its primary Investigation."""
    s = SPACE[space_id]
    rows = "".join(
        f'<li><strong>{e(c["name"])}</strong><span class="proof-st">{maturity(c["status"])}{status_chip(c["status"])}</span></li>'
        for c in DATA["customers"] if c.get("spaces", [None])[0] == space_id)
    return f'''<div class="pf-group">
  <a class="pf-h" href="{ctx["root"]}{s["href"]}">{wordmark(space_id)}<span>{e(s["primary"])}</span></a>
  <ul>{rows}</ul>
</div>'''


def c_proof_legend(arg, ctx):
    a, b, c = (e(x) for x in UI["legend"])
    return (f'<div class="proof-legend"><span><span class="pips"><i class="on"></i><i></i><i></i></span>{a}</span>'
            f'<span><span class="pips"><i class="on"></i><i class="on"></i><i></i></span>{b}</span>'
            f'<span><span class="pips"><i class="on"></i><i class="on"></i><i class="on"></i></span>{c}</span></div>')


def c_space_growth(space_id, ctx):
    s = SPACE[space_id]
    rows, prev = [], set()
    for n, stage in enumerate(s["growth"]):
        chips = "".join(f'<span class="{"" if x in prev else "new"}">{e(x)}</span>' for x in stage)
        prev = set(stage)
        rows.append(f'<li><span class="g-lbl">{e(UI["growth_labels"][n])}</span><span class="g-chips">{chips}</span></li>')
    return f'''<div class="growth">
  <ol class="g-stages">{"".join(rows)}</ol>
  <div class="g-down" aria-hidden="true"></div>
  <a class="g-space" href="{s["href"]}">
    <span class="g-top">{wordmark(s["id"])}{status_chip(s["status"])}</span>
    <span class="g-title">{e(s["title"])}</span>
    <span class="g-meta"><span>{e(UI["primary"])}</span><b>{e(s["primary"])}</b></span>
    <span class="g-note">{e(s["note"])}</span>
    <span class="go">{e(UI["explore_space"].format(name="deepin." + s["id"]))}</span>
  </a>
</div>'''


def c_spaces_scene(arg, ctx):
    proven = "".join(c_space_growth(s["id"], ctx) for s in DATA["spaces"] if s["status"] != "exploring")
    explore = "".join(
        f'<a class="x-space" href="{s["href"]}">{wordmark(s["id"])}<span>{e(s["title"])}</span>{status_chip(s["status"])}</a>'
        for s in DATA["spaces"] if s["status"] == "exploring")
    return f'''<div class="spaces-proven">{proven}</div>
<div class="spaces-explore"><span class="lbl">{e(UI["exploring"])}</span>{explore}</div>'''


def c_enterprise_chips(arg, ctx):
    chips = ctx["content"].get("enterprise") if arg == "content" else UI["chips"]
    li = "".join(
        f'<li><svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">{ICONS[k]}</svg>{e(t)}</li>'
        for k, t in chips)
    return f'<ul class="ent-chips">{li}</ul>'


def c_evidence_rail(arg, ctx):
    steps = ctx["content"]["rail"] if arg == "content" else UI["rail"]
    if arg == "short":
        steps = steps[:4]
    li = "".join(f'<li><span class="n">{n+1:02d}</span><div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>' for n, (t, d) in enumerate(steps))
    return f'<ol class="evidence">{li}</ol>'


def c_data_note(arg, ctx):
    assets = "".join(f"<li>{e(a)}</li>" for a in UI["data_assets"])
    return f'''<div class="datanote">
  <strong>{e(UI["data_h"])}</strong>
  <p>{e(UI["data_p"])}</p>
  <ul class="assets">{assets}</ul>
</div>'''


def c_copy_email(arg, ctx):
    return (f'<div class="mail"><code id="email">{EMAIL}</code><button class="copy" id="copyBtn" type="button" '
            f'data-copied="{e(UI["copied"])}" data-selected="{e(UI["selected"])}">{e(UI["copy"])}</button></div>')


COMPONENTS = {
    "investigation_catalog": c_investigation_catalog,
    "proof_grid": c_proof_grid,
    "proof_legend": c_proof_legend,
    "proof_space": c_proof_space,
    "spaces_scene": c_spaces_scene,
    "space_growth": c_space_growth,
    "enterprise_chips": c_enterprise_chips,
    "evidence_rail": c_evidence_rail,
    "data_note": c_data_note,
    "copy_email": c_copy_email,
}
COMPONENTS.update(risk_components.COMPONENTS)
COMPONENTS.update(harness_components.COMPONENTS)
COMPONENTS.update(organism_components.COMPONENTS)


# ---------------------------------------------------------------- chrome
def logo_imgs(assets):
    return (f'<img class="logo-l" src="{assets}assets/deepin-logo.png" alt="deepin" width="632" height="190">'
            f'<img class="logo-d" src="{assets}assets/deepin-logo-mint.png" alt="deepin" width="652" height="194">')


def sub_brand(page):
    sub = SUB.get(page, "." + page)
    if not sub:
        return ""
    if sub.startswith(" "):
        return f'<span class="sub sub-word">{e(sub.strip())}</span>'
    return f'<span class="sub">{e(sub)}</span>'


def lang_switch(ctx):
    links = []
    for lang, _ in LOCALES:
        cur = lang == ctx["lang"]
        attrs = ' aria-current="true"' if cur else ""
        links.append(f'<a href="{ctx["alt"][lang]}" hreflang="{lang}" lang="{lang}"{attrs} title="{e(UI_ALL[lang]["lang_name"])}">{lang.upper()}</a>')
    return f'<span class="langs" role="group" aria-label="{e(UI["aria_lang"])}">{"".join(links)}</span>'


def nav(page, ctx):
    """One global navigation on every page: Deepin, the two Spaces, Harness, customers."""
    root = ctx["root"]
    home = "#top" if page == "home" else root
    items = [("home", "Deepin", root or "./"), ("risk", "deepin.risk", f"{root}risk/"),
             ("finance", "deepin.finance", f"{root}finance/"), ("harness", "Harness", f"{root}harness/"),
             ("customers", UI["customers"], f"{root}#customers" if root else "#customers")]
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{h}"{cur if k == page else ""}>{e(t)}</a>' for k, t, h in items)
    login = f'<a class="login" href="https://platform.deepin.space">{e(UI["login"])}</a>' if page == "home" else ""
    cta_href = "#request" if page == "risk" else "#contact"
    return f'''<header class="nav" id="top">
  <div class="wrap">
    <a class="brand" href="{home}" aria-label="{e(UI["home_label"])}">{logo_imgs(ctx["assets"])}{sub_brand(page)}</a>
    <nav class="nav-links" aria-label="{e(UI["aria_main"])}">{links}</nav>
    <div class="nav-cta">{lang_switch(ctx)}{login}<a class="btn btn-primary btn-sm" href="{cta_href}">{e(UI["cta"][page])}</a>
      <details class="menu"><summary aria-label="{e(UI["aria_main"])}"><span></span><span></span></summary><nav class="menu-panel" aria-label="{e(UI["aria_main"])}">{links}<a class="menu-cta" href="{cta_href}">{e(UI["cta"][page])} →</a></nav></details>
    </div>
  </div>
</header>'''


def footer(page, ctx):
    root = ctx["root"]
    home = "#top" if page == "home" else root
    subspan = sub_brand(page)
    spaces = "".join(f'<a href="{root}{s["href"]}">deepin.{s["id"]}</a>' for s in DATA["spaces"])
    return f'''<footer id="company">
  <div class="wrap">
    <div class="f-about">
      <a class="brand" href="{home}" aria-label="{e(UI["home_label"])}">{logo_imgs(ctx["assets"])}{subspan}</a>
      <p>{e(UI["footer_about"])}</p>
      <span class="addr">{ADDRESS}</span>
    </div>
    <nav class="f-col" aria-label="{e(UI["footer_spaces"])}"><span class="lbl">{e(UI["footer_spaces"])}</span>{spaces}</nav>
    <nav class="f-col" aria-label="{e(UI["footer_company"])}"><span class="lbl">{e(UI["footer_company"])}</span>
      <a href="{root}harness/">Deepin Harness</a><a href="{root}#customers">{e(UI["customers"])}</a><a href="{root}#enterprise">{e(UI["enterprise"])}</a>
      <a href="https://platform.deepin.space">{e(UI["login"])}</a>
      <a href="https://www.linkedin.com/company/93368167">LinkedIn</a><a href="https://www.youtube.com/@deepin--space">YouTube</a>
    </nav>
    <div class="f-col"><span class="lbl">{e(UI["footer_contact"])}</span><span>{EMAIL}</span><span class="f-copy">© 2026 Deepin</span>{lang_switch(ctx)}</div>
  </div>
</footer>'''



# English product terms inside Turkish pages are marked lang="en", so uppercase
# labels render "INVESTIGATION" rather than the Turkish-cased "INVESTİGATİON".
EN_TERMS = re.compile(r"\b(deepin\.[a-z]+|Deepin|Investigation|Enterprise|Decision|Automation|Continuous|Monitoring|"
                      r"Security|Operational|Supplier|Harness|On-premise|Air-gapped|Fintech|fintech|Company|Organizational|Reasoning)\b")


def mark_english(markup):
    parts = re.split(r"(<[^>]+>)", markup)
    skip = False
    for i, p in enumerate(parts):
        if p.startswith("<"):
            t = p[1:].split(None, 1)[0].lower() if len(p) > 2 else ""
            if t in ("script", "style", "textarea", "title"):
                skip = True
            elif t in ("/script", "/style", "/textarea", "/title"):
                skip = False
            continue
        if not skip and p.strip():
            parts[i] = EN_TERMS.sub(r'<span lang="en">\1</span>', p)
    return "".join(parts)

# ---------------------------------------------------------------- pages
def front_matter(txt):
    m = re.match(r"<!--\s*\n(.*?)\n-->\n", txt, re.S)
    meta = {}
    for line in m.group(1).splitlines():
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip()
    return meta, txt[m.end():]


def fill(text, content):
    copy = content.get("copy", {})
    return re.sub(r"\{\{(\w+)\}\}", lambda m: copy[m.group(1)], text)


def render(body, ctx):
    body = fill(body, ctx["content"]).replace("%ROOT%", ctx["root"])

    def rep(m):
        name, _, arg = m.group(1).partition(":")
        return COMPONENTS[name](arg, ctx)
    return re.sub(r"<!--@([\w:.-]+)-->", rep, body)


def page_path(lang_dir, page):
    return lang_dir + PAGE_DIR.get(page, page + "/")


def build():
    written = []
    for lang, lang_dir in LOCALES:
        set_locale(lang)
        for page in PAGES:
            out = page_path(lang_dir, page)
            depth = out.count("/")
            page_depth = PAGE_DIR.get(page, page + "/").count("/")
            ctx = {
                "lang": lang,
                "ui": UI,
                "assets": "../" * depth,          # to the site root (shared assets)
                "root": "../" * page_depth,       # to this language's home page
                "alt": {l: "../" * depth + page_path(d, page) for l, d in LOCALES},
            }
            src = os.path.join(SRC, "pages", lang, f"{page}.html")
            if not os.path.exists(src):
                src = os.path.join(SRC, "pages", f"{page}.html")
            cpath = os.path.join(SRC, "content", f"{page}.{lang}.json")
            ctx["content"] = json.load(open(cpath, encoding="utf-8")) if os.path.exists(cpath) else {}
            risk_components.set_locale(ctx["content"])
            organism_components.set_data(DATA, STATUS)

            meta, body = front_matter(open(src, encoding="utf-8").read())
            meta = {k: fill(v, ctx["content"]) for k, v in meta.items()}
            body = render(body, ctx).replace('src="assets/', f'src="{ctx["assets"]}assets/').replace('poster="assets/', f'poster="{ctx["assets"]}assets/')
            chrome_nav, chrome_footer = nav(page, ctx), footer(page, ctx)
            if lang == "tr":
                body, chrome_nav, chrome_footer = (mark_english(x) for x in (body, chrome_nav, chrome_footer))
            style = open(os.path.join(SRC, "styles", f"{page}.css"), encoding="utf-8").read()
            css = BASE_CSS.replace('url("assets/', f'url("{ctx["assets"]}assets/') + "\n" + style
            jpath = os.path.join(SRC, "scripts", f"{page}.js")
            page_js = open(jpath, encoding="utf-8").read() if os.path.exists(jpath) else ""
            url = f"https://deepin.space/{out}"
            alternates = "\n".join(f'<link rel="alternate" hreflang="{l}" href="https://deepin.space/{page_path(d, page)}">' for l, d in LOCALES)
            alternates += f'\n<link rel="alternate" hreflang="x-default" href="https://deepin.space/{page_path(LOCALES[0][1], page)}">'
            # honour a language the visitor picked with the TR/EN switch (set in base.js)
            alt_json = json.dumps({l: u for l, u in ctx["alt"].items() if l != lang})
            alternates += ('\n<script>(function(){try{var s=localStorage.getItem("deepin-lang"),a=' + alt_json +
                           ';if(s&&a[s]){var u=a[s];if(!/(^|\\.)deepin\\.space$/.test(location.hostname)&&/\\/$/.test(u))u+="index.html";'
                           'location.replace(u+location.hash)}}catch(e){}})()</script>')
            doc = f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(meta["title"])}</title>
<meta name="description" content="{e(meta["description"])}">
<meta property="og:title" content="{e(meta["title"])}">
<meta property="og:description" content="{e(meta["description"])}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{"tr_TR" if lang == "tr" else "en_US"}">
<meta property="og:image" content="https://deepin.space/assets/waves.jpg">
<meta name="theme-color" content="#F7FAF9">
<meta name="generator" content="deepin/organism">
<link rel="canonical" href="{url}">
{alternates}
<link rel="icon" type="image/png" href="{ctx["assets"]}assets/favicon-64.png">
<link rel="apple-touch-icon" href="{ctx["assets"]}assets/favicon.png">
{FONTS}
<style>
{css}
</style>
</head>
<body class="pg-{page}">
{chrome_nav}
<main>
{body.strip()}
</main>
{chrome_footer}
<script>
{BASE_JS}
{page_js}
</script>
</body>
</html>
'''
            path = os.path.join(ROOT, out, "index.html")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, "w", encoding="utf-8").write(doc)
            written.append(out + "index.html")
    print("built:", ", ".join(written))


if __name__ == "__main__":
    build()
