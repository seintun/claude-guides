# Proposal: reset the harness to a lean baseline (v2)

Status: draft v2, revised after adversarial review. Date: 2026-10-24. Risk: **high**, because it touches `settings.json` permissions and hooks. Playbook references use § numbers from `agent-harness-playbook.md`.

This proposal describes a personal Claude Code harness in general terms. The counts come from one example harness; replace them with your own.

## 0. What changed from v1, and why

An adversarial reviewer checked v1 against the real `~/.claude`, an earlier friction audit and an earlier incident record. Three objections held up, and I verified the key facts myself:

| v1 claim | What is true | Verified by |
|---|---|---|
| Drop the 97 ask rules; the sandbox covers them | 49 guard cloud and infrastructure writes, which run *inside* the sandbox with no prompt (`autoAllowBashIfSandboxed: true`, cloud API hosts allowed). 17 guard harness self-edits, 13 guard password-manager commands, 8 guard browser credentials and uploads. The friction audit had already proposed and withdrawn this cut | The user `settings.json`; classifying the 97 rules by pattern |
| Tracker friction comes from the client rule firing outside client work | All of the tracker prompts came from sessions in the client project. Moving the gate removes none of them, and it would leave the client workspace ungated from every other folder | The prompt log, grouped by project |
| The git hook script can be archived | The `pre-push` and `pre-commit` hooks in the harness repo link to it; it runs a secret scanner before the harness repo is pushed to GitHub. Archiving it disables that silently | `ls -l` on the repo's `.git/hooks` |

Also kept, per the reviewer's evidence:
- The gate scripts and their shared library stay global, because other projects and several `bin/` tools use them.
- The destructive-command guard hook stays.
- The `autoMode` block stays global, because the classifier ignores project settings.

**Lesson:** the security floor is not where the bloat is. The bloat is in the workflow layer (skills, agents, rules, docs, plugins). The prompts mostly come from the security floor doing its job, plus time spent working on the harness itself.

## 1. Problem (restated)

1. **Cognitive and maintenance load.** There are 13 skills, 7 agents, 7 rules, 83 docs and 13 plugins, and a rigid, client-shaped discovery skill. None of it fits a report, a decision or a non-product project.
2. **Interruptions.** These come from the harness's prompt log (since 2026-10-11, questions excluded):

| Count | Source | Project group | Root cause |
|---|---|---|---|
| 301 | Tracker writes | client | The client write policy, posting item by item |
| 113 | `run_in_terminal` | other, harness | The agent running commands in the user's terminal, outside the sandbox |
| 105 | Chrome `javascript_tool` | other | An ask rule on the user's real browser |
| 76 | `Edit` | harness | Self-edit asks while working on the harness |
| 63 | `Bash` | client, other | Mixed |
| 21 | Scheduled-task updates | other | An ask rule (it persists past the session) |

## 2. Principles (with sources)

| Principle | Source |
|---|---|
| Every component names the failure it prevents | Anthropic, Building effective agents [P]; Law 1 |
| Add instructions only from observed failures | Anthropic, Effective context engineering [P]; Law 8 |
| Instruction files are a short map | OpenAI Codex harness engineering [P]; Thoughtworks Radar Vol. 34 [P]; §19.1 item 8 |
| Enforce at the tool and OS boundary; prose is not a control | Claude Code hooks, sandbox and permissions docs [P]; Law 9 |
| External verification beats self-critique | MAST [R: NeurIPS 2025]; Huang et al. [R: ICLR 2024]. This proposal is the example: v1's self-check missed all three objections |
| A new guard names an incident, or removes an older guard | Your own rule: freeze the harness until the review date |

## 3. Scope

**Untouched (the security floor):**
- the sandbox config
- all 217 deny rules
- the 88 security ask rules (cloud and infrastructure, harness self-edit, password manager, browser credentials and uploads)
- the destructive-command guard
- the gate scripts: the Stop gate, the tracker-status gate, the PR-text gate and the green-stamp helper
- the git hook script that runs the secret scanner, with the pre-push wrapper
- the `autoMode` block
- the hook that denies edits in a primary checkout

**Reset (the workflow layer):**

| Layer | From | To |
|---|---|---|
| Workflow skills | The six multi-stage skills (discovery, shaping, build, next-task, wrap-up and a planning-file skill) | `/brief` (draft in §7). Planning and building use built-in plan mode and `/goal` |
| Agents | 7 | An adversarial reviewer and a doc checker. Archive the planner, audit reader, release verifier, plan reviewer and config auditor only after the dependency check in step 3 |
| Rules | 7 files | 3 files: the review-tier rule (trimmed), the client-tracker-write rule and the web-research rule. Fold the grilling rule into `/brief`; fold the model-role, scratch-file and worktree rules into one line each in CLAUDE.md, or drop them |
| CLAUDE.md | 34 lines | 25 lines or fewer, as a map |
| Plugins | 13 | 6: a docs lookup, a web search, a browser driver, a security-guidance plugin, one skills pack, and a prose-style plugin (your choice). Disable the rest; re-enable on need |
| Hooks to archive | n/a | The session-digest hook (it only feeds the next-task and wrap-up skills), after the step 3 dependency check |
| Docs | 83 | Move dated session notes to `docs/archive/`; keep the design docs and incident docs |

**Targeted friction fixes (each is a separate decision; see §8):**
- **F1, tracker writes (301).** Batch client writes: post once per task, as the client-tracker-write rule already says, and have `/brief` and the hand-off collect them. Option: let label writes skip the ask when the hook's scan passes (72 prompts).
- **F2, `run_in_terminal` (113).** Find out why the agent leaves the sandbox. If it is working around sandbox denials, fix the denial at its source (allowlist the host or path) instead of using the terminal.
- **F3, Chrome JS (105).** Default to the built-in browser, which has no ask rule, and keep the Chrome ask.
- **Harness Edit (76).** No change. These prompts guard against an earlier incident, and a leaner harness means less harness editing.

## 4. Migration plan

Every step is a commit on a branch, `harness-reset`, in `~/.claude`. `main` stays untouched until the soak passes, so restoring is a branch switch. Steps go from lowest risk to highest. Run the canaries (§5) after every step, and stop at the first failure.

| Step | Change | Risk | Canary after |
|---|---|---|---|
| 0 | Pre-flight backup (§6.1) | None | Backup files exist |
| 1 | Disable 7 plugins | Low | C1, C6 |
| 2 | Add `skills/brief`; move the 6 workflow skills to `archive/skills/` | Low | C1, C7 |
| 3 | Dependency check: `grep -rn` each agent, hook and bin name across skills, hooks, bin and settings. Archive only names with zero references | Low | Grep output is clean |
| 4 | Archive the cleared agents and the session-digest hook (and remove its settings entry) | Medium | C1 to C6 |
| 5 | Trim rules and CLAUDE.md | Low | C1, C7 |
| 6 | Archive dated docs | None | n/a |
| 7 | Friction fixes F1 to F3, one commit each, only those approved | Medium | C1 to C6 |
| 8 | Soak: 7 days of real work on the branch | n/a | Daily C1; prompt-log count at day 7 |
| 9 | Merge the branch into `main` and push (the pre-push secret scan runs) | Low | C5 |

## 5. Canaries (pass or fail, run from a new session)

| ID | Check | Pass means |
|---|---|---|
| C1 | A new session starts with no hook or plugin errors (`claude --debug` or the Desktop log) | Clean start |
| C2 | `cat ~/.ssh/id_ed25519` and `cat .env` | Both denied |
| C3 | `aws s3 rm s3://canary-nonexistent --recursive` in a client project | Ask prompt shown (decline it) |
| C4 | A tracker write from a scratch folder | Denied by the tracker-status gate |
| C5 | Push a throwaway commit with a fake key to a scratch branch of `~/.claude` | Blocked by the secret scanner |
| C6 | Edit `~/.claude/settings.json` | Ask prompt shown (decline it) |
| C7 | `/brief` on a sample report idea | Asks one question at a time, writes `brief.md`, calls the reviewer, stops at the gate |

## 6. Restore plan

### 6.1 Pre-flight (step 0)

Back up what git does not track: the git hook links, the Codex config, the client project's settings and the plugin state. Keep the tarball local and never commit it; `~/.claude.json` can hold tokens.

```bash
cd ~/.claude && git status --short
```

```bash
cd ~/.claude && git add -A && git commit -m "chore: snapshot before harness reset" && git tag pre-reset
```

```bash
tar -czf ~/harness-backup.tgz -C ~ .claude/.git/hooks .codex/config.toml .claude.json <client-project>/.claude/settings.json <client-project>/.claude/settings.local.json
```

In the last command, replace `<client-project>` with the path of the client project, relative to your home directory.

```bash
cd ~/.claude && git switch -c harness-reset
```

Review the first command's output before committing: dirty files may include memory files.

### 6.2 When to abort

Restore if any of these happen:
- A canary fails, and the fix is not obvious within 15 minutes.
- A session will not start, or a hook errors on every tool call.
- A client gate stops firing (C3, C4 or C5).
- The day-7 count of non-question interruptions is higher than before.

### 6.3 Restore one step

Each step is one commit, so undo that commit and keep the others:

```bash
cd ~/.claude && git log --oneline main..HEAD
```

```bash
cd ~/.claude && git revert --no-edit <step-commit-sha>
```

Then rerun the canary that failed.

### 6.4 Restore everything (`main` is untouched)

```bash
cd ~/.claude && git switch main
```

The branch stays for later inspection. If plugins, git hooks, the Codex config or the client project's settings drifted, restore them from the tarball:

```bash
tar -xzf ~/harness-backup.tgz -C ~
```

Then restart the Desktop app and run C1 to C6.

### 6.5 Restore after merge (if a problem appears later)

```bash
cd ~/.claude && git revert --no-edit -m 1 <merge-commit-sha>
```

The tag `pre-reset` always marks the last known-good state:

```bash
cd ~/.claude && git diff pre-reset --stat
```

## 7. `/brief` skill (draft)

```markdown
---
name: brief
description: Turn a brain-dump about any project, report, decision or task into a reviewed brief.md before work starts. Use when the user says "/brief", "write a brief" or "frame this before we start". Not for plans or code.
---

# /brief

1. **Orient.** Read the dump and any files it names. Look up facts yourself; never ask the user for one.
2. **Grill to the bar.** Ask about empty or weak fields only, one question per message with AskUserQuestion: 2 to 4 options, recommended first, reasoning in each option. Stop when every field meets its bar and the user confirms.

| Field | Bar |
|---|---|
| Problem | What happens today, to whom, what it costs. No solution |
| Outcome | One sentence, the end state |
| Done when | A command, a number with a date, or a numbered acceptance list |
| Constraints and out of scope | What must not change; what is left out |
| Riskiest assumption | What sinks it if wrong; the cheapest test |
| Stop and ask if | Irreversible or ambiguous cases |

   A field the user cannot answer reads `UNKNOWN: <why>`. Never invent one.
3. **Write** the brief where the project's CLAUDE.md says, otherwise `./brief.md`. If one exists, ask before overwriting it.
4. **Fresh review.** Send `adversarial-reviewer` the brief and the bar only. Bring its top 3 objections to the user with your recommendation; revise where they agree.
5. **Gate.** Show the final brief. Only a typed yes in chat approves it. Then suggest the next step (plan mode, or the project's own command) and stop. Do not plan or build.
```

## 8. Open decisions

| # | Decision | Recommendation |
|---|---|---|
| D1 | Accept v2's scope: security floor untouched, workflow layer reset | Yes |
| D2 | F1: let label writes skip the ask after a passing scan | Decide after reading the tracker policy file. Client data, so high risk |
| D3 | F2: investigate `run_in_terminal` use before changing anything | Yes, read-only |
| D4 | F3: default to the built-in browser over Chrome | Yes |
| D5 | Who applies it: a sandboxed session may not be able to write `~/.claude` | You, from a session opened in `~/.claude`, following §4 step by step |

## 9. What the reset will and will not do

- **Will:** cut the workflow surface from 13 skills to `/brief` and from 13 plugins to 6, give you one universal starting skill, and shrink CLAUDE.md to a map.
- **Will not by itself:** remove most prompts. Most of them are the security floor working. The prompt count drops only through F1 to F3 and through less time spent editing the harness. Day-7 target: 30% fewer non-question interruptions. It is a target, not a promise.
