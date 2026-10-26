"""Writes each lesson's level and reading time into its kicker, and the totals into the reading paths.

Rerun after any content change: python3 -I tools/lesson_meta.py site/orchestrating-claude.html
Reading time is words / 200, rounded up, counting all visible text in the section.
"""
import math
import re
import sys

LEVELS = {
    "core": ("Core", ["loop", "goals", "phases", "orchestration", "selfcheck", "failures", "checklist"]),
    "builder": ("Builder", ["discovery", "patterns", "toolbox", "guardrails", "running", "pipeline", "growing"]),
    "reference": ("Reference", ["rules", "prompts", "evidence"]),
}

path = sys.argv[1]
s = open(path, encoding="utf-8").read()


def words(html):
    # Quiz questions live in a JSON script block; count them, then drop other scripts and styles.
    html = re.sub(r'<script type="application/json"[^>]*>(.*?)</script>', r" \1 ", html, flags=re.S)
    html = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S)
    html = re.sub(r"<[^>]+>", " ", html)
    html = re.sub(r"&[a-z#0-9]+;", " ", html)
    return len(re.findall(r"[A-Za-z0-9][\w'’.-]*", html))


def section(sid):
    start = s.index(f'<section id="{sid}"')
    return start, s.index("</section>", start)


minutes = {}
for key, (label, ids) in LEVELS.items():
    for sid in ids:
        start, end = section(sid)
        body = s[start:end]
        body_wo_meta = re.sub(r'<span class="lv[^"]*">.*?</span>', "", body)
        m = max(1, math.ceil(words(body_wo_meta) / 200))
        minutes[sid] = m
        chip = f'<span class="lv {key}">{label} · {m} min</span>'
        k0 = s.index('<p class="kicker">', start)
        k1 = s.index("</p>", k0)
        kicker = s[k0:k1]
        kicker = re.sub(r'\s*<span class="lv[^"]*">.*?</span>', "", kicker) + " " + chip
        s = s[:k0] + kicker + s[k1:]

total = sum(minutes.values())


def fill(match):
    ids = match.group(2).split()
    n = total if ids == ["all"] else sum(minutes[i] for i in ids if i in minutes)
    return f"{match.group(1)}about {n} min{match.group(3)}"


s, n = re.subn(r'(<[a-z]+ class="path-min" data-lessons="([^"]+)">)[^<]*(</[a-z]+>)', fill, s)
open(path, "w", encoding="utf-8").write(s)
print(f"{len(minutes)} lessons, {total} min in all, {n} path totals")
for sid, m in minutes.items():
    print(f"  {sid}: {m}")
