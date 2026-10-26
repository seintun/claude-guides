"""Live routing test: fresh `claude -p` sessions, outside this repository, route real requests.

Each run takes a scenario from tests/scenarios/routing.json and one way of calling the guide
(the /guide skill, the CLAUDE.md snippet, or the paste-in prompt). It runs a fresh session in
an empty folder under build/test-tmp/live/ and checks three things: the session names the
expected router row (or an accepted alternative), it never reads the whole playbook, and it
ends without an error. It also records duration, turns, tokens and cost.

This costs model usage: about $0.20 a run with Sonnet. The default is 3 runs, one per way.
Usage: python3 -I tests/live/route_scenarios.py                          3 runs, one per way
       python3 -I tests/live/route_scenarios.py --all                    every scenario through every way
       python3 -I tests/live/route_scenarios.py --only stuck-agent,retro --ways skill
       add --record to append the results to tests/results/live.jsonl
Needs the claude CLI, signed in; the skill way needs /guide installed (skills/guide/install.sh).
"""
import argparse
import datetime
import json
import pathlib
import re
import shutil
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]
WORK = ROOT / "build" / "test-tmp" / "live"
RESULTS = ROOT / "tests" / "results" / "live.jsonl"
SCENARIOS = json.loads((ROOT / "tests" / "scenarios" / "routing.json").read_text(encoding="utf-8"))["scenarios"]
DEFAULT = [("stuck-agent", "skill"), ("add-hooks", "snippet"), ("vague-idea", "prompt")]
ASK = ("This is a routing check: do not create or edit any file. "
       "Start your answer with the line ROUTE <row number> for the router row you chose, then give the plan.")


def fill(path):
    return (ROOT / "skills" / "guide" / path).read_text(encoding="utf-8").replace("{{GUIDE}}", str(ROOT)).strip()


def run_one(scn, way, model):
    folder = WORK / f"{way}-{scn['id']}"
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    tools = "Read,Grep,Glob,Bash(python3 -I:*),Bash(git -C:*)"
    if way == "skill":
        prompt, tools = f"/guide {scn['request']} {ASK}", tools + ",Skill"
    elif way == "snippet":
        (folder / "CLAUDE.md").write_text(f"# Demo project\n\nTests: npm test.\n\n{fill('snippet.md')}\n", encoding="utf-8")
        prompt = f"{scn['request']} Use the guide this project's CLAUDE.md points to. {ASK}"
    else:
        prompt = fill("prompt.md").replace("<describe it>", scn["request"]) + "\n" + ASK
    started = time.time()
    # Route only: a request like "set up hooks" would otherwise get built, and a Stop hook it
    # installs can block the session before it answers.
    proc = subprocess.run(["claude", "-p", prompt, "--model", model, "--allowedTools", tools,
                           "--disallowedTools", "Write,Edit,NotebookEdit",
                           "--output-format", "stream-json", "--verbose"],
                          cwd=folder, capture_output=True, text=True, timeout=600)
    (folder / "transcript.jsonl").write_text(proc.stdout, encoding="utf-8")   # kept for inspection; build/ is git-ignored
    wall = time.time() - started
    events = []
    for line in proc.stdout.splitlines():
        try:
            events.append(json.loads(line))
        except ValueError:
            pass
    calls = [c for e in events if e.get("type") == "assistant"
             for c in e.get("message", {}).get("content", []) if c.get("type") == "tool_use"]
    whole = any(c["name"] == "Read" and str(c["input"].get("file_path", "")).endswith("agent-harness-playbook.md")
                and not (c["input"].get("offset") or c["input"].get("limit")) for c in calls)
    result = next((e for e in events if e.get("type") == "result"), {})
    text = result.get("result", "") or ""
    m = re.search(r"ROUTE\s*(?:row\s*)?(\d+)", text, re.I) or re.search(r"\brow\s*(\d+)\b", text, re.I)
    row = int(m.group(1)) if m else None
    usage = result.get("usage", {}) or {}
    ok = row in [scn["row"], *scn.get("also", [])] and not whole and not result.get("is_error", True)
    return {
        "date": datetime.date.today().isoformat(), "scenario": scn["id"], "way": way, "model": model,
        "expected_row": scn["row"], "row": row, "pass": ok, "whole_playbook_read": whole,
        "tool_calls": len(calls), "files_written": sum(1 for f in folder.rglob("*") if f.is_file() and f.name not in ("CLAUDE.md", "transcript.jsonl")), "turns": result.get("num_turns"),
        "duration_s": round((result.get("duration_ms") or wall * 1000) / 1000, 1),
        "cost_usd": round(result.get("total_cost_usd") or 0, 4),
        "input_tokens": usage.get("input_tokens", 0) + usage.get("cache_read_input_tokens", 0) + usage.get("cache_creation_input_tokens", 0),
        "output_tokens": usage.get("output_tokens", 0),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--only", default="")
    ap.add_argument("--ways", default="skill,snippet,prompt")
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--record", action="store_true")
    a = ap.parse_args()
    by_id = {s["id"]: s for s in SCENARIOS}
    ways = a.ways.split(",")
    if a.only:
        plan = [(i, w) for i in a.only.split(",") for w in ways]
    elif a.all:
        plan = [(s["id"], w) for s in SCENARIOS for w in ways]
    else:
        plan = [p for p in DEFAULT if p[1] in ways]
    rows = []
    for sid, way in plan:
        r = run_one(by_id[sid], way, a.model)
        rows.append(r)
        print(f"{'PASS' if r['pass'] else 'FAIL'} {way:7} {sid:18} row {r['row']} (expected {r['expected_row']}) "
              f"{r['duration_s']}s {r['turns']} turns {r['input_tokens']:,} in / {r['output_tokens']:,} out tokens ${r['cost_usd']}"
              f"{' WHOLE PLAYBOOK READ' if r['whole_playbook_read'] else ''}")
    if a.record:
        RESULTS.parent.mkdir(parents=True, exist_ok=True)
        with RESULTS.open("a", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
        print(f"recorded {len(rows)} runs in {RESULTS.relative_to(ROOT)}")
    passed = sum(r["pass"] for r in rows)
    print(f"SUMMARY {passed} of {len(rows)} passed")
    return 0 if passed == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
