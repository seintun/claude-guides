"""Review bugs, chart blockers, child 8 (L1, L5, L9), the rest of child 11, and child 12."""
import json
import re
import sys

path = sys.argv[1]
s = open(path, encoding="utf-8").read()


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"expected {count} of {old[:90]!r}, found {n}")
    s = s.replace(old, new)


def span(sid):
    a = s.index(f'<section id="{sid}"')
    return a, s.index("</section>", a)


def in_sec(sid, old, new):
    global s
    a, b = span(sid)
    part = s[a:b]
    if part.count(old) != 1:
        raise SystemExit(f"{sid}: expected 1 of {old[:70]!r}, found {part.count(old)}")
    s = s[:a] + part.replace(old, new) + s[b:]


def cut(sid, start, end_marker):
    """Remove and return the text from `start` up to and including `end_marker` inside a section."""
    global s
    a, b = span(sid)
    i = s.index(start, a)
    j = s.index(end_marker, i) + len(end_marker)
    if j > b:
        raise SystemExit(f"{sid}: block runs past the section")
    block = s[i:j]
    s = s[:i] + s[j:]
    return block


def insert_before(sid, marker, text):
    global s
    a, b = span(sid)
    i = s.index(marker, a)
    if i > b:
        raise SystemExit(f"{sid}: marker {marker[:40]!r} not in section")
    s = s[:i] + text + s[i:]


def insert_after(sid, marker, text):
    global s
    a, b = span(sid)
    i = s.index(marker, a) + len(marker)
    if i > b:
        raise SystemExit(f"{sid}: marker {marker[:40]!r} not in section")
    s = s[:i] + text + s[i:]


END = '  <p class="lesson-end">'

# ================= review bugs =================
rep('<li><a href="#sources">Sources</a></li>', '<li class="src-link"><a href="#sources">Sources</a></li>', count=2)

# ================= chart blockers and extras =================
rep("tip.innerHTML = '<b>Step '+i+' · illustrative</b>", "tip.innerHTML = '<b>Illustrative: step '+i+'</b>")
rep("""    tip.style.top = Math.max(tip.offsetHeight + 4, sc.y - wr.top - 6) + 'px';
  }""", """    tip.style.top = Math.max(tip.offsetHeight + 4, sc.y - wr.top - 6) + 'px';
    document.getElementById('sr-status').textContent = 'Illustrative, step ' + i + ': one long session ' + about(solo[i]) + ', lead with helpers ' + about(lead[i]);
  }""")
rep("""    readout(Math.max(0, Math.min(10, Math.round((p.x - CX0) / ((CX1-CX0)/10)))));
  }
  hit.addEventListener('pointermove', fromPointer);
  hit.addEventListener('pointerdown', fromPointer);
  hit.addEventListener('pointerleave', hide);
  var step = 0;
  chart.addEventListener('focus', function(){ readout(step); });""",
    """    step = Math.max(0, Math.min(10, Math.round((p.x - CX0) / ((CX1-CX0)/10))));
    readout(step);
  }
  var step = 0;
  hit.addEventListener('pointermove', fromPointer);
  hit.addEventListener('pointerdown', fromPointer);
  // A finger lifting fires pointerleave; only a mouse leaving should clear the readout.
  hit.addEventListener('pointerleave', function(e){ if(e.pointerType === 'mouse') hide(); });
  document.addEventListener('pointerdown', function(e){ if(!wrap.contains(e.target)) hide(); });
  chart.addEventListener('focus', function(){ if(chart.matches(':focus-visible')) readout(step); });""")
rep("""c += '<text x="16" y="18" class="d-sub">Context used (share of the window)</text>';
  c += '<text x="'+CX1+'" y="18" text-anchor="end" class="d-band-text">ILLUSTRATIVE · NOT MEASURED</text>';""",
    """c += '<text x="16" y="18" class="d-sub">Context used (% of window)</text>';
  c += '<text x="'+(CX0+10)+'" y="'+(sy(100)+20)+'" class="d-band-text halo">ILLUSTRATIVE · NOT MEASURED</text>';""")
rep('<table id="ctx-table"><caption>Illustrative values, not measurements</caption><thead><tr><th>Step</th><th>One long session</th><th>Lead + helpers</th></tr>',
    '<table id="ctx-table"><caption>Illustrative: values, not measurements</caption><thead><tr><th scope="col">Step</th><th scope="col">One long session</th><th scope="col">Lead + helpers</th></tr>')

# Lesson 17 dot plot, rebuilt with the review's wording fixes.
TAG = ('<a class="ev r" href="https://arxiv.org/abs/2512.08296v1" target="_blank" rel="noopener" '
       'data-src="Google Research: Towards a science of scaling agent systems, version 1 (Dec 2025)" '
       'aria-label="R, research paper: Google Research, scaling agent systems, version 1 (opens in a new tab)">R</a>')
ROWS = [
    ("Finance-Agent", "financial reasoning", 34.9, ("Centralized", 80.9, False), ("Independent", 57, True)),
    ("BrowseComp-Plus", "web navigation", 31.8, ("Decentralized", 9.2, False), ("Independent", -35, True)),
    ("Workbench", "workflows and tools", 62.9, ("Decentralized", 5.7, False), ("Independent", -11, True)),
    ("PlanCraft", "step-by-step planning", 56.8, ("Hybrid", -39, False), ("Independent", -70, False)),
]
X0, X1, ZERO = 340, 860, 600
K = (X1 - ZERO) / 100


def x(v):
    return round(ZERO + v * K, 1)


def pct(v, approx):
    sign = "+" if v > 0 else "−" if v < 0 else ""
    return f"{'≈' if approx else ''}{sign}{abs(v):g}%"


top, step = 34, 68
bottom = top + step * len(ROWS)
svg = [
    '<svg viewBox="0 0 880 360" style="--vbw:880px;max-width:880px" role="img" aria-label="Dot plot of selected results from Google Research\'s agent-scaling study, paper version 1. '
    'For each benchmark, the best and worst of four multi-agent designs, pooled over three model families, as relative change in tasks solved compared with one agent alone: '
    'Finance-Agent, best centralized +80.9%, worst independent about +57%; BrowseComp-Plus web navigation, best decentralized +9.2%, worst independent about −35%; '
    'Workbench, best decentralized +5.7%, worst independent about −11%; PlanCraft step-by-step planning, best hybrid −39%, worst independent −70%.">',
    f'      <rect x="{X0}" y="{top}" width="{ZERO - X0}" height="{bottom - top}" fill="var(--fail)" fill-opacity=".06"/>',
    f'      <rect x="{ZERO}" y="{top}" width="{X1 - ZERO}" height="{bottom - top}" fill="var(--accent)" fill-opacity=".06"/>',
    '      <text x="16" y="22" class="d-small">BENCHMARK (TASK)</text>',
    '      <text x="270" y="22" text-anchor="middle" class="d-small">ONE AGENT ALONE</text>',
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
    svg.append(f'        <text x="270" y="{y + 5}" text-anchor="middle" class="d-title sm">{alone:.1f}%</text>')
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
svg.append(f'      <text x="{ZERO}" y="{bottom + 42}" text-anchor="middle" class="d-sub">relative change in tasks solved; 0 = same as one agent alone</text>')
svg.append("    </svg>")
rows_html = "".join(
    f'<tr><th scope="row">{b}</th><td>{t}</td><td>{a:.1f}%</td><td>{bs[0]} {pct(bs[1], bs[2])}</td><td>{w[0]} {pct(w[1], w[2])}</td></tr>'
    for b, t, a, bs, w in ROWS)
figure = f'''<figure>
    <p class="scroll-cue" aria-hidden="true">Swipe sideways to see the whole figure →</p>
    <div class="scroll">
    {chr(10).join(svg)}
    </div>
    <ul class="fig-key"><li><i class="k-help"></i>Better than one agent</li><li><i class="k-hurt"></i>Worse than one agent</li><li><i class="k-best"></i>Best design</li><li><i class="k-worst"></i>Worst design</li><li><i class="k-line"></i>Spread from worst to best</li></ul>
    <details class="table-view">
      <summary>Show the numbers</summary>
      <div class="tbl-wrap"><table><caption>Different tasks, not comparable in size. Relative change in tasks solved versus one agent alone, paper version 1; ≈ marks values rounded from the paper's Figure 2.</caption><thead><tr><th scope="col">Benchmark</th><th scope="col">Task</th><th scope="col">One agent alone</th><th scope="col">Best design</th><th scope="col">Worst design</th></tr></thead><tbody>{rows_html}</tbody></table></div>
      <p class="note">More from the same paper: gains shrank, and often turned negative, once one agent alone already solved more than about 45% of tasks. The authors fit that line from their data; it is not a hard cutoff, and Workbench's best design still gained though one agent alone solved 62.9%. Independent agents multiplied errors 17.2 times compared with one agent, against 4.4 times with a central coordinator. Samples are small: the paper lists 50 to 100 tasks for three of the four benchmarks. A later version of the paper (April 2026) adds two more benchmarks, for 260 setups in all. {TAG}</p>
    </details>
    <figcaption><strong>Selected results, not an average: read the direction, not the size.</strong> Each row compares the best and worst of four multi-agent designs, pooled over 3 model families, with one agent alone on the same tasks. The rows are different tasks, so a longer line does not mean a bigger effect, and with 50 to 100 tasks per benchmark, small gains may be noise. Google Research, paper version 1 (December 2025): 180 setups, 4 benchmarks. {TAG}</figcaption>
  </figure>'''
a, b = span("evidence")
f0 = s.index("<figure>", a)
f1 = s.index("</figure>", f0) + len("</figure>")
s = s[:f0] + figure + s[f1:]

in_sec("evidence", "GPT-4o passed about 61% of tau-bench tasks once, but under 25% eight times in a row.",
       "GPT-4o passed about 61% of tau-bench tasks on one try, but under 25% when every one of several tries had to pass.")
a, b = span("evidence")
li5 = s.index('<li><span class="n">05</span>', a)
m5 = s.index('<details class="more-nums"><summary>More numbers</summary><p>', li5) + len('<details class="more-nums"><summary>More numbers</summary><p>')
s = s[:m5] + "Several tries here means eight in a row. " + s[m5:]

# ================= child 8: Lesson 1, Lesson 5, Lesson 9 =================
in_sec("loop", '<rect x="430" y="204" width="140" height="58" rx="8" class="d-box"/>', '<rect x="430" y="204" width="140" height="58" rx="8" class="d-box check"/>')
in_sec("loop", '<text x="500" y="247" text-anchor="middle" class="d-sub">against the criteria</text>',
       '<text x="500" y="247" text-anchor="middle" class="d-sub">against the criteria</text>\n      <text x="500" y="284" text-anchor="middle" class="d-small">must be real: a test, a command, an observation</text>')

rep("""  function back(from, to, depth, label, next){
    var x1 = cx(from), x2 = cx(to);""", """  function back(from, to, depth, label, next, shift){
    var x1 = cx(from), x2 = cx(to) + (shift || 0);""")
rep("s += back(6,5,34,'fails');", "s += back(6,5,34,'fails');\n  s += back(7,5,66,'review findings', false, -18);")
in_sec("phases", "Loops back: Synthesize to Explore for gaps, Critique to Plan for objections, Verify to Build for failures, Learn to Frame for the next run.",
       "Loops back: Synthesize to Explore for gaps, Critique to Plan for objections, Verify to Build for failures, Review to Build for review findings, Learn to Frame for the next run.")

for n in range(1, 7):
    rep(f'<span class="meter" aria-label="Trust {n} of 6">', f'<span class="meter" role="img" aria-label="Trust {n} of 6">')
in_sec("selfcheck", '<span class="who">2 · Claude shows the command and output</span>',
       '<span class="who">2 · Claude shows the command and output <span class="risk">enough for a typo fix</span></span>')
in_sec("selfcheck", '<span class="who">5 · An adversary tries to break it</span>',
       '<span class="who">5 · An adversary tries to break it <span class="risk">login, payments, data</span></span>')
in_sec("selfcheck", "<span class=\"who\">6 · You sign off</span>",
       "<span class=\"who\">6 · You sign off <span class=\"risk\">login, payments, data</span></span>")

# ================= child 11: Lesson 7 groups and the short shape table =================
a, b = span("patterns")
t0 = s.index('<div class="tbl-wrap">', a)
t1 = s.index("</div>", t0) + len("</div>")
table = s[t0:t1]
rows = re.findall(r"<tr><td class=\"job\">(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>", table, re.S)
if len(rows) != 11:
    raise SystemExit(f"patterns: {len(rows)} rows")
by = {r[0]: r for r in rows}
DEFAULT = ["Plan, critique, build", "Goal loop", "Lead + workers"]
order = DEFAULT + [r[0] for r in rows if r[0] not in DEFAULT]


def prow(name, cls):
    _, how, when, watch, src = by[name]
    tag = re.search(r'<a class="ev [psrd]"[^>]*>[PSRD]</a>', src).group(0)
    badge = ' <span class="badge">Default</span>' if name == "Plan, critique, build" else ""
    return f'        <tr{cls}><td class="job">{name} {tag}{badge}</td><td>{how}</td><td>{when}</td><td>{watch}</td></tr>'


body = ['        <tr class="group"><th colspan="4" scope="colgroup">Default: start with these</th></tr>']
body += [prow(n, ' class="default"' if n == "Plan, critique, build" else "") for n in DEFAULT]
body.append('        <tr class="group more"><th colspan="4" scope="colgroup">Specialist: use when the task fits</th></tr>')
body += [prow(n, ' class="more"') for n in order[3:]]
new_table = ('<div class="tbl-wrap">\n    <table id="patterns-table" class="collapsible collapsed" data-more="Show all 11 patterns">\n'
             '      <thead><tr><th>Pattern</th><th>How it works</th><th>Use it when</th><th>Watch out for</th></tr></thead>\n'
             '      <tbody>\n' + "\n".join(body) + '\n      </tbody>\n    </table>\n  </div>')
s = s[:t0] + new_table + s[t1:]
in_sec("patterns", 'The "watch out for" column is our advice; the last column names where each pattern comes from.',
       'The "watch out for" column is our advice; the tag beside each name shows where the pattern comes from.')

a, b = span("evidence")
shape_start = s.index("<h3>Pick the shape by the task</h3>", a)
shape_table = s[s.index("<tbody>", shape_start) + 7:s.index("</tbody>", shape_start)]
shape_rows = re.findall(r"<tr>.*?</tr>", shape_table, re.S)
keys = ["Steps with shared state", "Many independent, read-heavy parts", "A large mechanical change", "A judgment call with no test"]
picked = []
for k in keys:
    row = next(r for r in shape_rows if k in r)
    if k.startswith("Steps"):
        row = row.replace("<tr>", '<tr class="default">', 1)
    picked.append("        " + row)
short = ('\n  <h3>Pick the shape by the task</h3>\n  <div class="tbl-wrap">\n    <table>\n'
         '      <thead><tr><th>Task shape</th><th>Shape that held up</th><th>Evidence</th></tr></thead>\n      <tbody>\n'
         + "\n".join(picked) + '\n      </tbody>\n    </table>\n  </div>\n'
         '  <p class="note">The full table, with one more shape and its sources: <a href="#evidence">Lesson 17</a>.</p>\n')
insert_before("patterns", "  <h3>Named methods, compared</h3>", short.lstrip("\n") + "\n")

# ================= child 11: Lesson 8, five features first =================
a, b = span("toolbox")
t0 = s.index("<tbody>", a) + len("<tbody>")
t1 = s.index("</tbody>", t0)
trs = re.findall(r"<tr><td class=\"job\">.*?</tr>", s[t0:t1], re.S)
if len(trs) != 16:
    raise SystemExit(f"toolbox: {len(trs)} rows")
first_jobs = ["Standing rules", "Think first", "Repeat a recipe", "Side jobs", "Checks it can't skip"]
first = [next(r for r in trs if f'<td class="job">{j}</td>' in r) for j in first_jobs]
rest = [r for r in trs if r not in first]
tb = ['        <tr class="group"><th colspan="4" scope="colgroup">Start with these five</th></tr>']
tb += ["        " + r for r in first]
tb.append('        <tr class="group more"><th colspan="4" scope="colgroup">Reach for these when a job needs them</th></tr>')
tb += ["        " + r.replace("<tr>", '<tr class="more">', 1) for r in rest]
s = s[:t0] + "\n" + "\n".join(tb) + "\n      " + s[t1:]
in_sec("toolbox", '<div class="tbl-wrap">\n    <table>', '<div class="tbl-wrap">\n    <table id="toolbox-table" class="collapsible collapsed" data-more="Show all 16 features">')

# ================= child 11: Lesson 15 cause chips =================
CAUSE = ["goal", "check", "context", "goal", "check", "goal", "permissions", "permissions", "permissions", "goal", "check", "permissions", "permissions", "check"]
a, b = span("failures")
t0 = s.index("<tbody>", a) + len("<tbody>")
t1 = s.index("</tbody>", t0)
frs = re.findall(r"<tr><td class=\"job\">.*?</tr>", s[t0:t1], re.S)
if len(frs) != 14:
    raise SystemExit(f"failures: {len(frs)} rows")
out = []
for i, (r, c) in enumerate(zip(frs, CAUSE)):
    cls = ' class="more"' if i >= 5 else ""
    out.append(f'        <tr{cls}><td><span class="cause">{c}</span></td>' + r[len("<tr>"):])
s = s[:t0] + "\n" + "\n".join(out) + "\n      " + s[t1:]
in_sec("failures", "<thead><tr><th>What you see</th>", "<thead><tr><th>Cause</th><th>What you see</th>")
in_sec("failures", '<div class="tbl-wrap">\n    <table>', '<div class="tbl-wrap">\n    <table id="failures-table" class="collapsible collapsed" data-more="Show all 14 failures">')
in_sec("failures", "traces back to a missing goal, a missing check, or too much in one context.",
       "traces back to a missing goal, a missing check, too much in one context, or too much permission.")

# ================= child 11: Reference disclosures (Lessons 3, 10, 12) =================
stage = cut("discovery", '  <div class="tbl-wrap">', "</div>\n")
note = cut("discovery", '  <p class="note"><span class="ev d"', "</p>\n")
insert_before("discovery", "  <h3>Should you grill like Matt Pocock? Yes, with rules</h3>",
              '  <details class="reference">\n    <summary>Reference: what each stage produces (7 stages)</summary>\n' + stage + note + "  </details>\n\n")
spec = cut("discovery", "  <h3>How much spec before code?</h3>", "keep the tests as the real contract.</p>\n")
spec = spec.replace("  <h3>How much spec before code?</h3>\n", "")
spec = re.sub(r"<h4>(.*?)</h4>", r'<p class="card-title">\1</p>', spec)
insert_before("discovery", END, '  <details class="reference">\n    <summary>Reference: how much spec before code</summary>\n' + spec + "  </details>\n")

facts = cut("guardrails", "  <h3>Facts to design around</h3>", "</ul>\n")
layers = cut("guardrails", '  <div class="layers">', "  </div>\n  </div>\n")
mistakes = cut("guardrails", "  <h3>Top mistakes</h3>", "</ul>\n")
facts = facts.replace("  <h3>Facts to design around</h3>\n", "")
mistakes = mistakes.replace("  <h3>Top mistakes</h3>\n", "")
ref10 = ('  <details class="reference">\n    <summary>Reference: 6 facts to design around</summary>\n' + facts + "  </details>\n"
         '  <details class="reference">\n    <summary>Reference: 17 controls to prevent, detect and recover</summary>\n' + layers + "  </details>\n"
         '  <details class="reference">\n    <summary>Reference: 7 top mistakes</summary>\n' + mistakes + "  </details>\n")
insert_before("guardrails", END, ref10)

gate = cut("pipeline", '    <div class="panel">\n      <h3>The gate at each step</h3>', "</ul>\n    </div>\n")
gate = gate.replace('    <div class="panel">\n      <h3>The gate at each step</h3>\n', "").replace("\n    </div>\n", "\n")
in_sec("pipeline", '  <div class="two-col">\n    <div class="panel">\n      <h3>Who moves each status</h3>', '  <div class="panel">\n      <h3>Who moves each status</h3>')
a, b = span("pipeline")
p0 = s.index('<h3>Who moves each status</h3>', a)
p1 = s.index("</ul>\n    </div>\n  </div>\n", p0)
s = s[:p1] + "</ul>\n  </div>\n" + s[p1 + len("</ul>\n    </div>\n  </div>\n"):]
know = cut("pipeline", "  <h3>Things worth knowing</h3>", "</ul>\n")
know = know.replace("  <h3>Things worth knowing</h3>\n", "")
insert_before("pipeline", '  <div class="rule-box">',
              '  <details class="reference">\n    <summary>Reference: the gate at each step (6)</summary>\n' + gate + "  </details>\n"
              '  <details class="reference">\n    <summary>Reference: 7 things worth knowing about GitHub and Linear</summary>\n' + know + "  </details>\n\n")

# ================= child 12: running example, recall items, quiz, try now =================
EX = {
    "loop": 'Take the goal "Users can export the reports table to CSV." Claude plans a small step and makes the change. Check then runs <code>npm test</code>: a fail sends it back to adjust, and only a pass lets it call the work done, with proof.',
    "discovery": 'The pain: people want the reports table in a spreadsheet. Slice turns it into one issue: outcome "Users can export the reports table to CSV", boundary "only <code>src/reports/</code>, no new packages", and no dependencies. Its check has three lines: the export has exactly the rows on screen, <code>npm test</code> passes with a new test for an empty report, and the file opens in Excel with the same columns as the table.',
    "phases": 'For the CSV export, Explore returns a few short reports with file paths: where the reports table gets its rows and its columns. Plan is a plan file in <code>docs/</code> with ordered slices, the test for each, and how to undo each one. Verify ends in a receipt: PASS, FAIL or NOT RUN, with the command, for each of the three Done when lines.',
    "orchestration": 'The CSV goal allows up to 3 helpers, so the lead sends a scout to read how the table builds its rows and columns, a builder to make the export in its own worktree, and a verifier to re-run the checks. Before and after, with made-up numbers (illustrative, not measured): one session reading everything itself opens about 40 files and its window fills with raw reading; with the scout, the lead receives 3 short summaries. The lead keeps the plan and the final say on "done".',
    "pipeline": 'The CSV issue from <a href="#discovery">Lesson 3</a> goes into Triage, and you delegate it. The agent opens a branch and a draft PR, and the required checks run <code>npm test</code>, including the empty-report test. Your team\'s GitHub automation moves the issue to In Review; after you approve, merging the PR that says "Fixes ID" moves it to Done.',
    "growing": 'The CSV row in the log shows one rework loop: Verify sent the work back to Build once, because the first file held a row the filter had hidden. The retro picks one change: turn the check "3 rows filtered to 2" into a test in <code>npm test</code>, so the gate catches it on the next run.',
    "failures": 'The CSV builder said "Done!", but the file had 3 rows when the screen showed 2: it included the row the filter had hidden. That is the "Done!" but broken row: the builder graded its own work, so nobody ran the check. The fix was a fresh verifier running "Given 3 rows filtered to 2…" and recording FAIL; the work went back to Build, and the receipt now shows PASS with the command.',
}


def ex(sid):
    lead = "Running example</b> (it comes back in later lessons)." if sid == "loop" else "Running example.</b>"
    return f'  <p class="note running-ex"><b>{lead} {EX[sid]}</p>\n'


def recall(q, a):
    return f'  <details class="recall"><summary>{q}</summary><p>{a}</p></details>\n'


insert_before("loop", "  <p>Three roles keep this loop healthy", ex("loop"))
insert_before("loop", END, recall("What happens if Check is missing?", "Claude stops when it feels finished, which is not the same as done. Why: the loop ends well only when Check is real, such as a test, a command or an observation."))
insert_before("discovery", "  <h3>Should you grill like Matt Pocock? Yes, with rules</h3>", ex("discovery") + "\n")
insert_before("goals", "  <h3>Build your goal prompt</h3>", recall('In the CSV goal, "up to 3 helper agents" belongs under which of the five parts, and "No new packages" under which?', "Budget, then Constraints. Why: Budget is how much effort to spend; Constraints is what is off limits, such as files and packages.") + "\n")
TRY = ('  <h3>Try now (10 min)</h3>\n  <ol class="try">\n'
       '    <li>Pick a small task of your own that you can check in a minute or two.</li>\n'
       '    <li>Write a goal with the five parts: Outcome, Done when (2 to 5 checks), Constraints, Stop and ask if, Budget. The builder above can help.</li>\n'
       '    <li>Paste it into Claude and add: "At the end, give me a <a class="term" id="fu-receipt" href="#gl-receipt">receipt</a>: each Done when line marked PASS, FAIL or NOT RUN, with the command behind it."</li>\n'
       '    <li>Let Claude work. If it reaches a Stop and ask if line, answer it.</li>\n'
       '    <li>Read the receipt. You are done when every line shows PASS with its command; FAIL or NOT RUN means it is not done, so paste the receipt back and name the line to fix.</li>\n'
       '  </ol>\n')
insert_before("goals", END, TRY)
rep('ends by giving you a <a class="term" id="fu-receipt" href="#gl-receipt">receipt</a>:', "ends by giving you a receipt:")
rep('<a class="g-where" href="#fu-receipt">Lesson 6</a>', '<a class="g-where" href="#fu-receipt">Lesson 4</a>')
insert_before("phases", END, ex("phases") + recall("Which of the ten phases comes before anything is built and has a fresh reviewer argue against the plan?", "Critique. Why: a reviewer that never saw Claude's reasoning argues against the plan before building starts."))
insert_before("orchestration", '  <div class="rule-box">', ex("orchestration") + "\n")
insert_before("orchestration", "  <p><b>Brief a helper like a capable colleague", recall("Sort these 6 jobs into lead or helper: (a) read many files and report only the conclusion; (b) change one line in a file you already have open; (c) fix a failing test from the exact error text you just saw; (d) review a finished change you did not write; (e) list every place a name appears; (f) two jobs that would both edit the same file.", "Helper: a, d, e. Lead: b, c, f. Why: a is wide reading where only the conclusion matters, d needs a judge who didn't do the work, e is a cheap list job; b would take longer to brief than to do, c needs every detail, f would have two helpers editing the same file.") + "\n")
insert_before("selfcheck", "  <p>For anything that runs unattended, measure how often <b>every</b> run succeeds", recall("75% per run: what's the chance 3 runs in a row all pass?", "About 42% (0.75 × 0.75 × 0.75 ≈ 0.42). Why: for unattended work, what counts is how often every run succeeds, not whether one did."))
a, b = span("pipeline")
fig_end = s.index("</figure>", a) + len("</figure>\n")
s = s[:fig_end] + "\n" + ex("pipeline") + s[fig_end:]
insert_before("growing", END, ex("growing"))
insert_before("failures", '  <div class="tbl-wrap">', recall("Claude keeps retrying the CSV export test and has failed with the same error five times. What is the likely cause?", 'No retry cap. Why: the fix is a rule to stop after 2 failures with the same cause and ask a fresh agent for a second opinion, like the "same test fails twice" line in the Lesson 4 goal.') + "\n")
insert_before("failures", END, ex("failures"))

QUIZ = [
    {"q": "Claude changes the CSV export, runs the tests, and they fail. In the loop, what happens next?", "options": ["It stops and reports that it tried", "It adjusts, fixing the cause, and plans again", "It skips the check and ships anyway", "It asks you to write a new goal"], "answer": 1, "why": "Lesson 1: a failed check sends Claude to Adjust and then back to Plan, and only a pass ends the loop, with proof."},
    {"q": "Which line is a good \"Done when\" for the CSV export?", "options": ["The export works well and feels fast.", "Claude is confident the export is finished.", "npm test passes, with a new test for an empty report.", "The code follows good practice."], "answer": 2, "why": "Lesson 4: Done when is 2 to 5 checks that a command or a person can run; a goal without a test is a wish."},
    {"q": "You ask a helper to review your change. What should its brief hand over?", "options": ["The code and the criteria", "The code and your conclusion that it is fine", "The criteria only, without the code", "Only the words \"please review\""], "answer": 0, "why": "Lesson 6: hand over the code and the criteria. A reviewer that reads your conclusion tends to agree with it."},
    {"q": "In the chain from criterion to scenario to gate, which line is the gate?", "options": ["Export downloads exactly the rows on screen.", "Given 3 rows filtered to 2, when I click Export, then the CSV has a header and 2 rows.", "A test in npm test, rerun by a Stop hook and by CI on every push.", "Claude reports that the export works."], "answer": 2, "why": "Lesson 9: the gate is something that runs every time, whether or not anyone remembers."},
    {"q": "Claude says \"Done!\" but the feature is broken. What is the likely cause?", "options": ["The builder graded its own work.", "The lead's context filled up with raw reading.", "The goal had no budget.", "Two writers edited the same files."], "answer": 0, "why": "Lesson 15: \"Done!\" but broken comes from the builder grading its own work; the fix is command output plus a hook or a fresh verifier."},
]
quiz = ('  <h3>Check what stuck</h3>\n  <p>Five questions on the core lessons. Your answers stay on this page and reset when you reload.</p>\n'
        '  <div class="quiz" id="quiz"></div>\n  <p class="progress" id="quiz-score" aria-live="polite"></p>\n'
        '  <script type="application/json" id="quiz-data">' + json.dumps(QUIZ, ensure_ascii=False) + '</script>\n')
insert_before("checklist", END, quiz)

open(path, "w", encoding="utf-8").write(s)
print("ok")
