"""Child 6: apply the visual language to every figure. Each replacement must match exactly the expected number of times."""
import sys

path = sys.argv[1]
s = open(path, encoding="utf-8").read()


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"expected {count} of {old[:70]!r}, found {n}")
    s = s.replace(old, new)


# ---------- Lesson 1: the loop ----------
rep('<svg viewBox="0 0 770 300" role="img"', '<svg viewBox="0 0 770 300" style="max-width:770px" role="img"')
rep('<rect x="16" y="122" width="140" height="58" rx="8" class="d-box key"/>',
    '<rect x="16" y="122" width="140" height="58" rx="29" class="d-you"/>')
rep('<rect x="210" y="204" width="140" height="58" rx="8" class="d-box warn"/>',
    '<rect x="210" y="204" width="140" height="58" rx="8" class="d-box"/>')
rep('<figcaption><strong>The agent loop.</strong> The loop only ends well',
    '<ul class="fig-key"><li><i class="k-you"></i>You</li><li><i class="k-box"></i>Claude</li><li><i class="k-line pass"></i>Check passes</li><li><i class="k-line loop"></i>Sent back</li></ul>\n'
    '    <figcaption><strong>The check decides when the loop ends.</strong> The loop only ends well')

# ---------- Lesson 3: discovery pipeline, redrawn 880 wide ----------
old_l3_start = s.index('<svg viewBox="0 0 980 170"')
old_l3_end = s.index('</svg>', old_l3_start) + len('</svg>')
names = [("Frame", "you", True), ("Assumptions", "you rank", True), ("Grill", "agent asks", False),
         ("Shape", "agent drafts", False), ("Bet", "you decide", True), ("Specify", "agent drafts", False),
         ("Slice", "agent drafts", False), ("Deliver", "agents build", False)]
X0, W, STEP = 12, 100, 108
parts = [
    '<svg viewBox="0 0 880 170" style="max-width:880px" role="img" aria-label="You own the why and the bet; the agent drafts the rest. Discovery pipeline: Frame, Assumptions and Bet are yours; Grill, Shape, Specify and Slice are drafted by the agent; then agents deliver. Ideas that are not bet on get parked. QA findings from delivery come back as new issues.">',
    '      <defs>',
    '        <marker id="d-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="d-arrow"/></marker>',
    '        <marker id="d-al" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="d-arrow loop"/></marker>',
    '      </defs>',
]
disc_end = X0 + 6 * STEP + W
parts.append(f'      <rect x="{X0}" y="14" width="{disc_end - X0}" height="22" rx="4" class="d-band"/>')
parts.append(f'      <text x="{(X0 + disc_end) // 2}" y="29" text-anchor="middle" class="d-band-text">DISCOVERY · YOU OWN THE WHY</text>')
dx = X0 + 7 * STEP
parts.append(f'      <rect x="{dx}" y="14" width="{W}" height="22" rx="4" class="d-band"/>')
parts.append(f'      <text x="{dx + W // 2}" y="29" text-anchor="middle" class="d-band-text">DELIVERY</text>')
for i, (name, who, yours) in enumerate(names):
    x = X0 + i * STEP
    cls = 'rx="29" class="d-you"' if yours else 'rx="8" class="d-box"'
    parts.append(f'      <rect x="{x}" y="52" width="{W}" height="58" {cls}/>')
    parts.append(f'      <text x="{x + W // 2}" y="78" text-anchor="middle" class="d-title sm">{name}</text>')
    parts.append(f'      <text x="{x + W // 2}" y="97" text-anchor="middle" class="d-sub">{who}</text>')
for i in range(7):
    a = X0 + i * STEP + W + 1
    parts.append(f'      <path d="M{a},81 L{a + 6},81" class="d-edge" marker-end="url(#d-a)"/>')
bet = X0 + 4 * STEP + W // 2
parts.append(f'      <path d="M{bet},110 L{bet},138" class="d-edge" marker-end="url(#d-a)"/>')
parts.append(f'      <text x="{bet + 10}" y="134" class="d-label">not now: park it</text>')
dlv, slc = X0 + 7 * STEP + W // 2, X0 + 6 * STEP + W // 2
parts.append(f'      <path d="M{dlv},110 C{dlv},146 {slc},146 {slc},114" class="d-edge loop" marker-end="url(#d-al)"/>')
parts.append(f'      <text x="{(dlv + slc) // 2}" y="160" text-anchor="middle" class="d-label loop">QA findings become new issues</text>')
parts.append('    </svg>')
s = s[:old_l3_start] + "\n".join(parts) + s[old_l3_end:]
rep('<figcaption><strong>Discovery, then delivery.</strong> Each stage',
    '<ul class="fig-key"><li><i class="k-you"></i>You decide</li><li><i class="k-box"></i>The agent drafts or builds</li><li><i class="k-line loop"></i>Sent back</li></ul>\n'
    '    <figcaption><strong>You own the why and the bet; the agent drafts the rest.</strong> Each stage')

# ---------- Lesson 5: phase explorer (drawn by script) ----------
rep('<svg id="phase-svg" class="phase-svg" viewBox="0 0 980 240" role="group"',
    '<svg id="phase-svg" class="phase-svg" viewBox="0 0 880 240" style="max-width:880px" role="group"')
rep("var W = 84, H = 60, Y = 56, GAP = 96, X0 = 16;", "var W = 78, H = 60, Y = 56, GAP = 86, X0 = 15;")
rep("""  function back(from, to, depth, label){
    var x1 = cx(from), x2 = cx(to);
    var out = '<path d="M'+x1+','+B+' C'+x1+','+(B+depth)+' '+x2+','+(B+depth)+' '+x2+','+(B+4)+'" class="d-edge loop" marker-end="url(#p-al)"/>';
    out += '<text x="'+((x1+x2)/2)+'" y="'+(B+depth*0.75+15)+'" text-anchor="middle" class="d-label loop">'+label+'</text>';
    return out;
  }""",
    """  // Orange arcs send work back to an earlier phase; the grey dashed arc is the next run.
  function back(from, to, depth, label, next){
    var x1 = cx(from), x2 = cx(to);
    var out = '<path d="M'+x1+','+B+' C'+x1+','+(B+depth)+' '+x2+','+(B+depth)+' '+x2+','+(B+4)+'" class="d-edge '+(next ? 'dash' : 'loop')+'" marker-end="url(#'+(next ? 'p-a' : 'p-al')+')"/>';
    out += '<text x="'+((x1+x2)/2)+'" y="'+(B+depth*0.75+15)+'" text-anchor="middle" class="d-label'+(next ? '' : ' loop')+'">'+label+'</text>';
    return out;
  }""")
rep("s += back(9,0,120,'next run, with lessons');", "s += back(9,0,120,'next run, with lessons', true);")
rep("""      </div>
    </div>
  </figure>

  <p>Two phases are the ones people skip""",
    """      </div>
    </div>
    <ul class="fig-key"><li><i class="k-box"></i>A phase (select one)</li><li><i class="k-line loop"></i>Sent back to an earlier phase</li><li><i class="k-line auto"></i>Next run</li></ul>
    <figcaption><strong>Work moves left to right, and a failed check sends it back.</strong> Each orange arc is a loop back; the dashed arc carries lessons into the next run.</figcaption>
  </figure>

  <p>Two phases are the ones people skip""")

# ---------- Lesson 6: lead and helpers ----------
rep('<svg viewBox="0 0 900 400" role="img" aria-label="You give the lead session',
    '<svg viewBox="0 0 880 400" style="max-width:880px" role="img" aria-label="Helpers do the reading; the lead keeps only their summaries. You give the lead session')
rep('<rect x="16" y="158" width="120" height="64" rx="8" class="d-box key"/>',
    '<rect x="16" y="158" width="120" height="64" rx="32" class="d-you"/>')
rep('<rect x="200" y="96" width="220" height="184" rx="10" class="d-fill-accent"/>',
    '<rect x="200" y="96" width="220" height="184" rx="10" class="d-box lead"/>')
rep('<text x="310" y="144" text-anchor="middle" class="d-small">the orchestrator</text>',
    '<text x="310" y="144" text-anchor="middle" class="d-sub">the orchestrator</text>')
for y in (16, 80, 144, 208, 272):
    for cls in ("d-box", "d-box warn", "d-box good"):
        old = f'<rect x="600" y="{y}" width="284" height="52" rx="8" class="{cls}"/>'
        if old in s:
            rep(old, f'<rect x="600" y="{y}" width="264" height="52" rx="8" class="d-box"/>')
rep('<text x="870" y="', '<text x="850" y="', count=5)
rep('<rect x="200" y="344" width="684" height="44" rx="8" class="d-box soft"/>',
    '<rect x="200" y="344" width="664" height="44" rx="8" class="d-box auto"/>')
rep('<figcaption><strong>The lead and its helpers.</strong>',
    '<ul class="fig-key"><li><i class="k-you"></i>You</li><li><i class="k-box"></i>Claude (lead or helper)</li><li><i class="k-auto"></i>Runs on its own</li><li><i class="k-line you"></i>You act</li></ul>\n'
    '    <figcaption><strong>Helpers do the reading; the lead keeps only their summaries.</strong>')

# ---------- Lesson 6: context chart colours (child 7 reworks the chart) ----------
rep('<svg id="ctx-chart" viewBox="0 0 780 290" role="img"', '<svg id="ctx-chart" viewBox="0 0 780 290" style="max-width:780px" role="img"')
rep('<i style="background:var(--series-2)"></i>', '<i style="background:var(--ink-2)"></i>')
rep('<i style="background:var(--series-1)"></i>', '<i style="background:var(--accent)"></i>')
rep('rx="3" fill="var(--series-1)"', 'rx="3" fill="var(--accent)"', count=2)  # Lesson 17 bars; child 7 rebuilds that chart
rep('var(--series-2)', 'var(--ink-2)', count=4)
rep('var(--series-1)', 'var(--accent)', count=4)

# ---------- Lesson 10: Venn ----------
rep('<svg viewBox="0 0 640 310" role="img" aria-label="The lethal trifecta:',
    '<svg viewBox="0 0 640 310" style="max-width:640px" role="img" aria-label="Take away any one circle and the danger zone is gone. The lethal trifecta:')
rep('class="v1"/>', 'class="venn"/>')
rep('class="v2"/>', 'class="venn"/>')
rep('class="v3"/>', 'class="venn"/>')
rep('<figcaption><strong>The lethal trifecta.</strong>', '<figcaption><strong>Take away any one circle and the danger zone is gone.</strong>')

# ---------- Lesson 11: timeline ----------
rep('<svg viewBox="0 0 900 250" role="img" aria-label="Timeline over three days.',
    '<svg viewBox="0 0 880 250" style="max-width:880px" role="img" aria-label="What wakes Claude decides whether your computer must stay on. Timeline over three days.')
rep('<line x1="880" y1="30" x2="880" y2="236" class="d-grid"/>', '<line x1="879" y1="30" x2="879" y2="236" class="d-grid"/>')
rep('class="d-dot loop"/>', 'class="d-dot ev"/>', count=4)
rep('<figcaption><strong>Three ways to run continuously.</strong>',
    '<ul class="fig-key"><li><i class="k-line"></i>/loop runs</li><li><i class="k-help" style="background:var(--ink-2)"></i>Scheduled run</li><li><i class="k-help" style="background:var(--surface);border:2px solid var(--ink-2)"></i>Event</li></ul>\n'
    '    <figcaption><strong>What wakes Claude decides whether your computer must stay on.</strong>')

# ---------- Lesson 12: sequence ----------
rep('<svg viewBox="0 0 880 536" role="img" aria-label="Sequence:',
    '<svg viewBox="0 0 880 536" style="max-width:880px" role="img" aria-label="You act only at the edges; checks and status moves happen on their own. Sequence:')
rep('<rect x="20" y="12" width="120" height="36" rx="8" class="d-box key"/>', '<rect x="20" y="12" width="120" height="36" rx="18" class="d-you"/>')
rep('<rect x="740" y="12" width="120" height="36" rx="8" class="d-box"/>', '<rect x="740" y="12" width="120" height="36" rx="8" class="d-box auto"/>')
rep('class="d-edge dash"/>\n      <line x1="260"', 'class="d-edge dash life"/>\n      <line x1="260"')
for x in (260, 440, 620, 800):
    rep(f'<line x1="{x}" y1="48" x2="{x}" y2="524" class="d-edge dash"/>', f'<line x1="{x}" y1="48" x2="{x}" y2="524" class="d-edge dash life"/>')
rep('class="d-edge loop dash" marker-end="url(#s-al)"', 'class="d-edge loop" marker-end="url(#s-al)"')
rep('<figcaption><strong>One issue, end to end.</strong> You act only at the edges:',
    '<ul class="fig-key"><li><i class="k-you"></i>You</li><li><i class="k-auto"></i>Automatic checks</li><li><i class="k-line you"></i>You act</li><li><i class="k-line loop"></i>Sent back</li><li><i class="k-line pass"></i>Done</li></ul>\n'
    '    <figcaption><strong>You act only at the edges; checks and status moves happen on their own.</strong> You act at three points:')

# ---------- Lesson 13: learning loop ----------
rep('<svg viewBox="0 0 860 176" role="img" aria-label="The learning loop:',
    '<svg viewBox="0 0 860 176" style="max-width:860px" role="img" aria-label="Each run should leave the next one a better rule. The learning loop:')
rep('<rect x="676" y="24" width="170" height="60" rx="8" class="d-box key"/>', '<rect x="676" y="24" width="170" height="60" rx="8" class="d-box"/>')
rep('<path d="M761,84 C761,150 101,150 101,88" class="d-edge loop" marker-end="url(#g-al)"/>',
    '<path d="M761,84 C761,150 101,150 101,88" class="d-edge dash" marker-end="url(#g-a)"/>')
rep('<text x="431" y="168" text-anchor="middle" class="d-label loop">the next run starts smarter</text>',
    '<text x="431" y="168" text-anchor="middle" class="d-label">the next run starts smarter</text>')
rep('<figcaption><strong>The learning loop.</strong>', '<figcaption><strong>Each run should leave the next one a better rule.</strong>')

# ---------- Lesson 13: scorecard direction ----------
rep('<td class="want up">Up</td>', '<td class="want">↑ Up</td>', count=2)
rep('<td class="want down">Down</td>', '<td class="want">↓ Down</td>', count=3)
rep('<td class="want">Steady</td>', '<td class="want">→ Steady</td>')

# ---------- Lesson 17: bars (child 7 rebuilds this chart) ----------
rep('<svg viewBox="0 0 720 230" role="img"', '<svg viewBox="0 0 720 230" style="max-width:720px" role="img"')

open(path, "w", encoding="utf-8").write(s)
print("ok")
