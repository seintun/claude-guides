"""Fixes from the final independent review (besides the quiz button, done by hand)."""
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


# Figures keep their drawn size at every width; the cue shows only where a figure scrolls.
rep(".scroll-cue{display:none;font-size:13px;color:var(--ink-2);margin:0 0 6px}",
    ".scroll-cue{font-size:13px;color:var(--ink-2);margin:0 0 6px}")
rep(".scroll > svg{min-width:640px}", ".scroll > svg{min-width:var(--vbw,640px)}")
rep("  .scroll > svg{min-width:var(--vbw,640px)}\n  .scroll-cue{display:block}\n", "")
rep("""      if(el.scrollWidth > el.clientWidth + 1){
        el.setAttribute('data-scroll-ok', '');""", """      var cue = el.previousElementSibling;
      var scrolls = el.scrollWidth > el.clientWidth + 1;
      if(cue && cue.classList.contains('scroll-cue')) cue.hidden = !scrolls;
      if(scrolls){
        el.setAttribute('data-scroll-ok', '');""")

# Two more long tables fold after five rows.
for sid, table_open, label in [("patterns", None, "Show all 7 methods"), ("growing", None, "Show all 6 measures")]:
    a, b = span(sid)
    if sid == "patterns":
        t0 = s.index("<h3>Named methods, compared</h3>", a)
    else:
        t0 = s.index("<h3>A scorecard to track per task</h3>", a)
    tb0 = s.index("<table>", t0)
    tid = "methods-table" if sid == "patterns" else "scorecard-table"
    s = s[:tb0] + f'<table id="{tid}" class="collapsible collapsed" data-more="{label}">' + s[tb0 + len("<table>"):]
    body0 = s.index("<tbody>", tb0) + len("<tbody>")
    body1 = s.index("</tbody>", body0)
    rows = re.findall(r"<tr>.*?</tr>", s[body0:body1], re.S)
    new_body = s[body0:body1]
    for r in rows[5:]:
        new_body = new_body.replace(r, r.replace("<tr>", '<tr class="more">', 1), 1)
    s = s[:body0] + new_body + s[body1:]

# Plain-word glosses where a term turns up before its definition on some reading paths.
rep("tools:'Subagents (Explore, scouts on a cheap model), web search, docs lookups, MCP connectors.',",
    "tools:'Subagents (Explore, scouts on a cheap model), web search, docs lookups, MCP connectors (plug-ins for outside tools).',")
rep("tools:'Edits and shell, a test-first (TDD) skill, worktrees for parallel builders, Workflows for big fan-outs.',",
    "tools:'Edits and shell, a test-first (TDD) skill, worktrees (separate copies of the code) for parallel builders, Workflows for big fan-outs.',")
rep('<div class="ex">A test in npm test, rerun by a Stop hook and by CI on every push.</div>',
    '<div class="ex">A test in npm test, rerun by a Stop hook (a script that runs when Claude tries to finish) and by CI on every push.</div>')

# Wording that contradicted other text.
rep("After 2 failures with the same cause, stop and report. Don't try a sixth time.",
    "After 2 failures with the same cause, stop and report. Don't try a third time.")
rep('boundary "only <code>src/reports/</code>, no new packages"', 'boundary "code changes only in <code>src/reports/</code>, no new packages"')
rep("The rows are different tasks, so a longer line does not mean a bigger effect, and with 50 to 100 tasks per benchmark, small gains may be noise.",
    "The rows are different tasks, so a longer line does not mean a bigger effect, and the samples are small, so small gains may be noise.")
rep('<p class="path-for">The core ideas, in the order that builds them.</p>',
    '<p class="path-for">The core ideas, in the order that builds them, plus a 10-minute exercise in Lesson 4.</p>')

# A malformed #hash must not stop the rest of the script.
rep("    var t = document.getElementById(decodeURIComponent(a.getAttribute('href').slice(1)));",
    "    var t = null;\n    try { t = document.getElementById(decodeURIComponent(a.getAttribute('href').slice(1))); } catch(err) {}")
rep("    var target = document.getElementById(decodeURIComponent(location.hash.slice(1)));",
    "    var target = null;\n    try { target = document.getElementById(decodeURIComponent(location.hash.slice(1))); } catch(err) {}")

open(path, "w", encoding="utf-8").write(s)
print("ok")
