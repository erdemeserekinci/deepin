"""deepin.risk components.

Every component takes (arg, ctx); ctx["content"] is the page content file
(src/content/risk.<lang>.json). User-facing text lives in that file, so a Turkish
page only needs risk.tr.json.

Components, roughly in page order:
  company_investigation_card  hero: live investigation (InvestigationActivity, MaterialChange)
  living_investigation        static report vs CompanyTimeline (clickable events)
  what_changed                OwnershipChange, AuthorityChange, RelationshipGraph, financial timeline
  monitoring_vs_investigation Detect -> Investigate -> Explain
  evidence_chain              Source -> ... -> Human decision
  roles                       Deepin investigates, your team decides
  risk_context_change         EvidenceCard / ReasoningTrail / RecommendationCard / HumanApproval
  risk_stack                  corporate intelligence -> deepin.risk -> your risk process
  one_to_many                 one Company Investigation, multiple decisions
  request_form                Company Investigation request (inline on desktop, sheet on mobile)
"""
import json
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


def _ck():
    return '<svg class="ck" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="6.5"/><path d="M5 8.2l2 2 4-4.4"/></svg>'


def _see_evidence(label, ev):
    return (f'<details class="see-ev"><summary>{e(label)}</summary>'
            f'<div class="see-ev-body"><small>{e(ev["source"])}</small><p>{e(ev["excerpt"])}</p></div></details>')


# ------------------------------------------------------------------ hero
def company_investigation_card(arg, ctx):
    L, t = ctx["content"]["live"], ctx["content"]["copy"]
    s = 0
    event = f'<div class="ci-event" data-s="{s}"><span class="ci-pulse" aria-hidden="true"></span><div><b>{e(L["event"])}</b><small>{e(L["event_meta"])}</small></div></div>'
    s += 1
    started = f'<div class="ci-start" data-s="{s}"><span>{e(L["started"])}</span></div>'
    acts = []
    for a in L["activity"]:
        s += 1
        acts.append(f'<li data-s="{s}">{_ck()}<span>{e(a)}</span></li>')
    s += 1
    finds = "".join(f'<li><span class="n">{i+1:02d}</span>{e(f)}</li>' for i, f in enumerate(L["findings"]))
    labels = e(json.dumps(L["status"], ensure_ascii=False))
    return f'''<figure class="case ci" data-live data-labels="{labels}" aria-label="{e(_u("aria_live", "Live company investigation (demo)"))}">
  <div class="case-top ci-top">
    <div><span class="lbl">{e(L["mode"])}</span><strong>{e(L["company"])}</strong></div>
    <span class="chip st-wait" data-live-status>{e(L["status"][-1])}</span>
  </div>
  <ol class="live-bar" aria-hidden="true">{"<li></li>" * (s + 1)}</ol>
  <div class="case-body">
    {event}
    {started}
    <ul class="ci-activity">{"".join(acts)}</ul>
    <div class="ci-findings" data-s="{s}"><span class="lbl">{e(L["findings_label"])}</span><ol>{finds}</ol></div>
    <a class="btn btn-ghost btn-sm ci-link" href="#evidence" data-s="{s}">{e(L["link"])} →</a>
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
    loop = "".join(f"<li>{e(x)}</li>" for x in T["loop"])
    return f'''<div class="liv">
  {report}
  <div class="liv-tl">
    <div class="liv-head"><span class="lbl">{e(_u("living", "Living investigation"))}</span><strong>{e(T["company"])}</strong><small class="liv-hint">{e(t["mon_hint"])}</small></div>
    <div class="lt-axis" aria-hidden="true">{ticks}</div>
    <ol class="lt-track">{"".join(pts)}</ol>
    <div class="lt-panels" aria-live="polite">{"".join(panels)}</div>
  </div>
</div>
<ol class="loop" aria-label="{e(_u("aria_loop", "What happens when a material change is detected"))}">{loop}</ol>'''


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
    t = ctx["content"]["copy"]
    rows = []
    for d in ctx["content"]["dimensions"]:
        items = "".join(f"<li>{e(x)}</li>" for x in d["items"])
        viz = {"ownership": lambda: _ownership(d["ownership"]), "authority": lambda: _authority(d["authority"]),
               "graph": lambda: _graph(d["graph"]), "financial": lambda: _financial(d["financial"])}[d["visual"]]()
        note = f'<p class="dim-note">{e(d["note"])}</p>' if d.get("note") else ""
        rows.append(f'''<article class="dim">
  <div class="dim-q"><span class="dim-key">{e(d["key"])}</span><h3>{e(d["question"])}</h3><ul class="dim-items">{items}</ul>{note}</div>
  <div class="dim-a">{viz}{_see_evidence(t["see_evidence"], d["evidence"])}</div>
</article>''')
    return f'<div class="dims">{"".join(rows)}</div>'


# ------------------------------------------------------------------ monitoring vs investigation
def monitoring_vs_investigation(arg, ctx):
    out = []
    for i, s in enumerate(ctx["content"]["stages"]):
        items = "".join(f"<li>{e(x)}</li>" for x in s["items"])
        cls = "mon" if i == 0 else "inv"
        out.append(f'<li class="stage {cls}"><span class="stage-k">{e(s["key"])}</span><b>{e(s["q"])}</b><ul>{items}</ul><span class="stage-who">{e(s["who"])}</span></li>')
    return f'<ol class="stages">{"".join(out)}</ol>'


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
    <details class="ev-d"><summary data-hide="{e(C["hide"])}" data-view="{e(C["view"])}">{e(C["view"])}</summary><blockquote>{e(w["excerpt"])}</blockquote></details>
  </div>
</li>''')
    steps = "".join(f'<li hidden>{e(s)}</li>' for s in C["further_steps"])
    return f'''<figure class="evui rcx2" aria-label="{e(_u("aria_context", "Risk context change with evidence (demo)"))}">
  <div class="evui-top"><span>{e(C["company"])}</span><span class="chip st-wait">{e(C["label"])}</span></div>
  <div class="evui-body">
    <div class="rcx-bar"><span>{_risk(C["from"])}</span><span class="rcx-line" aria-hidden="true"></span><span>{_risk(C["to"])}</span></div>
    <div><div class="lbl">{e(C["why_label"])}</div><ol class="why3s">{"".join(why)}</ol></div>
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
    <p class="rcx-note">{e(t["demo_note"])}</p>
  </div>
</figure>'''


# ------------------------------------------------------------------ stack + uses
def risk_stack(arg, ctx):
    S = ctx["content"]["stack"]

    def layer(x, cls):
        items = "".join(f"<li>{e(i)}</li>" for i in x["items"])
        name = x["name"]
        name = f'deep<b>in</b>.{e(name.split(".", 1)[1])}' if name.startswith("deepin.") else e(name)
        return f'<li class="stk {cls}"><div class="stk-h"><span class="stk-n">{name}</span><small>{e(x["role"])}</small></div><ul>{items}</ul></li>'
    arrow = '<li class="stk-arrow" aria-hidden="true"></li>'
    return f'<ol class="stack">{layer(S["top"], "top")}{arrow}{layer(S["mid"], "mid")}{arrow}{layer(S["bottom"], "bot")}</ol>'


def one_to_many(arg, ctx):
    U = ctx["content"]["uses"]
    br = "".join(f'<li><span class="u1">{e(b["name"])}</span><span class="u2">{e(b["then"])}</span></li>' for b in U["branches"])
    return f'''<div class="o2m">
  <div class="o2m-root">{e(U["root"])}</div>
  <ol class="o2m-br">{br}</ol>
  <p class="o2m-foot">{e(U["footer"])} <span class="nm">deep<b>in</b>.risk</span></p>
</div>'''


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
    "company_investigation_card": company_investigation_card,
    "living_investigation": living_investigation,
    "what_changed": what_changed,
    "monitoring_vs_investigation": monitoring_vs_investigation,
    "evidence_chain": evidence_chain,
    "roles": roles,
    "risk_context_change": risk_context_change,
    "risk_stack": risk_stack,
    "one_to_many": one_to_many,
    "request_form": request_form,
}
