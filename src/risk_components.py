"""deepin.risk components.

Every component takes (arg, ctx); ctx["content"] is the page content file
(src/content/risk.<lang>.json). User-facing text lives in that file, so a Turkish
page only needs risk.tr.json.

Components, roughly in page order:
  trust_strip                 hero: compliance badges under the buttons
  hero_depth                  hero: one case, surface (monitoring tool) -> deeper findings -> risk + recommendation
  living_investigation        static report vs CompanyTimeline (clickable events)
  evidence_chain              Source -> ... -> Human decision
  roles                       Deepin investigates, your team decides
  risk_context_change         EvidenceCard / ReasoningTrail / RecommendationCard / HumanApproval
  what_changed                tabs: RelationshipGraph, OwnershipChange, AuthorityChange, financial timeline
  value_chain                 company data + deepin.risk = your decision
  sectors                     one Company Intelligence capability, a decision per sector
  risk_customers              customer cards with a quote each (draft quotes are tagged)
  get_started                 three steps before the contact band
  request_form                Company Intelligence request (inline on desktop, sheet on mobile)

All company and person names are role names (Tedarikçi A.Ş., Yetkili X ...), never real or
realistic ones.
"""
import json
import os
from html import escape as e


UI = {}


def _u(key, default):
    return UI.get(key, default)


def set_locale(content):
    """Point the module at the current page's UI strings (content["ui"])."""
    global UI
    UI = content.get("ui", {})


def _risk(level):
    return f'<span class="risk r-{level.lower()}">{e(_u("levels", {}).get(level, level))}</span>'


def _see_evidence(label, ev):
    return (f'<details class="see-ev"><summary>{e(label)}</summary>'
            f'<div class="see-ev-body"><small>{e(ev["source"])}</small><p>{e(ev["excerpt"])}</p></div></details>')


# ------------------------------------------------------------------ hero
def _wm(name):
    return f'deep<b>in</b>.{e(name.split(".", 1)[1])}' if name.startswith("deepin.") else e(name)


def hero_depth(arg, ctx):
    """Surface to depth: what a monitoring tool sees on top, what Deepin finds further down."""
    H, t = ctx["content"]["hero_depth"], ctx["content"]["copy"]
    layers = []
    for i, x in enumerate(H["layers"]):
        meta = f'<small>{e(x["meta"])}</small>' if x.get("meta") else ""
        layers.append(f'<li class="dl{" top" if i == 0 else ""}" style="--d:{i}" data-s="{i}"><span class="dl-k">{e(x["k"])}</span><p>{e(x["text"])}</p>{meta}</li>')
    n = len(H["layers"])
    labels = e(json.dumps(H["status"], ensure_ascii=False))
    return f'''<figure class="case hd" data-live data-labels="{labels}" aria-label="{e(_u("aria_depth", "One case, from the surface to depth (demo)"))}">
  <div class="case-top hd-top">
    <div><span class="lbl">{e(H["mode"])}</span><strong>{e(H["company"])}</strong></div>
    <span class="chip st-wait" data-live-status>{e(H["status"][-1])}</span>
  </div>
  <div class="case-body">
    <ol class="dls">{"".join(layers)}</ol>
    <div class="dl-bottom" data-s="{n}">
      <span class="dl-k">{e(H["bottom"])}</span>
      <div class="dl-risk"><span class="lbl">{e(H["risk_label"])}</span>{_risk(H["risk_from"])}<span aria-hidden="true">→</span>{_risk(H["risk_to"])}</div>
      <div class="dl-rec"><span class="lbl">{e(H["rec_label"])}</span><strong>{e(H["rec"])}</strong><small>{e(H["ev_meta"])}</small></div>
      <a class="dl-link" href="#evidence">{e(H["link"])} →</a>
    </div>
  </div>
  <figcaption class="case-note">{e(t["demo_note"])}</figcaption>
</figure>'''


# ------------------------------------------------------------------ living investigation
def living_investigation(arg, ctx):
    R, T, t = ctx["content"]["report"], ctx["content"]["timeline"], ctx["content"]["copy"]
    rows = "".join(f'<li>{e(r)}<span aria-hidden="true">✓</span></li>' for r in R["rows"])
    report = f'''<div class="rep">
  <span class="lbl">{e(R["label"])}</span>
  <div class="rep-doc">
    <div class="rep-head"><small>{e(R["month"])}</small><b>{e(R["title"])}</b></div>
    <ul>{rows}</ul>
    <div class="rep-risk"><span class="lbl">{e(_u("risk", "Risk"))}</span>{_risk(R["risk"])}</div>
    <span class="rep-stale">{e(R["stale"])}</span>
  </div>
</div>'''
    n = len(T["ticks"]) - 1
    pos = lambda i: f"{i / n * 100:.4g}%"
    ticks = "".join(f'<span style="--x:{pos(i)}">{e(m)}</span>' for i, m in enumerate(T["ticks"]))
    pts = [f'<li class="lt-pt start" style="--x:0%"><span class="lt-dot"></span><span class="lt-lbl"><b>{e(T["start"]["label"])}</b>{_risk(T["start"]["risk"])}</span></li>']
    panels = []
    for i, ev in enumerate(T["events"]):
        cls = " end" if ev["tick"] == n else ""
        sel = " sel" if i == len(T["events"]) - 1 else ""
        pts.append(f'''<li class="lt-pt{cls}" style="--x:{pos(ev["tick"])}"><button type="button" class="lt-btn{sel}" data-ev="{i}" aria-pressed="{"true" if sel else "false"}"><span class="lt-dot"></span><span class="lt-lbl"><small>{e(ev["date"])}</small><b>{e(ev["change"])}</b></span></button></li>''')
        change = (f'{_risk(ev["risk_from"])}<span aria-hidden="true">→</span>{_risk(ev["risk_to"])}' if ev["risk_from"] != ev["risk_to"] else _risk(ev["risk_to"]))
        panels.append(f'''<div class="lt-panel" data-panel="{i}"{"" if sel else " hidden"}>
  <div class="lt-ba"><div><span class="lbl">{e(T["before_label"])}</span><p>{e(ev["before"])}</p></div><span class="lt-arrow" aria-hidden="true">→</span><div class="after"><span class="lbl">{e(T["after_label"])}</span><p>{e(ev["after"])}</p></div></div>
  <div class="lt-meta"><span class="lt-re">↻ {e(T["reopened"])}</span><span class="lt-risk"><span class="lbl">{e(T["risk_label"])}</span>{change}</span><small>{e(ev["source"])}</small></div>
</div>''')
    return f'''<div class="liv">
  {report}
  <div class="liv-tl">
    <div class="liv-head"><span class="lbl">{e(_u("living", "Living investigation"))}</span><strong>{e(T["company"])}</strong><small class="liv-hint">{e(t["mon_hint"])}</small></div>
    <div class="lt-axis" aria-hidden="true">{ticks}</div>
    <ol class="lt-track">{"".join(pts)}</ol>
    <div class="lt-panels" aria-live="polite">{"".join(panels)}</div>
  </div>
</div>'''


# ------------------------------------------------------------------ what changed
def _ownership(o):
    def bar(parts):
        segs = "".join(
            f'<span class="own-seg{" new" if len(x) > 2 and x[2] else ""}" style="flex:{x[1]}"><b>{x[1]:g}%</b><small>{e(x[0])}</small></span>'
            for x in parts)
        return f'<div class="own-bar">{segs}</div>'
    return f'''<div class="viz own"><div class="own-row"><span class="lbl">{e(_u("before", "Before"))}</span>{bar(o["before"])}</div><div class="own-row"><span class="lbl">{e(_u("after", "After"))}</span>{bar(o["after"])}</div></div>'''


def _authority(a):
    def card(x, cls):
        ppl = "".join(f"<li>{e(p)}</li>" for p in x["people"])
        return f'<div class="auth-card {cls}"><span class="lbl">{e(x["label"])}</span><b>{e(x["rule"])}</b><ul>{ppl}</ul></div>'
    return f'<div class="viz auth">{card(a["before"], "was")}<span class="auth-arrow" aria-hidden="true">→</span>{card(a["after"], "now")}</div>'


def _graph(g):
    N = {n["id"]: n for n in g["nodes"]}
    edges = []
    for ed in g["edges"]:
        a, b, lbl = N[ed[0]], N[ed[1]], ed[2]
        new = len(ed) > 3
        mx, my = (a["x"] + b["x"]) / 2, (a["y"] + b["y"]) / 2
        edges.append(f'<line class="ge{" new" if new else ""}" x1="{a["x"]}" y1="{a["y"]}" x2="{b["x"]}" y2="{b["y"]}"/>'
                     f'<text class="gel" x="{mx}" y="{my - 6}" text-anchor="middle">{e(lbl)}</text>')
    nodes = []
    for n in g["nodes"]:
        w = max(96, len(n["label"]) * 7.4 + 22)
        nodes.append(f'''<g class="gn {n["kind"]}" tabindex="0" role="button" data-info="{e(n["info"])}" aria-label="{e(n["label"])}">
  <rect x="{n["x"] - w / 2:.0f}" y="{n["y"] - 15}" width="{w:.0f}" height="30" rx="15"/>
  <text x="{n["x"]}" y="{n["y"] + 4}" text-anchor="middle">{e(n["label"])}</text></g>''')
    return f'''<div class="viz rgraph">
  <svg viewBox="0 0 360 250" role="group" aria-label="{e(_u("aria_graph", "Relationship graph"))}">{"".join(edges)}{"".join(nodes)}</svg>
  <p class="rg-info" aria-live="polite"><span class="lbl">{e(g["hint"])}</span></p>
</div>'''


def _financial(f):
    li = "".join(f'<li class="{"hot" if x.get("hot") else ""}"><small>{e(x["date"])}</small><span>{e(x["text"])}</span></li>' for x in f)
    return f'<ol class="viz fin">{li}</ol>'


def what_changed(arg, ctx):
    """Four dimensions as tabs; without JS every panel stays visible."""
    t = ctx["content"]["copy"]
    tabs, panels = [], []
    for i, d in enumerate(ctx["content"]["dimensions"]):
        items = "".join(f"<li>{e(x)}</li>" for x in d["items"])
        viz = {"ownership": lambda: _ownership(d["ownership"]), "authority": lambda: _authority(d["authority"]),
               "graph": lambda: _graph(d["graph"]), "financial": lambda: _financial(d["financial"])}[d["visual"]]()
        note = f'<p class="dim-note">{e(d["note"])}</p>' if d.get("note") else ""
        sel = "true" if i == 0 else "false"
        tabs.append(f'<button type="button" role="tab" id="dt-{i}" aria-controls="dp-{i}" aria-selected="{sel}" tabindex="{0 if i == 0 else -1}">{e(d["tab"])}</button>')
        panels.append(f'''<article class="dim" role="tabpanel" id="dp-{i}" aria-labelledby="dt-{i}">
  <div class="dim-q"><span class="dim-key">{e(d["key"])}</span><h3>{e(d["question"])}</h3><ul class="dim-items">{items}</ul>{note}</div>
  <div class="dim-a">{viz}{_see_evidence(t["see_evidence"], d["evidence"])}</div>
</article>''')
    return (f'<div class="dims" data-tabs><div class="dim-tabs" role="tablist" aria-label="{e(_u("aria_tabs", "Change dimensions"))}">{"".join(tabs)}</div>'
            f'{"".join(panels)}</div>')


# ------------------------------------------------------------------ evidence
def evidence_chain(arg, ctx):
    c = ctx["content"]["chain"]
    li = "".join(f'<li class="{"hd" if i == len(c) - 1 else ""}">{e(x)}</li>' for i, x in enumerate(c))
    return f'<ol class="chain2" aria-label="{e(_u("aria_chain", "From source to human decision"))}">{li}</ol>'


def roles(arg, ctx):
    R = ctx["content"]["roles"]
    d = "".join(f"<li>{e(x)}</li>" for x in R["deepin"]["items"])
    tm = "".join(f"<li>{e(x)}</li>" for x in R["team"]["items"])
    return f'''<div class="roles">
  <div class="role-d"><span class="lbl">{e(R["deepin"]["label"])}</span><ul>{d}</ul></div>
  <div class="role-arrow" aria-hidden="true"></div>
  <div class="role-t"><span class="lbl">{e(R["team"]["label"])}</span><ul>{tm}</ul></div>
</div>'''


def risk_context_change(arg, ctx):
    C, t = ctx["content"]["context"], ctx["content"]["copy"]
    why = []
    for i, w in enumerate(C["why"]):
        why.append(f'''<li class="why3">
  <span class="n">{i+1:02d}</span>
  <div><b>{e(w["title"])}</b><small>{e(w["date"])}</small>
    <p class="src"><span class="lbl">{e(C["source_label"])}</span>{e(w["source"])}</p>
    <blockquote>{e(w["excerpt"])}</blockquote>
  </div>
</li>''')
    steps = "".join(f'<li hidden>{e(s)}</li>' for s in C["further_steps"])
    return f'''<figure class="evui rcx2" aria-label="{e(_u("aria_context", "Risk context change with evidence (demo)"))}">
  <div class="evui-top"><span>{e(C["company"])}</span><span class="chip st-wait">{e(C["label"])}</span></div>
  <div class="evui-body">
    <div class="rcx-main">
      <div class="rcx-bar"><span>{_risk(C["from"])}</span><span class="rcx-line" aria-hidden="true"></span><span>{_risk(C["to"])}</span></div>
      <div><div class="lbl">{e(C["why_label"])}</div><ol class="why3s">{"".join(why)}</ol>
        <button type="button" class="btn btn-ghost btn-sm ev-all" data-ev-all data-show="{e(C["view_all"])}" data-hide="{e(C["hide_all"])}" hidden>{e(C["view_all"])}</button></div>
    </div>
    <div class="rcx-side">
      <div class="rcx-reason"><div class="lbl">{e(C["reasoning_label"])}</div><p>{e(C["reasoning"])}</p></div>
      <div class="rcx-rec"><div class="lbl">{e(C["rec_label"])}</div><strong>{e(C["recommendation"])}</strong></div>
      <div class="rcx-team" data-decision>
        <div class="rcx-team-h"><span class="lbl">{e(C["team_label"])}</span><span>{e(C["team_task"])}</span></div>
        <div class="rcx-acts">
          <button type="button" class="btn btn-primary btn-sm" data-act="approve" data-msg="{e(C["approved"])}">{e(C["approve"])}</button>
          <button type="button" class="btn btn-ghost btn-sm" data-act="reject" data-msg="{e(C["rejected"])}">{e(C["reject"])}</button>
          <button type="button" class="btn btn-ghost btn-sm" data-act="further">{e(C["further"])} →</button>
        </div>
        <p class="rcx-result" role="status" hidden></p>
        <ol class="rcx-further" aria-live="polite">{steps}</ol>
      </div>
    </div>
    <p class="rcx-note">{e(t["demo_note"])}</p>
  </div>
</figure>'''


# ------------------------------------------------------------------ hero trust strip + get started
def trust_strip(arg, ctx):
    T = ctx["content"]["trust"]
    li = "".join(f'<li><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 1.5l5.5 2v4.2c0 3.2-2.3 5.7-5.5 6.8-3.2-1.1-5.5-3.6-5.5-6.8V3.5z"/><path d="M5.6 8.1l1.7 1.7 3.2-3.4"/></svg>{e(x)}</li>' for x in T["items"])
    return f'<ul class="trust" aria-label="{e(T["label"])}">{li}</ul>'


def get_started(arg, ctx):
    steps = "".join(f'<li><span class="n">{i + 1:02d}</span><h3>{e(x["t"])}</h3><p>{e(x["p"])}</p></li>' for i, x in enumerate(ctx["content"]["start"]))
    return f'<ol class="gs">{steps}</ol>'


# ------------------------------------------------------------------ value + sectors + customers
def value_chain(arg, ctx):
    """Company data + deepin.risk = your decision, one line of the same case in each box."""
    steps, ops = ctx["content"]["value"]["steps"], ["+", "="]
    out = []
    for i, x in enumerate(steps):
        risk = f'<span class="eq-risk">{_risk(x["risk_from"])}<span aria-hidden="true">→</span>{_risk(x["risk_to"])}</span>' if x.get("risk_from") else ""
        cls = ["data", "dp", "dec"][i]
        out.append(f'<li class="eq-box {cls}"><span class="eq-n">{_wm(x["name"])}</span><b class="eq-q">{e(x["q"])}</b>'
                   f'<p class="eq-ex">“{e(x["ex"])}”</p>{risk}<small class="eq-by">{e(x["by"])}</small></li>')
        if i < len(ops):
            out.append(f'<li class="eq-op" aria-hidden="true">{ops[i]}</li>')
    return f'<ol class="eq" aria-label="{e(_u("aria_value", "Company data plus Deepin Risk equals a decision"))}">{"".join(out)}</ol>'


def sectors(arg, ctx):
    S = ctx["content"]["sectors"]
    cards = []
    for x in S["items"]:
        who = "".join(f"<li>{e(i)}</li>" for i in x["who"])
        dec = "".join(f"<li>{e(i)}</li>" for i in x["decisions"])
        tag = f'<span class="sct-tag">{e(x["tag"])}</span>' if x.get("tag") else ""
        cards.append(f'''<li class="sct">
  <div class="sct-h"><h3>{e(x["name"])}</h3>{tag}</div>
  <div class="sct-b">
    <div><span class="lbl">{e(S["who"])}</span><ul class="sct-who">{who}</ul></div>
    <div><span class="lbl">{e(S["decides"])}</span><ul class="sct-dec">{dec}</ul></div>
  </div>
</li>''')
    return f'<ul class="sectors">{"".join(cards)}</ul>'


def risk_customers(arg, ctx):
    """Customer cards (product, context from src/data.<lang>.json) with a quote each; an alias replaces the name when set.
    Quotes marked draft are hypothetical and carry a visible 'pending approval' tag."""
    Tm = ctx["content"]["testimonials"]
    data = json.load(open(os.path.join(os.path.dirname(__file__), f'data.{ctx["lang"]}.json'), encoding="utf-8"))
    cards = []
    for c in data["customers"]:
        q = Tm["quotes"].get(c["name"])
        if "risk" not in c.get("spaces", []) or not q:
            continue
        ctx_line = f'<span class="proof-ctx">{e(c["context"]["risk"])}</span>' if c.get("context", {}).get("risk") else ""
        draft = f'<span class="tsm-draft">{e(Tm["draft_label"])}</span>' if q.get("draft") else ""
        cards.append(f'''<li class="proof-card tsm">
  <strong>{e(q.get("alias") or c["name"])}</strong>
  <span class="proof-inv">{e(c["investigation"])}</span>{ctx_line}
  <blockquote>{e(q["quote"])}</blockquote>{draft}
</li>''')
    cls = " n4" if len(cards) == 4 else ""
    return f'''<div class="sec-head">
  <p class="eyebrow">{e(Tm["eyebrow"])}</p>
  <h2 class="h2">{Tm["h2"]}</h2>
  <p class="lede">{e(Tm["lede"])}</p>
</div>
<ul class="proof-grid tsms{cls}">{"".join(cards)}</ul>'''


# ------------------------------------------------------------------ request form
def request_form(arg, ctx):
    Fm = ctx["content"]["form"]

    def field(f):
        req = " required" if f.get("required") else ""
        star = ' <span aria-hidden="true">*</span>' if f.get("required") else ""
        ph = f' placeholder="{e(f["placeholder"])}"' if f.get("placeholder") else ""
        if f.get("type") == "textarea":
            ctl = f'<textarea id="rq-{f["id"]}" name="{f["id"]}" rows="3"{ph}{req}></textarea>'
        else:
            ctl = f'<input id="rq-{f["id"]}" name="{f["id"]}" type="{f.get("type", "text")}"{ph}{req}>'
        return f'<label for="rq-{f["id"]}"><span>{e(f["label"])}{star}</span>{ctl}</label>'

    def group(title, fields):
        return f'<div class="rq-group"><span class="lbl">{e(title)}</span>{"".join(field(f) for f in fields)}</div>'

    return f'''<div class="rq-wrap" id="request-sheet">
<form class="rq" id="request" data-endpoint="{e(Fm["endpoint"])}" data-subject="{e(Fm["email_subject"])}" novalidate>
  <div class="rq-top"><b>{e(Fm["title"])}</b><button type="button" class="rq-close" data-close aria-label="{e(Fm["close"])}">×</button></div>
  <ol class="rq-steps" aria-hidden="true"><li class="on">1 · {e(Fm["step1"])}</li><li>2 · {e(Fm["step2"])}</li></ol>
  <fieldset class="rq-page" data-page="1"><legend class="sr">{e(Fm["step1"])}</legend>
    {group(Fm["group_company"], Fm["fields_company"])}
    {group(Fm["group_question"], Fm["fields_question"])}
    <div class="rq-actions"><button class="btn btn-primary" type="button" data-next>{e(Fm["next"])} →</button></div>
  </fieldset>
  <fieldset class="rq-page" data-page="2"><legend class="sr">{e(Fm["step2"])}</legend>
    {group(Fm["group_contact"], Fm["fields_contact"])}
    <div class="rq-actions"><button class="btn btn-ghost" type="button" data-back>{e(Fm["back"])}</button><button class="btn btn-primary" type="submit">{e(Fm["submit"])}</button></div>
  </fieldset>
  <p class="rq-done" hidden role="status">{e(Fm["done"])}</p>
</form>
</div>'''


COMPONENTS = {
    "hero_depth": hero_depth,
    "living_investigation": living_investigation,
    "what_changed": what_changed,
    "evidence_chain": evidence_chain,
    "roles": roles,
    "risk_context_change": risk_context_change,
    "trust_strip": trust_strip,
    "get_started": get_started,
    "value_chain": value_chain,
    "sectors": sectors,
    "risk_customers": risk_customers,
    "request_form": request_form,
}
