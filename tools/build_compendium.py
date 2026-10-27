"""Build docs/orchestrating-claude-compendium.html: one self-contained, searchable, offline file.

Usage (from the repository root): python3 -I tools/build_compendium.py
Reads the Markdown and HTML sources in this repository, needs no third-party packages, and
writes a single HTML file with inline CSS and JavaScript and no network requests.
"""
import html
import os
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# An optional first argument writes elsewhere; tests/test_generated.py uses it to compare.
OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(ROOT, "docs", "orchestrating-claude-compendium.html")
ARTIFACT_URL = "https://claude.ai/artifact/8q1jNZyZ1HTjDBvqgBWMLq"
sys.path.insert(0, os.path.join(ROOT, "tools"))   # python3 -I leaves the script's folder off sys.path
import section as playbook_sections  # noqa: E402  (this file has its own section())

PB_VERSION, PB_UPDATED = playbook_sections.version()   # from the playbook's Version line, never hard-coded


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


WIKI = [
    ("start-a-task.md", "Start a task"),
    ("grill.md", "Grill before you plan"),
    ("orchestrate.md", "Orchestrate"),
    ("verify.md", "Verify"),
    ("run-unattended.md", "Run unattended"),
    ("guardrails.md", "Guardrails"),
    ("build-a-harness.md", "Build a harness"),
    ("records.md", "Where records live"),
    ("improve.md", "Improve"),
    ("unstick.md", "Unstick an agent"),
    ("case-study.md", "Case study: this repository"),
]
# Markdown file name -> (prefix for its heading anchors, id of its block in the compendium)
DOC_LINKS = {
    "agent-harness-playbook.md": ("pb", "playbook"),
    "decision-log.md": ("decisions", "decisions"),
    "session-log.md": ("session", "session"),
    "version-history.md": ("versions", "versions"),
    "final-review-v15.md": ("status", "status"),
    "orchestrating-claude-ux.md": ("issue", "issue"),
    "google-scaling-check.md": ("gsc", "gsc"),
    "bounded-review-evidence.md": ("bre", "bre"),
    "AGENTS.md": ("agents", "agents"),
    "ENTRY.md": ("entry", "entry"),
    "orchestration-index.md": ("oi", "index"),
    "claude-cheat-sheet.md": ("cs", "cs"),
    "SKILL.md": ("skill-brief", "skill-brief"),
    "harness-reset-proposal.md": ("prop", "prop"),
    "playbook-factcheck-v0.3.md": ("rev-fc", "rev-fc"),
}
for _name, _label in WIKI:
    _key = "wiki-" + _name[:-3]
    DOC_LINKS[_name] = (_key, _key)


# ---------------------------------------------------------------- Markdown -> HTML
def slugify(text, seen):
    """GitHub-style heading slug, made unique within one document."""
    s = re.sub(r"<[^>]+>", "", text).strip().lower()
    s = re.sub(r"[^\w\- ]", "", s, flags=re.UNICODE).replace(" ", "-")
    base, n = s, 1
    while s in seen:
        s = f"{base}-{n}"
        n += 1
    seen.add(s)
    return s


def inline(text, prefix):
    """Inline Markdown: code spans, links, bold, italics. Everything else is escaped."""
    codes = []

    def keep_code(m):
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", keep_code, text)
    text = html.escape(text, quote=False)

    def link(m):
        label, url = m.group(1), m.group(2).strip()
        if url.startswith("#"):
            return f'<a href="#{prefix}-{url[1:]}">{label}</a>'
        if re.match(r"https?://", url):
            return f'<a href="{html.escape(url)}" target="_blank" rel="noopener">{label}</a>'
        # Links between this repository's documents point inside the compendium.
        target, _, anchor = url.partition("#")
        mapped = DOC_LINKS.get(os.path.basename(target))
        if mapped:
            anchor_prefix, section_id = mapped
            return f'<a href="#{anchor_prefix}-{anchor}">{label}</a>' if anchor else f'<a href="#{section_id}">{label}</a>'
        return f'<span class="file-ref" title="{html.escape(url)}">{label}</span>'

    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, text)
    text = re.sub(r"&lt;(https?://[^&\s]+)&gt;", r'<a href="\1" target="_blank" rel="noopener">\1</a>', text)
    text = re.sub(r"(?<![=\"'>/])(https?://[^\s<)\]]+[^\s<)\].,;:])", r'<a href="\1" target="_blank" rel="noopener">\1</a>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{html.escape(codes[int(m.group(1))], quote=False)}</code>", text)


def split_row(line):
    cells = re.split(r"(?<!\\)\|", line.strip().strip("|"))
    return [c.strip().replace("\\|", "|") for c in cells]


LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")


def md_to_html(md, prefix, drop_title=True):
    lines = md.replace("\r\n", "\n").split("\n")
    out, seen, i, first_h1 = [], set(), 0, drop_title

    def flush_para(buf):
        if buf:
            out.append(f"<p>{inline(' '.join(x.strip() for x in buf), prefix)}</p>")
            buf.clear()

    para = []
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            flush_para(para)
            lang = line.strip()[3:].strip()
            body = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            cls = f' class="lang-{html.escape(lang)}"' if lang else ""
            out.append(f"<pre><code{cls}>{html.escape(chr(10).join(body), quote=False)}</code></pre>")
            continue
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*$", line)
        if m:
            flush_para(para)
            level, text = len(m.group(1)), m.group(2)
            if level == 1 and first_h1:
                first_h1 = False
                i += 1
                continue
            tag = f"h{min(6, max(3, level + 1))}"
            out.append(f'<{tag} id="{prefix}-{slugify(text, seen)}">{inline(text, prefix)}</{tag}>')
            i += 1
            continue
        if re.match(r"^\s*(---+|\*\*\*+)\s*$", line):
            flush_para(para)
            out.append("<hr>")
            i += 1
            continue
        if line.lstrip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{2,}", lines[i + 1]):
            flush_para(para)
            head = split_row(line)
            i += 2
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            t = ['<div class="tw"><table><thead><tr>' + "".join(f"<th>{inline(c, prefix)}</th>" for c in head) + "</tr></thead><tbody>"]
            for r in rows:
                t.append("<tr>" + "".join(f"<td>{inline(c, prefix)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table></div>")
            out.append("".join(t))
            continue
        if line.startswith(">"):
            flush_para(para)
            quote = []
            while i < len(lines) and lines[i].startswith(">"):
                quote.append(lines[i][1:].lstrip() if lines[i][1:2] == " " else lines[i][1:])
                i += 1
            out.append(f"<blockquote>{md_to_html(chr(10).join(quote), prefix, drop_title=False)}</blockquote>")
            continue
        if LIST_RE.match(line):
            flush_para(para)
            items = []  # (indent, ordered, text)
            while i < len(lines):
                lm = LIST_RE.match(lines[i])
                if lm:
                    items.append([len(lm.group(1).expandtabs(4)), lm.group(2)[0].isdigit(), lm.group(3)])
                    i += 1
                elif lines[i].strip() and lines[i].startswith((" ", "\t")) and items and not lines[i].strip().startswith("```"):
                    items[-1][2] += " " + lines[i].strip()
                    i += 1
                else:
                    break
            out.append(render_list(items, prefix))
            continue
        if not line.strip():
            flush_para(para)
            i += 1
            continue
        para.append(line)
        i += 1
    flush_para(para)
    return "\n".join(out)


def render_list(items, prefix):
    html_parts, stack = [], []  # stack of (indent, tag)
    for indent, ordered, text in items:
        tag = "ol" if ordered else "ul"
        while stack and indent < stack[-1][0]:
            html_parts.append(f"</li></{stack.pop()[1]}>")
        if not stack or indent > stack[-1][0]:
            html_parts.append(f"<{tag}>")
            stack.append((indent, tag))
        else:
            html_parts.append("</li>")
        html_parts.append(f"<li>{inline(text, prefix)}")
    while stack:
        html_parts.append(f"</li></{stack.pop()[1]}>")
    return "".join(html_parts)


# ---------------------------------------------------------------- the teaching page
PAGE = read("site/orchestrating-claude.html")
# The page shows its own version in its footer; read it there, never hard-code it.
PAGE_VERSION, PAGE_UPDATED = re.search(r"Version (\d+), last updated (\d{4}-\d{2}-\d{2})\.", PAGE).groups()


def page_document(src):
    # No web fonts inside the compendium: the page falls back to system fonts, so nothing loads over the network.
    src = re.sub(r'<link rel="(?:preconnect|stylesheet)" href="https://fonts\.[^"]+"[^>]*>\n?', "", src)
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"></head><body>' + src + "</body></html>"


def page_text_blocks(src):
    """The page's lessons as plain text, one block per paragraph, for reading and search."""
    blocks = []
    for m in re.finditer(r'<section id="([^"]+)"[^>]*>(.*?)</section>', src, re.S):
        sid, body = m.group(1), m.group(2)
        body = re.sub(r"<(script|style)\b.*?</\1>", " ", body, flags=re.S)
        body = re.sub(r'<p class="lesson-end">.*?</p>', " ", body, flags=re.S)
        kicker = re.search(r'<p class="kicker">(.*?)</p>', body, re.S)
        title = re.search(r"<h2>(.*?)</h2>", body, re.S)
        clean = lambda s: html.unescape(re.sub(r"<[^>]+>", " ", s)).split()
        head = " ".join(clean(kicker.group(1))) if kicker else sid
        head = re.sub(r"\s*(Core|Builder|Reference) · \d+ min$", "", head)
        h2 = " ".join(clean(title.group(1))) if title else ""
        body = re.sub(r"<(/?)(p|li|h3|h4|tr|figcaption|summary|dt|dd|div|text|pre)\b[^>]*>", "\n", body)
        paras = [" ".join(clean(p)) for p in body.split("\n")]
        paras = [p for p in paras if len(p) > 1 and p not in (h2,)]
        blocks.append((sid, head, h2, paras))
    return blocks


def page_sources(src):
    """The page's Sources lesson as (group, title, url, grade) rows."""
    a = src.index('<section id="sources"')
    b = src.index("</section>", a)
    rows, group = [], ""
    for m in re.finditer(r'<h3>(.*?)</h3>|<li><a href="([^"]+)"[^>]*>(.*?)</a>\s*<a class="ev ([psrd])"', src[a:b], re.S):
        if m.group(1):
            group = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))
        else:
            rows.append((group, html.unescape(m.group(3)), html.unescape(m.group(2)), m.group(4).upper()))
    return rows


# ---------------------------------------------------------------- sections
GRADE = {"P": "Primary", "S": "Second-hand", "R": "Research", "D": "Design advice"}


def code_listing(rel, note):
    src = read(rel)
    lines = src.count("\n") + 1
    return (f'<details class="code"><summary><code>{html.escape(rel)}</code> <span class="muted">· {lines} lines · {html.escape(note)}</span></summary>'
            f'<pre><code>{html.escape(src, quote=False)}</code></pre></details>')


def doc(rel, prefix, label=None):
    body = md_to_html(read(rel), prefix)
    src = f'<p class="src-path">Source: <code>{html.escape(rel)}</code></p>'
    if label:
        return f'<section class="sub" id="{prefix}"><h3 class="subhead">{html.escape(label)}</h3>{src}{body}</section>'
    return src + body


sections = []


def section(sid, title, lead, body):
    sections.append((sid, title, lead, body))


# About
layout = [
    ("site/orchestrating-claude.html", f"The teaching page, version {PAGE_VERSION}, last updated {PAGE_UPDATED} (artifact body: no doctype; the viewer wraps it)"),
    ("site/history/orchestrating-claude-v11.html", "The version 11 baseline the UX issue was written against"),
    ("playbook/agent-harness-playbook.md", f"The agent harness playbook, version {PB_VERSION}, last updated {PB_UPDATED}"),
    ("research/google-scaling-check.md", "Primary-source fact-check of the Google agent-scaling study"),
    ("issues/orchestrating-claude-ux.md", "The UX issue: parent, 13 children, plan and task contract"),
    ("issues/reviews/", "Every review report: UX, learning, charts, playbook, chart, post-launch, final"),
    ("issues/drafts/", "Drafts that subagents wrote and the lead spliced in"),
    ("docs/", "Decision log, session log, version history, and this compendium"),
    ("checks/", "Static and browser checks, the v11 baseline, the URL baseline"),
    ("tools/", "Build and maintenance scripts; tools/provenance holds the one-off edit scripts"),
]
about = f"""
<p>This file collects everything from one working session on 24 October 2026. The session built and reviewed
<strong>Orchestrating Claude</strong>, a 17-lesson teaching page about goals, checks, helper agents and unattended runs,
and the <strong>Agent Harness Playbook</strong> that the page summarises. It includes the research, every review, every
decision, the issue that drove the rework, and the scripts that check and rebuild the work.</p>
<p>It is one HTML file with no network requests, so it reads offline. Press <kbd>/</kbd> to search: results come from every
section, including the full text of the page and the playbook. The page itself is embedded in the
<a href="#page">Teaching page</a> section, and the live version is at <a href="{ARTIFACT_URL}" target="_blank" rel="noopener">claude.ai</a>
(private to its owner until shared).</p>
<div class="tw"><table><thead><tr><th>Path in the repository</th><th>What it is</th></tr></thead><tbody>
{''.join(f'<tr><td><code>{html.escape(p)}</code></td><td>{html.escape(d)}</td></tr>' for p, d in layout)}
</tbody></table></div>
<h3 id="about-reproduce">Rebuild and check</h3>
<pre><code>python3 -I tools/build_compendium.py        # rebuild this file
checks/static.sh                            # static checks; also writes build/preview.html
# then run checks/run-dom.js with Playwright's run_code tool (see checks/README.md)
python3 -I tools/lesson_meta.py site/orchestrating-claude.html   # refresh reading times</code></pre>
<p class="muted">Built {date.today().isoformat()} from the repository's sources by <code>tools/build_compendium.py</code>.</p>
"""
section("about", "About this compendium", "What is here and how to use it offline.", about)

# Guides: the wiki runbooks, in reading order
wiki_present = [(n, l) for n, l in WIKI if os.path.exists(os.path.join(ROOT, "wiki", n))]
if wiki_present:
    guide_index = "<ul class='guide-list'>" + "".join(
        f'<li><a href="#wiki-{n[:-3]}">{html.escape(l)}</a></li>' for n, l in wiki_present) + "</ul>"
    guides = ("<p>Short runbooks distilled from the playbook. Each one gives steps, a checklist, the templates to copy, "
              "the pitfalls, and links to the detail.</p>" + guide_index
              + "".join(doc(f"wiki/{n}", f"wiki-{n[:-3]}", l) for n, l in wiki_present)
              + doc("playbook/claude-cheat-sheet.md", "cs", "Claude Code cheat sheet"))
    section("entry", "Start here (ENTRY.md)", "The entry point for a session in another project: the scenario router and the phase table.", doc("ENTRY.md", "entry"))
    section("index", "Orchestration index", "The phase index: eight phases, what to read in each, and review checklists.", doc("orchestration-index.md", "oi"))
    section("guides", "Guides", "Runbooks for building, orchestrating and guiding agents.", guides)
section("status", "Where it stands", "The final independent review, with what changed after it.", doc("issues/reviews/final-review-v15.md", "status"))
section("session", "Session log", "Every request in the session and its outcome.", doc("docs/session-log.md", "session"))
section("decisions", "Decisions", "What was decided, why, and by whom, plus one open proposal.",
        doc("docs/decision-log.md", "decisions")
        + doc("docs/proposals/harness-reset-proposal.md", "prop", "Proposal (draft): reset a personal harness to a lean baseline"))
section("versions", "Version history", f"Page versions 1–{PAGE_VERSION} and playbook versions 0.1–{PB_VERSION}.", doc("docs/version-history.md", "versions"))

# The page: embedded, plus its text
blocks = page_text_blocks(PAGE)
page_text = []
for sid, head, h2, paras in blocks:
    page_text.append(f'<details class="lesson" id="page-{sid}"><summary><span class="kick">{html.escape(head)}</span> {html.escape(h2)}</summary>'
                     + "".join(f"<p>{html.escape(p)}</p>" for p in paras) + "</details>")
page_body = f"""
<p>The page as published (version {PAGE_VERSION}, last updated {PAGE_UPDATED}), running inside this file. Its links open in a new tab. It starts dark,
and its sun and moon button switches between dark and light. This copy uses system fonts, so it needs no network.</p>
<p><button type="button" class="btn" id="open-page">Open the page on its own</button>
<a class="btn ghost" href="{ARTIFACT_URL}" target="_blank" rel="noopener">Open the live artifact</a></p>
<iframe class="page-frame" title="Orchestrating Claude, version {PAGE_VERSION}" loading="lazy" sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox" srcdoc="{html.escape(page_document(PAGE), quote=True)}"></iframe>
<h3 id="page-text">The page as text</h3>
<p class="muted">Every lesson's text, so search can reach it. Open a lesson to read it.</p>
{''.join(page_text)}
"""
section("page", "Teaching page", "Orchestrating Claude: 17 lessons and Sources, embedded and as text.", page_body)
section("playbook", "Agent Harness Playbook", f"The build reference behind the page, version {PB_VERSION}, last updated {PB_UPDATED}.", doc("playbook/agent-harness-playbook.md", "pb"))

# Research
src_rows = page_sources(PAGE)
groups = {}
for g, t, u, gr in src_rows:
    groups.setdefault(g, []).append((t, u, gr))
src_html = "".join(
    f"<h4>{html.escape(g)}</h4><ul class='sources'>" + "".join(
        f'<li><span class="grade g-{gr.lower()}" title="{GRADE[gr]}">{gr}</span> <a href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(t)}</a></li>'
        for t, u, gr in items) + "</ul>" for g, items in groups.items())
research = f"""
<p>Research ran through subagents using Firecrawl, Exa and web search, with <code>doc-checker</code> for primary-source checks.
Its findings live in the page (Lesson 17 and the evidence tags) and in playbook §19 and §20. This section adds the
fact-check that corrected the Lesson 17 chart and the list of sources the page cites.</p>
<p>Evidence grades: <span class="grade g-p">P</span> primary (the person's own words or official docs),
<span class="grade g-s">S</span> second-hand reports, <span class="grade g-r">R</span> research papers,
<span class="grade g-d">D</span> design advice built from the sources.</p>
{doc("research/google-scaling-check.md", "gsc", "Fact-check: Google's agent-scaling study")}
{doc("research/bounded-review-evidence.md", "bre", "Evidence: how agent reviews should end")}
<section class="sub" id="sources-cited"><h3 class="subhead">Sources the page cites ({len(src_rows)})</h3>{src_html}</section>
"""
section("research", "Research and sources", "Fact-checks and every source the page cites.", research)
section("issue", "The UX issue and plan", "Parent issue, 13 children, plan table and builder contract.", doc("issues/orchestrating-claude-ux.md", "issue"))

reviews = "".join([
    doc("issues/reviews/ux.md", "rev-ux", "UI/UX and accessibility review (v11)"),
    doc("issues/reviews/lx.md", "rev-lx", "Learning-psychology review (v11)"),
    doc("issues/reviews/vz.md", "rev-vz", "Charts and diagrams review (v11)"),
    doc("issues/reviews/playbook-factcheck-v0.3.md", "rev-fc", "Playbook v0.3 fact-check review, with the v0.5 receipt"),
    doc("issues/reviews/playbook-review.md", "rev-pb", "Playbook navigation review"),
    doc("issues/reviews/chart-review-v12.md", "rev-chart", "Chart review (v12)"),
    doc("issues/reviews/post-launch-review-v12.md", "rev-post", "Post-launch re-review (v12)"),
])
section("reviews", "Reviews", "Every independent review, in order. The final review is under Where it stands.", reviews)

drafts = "".join(
    f'<details class="draft"><summary>{label} <span class="muted">· <code>{rel}</code></span></summary>{md_to_html(read(rel), pfx)}</details>'
    for rel, pfx, label in [
        ("issues/drafts/glossary.md", "dr-gl", "Glossary and first-use definitions"),
        ("issues/drafts/density.md", "dr-dn", "Takeaways, starter sets, grouping and disclosures"),
        ("issues/drafts/running-example.md", "dr-rx", "Running example, recall items, quiz and try-now"),
    ])
drafts = "<p>Subagents wrote these drafts in parallel while the lead edited the page. The lead applied them with the changes noted in the decision log (D17, D18).</p>" + drafts
section("drafts", "Drafts", "Content the drafting agents produced.", drafts)

skills = ("<p>Skills are reusable Claude Code procedures. To install one, copy its folder into <code>~/.claude/skills/</code> "
          "or a project's <code>.claude/skills/</code>.</p>"
          + doc("skills/grill/SKILL.md", "skill-grill", "/grill: SKILL.md")
          + doc("skills/prompt/SKILL.md", "skill-prompt", "/prompt: SKILL.md")
          + f'<details class="code"><summary>How /grill and /prompt were tested together</summary>'
          + md_to_html(read("tests/live/grill-prompt/results.md"), "skill-grill-prompt-results")
          + "</details>")
section("skills", "Skills", "Claude Code skills built along the way.", skills)

repro = (doc("tests/README.md", "tests", "Tests: what each feature is tested by")
         + doc("checks/README.md", "chk")
         + f"<h3 id='chk-baseline'>Version 11 baseline</h3><pre><code>{html.escape(read('checks/baseline-v11.txt'), quote=False)}</code></pre>"
         + f"<h3 id='chk-final'>Version {PAGE_VERSION} result</h3><p>27 of 27 page checks pass in 8 views (320, 375 light and dark, 414, 768, 1024, 1280 light and dark): dom-1 to dom-13, phase-explorer keyboard (kbd-1 to kbd-3), phone menu (nav-1, nav-2), quiz keyboard (quiz-1), theme toggle (theme-1 to theme-5), unique ids and no script errors. Static checks 1 to 6 pass.</p>"
         + "<h3 id='chk-code'>Scripts</h3>"
         + code_listing("checks/static_checks.py", "static checks on the page source")
         + code_listing("checks/static.sh", "runs the static checks and writes build/preview.html")
         + code_listing("checks/dom-checks.js", "in-page checks, injected into each view")
         + code_listing("checks/run-dom.js", "Playwright runner: eight views and the keyboard scenarios")
         + code_listing("checks/shots.js", "screenshots of every figure")
         + code_listing("tools/lesson_meta.py", "writes levels, reading times and path totals")
         + code_listing("tools/splice_figs.py", "splices redrawn figures from a draft into the page")
         + code_listing("tools/check_links.py", "checks every Markdown link and anchor")
         + code_listing("checks/compendium-check.js", "browser check for this file")
         + code_listing("tools/build_compendium.py", "builds this file"))
section("reproduce", "Reproduce and verify", "How the checks work, their results, and the scripts.", repro)
section("agents", "Working on this repository", "The agent instructions that ship with the repository.", doc("AGENTS.md", "agents"))


# ---------------------------------------------------------------- assemble
toc = "".join(f'<li><a href="#{sid}">{html.escape(t)}</a></li>' for sid, t, _, _ in sections)
main = "".join(
    f'<section class="sec" id="{sid}" data-title="{html.escape(t)}"><header class="sec-head"><p class="eyebrow">{i + 1:02d}</p><h2>{html.escape(t)}</h2><p class="lead">{html.escape(lead)}</p></header>{body}</section>'
    for i, (sid, t, lead, body) in enumerate(sections))

CSS = r"""
/* Layout: a reading column with a sticky contents rail and a search bar; every colour is a token. */
:root{
  --bg:#F4F6F8; --surface:#FFFFFF; --ink:#16212B; --ink-2:#465462; --ink-3:#5B6875; --rule:#D6DCE2;
  --accent:#2443D6; --accent-soft:#E4E9FC; --mark:#FFE58A; --mark-ink:#16212B;
  --g-p:#0B7A43; --g-s:#7A3E9D; --g-r:#2443D6; --g-d:#5B6875; --code-bg:#EBEFF3; --shadow:rgba(20,32,43,.12);
  --f-body:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  --f-display:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  --f-mono:ui-monospace,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#0E141A; --surface:#151D25; --ink:#E5EBF0; --ink-2:#A8B5C1; --ink-3:#8C99A6; --rule:#2A3540;
    --accent:#8FA2FF; --accent-soft:#1B2650; --mark:#6B5A12; --mark-ink:#FFF6CC;
    --g-p:#4CC38A; --g-s:#C99BEA; --g-r:#8FA2FF; --g-d:#A8B5C1; --code-bg:#1B242E; --shadow:rgba(0,0,0,.5);
    color-scheme:dark;
  }
}
:root[data-theme="dark"]{
  --bg:#0E141A; --surface:#151D25; --ink:#E5EBF0; --ink-2:#A8B5C1; --ink-3:#8C99A6; --rule:#2A3540;
  --accent:#8FA2FF; --accent-soft:#1B2650; --mark:#6B5A12; --mark-ink:#FFF6CC;
  --g-p:#4CC38A; --g-s:#C99BEA; --g-r:#8FA2FF; --g-d:#A8B5C1; --code-bg:#1B242E; --shadow:rgba(0,0,0,.5);
  color-scheme:dark;
}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:76px}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 var(--f-body);-webkit-font-smoothing:antialiased}
a{color:var(--accent)}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:3px}
code,kbd{font-family:var(--f-mono);font-size:.88em;background:var(--code-bg);padding:.05em .35em;border-radius:4px;overflow-wrap:anywhere}
pre{background:var(--code-bg);border-radius:8px;padding:12px 14px;overflow:auto;font-size:13.5px;line-height:1.5;max-height:520px}
pre code{background:none;padding:0;font-size:inherit;overflow-wrap:normal}
.muted{color:var(--ink-2);font-size:.92em}
.topbar{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(6px);border-bottom:1px solid var(--rule)}
.topbar-in{max-width:1240px;margin:0 auto;display:flex;align-items:center;gap:14px;padding-block:10px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.brand{font-weight:800;letter-spacing:-.01em;white-space:nowrap}
.brand span{color:var(--ink-2);font-weight:500}
.search{position:relative;flex:1;max-width:560px;margin-left:auto}
.search input{width:100%;font:inherit;font-size:15px;color:var(--ink);background:var(--surface);border:1px solid var(--ink-3);border-radius:8px;padding:8px 72px 8px 34px}
.search input::-webkit-search-cancel-button{display:none}
.search svg{position:absolute;left:10px;top:50%;transform:translateY(-50%);width:16px;height:16px;stroke:var(--ink-2);fill:none;stroke-width:2}
.search-count{position:absolute;right:10px;top:50%;transform:translateY(-50%);font-size:12px;color:var(--ink-2);font-family:var(--f-mono)}
.results{position:absolute;left:0;right:0;top:calc(100% + 6px);background:var(--surface);border:1px solid var(--rule);border-radius:10px;box-shadow:0 12px 32px var(--shadow);max-height:min(70vh,560px);overflow:auto;padding:6px;margin:0;list-style:none}
.results li button{display:block;width:100%;text-align:left;font:inherit;font-size:14px;color:var(--ink);background:none;border:0;border-radius:6px;padding:8px 10px;cursor:pointer}
.results li button:hover,.results li button[aria-selected="true"]{background:var(--accent-soft)}
.results .r-sec{display:block;font-family:var(--f-mono);font-size:11.5px;letter-spacing:.04em;text-transform:uppercase;color:var(--ink-2);margin-bottom:2px}
.results .r-none{padding:10px;color:var(--ink-2);font-size:14px}
mark{background:var(--mark);color:var(--mark-ink);border-radius:2px;padding:0 1px}
.btn{display:inline-block;font:inherit;font-weight:700;font-size:14px;padding:7px 13px;border-radius:7px;border:1px solid var(--accent);background:var(--accent);color:var(--surface);cursor:pointer;text-decoration:none;line-height:1.2}
.btn.ghost{background:transparent;color:var(--accent)}
.theme-btn{font:inherit;font-size:13px;color:var(--ink-2);background:var(--surface);border:1px solid var(--rule);border-radius:7px;padding:6px 10px;cursor:pointer;white-space:nowrap}
.shell{max-width:1240px;margin:0 auto;display:grid;grid-template-columns:220px minmax(0,1fr);gap:40px;padding-block:28px 96px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.toc{position:sticky;top:76px;align-self:start;max-height:calc(100vh - 96px);overflow:auto}
.toc p{font-family:var(--f-mono);font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-2);margin:0 0 8px 10px}
.toc ol{list-style:none;margin:0;padding:0;display:grid;gap:1px;counter-reset:t}
.toc li{counter-increment:t}
.toc a{display:flex;gap:9px;padding:6px 10px;border-radius:6px;color:var(--ink-2);text-decoration:none;font-size:14.5px;line-height:1.3}
.toc a::before{content:counter(t,decimal-leading-zero);font-family:var(--f-mono);font-size:11.5px;color:var(--ink-3);padding-top:2px}
.toc a:hover{background:var(--surface);color:var(--ink)}
.toc a.on{background:var(--accent-soft);color:var(--ink);font-weight:600}
main{min-width:0}
.hero{padding:8px 0 26px;border-bottom:1px solid var(--rule);margin-bottom:8px}
.hero h1{font-size:clamp(30px,4.2vw,46px);line-height:1.05;letter-spacing:-.02em;margin:0 0 10px;text-wrap:balance}
.hero p{max-width:70ch;color:var(--ink-2);margin:0}
.stats{display:flex;flex-wrap:wrap;gap:8px 18px;margin-top:14px;font-size:14px;color:var(--ink-2)}
.stats b{color:var(--ink);font-variant-numeric:tabular-nums}
.sec{padding-top:34px;border-top:1px solid var(--rule);margin-top:26px}
.sec:first-of-type{border-top:0;margin-top:0}
.sec-head .eyebrow{font-family:var(--f-mono);font-size:12px;letter-spacing:.08em;color:var(--accent);margin:0 0 4px}
.sec h2{font-size:clamp(24px,2.8vw,32px);line-height:1.15;letter-spacing:-.01em;margin:0 0 6px;text-wrap:balance}
.sec .lead{color:var(--ink-2);margin:0 0 18px}
.sec h3{font-size:20px;line-height:1.25;margin:28px 0 8px;text-wrap:balance}
.sec h4{font-size:17px;margin:22px 0 6px}
.sec h5,.sec h6{font-size:15px;margin:18px 0 6px}
.sec p,.sec li{max-width:76ch;overflow-wrap:anywhere}
.sec h2,.sec h3,.sec h4,.sec h5,.sec h6,summary{overflow-wrap:anywhere}
td{overflow-wrap:anywhere}
.sec ul,.sec ol{padding-left:1.3em}
.sec li{margin:3px 0}
blockquote{margin:12px 0;padding:4px 0 4px 16px;border-left:3px solid var(--rule);color:var(--ink-2)}
hr{border:0;border-top:1px dashed var(--rule);margin:24px 0}
.tw{overflow-x:auto;margin:14px 0;border:1px solid var(--rule);border-radius:10px;background:var(--surface)}
table{width:100%;border-collapse:collapse;font-size:14.5px;line-height:1.45}
th{text-align:left;font-size:12.5px;letter-spacing:.03em;color:var(--ink-2);background:var(--bg);font-weight:700;padding:9px 12px;border-bottom:1px solid var(--rule);vertical-align:bottom}
td{padding:9px 12px;border-bottom:1px solid var(--rule);vertical-align:top}
tr:last-child td{border-bottom:0}
.src-path{font-size:13px;color:var(--ink-2);margin:0 0 12px}
.sub{margin-top:30px;padding-top:6px}
.subhead{font-size:21px!important;padding-bottom:6px;border-bottom:1px solid var(--rule)}
.file-ref{border-bottom:1px dotted var(--ink-3)}
details{margin:10px 0;border:1px solid var(--rule);border-radius:10px;background:var(--surface);padding:10px 14px}
details > summary{cursor:pointer;font-weight:600}
details[open] > summary{margin-bottom:8px}
details.lesson .kick{font-family:var(--f-mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--accent);margin-right:6px}
details.lesson p{font-size:15px;margin:6px 0}
details.code pre{max-height:640px}
.page-frame{display:block;width:100%;height:min(82vh,900px);border:1px solid var(--rule);border-radius:10px;background:var(--surface);margin:12px 0 4px}
.grade{display:inline-block;font-family:var(--f-mono);font-size:11px;font-weight:700;padding:0 6px;border-radius:4px;border:1px solid currentColor;vertical-align:1px}
.g-p{color:var(--g-p)} .g-s{color:var(--g-s)} .g-r{color:var(--g-r)} .g-d{color:var(--g-d)}
ul.sources{list-style:none;padding:0;display:grid;gap:5px}
ul.guide-list{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:8px}
ul.guide-list a{display:block;padding:10px 12px;border:1px solid var(--rule);border-radius:8px;background:var(--surface);text-decoration:none;font-weight:600}
ul.guide-list a:hover{border-color:var(--accent)}
.flash{animation:flash 2.2s ease-out}
@keyframes flash{0%,40%{box-shadow:0 0 0 3px var(--accent)}100%{box-shadow:0 0 0 0 transparent}}
.to-top{position:fixed;right:max(16px,env(safe-area-inset-right,0px));bottom:max(16px,env(safe-area-inset-bottom,0px));z-index:15}
@media (max-width:900px){
  .shell{grid-template-columns:minmax(0,1fr)}
  .toc{position:static;max-height:none;border:1px solid var(--rule);border-radius:10px;background:var(--surface);padding:10px}
  .brand span{display:none}
}
@media (max-width:560px){.brand{display:none}.theme-btn{padding:6px 8px}}
@media (prefers-reduced-motion: reduce){html{scroll-behavior:auto}.flash{animation:none;outline:3px solid var(--accent)}}
@media print{
  .topbar,.toc,.to-top,.page-frame,#open-page{display:none!important}
  .shell{display:block;padding:0}
  details{border:0;padding:0}
  pre{max-height:none;white-space:pre-wrap}
  a{color:inherit}
}
"""

JS = r"""
(function(){
  /* ---------- theme: system, light or dark; remembered when storage is available ---------- */
  var root = document.documentElement, themeBtn = document.getElementById('theme');
  var modes = ['system', 'light', 'dark'];
  function applyTheme(m){
    if(m === 'system') root.removeAttribute('data-theme'); else root.setAttribute('data-theme', m);
    themeBtn.textContent = 'Theme: ' + m;
  }
  var mode = 'system';
  try { mode = localStorage.getItem('compendium-theme') || 'system'; } catch(e) {}
  applyTheme(mode);
  themeBtn.addEventListener('click', function(){
    mode = modes[(modes.indexOf(mode) + 1) % modes.length];
    applyTheme(mode);
    try { localStorage.setItem('compendium-theme', mode); } catch(e) {}
  });

  /* ---------- contents rail: mark the section in view ---------- */
  var tocLinks = document.querySelectorAll('.toc a');
  var secs = Array.prototype.slice.call(document.querySelectorAll('main .sec'));
  function markToc(){
    var line = window.innerHeight * 0.25, cur = secs[0];
    secs.forEach(function(s){ if(s.getBoundingClientRect().top <= line) cur = s; });
    tocLinks.forEach(function(a){
      var on = a.getAttribute('href') === '#' + cur.id;
      a.classList.toggle('on', on);
      if(on) a.setAttribute('aria-current', 'location'); else a.removeAttribute('aria-current');
    });
  }
  window.addEventListener('scroll', markToc, {passive: true});
  markToc();

  /* ---------- open whatever hides an element, then show it ---------- */
  function reveal(el){
    for(var p = el.parentElement; p; p = p.parentElement){ if(p.tagName === 'DETAILS') p.open = true; }
  }
  function show(el){
    reveal(el);
    el.scrollIntoView({block: 'center'});
    el.classList.remove('flash'); void el.offsetWidth; el.classList.add('flash');
  }
  document.addEventListener('click', function(e){
    var a = e.target.closest('a[href^="#"]');
    if(!a || a.getAttribute('href').length < 2) return;
    var t = document.getElementById(a.getAttribute('href').slice(1));
    if(t) reveal(t);
  });

  /* ---------- search: every paragraph, list item, table row and code block ---------- */
  var SEL = 'h3,h4,h5,p,li,tr,pre,summary,blockquote';
  var index = [];
  document.querySelectorAll('main .sec').forEach(function(sec){
    var title = sec.getAttribute('data-title');
    sec.querySelectorAll(SEL).forEach(function(el){
      if(el.querySelector(SEL)) return;
      var raw = el.tagName === 'TR' ? Array.prototype.map.call(el.cells, function(c){ return c.textContent; }).join(' · ') : el.textContent;
      var text = raw.replace(/\s+/g, ' ').trim();
      if(text.length > 1) index.push({el: el, text: text, low: text.toLowerCase(), sec: title});
    });
  });
  document.getElementById('stat-blocks').textContent = index.length.toLocaleString();

  var input = document.getElementById('q'), list = document.getElementById('results'), count = document.getElementById('q-count');
  var hits = [], sel = -1, marked = [];
  function esc(s){ return s.replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function snippet(text, terms){
    var low = text.toLowerCase(), at = low.indexOf(terms[0]);
    var start = Math.max(0, at - 60), part = text.slice(start, start + 200);
    var out = esc(part);
    terms.forEach(function(t){
      if(!t) return;
      out = out.replace(new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig'), '<mark>$1</mark>');
    });
    return (start > 0 ? '… ' : '') + out + (start + 200 < text.length ? ' …' : '');
  }
  function clearMarks(){
    marked.forEach(function(m){ var p = m.parentNode; if(!p) return; p.replaceChild(document.createTextNode(m.textContent), m); p.normalize(); });
    marked = [];
  }
  function markIn(el, terms){
    var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), nodes = [], n;
    while((n = walker.nextNode())) nodes.push(n);
    var re = new RegExp('(' + terms.map(function(t){ return t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }).join('|') + ')', 'ig');
    nodes.forEach(function(node){
      if(!re.test(node.nodeValue)) return;
      re.lastIndex = 0;
      var frag = document.createDocumentFragment(), last = 0, m;
      node.nodeValue.replace(re, function(match, g, off){
        frag.appendChild(document.createTextNode(node.nodeValue.slice(last, off)));
        var mk = document.createElement('mark'); mk.textContent = match; frag.appendChild(mk); marked.push(mk);
        last = off + match.length;
        return match;
      });
      frag.appendChild(document.createTextNode(node.nodeValue.slice(last)));
      node.parentNode.replaceChild(frag, node);
    });
  }
  function render(){
    list.innerHTML = '';
    if(!input.value.trim()){ list.hidden = true; count.textContent = ''; return; }
    if(!hits.length){ list.innerHTML = '<li class="r-none">No matches. Try fewer or shorter words.</li>'; list.hidden = false; count.textContent = '0'; return; }
    var terms = input.value.toLowerCase().split(/\s+/).filter(Boolean);
    hits.slice(0, 80).forEach(function(h, i){
      var li = document.createElement('li');
      li.innerHTML = '<button type="button" role="option" id="r' + i + '" aria-selected="' + (i === sel) + '"><span class="r-sec">' + esc(h.sec) + '</span>' + snippet(h.text, terms) + '</button>';
      li.firstChild.addEventListener('click', function(){ go(i); });
      list.appendChild(li);
    });
    count.textContent = hits.length > 80 ? '80 of ' + hits.length : String(hits.length);
    list.hidden = false;
  }
  function run(){
    var terms = input.value.toLowerCase().split(/\s+/).filter(Boolean);
    hits = terms.length ? index.filter(function(b){ return terms.every(function(t){ return b.low.indexOf(t) >= 0; }); }) : [];
    sel = hits.length ? 0 : -1;
    render();
  }
  function go(i){
    var h = hits[i]; if(!h) return;
    clearMarks();
    markIn(h.el, input.value.toLowerCase().split(/\s+/).filter(Boolean));
    list.hidden = true;
    show(h.el);
  }
  input.addEventListener('input', run);
  input.addEventListener('focus', function(){ if(input.value.trim()) render(); });
  input.addEventListener('keydown', function(e){
    if(e.key === 'ArrowDown' || e.key === 'ArrowUp'){
      e.preventDefault();
      var max = Math.min(hits.length, 80) - 1; if(max < 0) return;
      sel = e.key === 'ArrowDown' ? Math.min(max, sel + 1) : Math.max(0, sel - 1);
      render();
      var b = document.getElementById('r' + sel); if(b) b.scrollIntoView({block: 'nearest'});
    } else if(e.key === 'Enter'){ e.preventDefault(); go(Math.max(0, sel)); }
    else if(e.key === 'Escape'){ input.value = ''; clearMarks(); run(); }
  });
  input.setAttribute('aria-controls', 'results');
  document.addEventListener('keydown', function(e){
    if(e.key === '/' && document.activeElement !== input && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)){ e.preventDefault(); input.focus(); input.select(); }
  });
  document.addEventListener('click', function(e){ if(!e.target.closest('.search')) list.hidden = true; });

  /* ---------- the embedded page, on its own ---------- */
  var openPage = document.getElementById('open-page');
  if(openPage){
    openPage.addEventListener('click', function(){
      var frame = document.querySelector('.page-frame');
      var url = URL.createObjectURL(new Blob([frame.getAttribute('srcdoc')], {type: 'text/html'}));
      var w = window.open(url, '_blank', 'noopener');
      if(!w) location.href = url;
    });
  }

  /* ---------- print everything, not only the open parts ---------- */
  window.addEventListener('beforeprint', function(){ document.querySelectorAll('details').forEach(function(d){ d.open = true; }); });
})();
"""

words = len(re.sub(r"<[^>]+>", " ", main).split())
doc_html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Orchestrating Claude Compendium</title>
<meta name="description" content="Everything from the Orchestrating Claude session: the teaching page, the agent harness playbook, research, reviews, decisions and checks, in one searchable offline file.">
<style>{CSS}</style>
</head>
<body>
<div class="topbar"><div class="topbar-in">
  <div class="brand">Orchestrating Claude <span>· compendium</span></div>
  <div class="search" role="search">
    <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><path d="M20 20l-4-4"></path></svg>
    <input id="q" type="search" placeholder="Search everything (press /)" aria-label="Search the compendium" autocomplete="off" role="combobox" aria-expanded="false">
    <span class="search-count" id="q-count" aria-live="polite"></span>
    <ul class="results" id="results" role="listbox" hidden></ul>
  </div>
  <button type="button" class="theme-btn" id="theme">Theme: system</button>
</div></div>
<div class="shell">
  <nav class="toc" aria-label="Contents"><p>Contents</p><ol>{toc}</ol></nav>
  <main>
    <header class="hero">
      <h1>Orchestrating Claude: what we built, checked and decided</h1>
      <p>A 17-lesson teaching page and an agent harness playbook, with the research behind them, three expert reviews,
      a 13-part rework, four more independent reviews, and the checks that gate every change. One file, offline, searchable.</p>
      <div class="stats"><span><b>{len(sections)}</b> sections</span><span><b>{words:,}</b> words</span><span><b id="stat-blocks">0</b> searchable blocks</span><span><b>{len(src_rows)}</b> sources</span><span>Page <b>v16</b></span><span>Playbook <b>v0.4</b></span></div>
    </header>
    {main}
  </main>
</div>
<a class="btn ghost to-top" href="#about">↑ Top</a>
<script>{JS}</script>
</body>
</html>
"""
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(doc_html)
print(f"wrote {os.path.relpath(OUT, ROOT)}: {len(doc_html) / 1024:.0f} KB, {len(sections)} sections, {words:,} words, {len(src_rows)} sources")
