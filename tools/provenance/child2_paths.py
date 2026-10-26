"""Child 2: reading paths, grouped rail, Lesson 2 collapse hook, author's-setup block as a closed details."""
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


# Rail: four groups in page order, numbers unchanged.
r0 = s.index('<nav class="rail" aria-label="Lessons">')
r1 = s.index("</nav>", r0) + len("</nav>")
items = re.findall(r'<li><a href="#([^"]+)">([^<]+)</a></li>', s[r0:r1])
names = dict(items)
groups = [
    ("Basics", ["loop", "rules", "discovery", "goals", "phases"]),
    ("Orchestrate", ["orchestration", "patterns", "toolbox", "selfcheck"]),
    ("Run it without you", ["guardrails", "running", "pipeline", "growing"]),
    ("Toolkit and evidence", ["prompts", "failures", "checklist", "evidence", "sources"]),
]
assert [i for _, g in groups for i in g] == [i for i, _ in items], "group order must match the rail"
rail = ['<nav class="rail" aria-label="Lessons">']
for label, ids in groups:
    rail.append(f'  <p class="rail-group" aria-hidden="true">{label}</p>')
    rail.append(f'  <ol aria-label="{label}">')
    rail += [f'    <li><a href="#{i}">{names[i]}</a></li>' for i in ids]
    rail.append("  </ol>")
rail.append("</nav>")
s = s[:r0] + "\n".join(rail) + s[r1:]

# Reading paths under the hero.
num = {i: n for n, (i, _) in enumerate(items, 1)}


def chips(ids):
    out = []
    for i in ids:
        label = f"{num[i]:02d} {names[i]}" if i != "sources" else names[i]
        out.append(f'<li><a href="#{i}">{label}</a></li>')
    return "".join(out)


paths = [
    ("new", "New to this", "The core ideas, in the order that builds them.", ["loop", "goals", "selfcheck", "orchestration", "phases", "failures", "checklist"], True),
    ("away", "Run it without watching", "Make it safe first, then pick how it runs while you're away.", ["guardrails", "running", "pipeline"], False),
    ("proof", "Check the evidence", "What has been measured, and where every claim comes from.", ["evidence", "sources"], False),
]
block = ['  <nav class="paths" id="paths" aria-label="Reading paths">',
         '    <p class="paths-label">Start here: pick a path</p>',
         '    <ul class="path-list">']
for pid, name, who, ids, main in paths:
    timed = " ".join(i for i in ids if i != "sources")
    block.append(f'      <li class="path{" main" if main else ""}">')
    block.append(f'        <p class="path-name">{name}</p>')
    block.append(f'        <p class="path-for">{who}</p>')
    block.append(f'        <ol data-path="{pid}">{chips(ids)}</ol>')
    block.append(f'        <p class="path-min" data-lessons="{timed}">about 0 min</p>')
    block.append("      </li>")
block.append("    </ul>")
block.append('    <p class="paths-all">Or read straight through: 17 lessons, <span class="path-min" data-lessons="all">about 0 min</span>. Each lesson is marked Core, Builder or Reference.</p>')
block.append("  </nav>")
rep("  </div>\n</header>", "  </div>\n" + "\n".join(block) + "\n</header>")

# Lesson 2: give the rule list an id so the script can collapse it after three cards.
rep('<p class="kicker">Lesson 2 · Ten rules</p>', '<p class="kicker">Lesson 2 · Ten rules</p>')
i2 = s.index('<section id="rules"')
j2 = s.index('<ol class="rules">', i2)
s = s[:j2] + '<ol class="rules" id="rules-list">' + s[j2 + len('<ol class="rules">'):]

# The author's own setup: closed by default and labelled as one example.
rep('''  <div class="yours">
    <p class="card-label">In your setup (your own harness; other setups differ)</p>
    <p style="margin:0">Your Claude setup already has a helper for most phases. Here is where each one fits:</p>''',
    '''  <details class="yours">
    <summary class="card-label">Example: one author's harness (other setups differ)</summary>
    <p style="margin:0">One person's Claude setup, shown as an example: it has a helper for most phases. Here is where each one fits:</p>''')
y0 = s.index('<details class="yours">')
y1 = s.index("    </dl>\n  </div>\n", y0) + len("    </dl>\n")
s = s[:y1] + "  </details>\n" + s[y1 + len("  </div>\n"):]
rep("<dd>Your Stop gate and pre-push chain rerun the checks;", "<dd>A Stop gate and a pre-push chain rerun the checks;")
rep("<dd>Your review tiers. T0:", "<dd>Review tiers. T0:")

open(path, "w", encoding="utf-8").write(s)
print("ok")
