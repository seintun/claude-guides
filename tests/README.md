# Tests

This repository is a guide that other sessions call. A bad edit here misleads every session that uses it. These tests keep its parts working, and they catch the changes that would quietly derail it:
- a deleted or renumbered playbook section;
- a router row that points nowhere;
- a skill that stalls or reads the whole playbook;
- a template that leaks a secret;
- a personal path in a public file.

## Run them

| Layer | Command | Cost | When |
|---|---|---|---|
| Offline suite | `tests/run.sh` (add `-v` for every test) | under 10 seconds, no network | Before every commit. The pre-commit hook runs it, and GitHub Actions runs it on every pull request and every push to `main` ([.github/workflows/tests.yml](../.github/workflows/tests.yml)). CI has no `.privacy-terms`, so it checks only the built-in privacy rules |
| Mutation suites | `python3 -I tests/mutation/mutate.py --record` (23 edits) and `python3 -I tests/mutation/review_edits.py --record` (75 edits from the independent review and the /prompt plans) | a few minutes each, no network | After changing a test, a check or a guarded file |
| Live routing | `python3 -I tests/live/route_scenarios.py --record` | about $0.20 a run (3 runs by default) | After changing ENTRY.md, a skill, the snippet or the prompt |
| Live grill | `skills/grill/test.sh` | one short session | After changing `/grill` |
| Grill-then-prompt dry run | Agent-run: see [live/grill-prompt/README.md](live/grill-prompt/README.md) | 6 runner agents and 1 judge | After changing the rules in `/grill` or `/prompt` |
| Browser checks | `checks/run-dom.js` and `checks/compendium-check.js` through Playwright; see [checks/README.md](../checks/README.md) | a headless browser | After changing the page or the compendium builder |
| Metrics | `python3 -I tools/metrics.py --write --record` | about 3 seconds | When you want the numbers in [docs/metrics.md](../docs/metrics.md) refreshed |

To make the offline suite a commit gate in your clone, run this once. Skip it if you already use a global `core.hooksPath`, because it would replace that for this clone.

```bash
git config core.hooksPath .githooks
```

## What each feature is tested by

`python3 -I tests/catalog.py` lists every test case with the failure it guards against.

| Feature | Fails if… | Tests | Scenarios |
|---|---|---|---|
| Playbook, the source of truth | a section, law or template disappears, is renamed or moved; a §20 source is dropped; graded claims or lines are mass-deleted; an in-file anchor breaks | [test_playbook.py](test_playbook.py), against [baselines/playbook.json](baselines/playbook.json) | Hard invariants (§0–§20, 3A, 17A, Laws 1–10, Templates A–M) plus the recorded baseline |
| ENTRY.md router | a scenario's row is deleted or renumbered; a row drops a section, template or runbook; a row has no scenario; a thin row stops naming its gap; a route points at the whole playbook | [test_router.py](test_router.py), `tools/check_entry.py` | [scenarios/routing.json](scenarios/routing.json): 18 requests, one per row |
| `tools/section.py` | an id kind stops resolving; a section runs on into the next; an unknown id passes | [test_router.py](test_router.py) | `9.5`, `17A`, `F`, `law-7`, `cs:3`, `99.9` |
| `/guide`, the snippet and the prompt | the skill gets a pre-run shell line again (it stalled `claude -p`); it stops pointing at ENTRY.md or `section.py`; the snippet becomes an `@` import or more than one line; the installer writes outside its symlink, overwrites a real folder, leaves `{{GUIDE}}` unfilled, or misreads the root when a git hook in a worktree sets `GIT_DIR` | [test_skills.py](test_skills.py); live: [live/route_scenarios.py](live/route_scenarios.py) | The installer runs against a throwaway `HOME`; live runs use the routing scenarios |
| `/grill` | a rule disappears from the skill, including open fact questions, the problem and riskiest assumption, and the `ASSUMED` and `UNKNOWN` markers; the transcript checker passes a bad grill | [test_skills.py](test_skills.py), with [fixtures/grill/](fixtures/grill/) | 9 recorded transcripts, good and bad: asks a known fact, two questions, no recommendation, writes a plan, and more |
| `/prompt` | it starts doing the task, writes into the user's project, runs on its own, loses one of its 32 rules or a consistency-pass check, or runs its checks out of order (consistency pass, `check_prompt.py`, fresh review, then save); its scorer misgrades a draft; `check_prompt.py` misses a merged UNKNOWN line, a relative term, a missing "not ready", an untraced figure, a figure marked twice or a check resting on an UNKNOWN, or misreads inline part labels or bulleted checks; a saved prompt could be committed | [test_prompt_skill.py](test_prompt_skill.py) with [fixtures/prompt/](fixtures/prompt/), [test_critical.py](test_critical.py); live, opt-in: [live/prompt/](live/prompt/) (A/B battle test, rubric, interview check), recorded in [results/prompt-battle.json](results/prompt-battle.json) | 6 scenarios: feature, bug fix, overnight loop, research with helpers, refactor, migration |
| Templates F, G and M | a hook script stops parsing or linting; the Stop hook stops blocking or stops leaving `.gate-failed`; Template M lets Bash write to the PR, loses the secret scrub or uses `pull_request_target`; Template F's deny rule turns into a rule that never matches | [test_templates.py](test_templates.py) | The Stop hook runs 4 failing stops and a passing one, in temp folders |
| Wiki runbooks | a runbook disappears or loses Steps, Checklist, Templates, Watch out for or Go deeper; it stops linking the playbook; the wiki index misses a page | [test_docs.py](test_docs.py) | All runbooks, plus the case study |
| Maps and rules | `llms.txt` points at a missing file or misses a page or skill; AGENTS.md drops "the playbook wins" or the privacy rule; ENTRY.md stops saying never load the whole playbook; a folder loses its README | [test_docs.py](test_docs.py), `tools/check_links.py` | |
| Generated files | the page or a source document changes, but `site/index.html` or the compendium is not rebuilt; the compendium starts loading from the network | [test_generated.py](test_generated.py), `checks/static.sh` | |
| Privacy | a personal path, email, session id or private term lands in a tracked file | `tools/check_privacy.py` | Terms of your own go in the git-ignored `.privacy-terms` |
| The test machinery itself | a checker always exits 0; `run.sh` ends in `exit 0` or skips the unit tests; the commit hook stops running the suite; a test file is deleted or the test count drops | [test_harness.py](test_harness.py), against [baselines/suite.json](baselines/suite.json) | Each checker is fed a known-bad input; a canary copies the clone, plants a leak and expects `run.sh` to fail |
| The guide's meaning | a section is hollowed out under its heading; a grade is promoted or stripped; `section.py` cuts a section short; Template B loses STOP AND ASK; Law 7 or Law 9 is flipped; ENTRY's rules or a row's meaning change; a deny rule disappears; the layers disagree on exit codes or NOT RUN; `/guide` asks for more tools; the installer touches more than its symlink; the compendium phones home | [test_guardrails.py](test_guardrails.py), [test_critical.py](test_critical.py), per-section words and grades in [baselines/playbook.json](baselines/playbook.json) | Exact-phrase pins, a 70% word floor per section, an independent re-slice of every section id |
| The teaching page | the artifact contract, a source URL or the visual language breaks; layout, contrast, keyboard or quiz behaviour regresses | `checks/static.sh`; browser: `checks/run-dom.js` | 8 views, from 320 to 1280px, light and dark |

## The tests are tested too

Two mutation suites check that the guards bite. Each starts with a control copy that must pass, then makes one damaging edit per copy and expects `tests/run.sh` to fail there. [mutation/review_edits.py](mutation/review_edits.py) holds the 75 edits from the independent review and later dry runs. It also retries each caught edit after the steps a careful editor would take: rebuilding the generated files, then regenerating the baseline. An edit only counts as caught if it still fails after both. Results are in [results/review-edits.json](results/review-edits.json).

[mutation/mutate.py](mutation/mutate.py) copies the clone into `build/test-tmp/` and makes one catastrophic edit per copy. Then it runs `tests/run.sh` there and expects a failure. The 23 edits include deleting a playbook section or template, renaming a law, truncating the playbook, dropping a source, deleting or breaking a router row, telling sessions to read the whole playbook, deleting a runbook, committing a personal path, dropping the "playbook wins" or privacy rule, and reintroducing each security bug the fact-check review found. A mutation the suite misses is printed as NOT CAUGHT, which means a guardrail is missing. The clone itself is never edited.

## When a test fails on purpose

Some changes are meant to break a guard. A guard is a contract, so change it in the same commit as the content, and say why in the message.
- **You renamed or removed a playbook section on purpose:** run `python3 -I tests/update_baselines.py` and commit the new baseline. AGENTS.md asks you to keep section numbers stable, so expect the reviewer to ask why. The script refuses to write a baseline that drops a heading or source, shrinks a section below 70% of its words, strips more than 3 grades of one kind, or promotes a grade, unless you pass `--allow-shrink`. That flag shows up in the commit, where a reviewer sees it.
- **You changed a pinned sentence** (in `test_guardrails.py` or `test_critical.py`) on purpose: change its pin in the same commit, and say why.
- **You added a router row:** add its scenario to `scenarios/routing.json`. The router tests require one.
- **You changed a skill's rules:** update its test and run its live test.

## Results

Recorded runs live in [results/](results/):
- `live.jsonl`: one line per live session, with the row it chose, pass or fail, duration, turns, tokens and cost.
- `mutation.json`: the last mutation run. `review-edits.json`: the last run of the 56 review edits.
- `prompt-battle.json`: the `/prompt` battle test: sixteen blind reviews (v1 tied 3 to 3; v2, v3, v4 and v5 won 6 to 0; v5 beat v4 4 to 2; v5 beat the unshipped checker trial (round 9) 11 to 1 and tied v6 6 to 6, v7 tied v6 7 to 5, v7 beat the unshipped v8 11 to 1 and the unshipped v9 7 to 5, each across both position orders), seven contradiction audits and the rubric (v4 scored 67 of 67, against 23 to 24 for a plain request).
- `metrics-history.jsonl`: one snapshot per `tools/metrics.py --record`.

[docs/metrics.md](../docs/metrics.md) is the latest report.
