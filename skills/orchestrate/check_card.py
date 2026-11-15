"""Check a routing card written by /orchestrate. Code, not prose, decides whether a card is usable.

Usage: python3 -I skills/orchestrate/check_card.py <card.txt> [--expect N] [--accept N,M] [--risk high] [--facts '<json>']
       python3 -I skills/orchestrate/check_card.py --outcome <file>   check the outcome lines in a decisions file
Reads the whole file and checks the card inside it (a fenced block or plain lines both work). When the
text holds more than one "Route:" line, the last block that has all nine fields is the card.
Prints one PASS or FAIL line per check and exits 1 on any FAIL.

  k-1  all nine fields are there, in order: Route, Answers, Reasoning, Runner-up, Parts, Order, Checks, Budget, Not used
  k-2  Route starts with a number 1 to 6 followed by exactly that route's name
  k-3  Runner-up starts with a different route number, 1 to 6
  k-4  every part line reads "<part> | <model>, <effort> | reads or writes | <scope>" with a known model and effort
       ("main thread", "human" or "no model" (a script step) may leave out the effort; an indented sub-bullet
       belongs to the part above it; "does not write" counts as reading)
  k-5  writers: none when Answers say read-only yes; otherwise routes 1 and 2 at most one (route 1 has exactly
       one part), routes 3, 4 and 5 at least one, route 6 none
  k-6  no two writers share a scope, and no writer's scope sits inside another's (src/ and src/handlers/ overlap)
  k-7  Checks lists 2 to 5 items, each a `command` or at least 3 words
  k-8  Budget has a figure above zero with a unit (up to two words between, as in "12 builder sessions"),
       and Stop when caps failures ("2 failures")
  k-9  high risk (F yes in Answers, --risk high or high_risk in --facts): reading parts on Opus at high effort
       or above named as a critic and as an adversarial reviewer, and "human" in Order
  k-10 with --expect: the route is the expected one (or one listed in --accept)
  k-11 the card carries what route.py says the route requires (/batch runs, builder cap, helper count, human
       sign-off), from --facts or, without them, from the card's own Answers
  k-12 Answers covers A to F, order, read-only, gate, comparison and items, and route.py, given those answers, picks the
       card's route and runner-up: the route follows from the card's own answers
  k-13 Reasoning walks rules 1 to N in order, each earlier one as "Rule k: skipped, <reason>", and says
       "Rule N: fired" for exactly the rule route.py computes from
       the Answers, has "Cheaper routes:" and "Would change if:", and stays under 150 words

Outcome lines (--outcome), one per finished route, in the form SKILL.md step 7 gives:
  o-1  date, task, route number and name, budget, spent, PASS/FAIL/NOT RUN counts, and "route again: yes|no, because ..."
"""
import importlib.util
import json
import pathlib
import re
import sys

FIELDS = ["Route", "Answers", "Reasoning", "Runner-up", "Parts", "Order", "Checks", "Budget", "Not used"]
# The Answers line, mapped to route.py's facts. Every key and items are required, as the card template lists them.
ANSWER_KEYS = {"a": "fits_one_context", "b": "independent", "c": "bulky_output", "d": "needs_judgment",
               "e": "outlives_session", "f": "high_risk", "order": "ordered", "read-only": "read_only",
               "gate": "gate_mid_run", "comparison": "comparison"}
REQUIRED_ANSWERS = ("a", "b", "c", "d", "e", "f", "order", "read-only", "gate", "comparison")
NAMES = {
    1: "inline",
    2: "inline plus helper subagents",
    3: "parallel builders in worktrees",
    4: "one session per task",
    5: "hub plus builder sessions",
    6: "workflow script",
}
MODELS = ("haiku", "sonnet", "opus", "fable", "human", "main thread", "main session", "no model", "no agent")
NO_EFFORT = ("human", "main thread", "main session", "no model", "no agent")
EFFORTS = ("low", "medium", "high", "xhigh", "max")
STRONG = ("high", "xhigh", "max")
FIELD_RE = re.compile(r"^\s*(?:[-*]\s*)?(?:\*\*)?(" + "|".join(re.escape(f) for f in FIELDS) + r")(?:\*\*)?\s*:\s*(.*)$", re.I)
BULLET = re.compile(r"^\s*(?:[-*]|\d+[.)])\s+")
COMMAND = re.compile(r"(?:npm|npx|pnpm|yarn|bun|deno|pytest|python3?|go|cargo|make|mvn|gradle|ruff|mypy|tox|grep|git|bash|sh)\b")
NUMBER_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6}


def parse(text):
    """Return {field: [lines]} for the card. Bullet lines after a field belong to it."""
    cards, cur, field = [], None, None
    for raw in text.splitlines():
        line = raw.rstrip()
        m = FIELD_RE.match(line)
        if m:
            name = next(f for f in FIELDS if f.lower() == m.group(1).lower())
            if name == "Route":
                cur = {"_order": []}
                cards.append(cur)
            if cur is None:
                continue
            field = name
            cur["_order"].append(name)
            cur.setdefault(name, [])
            if m.group(2).strip():
                cur[name].append(m.group(2).strip())
        elif cur is not None and field and cur[field] and re.match(r"\s{2,}(?:[-*]|\d+[.)])\s+", line):
            cur[field][-1] += " " + BULLET.sub("", line).strip()  # a sub-bullet belongs to its item
        elif cur is not None and field and BULLET.match(line):
            cur[field].append(BULLET.sub("", line).strip())
        elif cur is not None and field and line.strip():
            field = None  # an unlabelled, unbulleted line (notes, a fence) ends the field
    full = [c for c in cards if all(f in c for f in FIELDS)]
    return (full or cards)[-1] if cards else None


def split_checks(line):
    """Split a Checks line on semicolons outside `code spans` and (parentheses), so a shell loop stays one check."""
    out, cur, in_code, depth = [], "", False, 0
    for ch in line:
        if ch == "`":
            in_code = not in_code
        elif not in_code and ch == "(":
            depth += 1
        elif not in_code and ch == ")" and depth:
            depth -= 1
        if ch == ";" and not in_code and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return [x.strip() for x in out if x.strip()]


def route_number(lines):
    """The route number a field starts with ("3. Parallel ..."), or None."""
    m = re.match(r"\s*(?:\*\*)?\s*([1-6])\b", " ".join(lines))
    return int(m.group(1)) if m else None


def named_route(lines):
    """The route whose name follows the number: the longest name the text starts with."""
    m = re.match(r"\s*(?:\*\*)?\s*[1-6]\s*[.):-]?\s*(.*)", " ".join(lines).lower())
    if not m:
        return None
    rest = m.group(1)
    hits = [n for n, name in NAMES.items() if rest.startswith(name)]
    return max(hits, key=lambda n: len(NAMES[n])) if hits else None


def writes(cell):
    cell = cell.lower()
    if re.search(r"\b(?:not|no|never|nothing)\b[^|]{0,20}\bwrit", cell) or re.search(r"\bwrit\w*\s+nothing\b", cell):
        return False
    return bool(re.search(r"\bwrit", cell))


def parts(card):
    out = []
    for line in card.get("Parts", []):
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 4:
            out.append({"line": line, "ok": False})
            continue
        model_effort = cells[1].lower()
        model = next((m for m in MODELS if m in model_effort), None)
        effort = next((e for e in EFFORTS if re.search(rf"\b{e}\b", model_effort)), None)
        if model in NO_EFFORT:
            effort = effort or "n/a"
        w = writes(cells[2])
        reads = "read" in cells[2].lower() or (not w and "writ" in cells[2].lower())  # "writes nothing" is a reader
        out.append({"line": line, "ok": bool(model and effort and (w or reads)), "name": cells[0].lower(), "agent": model_effort,
                    "model": model, "effort": effort, "writes": w, "scope": cells[3].lower()})
    return out


PLACEHOLDER = re.compile(r"[*{}<>]|\b\w*n\.\w+\b|\bhandler\s*n\b|\bn\b", re.I)


def overlap(a, b):
    """Two writer scopes overlap if equal or nested. A per-item pattern (handlerN.js, *, <file>) names a
    different file for every item, so it never overlaps itself."""
    if PLACEHOLDER.search(a) and a == b:
        return False
    a, b = a.strip().rstrip("/"), b.strip().rstrip("/")
    return a == b or a.startswith(b + "/") or b.startswith(a + "/")


def load_route():
    path = pathlib.Path(__file__).with_name("route.py")
    spec = importlib.util.spec_from_file_location("route", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def mentions_number(text, n, after):
    """True if the text says n (digit or word) within a few words before `after`."""
    words = [w for w, v in NUMBER_WORDS.items() if v == n]
    num = "|".join([str(n)] + words)
    return bool(re.search(rf"\b(?:{num})\b[^.;\n]{{0,25}}{after}", text, re.I))


def parse_answers(lines):
    """Turn an Answers line into route.py facts. Returns (facts, missing keys)."""
    text = " ".join(lines).lower()
    facts, seen = {}, set()
    for key, value in re.findall(r"(?<![\w-])(a|b|c|d|e|f|order|read-only|gate|comparison)\s*[:=]?\s*(yes|no)\b", text):
        facts[ANSWER_KEYS[key]] = value == "yes"
        seen.add(key)
    m = re.search(r"\bitems\s*[:=]?\s*(\d+)", text)
    if m:
        facts["items"] = int(m.group(1))
    missing = [k for k in REQUIRED_ANSWERS if k not in seen] + ([] if m else ["items"])
    return facts, missing


OUTCOME_RE = re.compile(
    r"^-?\s*(\d{4}-\d{2}-\d{2}) /orchestrate outcome: (.+?) \| route ([1-6]) \(([^)]+)\) \| budget (.+?) \| spent (.+?) \| "
    r"checks PASS (\d+), FAIL (\d+), NOT RUN (\d+) \| route again: (yes|no), because (.{4,})$", re.I)


def check_outcomes(text):
    """Return (id, ok, message) for every line that says '/orchestrate outcome'."""
    res = []
    for n, line in enumerate(text.splitlines(), 1):
        if "/orchestrate outcome" not in line:
            continue
        m = OUTCOME_RE.match(line.strip())
        ok = bool(m) and NAMES[int(m.group(3))] == m.group(4).strip().lower()
        res.append(("o-1", ok, f"line {n}: " + ("outcome line complete" if ok else "needs date, task, route N (its name), budget, spent, PASS/FAIL/NOT RUN counts, route again: yes|no, because ...")))
    if not res:
        res.append(("o-1", False, "no '/orchestrate outcome' line found"))
    return res


def check(text, expect=None, accept=(), risk=None, facts=None):
    """Return a list of (id, ok, message)."""
    res = []
    card = parse(text)
    if card is None:
        return [("k-1", False, "no card found: no line starts with 'Route:'")]
    missing = [f for f in FIELDS if f not in card]
    in_order = [f for f in card["_order"] if f in FIELDS]
    order_ok = in_order[:len(FIELDS)] == FIELDS
    res.append(("k-1", not missing and order_ok,
                f"missing: {', '.join(missing)}" if missing else ("fields in order" if order_ok else f"order is {in_order}")))

    r = route_number(card.get("Route", []))
    named = named_route(card.get("Route", []))
    res.append(("k-2", r is not None and named == r,
                f"route {r}" if r and named == r else f"route line must start with a number and exactly that route's name: {' '.join(card.get('Route', []))[:80]}"))

    ru = route_number(card.get("Runner-up", []))
    res.append(("k-3", ru is not None and ru != r, f"runner-up {ru}" if ru and ru != r else f"runner-up {ru} is missing, not first on its line, or equals the route"))

    ps = parts(card)
    bad = [p["line"] for p in ps if not p["ok"]]
    res.append(("k-4", bool(ps) and not bad, f"{len(ps)} part(s)" if ps and not bad else f"unreadable part line(s): {bad or 'none listed'}"))

    answers, gaps = parse_answers(card.get("Answers", []))
    read_only = answers.get("read_only") is True or bool(facts and facts.get("read_only"))
    high = risk == "high" or answers.get("high_risk") is True or bool(facts and facts.get("high_risk"))

    writers = [p for p in ps if p.get("writes")]
    if read_only:
        ok, msg = not writers and (r != 1 or len(ps) == 1), f"{len(writers)} writer(s); the task is read-only"
    elif r in (1, 2):
        ok = len(writers) <= 1 and (r != 1 or len(ps) == 1)
        msg = f"{len(writers)} writer(s), {len(ps)} part(s)"
    elif r == 6:
        ok, msg = not writers, f"{len(writers)} writer(s); a workflow script is read-only"
    else:
        ok, msg = len(writers) >= 1, f"{len(writers)} writer(s); route {r} builds, so it needs at least one"
    res.append(("k-5", ok, msg))
    clash = [(a["scope"], b["scope"]) for i, a in enumerate(writers) for b in writers[i + 1:] if overlap(a["scope"], b["scope"])]
    res.append(("k-6", not clash, "writer scopes distinct" if not clash else f"writers overlap: {clash}"))

    checks = card.get("Checks", [])
    items = checks if len(checks) > 1 else sum((split_checks(line) for line in checks), [])
    # A check of one or two words is too thin to run, unless it is a command (`npm test`, pytest, go test).
    thin = [c for c in items if len(c.split()) < 3 and "`" not in c and not COMMAND.match(c.strip())]
    res.append(("k-7", 2 <= len(items) <= 5 and not thin,
                f"{len(items)} check(s)" + (f"; too thin to run: {thin}" if thin else "")))

    budget = " ".join(card.get("Budget", []))
    # A figure, up to two words, then a unit: "90 minutes", "12 builder sessions", "15 main-thread turns", "$15".
    figure = re.search(r"(\d+(?:\.\d+)?)\s*(?:[\w-]+\s+){0,2}(?:turns?|minutes?|mins?|hours?|hrs?|h\b|days?|weeks?|dollars?|usd|tool calls?|sessions?|contexts?|agents?|subagents?)\b|\$\s*(\d+(?:\.\d+)?)", budget, re.I)
    positive = bool(figure) and float(figure.group(1) or figure.group(2)) > 0
    caps = re.search(r"stop when", budget, re.I) and re.search(r"\b(?:2|two) (?:failures|fails|attempts)", budget, re.I)
    res.append(("k-8", bool(positive and caps), "budget and failure cap" if positive and caps else f"budget lacks a figure above zero or the 2-failure stop: {budget[:100]}"))

    if high:
        strong = [p for p in ps if p.get("model") == "opus" and p.get("effort") in STRONG and not p.get("writes")]
        critic = [p for p in strong if re.search(r"\bcritic", p.get("name", ""))]
        adversary = [p for p in strong if p not in critic and (re.search(r"\badversar|\bdiff\s+review", p.get("name", ""))
                                                               or re.search(r"\badversar", p.get("agent", "")))]
        signoff = re.search(r"human", " ".join(card.get("Order", [])), re.I)
        missing_roles = ([] if critic else ["a plan critic"]) + ([] if adversary else ["an adversarial reviewer of the diff"]) + \
                        ([] if signoff else ['"human sign-off" in Order'])
        res.append(("k-9", not missing_roles, "critic, adversarial reviewer and human sign-off" if not missing_roles
                    else f"high risk needs, on Opus at high effort and reading: {', '.join(missing_roles)}"))

    if expect is not None:
        ok = r == expect or r in accept
        res.append(("k-10", ok, f"route {r}, expected {expect}" + (f" (accepts {list(accept)})" if accept else "")))

    req_facts = facts if facts is not None else (answers if not gaps else None)
    if req_facts is not None:
        want = load_route().route(req_facts)
        whole = " ".join(sum((v for k, v in card.items() if k != "_order"), []))
        missing_req = []
        if r == want["route"]:
            for req in want["requires"]:
                m = re.match(r"(\d+) /batch run", req)
                if m and not (mentions_number(whole, int(m.group(1)), r"/?batch run") or
                              (re.search(r"/batch", whole) and mentions_number(whole, int(m.group(1)), r"runs?\b"))):
                    missing_req.append(req)
                m = re.match(r"(\d+) worktree subagents", req)
                if m and not re.search(r"worktree", whole, re.I):
                    missing_req.append(req)
                if req.startswith("at most") and not re.search(r"\b(?:3|three)\b", " ".join(card.get("Order", [])), re.I):
                    missing_req.append(req)
                if req.startswith("2 to 4"):
                    helpers = [p for p in ps if not p.get("writes") and p.get("model") not in NO_EFFORT
                               and not p.get("name", "").startswith(("main thread", "main session"))]
                    if not 2 <= len(helpers) <= 4:
                        missing_req.append(f"{req} (card has {len(helpers)})")
                if req == "human sign-off" and not re.search(r"human", whole, re.I):
                    missing_req.append(req)
        res.append(("k-11", not missing_req, "carries what the route requires" if not missing_req else f"missing: {missing_req}"))

    if gaps:
        res.append(("k-12", False, f"Answers lacks: {', '.join(gaps)}"))
        derived = None
    else:
        derived = load_route().route(answers)
        ok = derived["route"] == r and derived["runner_up"] == ru
        res.append(("k-12", ok, f"answers give route {derived['route']}, runner-up {derived['runner_up']}" +
                    ("" if ok else f"; the card says route {r}, runner-up {ru}")))

    reasoning = " ".join(card.get("Reasoning", []))
    fired = re.findall(r"\brule\s+([1-5])\s*[:,-]?\s*fired\b", reasoning, re.I)
    want_rule = derived["rule"] if derived else None
    parts_ok = re.search(r"cheaper routes?\s*:", reasoning, re.I) and re.search(r"would change if\s*:", reasoning, re.I)
    words = len(reasoning.split())
    seen = []
    for n in re.findall(r"\brule\s+([1-5])\b", reasoning, re.I):
        if int(n) not in seen:
            seen.append(int(n))
    skipped_ok = want_rule is None or all(
        re.search(rf"\brule\s+{k}\s*[:,-]?\s*skipped\b[\s,:;(-]*\w+", reasoning, re.I) for k in range(1, want_rule))
    walked = want_rule is None or (seen[:want_rule] == list(range(1, want_rule + 1)) and skipped_ok)
    ok = bool(fired) and (want_rule is None or fired == [str(want_rule)]) and bool(parts_ok) and words <= 150 and walked
    problems = []
    if not walked:
        problems.append(f"walks rules {seen}; it must take rules 1 to {want_rule} in order, each earlier one as \"Rule k: skipped, <reason>\"")
    if not fired:
        problems.append('no "Rule N: fired"')
    elif want_rule and fired != [str(want_rule)]:
        problems.append(f"says rule {', '.join(fired)} fired; the answers fire rule {want_rule}")
    if not parts_ok:
        problems.append('needs "Cheaper routes:" and "Would change if:"')
    if words > 150:
        problems.append(f"{words} words, over 150")
    res.append(("k-13", ok, f"rule {fired[0]} fired, {words} words" if ok else "; ".join(problems)))
    return res


def main(argv):
    if len(argv) == 2 and argv[0] == "--outcome":
        with open(argv[1], encoding="utf-8") as fh:
            results = check_outcomes(fh.read())
        for cid, ok, msg in results:
            print(f"{'PASS' if ok else 'FAIL'} {cid} {msg}")
        return 0 if all(ok for _, ok, _ in results) else 1
    if not argv or argv[0].startswith("-"):
        print(__doc__)
        return 2
    path, kw = argv[0], {}
    i = 1
    while i < len(argv):
        if i + 1 >= len(argv):
            print(f"{argv[i]} needs a value")
            return 2
        key, val = argv[i], argv[i + 1]
        if key == "--expect":
            kw["expect"] = int(val)
        elif key == "--accept":
            kw["accept"] = tuple(int(x) for x in val.split(",") if x)
        elif key == "--risk":
            kw["risk"] = val
        elif key == "--facts":
            kw["facts"] = json.loads(val)
        else:
            print(f"unknown argument {key}")
            return 2
        i += 2
    with open(path, encoding="utf-8") as fh:
        results = check(fh.read(), **kw)
    for cid, ok, msg in results:
        print(f"{'PASS' if ok else 'FAIL'} {cid} {msg}")
    return 0 if all(ok for _, ok, _ in results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
