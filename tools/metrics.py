"""Success and performance metrics for the guide: tests, speed, tokens, reading time, growth.

Usage: python3 -I tools/metrics.py            print the report (runs tests/run.sh, a few seconds)
       python3 -I tools/metrics.py --write    also write docs/metrics.md
       python3 -I tools/metrics.py --record   also append a snapshot to tests/results/metrics-history.jsonl
       python3 -I tools/metrics.py --no-run   skip running the suite (speed and pass counts left out)

Measures, and where each comes from:
- Success: tests/run.sh pass/fail per step; the mutation suite's catch rate (tests/results/mutation.json);
  live routing pass rate (tests/results/live.jsonl).
- Speed: seconds per step of tests/run.sh; section.py lookup time; live session duration and turns.
- Tokens and efficiency: tokens each router scenario loads (skill + ENTRY.md + its sections, characters / 4)
  against the whole playbook; live sessions' measured tokens and cost.
- Reading time: words / 200 per minute, the same rate tools/lesson_meta.py uses for the page.
- Growth: runbooks, skills, router rows, scenarios, test cases and playbook size at each commit (git history).
"""
import contextlib
import datetime
import io
import json
import pathlib
import re
import statistics
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import section  # noqa: E402

RESULTS = ROOT / "tests" / "results"
WPM = 200


def tokens(text):
    return round(len(text) / 4)


def minutes(text):
    return max(1, round(len(re.findall(r"\w+", text)) / WPM))


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout


def run_suite():
    started = time.time()
    proc = subprocess.run(["bash", "tests/run.sh"], cwd=ROOT, capture_output=True, text=True)
    steps = re.findall(r"^(PASS|FAIL) (.+?) \((\d+\.\d)s\)", proc.stdout, re.M)
    ran = re.search(r"Ran (\d+) tests", proc.stdout)
    skipped = len(re.findall(r"NOT RUN", proc.stdout))
    return {"ok": proc.returncode == 0, "total_s": round(time.time() - started, 1),
            "steps": [(s, name, float(t)) for s, name, t in steps],
            "test_cases": int(ran.group(1)) if ran else 0, "not_run": skipped}


def route_tokens():
    sys.path.insert(0, str(ROOT / "tests"))
    scenarios = json.loads(read("tests/scenarios/routing.json"))["scenarios"]
    entry = read("ENTRY.md")
    rows = {int(m.group(1)): m.group(2) for m in re.finditer(r"^\| (\d+) \| [^|]+\| ([^|]+)\|", entry, re.M)}
    base = tokens(read("skills/guide/SKILL.md")) + tokens(entry)
    out = []
    for s in scenarios:
        ids = re.findall(r"`([^`]+)`", rows[s["row"]])
        ids = [i for span in ids for i in span.split()]
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            section.main(ids)
        out.append((s["id"], s["row"], base + tokens(buf.getvalue())))
    return out


def lookup_ms(n=20):
    ids = ["9.5", "F", "law-7", "cs:3", "17A"]
    started = time.perf_counter()
    for _ in range(n):
        section.index(section.PLAYBOOK)
        with contextlib.redirect_stdout(io.StringIO()):
            section.main(ids)
    return round((time.perf_counter() - started) * 1000 / n, 1)


def growth():
    rows = []
    for line in git("log", "--reverse", "--format=%h %ad", "--date=short").splitlines():
        sha, day = line.split()
        files = git("ls-tree", "-r", "--name-only", sha).splitlines()
        runbooks = [f for f in files if re.fullmatch(r"wiki/(?!README)[\w-]+\.md", f)]
        skills = [f for f in files if f.startswith("skills/") and f.endswith("/SKILL.md")]
        entry = git("show", f"{sha}:ENTRY.md") if "ENTRY.md" in files else ""
        router = len(re.findall(r"^\| \d+ \|", entry.split("## Phase table")[0], re.M)) if entry else 0
        scen = git("show", f"{sha}:tests/scenarios/routing.json") if "tests/scenarios/routing.json" in files else ""
        cases = sum(len(re.findall(r"^\s+def test_", git("show", f"{sha}:{f}"), re.M))
                    for f in files if re.fullmatch(r"tests/test_\w+\.py", f))
        pb = git("show", f"{sha}:playbook/agent-harness-playbook.md").count("\n") if "playbook/agent-harness-playbook.md" in files else 0
        rows.append({"commit": sha, "date": day, "runbooks": len(runbooks), "skills": len(skills), "router_rows": router,
                     "scenarios": scen.count('"id":'), "test_cases": cases, "playbook_lines": pb})
    # Keep the commits where something changed.
    keep, last = [], None
    for r in rows:
        key = tuple(v for k, v in r.items() if k not in ("commit", "date"))
        if key != last:
            keep.append(r)
            last = key
    return keep


def load_jsonl(path):
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def report(run):
    lines = [f"# Guide metrics", "", f"Generated {datetime.date.today().isoformat()} by `python3 -I tools/metrics.py`. Rerun it to refresh; the numbers below are measurements, not targets.", ""]

    lines += ["## Success", ""]
    if run:
        status = "all PASS" if run["ok"] else "FAIL"
        lines += [f"- **Offline suite (`tests/run.sh`):** {status}. {run['test_cases']} test cases, {run['not_run']} not run (a tool missing)."]
    mut = json.loads((RESULTS / "mutation.json").read_text()) if (RESULTS / "mutation.json").exists() else None
    if mut:
        total = mut["caught"] + mut["not_caught"]
        lines += [f"- **Mutation suite:** caught {mut['caught']} of {total} catastrophic changes ({100 * mut['caught'] // total}%), run {mut['date']}."]
    rev = json.loads((RESULTS / "review-edits.json").read_text()) if (RESULTS / "review-edits.json").exists() else None
    if rev:
        rs = rev["results"]
        firm = sum(r["verdict"] == "CAUGHT" for r in rs)
        lines += [f"- **Adversarial review edits:** {firm} of {len(rs)} caught firmly, still failing after the generated files are rebuilt and the baseline regenerated ({100 * firm // len(rs)}%), run {rev['date']}."]
    every_live = load_jsonl(RESULTS / "live.jsonl")
    live = [r for r in every_live if not r.get("note")]   # a note marks a run voided by a harness flaw
    voided = len(every_live) - len(live)
    if live:
        ways = {}
        for r in live:
            ways.setdefault(r["way"], []).append(r["pass"])
        per = ", ".join(f"{w} {sum(v)}/{len(v)}" for w, v in sorted(ways.items()))
        lines += [f"- **Live routing (`tests/live/route_scenarios.py`):** {sum(r['pass'] for r in live)} of {len(live)} runs picked the expected row ({per}). Whole playbook read in {sum(r['whole_playbook_read'] for r in live)} runs."
                  + (f" {voided} more run(s) voided by a test-harness flaw, explained in its note in tests/results/live.jsonl." if voided else "")]
    lines += [""]

    lines += ["## Speed", ""]
    if run:
        lines += ["| Step of `tests/run.sh` | Result | Seconds |", "|---|---|---|"]
        lines += [f"| {name} | {s} | {t} |" for s, name, t in run["steps"]]
        lines += [f"| **Total** | | **{run['total_s']}** |", ""]
    lines += [f"- **Section lookup:** {lookup_ms()} ms to load one playbook index and print 5 sections (`tools/section.py`)."]
    if live:
        lines += [f"- **Live session:** median {statistics.median(r['duration_s'] for r in live)} s and {statistics.median(r['turns'] or 0 for r in live)} turns from request to routed answer ({len(live)} runs)."]
    if mut:
        lines += [f"- **Mutation suite:** {mut['duration_s']} s for {mut['caught'] + mut['not_caught']} mutations."]
    lines += [""]

    pb = read("playbook/agent-harness-playbook.md")
    whole = tokens(pb)
    routes = route_tokens()
    vals = [t for _, _, t in routes]
    lines += ["## Tokens and efficiency", "",
              f"- **Whole playbook:** {whole:,} tokens. A session never loads it; it loads the skill, ENTRY.md and one row's sections.",
              f"- **Per route, all {len(routes)} router scenarios:** median {int(statistics.median(vals)):,} tokens ({100 * statistics.median(vals) / whole:.0f}% of the playbook), smallest {min(vals):,}, largest {max(vals):,}.",
              f"- **Savings:** a median route loads {whole / statistics.median(vals):.1f} times less than the whole playbook."]
    if live:
        lines += [f"- **Live sessions, measured:** median {int(statistics.median(r['input_tokens'] for r in live)):,} input and {int(statistics.median(r['output_tokens'] for r in live)):,} output tokens, median ${statistics.median(r['cost_usd'] for r in live):.2f} a run. Input includes the session's own system prompt and tools, not only the guide."]
    lines += ["", "| Scenario | Row | Tokens loaded | Share of playbook |", "|---|---|---|---|"]
    lines += [f"| {sid} | {row} | {t:,} | {100 * t / whole:.0f}% |" for sid, row, t in sorted(routes, key=lambda x: x[1])]
    lines += ["", "Tokens are characters divided by 4; the exact count depends on the tokenizer.", ""]

    lines += ["## Reading time", "", f"At {WPM} words a minute, the rate `tools/lesson_meta.py` uses for the page.", "",
              "| Document | Minutes |", "|---|---|",
              f"| Whole playbook | {minutes(pb)} |",
              f"| Teaching page (visible text) | {minutes(re.sub(r'<script.*?</script>|<style.*?</style>|<[^>]+>', ' ', read('site/orchestrating-claude.html'), flags=re.S))} |",
              f"| ENTRY.md | {minutes(read('ENTRY.md'))} |"]
    for f in sorted((ROOT / "wiki").glob("*.md")):
        if f.name != "README.md":
            lines += [f"| wiki/{f.name} | {minutes(f.read_text(encoding='utf-8'))} |"]
    lines += [""]

    g = growth()
    lines += ["## Growth", "", "Each row is a commit where one of the counts changed.", "",
              "| Date | Commit | Runbooks | Skills | Router rows | Scenarios | Test cases | Playbook lines |", "|---|---|---|---|---|---|---|---|"]
    lines += [f"| {r['date']} | `{r['commit']}` | {r['runbooks']} | {r['skills']} | {r['router_rows']} | {r['scenarios']} | {r['test_cases']} | {r['playbook_lines']:,} |" for r in g]
    lines += [""]
    snapshot = {"date": datetime.date.today().isoformat(), "suite_ok": run["ok"] if run else None,
                "suite_s": run["total_s"] if run else None, "test_cases": run["test_cases"] if run else None,
                "route_tokens_median": int(statistics.median(vals)), "playbook_tokens": whole,
                **{k: v for k, v in (g[-1] if g else {}).items() if k not in ("commit", "date")}}
    return "\n".join(lines), snapshot


def main(args):
    run = None if "--no-run" in args else run_suite()
    text, snap = report(run)
    print(text)
    if "--write" in args:
        (ROOT / "docs" / "metrics.md").write_text(text, encoding="utf-8")
        print("wrote docs/metrics.md")
    if "--record" in args:
        RESULTS.mkdir(parents=True, exist_ok=True)
        with (RESULTS / "metrics-history.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(snap) + "\n")
        print("appended a snapshot to tests/results/metrics-history.jsonl")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
