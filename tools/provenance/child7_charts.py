"""Child 7: an honest evidence chart (all four benchmarks, best and worst setup, data table) and an
unmistakably illustrative context chart. Numbers come from issues/drafts/google-scaling-check.md."""
import re
import sys

path = sys.argv[1]
s = open(path, encoding="utf-8").read()


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"expected {count} of {old[:70]!r}, found {n}")
    s = s.replace(old, new)


TAG = ('<a class="ev r" href="https://arxiv.org/abs/2512.08296v1" target="_blank" rel="noopener" '
       'data-src="Google Research: Towards a science of scaling agent systems, version 1 (Dec 2025)" '
       'aria-label="R, research paper: Google Research, scaling agent systems, version 1 (opens in a new tab)">R</a>')

# ---------- Lesson 17: dot plot ----------
# (benchmark, task, one agent alone, best (setup, change, rounded?), worst (setup, change, rounded?))
ROWS = [
    ("Finance-Agent", "financial reasoning", 35, ("Centralized", 80.9, False), ("Independent", 57, True)),
    ("BrowseComp-Plus", "web navigation", 32, ("Decentralized", 9.2, False), ("Independent", -35, True)),
    ("Workbench", "workflows and tools", 63, ("Decentralized", 5.7, False), ("Independent", -11, True)),
    ("PlanCraft", "step-by-step planning", 57, ("Hybrid", -39, False), ("Independent", -70, False)),
]
X0, X1, ZERO = 340, 860, 600
K = (X1 - ZERO) / 100


def x(v):
    return round(ZERO + v * K, 1)


def pct(v, approx):
    sign = "+" if v > 0 else "−" if v < 0 else ""
    num = f"{abs(v):g}"
    return f"{'≈' if approx else ''}{sign}{num}%"


top, step = 34, 68
bottom = top + step * len(ROWS)
svg = [
    '<svg viewBox="0 0 880 360" style="max-width:880px" role="img" aria-label="Dot plot of selected results from Google Research\'s agent-scaling study, paper version 1. '
    'For each benchmark, the best and worst multi-agent setup compared with one agent alone on the same tasks: '
    'Finance-Agent, best centralized +80.9%, worst independent about +57%; BrowseComp-Plus web navigation, best decentralized +9.2%, worst independent about −35%; '
    'Workbench, best decentralized +5.7%, worst independent about −11%; PlanCraft step-by-step planning, best hybrid −39%, worst independent −70%.">',
    f'      <rect x="{X0}" y="{top}" width="{ZERO - X0}" height="{bottom - top}" fill="var(--fail)" fill-opacity=".06"/>',
    f'      <rect x="{ZERO}" y="{top}" width="{X1 - ZERO}" height="{bottom - top}" fill="var(--accent)" fill-opacity=".06"/>',
    '      <text x="16" y="22" class="d-small">BENCHMARK (TASK)</text>',
    '      <text x="270" y="22" text-anchor="middle" class="d-small">ONE AGENT</text>',
    f'      <text x="{(X0 + ZERO) // 2}" y="22" text-anchor="middle" class="d-small">WORSE THAN ONE AGENT</text>',
    f'      <text x="{(ZERO + X1) // 2}" y="22" text-anchor="middle" class="d-small">BETTER THAN ONE AGENT</text>',
]
for i, (bench, task, alone, best, worst) in enumerate(ROWS):
    y = top + step * i + step // 2
    if i:
        svg.append(f'      <line x1="16" y1="{top + step * i}" x2="{X1}" y2="{top + step * i}" class="d-grid"/>')
    svg.append(f'      <g data-benchmark="{bench}">')
    svg.append(f'        <text x="16" y="{y - 3}" class="d-title sm">{bench}</text>')
    svg.append(f'        <text x="16" y="{y + 15}" class="d-sub">{task}</text>')
    svg.append(f'        <text x="270" y="{y + 5}" text-anchor="middle" class="d-title sm">{alone}%</text>')
    bx, wx = x(best[1]), x(worst[1])
    svg.append(f'        <line x1="{min(bx, wx)}" y1="{y}" x2="{max(bx, wx)}" y2="{y}" class="d-range"/>')
    for (name, v, approx), cls, ly in ((worst, "worst", y + 25), (best, "best", y - 13)):
        hue = "help" if v > 0 else "hurt"
        svg.append(f'        <circle cx="{x(v)}" cy="{y}" r="6" class="d-pt {cls} {hue}"/>')
        svg.append(f'        <text x="{x(v)}" y="{ly}" text-anchor="middle" class="d-label">{name} {pct(v, approx)}</text>')
    svg.append("      </g>")
svg.append(f'      <line x1="{ZERO}" y1="{top - 4}" x2="{ZERO}" y2="{bottom + 4}" class="d-tick"/>')
for v in (-100, -50, 0, 50, 100):
    label = "0" if v == 0 else pct(v, False)
    svg.append(f'      <line x1="{x(v)}" y1="{bottom}" x2="{x(v)}" y2="{bottom + 6}" class="d-tick"/>')
    svg.append(f'      <text x="{x(v)}" y="{bottom + 22}" text-anchor="middle" class="d-small tick">{label}</text>')
svg.append(f'      <text x="{ZERO}" y="{bottom + 42}" text-anchor="middle" class="d-sub">change in tasks solved, versus one agent alone on the same tasks</text>')
svg.append("    </svg>")

rows_html = "".join(
    f"<tr><th scope=\"row\">{b}</th><td>{t}</td><td>{a}%</td><td>{bs[0]} {pct(bs[1], bs[2])}</td><td>{w[0]} {pct(w[1], w[2])}</td></tr>"
    for b, t, a, bs, w in ROWS)
figure = f'''<figure>
    <div class="scroll">
    {chr(10).join(svg)}
    </div>
    <ul class="fig-key"><li><i class="k-help"></i>Better than one agent</li><li><i class="k-hurt"></i>Worse than one agent</li><li><i class="k-best"></i>Best setup</li><li><i class="k-worst"></i>Worst setup</li></ul>
    <details class="table-view">
      <summary>Show the numbers</summary>
      <div class="tbl-wrap"><table><caption>Change in tasks solved versus one agent alone (paper version 1). ≈ marks values rounded from the paper's Figure 2.</caption><thead><tr><th scope="col">Benchmark</th><th scope="col">Task</th><th scope="col">One agent alone</th><th scope="col">Best setup</th><th scope="col">Worst setup</th></tr></thead><tbody>{rows_html}</tbody></table></div>
      <p class="note">More from the same paper: gains shrank, and often turned negative, once one agent alone already solved more than about 45% of tasks. The authors fit that line from their data; it is not a hard cutoff, and Workbench (63% alone) still gained. Independent agents multiplied errors 17.2 times compared with one agent, against 4.4 times with a central coordinator. Samples are small, 50 to 100 tasks per benchmark, and a later version of the paper (April 2026) adds two more benchmarks, for 260 setups in all.</p>
    </details>
    <figcaption><strong>Selected results, not an average: read the direction, not the size.</strong> Each row compares the best and worst multi-agent setups with one agent alone on the same tasks. The rows are different tasks, so a longer line does not mean a bigger effect. Google Research, paper version 1 (December 2025): 180 setups, 4 benchmarks, 3 model families. {TAG}</figcaption>
  </figure>'''

f0 = s.index('<figure>', s.index('<section id="evidence"'))
f1 = s.index('</figure>', f0) + len('</figure>')
if 'viewBox="0 0 720 230"' not in s[f0:f1]:
    raise SystemExit("evidence figure not found")
s = s[:f0] + figure + s[f1:]

# ---------- Lesson 17: at most two numbers per finding in view ----------
PAIR = re.compile(r'(.*?)(<a class="ev [psrd]"[^>]*>[PSRD]</a>)', re.S)


def restructure(num, visible, keep_first_tag, extra_lead=""):
    """Rebuild a finding's source line: `visible` replaces the text before the first tag; the other pairs move into a disclosure."""
    global s
    li0 = s.index(f'<li><span class="n">{num}</span>', s.index('<section id="evidence"'))
    p0 = s.index('<p class="src">', li0) + len('<p class="src">')
    p1 = s.index('</p></li>', p0)
    pairs = PAIR.findall(s[p0:p1])
    head = f"{visible} {pairs[0][1]}" if keep_first_tag else visible
    rest = "".join(f" {t.strip()} {tag}" for t, tag in pairs[1:])
    more = f'<details class="more-nums"><summary>More numbers</summary><p>{extra_lead}{rest.strip()}</p></details>'
    s = s[:p0] + head + more + s[p1:]


restructure("02", "Airbnb finished a test migration estimated at 1.5 engineer-years in about 6 weeks.", True,
            "Airbnb's run covered about 3,500 test files: 75% done in 4 hours and 97% in four days. ")
restructure("03", "Adding a verifier fixed 15.6% more multi-agent runs.", True, "That study covered 1,600+ traces. ")
restructure("04", "SWE-agent's purpose-built file tools added 10.7 points over a raw shell.", True)
restructure("05", "GPT-4o passed about 61% of tau-bench tasks once, but under 25% eight times in a row.", True)
restructure("06", "In METR's randomized trial, experienced developers were 19% slower with early-2025 AI tools while believing they were 20% faster.", True)

# Finding 03's self-correction result has no number, so it stays in view.
rep('<details class="more-nums"><summary>More numbers</summary><p>That study covered 1,600+ traces. Self-correction without outside feedback lowered reasoning accuracy. ',
    ' Self-correction without outside feedback lowered reasoning accuracy. ')
m = re.search(r'(Self-correction without outside feedback lowered reasoning accuracy\. <a class="ev r"[^>]*>R</a>) (Meta)', s)
if not m:
    raise SystemExit("finding 03 split failed")
s = s[:m.start()] + m.group(1) + '<details class="more-nums"><summary>More numbers</summary><p>That study covered 1,600+ traces. ' + m.group(2) + s[m.end():]

# ---------- Lesson 6: context chart ----------
rep('<svg id="ctx-chart" viewBox="0 0 780 290" style="max-width:780px" role="img" aria-label="Line chart, illustrative. Context used by one long session rises from 4 percent to 99 percent over ten steps. Context used by a lead with helpers rises from 4 percent to 30 percent."></svg>',
    '<svg id="ctx-chart" viewBox="0 0 780 290" style="max-width:780px" role="img" tabindex="0" aria-label="Illustrative line chart, not measured data. One long session fills its context window by step 8, is compacted at step 9 and loses early details. A lead with helpers stays under about a third full. Use the left and right arrow keys to step through it."></svg>')
rep('<table id="ctx-table"><thead>', '<table id="ctx-table"><caption>Illustrative values, not measurements</caption><thead>')
c0 = s.index("  /* ---------- context chart ---------- */")
c1 = s.index("  hit.addEventListener('pointerleave', hide);\n", c0) + len("  hit.addEventListener('pointerleave', hide);\n")
s = s[:c0] + open(sys.argv[2], encoding="utf-8").read() + s[c1:]

open(path, "w", encoding="utf-8").write(s)
print("ok")
