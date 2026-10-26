"""Child 3: the "Words you'll meet" strip, and a definition where each term first appears.
Definitions and first-use edits come from issues/drafts/glossary.md."""
import html
import sys

path = sys.argv[1]
s = open(path, encoding="utf-8").read()


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"expected {count} of {old[:80]!r}, found {n}")
    s = s.replace(old, new)


def term(key, word):
    return f'<a class="term" id="fu-{key}" href="#g-{key}">{word}</a>'


# (key, label, definition, regex, lesson where it is first defined)
TERMS = [
    ("goal", "goal", "What you want done, how you will know it is done, and the limits Claude works within.", r"(?<!/)\bgoals?\b", "Lesson 1"),
    ("check", "check, gate", "A test, command or observation that decides if the work is done. A gate runs one automatically, so Claude can't skip it.", r"\b(?:the|a|an|each|every|one|stricter|real|your|any|good|these|missing|runnable|required|automatic|no) checks?\b|\bchecks\b|\bgates?\b", "Lesson 1"),
    ("context", "context window", "Claude's working memory. Every file it reads fills it, and when it gets full, early details fade.", r"context windows?|(?:own|fresh|clean|main|one|lead's|only) context\b|window (?:fills|gets full)|own windows", "Lesson 2"),
    ("subagent", "subagent, helper", "A helper agent that does one narrow job in its own context window and sends back a short summary.", r"sub-?agents?|\bhelpers?\b", "Lesson 1"),
    ("lead", "orchestrator, lead", "The main Claude session. It holds the goal and plan, makes the calls, and hands jobs to helpers. That is orchestration.", r"orchestrators?|\blead\b", "Lesson 1"),
    ("hook", "hook", "A script of yours that runs on its own when a set event happens, so Claude can't skip it.", r"\bhooks?\b", "Lesson 1"),
    ("stophook", "Stop hook", "A hook that runs when Claude tries to finish, for example to rerun the tests. It can block Claude from finishing.", r"\bstop (?:hooks?|gates?)\b", "Lesson 2"),
    ("harness", "harness", "Everything wrapped around the model to steer it: its tools, rules and checks. Each piece should prevent a named failure.", r"harness(?:es)?", "Lesson 2"),
    ("receipt", "receipt", "A closing report: each check from your goal marked PASS, FAIL or NOT RUN, with the command behind it.", r"\breceipts?\b", "Lesson 6"),
    ("worktree", "worktree", "A separate copy of your project's code, so two agents never edit the same files.", r"\bworktrees?\b", "Lesson 6"),
    ("mcp", "MCP", "Short for Model Context Protocol. Plug-ins that connect Claude to outside tools such as GitHub, Linear and browsers.", r"\bMCP\b|model context protocol", "Lesson 8"),
    ("headless", "headless", "Claude running with no chat window, called from a script (claude -p) instead of you typing to it.", r"\bheadless\b", "Lesson 10"),
    ("sandbox", "sandbox", "A restricted space for shell commands, limiting the files and network they can reach. Edits, hooks and MCP servers run outside it.", r"\b(?:un)?sandbox(?:es|ed)?\b", "Lesson 7"),
    ("trifecta", "lethal trifecta", "An agent that holds private data, reads untrusted content and can send data out can be steered into leaking it.", r"lethal trifecta|\btrifecta\b", "Lesson 10"),
]

items = []
for key, label, definition, rx, where in TERMS:
    items.append(
        f'    <div class="g-item" id="g-{key}" data-term="{html.escape(rx, quote=True)}" data-first="fu-{key}">'
        f'<dt>{label}</dt><dd>{definition} <a class="g-where" href="#fu-{key}">{where}</a></dd></div>')
names = ", ".join(t[1].split(",")[0] for t in TERMS)
strip = (
    '<details class="glossary" id="glossary">\n'
    f'  <summary><span class="g-label">Words you\'ll meet</span> <span class="g-list">{names}</span></summary>\n'
    '  <dl>\n' + "\n".join(items) + '\n  </dl>\n'
    '</details>\n\n')
rep('</header>\n\n<details class="lessons-menu"', '</header>\n\n' + strip + '<details class="lessons-menu"')

# Lesson 1: check, subagent, hook and goal in the intro; gate and lead in the roles list.
rep('<p class="intro">An AI agent is a loop: plan a step, do it, check the result, and adjust. Orchestration, subagents, hooks and schedules are all ways to run this loop better. A sharper goal makes the check honest.',
    f'<p class="intro">An AI agent is a loop: plan a step, do it, {term("check", "check")} the result (with a test, a command or an observation), and adjust. Orchestration, {term("subagent", "subagents")} (helpers that each take one job), {term("hook", "hooks")} (scripts that run on their own) and schedules are all ways to run this loop better. A sharper {term("goal", "goal")} (what you want done, and how you will know) makes the check honest.')
rep('<li><b>The lead session</b> (the orchestrator) holds the plan and makes the calls.</li>',
    f'<li><b>The {term("lead", "lead")} session</b> (the orchestrator) holds the plan and makes the calls.</li>')
rep("<li><b>Helpers and gates</b> do side work and run checks the lead can't skip.</li>",
    "<li><b>Helpers and gates</b> do side work and run checks the lead can't skip; a gate is a check that runs on its own.</li>")

# Lesson 2: harness, context window, Stop hook.
rep('<h3>Keep the harness thin</h3><p>Let the model do the thinking. Every piece of scaffolding should name the failure it prevents',
    f'<h3>Keep the harness thin</h3><p>Let the model do the thinking. The {term("harness", "harness")} is the scaffolding around it: tools, rules and checks. Every piece should name the failure it prevents')
rep('<p>Load what the next step needs, not everything. Send heavy reading to helpers.</p>',
    f'<p>Load what the next step needs into the {term("context", "context window")} (Claude\'s working memory), not everything. Send heavy reading to helpers.</p>')
rep('<p>Anything that must happen every time lives in a hook, CI or a permission rule, not only in prose.</p>',
    f'<p>Anything that must happen every time lives in a hook (such as a {term("stophook", "Stop hook")}, which runs when Claude tries to finish), CI or a permission rule, not only in prose.</p>')

# Lesson 6: receipt and worktree, before the figure that uses them.
rep('It hands narrow jobs to helper agents (subagents). Each helper starts with a clean memory, does one job, and sends back a short summary. The lead sees the conclusion, not the pile of reading behind it.</p>',
    f'It hands narrow jobs to helper agents (subagents). Each helper starts with a clean memory, does one job (a builder works in its own {term("worktree", "worktree")}, a separate copy of the project\'s code), and sends back a short summary. The lead sees the conclusion, not the pile of reading behind it, and ends by giving you a {term("receipt", "receipt")}: each success criterion marked PASS, FAIL or NOT RUN, with the command behind it.</p>')

# Lesson 7: sandbox.
rep('a sandboxed loop builds the issues overnight', f'a {term("sandbox", "sandboxed")} loop (its shell commands run in a restricted space) builds the issues overnight')

# Lesson 8: MCP.
rep('<span class="feat">MCP connectors</span>', f'<span class="feat">{term("mcp", "MCP")} (Model Context Protocol) connectors</span>')

# Lesson 10: headless and the lethal trifecta.
rep('<li><b>Headless runs trust the repo.</b>', f'<li><b>{term("headless", "Headless")} runs (Claude called from a script, with no chat window) trust the repo.</b>')
rep("Simon Willison's warning: an agent that holds private data",
    f"Simon Willison's warning, the {term('trifecta', 'lethal trifecta')}: an agent that holds private data")

open(path, "w", encoding="utf-8").write(s)
print("ok")
