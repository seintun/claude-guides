"""Turn every <b class="ev x">X</b> evidence tag in the page into a cited link.

Each tag gets the URL and title of the source it stands for, chosen by the
text right after the tag (or right before it, for tags that end a sentence or
sit in a table row). Tags in the Sources section reuse the link beside them.
Any tag left unmatched is reported and the file is not written.
"""
import html
import re
import sys

path = sys.argv[1]
src = open(path, encoding="utf-8").read()

U = {
    "latent": ("https://latent.space/p/claude-code", "Latent Space: Boris Cherny and Cat Wu on Claude Code (May 2025)"),
    "paddo_boris": ("https://paddo.dev/blog/how-boris-uses-claude-code", "paddo.dev: how Boris Cherny uses Claude Code (recap)"),
    "sdk": ("https://claude.com/blog/building-agents-with-the-claude-agent-sdk", "Anthropic: Building agents with the Claude Agent SDK (Sep 2025)"),
    "karpathy_notes": ("https://github.com/forrestchang/andrej-karpathy-skills", "Karpathy's Jan 2026 notes, as quoted in andrej-karpathy-skills"),
    "karpathy_decoder": ("https://the-decoder.com/former-tesla-ai-chief-andrej-karpathy-now-codes-mostly-in-english-just-three-months-after-calling-ai-agents-useless/", "The Decoder: Karpathy now codes mostly through agents (Jan 2026)"),
    "ctx_eng_karpathy": ("https://the-decoder.com/shopify-ceo-and-ex-openai-researcher-agree-that-context-engineering-beats-prompt-engineering/", "The Decoder: Karpathy and Lütke on context engineering (Jun 2025)"),
    "ctx_eng": ("https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents", "Anthropic: Effective context engineering for AI agents (Sep 2025)"),
    "pragmatic": ("https://newsletter.pragmaticengineer.com/p/building-claude-code-with-boris-cherny", "Pragmatic Engineer: Building Claude Code with Boris Cherny (Mar 2026)"),
    "best": ("https://code.claude.com/docs/en/best-practices", "Claude Code docs: Best practices"),
    "team_tips": ("https://www.jitendrazaa.com/blog/others/tips/10-claude-code-tips-from-the-creator-boris-cherny-february/", "Recap of the Claude Code team's tips thread (Jan 2026)"),
    "hooks": ("https://code.claude.com/docs/en/hooks", "Claude Code docs: Hooks"),
    "multi": ("https://www.anthropic.com/engineering/multi-agent-research-system", "Anthropic: How we built our multi-agent research system (Jun 2025)"),
    "shapeup": ("https://basecamp.com/shapeup", "Basecamp: Shape Up, plus the other discovery sources listed below"),
    "prd_trap": ("https://tuchizblog.today/en/posts/ai-prd-to-dev-tickets/", "Practitioner post: turning AI-drafted PRDs into tickets"),
    "pocock_repo": ("https://github.com/mattpocock/skills/", "Matt Pocock's skills repo (grill-me, PRD and issue skills)"),
    "pocock_talk": ("https://www.youtube.com/watch?v=-QFHIoCo-Ko", "Matt Pocock: full AI coding workflow walkthrough (AI Engineer)"),
    "bockeler": ("https://www.martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html", "Birgitta Böckeler: Understanding spec-driven development tools"),
    "bea": ("https://www.anthropic.com/engineering/building-effective-agents", "Anthropic: Building effective agents (Dec 2024)"),
    "harness": ("https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents", "Anthropic: Effective harnesses for long-running agents (Nov 2025)"),
    "huntley": ("https://ghuntley.com/ralph/", "Geoffrey Huntley: Ralph"),
    "autoresearch": ("https://github.com/karpathy/autoresearch", "karpathy/autoresearch on GitHub"),
    "council": ("https://github.com/karpathy/llm-council", "karpathy/llm-council on GitHub"),
    "goal": ("https://code.claude.com/docs/en/goal", "Claude Code docs: /goal"),
    "kiro": ("https://kiro.dev/docs/specs/", "Kiro docs: Specs"),
    "bmad_trap": ("https://paddo.dev/blog/the-19-agent-trap/", "paddo.dev: The 19-agent trap (BMAD critique)"),
    "humanlayer": ("https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md", "HumanLayer: Advanced context engineering for coding agents"),
    "beck": ("https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes", "Kent Beck: Augmented coding, beyond the vibes (Jun 2025)"),
    "evals": ("https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents", "Anthropic: Demystifying evals for AI agents (Jan 2026)"),
    "trifecta": ("https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "Simon Willison: The lethal trifecta (Jun 2025)"),
    "perms": ("https://code.claude.com/docs/en/permissions", "Claude Code docs: Permissions"),
    "automode_paper": ("https://arxiv.org/html/2604.04978v1", "arXiv 2604.04978: stress test of Claude Code auto mode"),
    "sandbox": ("https://code.claude.com/docs/en/sandboxing", "Claude Code docs: Sandboxing"),
    "settings": ("https://code.claude.com/docs/en/settings", "Claude Code docs: Settings and managed settings"),
    "headless": ("https://code.claude.com/docs/en/headless", "Claude Code docs: Headless mode"),
    "skills_paper": ("https://arxiv.org/abs/2602.06547", "arXiv 2602.06547: malicious community skills (MCPTox figure: AAAI paper in Sources)"),
    "web": ("https://code.claude.com/docs/en/claude-code-on-the-web", "Claude Code docs: Claude Code on the web"),
    "costs": ("https://code.claude.com/docs/en/costs", "Claude Code docs: Costs"),
    "scheduled": ("https://code.claude.com/docs/en/routines", "Claude Code docs: Scheduled tasks"),
    "bg_compare": ("https://dreaming.press/posts/devin-vs-codex-vs-cursor-vs-jules-background-agents.html", "Comparison of background coding agents (dreaming.press)"),
    "gha": ("https://github.com/anthropics/claude-code-action", "anthropics/claude-code-action on GitHub"),
    "gha_security": ("https://github.com/anthropics/claude-code-action/blob/main/docs/security.md", "claude-code-action: security notes"),
    "gh_secure": ("https://docs.github.com/en/actions/reference/security/secure-use", "GitHub docs: Secure use of Actions"),
    "gh_queue": ("https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue", "GitHub docs: Managing a merge queue"),
    "linear_agents": ("https://linear.app/docs/agents-in-linear", "Linear docs: Agents in Linear"),
    "linear_gh": ("https://linear.app/docs/github", "Linear docs: GitHub integration"),
    "symphony": ("https://pub.towardsai.net/i-pointed-openais-symphony-at-20-linear-issues-the-15k-star-orchestrator-killed-my-standup-27e19cf85233", "Towards AI: a coding agent on 20 Linear issues"),
    "ours": ("#sources", "Our own advice, built from the sources on this page"),
}

# (where, needle, key): "after" looks at the text right after the tag,
# "before" at the text right before it. First match wins.
RULES = [
    ("after", "their own words", ("#sources", "Primary: the person's own words, or official docs")),
    ("after", "second-hand reports of a post", ("#sources", "Second-hand: articles or recaps quoting a post")),
    ("after", "an independent research paper", ("#sources", "Research: an independent paper or preprint")),
    ("after", "advice built from the sources", ("#sources", "Design advice: our synthesis, not a quote")),
    ("after", "Boris Cherny describes Claude Code", "latent"),
    ("after", "Recaps of Boris Cherny's setup", "paddo_boris"),
    ("after", "Anthropic's Agent SDK loop", "sdk"),
    ("after", "Reports of Karpathy's notes", "karpathy_notes"),
    ("after", "Anthropic: pitch prompts", "ctx_eng"),
    ("after", "Karpathy endorsed", "ctx_eng_karpathy"),
    ("after", "Anthropic: recall drops", "ctx_eng"),
    ("after", "Early Claude Code tried RAG", "latent"),
    ("after", "Boris Cherny starts most sessions", "pragmatic"),
    ("after", "Official best practices: explore", "best"),
    ("after", "Best practices: an adversarial review", "best"),
    ("after", "Boris Cherny: after a correction", "team_tips"),
    ("after", "Best practices: cut any CLAUDE.md", "best"),
    ("after", "A Stop hook exiting with code 2", "hooks"),
    ("after", "Anthropic's multi-agent research system beat", "multi"),
    ("after", "By December he was doing", "karpathy_decoder"),
    ("after", "Our pipeline, built from these", "ours"),
    ("after", "sources: Jobs to Be Done", "shapeup"),
    ("after", "A common trap: AI-drafted specs", "prd_trap"),
    ("after", "Birgitta Böckeler (martinfowler.com) found", "bockeler"),
    ("after", "So treat the spec as intent", "ours"),
    ("after", 'The "watch out for" column is our advice', "ours"),
    ("before", "then build in a fresh session.", "pocock_repo"),
    ("before", "turns findings into new issues.", "pocock_talk"),
    ("before", "Skipping the critic", "best"),
    ("before", "Brittle when a stage varies", "bea"),
    ("before", "Two writers on one file", "bea"),
    ("before", "About 15 times chat tokens", "multi"),
    ("before", "Endless loops when they aren't", "bea"),
    ("before", "Declaring victory early", "harness"),
    ("before", "(GitHub issue)", "huntley"),
    ("before", "read-only to the agent", "autoresearch"),
    ("before", "not a product", "council"),
    ("before", "Needs a real sandbox", "pocock_talk"),
    ("before", "must show in the output", "goal"),
    ("before", "Spec-first only; heavy for small changes", "bockeler"),
    ("before", "no independent evaluation found", "kiro"),
    ("before", "long ramp to first code", "bmad_trap"),
    ("before", "Rule bloat unless pruned", "ours"),
    ("before", "Specs miss edge cases, so add QA", "pocock_talk"),
    ("before", "Only the author's case studies", "humanlayer"),
    ("before", "Agents still try to delete tests", "beck"),
    ("before", "calls this pass^k.", "evals"),
    ("before", "Remove at least one of the three in every session.", "trifecta"),
    ("before", "deny rules hold in every mode.", "perms"),
    ("before", "Anthropic reports on real traffic.", "automode_paper"),
    ("before", "to stop that.", "sandbox"),
    ("before", "run agents only in checkouts you trust.", "settings"),
    ("before", "put the checks in the CI job.", "headless"),
    ("before", "attack success in tests.", "skills_paper"),
    ("before", "count against your plan limits.", "web"),
    ("before", "the two copies drift apart.", "web"),
    ("before", "comment-driven deploy bots.", "web"),
    ("before", "the Console is the real bill.", "costs"),
    ("before", "as well as failed ones.", "scheduled"),
    ("before", "where you start them.", "bg_compare"),
    ("before", "never allow every bot on a public repo.", "gha"),
    ("before", "still come from the PR.", "gha_security"),
    ("before", "pin actions to a full commit SHA.", "gh_secure"),
    ("before", "to listen for merge_group.", "gh_queue"),
    ("before", "it's advice to the agent, not a gate.", "linear_agents"),
    ("before", "close an issue without any review.", "linear_gh"),
    ("before", "missed the real cause.", "symphony"),
]

TAG = re.compile(r'<b class="ev ([psrd])">([PSRD])</b>')
ANCHOR_BEFORE = re.compile(r'<a href="([^"]+)"[^>]*>([^<]+)</a>\s*$')


def text(fragment):
    t = re.sub(r"<[^>]+>", "", fragment)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def resolve(m):
    before_raw = src[max(0, m.start() - 400):m.start()]
    a = ANCHOR_BEFORE.search(before_raw)
    if a:
        return a.group(1), html.unescape(a.group(2)).strip()
    after = text(src[m.end():m.end() + 300])[:90]
    before = text(before_raw)[-110:]
    for where, needle, key in RULES:
        hay = after if where == "after" else before
        if needle in hay:
            return key if isinstance(key, tuple) else U[key]
    return None


KIND = {"p": "primary source", "s": "second-hand report", "r": "research paper", "d": "our design advice"}
out, last, missing = [], 0, []
for m in TAG.finditer(src):
    found = resolve(m)
    if not found:
        missing.append(text(src[max(0, m.start() - 120):m.end() + 120]))
        continue
    url, title = found
    kind, letter = m.group(1), m.group(2)
    external = not url.startswith("#")
    label = f"{letter}, {KIND[kind]}: {title}" + (" (opens in a new tab)" if external else "")
    attrs = [f'class="ev {kind}"', f'href="{html.escape(url, quote=True)}"']
    if external:
        attrs.append('target="_blank" rel="noopener"')
    attrs.append(f'data-src="{html.escape(title, quote=True)}"')
    attrs.append(f'aria-label="{html.escape(label, quote=True)}"')
    out.append(src[last:m.start()])
    out.append(f"<a {' '.join(attrs)}>{letter}</a>")
    last = m.end()
out.append(src[last:])

if missing:
    print(f"{len(missing)} tag(s) unmatched; file not written:")
    for s in missing:
        print("  -", s)
    sys.exit(1)

open(path, "w", encoding="utf-8").write("".join(out))
print(f"linked {len(TAG.findall(src))} tags")
