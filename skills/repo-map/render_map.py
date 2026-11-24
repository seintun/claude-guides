#!/usr/bin/env python3
"""Render a repo-map folder as one interactive study page (map.html).

Usage: python3 render_map.py <map-folder> [--out <file>] [--fonts]

--out defaults to <map-folder>/map.html. Standard library only. The page is one self-contained file:
inline CSS and JS, no libraries. By default it makes no network request at all and uses system fonts; --fonts
adds three fonts from Google Fonts (sent with no referrer, but Google sees the viewer's IP address). It opens from disk in any browser.

The page: a sticky header with a notes-read meter, display settings (System, Light, Paper, Dark; three
text sizes) and Expand all; a fact strip; a guided reading path; the component graph; one collapsible
section per note in What / Why / How form; flow walkthroughs that light each step's components; a
glossary with flashcard review; open questions; read checkboxes saved in the browser.
"""
import argparse
import html
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import check_map  # noqa: E402  (same folder: one parser for notes)

CARD_W, CARD_H = 200, 64  # full box size; top-down levels may narrow boxes to 150px; labels stay 14px and 12px


def components(notes):
    comps = {}
    for rel, n in notes.items():
        p = n["props"] or {}
        if p.get("type") == "component":
            deps = [t.strip() for d in check_map.as_list(p.get("depends_on")) for t in check_map.WIKILINK.findall(d)]
            comps[n["name"]] = {"kind": str(p.get("kind", "")), "system": str(p.get("system", "") or ""), "provides": str(p.get("provides", "") or ""), "deps": deps}
    return comps




def make_ids(names):
    """One unique element id per note name. Unicode letters are kept (注文 stays 注文), and names that differ only
    in punctuation or case (order-api, order_api, Order API) get a numeric suffix instead of colliding."""
    ids, used = {}, set()
    for name in sorted(names):
        base = "n-" + (re.sub(r"[^\w]+", "-", name.lower(), flags=re.UNICODE).strip("-_") or "note")
        cand, k = base, 2
        while cand in used:
            cand, k = f"{base}-{k}", k + 1
        used.add(cand)
        ids[name] = cand
    return ids


def page(notes, fonts=False):
    comps = components(notes)
    ids = make_ids([n["name"] for n in notes.values()])
    idx = (notes.get("index.md") or {}).get("props") or {}
    repo = str(idx.get("repo", "repository"))
    data = {
        "repo": repo, "commit": str(idx.get("commit", "")), "date": str(idx.get("date", "")),
        "notes": [{"name": n["name"], "id": ids[n["name"]], "rel": rel, "type": (n["props"] or {}).get("type", ""),
                   "aliases": check_map.as_list((n["props"] or {}).get("aliases")),
                   "props": {k: v for k, v in (n["props"] or {}).items() if k != "type"},
                   "body": n["body"]} for rel, n in sorted(notes.items())],
        "graph": {"nodes": [{"name": k, "id": ids.get(k, "n-missing"), "kind": c["kind"], "system": c["system"], "provides": c["provides"]} for k, c in sorted(comps.items())],
                  "edges": [[k, d] for k, c in comps.items() for d in c["deps"] if d in comps],
                  "w": CARD_W, "h": CARD_H},
    }
    # Escape every <, > and & in the embedded data, not only "</": "<!--" followed by "<script" would otherwise
    # switch the HTML parser into a state where the real </script> no longer ends the script, and the page goes blank.
    payload = json.dumps(data).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    key = "repo-map-" + re.sub(r"[^a-z0-9]+", "-", repo.lower()) + "-v1"
    return TEMPLATE.replace("__FONTS__", FONTS if fonts else "").replace("__TITLE__", html.escape(repo)).replace("__KEY__", key).replace("__DATA__", payload)


FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&family=Space+Grotesk:wght@500;700&family=JetBrains+Mono:wght@400;600&display=swap">
"""


TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__ repo map</title>
<meta name="referrer" content="no-referrer">
__FONTS__<style>
/* A calm study page: one reading column, collapsible sections, no pure white or black, four themes, three text sizes. */
:root {
  --bg: #f2f3ee; --surface: #f9faf6; --ink: #1e2924; --muted: #52605a; --line: #d8ddd4;
  --accent: #2e6a4e; --accent-ink: #f9faf6; --accent-soft: #e0ebe3; --amber: #845200; --amber-soft: #f4e9d4;
  --ph1: #2e6a4e; --ph2: #2c6688; --ph3: #6e4f96; --focus: #1f5fbf;
  --k-service: #2a78d6; --k-job: #e0632a; --k-library: #13996a; --k-website: #b0408e; --k-resource: #6b7a74;
  --fs: 1.0625rem; --hdr: 60px;
  --font-display: "Space Grotesk", "Segoe UI", system-ui, sans-serif;
  --font-body: "Atkinson Hyperlegible", "Segoe UI", system-ui, -apple-system, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, "SF Mono", Menlo, Consolas, monospace;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]):not([data-theme="paper"]) {
    --bg: #14181a; --surface: #1a1f22; --ink: #dde4df; --muted: #a2ada7; --line: #2c3337;
    --accent: #86c9a3; --accent-ink: #10201a; --accent-soft: #1e2b25; --amber: #e0b566; --amber-soft: #2a2418;
    --ph1: #86c9a3; --ph2: #7db8db; --ph3: #c0a2e3; --focus: #8ab4ff; color-scheme: dark;
    --k-service: #4189e4; --k-job: #d4602a; --k-library: #199e70; --k-website: #d860a8; --k-resource: #93a09a;
  }
}
:root[data-theme="dark"] {
  --bg: #14181a; --surface: #1a1f22; --ink: #dde4df; --muted: #a2ada7; --line: #2c3337;
  --accent: #86c9a3; --accent-ink: #10201a; --accent-soft: #1e2b25; --amber: #e0b566; --amber-soft: #2a2418;
  --ph1: #86c9a3; --ph2: #7db8db; --ph3: #c0a2e3; --focus: #8ab4ff; color-scheme: dark;
  --k-service: #4189e4; --k-job: #d4602a; --k-library: #199e70; --k-website: #d860a8; --k-resource: #93a09a;
}
:root[data-theme="paper"] {
  --bg: #f1e8d6; --surface: #f7efdf; --ink: #3a2e22; --muted: #66563f; --line: #dccdb0;
  --accent: #3b6a56; --accent-ink: #f7efdf; --accent-soft: #e4e2c9; --amber: #844b00; --amber-soft: #ecdcbb;
  --ph1: #3b6a56; --ph2: #2f5f7c; --ph3: #6c4d8a; --focus: #1f5fbf; color-scheme: light;
}
:root[data-size="sm"] { --fs: 1rem; }
:root[data-size="lg"] { --fs: 1.1875rem; }
* { box-sizing: border-box; }
html { scroll-padding-top: calc(var(--hdr) + 12px); }
body { margin: 0; background: var(--bg); color: var(--ink); font-family: var(--font-body); font-size: var(--fs); line-height: 1.7; }
a { color: var(--accent); text-underline-offset: 0.18em; }
a:hover { text-decoration-thickness: 2px; }
a.missing { color: var(--amber); text-decoration: underline dotted; }
:focus-visible { outline: 3px solid var(--focus); outline-offset: 2px; border-radius: 4px; }
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0; }
.skip { position: absolute; left: -999px; top: 8px; background: var(--surface); color: var(--ink); padding: 8px 12px; z-index: 20; }
.skip:focus { left: 16px; }
.wrap { max-width: 880px; margin: 0 auto; padding-left: 16px; padding-right: 16px; }
header.top { position: sticky; top: 0; z-index: 5; background: var(--surface); border-bottom: 1px solid var(--line); }
header.top .wrap { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 12px; padding-block: 8px; }
.brand { font-family: var(--font-display); font-weight: 700; font-size: 1.05rem; margin-right: auto; }
.meter { display: flex; align-items: center; gap: 8px; font-size: 0.875rem; color: var(--muted); font-variant-numeric: tabular-nums; }
.meter progress { width: 110px; height: 10px; accent-color: var(--accent); }
.btn { font: inherit; font-size: 0.875rem; min-height: 36px; padding: 6px 12px; border-radius: 8px; border: 1px solid var(--line); background: var(--surface); color: var(--ink); cursor: pointer; display: inline-flex; align-items: center; gap: 6px; }
.btn:hover { border-color: var(--accent); }
.btn.primary { background: var(--accent); color: var(--accent-ink); border-color: var(--accent); }
details.display { position: relative; }
details.display > summary { list-style: none; }
details.display > summary::-webkit-details-marker { display: none; }
.display-panel { position: absolute; right: 0; top: calc(100% + 6px); width: min(300px, calc(100vw - 32px)); background: var(--surface); border: 1px solid var(--line); border-radius: 12px; padding: 14px 16px; box-shadow: 0 8px 28px rgb(0 0 0 / 0.16); z-index: 30; }
.display-panel fieldset { border: 0; margin: 0 0 12px; padding: 0; }
.display-panel legend { font-family: var(--font-display); font-weight: 700; font-size: 0.95rem; margin-bottom: 6px; }
.seg { display: flex; flex-wrap: wrap; gap: 6px; }
.seg label { position: relative; }
.seg input { position: absolute; opacity: 0; width: 1px; height: 1px; }
.seg span { display: inline-flex; align-items: center; gap: 6px; min-height: 36px; padding: 4px 10px; border: 1px solid var(--line); border-radius: 8px; font-size: 0.875rem; cursor: pointer; }
.seg input:checked + span { border-color: var(--accent); background: var(--accent-soft); font-weight: 700; }
.seg input:focus-visible + span { outline: 3px solid var(--focus); outline-offset: 2px; }
.sw { width: 14px; height: 14px; border-radius: 50%; border: 1px solid var(--muted); }
.sw.light { background: #f9faf6; } .sw.paper { background: #f1e8d6; } .sw.dark { background: #1a1f22; } .sw.system { background: linear-gradient(90deg, #f9faf6 50%, #1a1f22 50%); }
main { padding-block: 28px 64px; }
h1, h2, h3, h4 { font-family: var(--font-display); line-height: 1.25; text-wrap: balance; }
h1 { font-size: clamp(1.8rem, 4.5vw, 2.5rem); margin: 0 0 12px; letter-spacing: -0.01em; }
h2 { font-size: 1.25rem; margin: 0; }
h3 { font-size: 1.05rem; margin: 1.3em 0 0.4em; }
h4 { font-size: 0.8125rem; font-family: var(--font-mono); letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); margin: 1.2em 0 0.2em; }
p, li { max-width: 66ch; }
.lede { font-size: 1.12em; color: var(--muted); margin: 0 0 24px; }
.eyebrow { font-family: var(--font-mono); font-size: 0.8125rem; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); margin: 0 0 6px; }
.part { font-family: var(--font-mono); font-size: 0.8125rem; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); margin: 32px 0 4px; border-bottom: 2px solid var(--line); padding-bottom: 4px; }
.facts { display: grid; grid-template-columns: repeat(5, 1fr); border: 1px solid var(--line); border-radius: 12px; background: var(--surface); margin: 0 0 28px; overflow: hidden; }
.facts div { padding: 12px 16px; border-right: 1px solid var(--line); min-width: 0; }
.facts div:last-child { border-right: none; }
.facts dt { font-family: var(--font-mono); font-size: 0.75rem; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); }
.facts dd { margin: 2px 0 0; font-weight: 700; font-size: 1.3rem; font-family: var(--font-display); }
.path { margin: 0 0 28px; }
.path h2 { margin-bottom: 10px; }
.path ol { list-style: none; padding: 0; margin: 0; counter-reset: step; }
.path li { counter-increment: step; display: grid; grid-template-columns: 2.4rem 1fr; gap: 4px 12px; padding: 12px 0; border-bottom: 1px solid var(--line); max-width: none; }
.path li::before { content: counter(step); font-family: var(--font-mono); font-weight: 600; color: var(--accent); font-size: 1.1rem; }
.path .why { display: block; color: var(--muted); font-size: 0.95rem; }
.filter { width: 100%; font: inherit; padding: 8px 12px; border: 1px solid var(--line); border-radius: 8px; background: var(--surface); color: var(--ink); margin: 8px 0 4px; }
details.sec { border-bottom: 1px solid var(--line); scroll-margin-top: calc(var(--hdr) + 12px); }
details.sec > summary { list-style: none; cursor: pointer; display: grid; grid-template-columns: 1fr auto; gap: 12px; align-items: center; padding: 14px 4px; }
details.sec > summary::-webkit-details-marker { display: none; }
details.sec > summary:hover h3 { color: var(--accent); }
details.sec > summary h3 { margin: 0; }
details.sec > summary .sub { display: block; color: var(--muted); font-size: 0.92rem; font-family: var(--font-body); font-weight: 400; margin-top: 2px; }
.side { display: flex; align-items: center; gap: 8px; }
.chip { font-family: var(--font-mono); font-size: 0.75rem; padding: 2px 8px; border-radius: 999px; background: var(--accent-soft); color: var(--accent); }
.chip[class*="kind-"] { background: transparent; color: var(--ink); border: 1px solid var(--line); display: inline-flex; align-items: center; gap: 6px; }
.chip[class*="kind-"]::before { content: ""; width: 9px; height: 9px; border-radius: 2px; background: var(--kc, var(--muted)); }
.kind-service { --kc: var(--k-service); } .kind-job { --kc: var(--k-job); } .kind-library { --kc: var(--k-library); } .kind-website { --kc: var(--k-website); } .kind-resource { --kc: var(--k-resource); }
.kind-website.chip::before { border-radius: 50% 0; } .kind-job.chip::before { border-radius: 50%; } .kind-resource.chip::before { border-radius: 1px; transform: rotate(45deg) scale(.8); }
.chev { width: 18px; height: 18px; transition: transform 0.2s; color: var(--muted); }
details[open] > summary .chev { transform: rotate(180deg); }
.body { padding: 0 4px 24px; min-width: 0; }
dl.props { display: grid; grid-template-columns: max-content 1fr; gap: 2px 14px; font-size: 0.92rem; background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 10px 14px; margin: 4px 0 8px; }
dl.props dt { font-family: var(--font-mono); color: var(--muted); }
dl.props dd { margin: 0; min-width: 0; overflow-wrap: anywhere; }
pre { background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; overflow-x: auto; }
code { font-family: var(--font-mono); font-size: 0.86em; background: var(--accent-soft); color: var(--ink); padding: 1px 6px; border-radius: 5px; overflow-wrap: anywhere; }
pre code { background: none; padding: 0; }
.donebox { display: inline-flex; align-items: center; gap: 8px; margin-top: 8px; font-size: 0.92rem; color: var(--muted); cursor: pointer; }
.donebox input { width: 20px; height: 20px; accent-color: var(--accent); }
figure.viz { margin: 16px 0; background: var(--surface); border: 1px solid var(--line); border-radius: 12px; padding: 12px; }
figure.viz .scroll { overflow-x: auto; overscroll-behavior-x: contain; }
figure.viz svg { display: block; max-width: none; height: auto; }
.vizbar { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 16px; margin: 0 0 8px; font-size: 0.875rem; color: var(--muted); }
.legend { display: flex; flex-wrap: wrap; gap: 6px 14px; list-style: none; margin: 0; padding: 0; }
.legend li { display: inline-flex; align-items: center; gap: 6px; color: var(--ink); max-width: none; }
.legend svg { width: 12px; height: 12px; }
.vizbar label { display: inline-flex; align-items: center; gap: 6px; margin-left: auto; cursor: pointer; }
.vizbar input { accent-color: var(--accent); width: 16px; height: 16px; }
.kindbar { display: flex; gap: 2px; height: 12px; margin: 6px 0 4px; }
.kindbar span { background: var(--kc); min-width: 6px; }
.kindbar span:first-child { border-radius: 4px 0 0 4px; } .kindbar span:last-child { border-radius: 0 4px 4px 0; }
.kindbar span:only-child { border-radius: 4px; }
.kindsum { margin: 0 0 28px; }
.kindsum .eyebrow { margin-bottom: 2px; }
figure.viz figcaption { font-size: 0.9rem; color: var(--muted); margin-top: 8px; }
.s-box { fill: var(--surface); stroke: var(--line); stroke-width: 1.25; }
.s-hi { fill: var(--accent-soft); stroke: var(--accent); stroke-width: 2.5; }
.s-stripe { fill: var(--kc, var(--muted)); }
.s-glyph { fill: var(--kc, var(--muted)); }
.s-col { fill: var(--muted); font-family: var(--font-mono); font-size: 12px; letter-spacing: .06em; text-transform: uppercase; }
.s-t { fill: var(--ink); font-family: var(--font-body); font-size: 14px; font-weight: 700; }
.s-sub { fill: var(--muted); font-family: var(--font-body); font-size: 12px; }
.s-line { stroke: var(--muted); stroke-width: 1.5; fill: none; opacity: .55; transition: opacity .15s, stroke .15s; }
.s-dim { opacity: 0.25; }
svg.hovering .s-line { opacity: .1; } svg.hovering .s-node { opacity: .35; }
svg.hovering .s-line.hl { opacity: 1; stroke: var(--accent); stroke-width: 2.25; }
svg.hovering .s-node.hl { opacity: 1; }
@media (prefers-reduced-motion: reduce) { .s-line { transition: none; } }
.s-node { cursor: pointer; }
.s-node:focus-visible .s-box, .s-node:focus-visible .s-hi { stroke: var(--focus); stroke-width: 3; }
.stepbar { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin: 8px 0; }
.stepbar .pos { font-family: var(--font-mono); font-size: 0.875rem; color: var(--muted); }
ol.steps { list-style: none; padding: 0; margin: 8px 0; display: grid; gap: 6px; }
ol.steps li { border: 1px solid var(--line); border-radius: 10px; padding: 8px 12px; background: var(--surface); cursor: pointer; max-width: none; }
ol.steps li.on { border-color: var(--accent); background: var(--accent-soft); }
dl.gloss { display: grid; grid-template-columns: minmax(110px, max-content) 1fr; gap: 8px 16px; margin: 12px 0; }
dl.gloss dt { font-weight: 700; font-family: var(--font-mono); font-size: 0.92rem; }
dl.gloss dd { margin: 0; min-width: 0; }
dl.gloss .aka { display: block; color: var(--muted); font-size: 0.875rem; }
.quiz { background: var(--accent-soft); border-radius: 12px; padding: 14px 16px; margin: 16px 0; }
.quiz .q { font-family: var(--font-display); font-weight: 700; font-size: 1.15rem; }
.quiz .a { margin: 6px 0 10px; }
.gaps { display: grid; gap: 10px; margin: 12px 0; padding: 0; list-style: none; }
.gaps li { padding: 10px 14px; border: 1px solid var(--line); border-radius: 10px; background: var(--surface); max-width: none; }
.gaps .who { font-family: var(--font-mono); font-size: 0.8125rem; color: var(--muted); }
.hidden { display: none !important; }
footer { color: var(--muted); font-size: 0.9rem; border-top: 1px solid var(--line); margin-top: 48px; padding-top: 16px; }
.admin { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 12px; margin-top: 12px; }
@media (max-width: 560px) {
  header.top .brand { display: none; }
  .facts { grid-template-columns: 1fr 1fr; }
  .facts div { border-right: none; border-bottom: 1px solid var(--line); }
  dl.gloss, dl.props { grid-template-columns: 1fr; gap: 2px 0; }
  dl.gloss dd { margin-bottom: 8px; }
}
@media (prefers-reduced-motion: reduce) { .chev { transition: none; } }
@media (prefers-reduced-motion: no-preference) { html { scroll-behavior: smooth; } }
</style></head><body>
<a class="skip" href="#main">Skip to the map</a>
<header class="top" id="topbar"><div class="wrap">
  <span class="brand" id="brand"></span>
  <span class="meter"><progress id="readProg" value="0" max="1"></progress><span id="readText"></span></span>
  <details class="display" id="display">
    <summary class="btn" aria-label="Display settings: theme and text size"><svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M8 1.5a6.5 6.5 0 0 1 0 13z" fill="currentColor"/></svg>Display</summary>
    <div class="display-panel">
      <fieldset><legend>Theme</legend><div class="seg">
        <label><input type="radio" name="theme" value="system" id="th-system"><span><i class="sw system" aria-hidden="true"></i>System</span></label>
        <label><input type="radio" name="theme" value="light" id="th-light"><span><i class="sw light" aria-hidden="true"></i>Light</span></label>
        <label><input type="radio" name="theme" value="paper" id="th-paper"><span><i class="sw paper" aria-hidden="true"></i>Paper</span></label>
        <label><input type="radio" name="theme" value="dark" id="th-dark"><span><i class="sw dark" aria-hidden="true"></i>Dark</span></label>
      </div></fieldset>
      <fieldset><legend>Text size</legend><div class="seg">
        <label><input type="radio" name="size" value="sm" id="sz-sm"><span>Small</span></label>
        <label><input type="radio" name="size" value="md" id="sz-md"><span>Medium</span></label>
        <label><input type="radio" name="size" value="lg" id="sz-lg"><span>Large</span></label>
      </div></fieldset>
    </div>
  </details>
  <button class="btn" id="toggleAll" type="button" aria-controls="main">Expand all</button>
</div></header>
<main id="main" class="wrap"></main>
<div class="sr-only" role="status" id="stat"></div>
<script>
const D = __DATA__;
(function () {
  var root = document.documentElement, hostTheme = root.getAttribute('data-theme');
  var KEY = '__KEY__', PREFS = KEY + '-prefs';
  var CHEV = '<svg class="chev" viewBox="0 0 20 20" aria-hidden="true"><path d="M5 7.5l5 5 5-5" fill="none" stroke="currentColor" stroke-width="2"/></svg>';
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); };
  var dict = function () { return Object.create(null); };  /* no inherited keys: a note may be named constructor */
  var byName = dict();
  D.notes.forEach(function (n) { byName[n.name.toLowerCase()] = n; });
  D.notes.forEach(function (n) { n.aliases.forEach(function (a) { var k = String(a).toLowerCase(); if (!byName[k]) byName[k] = n; }); });  /* a note name always wins over an alias */
  var of = function (t) { return D.notes.filter(function (n) { return n.type === t; }); };

  function inline(s) {
    return esc(s).replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]*))?\]\]/g, function (m, t, label) {
        var n = byName[t.trim().toLowerCase()];
        return n ? '<a href="#' + n.id + '">' + (label || t) + '</a>' : '<a class="missing" title="No note">' + (label || t) + '</a>';
      })
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/\bUNKNOWN\b/g, '<strong>UNKNOWN</strong>');
  }
  function md(text) {
    var out = [], list = null, fence = null, buf = [], pending = null;
    function push(x) { if (pending) { out.push(pending); pending = null; } out.push(x); }
    function close() { if (list) { out.push('</' + list + '>'); list = null; } }
    text.split('\n').forEach(function (line) {
      if (fence !== null) {
        if (line.indexOf('```') === 0) {
          push(fence === 'mermaid' ? '<details><summary>Mermaid source (renders in Obsidian)</summary><pre><code>' + esc(buf.join('\n')) + '</code></pre></details>'
                                       : '<pre tabindex="0"><code>' + esc(buf.join('\n')) + '</code></pre>');
          fence = null; buf = [];
        } else buf.push(line);
        return;
      }
      if (line.indexOf('```') === 0) { close(); fence = line.slice(3).trim(); return; }
      var m;
      if (/^#\s/.test(line)) { close(); return; }   /* the note title is already the section heading */
      if ((m = line.match(/^(#{2,4}) (.*)/))) { close(); pending = '<h4>' + inline(m[2]) + '</h4>'; }   /* written only if content follows */
      else if ((m = line.match(/^\s*[-*] (.*)/))) { if (list !== 'ul') { close(); push('<ul>'); list = 'ul'; } push('<li>' + inline(m[1]) + '</li>'); }
      else if ((m = line.match(/^\s*\d+\. (.*)/))) { if (list !== 'ol') { close(); push('<ol>'); list = 'ol'; } push('<li>' + inline(m[1]) + '</li>'); }
      else if (!line.trim()) close();
      else { close(); push('<p>' + inline(line) + '</p>'); }
    });
    close();
    return out.join('\n');
  }
  function title(n) { var m = n.body.match(/^# (.+)$/m); return m ? m[1] : n.name; }
  function firstLine(n) {
    var lines = n.body.split('\n').filter(function (l) { return l.trim() && !/^#|^```|^\s*[-*\d]/.test(l); });
    return lines.length ? lines[0].replace(/\[\[([^\]|#]+)[^\]]*\]\]/g, '$1').replace(/`/g, '') : '';
  }
  function props(n) {
    var keys = Object.keys(n.props).filter(function (k) { return k !== 'aliases'; });
    if (!keys.length) return '';
    return '<dl class="props">' + keys.map(function (k) { var v = n.props[k]; return '<dt>' + esc(k) + '</dt><dd>' + inline(Array.isArray(v) ? v.join(', ') : v) + '</dd>'; }).join('') + '</dl>';
  }
  function linksIn(text) {
    var s = new Set(), re = /\[\[([^\]|#]+)/g, m;
    while ((m = re.exec(String(text)))) { var n = byName[m[1].trim().toLowerCase()]; s.add(n ? n.name : m[1].trim()); }
    return s;
  }

  var gid = 0, GX = 88, GY = 22, TGX = 28, TGY = 64, HEAD = 30;
  var KINDS = ['service', 'website', 'job', 'library', 'resource'];
  var GLYPH = {  /* a second cue beside colour: circle, diamond, triangle, square, hexagon */
    service: '<circle cx="6" cy="6" r="5"/>', website: '<path d="M6 0.5 11.5 6 6 11.5 0.5 6z"/>',
    job: '<path d="M6 0.8 11.4 11 0.6 11z"/>', library: '<rect x="1" y="1" width="10" height="10" rx="1.5"/>',
    resource: '<path d="M6 0.5 10.8 3.25 10.8 8.75 6 11.5 1.2 8.75 1.2 3.25z"/>'
  };
  function fitName(name, room) {  /* ~8px per character of 14px bold text; the full name stays in the tooltip */
    var max = Math.max(4, Math.floor(room / 8));
    return name.length <= max ? name : name.slice(0, max - 1) + '\u2026';
  }
  function glyph(kind, x, y) { return '<g class="s-glyph kind-' + esc(kind) + '" transform="translate(' + x + ',' + y + ')">' + (GLYPH[kind] || GLYPH.resource) + '</g>'; }

  /* Edges within a set of names, and the same edges with every edge implied by a longer path removed
     (if A uses B and B uses C, the direct A->C is dropped): the overview shows only the second set. */
  function edgesOf(set, reduce) {
    var out = dict();
    set.forEach(function (n) { out[n] = []; });
    D.graph.edges.forEach(function (e) { if (set.has(e[0]) && set.has(e[1]) && e[0] !== e[1] && out[e[0]].indexOf(e[1]) < 0) out[e[0]].push(e[1]); });
    var list = [];
    set.forEach(function (a) { out[a].forEach(function (b) { list.push([a, b]); }); });
    if (!reduce) return list;
    /* Strongly connected groups (Tarjan): components that reach each other through a cycle share a group. */
    var idx = dict(), low = dict(), onStack = dict(), comp = dict(), stack = [], counter = 0, groups = 0;
    function strong(v) {
      idx[v] = low[v] = counter++; stack.push(v); onStack[v] = true;
      out[v].forEach(function (w) {
        if (idx[w] === undefined) { strong(w); low[v] = Math.min(low[v], low[w]); }
        else if (onStack[w]) low[v] = Math.min(low[v], idx[w]);
      });
      if (low[v] === idx[v]) { var w; do { w = stack.pop(); onStack[w] = false; comp[w] = groups; } while (w !== v); groups++; }
    }
    set.forEach(function (v) { if (idx[v] === undefined) strong(v); });
    var cout = dict();  /* edges between groups */
    list.forEach(function (e) {
      var ca = comp[e[0]], cb = comp[e[1]];
      if (ca === cb) return;
      cout[ca] = cout[ca] || new Set(); cout[ca].add(cb);
    });
    function reachesAnotherWay(ca, cb) {  /* is group cb reachable from ca without the direct ca->cb link? */
      var seen = new Set([ca]), todo = Array.from(cout[ca] || []).filter(function (x) { return x !== cb; });
      while (todo.length) {
        var x = todo.pop();
        if (x === cb) return true;
        if (seen.has(x)) continue;
        seen.add(x);
        (cout[x] || new Set()).forEach(function (y) { todo.push(y); });
      }
      return false;
    }
    return list.filter(function (e) {
      var ca = comp[e[0]], cb = comp[e[1]];
      return ca === cb || !reachesAnotherWay(ca, cb);
    });
  }

  /* Layered layout: a component sits one level after everything in the set that uses it, so every arrow points
     forward, to a dependency. Rows inside each column are reordered to cut crossings (median of
     neighbours, a few sweeps each way). Boxes keep their full size; a wide graph scrolls sideways. Cycles are cut. */
  function layout(names, edges, dir) {
    var g = D.graph, set = new Set(names), users = dict(), deps = dict();
    names.forEach(function (n) { users[n] = []; deps[n] = []; });
    (edges || edgesOf(set, false)).forEach(function (e) { deps[e[0]].push(e[1]); users[e[1]].push(e[0]); });
    var level = dict();
    function lv(n, seen) {
      if (level[n] !== undefined) return level[n];
      if (seen.has(n)) return 0;
      var s2 = new Set(seen); s2.add(n);
      var l = users[n].length ? Math.max.apply(null, users[n].map(function (u) { return lv(u, s2) + 1; })) : 0;
      level[n] = l; return l;
    }
    names.forEach(function (n) { lv(n, new Set()); });
    var sys = dict(); g.nodes.forEach(function (n) { sys[n.name] = (n.system || '') + '\u0000' + n.kind; });
    var cols = [];
    names.forEach(function (n) { (cols[level[n]] = cols[level[n]] || []).push(n); });
    cols = cols.filter(Boolean).map(function (c) { return c.sort(function (a, b) { return (sys[a] + a).localeCompare(sys[b] + b); }); });
    var row = dict();
    function index() { cols.forEach(function (c) { c.forEach(function (n, i) { row[n] = i; }); }); }
    function median(list) {
      if (!list.length) return null;
      var v = list.map(function (n) { return row[n]; }).sort(function (a, b) { return a - b; }), m = Math.floor(v.length / 2);
      return v.length % 2 ? v[m] : (v[m - 1] + v[m]) / 2;
    }
    index();
    for (var sweep = 0; sweep < 6; sweep++) {
      var forward = sweep % 2 === 0, order = forward ? cols.slice(1) : cols.slice(0, -1).reverse();
      order.forEach(function (c) {
        var key = dict();
        c.forEach(function (n) { var m = median(forward ? users[n] : deps[n]); key[n] = m === null ? row[n] : m; });
        c.sort(function (a, b) { return key[a] - key[b] || row[a] - row[b]; });
        c.forEach(function (n, i) { row[n] = i; });
      });
    }
    var widest = Math.max.apply(null, cols.map(function (c) { return c.length; }));
    /* Direction: a graph deeper than it is wide reads top-down (the page already scrolls that way); a shallow, wide
       one reads left to right. Either way each level is one band; top-down boxes may narrow to fit, never under 150px. */
    var tb = dir ? dir === 'TB' : cols.length > widest;
    var bw = g.w;
    if (tb) {  /* fit the widest level to the column: narrower boxes, never under 150px (then the frame scrolls) */
      var main = typeof document !== 'undefined' && document.getElementById ? document.getElementById('main') : null;
      var avail = (main && main.clientWidth ? main.clientWidth : 880) - 32 - 26 - 30 - 24;  /* page padding, frame, loop room, margins */
      bw = Math.max(150, Math.min(g.w, Math.floor((avail - (widest - 1) * TGX) / widest)));
    }
    var pos = dict();
    cols.forEach(function (c, li) {
      if (tb) {
        var offx = (widest - c.length) * (bw + TGX) / 2;   /* centre narrow levels */
        c.forEach(function (n, i) { pos[n] = { x: offx + i * (bw + TGX), y: HEAD + li * (g.h + TGY), col: li }; });
      } else {
        var offy = (widest - c.length) * (g.h + GY) / 2;     /* centre short columns */
        c.forEach(function (n, i) { pos[n] = { x: li * (g.w + GX), y: HEAD + offy + i * (g.h + GY), col: li }; });
      }
    });
    if (tb) return { pos: pos, cols: cols.length, tb: true, bw: bw, W: widest * (bw + TGX) - TGX + 24, H: HEAD + cols.length * (g.h + TGY) - TGY + 24 };
    return { pos: pos, cols: cols.length, tb: false, bw: bw, W: cols.length * (g.w + GX) - GX + 24, H: HEAD + widest * (g.h + GY) - GY + 24 };
  }

  /* opts: only (Set of names; all when absent), lit (Set: others dimmed), cur (Set: outlined), all (bool: show
     implied edges too), caption, label, heads (bool: column headings) */
  function graph(opts) {
    var g = D.graph, at = dict();
    g.nodes.forEach(function (n) { at[n.name] = n; });
    var names = g.nodes.map(function (n) { return n.name; }).filter(function (n) { return !opts.only || opts.only.has(n); });
    if (!names.length) return '';
    var set = new Set(names), full = edgesOf(set, false), shown = opts.all ? full : edgesOf(set, true);
    var L = layout(names, full), P = L.pos;
    if (L.tb) L.W += 30;
    var BW = L.bw;
    var mid = 'arr' + (++gid), lit = opts.lit || null, cur = opts.cur || null;
    var ox = 12, oy = 12;
    var edges = shown.map(function (e) {
      var a = P[e[0]], b = P[e[1]], dim = lit && !(lit.has(e[0]) && lit.has(e[1])) ? ' s-dim' : '';
      var x1 = a.x + BW + ox, y1 = a.y + g.h / 2 + oy, x2 = b.x + ox - 3, y2 = b.y + g.h / 2 + oy, d;
      if (L.tb && b.col > a.col) {   /* top-down: bottom edge of the user to the top edge of the dependency */
        x1 = a.x + BW / 2 + ox; y1 = a.y + g.h + oy; x2 = b.x + BW / 2 + ox; y2 = b.y + oy - 3;
        var cy = Math.max(24, (y2 - y1) / 2);
        d = 'M' + x1 + ',' + y1 + ' C' + x1 + ',' + (y1 + cy) + ' ' + x2 + ',' + (y2 - cy) + ' ' + x2 + ',' + y2;
      } else if (L.tb) {             /* a cycle pointing back up: loop out to the right */
        x1 = a.x + BW + ox; y1 = a.y + g.h / 2 + oy; x2 = b.x + BW + ox + 3; y2 = b.y + g.h / 2 + oy;
        var rx = Math.max(x1, x2) + 22;
        d = 'M' + x1 + ',' + y1 + ' C' + rx + ',' + y1 + ' ' + rx + ',' + y2 + ' ' + x2 + ',' + y2;
      } else if (b.col > a.col) {
        var c = Math.max(36, (x2 - x1) / 2);
        d = 'M' + x1 + ',' + y1 + ' C' + (x1 + c) + ',' + y1 + ' ' + (x2 - c) + ',' + y2 + ' ' + x2 + ',' + y2;
      } else {  /* a cycle pointing back: loop under the boxes */
        var low = Math.max(a.y, b.y) + g.h + oy + 14;
        x1 = a.x + BW / 2 + ox; x2 = b.x + BW / 2 + ox;
        d = 'M' + x1 + ',' + (a.y + g.h + oy) + ' C' + x1 + ',' + low + ' ' + x2 + ',' + low + ' ' + x2 + ',' + (b.y + g.h + oy + 3);
      }
      return '<path class="s-line' + dim + '" data-a="' + esc(e[0]) + '" data-b="' + esc(e[1]) + '" marker-end="url(#' + mid + ')" d="' + d + '"/>';
    }).join('');
    var heads = '';
    if (opts.heads && L.cols > 1) {
      if (L.tb) heads = '<text class="s-col" x="' + ox + '" y="16">uses others, top · foundations, bottom</text>';
      else for (var ci = 0; ci < L.cols; ci++) {
        var label = ci === 0 ? 'uses others' : ci === L.cols - 1 ? 'foundations' : '';
        if (label) heads += '<text class="s-col" x="' + (ci * (BW + GX) + ox) + '" y="16">' + label + '</text>';
      }
    }
    var nodes = names.map(function (name) {
      var n = at[name], q = P[name], dim = lit && !lit.has(name) ? ' s-dim' : '', on = cur && cur.has(name);
      var sub = n.kind + (n.system ? ' · ' + n.system : '');
      var tip = name + ' (' + n.kind + ')' + (n.provides ? ': ' + n.provides : '');
      return '<g class="s-node kind-' + esc(n.kind) + dim + '" tabindex="0" role="link" aria-label="Open ' + esc(name) + ', ' + esc(n.kind) + '" data-go="' + n.id + '" data-n="' + esc(name) + '" transform="translate(' + (q.x + ox) + ',' + (q.y + oy) + ')">'
        + '<title>' + esc(tip) + '</title>'
        + '<rect class="' + (on ? 's-hi' : 's-box') + '" width="' + BW + '" height="' + g.h + '" rx="10"/>'
        + '<rect class="s-stripe" x="0" y="0" width="5" height="' + g.h + '" rx="2.5"/>'
        + glyph(n.kind, BW - 24, 12)
        + '<text class="s-t" x="16" y="27">' + esc(fitName(name, BW - 16 - 30)) + '</text><text class="s-sub" x="16" y="47">' + esc(fitName(sub, (BW - 16 - 30) * 1.15)) + '</text></g>';
    }).join('');
    var hidden = full.length - shown.length;
    var bar = opts.legend ? legend(names, hidden) : '';
    return '<figure class="viz">' + bar + '<div class="scroll" tabindex="0" role="region" aria-label="' + esc(opts.label || 'Component graph') + '"><svg viewBox="0 0 ' + L.W + ' ' + L.H + '" width="' + L.W + '" height="' + L.H + '" role="img">'
      + '<title>' + esc(opts.label || 'Component graph') + '</title><desc>' + (L.tb ? 'Levels run top to bottom: each box is a component, and an arrow points down' : 'Columns run left to right: each box is a component, and an arrow points right') + ' to what it depends on.</desc>'
      + '<defs><marker id="' + mid + '" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker></defs>'
      + heads + edges + nodes + '</svg></div><figcaption>' + (opts.caption || '') + '</figcaption></figure>';
  }
  var showAll = false;
  function legend(names, hidden) {
    var kinds = KINDS.filter(function (k) { return D.graph.nodes.some(function (n) { return n.kind === k && names.indexOf(n.name) >= 0; }); });
    var items = kinds.map(function (k) {
      return '<li class="kind-' + k + '"><svg viewBox="0 0 12 12" aria-hidden="true">' + glyph(k, 0, 0) + '</svg>' + k + '</li>';
    }).join('');
    var toggle = (hidden || showAll) ? '<label><input type="checkbox" id="showAll"' + (showAll ? ' checked' : '') + '>Show all dependencies'
      + (hidden ? ' (' + hidden + ' implied hidden)' : '') + '</label>' : '';
    return '<div class="vizbar">' + (kinds.length > 1 ? '<ul class="legend" role="list" aria-label="Component kinds">' + items + '</ul>' : '') + toggle + '</div>';
  }
  /* Hover or keyboard focus on a box lights its own arrows and neighbours and fades the rest. */
  function wireHover(root) {
    root.querySelectorAll('svg').forEach(function (svg) {
      function on(name) {
        svg.classList.add('hovering');
        svg.querySelectorAll('.s-line').forEach(function (l) {
          var hit = l.getAttribute('data-a') === name || l.getAttribute('data-b') === name;
          l.classList.toggle('hl', hit);
          if (hit) { svg.querySelector('[data-n="' + CSS.escape(l.getAttribute('data-a')) + '"]').classList.add('hl'); svg.querySelector('[data-n="' + CSS.escape(l.getAttribute('data-b')) + '"]').classList.add('hl'); }
        });
        var me = svg.querySelector('[data-n="' + CSS.escape(name) + '"]'); if (me) me.classList.add('hl');
      }
      function off() { svg.classList.remove('hovering'); svg.querySelectorAll('.hl').forEach(function (x) { x.classList.remove('hl'); }); }
      svg.querySelectorAll('.s-node').forEach(function (node) {
        var name = node.getAttribute('data-n');
        node.addEventListener('mouseenter', function () { on(name); }); node.addEventListener('mouseleave', off);
        node.addEventListener('focus', function () { on(name); }); node.addEventListener('blur', off);
      });
    });
  }
  function neighbours(name) {
    var s2 = new Set([name]);
    D.graph.edges.forEach(function (e) { if (e[0] === name) s2.add(e[1]); if (e[1] === name) s2.add(e[0]); });
    return s2;
  }

  function section(n, extra, sub, chip) {
    return '<details class="sec" id="' + n.id + '" data-search="' + esc((n.name + ' ' + n.aliases.join(' ') + ' ' + n.body).toLowerCase()) + '">'
      + '<summary><div><h3>' + inline(title(n)) + '</h3><span class="sub">' + esc(sub || '') + '</span></div><span class="side">' + (chip || '') + CHEV + '</span></summary>'
      + '<div class="body">' + props(n) + (extra || md(n.body))
      + '<label class="donebox"><input type="checkbox" data-done="' + n.id + '" aria-label="Mark ' + esc(n.name) + ' as read">Read</label></div></details>';
  }

  function flowBody(n) {
    var isStep = function (l) { return /^\s*\d+\. /.test(l); };
    var steps = n.body.split('\n').filter(isStep).map(function (l) { return l.replace(/^\s*\d+\. /, ''); });
    var rest = n.body.split('\n').filter(function (l) { return !isStep(l); }).join('\n');
    return md(rest) + '<div class="flow" data-steps="' + esc(JSON.stringify(steps)) + '" data-lit="' + esc(JSON.stringify(Array.from(linksIn(JSON.stringify(n.props) + n.body)))) + '">'
      + '<div class="stepbar"><button class="btn" type="button" data-step="-1">Previous</button><span class="pos"></span><button class="btn primary" type="button" data-step="1">Next</button></div>'
      + '<ol class="steps">' + steps.map(function (s, i) { return '<li data-i="' + i + '">' + (i + 1) + '. ' + inline(s) + '</li>'; }).join('') + '</ol><div class="fgraph"></div></div>';
  }
  function stepTo(box, i) {
    var steps = JSON.parse(box.getAttribute('data-steps')), lit = new Set(JSON.parse(box.getAttribute('data-lit')));
    if (!steps.length) return;
    i = Math.max(0, Math.min(steps.length - 1, i)); box.setAttribute('data-i', i);
    box.querySelectorAll('ol.steps li').forEach(function (li) { li.classList.toggle('on', +li.getAttribute('data-i') === i); });
    box.querySelector('.pos').textContent = 'Step ' + (i + 1) + ' of ' + steps.length;
    var only = new Set(Array.from(lit).filter(function (x) { return D.graph.nodes.some(function (n) { return n.name === x; }); }));
    box.querySelector('.fgraph').innerHTML = graph({ only: only, cur: linksIn(steps[i]), all: true, label: 'Flow graph',
      caption: 'The components this flow touches. Outlined: the ones step ' + (i + 1) + ' names. Arrow keys step too.' });
    wireHover(box.querySelector('.fgraph'));
  }

  /* ---------- build the page ---------- */
  var comps = of('component'), terms = of('term'), decisions = of('decision'), flows = of('flow'), questions = of('question');
  var arch = byName['architecture'], open = questions.filter(function (q) { return q.props.status !== 'answered'; });
  var h = [];
  document.title = D.repo + ' repo map';
  document.getElementById('brand').textContent = D.repo + ': repo map';
  h.push('<p class="eyebrow">Repo map · commit ' + esc(D.commit) + ' · ' + esc(D.date) + '</p>');
  h.push('<h1>How ' + esc(D.repo) + ' works</h1>');
  h.push('<p class="lede">What each part is, why it is that way, and how a request moves through it. Follow the path first; every section opens and closes, and the boxes in each graph open their notes.</p>');
  h.push('<dl class="facts">' + [['Components', comps.length], ['Flows', flows.length], ['Decisions', decisions.length], ['Terms', terms.length], ['Open questions', open.length]]
    .map(function (x) { return '<div><dt>' + x[0] + '</dt><dd>' + x[1] + '</dd></div>'; }).join('') + '</dl>');
  var kindCounts = KINDS.map(function (k) { return [k, comps.filter(function (n) { return n.props.kind === k; }).length]; }).filter(function (x) { return x[1]; });
  if (comps.length) h.push('<div class="kindsum"><p class="eyebrow">Components by kind</p><div class="kindbar" role="img" aria-label="' + esc(kindCounts.map(function (x) { return x[1] + ' ' + x[0]; }).join(', ')) + '">' + kindCounts.map(function (x) { return '<span class="kind-' + x[0] + '" style="flex:' + x[1] + '" title="' + x[1] + ' ' + x[0] + '"></span>'; }).join('') + '</div><ul class="legend" role="list">' + kindCounts.map(function (x) { return '<li class="kind-' + x[0] + '"><svg viewBox="0 0 12 12" aria-hidden="true">' + glyph(x[0], 0, 0) + '</svg>' + x[0] + ' <strong>' + x[1] + '</strong></li>'; }).join('') + '</ul></div>');
  var path = [];
  if (arch) path.push(['#' + arch.id, 'The architecture', 'the big picture: the parts, their boundaries, how to build and test']);
  if (comps.length) path.push(['#' + comps[0].id, 'The components', 'what each part does and why; start with ' + comps[0].name]);
  if (flows.length) path.push(['#' + flows[0].id, 'Walk a flow', 'step through "' + title(flows[0]) + '" and watch the graph']);
  if (decisions.length) path.push(['#' + decisions[0].id, 'The decisions', 'why the code has this shape, and the source for each']);
  if (terms.length) path.push(['#glossary', 'The glossary', 'the project\'s words, then review them as flashcards']);
  if (open.length) path.push(['#questions', 'Open questions', 'what the map could not prove, and who to ask']);
  h.push('<nav class="path" aria-labelledby="pathH"><h2 id="pathH">Guided path</h2><ol role="list">' + path.map(function (p) {
    return '<li><div><a href="' + p[0] + '"><strong>' + p[1] + '</strong></a><span class="why">' + esc(p[2]) + '</span></div></li>'; }).join('') + '</ol></nav>');
  var MAINCAP = 'A box uses the boxes its arrows point to. Hover a box to trace its links; click it to open its note.';
  h.push('<div id="maingraph"></div>');
  h.push('<label class="sr-only" for="filter">Filter notes</label><input class="filter" id="filter" type="search" placeholder="Filter notes by name, alias or text">');
  if (arch) { h.push('<p class="part">The how: architecture</p>'); h.push(section(arch, null, 'bird\'s-eye view, boundaries, build and test')); }
  if (comps.length) { h.push('<p class="part">The what: components</p>'); comps.forEach(function (n) { h.push(section(n, md(n.body) + '<h4>Neighbours</h4><div class="focus" data-focus="' + esc(n.name) + '"></div>', n.props.provides || '', '<span class="chip kind-' + esc(n.props.kind || '') + '">' + esc(n.props.kind || '') + '</span>')); }); }
  if (flows.length) { h.push('<p class="part">The how: flows</p>'); flows.forEach(function (n) { h.push(section(n, flowBody(n), 'from ' + (n.props.entry || ''), '<span class="chip">flow</span>')); }); }
  if (decisions.length) { h.push('<p class="part">The why: decisions</p>'); decisions.forEach(function (n) { h.push(section(n, null, 'source: ' + (n.props.source || 'UNKNOWN'), '<span class="chip">' + esc(n.props.status || '') + '</span>')); }); }
  if (terms.length) {
    h.push('<p class="part" id="glossary">The words: glossary</p><dl class="gloss">' + terms.map(function (n) {
      return '<dt id="' + n.id + '">' + esc(title(n)) + '</dt><dd>' + inline(firstLine(n) || '') + (n.aliases.length ? '<span class="aka">also: ' + esc(n.aliases.join(', ')) + '</span>' : '') + '</dd>'; }).join('') + '</dl>');
    h.push('<div class="quiz" id="quiz"><p class="eyebrow">Flashcards</p><p class="q" id="qq">Ready when you are.</p><p class="a hidden" id="qa"></p>'
      + '<div class="admin"><button class="btn primary" type="button" id="qnext">Next card</button><button class="btn" type="button" id="qshow" disabled>Show answer</button></div></div>');
  }
  if (questions.length) {
    h.push('<p class="part" id="questions">Open questions</p><ul class="gaps" role="list">' + questions.map(function (n) {
      return '<li id="' + n.id + '"><strong>' + inline(title(n)) + '</strong><div class="who">' + esc(n.props.status || '') + ' · ask: ' + esc(n.props.ask || '') + '</div>' + md(n.body) + '</li>'; }).join('') + '</ul>');
  }
  h.push('<footer><p>Generated by the repo-map skill from the notes in this map. Read marks and display settings stay in this browser.</p>'
    + '<div class="admin"><button class="btn" type="button" id="resetBtn">Clear read marks</button><span id="resetConfirm" hidden>Clear them? <button class="btn" type="button" id="resetYes">Yes, clear</button> <button class="btn" type="button" id="resetNo">Keep</button></span></div></footer>');
  document.getElementById('main').innerHTML = h.join('\n');
  var mainLit = null;
  function drawMain(lit) {
    mainLit = lit;
    var box = document.getElementById('maingraph');
    box.innerHTML = graph({ lit: lit, cur: lit, caption: MAINCAP, legend: true, heads: true, all: showAll });
    var t = document.getElementById('showAll');
    if (t) t.addEventListener('change', function () {
      showAll = t.checked; drawMain(mainLit);
      var again = document.getElementById('showAll'); if (again) again.focus();  /* the redraw replaced the box */
    });
    wireHover(box);
  }
  drawMain(null);
  /* The layout wraps to the column width, so redraw every graph when that width changes (phones, rotation). */
  var lastW = document.getElementById('main').clientWidth, rt = null;
  window.addEventListener('resize', function () {
    clearTimeout(rt);
    rt = setTimeout(function () {
      var w = document.getElementById('main').clientWidth;
      if (w === lastW) return;
      lastW = w; drawMain(mainLit);
      document.querySelectorAll('.focus').forEach(function (fc) { if (fc.innerHTML) { fc.innerHTML = ''; var d = fc.closest('details'); if (d.open) d.dispatchEvent(new Event('toggle')); } });
      document.querySelectorAll('.flow[data-i]').forEach(function (f) { stepTo(f, +f.getAttribute('data-i')); });
    }, 150);
  });

  /* ---------- display settings ---------- */
  var prefs = { theme: 'system', size: 'md' };
  try { var saved = JSON.parse(localStorage.getItem(PREFS) || 'null'); if (saved) { prefs.theme = saved.theme || 'system'; prefs.size = saved.size || 'md'; } } catch (e) {}
  function applyPrefs() {
    if (prefs.theme === 'system') { if (hostTheme) root.setAttribute('data-theme', hostTheme); else root.removeAttribute('data-theme'); }
    else root.setAttribute('data-theme', prefs.theme);
    if (prefs.size === 'md') root.removeAttribute('data-size'); else root.setAttribute('data-size', prefs.size);
    var t = document.getElementById('th-' + prefs.theme); if (t) t.checked = true;
    var s = document.getElementById('sz-' + prefs.size); if (s) s.checked = true;
  }
  document.querySelectorAll('input[name="theme"], input[name="size"]').forEach(function (r) {
    r.addEventListener('change', function () { prefs[r.name] = r.value; try { localStorage.setItem(PREFS, JSON.stringify(prefs)); } catch (e) {} applyPrefs(); });
  });
  applyPrefs();
  var display = document.getElementById('display');
  document.addEventListener('click', function (e) { if (display.open && !display.contains(e.target)) display.open = false; });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && display.open) { display.open = false; display.querySelector('summary').focus(); } });
  var bar = document.getElementById('topbar');
  function setHdr() { root.style.setProperty('--hdr', bar.offsetHeight + 'px'); }
  setHdr();
  if ('ResizeObserver' in window) new ResizeObserver(setHdr).observe(bar); else window.addEventListener('resize', setHdr);

  /* ---------- read marks ---------- */
  var state = {};
  try { state = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) { state = {}; }
  var boxes = document.querySelectorAll('input[data-done]');
  function renderRead() {
    var n = 0;
    boxes.forEach(function (b) { b.checked = !!state[b.getAttribute('data-done')]; if (b.checked) n++; });
    var p = document.getElementById('readProg'); p.max = boxes.length || 1; p.value = n;
    document.getElementById('readText').textContent = n + ' of ' + boxes.length + ' read';
  }
  boxes.forEach(function (b) { b.addEventListener('change', function () { state[b.getAttribute('data-done')] = b.checked; try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} renderRead(); }); });
  renderRead();
  var resetBtn = document.getElementById('resetBtn'), resetConfirm = document.getElementById('resetConfirm');
  resetBtn.addEventListener('click', function () { resetConfirm.hidden = false; resetBtn.hidden = true; document.getElementById('resetNo').focus(); });
  document.getElementById('resetNo').addEventListener('click', function () { resetConfirm.hidden = true; resetBtn.hidden = false; resetBtn.focus(); });
  document.getElementById('resetYes').addEventListener('click', function () {
    state = {}; try { localStorage.removeItem(KEY); } catch (e) {}
    renderRead(); resetConfirm.hidden = true; resetBtn.hidden = false; resetBtn.focus();
    document.getElementById('stat').textContent = 'Read marks cleared';
  });

  /* ---------- sections, links, graph clicks ---------- */
  var secs = Array.prototype.slice.call(document.querySelectorAll('details.sec'));
  var toggle = document.getElementById('toggleAll');
  function syncToggle() { toggle.textContent = secs.some(function (d) { return !d.open; }) ? 'Expand all' : 'Collapse all'; }
  toggle.addEventListener('click', function () {
    var openAll = toggle.textContent === 'Expand all';
    secs.forEach(function (d) { d.open = openAll; });
    syncToggle();
    if (!openAll) document.getElementById('main').scrollIntoView({ block: 'start' });
  });
  secs.forEach(function (d) {
    d.addEventListener('toggle', function () {
      syncToggle();
      var f = d.querySelector('.flow'); if (d.open && f && !f.hasAttribute('data-i')) stepTo(f, 0);
      var fc = d.querySelector('.focus');
      if (d.open && fc && !fc.innerHTML) { var nm = fc.getAttribute('data-focus');
        fc.innerHTML = graph({ only: neighbours(nm), cur: new Set([nm]), all: true, label: 'Neighbours of ' + nm, caption: 'This component (outlined), with what uses it and what it uses.' }); wireHover(fc); }
    });
  });
  function openTarget(id, focus) {
    var el = id && document.getElementById(id);
    if (!el) return;
    if (el.classList.contains('hidden')) {  /* the filter hid it: clear the filter so the target shows */
      var fi = document.getElementById('filter'); fi.value = ''; fi.dispatchEvent(new Event('input'));
    }
    if (el.tagName === 'DETAILS') el.open = true;
    requestAnimationFrame(function () { el.scrollIntoView({ block: 'start' }); });
    if (focus && el.tagName === 'DETAILS') el.querySelector('summary').focus({ preventScroll: true });
    try { history.replaceState(null, '', '#' + id); } catch (e) {}
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href^="#"]');
    if (a) { e.preventDefault(); openTarget(a.getAttribute('href').slice(1), true); return; }
    var node = e.target.closest('[data-go]');
    if (node) { openTarget(node.getAttribute('data-go'), true); return; }
    var stepBtn = e.target.closest('[data-step]');
    if (stepBtn) { var f = stepBtn.closest('.flow'); stepTo(f, +(f.getAttribute('data-i') || 0) + +stepBtn.getAttribute('data-step')); return; }
    var li = e.target.closest('ol.steps li');
    if (li) stepTo(li.closest('.flow'), +li.getAttribute('data-i'));
  });
  document.addEventListener('keydown', function (e) {
    var node = e.target.closest && e.target.closest('[data-go]');
    if (node && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); openTarget(node.getAttribute('data-go'), true); return; }
    var f = e.target.closest && e.target.closest('.flow');
    if (f && (e.key === 'ArrowRight' || e.key === 'ArrowLeft')) stepTo(f, +(f.getAttribute('data-i') || 0) + (e.key === 'ArrowRight' ? 1 : -1));
  });
  function hashId() {  /* location.hash keeps percent-encoding (n-%E6%B3%A8%E6%96%87 for n-注文): decode it, once */
    var h = location.hash.slice(1);
    try { return decodeURIComponent(h); } catch (e) { return h; }
  }
  window.addEventListener('hashchange', function () { openTarget(hashId()); });
  if (location.hash) openTarget(hashId());
  syncToggle();

  /* ---------- filter ---------- */
  document.getElementById('filter').addEventListener('input', function (e) {
    var q = e.target.value.trim().toLowerCase();
    secs.forEach(function (d) { var hit = !q || d.getAttribute('data-search').indexOf(q) >= 0; d.classList.toggle('hidden', !hit); if (q && hit) d.open = true; });
    var match = q ? new Set(comps.filter(function (n) { return (n.name + ' ' + n.body).toLowerCase().indexOf(q) >= 0; }).map(function (n) { return n.name; })) : null;
    drawMain(match);
    syncToggle();
  });

  /* ---------- flashcards ---------- */
  var deck = terms.map(function (n) { return { q: title(n), a: firstLine(n) }; }).filter(function (c) { return c.a; });
  var qn = document.getElementById('qnext'), qs = document.getElementById('qshow');
  if (qn) {
    var order = [], k = -1;
    qn.addEventListener('click', function () {
      if (k < 0 || k >= order.length - 1) { order = deck.map(function (_, i) { return i; }).sort(function () { return Math.random() - 0.5; }); k = -1; }
      k++; var c = deck[order[k]];
      document.getElementById('qq').textContent = c ? 'What does "' + c.q + '" mean here?' : 'No cards.';
      var a = document.getElementById('qa'); a.textContent = c ? c.a : ''; a.classList.add('hidden'); qs.disabled = !c;
    });
    qs.addEventListener('click', function () { document.getElementById('qa').classList.remove('hidden'); qs.disabled = true; });
  }
})();
</script></body></html>
"""


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("folder", type=pathlib.Path)
    ap.add_argument("--out", type=pathlib.Path)
    ap.add_argument("--fonts", action="store_true",
                    help="load three fonts from Google Fonts; never for a company or private repository")
    ap.add_argument("--offline", action="store_true", help="the default; kept so older instructions still work")
    args = ap.parse_args(argv)
    if not args.folder.is_dir():
        print(f"FAIL {args.folder} is not a folder")
        return 1
    notes = check_map.load_notes(args.folder)
    if "index.md" not in notes:
        print("FAIL no index.md: run the map first")
        return 1
    out = args.out or args.folder / "map.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(notes, fonts=args.fonts and not args.offline), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
