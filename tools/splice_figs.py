"""Splice redrawn figures from a draft file into the page.

Usage: python3 -I tools/splice_figs.py <page.html> <draft.html>
The draft holds blocks that start with marker lines such as "<!-- L3 SVG -->", "<!-- L3 CAPTION -->",
"<!-- L3 KEY -->" and "<!-- L12 PANEL EDITS -->" (lines of the form: old ⟶ new).
Each SVG replaces the first <svg> of the lesson's figure with the same viewBox width; captions and keys
replace that figure's <figcaption> and <ul class="fig-key"> contents.
"""
import re
import sys

LESSON = {"L3": "discovery", "L6": "orchestration", "L11": "running", "L12": "pipeline"}

page_path, draft_path = sys.argv[1], sys.argv[2]
s = open(page_path, encoding="utf-8").read()
draft = open(draft_path, encoding="utf-8").read()

blocks = {}
for m in re.finditer(r"^<!-- (L\d+) (SVG|CAPTION|KEY|PANEL EDITS) -->\n(.*?)(?=^<!-- L\d+ (?:SVG|CAPTION|KEY|PANEL EDITS) -->|\Z)", draft, re.S | re.M):
    blocks[(m.group(1), m.group(2))] = m.group(3).strip()


def figure_span(sid):
    a = s.index(f'<section id="{sid}"')
    f0 = s.index("<figure>", a)
    return f0, s.index("</figure>", f0) + len("</figure>")


done = []
for (lesson, kind), body in blocks.items():
    sid = LESSON[lesson]
    f0, f1 = figure_span(sid)
    fig = s[f0:f1]
    if kind == "SVG":
        new = body[body.index("<svg"):body.rindex("</svg>") + len("</svg>")]
        new = re.sub(r"\s*<!--.*?-->", "", new, flags=re.S)
        i, j = fig.index("<svg"), fig.index("</svg>") + len("</svg>")
        fig = fig[:i] + new + fig[j:]
    elif kind == "CAPTION":
        fig = re.sub(r"<figcaption>.*?</figcaption>", lambda _: f"<figcaption>{body}</figcaption>", fig, count=1, flags=re.S)
    elif kind == "KEY":
        fig = re.sub(r'<ul class="fig-key">.*?</ul>', lambda _: f'<ul class="fig-key">{body}</ul>', fig, count=1, flags=re.S)
    elif kind == "PANEL EDITS":
        a = s.index(f'<section id="{sid}"')
        b = s.index("</section>", a)
        sec = s[a:b]
        for line in body.splitlines():
            if "⟶" not in line:
                continue
            old, new = (x.strip() for x in line.split("⟶", 1))
            if sec.count(old) != 1:
                raise SystemExit(f"{lesson} panel edit: expected 1 of {old[:60]!r}, found {sec.count(old)}")
            sec = sec.replace(old, new)
        s = s[:a] + sec + s[b:]
        done.append(f"{lesson} {kind}")
        continue
    s = s[:f0] + fig + s[f1:]
    done.append(f"{lesson} {kind}")

open(page_path, "w", encoding="utf-8").write(s)
print("spliced:", ", ".join(done))
