"""Children 10, 4, 9 and the takeaways and callouts from child 11, in one pass for the launch."""
import re
import sys

path = sys.argv[1]
s = open(path, encoding="utf-8").read()


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"expected {count} of {old[:80]!r}, found {n}")
    s = s.replace(old, new)


def in_section(sid, old, new):
    global s
    a = s.index(f'<section id="{sid}"')
    b = s.index("</section>", a)
    part = s[a:b]
    if part.count(old) != 1:
        raise SystemExit(f"{sid}: expected 1 of {old[:60]!r}, found {part.count(old)}")
    s = s[:a] + part.replace(old, new) + s[b:]


# ---------- child 10: card titles under an h3 subhead become h4 ----------
for sid, title in [("discovery", "Small fix"), ("discovery", "Normal feature"), ("discovery", "Large or risky"),
                   ("orchestration", "Send a helper when"), ("orchestration", "Do it in the lead when"),
                   ("running", "Terminal"), ("running", "Cloud"), ("running", "Phone"),
                   ("evidence", "One writer by default"), ("evidence", "Wrap the model in a scripted pipeline"),
                   ("evidence", "External checks beat self-critique"), ("evidence", "Design the tools, keep the shape simple"),
                   ("evidence", "Measure reliability and cost"), ("evidence", "Human review is the bottleneck")]:
    in_section(sid, f"<h3>{title}</h3>", f"<h4>{title}</h4>")
in_section("evidence", "<h3>What this means for your harness ", "<h4>What this means for your harness ")
a = s.index("<h4>What this means for your harness ")
b = s.index("</h3>", a)
s = s[:b] + "</h4>" + s[b + 5:]

# Lesson 2: the tags can be focused or tapped, not only hovered.
rep("Hover over a tag to see its source, and click P, S or R to open that source in a new tab.",
    "Hover over, focus or tap a tag to see its source; clicking P, S or R opens that source in a new tab.")

# A key to the tags in the rail (and so in the phone menu, which copies the rail).
rep('</nav>\n\n<main id="main"',
    '  <p class="rail-key" aria-label="Evidence tags: P, their own words or official docs; S, second-hand; R, research; D, our advice">'
    '<span class="ev p" aria-hidden="true">P</span> own words or docs <span class="ev s" aria-hidden="true">S</span> second-hand '
    '<span class="ev r" aria-hidden="true">R</span> research <span class="ev d" aria-hidden="true">D</span> our advice</p>\n'
    '</nav>\n\n<main id="main"')

# Sources: each entry's title already links to the source, so its tag leaves the tab order.
src0 = s.index('<div class="src-grid">')
src1 = s.index("</section>", src0)
part = re.sub(r'(<a class="ev [psrd]") (href=)', r'\1 tabindex="-1" aria-hidden="true" \2', s[src0:src1])
s = s[:src0] + part + s[src1:]

# Live regions for copy feedback and checklist progress.
rep('<p class="progress" id="check-progress">', '<p class="progress" id="check-progress" aria-live="polite">')
rep("</main>", '</main>\n<p id="sr-status" class="sr-only" role="status" aria-live="polite"></p>')
rep("    btn.textContent = text;\n", "    btn.textContent = text;\n    document.getElementById('sr-status').textContent = text;\n")

# Phase explorer: one tab stop, arrows move from the focused phase, Home and End.
rep('''role="button" tabindex="0" aria-label="Phase '+(i+1)+': '+p.n+'">''',
    '''role="button" tabindex="'+(i === 0 ? 0 : -1)+'" aria-label="Phase '+(i+1)+': '+p.n+'">''')
rep("""  function show(i){
    cur = i;
    var p = PH[i];
    nodes.forEach(function(n){
      var on = +n.getAttribute('data-i') === i;
      n.classList.toggle('sel', on);
      n.setAttribute('aria-pressed', on ? 'true' : 'false');
    });""",
    """  function show(i, reveal){
    cur = i;
    var p = PH[i];
    nodes.forEach(function(n){
      var on = +n.getAttribute('data-i') === i;
      n.classList.toggle('sel', on);
      n.setAttribute('aria-pressed', on ? 'true' : 'false');
      n.setAttribute('tabindex', on ? '0' : '-1');
    });
    // On a phone the diagram scrolls sideways; keep the chosen phase in view.
    if(reveal) nodes[i].scrollIntoView({inline: 'center', block: 'nearest'});""")
rep("""    document.getElementById('pd-tools').textContent = p.tools;""",
    """    document.getElementById('pd-tools').innerHTML = p.tools.replace('Lesson 4', '<a href="#goals">Lesson 4</a>');""")
rep("""    n.addEventListener('click', function(){ show(+n.getAttribute('data-i')); });
    n.addEventListener('keydown', function(e){
      if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); show(+n.getAttribute('data-i')); }
      if(e.key === 'ArrowRight' && cur < PH.length-1){ e.preventDefault(); show(cur+1); nodes[cur].focus(); }
      if(e.key === 'ArrowLeft' && cur > 0){ e.preventDefault(); show(cur-1); nodes[cur].focus(); }
    });""",
    """    n.addEventListener('click', function(){ show(+n.getAttribute('data-i'), true); });
    n.addEventListener('keydown', function(e){
      var k = +n.getAttribute('data-i'), to = null;
      if(e.key === 'Enter' || e.key === ' ') to = k;
      if(e.key === 'ArrowRight' || e.key === 'ArrowDown') to = Math.min(PH.length-1, k+1);
      if(e.key === 'ArrowLeft' || e.key === 'ArrowUp') to = Math.max(0, k-1);
      if(e.key === 'Home') to = 0;
      if(e.key === 'End') to = PH.length-1;
      if(to === null) return;
      e.preventDefault();
      show(to, true);
      nodes[to].focus();
    });""")
rep("""document.getElementById('pd-prev').addEventListener('click', function(){ if(cur>0) show(cur-1); });
  document.getElementById('pd-next').addEventListener('click', function(){ if(cur<PH.length-1) show(cur+1); });""",
    """document.getElementById('pd-prev').addEventListener('click', function(){ if(cur>0) show(cur-1, true); });
  document.getElementById('pd-next').addEventListener('click', function(){ if(cur<PH.length-1) show(cur+1, true); });""")
rep('<div class="phase-detail" id="phase-detail" aria-live="polite">', '<div class="phase-detail" id="phase-detail">')
rep('<div class="pd-top"><h3 id="pd-name">', '<div class="pd-top" aria-live="polite"><h3 id="pd-name">')

# Escape hides the evidence tooltip (WCAG 1.4.13).
rep("  window.addEventListener('scroll', hideTip, {passive: true});",
    "  window.addEventListener('scroll', hideTip, {passive: true});\n  document.addEventListener('keydown', function(e){ if(e.key === 'Escape') hideTip(); });")

# Goal builder: "Where results go" only matters for scheduled runs.
rep("    ghint.textContent = hints[mode];", "    ghint.textContent = hints[mode];\n    gi.sink.closest('.field').hidden = mode !== 'schedule';")

# ---------- child 4: lesson references become links; each lesson names its playbook section ----------
in_section("phases", "Frame is the short version of Lesson 3:", 'Frame is the short version of <a href="#discovery">Lesson 3</a>:')
in_section("phases", "a goal prompt like the one in Lesson 4.</dd>", 'a goal prompt like the one in <a href="#goals">Lesson 4</a>.</dd>')
in_section("prompts", "The goal prompt from Lesson 4 is the main one", 'The goal prompt from <a href="#goals">Lesson 4</a> is the main one')
PLAYBOOK = {"loop": "§1, §2, §4", "rules": "§1, §2", "discovery": "§5.1–5.3", "goals": "Template B", "phases": "§5.4",
            "orchestration": "§3, §7", "patterns": "§5.3, §6", "toolbox": "§3A", "selfcheck": "§9", "guardrails": "§10",
            "running": "§11", "pipeline": "§12", "growing": "§13", "prompts": "§16", "failures": "§14, §15",
            "checklist": "§9, §13", "evidence": "§19"}
for sid, sec in PLAYBOOK.items():
    in_section(sid, '<p class="lesson-end">', f'<p class="lesson-end"><span class="pb">More in the playbook: {sec}</span>')

# ---------- child 9: figures keep 1 unit = 1px on phones and scroll with a cue; tables become cards ----------
s, n = re.subn(r'style="max-width:(\d+)px"', r'style="--vbw:\1px;max-width:\1px"', s)
if n != 10:
    raise SystemExit(f"expected 10 figure widths, found {n}")
s, n = re.subn(r'(\n\s*)<div class="scroll">', r'\1<p class="scroll-cue" aria-hidden="true">Swipe sideways to see the whole figure →</p>\1<div class="scroll">', s)
print("scroll cues", n)

# ---------- child 11 (part): a takeaway under each lesson title, and two callouts ----------
TAKE = {
    "loop": "You say what done means; Claude runs the loop until it can prove it. Without a real test, it stops when it feels finished.",
    "rules": "Give outcomes and a way to prove them, load only what the next step needs, and enforce must-happen rules in code.",
    "discovery": "By the end, every issue has an outcome, a runnable check and a boundary, and open questions are written down, not guessed.",
    "goals": "State the result you want and two to five checks that prove it, plus when Claude must stop and ask.",
    "phases": "Ten phases take big tasks from goal to ship. Critique and Learn get skipped, but matter most when Claude works alone.",
    "orchestration": "Send helpers wide reading, parallel jobs and fresh-eyes review. Keep small jobs, and jobs that touch the same files, in the lead.",
    "patterns": "Plan, critique, build is the default for most coding. Use a specialist pattern only when your task matches its “Use it when” column.",
    "toolbox": "Start with five features: CLAUDE.md for standing rules, Plan mode, Skills, Subagents and Hooks. Look up the rest when a job needs them.",
    "selfcheck": "The builder never grades its own work. Ask for a receipt: each criterion marked PASS, FAIL or NOT RUN, with its command.",
    "guardrails": "Deny rules win in every mode. Never give one session all three: private data, untrusted content, a way to send data out.",
    "running": "Any run without you needs a stop condition, a retry cap, a cost ceiling and a home for its results.",
    "pipeline": "You act at the edges: write the issue, delegate, approve. Protect the gate files so the agent can't switch off its own checks.",
    "growing": "After ten tasks, the trend in your scorecard shows where to invest. Growing also means pruning rules that never fire.",
    "prompts": "Pick the template for the step you're on; paste Self-check before Claude wraps up and Retro after a real task.",
    "failures": "Match the symptom to its likely cause, then apply the fix. After two failures with the same cause, stop and get a second opinion.",
    "checklist": "Before: a checkable goal. During: an approved plan. After: a receipt with commands and a retro that produces one to three changes.",
    "evidence": "The evidence backs one writer by default, outside checks over self-critique, and measuring repeated runs and cost, not single wins.",
}
for sid, text in TAKE.items():
    a = s.index(f'<section id="{sid}"')
    h = s.index("</h2>", a) + len("</h2>")
    s = s[:h] + f'\n  <p class="takeaway"><span>Takeaway</span> {text}</p>' + s[h:]

P_PERM = '<a class="ev p" href="https://code.claude.com/docs/en/permissions" target="_blank" rel="noopener" data-src="Claude Code docs: Permissions" aria-label="P, primary source: Claude Code docs: Permissions (opens in a new tab)">P</a>'
P_SAND = '<a class="ev p" href="https://code.claude.com/docs/en/sandboxing" target="_blank" rel="noopener" data-src="Claude Code docs: Sandboxing" aria-label="P, primary source: Claude Code docs: Sandboxing (opens in a new tab)">P</a>'
P_TRI = '<a class="ev p" href="https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/" target="_blank" rel="noopener" data-src="Simon Willison: The lethal trifecta (Jun 2025)" aria-label="P, primary source: Simon Willison: The lethal trifecta (Jun 2025) (opens in a new tab)">P</a>'
D_TAG = '<span class="ev d" tabindex="0" role="note" data-src="Our own advice, built from the sources on this page" aria-label="D, our design advice: Our own advice, built from the sources on this page">D</span>'
starter = f'''
  <div class="panel starter">
    <h3>Start with these 3</h3>
    <ol>
      <li>Deny rules for secrets. A deny always beats an allow, in every mode. {P_PERM}</li>
      <li>Sandbox on, with no unsandboxed retries. It covers shell commands only. {P_SAND}</li>
      <li>In every session, remove one of the three dangers in the figure below: private data, untrusted content, or a way to send data out. {P_TRI}</li>
    </ol>
    <p><b>Good enough for a solo developer:</b> these three are enough to start. The rest of this lesson is for teams and unattended runs. {D_TAG}</p>
  </div>'''
a = s.index('<section id="guardrails"')
t = s.index("</p>", s.index('<p class="takeaway">', a)) + len("</p>")
s = s[:t] + starter + s[t:]
reality = '''  <div class="rule-box">
    <span>Reality check</span>
    <p>One writer by default. Fan out only for parallel, read-heavy work; steps that depend on each other go worse with more agents. External checks beat self-critique. See <a href="#evidence">Lesson 17</a>.</p>
  </div>

  <div class="two-col">
    <div class="panel">
      <h4>Send a helper when</h4>'''
rep('''  <div class="two-col">
    <div class="panel">
      <h4>Send a helper when</h4>''', reality)

open(path, "w", encoding="utf-8").write(s)
print("ok")
