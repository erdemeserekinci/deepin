"""Deepin Harness page components.

Every component takes (arg, ctx); text comes from ctx["content"]
(src/content/harness.<lang>.json). Diagrams are HTML so they reflow on small
screens; connector lines are drawn by base.js from each figure's data-links
edge list ([from, to, kind]) between elements marked data-n="id".

The organization model is conceptual: it names the ideas Harness works with,
not code-level classes.

Components, in page order:
  hx_runtime_org      hero: organization -> roles -> agents -> task -> approval -> action
  hx_problem          a plain agent vs the questions an enterprise asks
  hx_org_model        Organization, Role, Authority, Policy, Agent, Task, Capability, Tool, Service, Knowledge
  hx_reasoning        state -> event -> checks -> act / delegate / collaborate -> new state
  hx_runtime          request -> Harness layers (each leaves a trace) -> enterprise systems
  hx_collab           illustrative Company Investigation collaboration
  hx_gate             governance gate with three example requests
  hx_knowledge        sources -> organizational knowledge -> roles / agents / Investigations
  hx_evaluation       task -> trace -> outcome -> evaluation criteria -> regression / improvement
  hx_trace            clickable execution trace with a record inspector
  hx_spaces           one Harness, two Spaces
  hx_research         four R&D areas
"""
import json
from html import escape as e

ICONS = {
    "lock": '<rect x="3" y="8" width="12" height="8" rx="2"/><path d="M6 8V6a3 3 0 016 0v2"/>',
    "air": '<path d="M3 6h9a2 2 0 100-4M3 12h11a2 2 0 110 4M3 9h6"/>',
    "user": '<circle cx="9" cy="6" r="3"/><path d="M3 16c1-3 3.5-4.5 6-4.5s5 1.5 6 4.5"/>',
    "doc": '<path d="M4 3h10v12H4z"/><path d="M7 7h4M7 10h4"/>',
    "net": '<circle cx="4" cy="9" r="2"/><circle cx="14" cy="4" r="2"/><circle cx="14" cy="14" r="2"/><path d="M6 8l6-3M6 10l6 3"/>',
    "shield": '<path d="M9 2l6 3v4c0 4-3 6-6 7-3-1-6-3-6-7V5z"/>',
    "hand": '<path d="M6 9V4a1.2 1.2 0 012.4 0v4M8.4 8V3a1.2 1.2 0 012.4 0v5M10.8 8V4.5a1.2 1.2 0 012.4 0V11c0 3-2 5-4.5 5S4 14.5 3.5 12L2.8 9.6a1.1 1.1 0 012-.8L6 11"/>',
    "key": '<circle cx="6" cy="9" r="3"/><path d="M9 9h7M13 9v3M15.5 9v2"/>',
}
ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'


def _links(edges):
    return e(json.dumps(edges), quote=True)


def _c(ctx, key):
    return ctx["content"][key]


def _wm(space):
    return f'<span class="nm">deep<b>in</b>.{e(space)}</span>'


# ------------------------------------------------------------------ hero
def hx_runtime_org(arg, ctx):
    h = _c(ctx, "hero_org")
    cols = []
    for n, res in enumerate(h["res"], 1):
        cols.append(f'''<div class="ho-col">
        <span class="ho-n ho-role" data-n="r{n}" data-s="1">{e(h["role"])}</span>
        <span class="ho-n ho-agent" data-n="a{n}" data-s="2">{e(h["agent"])}</span>
        <span class="ho-n ho-res" data-n="c{n}" data-s="3">{e(res)}</span>
      </div>''')
    edges = [["o", f"r{n}", "fl"] for n in (1, 2, 3)]
    edges += [[f"r{n}", f"a{n}", ""] for n in (1, 2, 3)] + [[f"a{n}", f"c{n}", ""] for n in (1, 2, 3)]
    edges += [[f"c{n}", "t", "fl"] for n in (1, 2, 3)] + [["t", "h", "w"], ["h", "x", ""]]
    return f'''<figure class="case ho" data-live data-labels="{_links(h["labels"])}" aria-label="{e(h["aria"])}">
  <div class="case-top"><span class="case-id">{e(h["title"])}</span><span class="chip st-production" data-live-status>{e(h["labels"][-1])}</span></div>
  <div class="ho-body" data-links="{_links(edges)}">
    <div class="ho-org" data-n="o" data-s="0"><span>{e(h["org"])}</span></div>
    <div class="ho-cols">{"".join(cols)}</div>
    <span class="ho-n ho-task" data-n="t" data-s="4">{e(h["task"])}</span>
    <span class="ho-n ho-ap" data-n="h" data-s="5">{e(h["approval"])}</span>
    <span class="ho-n ho-act" data-n="x" data-s="6">{e(h["action"])}</span>
  </div>
</figure>'''


# ------------------------------------------------------------------ problem
def hx_problem(arg, ctx):
    p, c = _c(ctx, "problem"), ctx["content"]["copy"]
    stack = '<i aria-hidden="true"></i>'.join(f"<span>{e(x)}</span>" for x in p["stack"])
    qs = "".join(f"<li>{e(q)}</li>" for q in p["questions"])
    return f'''<div class="hp">
  <div class="hp-simple">
    <div class="lbl">{e(c["problem_simple"])}</div>
    <div class="hp-stack">{stack}</div>
    <p>{e(c["problem_simple_cap"])}</p>
  </div>
  <div class="hp-qs">
    <div class="lbl">{e(c["problem_q"])}</div>
    <ul class="hp-q">{qs}</ul>
  </div>
</div>
<p class="quote hp-land">{c["problem_land"]}</p>'''


# ------------------------------------------------------------------ organization model
def hx_org_model(arg, ctx):
    m = _c(ctx, "model")
    n = m["nodes"]

    def node(k, cls=""):
        t, q, ex = n[k]
        exs = f'<small>{e(ex)}</small>' if ex else ""
        return f'<div class="om-n om-{k} {cls}" data-n="{k}"><span class="om-t">{e(t)}</span><span class="om-q">{e(q)}</span>{exs}</div>'

    g = [f'<span class="om-g">{e(x)}</span>' for x in m["groups"]]
    edges = [["role", "agent", ""], ["auth", "agent", "d"], ["pol", "agent", "d"],
             ["agent", "task", ""], ["task", "cap", ""], ["cap", "tool", ""], ["cap", "svc", ""],
             ["agent", "know", "nd"]]
    return f'''<figure class="om" aria-label="{e(m["aria"])}">
  <div class="om-org"><span class="om-t">{e(m["org"][0])}</span><span>{e(m["org"][1])}</span></div>
  <div class="om-grid" data-links="{_links(edges)}">
    {g[0]}{node("role")}{node("auth", "om-gov")}{node("pol", "om-gov")}
    {g[1]}{node("agent", "core")}{node("task")}{node("cap")}{node("tool", "tech")}{node("svc", "tech")}
    {g[2]}{node("know")}
  </div>
  <figcaption class="om-note">{m["note"]}</figcaption>
</figure>'''


# ------------------------------------------------------------------ organizational reasoning
def hx_reasoning(arg, ctx):
    r = _c(ctx, "reasoning")
    pair = "".join(f'<div><span class="om-t">{e(t)}</span><p>{e(d)}</p></div>' for t, d in r["pair"])
    checks = "".join(f'<li data-s="{2 + i}">{e(q)}</li>' for i, q in enumerate(r["checks"]))
    outs = "".join(f"<span>{e(o)}</span>" for o in r["outcomes"])
    return f'''<div class="rs-pair">{pair}</div>
<figure class="rs" data-live aria-label="{e(r["aria"])}">
  <div class="rs-flow">
    <div class="rs-n rs-state" data-s="0">{e(r["state"])}</div>
    <div class="rs-n rs-event" data-s="1">{e(r["event"])}</div>
    <ol class="rs-checks">{checks}</ol>
    <div class="rs-n rs-out" data-s="6">{outs}</div>
    <div class="rs-n rs-state next" data-s="7">{e(r["next"])}</div>
  </div>
  <div class="rs-loop" aria-hidden="true"><span>↺ {e(r["loop"])}</span></div>
  <figcaption class="rs-note">{e(r["note"])}</figcaption>
</figure>'''


# ------------------------------------------------------------------ runtime
def hx_runtime(arg, ctx):
    r, c = _c(ctx, "runtime"), ctx["content"]["copy"]
    rows = "".join(
        f'<li data-s="{i}" class="{"hum" if i == r["human"] else ""}"><span class="n">{i + 1:02d}</span>'
        f'<span class="l">{e(t)}</span><span class="tr">{e(tag)}</span></li>'
        for i, (t, tag) in enumerate(r["layers"]))
    return f'''<div class="rt-grid">
  <figure class="rt" data-live aria-label="{e(r["box"])}">
    <span class="rt-io">{e(r["in"])}</span>
    <div class="rt-box">
      <div class="rt-h"><span>{e(r["box"])}</span><span>{e(r["trace"])}</span></div>
      <ol class="rt-layers">{rows}</ol>
    </div>
    <span class="rt-io out">{e(r["out"])}</span>
  </figure>
  <div class="rt-side">
    <p class="quote">{c["rt_quote"]}</p>
    <p class="rt-p">{e(c["rt_side"])}</p>
  </div>
</div>'''


# ------------------------------------------------------------------ collaboration
def hx_collab(arg, ctx):
    k = _c(ctx, "collab")
    n = k["nodes"]

    def node(key, cls=""):
        t, s = n[key]
        sub = f"<small>{e(s)}</small>" if s else ""
        return f'<div class="cl-n cl-{key} {cls}" data-n="{key}"><b>{e(t)}</b>{sub}</div>'

    edges = [["inv", "lead", ""], ["lead", "reg", ""], ["lead", "fin", ""], ["reg", "regc", ""], ["fin", "finc", ""],
             ["regc", "ev", ""], ["finc", "ev", ""], ["ev", "eval", ""], ["eval", "dec", "w"]]
    concepts = "".join(f'<li><b>{e(t)}</b><span>{e(d)}</span></li>' for t, d in k["concepts"])
    return f'''<div class="cl-wrap">
  <figure class="cl">
    <div class="cl-top"><span class="lbl" style="margin:0">{e(k["label"])}</span></div>
    <div class="cl-grid" data-links="{_links(edges)}">
      {node("inv", "wide")}{node("lead", "wide role")}{node("reg", "role")}{node("fin", "role")}
      {node("regc", "cl-cap")}{node("finc", "cl-cap")}{node("ev", "wide ev")}{node("eval", "wide")}{node("dec", "wide hum")}
    </div>
    <figcaption class="cl-note">{e(k["note"])}</figcaption>
  </figure>
  <ul class="cl-concepts">{concepts}</ul>
</div>'''


# ------------------------------------------------------------------ governance
def hx_gate(arg, ctx):
    g, c = _c(ctx, "gate"), ctx["content"]["copy"]
    btns = "".join(
        f'<button type="button" class="gt-btn{" sel" if i == 0 else ""}" aria-pressed="{"true" if i == 0 else "false"}" '
        f'data-res="{_links(x["res"])}" data-out="{x["out"]}" data-why="{e(x["why"], quote=True)}">{e(x["label"])}</button>'
        for i, x in enumerate(g["examples"]))
    first = g["examples"][0]
    checks = "".join(
        f'<li data-state="{first["res"][i]}"><span class="gt-ic" aria-hidden="true"></span>{e(t)}</li>'
        for i, t in enumerate(g["checks"]))
    outs = "".join(
        f'<span class="gt-o gt-o{i}{" on" if i == first["out"] else ""}">{e(t)}</span>' for i, t in enumerate(g["outcomes"]))
    chips = "".join(
        f'<li><svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">{ICONS[i]}</svg>{e(t)}</li>'
        for i, t in g["chips"])
    return f'''<div class="gt" data-gate>
  <div class="gt-pick"><span class="lbl" style="margin:0">{e(g["try"])}</span><div class="gt-btns">{btns}</div></div>
  <div class="gt-flow">
    <span class="gt-req"><span class="lbl" style="margin:0">{e(g["request"])}</span><b data-gate-label>{e(first["label"])}</b></span>
    <ol class="gt-checks">{checks}</ol>
    <div class="gt-outs">{outs}</div>
  </div>
  <p class="gt-why" data-gate-why aria-live="polite">{e(first["why"])}</p>
</div>
<div class="gt-controls">
  <div class="lbl">{e(c["gv_controls"])}</div>
  <ul class="ent-chips">{chips}</ul>
  <p class="gt-note">{e(c["gv_note"])}</p>
</div>'''


# ------------------------------------------------------------------ knowledge
def hx_knowledge(arg, ctx):
    k = _c(ctx, "knowledge")
    srcs = "".join(f'<li data-n="s{i}">{e(x)}</li>' for i, x in enumerate(k["sources"]))
    users = "".join(f'<li data-n="u{i}">{e(x)}</li>' for i, x in enumerate(k["users"]))
    edges = [[f"s{i}", "hub", "nd"] for i in range(len(k["sources"]))] + [["hub", f"u{i}", ""] for i in range(len(k["users"]))]
    return f'''<figure class="km" aria-label="{e(k["aria"])}">
  <div class="km-grid" data-links="{_links(edges)}" data-links-dir="h">
    <ul class="km-src">{srcs}</ul>
    <span class="km-arr" aria-hidden="true"></span>
    <div class="km-hub" data-n="hub"><b>{e(k["hub"])}</b><span>{e(k["hub_sub"])}</span></div>
    <span class="km-arr" aria-hidden="true"></span>
    <ul class="km-use">{users}</ul>
  </div>
  <p class="km-loop"><i class="km-ic" aria-hidden="true">↺</i>{e(k["loop"])}</p>
</figure>
<div class="datanote km-data"><strong>{e(k["data_h"])}</strong><p>{e(k["data_p"])}</p></div>'''


# ------------------------------------------------------------------ evaluation
def hx_evaluation(arg, ctx):
    v = _c(ctx, "evaluation")
    changes = "".join(f"<span>{e(x)}</span>" for x in v["changes"])
    flow = "".join(f'<span class="ev-n">{e(x)}</span><i aria-hidden="true"></i>' for x in v["flow"])
    crit = "".join(f'<li><b>{e(t)}</b><span>{e(d)}</span></li>' for t, d in v["criteria"])
    return f'''<div class="ev-changes"><span class="lbl" style="margin:0">{e(v["changes_lbl"])}</span>{changes}</div>
<figure class="evl">
  <div class="ev-flow">{flow}</div>
  <div class="ev-card">
    <div class="ev-card-h">{e(v["eval"])}</div>
    <ul class="ev-crit">{crit}</ul>
  </div>
  <i class="ev-down" aria-hidden="true"></i>
  <div class="ev-res"><b>{e(v["result"])}</b><span>{e(v["result_sub"])}</span></div>
  <figcaption class="ev-note">{e(v["note"])}</figcaption>
</figure>'''


# ------------------------------------------------------------------ observability
def hx_trace(arg, ctx):
    t = _c(ctx, "trace")
    fields = t["fields"]
    rows, panels = [], []
    last = len(t["rows"]) - 1
    for i, (time, label, vals) in enumerate(t["rows"]):
        sel = i == last
        hum = " hum" if i == t["human"] else ""
        rows.append(f'<li><button type="button" class="tr-row{hum}{" sel" if sel else ""}" aria-pressed="{"true" if sel else "false"}" data-tr="{i}">'
                    f'<time>{e(time)}</time><span>{e(label)}</span></button></li>')
        vals = vals + [f'{t["date"]} · {time}']
        muted = ' class="muted"'
        dl = "".join(f'<div><dt>{e(f)}</dt><dd{muted if v == "—" else ""}>{e(v)}</dd></div>' for f, v in zip(fields, vals))
        panels.append(f'<div class="tr-panel" data-trp="{i}"{"" if sel else " hidden"}><div class="tr-ph"><time>{e(time)}</time><b>{e(label)}</b></div><dl>{dl}</dl></div>')
    return f'''<div class="ob" data-trace>
  <div class="tr-list">
    <div class="tr-top"><span class="case-id">{e(t["title"])}</span></div>
    <ol>{"".join(rows)}</ol>
    <p class="tr-hint">{e(t["hint"])}</p>
  </div>
  <div class="tr-insp">{"".join(panels)}<p class="tr-note">{e(t["note"])}</p></div>
</div>'''


# ------------------------------------------------------------------ harness -> spaces
def hx_spaces(arg, ctx):
    s = _c(ctx, "spaces")
    root = ctx["root"]
    chips = "".join(f"<span>{e(x)}</span>" for x in s["chips"])

    def card(space, steps):
        li = "".join(f'<li class="{"hum" if i == len(steps) - 1 else ""}">{e(x)}</li>' for i, x in enumerate(steps))
        return f'<a class="hs-card" href="{root}{space}/"><span class="hs-top">{_wm(space)}<span class="go">→</span></span><ol>{li}</ol></a>'

    legend = "".join(f'<div><b>{e(t)}</b><span>{e(d)}</span></div>' for t, d in s["legend"])
    return f'''<figure class="hs">
  <div class="hs-harness"><span class="hs-name">Deepin Harness</span><span class="hs-chips">{chips}</span></div>
  <svg class="hs-split" viewBox="0 0 400 44" preserveAspectRatio="none" aria-hidden="true"><path d="M200 0 V14 C200 30 100 22 100 44 M200 14 C200 30 300 22 300 44"/></svg>
  <div class="hs-cards">{card("risk", s["risk"])}{card("finance", s["finance"])}</div>
</figure>
<div class="hs-legend">{legend}</div>'''


# ------------------------------------------------------------------ research
def hx_research(arg, ctx):
    items = "".join(f'<li><span class="n">{i + 1:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>'
                    for i, (t, d) in enumerate(ctx["content"]["research"]))
    return f'<ol class="rsx">{items}</ol>'


COMPONENTS = {
    "hx_runtime_org": hx_runtime_org,
    "hx_problem": hx_problem,
    "hx_org_model": hx_org_model,
    "hx_reasoning": hx_reasoning,
    "hx_runtime": hx_runtime,
    "hx_collab": hx_collab,
    "hx_gate": hx_gate,
    "hx_knowledge": hx_knowledge,
    "hx_evaluation": hx_evaluation,
    "hx_trace": hx_trace,
    "hx_spaces": hx_spaces,
    "hx_research": hx_research,
}
