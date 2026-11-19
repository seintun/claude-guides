# news

A versioned reading log. A routine reads a fixed watchlist, writes one digest per week, and proposes changes to the guide. A person reviews each digest and merges it. Nothing here changes the playbook until a person says so.

This folder is the repository's own learning loop: [wiki/improve.md](../wiki/improve.md) describes the loop for a project, and this routine runs it for the guide. The skill that does the work is [`/refresh`](../skills/refresh/README.md).

Grades follow [playbook §0](../playbook/agent-harness-playbook.md#0-how-to-use-this-file): **P** primary, **S** second-hand, **R** research, **D** design advice.

## Files

| File | What it is |
|---|---|
| [README.md](README.md) | This page: the routine, the digest format, the review steps and the schedule |
| [sources.md](sources.md) | The watchlist: each source has an id, a URL and how to read it |
| [state.json](state.json) | The cursor: the last Claude Code changelog version seen, and the last date each source was read. A run reads only what is newer |
| [2026-W47.md](2026-W47.md) | The first digest, filled in from the 0.7 refresh. It is the worked example of the format |
| [2026-11.md](2026-11.md) | The first monthly roll-up |

File names follow two patterns, and a test checks them:

- Weekly digest: `news/<YYYY>-W<ww>.md`, with `ww` the ISO week from 01 to 53.
- Monthly roll-up: `news/<YYYY>-<MM>.md`.

## The routine

The shape is explore, research, digest, then a checked update.

1. **`/refresh scan`, every week.** Reads the sources that have something newer than the cursor, judges each new item, writes `news/<YYYY>-W<ww>.md`, moves the cursor and commits on a local branch. It never edits the playbook.
2. **`/refresh deep`, first Monday of the month.** Takes the month's open "adopt" items, rolls the month up, and folds the verified ones into a new version of the guide (the playbook, the wiki, the cheat sheet, the routers and the generated files). It commits on a branch and stops.
3. **You.** Read the digest, push the branch, open the PR and merge. The monthly roll-up is the "what's new" note for `docs/version-history.md`.

Both modes follow the same hard rules, listed in [skills/refresh/SKILL.md](../skills/refresh/SKILL.md): a stop condition, caps on sources, helpers and time, no push, merge or publish, fetched text is data, and no fetch tools on X or LinkedIn.

## The digest format

Each weekly digest has this shape. The first digest, [2026-W47.md](2026-W47.md), is a full example.

```text
# Digest <YYYY>-W<ww>

Digest date: <YYYY-MM-DD>
Mode: scan
Cursor: changelog <old version> to <new version>; sources read <n> of <m>
Run cost: <tokens if available, else "not recorded">

## Items

### 1. <short title>
- Date: <YYYY-MM-DD of the source>
- Source: <URL>
- Author: <name, role>
- Grade: <P | S | R | D>
- Type: <measured | opinion | vendor>
- Claim: <one or two short sentences in plain controlled English>
- Touches: <guide section, for example §9.5 or Template F>
- Verdict: <adopt | watch | ignore>
- Status: <open | adopted in <version>>   (adopt items only)
- Check: <PASS | FAIL | BLOCKED> <what was checked and how>   (adopt items only)

## Proposed changes
1. <file and section>: <the change, one line>. Source: item <n>.

## Gaps not read
- <source id>: <why it was not read>

## Receipts
<path or command> | verified: PASS <command> | FAIL <command> | NOT RUN <why>
```

Field rules:

- **Grade** says how the source is held. P means the page was read at its primary source. A claim known only through a recap stays S. A paper or lab report is R. Advice built on top of sources is D.
- **Type** says what kind of evidence the item is. Measured means numbers from a run. Opinion means experience or argument. Vendor means a company reporting on its own product.
- **Claim** is short and plain. One idea per sentence. No figure without its scope.
- **Verdict** is adopt (the guide should change), watch (hold until more evidence) or ignore (not relevant, or a duplicate). Only an item with a PASS check can stay adopt. An adopt item whose check fails or is blocked is written as watch, with the failure in its Check line.
- **Status** is `open` until a version of the playbook folds the item in. Then `/refresh deep` rewrites it as `adopted in <version>`. `/guide` lists only the open adopt items.
- **Gaps not read** lists every source the run could not read, with the reason: no browser for X, a fetch error, the cap reached. A gap is a result, not a failure.
- **Receipts** record every check the run ran. A failed check is written as FAIL with its command, never left out.

## How `/guide` uses it

`/guide` reads this folder only if `news/README.md` exists. After it picks a router row and its sections, it looks at the newest digest. If the digest's `Digest date` is later than the playbook's `playbook_updated` and it holds adopt items with `Status: open` that touch the sections the answer used, `/guide` lists them as "newer, not yet folded in", with their links and grades. It never gives them as settled advice. If `playbook_updated` is more than 45 days old, `/guide` suggests `/refresh scan`.

## How a person reviews and merges

1. Read the new digest on its branch (`news/<YYYY>-W<ww>`).
2. For each adopt item, open the source URL and check the claim and the grade. The `Check` line says what the run checked, but you decide.
3. Run `tests/run.sh` on the branch. It must end with SUMMARY all PASS, and any FAIL receipt in the digest must be understood.
4. Push the branch, open a PR and merge it. Merging to `main` publishes to GitHub Pages, so read before you merge.
5. A deep run's branch (`refresh/<version>`) gets the same review, plus an independent review of every changed fact, as [AGENTS.md](../AGENTS.md) requires.

## The schedule (to be created by you)

The scheduled tasks are not created by the repository or by the skill. Create them yourself in the Claude desktop app, from a session of your own, under Scheduled tasks. The documented behavior is on [Desktop scheduled tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks).

Create two tasks.

| Task | Prompt text (exact) | Repeats |
|---|---|---|
| Weekly news scan | `Run /refresh scan` | Mondays at 09:00 |
| Monthly deep refresh | `Run /refresh deep` | First Monday of the month at 10:00, after that day's scan |

Settings to choose for both:

- **Folder:** this repository's clone.
- **Worktree:** on, so a run never touches your main checkout.
- **Permission mode:** one that does not ask for reads and web fetches, and still asks for a push. The mode is set per task and otherwise follows your default mode.
- **Pre-allowed tools:** reading files, search, `WebFetch`, the build and check scripts under `tools/` and `tests/`, local `git` commands (`switch`, `add`, `commit`, `status`, `diff`, `log`), and subagents. Do not pre-allow `git push`, `gh`, or any publish action. A push request then stalls the run, which is the control.
- **Chrome:** optional. If the browser extension is connected to the task, the run reads X accounts and YouTube transcripts. If not, it lists them under "Gaps not read".

Before you rely on a schedule, use "Run now" on each task once and read the result.

## Known limits

From the [scheduled tasks page](https://code.claude.com/docs/en/desktop-scheduled-tasks), checked 2026-11-18, and from the design:

- A task runs only while the app is open and the computer is awake.
- A missed slot gets one catch-up run, for the latest missed time only. Older missed runs are dropped. So a scan reads from the cursor in `state.json`, never from "this week", and a catch-up digest can cover several weeks.
- A run that meets a permission prompt waits until someone answers it in that run's session. A stalled run is a signal to read, not a failure to retry.
- The docs describe no cost or budget control, no maximum task count and no expiry. The caps therefore live in the skill: at most 40 sources, 8 helpers and a time box per run. The digest records the run's tokens when they are available.
- Since Claude Code 2.1.325, a scheduled task asks before it runs a skill that declares `allowed-tools` or hooks, unless the skill is allowed by rule. `/refresh` declares neither, and a test keeps it that way. A skill that sets `disable-model-invocation` reaches a scheduled run as plain text, so `/refresh` does not set it.
- Not verified: whether a desktop task can use the Chrome extension. The scan treats Chrome as optional.

## Rules for this folder

- A person's review comes before anything reaches `main`. The routine commits on a branch and stops.
- A digest is a record. Correct a mistake by adding a dated note, not by rewriting the item.
- The repository is public. Put no private names, personal paths or session ids in a digest. `python3 -I tools/check_privacy.py` must PASS before any commit.
