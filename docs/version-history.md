# Version history

## Teaching page (artifact https://claude.ai/artifact/8q1jNZyZ1HTjDBvqgBWMLq)

| Version | What changed | Checks |
|---|---|---|
| 1–10 | First build of 17 lessons and Sources; research folded in; fact-check corrections; graded P/S/R/D tags with links and tooltips; Lesson 17 on proven orchestration; tooltip theming; D tags made tooltip-only | Manual review in the built-in browser; link check: 77 of 82 links returned 2xx, the rest load in a browser |
| 11 | Baseline for the UX issue (`site/history/orchestrating-claude-v11.html`) | `checks/baseline-v11.txt`: 12 PASS, 57 FAIL |
| 12 | 30-minute launch. Children 0–7, 9 and 10, plus the takeaways and callouts from child 11 | 20 of 20 in 6 views |
| 13 | Phase buttons under the diagram; the panel height is held; the page no longer jumps | Steady over 18 clicks in 3 views |
| 14 | Phase nav centered, with "← Prev" and "Next →" | Steady and symmetric at 1280, 375 and 320px |
| 15 | Fixes from the reviews and the blocking chart items; child 8 diagrams (L1, L3, L5, L6, L9, L11, L12); the rest of child 11; child 12 (running example, recall items, try-now, quiz); glossary tooltips; quiz colours | 20 of 20 in 6 views |
| 16 | Final review fixes: keyboard-safe quiz, 12px figure text at every width, tables that wrap at mid widths, two more folded tables, glosses, wording, safe hash handling | 21 of 21 in 8 views (320, 375 ×2, 414, 768, 1024, 1280 ×2) |

## Repository releases

| Tag | Date | What changed |
|---|---|---|
| v1.0.0 | 2026-10-26 | First public release |
| v1.1.0 | 2026-10-26 | Agents use the guide from its repository link with no clone: `guide-index.json`, `sections/` and `routes/` (one fetch per route), `npx skills add` for `/grill`, `/prompt` and `/guide`, `/guide`'s remote mode; plus the offline suite in CI, CodeRabbit config and GitHub Pages (PRs #1 to #5) |

## Playbook (`playbook/agent-harness-playbook.md`)

| Version | Date | What changed |
|---|---|---|
| 0.1–0.3 | — | First draft; research sections; Templates A–M; the fact-check; hardened Templates F, G and M |
| 0.4 | — | Contents, find-it-fast, the page map as a table, a template index, Read-when notes, page-term aliases, Build-it-first Laws, a text version of the §3 diagram, and corrected Google-study wording. Independent review: PASS |
| 0.5 | 2026-10-24 | Fixes from the [v0.3 fact-check review](../issues/reviews/playbook-factcheck-v0.3.md): the Stop gate is protected by an `Edit` deny rule and leaves a `.gate-failed` marker on give-up; a guardrails block for irreversible actions; a RISK switch in Template B; 23 corrected claims and six caveats; §0 and §19 link the review as their evidence. Checks: `bash -n` and `shellcheck` on both hook scripts, a YAML parse of Template M, a scripted give-up test |
| 0.6 | 2026-10-27 | Evidence additions from a review of a workshop's advice on running coding agents, cut to the rule under each finding: generated context files (§8); a hidden acceptance check, LLM-judge bias and over-mocking (§9.3); mined lessons, reviewed skills and hand-labelled failures (§13); approval fatigue, merge rate, flaky tests, dark launches and restore tests (§18); a prior-art rule (§5.4); UTBoost, Cursor adoption, skill formation and Intercom (§19); follow-on qualifiers in Laws 2, 5 and 8, §14 and §19; router rows 9, 10, 14 and 16; one clause in four runbooks. Evidence: [research/mega-workshop-evidence.md](../research/mega-workshop-evidence.md). Checks: six `doc-checker` passes on every claim and number (20 playbook claims: 9 confirmed, 10 partial, 1 wrong, all reworded to match the source), a one-off tag-to-source check, `tests/run.sh`, the mutation suite. Independent review: pending |
