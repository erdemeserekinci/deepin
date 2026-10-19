"""DEEPIN / ORGANISM homepage components.

The homepage is one journey: a signal arrives, an Investigation organizes around
it, evidence emerges, a person decides, the pattern repeats into Spaces, and
underneath it all sits Deepin Harness. Text comes from src/content/home.<lang>.json;
investigations, Spaces and customers come from src/data.<lang>.json.

Scroll-driven motion lives in src/scripts/home.js. Every component renders a
complete, readable final state without JavaScript or with reduced motion.

Components:
  org_rail        state rail (desktop): where the signal is in the journey
  org_scene       the Investigation transformation (fragments -> sources -> evidence -> finding -> decision)
  org_decision    the human moment: recommendation, provenance, approve / reject / investigate further
  org_index       Investigation catalog as an editorial index
  org_grammar     two Spaces, one grammar (deepin.risk and deepin.finance side by side)
  org_proof       customers at the maturity they have reached
  org_under       Deepin Harness revealed underneath the Investigation surface
  org_close       closing steps
"""
import json
from html import escape as e

DATA, STATUS = {}, {}


def set_data(data, status):
    global DATA, STATUS
    DATA, STATUS = data, status


def _j(x):
    return e(json.dumps(x, ensure_ascii=False), quote=True)


def _wm(space):
    return f'<span class="nm">deep<b>in</b>.{e(space)}</span>'


def _chip(status):
    return f'<span class="chip st-{status}">{e(STATUS[status]["label"])}</span>'


def _pips(status):
    lvl = STATUS[status]["level"]
    return '<span class="pips" aria-hidden="true">' + "".join(f'<i class="{"on" if n < lvl else ""}"></i>' for n in range(3)) + "</span>"


# ------------------------------------------------------------------ rail
def org_rail(arg, ctx):
    items = "".join(f'<a href="#{i}" data-rail="{i}"><i></i><span>{e(t)}</span></a>' for i, t in ctx["content"]["rail"])
    return f'<nav class="rail" aria-label="{e(ctx["content"]["copy"]["rail_label"])}">{items}</nav>'


# ------------------------------------------------------------------ investigation scene
# organized (final) positions, used before JavaScript takes over and without it
_ORDER = {"co": (50, 7), "reg1": (14, 20), "reg2": (14, 30), "graph": (14, 40), "pdf": (14, 51), "crm": (14, 60),
          "mail": (14, 69), "sheet": (14, 78), "web": (14, 87), "E1": (47, 25), "E2": (47, 46), "E3": (47, 67),
          "find": (80.5, 40), "dec": (80.5, 77)}


def _pos(k):
    x, y = _ORDER[k]
    return f' style="--x:{x};--y:{y}"'


def org_scene(arg, ctx):
    s, c = ctx["content"]["scene"], ctx["content"]["copy"]
    phases = "".join(
        f'<div class="ph" data-ph="{i}"><span class="lab">{i + 1:02d} · {e(p["k"])}</span><h2>{p["h"]}</h2><p>{e(p["p"])}</p></div>'
        for i, p in enumerate(s["phases"]))
    steps = "".join(f'<li><button type="button" data-step="{i}"><span>{i + 1:02d}</span>{e(p["k"])}</button></li>' for i, p in enumerate(s["phases"]))
    srcs = "".join(
        f'<div class="st-n st-src{" rel" if ev else ""}" data-node="{k}" data-ev="{e(ev)}"{_pos(k)}>'
        f'<b>{e(t)}</b><small class="t0">{e(t0)}</small><small class="t1">{e(t1)}</small>'
        f'<span class="st-chk">{"→ " + e(ev) if ev else "✓ " + e(s["checked"])}</span></div>'
        for k, t, t0, t1, ev in s["sources"])
    notes = "".join(f'<span class="st-tn" data-a="{a}" data-b="{b}">{e(t)}</span>' for a, b, t in s["tangle"] if t)
    evs = "".join(f'<div class="st-n st-ev" data-node="{i}"{_pos(i)}><span class="ev-id">{e(i)}</span><b>{e(t)}</b><small>{e(src)}</small></div>'
                  for i, t, src in s["evidence"])
    cites = "".join(f"<i>{e(i)}</i>" for i, _, _ in s["evidence"])
    return f'''<div class="scene-sticky">
  <div class="wrap scene-grid">
    <div class="scene-copy">
      <p class="lab sec-k"><span>§01</span>{e(c["sc_kicker"])}</p>
      <div class="phases">{phases}</div>
      <ol class="steps-nav" aria-label="{e(c["sc_steps"])}">{steps}</ol>
    </div>
    <figure class="stage org ev" data-tangle="{_j([[a, b] for a, b, _ in s["tangle"]])}" aria-label="{e(s["phases"][-1]["p"])}">
      <svg class="stage-lines" aria-hidden="true"></svg>
      <div class="st-n st-co" data-node="co"{_pos("co")}><span class="lab">{e(s["case"])}</span><b>{e(s["company"])}</b></div>
      {srcs}{notes}{evs}
      <div class="st-n st-find" data-node="find"{_pos("find")}><span class="lab">{e(s["finding_k"])}</span><p>{e(s["finding"])}</p><span class="cites">{cites}</span></div>
      <div class="st-n st-dec" data-node="dec"{_pos("dec")}><span class="lab">{e(s["decision_k"])}</span><b>{e(s["decision"])}</b><small>{e(s["decision_sub"])}</small></div>
    </figure>
  </div>
</div>'''


# ------------------------------------------------------------------ the human moment
def org_decision(arg, ctx):
    d = ctx["content"]["decision"]
    ev = {i: (t, src) for i, t, src in ctx["content"]["scene"]["evidence"]}
    chain = "".join(f'<li class="{"hum" if n == len(d["chain"]) - 1 else ""}">{e(x)}</li>' for n, x in enumerate(d["chain"]))
    why = "".join(f'<li data-cite="{e(r)}" tabindex="0"><span>{e(t)}</span><sup>{e(r)}</sup></li>' for t, r in d["why"])
    slips = "".join(f'<li class="slip" data-slip="{e(i)}" tabindex="0"><span class="ev-id">{e(i)}</span><b>{e(t)}</b><small>{e(src)}</small></li>'
                    for i, (t, src) in ev.items())
    btns = "".join(f'<button type="button" class="d-btn d-{k}" data-act="{k}" data-msg="{e(m, quote=True)}">{e(t)}</button>' for k, t, m in d["actions"])
    further = "".join(f'<li hidden>{e(x)}</li>' for x in d["further"])
    return f'''<div class="dcard" data-dcard>
  <div class="dcard-top"><span class="lab">{e(d["head"])}</span><span class="chip st-wait">{e(d["status"])}</span></div>
  <ol class="dchain" aria-hidden="true">{chain}</ol>
  <div class="dcard-body">
    <div class="drec"><span class="lab">{e(d["rec_k"])}</span><strong>{e(d["rec"])}</strong><span class="drec-sub">{e(d["rec_sub"])}</span>
      <span class="lab dwhy-k">{e(d["why_k"])}</span><ol class="dwhy">{why}</ol></div>
    <div class="dev"><span class="lab">{e(d["ev_k"])}</span><ol class="slips">{slips}</ol></div>
  </div>
  <div class="dact"><div class="d-btns">{btns}</div><p class="d-res" aria-live="polite" hidden></p><ol class="d-next">{further}</ol></div>
</div>
<p class="note">{e(d["note"])}</p>'''


# ------------------------------------------------------------------ investigations index
def org_index(arg, ctx):
    ui = ctx["ui"]
    rows = []
    for n, i in enumerate(DATA["investigations"], 1):
        trail = ""
        if i.get("sources"):
            srcs = "".join(f"<li>{e(x)}</li>" for x in i["sources"])
            outs = "".join(f"<li>{e(x)}</li>" for x in i["outputs"])
            trail = (f'<div class="ix-trail"><div><span class="lab">{e(ui["investigates"])}</span><ul>{srcs}</ul></div>'
                     f'<i aria-hidden="true"></i><div><span class="lab">{e(ui["delivers"])}</span><ul class="out">{outs}</ul></div></div>')
        rows.append(f'''<li class="ix-row{" minor" if i["weight"] != "primary" else ""}"><details>
  <summary><span class="ix-n">{n:02d}</span><span class="ix-name">{e(i["name"])}</span><span class="ix-sp">{_wm(i["space"])}</span>{_chip(i["status"])}<span class="ix-plus" aria-hidden="true"></span></summary>
  <div class="ix-body"><p class="ix-head">{e(i["headline"])}</p>{trail}<a class="ix-go" href="{ctx["root"]}{i["href"]}">{e(i["cta"])} →</a></div>
</details></li>''')
    rows.append(f'<li class="ix-row more"><a href="#contact"><span class="ix-n">+</span><span class="ix-name">{e(ui["more_title"])}</span>'
                f'<span class="ix-more">{e(ui["more_text"])} <b>{e(ui["more_cta"])}</b></span></a></li>')
    return f'<ol class="ix">{"".join(rows)}</ol>'


# ------------------------------------------------------------------ two Spaces, one grammar
def org_grammar(arg, ctx):
    g = ctx["content"]["grammar"]
    sp = {s["id"]: s for s in DATA["spaces"]}
    root = ctx["root"]

    def head(k, cls):
        s = sp[k]
        return (f'<a class="gm-sp {cls}" href="{root}{s["href"]}">{_wm(k)}{_chip(s["status"])}'
                f'<span class="gm-inv">{e(s["primary"])}</span></a>')
    rows = "".join(
        f'<li class="gm-row{" hum" if n == len(g["rows"]) - 1 else ""}"><span class="gm-a">{e(a)}</span><span class="gm-k"><i></i>{e(k)}</span><span class="gm-b">{e(b)}</span></li>'
        for n, (k, a, b) in enumerate(g["rows"]))
    explore = "".join(f'<a href="{root}{s["href"]}">{_wm(s["id"])}<span>{e(s["title"])}</span></a>' for s in DATA["spaces"] if s["status"] == "exploring")
    return f'''<div class="gm">
  <div class="gm-head">{head("risk", "a")}<span class="gm-lbl lab">{e(g["label"])}</span>{head("finance", "b")}</div>
  <ol class="gm-rows">{rows}</ol>
</div>
<p class="note gm-note">{e(g["note"])}</p>
<div class="gm-explore"><span class="lab">{e(ctx["ui"]["exploring"])}</span>{explore}</div>'''


# ------------------------------------------------------------------ customers
def org_proof(arg, ctx):
    rows = "".join(
        f'<li><span class="pf-name">{e(c["name"])}</span><span class="pf-inv">{e(c["investigation"])}</span>'
        f'<span class="pf-st">{_pips(c["status"])}{_chip(c["status"])}</span></li>'
        for c in DATA["customers"])
    a, b, c3 = (e(x) for x in ctx["ui"]["legend"])
    legend = (f'<div class="proof-legend"><span><span class="pips"><i class="on"></i><i></i><i></i></span>{a}</span>'
              f'<span><span class="pips"><i class="on"></i><i class="on"></i><i></i></span>{b}</span>'
              f'<span><span class="pips"><i class="on"></i><i class="on"></i><i class="on"></i></span>{c3}</span></div>')
    return f'<ul class="pf-list">{rows}</ul>{legend}'


# ------------------------------------------------------------------ harness underneath
def org_under(arg, ctx):
    u = ctx["content"]["under"]
    slab = '<i aria-hidden="true"></i>'.join(f'<span class="{"hum" if n == len(u["slab"]) - 1 else ""}">{e(x)}</span>' for n, x in enumerate(u["slab"]))
    xs = (130, 320, 510)
    roles = "".join(
        f'<g class="t-node" style="--d:{n}"><circle cx="{x}" cy="92" r="6"/><text x="{x}" y="72" text-anchor="middle" class="t-l">{e(u["role"])}</text>'
        f'<text x="{x}" y="118" text-anchor="middle" class="t-a">{e(u["authority"])}</text></g>' for n, x in enumerate(xs))
    agents = "".join(
        f'<g class="t-node" style="--d:{3 + n}"><rect x="{x - 34}" y="178" width="68" height="26" rx="13"/><text x="{x}" y="195" text-anchor="middle">{e(u["agent"])}</text></g>'
        for n, x in enumerate(xs))
    edges = "".join(f'<path pathLength="1" d="M320 40 C320 60 {x} 60 {x} 86"/>' for x in xs)
    edges += "".join(f'<path pathLength="1" d="M{x} 126 V178"/>' for x in xs)
    edges += "".join(f'<path pathLength="1" d="M{x} 204 C{x} 236 320 232 320 258"/>' for x in xs)
    edges += '<path pathLength="1" d="M320 284 V306"/><path pathLength="1" d="M320 332 V352"/>'
    strata_y = (408, 430, 452, 474)
    strata = "".join(
        f'<g class="t-str" style="--d:{8 + n}"><text x="24" y="{y + 4}" class="t-s">{e(t)}</text><path pathLength="1" d="M128 {y} H616"/></g>'
        for n, (y, t) in enumerate(zip(strata_y, u["strata"])))
    ties = "".join(f'<path pathLength="1" class="tie" d="M{x} 204 V400"/>' for x in (130, 510)) + '<path pathLength="1" class="tie" d="M320 378 V400"/>'
    svg = f'''<svg viewBox="0 0 640 492" class="topo-svg" role="img" aria-label="{e(u["aria"])}">
  <rect class="t-org" x="6" y="6" width="628" height="380" rx="18"/>
  <text x="26" y="32" class="t-k">{e(u["org"])}</text>
  <circle class="t-hub" cx="320" cy="34" r="4"/>
  <g class="t-edges">{edges}{ties}</g>
  {roles}{agents}
  <g class="t-node" style="--d:6"><rect x="270" y="258" width="100" height="26" rx="13" class="t-task"/><text x="320" y="275" text-anchor="middle">{e(u["task"])}</text></g>
  <g class="t-node" style="--d:7"><rect x="262" y="306" width="116" height="26" rx="7"/><text x="320" y="323" text-anchor="middle">{e(u["capability"])}</text>
    <text x="320" y="368" text-anchor="middle" class="t-s">{e(u["tools"])}</text></g>
  {strata}
  <circle class="t-signal" r="4"><animateMotion dur="7s" repeatCount="indefinite" path="M320 34 C320 60 130 60 130 92 V191 C130 236 320 232 320 271 V319"/></circle>
</svg>'''
    chain = [u["org"], f'{u["role"]} · {u["authority"]}', u["agent"], u["task"], u["capability"], u["tools"]]
    mobile = ('<ol class="topo-m">' + "".join(f"<li>{e(x)}</li>" for x in chain) + "</ol>"
              + '<div class="topo-ms">' + "".join(f"<span>{e(x)}</span>" for x in u["strata"]) + "</div>")
    if arg == "slab":
        return f'<div class="slab" aria-hidden="true"><p class="slab-h">{u["slab_h"]}</p><div class="slab-in">{slab}</div></div>'
    return f'<figure class="topo">{svg}{mobile}</figure>'


# ------------------------------------------------------------------ closing steps
def org_close(arg, ctx):
    items = "".join(f'<li><span class="lab">{n:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for n, (t, d) in enumerate(ctx["content"]["close"], 1))
    return f'<ol class="close-steps">{items}</ol>'


COMPONENTS = {
    "org_rail": org_rail,
    "org_scene": org_scene,
    "org_decision": org_decision,
    "org_index": org_index,
    "org_grammar": org_grammar,
    "org_proof": org_proof,
    "org_under": org_under,
    "org_close": org_close,
}
