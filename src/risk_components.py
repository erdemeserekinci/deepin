"""deepin.risk components.

Each component takes (arg, ctx) where ctx["content"] is the page's content file
(src/content/risk.<lang>.json). Nothing user-facing is hardcoded here, so a
Turkish page only needs risk.tr.json.
"""
from html import escape as e


def check_icon():
    return '<svg class="ck" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="6.5"/><path d="M5 8.2l2 2 4-4.4"/></svg>'


def company_investigation_card(arg, ctx):
    """Hero: a live company investigation, replayed step by step."""
    L = ctx["content"]["live"]
    t = ctx["content"]["copy"]
    s = 0
    event = f'''<div class="ci-event" data-s="{s}"><span class="ci-pulse" aria-hidden="true"></span><div><b>{e(L["event"])}</b><small>{e(L["event_meta"])}</small></div></div>'''
    s += 1
    started = f'<div class="ci-start" data-s="{s}"><span>{e(L["started"])}</span></div>'
    acts = []
    for a in L["activity"]:
        s += 1
        acts.append(f'<li data-s="{s}">{check_icon()}<span>{e(a)}</span></li>')
    s += 1
    finds = "".join(f'<li><span aria-hidden="true">→</span>{e(f)}</li>' for f in L["findings"])
    import json
    labels = e(json.dumps(L["status"], ensure_ascii=False))
    return f'''<figure class="case ci" data-live data-labels="{labels}" aria-label="Live company investigation (demo)">
  <div class="case-top ci-top">
    <div><span class="lbl">{e(L["mode"])}</span><strong>{e(L["company"])}</strong></div>
    <span class="chip st-wait" data-live-status>{e(L["status"][-1])}</span>
  </div>
  <ol class="live-bar" aria-hidden="true">{"<li></li>" * (s + 1)}</ol>
  <div class="case-body">
    {event}
    {started}
    <ul class="ci-activity">{"".join(acts)}</ul>
    <div class="ci-findings" data-s="{s}"><span class="lbl">{e(L["findings_label"])}</span><ul>{finds}</ul></div>
    <a class="ci-link" href="#evidence" data-s="{s}">{e(L["link"])} →</a>
  </div>
  <figcaption class="case-note">{e(t["demo_note"])}</figcaption>
</figure>'''


def company_timeline(arg, ctx):
    T = ctx["content"]["timeline"]
    n = len(T["ticks"]) - 1
    pos = lambda i: f"{i / n * 100:.4g}%"
    ticks = "".join(f'<span style="--x:{pos(i)}">{e(m)}</span>' for i, m in enumerate(T["ticks"]))
    evs = [f'''<li class="tl2-ev start" style="--x:0%"><i></i><div class="tl2-card"><b>{e(T["start"]["label"])}</b><span class="risk r-{T["start"]["risk"].lower()}">{e(T["start"]["risk"])}</span></div></li>''']
    for ev in T["events"]:
        cls = " end" if ev["tick"] == n else ""
        change = (f'<span class="risk r-{ev["risk_from"].lower()}">{e(ev["risk_from"])}</span>→<span class="risk r-{ev["risk_to"].lower()}">{e(ev["risk_to"])}</span>'
                  if ev["risk_from"] != ev["risk_to"] else f'<span class="risk r-{ev["risk_to"].lower()}">{e(ev["risk_to"])}</span>')
        evs.append(f'''<li class="tl2-ev hot{cls}" style="--x:{pos(ev["tick"])}"><i></i><div class="tl2-card"><small>{e(ev["date"])}</small><b>{e(ev["change"])}</b><span class="tl2-re">↓ {e(T["reopened"])}</span><span class="tl2-risk">{change}</span></div></li>''')
    loop = "".join(f"<li>{e(x)}</li>" for x in T["loop"])
    return f'''<div class="tl2" aria-label="Company timeline for {e(T["company"])}">
  <div class="tl2-head"><span class="lbl">Company</span><strong>{e(T["company"])}</strong></div>
  <div class="tl2-axis" aria-hidden="true">{ticks}</div>
  <ol class="tl2-track">{"".join(evs)}</ol>
</div>
<div class="tl2-compare">
  <div class="tl2-static"><span class="lbl">{e(T["static_label"])}</span><p>{T["static_text"]}</p></div>
  <div class="tl2-living"><span class="lbl">{e(T["living_label"])}</span><p>{T["living_text"]}</p></div>
</div>
<ol class="loop" aria-label="What happens when a material event is detected">{loop}</ol>'''


def material_change(f):
    return f'''<div class="mc"><span class="mc-tag">Material change</span><b>{e(f["title"])}</b><p>{e(f["detail"])}</p><small>{e(f["meta"])}</small></div>'''


def relationship_tree(tree):
    br = []
    for b in tree["branches"]:
        kids = "".join(f"<li>{e(k)}</li>" for k in b["children"])
        br.append(f'<li><details open><summary>{e(b["label"])}</summary><ul>{kids}</ul></details></li>')
    return f'''<div class="rt"><span class="mc-tag">Relationship map</span><div class="rt-root">{e(tree["root"])}</div><ul class="rt-branches">{"".join(br)}</ul></div>'''


def investigation_dimensions(arg, ctx):
    rows = []
    for d in ctx["content"]["dimensions"]:
        items = "".join(f"<li>{e(x)}</li>" for x in d["items"])
        right = relationship_tree(d["tree"]) if "tree" in d else material_change(d["finding"])
        rows.append(f'''<article class="dim" id="dim-{d["key"].lower()}">
  <div class="dim-q"><span class="dim-key">{e(d["key"])}</span><h3>{e(d["question"])}</h3><ul class="dim-items">{items}</ul></div>
  <div class="dim-a">{right}</div>
</article>''')
    return f'<div class="dims">{"".join(rows)}</div>'


def risk_context_change(arg, ctx):
    C = ctx["content"]["context"]
    t = ctx["content"]["copy"]
    why = "".join(f'''<li data-ref="{w["ref"]}"><span class="n">{i+1:02d}</span><span><b>{e(w["title"])}</b><small>{e(w["date"])}</small></span><span class="ref">[{w["ref"]}]</span></li>''' for i, w in enumerate(C["why"]))
    ev = "".join(f'''<li data-ref="{x["ref"]}"><details><summary><span class="n">{x["ref"]}</span><span><strong>{e(x["source"])}</strong><small>{e(x["kind"])}</small></span><span class="view">View →</span></summary><p class="excerpt">{e(x["excerpt"])}</p></details></li>''' for x in C["evidence"])
    return f'''<figure class="evui rcx" aria-label="Risk context change with evidence (demo)">
  <div class="evui-top"><span>{e(C["company"])}</span><span class="chip st-wait">{e(C["label"])}</span></div>
  <div class="evui-body">
    <div class="rcx-change"><span class="risk r-{C["from"].lower()}">{e(C["from"])}</span><span aria-hidden="true">→</span><span class="risk r-{C["to"].lower()}">{e(C["to"])}</span></div>
    <div><div class="lbl">Why?</div><ol class="why why2">{why}</ol></div>
    <div><div class="lbl">Evidence</div><ol class="srcstack src2">{ev}</ol></div>
    <div class="rcx-reason"><div class="lbl">Reasoning</div><p>{e(C["reasoning"])}</p></div>
    <div class="rcx-rec"><div><div class="lbl">Recommendation</div><strong>{e(C["recommendation"])}</strong></div><span class="rcx-btn">{e(C["button"])}</span></div>
    <p class="rcx-note">{e(t["demo_note"])}</p>
  </div>
</figure>'''


def fit_layers(arg, ctx):
    rows = []
    F = ctx["content"]["fit"]
    for i, f in enumerate(F):
        items = "".join(f"<li>{e(x)}</li>" for x in f["items"])
        cls = " self" if f.get("self") else ""
        name = f["name"]
        if name.startswith("deepin."):
            name = f'deep<b>in</b>.{e(name.split(".", 1)[1])}'
        else:
            name = e(name)
        rows.append(f'<li class="fit-layer{cls}"><div class="fit-name"><span class="fit-n">{name}</span><small>{e(f["role"])}</small></div><ul>{items}</ul></li>')
        if i < len(F) - 1:
            rows.append('<li class="fit-arrow" aria-hidden="true"></li>')
    return f'<ol class="fit-stack">{"".join(rows)}</ol>'


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

    s1 = "".join(field(f) for f in Fm["fields1"])
    s2 = "".join(field(f) for f in Fm["fields2"])
    return f'''<form class="rq" id="request" data-endpoint="{e(Fm["endpoint"])}" data-subject="{e(Fm["email_subject"])}" novalidate>
  <ol class="rq-steps" aria-hidden="true"><li class="on">1 · {e(Fm["step1"])}</li><li>2 · {e(Fm["step2"])}</li></ol>
  <fieldset class="rq-page" data-page="1"><legend class="sr">{e(Fm["step1"])}</legend>{s1}
    <div class="rq-actions"><button class="btn btn-primary" type="button" data-next>{e(Fm["next"])} →</button></div>
  </fieldset>
  <fieldset class="rq-page" data-page="2"><legend class="sr">{e(Fm["step2"])}</legend>{s2}
    <div class="rq-actions"><button class="btn btn-ghost" type="button" data-back>{e(Fm["back"])}</button><button class="btn btn-primary" type="submit">{e(Fm["submit"])}</button></div>
  </fieldset>
  <p class="rq-done" hidden role="status">{e(Fm["done"])}</p>
</form>'''


COMPONENTS = {
    "company_investigation_card": company_investigation_card,
    "company_timeline": company_timeline,
    "investigation_dimensions": investigation_dimensions,
    "risk_context_change": risk_context_change,
    "fit_layers": fit_layers,
    "request_form": request_form,
}
