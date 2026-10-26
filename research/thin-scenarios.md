# Research: recipes for the seven thin scenarios

Date: 2026-10-24. Branch: `feat/guide-entry`.

**Method.** For each "(thin)" row in [ENTRY.md](../ENTRY.md) (rows 3, 4, 5, 7, 12, 13, 18), I read the playbook sections the row loads, then searched for primary sources that give a checkable procedure. About 40 sources were fetched and read: 17 Claude Code and Claude Platform doc pages, 2 Anthropic posts, 4 engineering write-ups from large teams (Airbnb, Google, Uber, Spotify), 3 papers, and 9 tool or classic primary works (git, GitHub, Google SRE, Zeller, Feathers, Fowler, Sato, Beck). Every claim below was checked against the page cited. Quotes are under 15 words; the rest is paraphrase. Nothing here has entered the playbook. The lead decides what goes in.

Grades follow playbook §0: **[P]** primary (an author's, vendor's or standard's own words), **[S]** second-hand, **[R]** research paper, **[D]** design advice (our own reasoning, no source says it).

**Caveat.** The Claude Code docs change weekly and several features below carry version floors (for example `onFailure` needs v2.1.295 or later). Re-check each [P: docs] line against the live page before it lands.

---

## 1. Bug fix

**What the playbook says now.** §5.3 says a small fix needs "an issue with a check"; §9.1 maps a criterion to a failing test and gate; §14 lists failure modes (looping on one approach, deleting tests) with countermeasures. There is no reproduce-first, localize or root-cause procedure.

**Primary sources found.**
- Claude Code's own bug-fix recipe is three prompts (share the error, ask for options, apply). Its tips: give Claude the command that reproduces the issue and say whether it is intermittent. [P: common-workflows, "Fix bugs efficiently"]
- Claude Code best practices: "address the root cause, don't suppress the error", and show evidence (the command and its output) rather than asserting success. [P: best-practices, "Give Claude a way to verify its work"]
- Andreas Zeller, *The Debugging Book*: debugging as the scientific method (question, hypothesis, prediction, experiment, repeat), with a written log; each new hypothesis must fit earlier observations. A diagnosis must explain both causality and why the code is wrong. "Fix the problem, not the symptom." After fixing, the failure must be gone and no new failure appear; add a test that catches the bug. [P]
- git bisect: `git bisect run <cmd>` marks a commit good on exit 0, bad on 1 to 127 except 125, skips on 125, and aborts on anything else; `git bisect reset` restores the original HEAD. [P: git docs]
- Agentless (Xia et al.): generate a reproduction test, keep it only if it reproduces the issue on the unfixed code, then keep only candidate patches that pass regression tests and turn the reproduction test from failing to passing. In the ablation, adding reproduction tests raised fixes from 81 to 96 of 300; only 94 generated tests passed with the ground-truth patch, so a reproduction test can itself be wrong. [R: arXiv 2407.01489v2 §3.3, §5.1.3, §5.2.3]

**Proposed recipe.**
1. Reproduce first: write the shortest command or test that shows the failure, run it, and record its output in the issue's Today line. Note whether it is intermittent (run it N times). [P: common-workflows tips; Zeller]
2. Turn the repro into a failing automated test and confirm it fails on the unfixed code for the reported reason, not some other error. [R: Agentless §3.3.1; P: Zeller "A First Fix"]
3. Localize: if a known-good version exists, run `git bisect run <repro-script>` with exit 125 for commits that do not build; otherwise read the stack trace and narrow by experiment. [P: git-bisect]
4. Diagnose in writing before editing: a hypothesis log with each prediction and experiment result, ending in a diagnosis that explains why the failure happens and why the code is wrong. [P: Zeller "Keep a Log", "Checking Diagnoses"]
5. Fix the cause, not the symptom: no special case for the failing input, no suppressed error. [P: Zeller; best-practices]
6. Verify: the repro test now passes, the full suite still passes, and the receipt shows both commands. If the failure persists, return to step 4. [P: Zeller "Fixing the Code"; R: Agentless regression filtering]
7. Keep the repro test in the suite and commit the fix with the diagnosis in the message. [P: Zeller "Commit the Fix"]

**Where it goes.** A new lettered subsection after §9.5, "9.6 Bug fixes: reproduce, localize, diagnose" (no renumbering), linked from the §5.3 "Small fix" bullet and from ENTRY row 3. Summarised in [wiki/verify.md](../wiki/verify.md).

**Unsourced or contested.** No study measures reproduce-first for coding agents beyond Agentless's benchmark ablation. The 94-of-213 figure shows generated repro tests are often wrong, so step 2's "fails for the reported reason" check is our safeguard [D].

---

## 2. Refactor

**What the playbook says now.** §5.3 cites Kent Beck's separation of structural and behavioural changes; §9.3 makes tests immutable to the builder; §18 says to write characterization tests before agents touch untested code. Nothing on slice size, the order of steps or interface changes.

**Primary sources found.**
- Martin Fowler defines refactoring as "a series of small behavior preserving transformations", with the system "kept fully working after each refactoring". [P: refactoring.com]
- Michael Feathers, characterization tests: break dependencies enough to get the code under a test, write an assertion with a placeholder value, run it, paste the actual value in, and rename the test to describe the behaviour. Surprising behaviour is investigated, not "fixed", during this step. [P: Feathers, 2016]
- Kent Beck's agent system prompt: "Never mix structural and behavioral changes in the same commit"; run tests before and after structural changes; commit only when all tests pass. Warning signs: loops, unrequested features, disabled or deleted tests. [P: Beck, June 2025]
- Danilo Sato, Parallel Change: expand (add the new interface next to the old), migrate callers, contract (delete the old). Code can ship in any phase. [P: martinfowler.com, 2014]
- Claude Code's refactor recipe: find legacy usage, get options, apply "while maintaining the same behavior", run the tests; do it "in small, testable increments". [P: common-workflows, "Refactor code"]

**Proposed recipe.**
1. Pin behaviour first: run the existing tests and record the result. Where the code you will touch has no tests, write characterization tests by Feathers' method and commit them alone. [P: Feathers; P: Beck "before and after"]
2. Freeze the tests: the builder may not edit them during the refactor (hook or CODEOWNERS on test paths, as in §9.3). [P: §9.3 harness rule]
3. Plan the slices: each slice is one named transformation (extract, rename, move) small enough to review in one sitting. [P: Fowler "small"; D: the review-size bound]
4. One slice, one commit: apply it, run the full suite, commit only on green, and never mix in a behaviour change. [P: Beck system prompt]
5. For a signature or interface change, use expand, migrate, contract, each as its own slice; delete the old path only when a search shows no callers. [P: Sato; D: the search check]
6. Gate: the reviewer gets the diff and the test diff, and rejects any change to test assertions or any new behaviour. The receipt shows the same test command green before and after. [P: Beck warning signs; D: the reviewer brief]

**Where it goes.** New paragraphs at the end of §9.3, or a new subsection "9.7 Refactors: pin, slice, verify" after the bug-fix one. Template D (plan file) already fits the slice list. Summarised in [wiki/verify.md](../wiki/verify.md).

**Unsourced or contested.** No measured evidence on agents and refactor slice size. Feathers' "investigate surprising behaviour" step needs a human call on whether the behaviour is a bug.

---

## 3. Migration across many files

**What the playbook says now.** §19.1 item 2 gives the evidence (Airbnb per-file state machine, Google's 74.45% figure, Spotify's verifiers, Uber's failed AI batch); §19.3 says "script the pipeline, gate every file, budget for the long tail"; §11.1 and §11.3 give loop guardrails. There is no step-by-step recipe.

**Primary sources found.**
- **Airbnb** (Covey-Brandt): per-file state machine with steps refactor, fix Jest, fix lint and tsc, mark complete; a step advances only after its check passes; each retry gets the latest file and the validation errors. Context of 40K to 100K tokens drawn from up to about 50 related files mattered more than prompt wording. Long tail by "sample, tune, sweep": collect failures, pick 5 to 10 representative files, change the prompt or script, re-run the sample, then re-run everything. 75% done in about 4 hours, 97% after about 4 days, the last 3% by hand. [P]
- **Google** (Ziftci et al., FSE 2025): find references with a code index; sort each location into not-migrated, irrelevant, relevant or left-over; the model edits whole files at temperature 0 with three attempts per file; each file passes six checks ordered cheapest first (success, whitespace, AST parse, "punt" judge, build, test) or is flagged for a human; nightly runs batch passing files into changes that a developer checks and sends to code owners. 39 migrations, 595 changes, 74.45% model-generated; time savings are developer estimates. [R: arXiv 2504.09691 §3.1 to §4.3]
- **Uber** (Mishra and Vejju, 2026): JUnit 4 to 5 with deterministic OpenRewrite recipes; a precondition excludes files the recipe cannot fully handle; per target, a script applies the patch, updates dependencies, builds and runs the tests, and proceeds only if all pass; failing targets were reverted and recipes added; AI batch migration "proved" less practical than deterministic tooling, and AI was kept for debugging failures. 75,000+ test classes, 5,000+ diffs, about 4 months. [P]
- **Anthropic**, "How Anthropic runs large-scale code migrations with Claude Code" (July 2026, no author named): build and validate a judge first (it must pass on the original and fail on broken code); write a rulebook, then a dependency map from a deterministic script, then a gap inventory; stress-test the rules on a small pilot and discard its output; build the work queue from disk so a file's existence marks it done; when a mistake recurs, amend the rulebook and regenerate the batch; then compile, smoke-test and run the parity suite. Bun's port: about 1M lines in under two weeks, roughly $165,000 at API prices. "Let scripts ... be the referee." [P, vendor]
- **Claude Code best practices**, "Fan out across files": write the file list to a file, loop `claude -p` per file with `--allowedTools` and `--permission-mode dontAsk`, refine the prompt on the first 2 or 3 files, then run all; `/batch` splits a change across 5 to 30 worktree subagents. [P: best-practices] Dynamic workflows cap a run at 1,000 agents and advise a small slice first. [P: workflows, "Cost"]
- **Spotify** part 1: the agent replaces the deterministic transformation script inside the existing fleet infrastructure, which opens PRs; formatting, lint and an LLM judge run on each diff. [P]

**Proposed recipe.**
1. Build the referee before any edit: the check that decides a file is done (build, tests, lint, or a parity harness). Prove it passes on the current code and fails on a deliberately broken file. [P: Anthropic migration post]
2. Inventory with a script, not the model: list every target location to a file (code search, an index, or a deterministic query) and tag each one migrate, skip or human. [R: Google §3.1, §3.2; P: best-practices step 1]
3. Write the rules: a short rulebook of before-and-after patterns, plus a list of cases the rules do not cover. Use a deterministic tool (codemod, OpenRewrite) for the patterns it fully covers and send only the rest to the model. [P: Anthropic; P: Uber]
4. Make it a per-file state machine with state on disk: each file records its step and its last check output; a step advances only when its check passes; each retry gets the file and the errors; set a retry cap per step. [P: Airbnb; D: the cap value, from §11.3]
5. Pilot on 2 to 10 representative files, fix the rules or prompt, discard the pilot output, then run the full set breadth-first. [P: best-practices step 3; P: Airbnb; P: Anthropic]
6. Work the long tail by pattern: group the failures, change the rulebook or prompt once per pattern, re-run the sample, then sweep. Stop automating when a sweep moves nothing and hand the rest to a human. [P: Airbnb]
7. Land in batches sized for review: group passing files into PRs the code owners can read; CI reruns the full check; files that still fail are reverted, not merged. [R: Google §3.3; P: Uber]
8. Record cost and yield per sweep (files done, dollars) so the stop decision is a number. [P: Anthropic token figures; D: the per-sweep record]

**Where it goes.** A new lettered subsection after §11.5, "11.6 Migration pipeline recipe", citing §19.1 item 2 for the evidence; Template E already covers the state files. Summarised in [wiki/run-unattended.md](../wiki/run-unattended.md).

**Unsourced or contested.** Uber's failed AI batch versus Airbnb's and Google's success: the difference may be custom patterns and scale, but no source tests that. Google's time savings and Spotify's 60 to 90% are self-reported. The Anthropic post is a vendor write-up of its own runs.

---

## 4. Guard hooks (PreToolUse)

**What the playbook says now.** §9.5 covers Stop-hook behaviour, matcher syntax, and that hooks run with full user permissions; §10.2 "Detect" has one line on a PreToolUse logging hook; Template F covers the Stop gate and notes `onFailure: "block"` has no effect on Stop. There is no guard-hook template or test procedure.

**Primary sources found (all [P: Claude Code docs]).**
- Input: PreToolUse receives `tool_name`, `tool_input` and `tool_use_id` on stdin; for `Write`, `Edit` and `Read`, `tool_input.file_path` "is always absolute". [hooks reference, "PreToolUse input"]
- Exit 2 blocks the call and sends stderr to Claude; exit 2 blocks even if the JSON says allow. Exit 0 with no output is no decision: the call goes through the normal permission flow. [hooks guide, "Hook output"]
- JSON control: `hookSpecificOutput.permissionDecision` is `allow`, `deny`, `ask` or `defer` (`defer` only with `-p`), with `permissionDecisionReason`. A hook's `allow` does not bypass deny or ask rules. [hooks guide; hooks reference, "PreToolUse decision control"]
- A hook's `deny` "blocks the tool even in `bypassPermissions` mode"; PreToolUse fires before any permission-mode check. [hooks guide, "Hooks and permission modes"]
- Several matching hooks run in parallel; the most restrictive decision wins in the order deny, defer, ask, allow; one hook's deny does not stop a sibling's side effects. [hooks guide, "Combine results from multiple hooks"]
- Fail closed: by default a hook that fails or times out lets the action through; `"onFailure": "block"` makes a failure (cannot start, exit other than 0 or 2, timeout, invalid JSON) block instead. Needs v2.1.295 or later. Default timeout is 600 seconds on most events. [hooks reference, "Block the action when a hook fails"]
- Worked example: `protect-files.sh` reads `tool_input.file_path` with `jq`, exits 2 on `.env`, `package-lock.json` or `.git/`, is made executable, and is registered under `PreToolUse` with matcher `Edit|Write`. [hooks guide, "Block edits to protected files"]
- Coverage gap: an `Edit|Write` matcher does not see files changed through Bash; match `Bash|PowerShell` too, or scan the tree in a Stop hook. [hooks guide, "Filter hooks with matchers"]
- The `if` filter on Bash subcommands is best-effort, so the docs say to use permission rules, not a hook, "to enforce a hard allow or deny". [hooks guide]
- Test by piping JSON into the script and checking `echo $?`; confirm registration with `/hooks`; read outcomes in the transcript (`Ctrl+O`) or with `claude --debug-file <path>`. [hooks guide, "Hook error in output", "Check what a hook did"]
- Security list: validate inputs, quote shell variables, block `..` path traversal, use absolute script paths, skip sensitive files. In `-p` and SDK sessions, repo hooks run with no trust dialog. [hooks reference, "Security considerations"]

**Proposed recipe (a candidate Template N).**
1. Decide the layer first: a fixed path or command pattern belongs in a permission deny rule; use a PreToolUse hook only for logic a rule cannot express (content checks, computed paths). [P: hooks guide; §10.2]
2. Write the script to read stdin JSON, extract `tool_name` and `tool_input`, normalise the path, reject `..`, and exit 2 with a one-line reason on stderr; exit 0 otherwise. Quote every variable. [P: hooks guide example; P: security best practices]
3. Register it in `.claude/settings.json` under `PreToolUse` with an exact matcher (`Edit|Write`, plus `Bash` if Bash can reach the same files), an absolute `${CLAUDE_PROJECT_DIR}` path, and `"onFailure": "block"`. [P: hooks guide; P: hooks reference]
4. `chmod +x` the script, then test offline: pipe one JSON sample that must block and one that must pass, and check the exit codes are 2 and 0. Also test fail-closed: rename the script and confirm a call is blocked with the `onFailure` message. [P: hooks guide "Hook error in output"; P: hooks reference test steps]
5. Test live: run `/hooks` to see it listed, ask Claude to touch a protected file, and confirm the `Blocked:` reason in the transcript. [P: hooks guide]
6. Protect the guard: deny edits to the hook script and its settings entry, as Template F does for the Stop gate. [P: Template F's cited permissions docs]
7. Keep logging separate from blocking: a logging hook exits 0 and a guard hook exits 2; both run in parallel. [P: hooks guide "Combine results"]

**Where it goes.** A new Template N, "PreToolUse guard hook", appended after Template M in §16; one new bullet at the end of §9.5 pointing to it; the §10.2 "Prevent" row can cite it. Summarised in [wiki/guardrails.md](../wiki/guardrails.md).

**Unsourced or contested.** The docs' own example matches `.env` as a substring, which also matches names like `.envrc`; a production pattern needs exact matching [D]. A mod can approve a call a hook blocked on machines without managed settings or Team or Enterprise login [P: hooks guide note], so a hook is not a hard boundary there.

---

## 5. Cost blowup

**What the playbook says now.** §18 says to cap fan-outs in the lead's prompt, set `--max-budget-usd` on headless runs, read cost from OpenTelemetry or the Console rather than `/usage`, and write a kill-switch runbook; §11.5 notes no per-session cap for cloud sessions; §11.3 gives loop stop conditions. There is no incident procedure.

**Primary sources found.**
- Find: `/usage` dollars are a local list-price estimate; the Console Usage page is authoritative. On paid plans `/usage` attributes recent usage to skills, subagents, plugins and MCP servers as percentages. [P: costs, "Using the /usage command", "Plan usage breakdown"]
- Find: OpenTelemetry metric `claude_code.cost.usage` (USD) carries `session.id`, `model`, `query_source` (main, subagent, auxiliary), `agent.name` and `skill.name`; the `api_request` event carries `cost_usd`, `agent_id`, `parent_agent_id` and `workflow.run_id`. The docs list cost spikes as an alert to set. Cost metrics "are approximations". [P: monitoring-usage]
- Find, org level: Teams and Enterprise spend reports per user and model; Console dashboard and the Claude Code Analytics API per member; the Usage and Cost API groups by workspace. [P: costs, "Manage costs for your organization"; P: Claude Platform workspaces]
- Known drivers: long context resent each turn, cache misses after a break, session-scoped scheduled tasks firing while idle, subagents and workflows, agent teammates (about 7x tokens in plan mode), compaction. [P: costs, "Why usage climbs in a long session", "Manage agent team costs"]
- Stop: a fixed-interval `/loop` is not stopped by Esc or Ctrl+C; ask Claude to cancel it or use `CronDelete`; `CLAUDE_CODE_DISABLE_CRON=1` stops all session-scoped tasks. A running workflow can be stopped from `/workflows`, usually keeping completed work. [P: scheduled-tasks; P: workflows "Cost"]
- Cap: Console workspace spend limits and alert thresholds; a workspace rate limit can cap Claude Code's share; the Claude Code workspace is the only one with per-user monthly spend limits. [P: Claude Platform workspaces; P: costs "Claude Console"]
- Prevent: `--max-budget-usd` (print mode only) counts subagent spend, stops background subagents at the cap, and can be overshot, so leave headroom; `--max-turns` limits turns. Workflows cap a run at 1,000 agents and warn above 25 agents or 1.5M projected tokens. [P: cli-reference; P: workflows]
- Incident shape: "Stop the bleeding, restore service, and preserve the evidence"; root cause after mitigation; one live incident document; declare early. [P: Google SRE book, "Managing Incidents"]

**Proposed recipe.**
1. Stop the spend first: cancel loops (`CronDelete`, or ask Claude), stop workflows in `/workflows`, end background sessions, disable scheduled or cloud tasks per your §18 kill-switch runbook; if the spend is org-wide, lower the workspace spend or rate limit. Root cause comes after. [P: SRE "Managing Incidents"; P: scheduled-tasks; P: workflows; P: workspaces; D: the order]
2. Preserve evidence before cleanup: note the time window, session ids and any workflow run id in one incident note. [P: SRE "live incident state document"; D: which fields]
3. Read the authoritative number: Console Usage page or the spend report, not `/usage`. [P: costs]
4. Attribute it: in OpenTelemetry, group `claude_code.cost.usage` by `session.id`, then `query_source` and `agent.name` or `skill.name`; drill into `api_request` events by `agent_id` or `workflow.run_id`. Without telemetry, use the `/usage` attribution breakdown. [P: monitoring-usage; P: costs]
5. Match the pattern against the known drivers (idle scheduled tasks, unbounded fan-out, teammates left running, long context, cache misses) and write the cause in the note. [P: costs "Why usage climbs"; D: the matching step]
6. Prevent a repeat with a mechanism, not a sentence: `--max-budget-usd` with headroom and `--max-turns` on every headless run, a workspace spend limit with alerts, a cost-spike alert on `claude_code.cost.usage`, and a fan-out cap in the lead's prompt. [P: cli-reference; P: workspaces; P: monitoring-usage; D: the fan-out cap, from §18]
7. Close with a short retro (Template I) that names the mechanism added. [D]

**Where it goes.** New paragraphs at the end of §18, or a new subsection "18A. Cost incident runbook" after §18 (the playbook already uses lettered ids such as 3A and 17A). Summarised in [wiki/run-unattended.md](../wiki/run-unattended.md); a one-line pointer in [wiki/unstick.md](../wiki/unstick.md).

**Unsourced or contested.** Still no documented per-session dollar cap for cloud sessions or cloud scheduled tasks (no doc found either way, matching §11.5). How fast the Console usage page updates was not checked. The step order is SRE practice applied to spend, not a Claude-specific source.

---

## 6. Work across several repos

**What the playbook says now.** §18's last-but-one bullet: nested CLAUDE.md, affected-tests gates, one plan file per task, and "cross-repo order written into the plan" [D]; §7 gives the brief schema; §12.1 covers Linear as the planning layer. Nothing on access, interface changes between repos, or landing order.

**Primary sources found.**
- `--add-dir` gives Claude read and edit access to other directories but does not discover most `.claude/` configuration there; persist with `permissions.additionalDirectories`. [P: cli-reference] Their CLAUDE.md loads only with `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`. [P: memory, "Load from additional directories"]
- `claude --cloud` "works with a single repository at a time". [P: claude-code-on-the-web]
- Claude Code Projects (public beta, Pro and Max only): "Claude can run a thread per repository, each with its own pull request"; threads pick up each repository's CLAUDE.md but not its skills, `.claude/settings.json` or `.mcp.json`; needs the Claude GitHub App on every repository. [P: claude-projects]
- Parallel Change across separately deployed parts: run old and new side by side so services need no deployment orchestration; for remote APIs, add an endpoint or expand the payload. [P: Sato]
- Fleet-scale evidence is per-repository pipelines: Spotify's fleet infrastructure opens one PR per component; Uber runs a per-target script that builds and tests before generating a diff. [P: Spotify part 1; P: Uber]

**Proposed recipe.**
1. Write one plan file that lists each repo, its change, its check command and the landing order (producer before consumer). [D, from §18]
2. Give access deliberately: one session with `--add-dir` for the other repos, with `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` if their rules matter; or one session per repo (a Projects thread, or a worktree per repo) when each repo needs its own config, hooks and PR. [P: cli-reference; P: memory; P: claude-projects]
3. Change shared interfaces by expand, migrate, contract: land the additive change in the producer first, then move each consumer, then remove the old path. [P: Sato]
4. One PR per repo, each passing that repo's own check; link the PRs from the plan file. [P: Projects "thread per repository, each with its own pull request"; D: the linking]
5. Land in plan order and re-run each consumer's check against the producer as merged, before merging the consumer. [D]
6. Contract only when a search across all repos shows no caller of the old path. [D]

**Where it goes.** Expand the §18 "Monorepos, multiple repos and teams" bullet into a short numbered list at the end of §18 (or inside 18A if the cost runbook goes there; better a separate "18B"). Summarised in [wiki/orchestrate.md](../wiki/orchestrate.md).

**Unsourced or contested.** No primary source measures agent work across repos; landing order and cross-repo checks are our design. Projects is beta and not on Team or Enterprise plans, so it cannot be the default.

---

## 7. Several writers on one codebase

**What the playbook says now.** §7 house rules: one writer per file set, a worktree per builder [D]; §3A notes agent teams have no worktree isolation and `claude -w` creates a worktree; §12.2 already says a merge queue needs CI on `merge_group`. There is no merge or integration step.

**Primary sources found.**
- Worktrees: `--worktree` (or `isolation: worktree` on a subagent) gives each session its own files and branch on shared history; Claude Code blocks edits and git commands aimed at the main checkout; a `cp` or redirect into it is not caught. `-p` runs leave worktrees behind; remove them with `git worktree remove`. [P: worktrees]
- Agent teams: "Two teammates editing the same file leads to overwrites"; give each a different file set. [P: agent-teams, "Avoid file conflicts"]
- Anthropic's parallel C compiler (Carlini, Feb 2026): 16 agents, each in its own container cloning a shared bare repo; an agent claims a task by committing a lock file under `current_tasks/`, and git's push conflict forces a second agent to pick another; on finishing it pulls, merges, pushes and removes the lock. "Merge conflicts are frequent", and agents resolved them. A CI gate was added later because new work kept breaking old features. When every agent hit the same bug they overwrote each other's fixes; adding agents did not help. [P, vendor]
- GitHub merge queue: each queued PR is tested on a temporary branch of the latest base plus the PRs ahead of it; a PR that fails or conflicts is removed and the queue rebuilds; workflows must trigger on `merge_group`. [P: GitHub docs]
- git rerere records a conflict resolution and replays it when the same conflict recurs; enable with `rerere.enabled`; it leaves the index alone, so you still review and `git add`. [P: git docs]

**Proposed recipe.**
1. Partition before starting: the plan file assigns each writer a disjoint file set and a branch. If two tasks need the same file, run them one after the other. [P: agent-teams; D: the sequencing rule]
2. One worktree per writer (`claude --worktree <name>` or `isolation: worktree`), each branched from the same base commit. [P: worktrees]
3. Claim work visibly when writers pick their own tasks: a lock file per task committed to the shared branch, removed on finish. [P: C compiler post]
4. Each writer runs the full check in its worktree and rebases or merges the latest base before handing off; it resolves only conflicts in its own file set and re-runs the check after resolving. [P: C compiler post "pulls, merges, pushes"; D: the own-file-set limit]
5. Integrate one branch at a time through a merge queue (CI on `merge_group`), so each merge is tested against the base plus everything ahead of it. Without a queue, merge in plan order and re-run the full suite after each merge. [P: GitHub merge queue; D: the fallback]
6. When the same failure shows up in several writers, stop the parallel run and give the bug to one writer. [P: C compiler failure mode; D: the stop rule]
7. Clean up: remove merged worktrees and their branches (`git worktree remove`), and release any locks. [P: worktrees "Clean up worktrees"]

**Where it goes.** A new subsection after §7's house rules, as a closing block "Integrating parallel writers" at the end of §7 (no renumbering), cross-linked from §12.2's merge-queue line. Summarised in [wiki/orchestrate.md](../wiki/orchestrate.md).

**Unsourced or contested.** Merge order, the own-file-set conflict rule and the stop rule are design advice. The C compiler post is one vendor experiment on a project with an unusually strong test oracle; its agents resolving their own conflicts may not transfer to codebases with weaker tests. git rerere helps long-lived branches but no source tests it with agents.

---

## Summary

| Gap | Proposed home (playbook, runbook) | Sourced vs [D] steps | Confidence |
|---|---|---|---|
| 1. Bug fix | New §9.6 after §9.5; wiki/verify.md | 7 sourced, 0 [D] (step 2 adds a [D] safeguard) | High |
| 2. Refactor | End of §9.3 or new §9.7; wiki/verify.md | 4 sourced, 2 mixed P and D | Medium |
| 3. Migration | New §11.6 after §11.5; wiki/run-unattended.md | 7 sourced, 1 mixed P and D | High |
| 4. Guard hooks | New Template N after M, bullet at end of §9.5; wiki/guardrails.md | 7 sourced, 0 [D] | High |
| 5. Cost blowup | New §18A after §18; wiki/run-unattended.md, pointer in wiki/unstick.md | 5 sourced or mixed, 1 [D] (retro), order is [D] | Medium |
| 6. Several repos | New §18B (or end of §18); wiki/orchestrate.md | 3 sourced, 3 [D] | Low |
| 7. Several writers | Closing block at end of §7, linked from §12.2; wiki/orchestrate.md | 4 sourced, 3 mixed P and D | Medium |

---

## Sources

All fetched and read on 2026-10-24.

**1. Bug fix**
- [P] Claude Code docs, Common workflows, "Fix bugs efficiently": https://code.claude.com/docs/en/common-workflows#fix-bugs-efficiently
- [P] Claude Code docs, Best practices, "Give Claude a way to verify its work": https://code.claude.com/docs/en/best-practices#give-claude-a-way-to-verify-its-work
- [P] Andreas Zeller, The Debugging Book, "Introduction to Debugging": https://www.debuggingbook.org/html/Intro_Debugging.html#The-Scientific-Method
- [P] git documentation, git-bisect, "Bisect run": https://git-scm.com/docs/git-bisect#_bisect_run
- [R] Xia, Deng, Dunn, Zhang, Agentless (arXiv 2407.01489v2; the playbook's §19.1 cites it as FSE 2025): https://arxiv.org/html/2407.01489v2

**2. Refactor**
- [P] Martin Fowler, refactoring.com: https://refactoring.com/
- [P] Michael Feathers, "Characterization Testing" (2016): https://michaelfeathers.silvrback.com/characterization-testing
- [P] Kent Beck, "Augmented Coding: Beyond the Vibes" (June 2025): https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes
- [P] Danilo Sato, "Parallel Change" (2014): https://martinfowler.com/bliki/ParallelChange.html
- [P] Claude Code docs, Common workflows, "Refactor code": https://code.claude.com/docs/en/common-workflows#refactor-code

**3. Migration**
- [P] Charles Covey-Brandt, Airbnb, "Accelerating Large-Scale Test Migration with LLMs": https://airbnb.tech/infrastructure/accelerating-large-scale-test-migration-with-llms/
- [R] Ziftci et al., "Migrating Code At Scale With LLMs At Google" (FSE 2025): https://arxiv.org/html/2504.09691
- [R] Nikolov et al., "How is Google using AI for internal code migrations?" (experience report; abstract only, no procedure): https://arxiv.org/abs/2501.06972
- [P] Mishra and Vejju, Uber, "How Uber Executed A JUnit Migration at Massive Scale" (2026): https://www.uber.com/us/en/blog/junit-migration/
- [P, vendor] Anthropic, "How Anthropic runs large-scale code migrations with Claude Code" (July 2026): https://claude.com/blog/ai-code-migration
- [P] Claude Code docs, Best practices, "Fan out across files": https://code.claude.com/docs/en/best-practices#fan-out-across-files
- [P] Claude Code docs, Dynamic workflows, "Cost" and "Behavior and limits": https://code.claude.com/docs/en/workflows#cost
- [P] Charas and Bruggmann, Spotify, background coding agent part 1 (Nov 2025): https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1

**4. Guard hooks**
- [P] Claude Code docs, Hooks guide, "Block edits to protected files": https://code.claude.com/docs/en/hooks-guide#block-edits-to-protected-files
- [P] Claude Code docs, Hooks guide, "Hooks and permission modes": https://code.claude.com/docs/en/hooks-guide#hooks-and-permission-modes
- [P] Claude Code docs, Hooks guide, "Combine results from multiple hooks": https://code.claude.com/docs/en/hooks-guide#combine-results-from-multiple-hooks
- [P] Claude Code docs, Hooks reference, "PreToolUse decision control": https://code.claude.com/docs/en/hooks#pretooluse-decision-control
- [P] Claude Code docs, Hooks reference, "Block the action when a hook fails": https://code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails
- [P] Claude Code docs, Hooks reference, "Security considerations": https://code.claude.com/docs/en/hooks#security-considerations

**5. Cost blowup**
- [P] Claude Code docs, Manage costs effectively: https://code.claude.com/docs/en/costs#why-usage-climbs-in-a-long-session
- [P] Claude Code docs, Monitoring, "Cost counter" and "API request event": https://code.claude.com/docs/en/monitoring-usage#cost-counter
- [P] Claude Code docs, CLI reference (`--max-budget-usd`, `--max-turns`): https://code.claude.com/docs/en/cli-reference#cli-flags
- [P] Claude Code docs, Scheduled tasks, "Stop a loop": https://code.claude.com/docs/en/scheduled-tasks#stop-a-loop
- [P] Claude Code docs, Dynamic workflows, "Cost": https://code.claude.com/docs/en/workflows#cost
- [P] Claude Platform docs, Workspaces, "Workspace limits": https://platform.claude.com/docs/en/manage-claude/workspaces#workspace-limits
- [P] Google SRE book, "Managing Incidents": https://sre.google/sre-book/managing-incidents/

**6. Several repos**
- [P] Claude Code docs, CLI reference (`--add-dir`): https://code.claude.com/docs/en/cli-reference#cli-flags
- [P] Claude Code docs, Memory, "Load from additional directories": https://code.claude.com/docs/en/memory#load-from-additional-directories
- [P] Claude Code docs, Claude Code on the web (`--cloud` is single-repo): https://code.claude.com/docs/en/claude-code-on-the-web
- [P] Claude Code docs, Projects (public beta): https://code.claude.com/docs/en/claude-projects#when-to-use-a-project
- [P] Danilo Sato, "Parallel Change": https://martinfowler.com/bliki/ParallelChange.html
- [P] Spotify part 1 and Uber JUnit migration (above)

**7. Several writers**
- [P] Claude Code docs, Worktrees, "How Claude Code enforces isolation" and "Clean up worktrees": https://code.claude.com/docs/en/worktrees#how-claude-code-enforces-isolation
- [P] Claude Code docs, Agent teams, "Avoid file conflicts": https://code.claude.com/docs/en/agent-teams#avoid-file-conflicts
- [P, vendor] Nicholas Carlini, Anthropic, "Building a C compiler with a team of parallel Claudes" (Feb 2026): https://www.anthropic.com/engineering/building-c-compiler
- [P] GitHub docs, "Managing a merge queue": https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue
- [P] git documentation, git-rerere: https://git-scm.com/docs/git-rerere
