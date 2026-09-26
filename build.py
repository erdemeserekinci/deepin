#!/usr/bin/env python3
"""Build the static deepin.space site.

Pages live in src/pages/*.html. Each page starts with a small front-matter block
and uses <!--@component:arg--> markers that are rendered from src/data.json.

    python3 build.py        # writes index.html, risk/, finance/, security/, energy/
"""
import html, json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
DATA = json.load(open(os.path.join(SRC, "data.json"), encoding="utf-8"))
BASE_CSS = open(os.path.join(SRC, "base.css"), encoding="utf-8").read()
BASE_JS = open(os.path.join(SRC, "base.js"), encoding="utf-8").read()
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">')
EMAIL = "info@deepin.space"
ADDRESS = "Erzene Mah. Ankara Cad. EBİLTEM No: 172/14, Bornova / İzmir"

e = html.escape
INV = {i["id"]: i for i in DATA["investigations"]}
SPACE = {s["id"]: s for s in DATA["spaces"]}
STATUS = DATA["status"]


# ---------------------------------------------------------------- primitives
def arrow():
    return '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'


def wordmark(space_id, cls="nm"):
    return f'<span class="{cls}">deep<b>in</b>.{e(space_id)}</span>'


def status_chip(status):
    s = STATUS[status]
    return f'<span class="chip st-{status}">{e(s["label"])}</span>'


def maturity(status):
    lvl = STATUS[status]["level"]
    pips = "".join(f'<i class="{"on" if n < lvl else ""}"></i>' for n in range(3))
    return f'<span class="pips" aria-hidden="true">{pips}</span>'


# ---------------------------------------------------------------- components
def c_investigation_card(inv_id, prefix=""):
    i = INV[inv_id]
    href = prefix + i["href"]
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
    <div><div class="lbl">Investigates</div><ul class="inv-list in">{src}</ul></div>
    <div><div class="lbl">Delivers</div><ul class="inv-list out">{out}</ul></div>
  </div>
  <a class="inv-cta" href="{href}">{e(i["cta"])} →</a>
</article>'''
    return f'''<article class="inv inv-secondary" id="inv-{i["id"]}">
  <header class="inv-head"><h3>{e(i["name"])}</h3>{status_chip(i["status"])}</header>
  <p class="inv-lede">{e(i["headline"])}</p>
  <a class="inv-cta" href="{href}">{e(i["cta"])} →</a>
</article>'''


def c_investigation_catalog(_arg=""):
    prim = "".join(c_investigation_card(i["id"]) for i in DATA["investigations"] if i["weight"] == "primary")
    sec = "".join(c_investigation_card(i["id"]) for i in DATA["investigations"] if i["weight"] == "secondary")
    return f'''<div class="catalog">
  <div class="catalog-primary">{prim}</div>
  <div class="catalog-secondary">{sec}
    <a class="catalog-more" href="#contact"><strong>Don't see your investigation?</strong><span>Most of our work starts with a case nobody has automated yet.</span><span class="go">Tell us what your team investigates →</span></a>
  </div>
</div>'''


def c_proof_grid(arg=""):
    show_logos = DATA.get("proof", {}).get("show_logos", False)
    cards = []
    for c in DATA["customers"]:
        if arg and arg not in c.get("spaces", []):
            continue
        name = (f'<img class="proof-logo" src="{c["logo"]}" alt="{e(c["name"])}">'
                if show_logos and c.get("logo") else f'<strong>{e(c["name"])}</strong>')
        cards.append(f'''<li class="proof-card">
  {name}
  <span class="proof-inv">{e(c["investigation"])}</span>{f'<span class="proof-ctx">{e(c["context"][arg])}</span>' if arg and c.get("context", {}).get(arg) else ""}
  <span class="proof-st">{maturity(c["status"])}{status_chip(c["status"])}</span>
</li>''')
    cls = " n4" if len(cards) == 4 else ""
    return f'<ul class="proof-grid{cls}">{"".join(cards)}</ul>'


def c_proof_legend(_arg=""):
    return ('<div class="proof-legend"><span><span class="pips"><i class="on"></i><i></i><i></i></span>Contracted</span>'
            '<span><span class="pips"><i class="on"></i><i class="on"></i><i></i></span>Embedded or deploying</span>'
            '<span><span class="pips"><i class="on"></i><i class="on"></i><i class="on"></i></span>In production</span></div>')


def c_space_growth(space_id, prefix=""):
    s = SPACE[space_id]
    labels = ["One investigation", "Repeated", "Accumulated"]
    rows, prev = [], set()
    for n, stage in enumerate(s["growth"]):
        chips = "".join(f'<span class="{"" if x in prev else "new"}">{e(x)}</span>' for x in stage)
        prev = set(stage)
        rows.append(f'<li><span class="g-lbl">{labels[n]}</span><span class="g-chips">{chips}</span></li>')
    return f'''<div class="growth">
  <ol class="g-stages">{"".join(rows)}</ol>
  <div class="g-down" aria-hidden="true"></div>
  <a class="g-space" href="{prefix + s["href"]}">
    <span class="g-top">{wordmark(s["id"])}{status_chip(s["status"])}</span>
    <span class="g-title">{e(s["title"])}</span>
    <span class="g-meta"><span>Primary investigation</span><b>{e(s["primary"])}</b></span>
    <span class="g-note">{e(s["note"])}</span>
    <span class="go">Explore {e("deepin." + s["id"])} →</span>
  </a>
</div>'''


def c_spaces_scene(_arg=""):
    proven = "".join(c_space_growth(s["id"]) for s in DATA["spaces"] if s["status"] != "exploring")
    explore = "".join(
        f'<a class="x-space" href="{s["href"]}">{wordmark(s["id"])}<span>{e(s["title"])}</span>{status_chip(s["status"])}</a>'
        for s in DATA["spaces"] if s["status"] == "exploring")
    return f'''<div class="spaces-proven">{proven}</div>
<div class="spaces-explore"><span class="lbl">Exploring</span>{explore}</div>'''


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
CHIP_ICON = {"on-premise": "lock", "air-gapped": "air", "air-gapped deployment": "air", "rbac": "user",
             "role-based access": "user", "audit trail": "doc", "data lineage": "net",
             "policy enforcement": "shield", "evaluations": "check", "human approval": "hand"}
DEFAULT_CHIPS = ["On-premise", "Air-gapped deployment", "Role-based access", "Audit trail",
                 "Data lineage", "Policy enforcement", "Evaluations", "Human approval"]


def c_enterprise_chips(arg="", ctx=None):
    labels = (ctx or {}).get("content", {}).get("enterprise") if arg == "content" else None
    li = "".join(
        f'<li><svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">{ICONS[CHIP_ICON[t.lower()]]}</svg>{e(t)}</li>'
        for t in (labels or DEFAULT_CHIPS))
    return f'<ul class="ent-chips">{li}</ul>'


def c_evidence_rail(arg="", ctx=None):
    if arg == "content":
        steps = [tuple(x) for x in ctx["content"]["rail"]]
        li = "".join(f'<li><span class="n">{n+1:02d}</span><div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>' for n, (t, d) in enumerate(steps))
        return f'<ol class="evidence">{li}</ol>'
    steps = [("Source", "Each finding links to the record, document or system it came from."),
             ("Evidence", "The facts are collected, dated and kept with the case."),
             ("Reasoning", "The logic from evidence to conclusion is written out, with the policy it applies."),
             ("Recommendation", "A proposed decision, never a silent one."),
             ("Human approval", "A person approves, edits or rejects before anything changes.")]
    if arg == "short":
        steps = steps[:4]
    li = "".join(f'<li><span class="n">{n+1:02d}</span><div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>' for n, (t, d) in enumerate(steps))
    return f'<ol class="evidence">{li}</ol>'


def c_data_note(_arg=""):
    return '''<div class="datanote">
  <strong>Your data stays yours.</strong>
  <p>Deepin does not build its advantage by taking customer data. Your records stay yours. What we carry from one deployment to the next is how an investigation is solved:</p>
  <ul class="assets"><li>Investigation templates</li><li>Connector patterns</li><li>Workflows</li><li>Evaluations</li><li>Policy patterns</li><li>Agent capabilities</li></ul>
</div>'''


def c_copy_email(_arg=""):
    return f'''<div class="mail"><code id="email">{EMAIL}</code><button class="copy" id="copyBtn" type="button">Copy email</button></div>'''


COMPONENTS = {
    "investigation_catalog": c_investigation_catalog,
    "proof_grid": c_proof_grid,
    "proof_legend": c_proof_legend,
    "spaces_scene": c_spaces_scene,
    "space_growth": c_space_growth,
    "enterprise_chips": c_enterprise_chips,
    "evidence_rail": c_evidence_rail,
    "data_note": c_data_note,
    "copy_email": c_copy_email,
}


import sys
sys.path.insert(0, SRC)
import risk_components  # noqa: E402

CTX_COMPONENTS = dict(risk_components.COMPONENTS)
CTX_COMPONENTS["enterprise_chips"] = c_enterprise_chips
CTX_COMPONENTS["evidence_rail"] = c_evidence_rail

# ---------------------------------------------------------------- chrome
def logo_imgs(prefix):
    return (f'<img class="logo-l" src="{prefix}assets/deepin-logo.png" alt="deepin" width="632" height="190">'
            f'<img class="logo-d" src="{prefix}assets/deepin-logo-mint.png" alt="deepin" width="652" height="194">')


def nav(page, prefix, sub, cta, cta_href="#contact", back_label="← deepin.space"):
    links = "".join(f'<a href="{h}">{e(t)}</a>' for t, h in DATA["nav"][page])
    home = "#top" if page == "home" else prefix
    subspan = f'<span class="sub">.{e(sub)}</span>' if sub else ""
    back = "" if page == "home" else f'<a class="back" href="{prefix}">{e(back_label)}</a>'
    login = '<a class="login" href="https://platform.deepin.space">Log in</a>' if page == "home" else ""
    return f'''<header class="nav" id="top">
  <div class="wrap">
    <a class="brand" href="{home}" aria-label="Deepin home">{logo_imgs(prefix)}{subspan}</a>
    <nav class="nav-links" aria-label="Main">{links}</nav>
    <div class="nav-cta">{back}{login}<a class="btn btn-primary btn-sm" href="{cta_href}">{e(cta)}</a></div>
  </div>
</header>'''


def footer(page, prefix, sub):
    home = "#top" if page == "home" else prefix
    subspan = f'<span class="sub">.{e(sub)}</span>' if sub else ""
    spaces = "".join(f'<a href="{prefix}{s["href"]}">deepin.{s["id"]}</a>' for s in DATA["spaces"])
    return f'''<footer id="company">
  <div class="wrap">
    <div class="f-about">
      <a class="brand" href="{home}" aria-label="Deepin home">{logo_imgs(prefix)}{subspan}</a>
      <p>Deepin builds Enterprise Investigation &amp; Decision Automation: agents that investigate business cases, show the evidence and wait for a person to approve.</p>
      <span class="addr">{ADDRESS}</span>
    </div>
    <nav class="f-col" aria-label="Spaces"><span class="lbl">Spaces</span>{spaces}</nav>
    <nav class="f-col" aria-label="Company"><span class="lbl">Company</span>
      <a href="{prefix}#customers">Customers</a><a href="{prefix}#enterprise">Enterprise</a>
      <a href="https://platform.deepin.space">Log in</a>
      <a href="https://www.linkedin.com/company/93368167">LinkedIn</a><a href="https://www.youtube.com/@deepin--space">YouTube</a>
    </nav>
    <div class="f-col"><span class="lbl">Contact</span><span>{EMAIL}</span><span class="f-copy">© 2026 Deepin</span></div>
  </div>
</footer>'''


# ---------------------------------------------------------------- pages
PAGES = [
    dict(src="home.html", out="", nav="home", sub="", cta="Bring us an investigation"),
    dict(src="risk.html", out="risk/", nav="risk", sub="risk", cta="Run an Investigation", cta_href="#request",
         back="Deepin →", content="risk.en.json"),
    dict(src="finance.html", out="finance/", nav="finance", sub="finance", cta="Request a demo"),
    dict(src="security.html", out="security/", nav="security", sub="security", cta="Bring us a case"),
    dict(src="energy.html", out="energy/", nav="energy", sub="energy", cta="Bring us a case"),
]


def front_matter(txt):
    m = re.match(r"<!--\s*\n(.*?)\n-->\n", txt, re.S)
    meta = {}
    for line in m.group(1).splitlines():
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip()
    return meta, txt[m.end():]


def render(body, prefix, content=None):
    ctx = {"prefix": prefix, "content": content or {}}
    copy = ctx["content"].get("copy", {})
    body = re.sub(r"\{\{(\w+)\}\}", lambda m: copy[m.group(1)], body)

    def rep(m):
        name, _, arg = m.group(1).partition(":")
        if name in CTX_COMPONENTS and (arg == "content" or name in risk_components.COMPONENTS):
            return CTX_COMPONENTS[name](arg, ctx)
        fn = COMPONENTS[name]
        return fn(arg, prefix) if name == "space_growth" else fn(arg)
    return re.sub(r"<!--@([\w:.-]+)-->", rep, body)


def build():
    written = []
    for P in PAGES:
        src, out, key, sub, cta = P["src"], P["out"], P["nav"], P["sub"], P["cta"]
        prefix = "../" * out.count("/")
        content = json.load(open(os.path.join(SRC, "content", P["content"]), encoding="utf-8")) if P.get("content") else {}
        lang = content.get("lang", "en")
        meta, body = front_matter(open(os.path.join(SRC, "pages", src), encoding="utf-8").read())
        meta = {k: re.sub(r"\{\{(\w+)\}\}", lambda m: content["copy"][m.group(1)], v) for k, v in meta.items()}
        style = ""
        m = re.search(r"<style>(.*?)</style>\s*", body, re.S)
        if m:
            style, body = m.group(1), body[:m.start()] + body[m.end():]
        body = render(body, prefix, content)
        css = BASE_CSS.replace("url(\"assets/", f"url(\"{prefix}assets/") + style
        url = f"https://deepin.space/{out}"
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
<meta property="og:image" content="https://deepin.space/assets/waves.jpg">
<meta name="theme-color" content="#F7FAF9">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" href="{prefix}assets/favicon-64.png">
<link rel="apple-touch-icon" href="{prefix}assets/favicon.png">
{FONTS}
<style>
{css}
</style>
</head>
<body>
{nav(key, prefix, sub, cta, P.get("cta_href", "#contact"), P.get("back", "← deepin.space"))}
<main>
{body.strip()}
</main>
{footer(key, prefix, sub)}
<script>
{BASE_JS}
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
