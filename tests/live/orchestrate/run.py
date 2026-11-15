"""Live eval of /orchestrate: fresh claude -p sessions route labelled tasks, and code scores the result.

Each run builds a throwaway project (a README and placeholder files) under build/test-tmp/orchestrate/,
sends the skill's text with the case's request as $ARGUMENTS, and records the stream-json transcript.
score() then checks, with code only:
  s-0  the session finished: the CLI exited 0 within the time limit and wrote a result (a failure here is a run
       error, such as a signed-out CLI, not a routing failure)
  s-1  it started nothing: no Agent, Task, Write, Edit, NotebookEdit or Workflow call, and no Bash command
       with a redirect, -delete or -exec
  s-2  it routed in 5 tool calls or fewer (SKILL.md step 1)
  s-3  it ends with the exact line "Go, or change the route?"
  k-*  the card passes skills/orchestrate/check_card.py, including k-10 (the expected route) and k-11 (what
       route.py says that route requires, from the case's facts)

This costs model usage, roughly $0.05 to $0.20 per run with Sonnet.
Usage: python3 -I tests/live/orchestrate/run.py                      every case once, Sonnet
       python3 -I tests/live/orchestrate/run.py --k 2 --model haiku  every case twice on Haiku
       python3 -I tests/live/orchestrate/run.py --only add-mfa,readme-audit
       python3 -I tests/live/orchestrate/run.py --rescore <work dir> score saved transcripts again
       add --record to append one line per run to tests/results/orchestrate-live.jsonl
Needs the claude CLI, signed in.
"""
import argparse
import concurrent.futures as cf
import datetime
import importlib.util
import json
import pathlib
import re
import shutil
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[3]
HERE = pathlib.Path(__file__).resolve().parent
SKILL = ROOT / "skills" / "orchestrate" / "SKILL.md"
RESULTS = ROOT / "tests" / "results" / "orchestrate-live.jsonl"
SCENARIOS = json.loads((HERE / "scenarios.json").read_text(encoding="utf-8"))["scenarios"]
GO = "Go, or change the route?"
# A Bash command that writes: a redirect into a file, find -delete or -exec, tee, rm, mv, cp, touch, mkdir.
# Redirects to /dev/null and descriptor copies (2>&1) are removed before this runs.
WRITES = re.compile(r">|\s-delete\b|\s-exec\b|\b(?:tee|rm|mv|cp|touch|mkdir)\b")
STARTS_WORK = {"Agent", "Task", "Write", "Edit", "MultiEdit", "NotebookEdit", "Workflow"}
TOOLS = "Read,Grep,Glob,Bash(ls:*),Bash(cat:*),Bash(wc:*),Bash(head:*)"

spec = importlib.util.spec_from_file_location("check_card", ROOT / "skills" / "orchestrate" / "check_card.py")
check_card = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_card)


def skill_prompt(request):
    text = SKILL.read_text(encoding="utf-8")
    body = text.split("---", 2)[2]
    return body.replace("$ARGUMENTS", request)


def build_project(case, folder):
    if folder.exists():
        shutil.rmtree(folder)
    (folder / "project").mkdir(parents=True)
    (folder / "project" / "README.md").write_text(case["readme"], encoding="utf-8")
    for pattern, count in case.get("stubs", {}).items():
        for n in range(1, count + 1):
            path = folder / "project" / pattern.format(n=n)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"// placeholder {n}\n", encoding="utf-8")


def run_one(case, model, folder):
    build_project(case, folder)
    start = time.time()
    cmd = ["claude", "-p", skill_prompt(case["request"]), "--model", model, "--strict-mcp-config", "--disable-slash-commands",
           "--allowedTools", TOOLS, "--output-format", "stream-json", "--verbose"]
    with open(folder / "transcript.jsonl", "w", encoding="utf-8") as out:
        try:
            proc = subprocess.run(cmd, cwd=folder / "project", stdout=out, stderr=subprocess.PIPE, text=True, timeout=600)
            code, err = proc.returncode, proc.stderr or ""
        except subprocess.TimeoutExpired:
            code, err = "timeout", "timed out after 600 s"
    (folder / "stderr.txt").write_text(err, encoding="utf-8")
    (folder / "exit.txt").write_text(str(code), encoding="utf-8")
    return time.time() - start


def score(case, folder):
    tools, bash, final, cost, turns, got_result = [], [], "", None, None, False
    for line in (folder / "transcript.jsonl").read_text(encoding="utf-8").splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "assistant":
            for block in ev.get("message", {}).get("content", []):
                if block.get("type") == "tool_use":
                    tools.append(block.get("name"))
                    if block.get("name") == "Bash":
                        bash.append(str(block.get("input", {}).get("command", "")))
        if ev.get("type") == "result":
            final = ev.get("result") or ""
            cost, turns, got_result = ev.get("total_cost_usd"), ev.get("num_turns"), True
    (folder / "card.txt").write_text(final, encoding="utf-8")
    exit_file = folder / "exit.txt"
    code = exit_file.read_text().strip() if exit_file.exists() else "0"
    writing_bash = [c for c in bash if WRITES.search(re.sub(r"\d?>\s*/dev/null|\d?>&\d", "", c))]
    lines = [l.strip().strip("`*_ ") for l in final.strip().splitlines() if l.strip().strip("`*_ ")]
    last = lines[-1] if lines else ""
    checks = [("s-0", code == "0" and got_result, f"exit {code}, result event {'present' if got_result else 'missing'}"),
              ("s-1", not (set(tools) & STARTS_WORK) and not writing_bash, f"tools used: {tools}" + (f"; writing Bash: {writing_bash}" if writing_bash else "")),
              ("s-2", len(tools) <= 5, f"{len(tools)} tool call(s)"),
              ("s-3", last == GO, "ends with the go line" if last == GO else f"last line is not '{GO}': {last[:60]}")]
    checks += check_card.check(final, expect=case["expect"], accept=tuple(case.get("accept", [])), risk=case.get("risk"), facts=case["facts"])
    route = check_card.route_number((check_card.parse(final) or {}).get("Route", []))
    return {"case": case["id"], "route": route, "expect": case["expect"], "pass": all(ok for _, ok, _ in checks),
            "run_error": not (code == "0" and got_result),
            "failed": [f"{cid} {msg}" for cid, ok, msg in checks if not ok], "tools": len(tools), "cost_usd": cost, "turns": turns}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--k", type=int, default=1)
    ap.add_argument("--only", default="")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--work", default=str(ROOT / "build" / "test-tmp" / "orchestrate"))
    ap.add_argument("--rescore", default="")
    ap.add_argument("--record", action="store_true")
    a = ap.parse_args()
    cases = [c for c in SCENARIOS if not a.only or c["id"] in a.only.split(",")]
    work = pathlib.Path(a.rescore or a.work) / ("" if a.rescore else f"{a.model}-{datetime.datetime.now():%Y%m%d-%H%M%S}")
    jobs = [(c, work / f"{c['id']}-{i + 1}") for c in cases for i in range(a.k)]
    if not a.rescore:
        with cf.ThreadPoolExecutor(a.jobs) as pool:
            list(pool.map(lambda j: run_one(j[0], a.model, j[1]), jobs))
    rows = [dict(score(c, f), run=f.name, model=a.model) for c, f in jobs if (f / "transcript.jsonl").exists()]
    for r in rows:
        print(f"{'PASS' if r['pass'] else 'FAIL'} {r['run']:<24} route {r['route']} (want {r['expect']}) tools {r['tools']} "
              f"${(r['cost_usd'] or 0):.3f}" + ("" if r["pass"] else f"  {'; '.join(r['failed'])}"))
    by_case = {}
    for r in rows:
        by_case.setdefault(r["case"], []).append(r["pass"])
    pass_all = sum(all(v) for v in by_case.values())
    errors = sum(r["run_error"] for r in rows)
    if errors:
        print(f"RUN ERRORS {errors}: these failed before routing (CLI exit or timeout), not on the skill")
    print(f"SUMMARY {sum(r['pass'] for r in rows)}/{len(rows)} runs pass; {pass_all}/{len(by_case)} cases pass every run "
          f"(pass^{a.k}); ${sum(r['cost_usd'] or 0 for r in rows):.2f}; work dir {work}")
    if a.record:
        with open(RESULTS, "a", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(dict(r, date=f"{datetime.date.today()}")) + "\n")
    return 0 if all(r["pass"] for r in rows) else 1


if __name__ == "__main__":
    sys.exit(main())
