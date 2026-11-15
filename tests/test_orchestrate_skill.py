"""Deterministic tests for /orchestrate: the reference router, the card checker, and the prose they mirror.

Run this file:  python3 -I tests/test_orchestrate_skill.py
The live layer (fresh claude -p sessions scored by the same checker) is tests/live/orchestrate/run.py.
"""
import importlib.util
import json
import sys
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "orchestrate"
SKILL = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
FIXTURES = ROOT / "tests" / "fixtures" / "orchestrate"
SCENARIOS = json.loads((ROOT / "tests" / "live" / "orchestrate" / "scenarios.json").read_text(encoding="utf-8"))["scenarios"]


def load(name):
    spec = importlib.util.spec_from_file_location(name, SKILL_DIR / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


route = load("route")
check_card = load("check_card")


class ReferenceRouter(unittest.TestCase):
    def test_every_labelled_case_routes_as_labelled(self):
        """The code router agrees with every hand label in scenarios.json."""
        for s in SCENARIOS:
            with self.subTest(case=s["id"]):
                got = route.route(s["facts"])
                self.assertEqual(got["route"], s["expect"],
                                 f"{s['id']}: route.py picks {got['route']} ({got['why']}), the label says {s['expect']}. "
                                 "Fix the label or the rule, and the matching step in SKILL.md.")

    def test_cases_cover_every_route(self):
        """Each of the six routes has at least one labelled case, so no rule goes untested."""
        self.assertEqual({s["expect"] for s in SCENARIOS}, set(range(1, 7)),
                         "scenarios.json must hold at least one case per route 1 to 6.")

    def test_runner_up_differs_and_high_risk_adds_review(self):
        for s in SCENARIOS:
            got = route.route(s["facts"])
            with self.subTest(case=s["id"]):
                self.assertNotEqual(got["runner_up"], got["route"], f"{s['id']}: runner-up equals the route.")
                if s["facts"].get("high_risk"):
                    self.assertIn("adversarial review of the diff", got["requires"], f"{s['id']}: high risk must require an adversarial review.")

    def test_batch_runs_split_at_thirty(self):
        got = route.route({"independent": True, "items": 40})
        self.assertIn("2 /batch run(s) of at most 30 parts", got["requires"])
        self.assertEqual(route.route({"independent": True, "items": 30})["requires"], ["1 /batch run(s) of at most 30 parts"])

    def test_high_risk_makes_judgment_and_defaults_are_simple(self):
        """F makes D yes (SKILL.md question F), and an empty fact set is a small simple task."""
        self.assertEqual(route.route({"high_risk": True})["route"], 2)
        self.assertEqual(route.route({})["route"], 1)
        self.assertEqual(route.route({"items": 1})["route"], 1)
        self.assertIn("If yes, D is yes too.", SKILL)

    def test_small_batches_use_plain_worktree_subagents(self):
        self.assertEqual(route.route({"independent": True, "items": 4})["requires"], ["4 worktree subagents (below the 5 parts /batch needs)"])
        self.assertEqual(route.route({"independent": True, "items": 5})["requires"], ["1 /batch run(s) of at most 30 parts"])
        self.assertIn("plain worktree subagents when there are fewer than 5 parts", SKILL)

    def test_order_decides_between_sessions_and_hub(self):
        self.assertEqual(route.route({"outlives_session": True, "items": 5})["route"], 4)
        self.assertEqual(route.route({"outlives_session": True, "ordered": True, "items": 5})["route"], 5)

    def test_workflow_needs_twenty_read_only_items_and_no_gate(self):
        self.assertEqual(route.route({"read_only": True, "items": 20, "bulky_output": True})["route"], 6)
        self.assertEqual(route.route({"read_only": True, "items": 19, "bulky_output": True})["route"], 2)
        self.assertEqual(route.route({"read_only": True, "items": 50, "gate_mid_run": True, "bulky_output": True})["route"], 2)
        # A pattern one search answers (C no) stays inline, however many files it spans: a live run beat our first label here.
        self.assertEqual(route.route({"read_only": True, "items": 60, "fits_one_context": True})["route"], 1)


class ProseMatchesCode(unittest.TestCase):
    """SKILL.md is what the model reads; route.py is what the tests trust. They must say the same."""

    def test_thresholds_appear_in_the_skill(self):
        self.assertIn(f"({route.WORKFLOW_MIN_ITEMS} or more)", SKILL, "SKILL.md must state the workflow threshold route.py uses.")
        self.assertIn(f"{route.BATCH_MIN} to {route.BATCH_MAX} worktree subagents", SKILL, "SKILL.md must state the /batch range route.py uses.")
        self.assertIn(f"one `/batch` run per {route.BATCH_MAX} parts", SKILL, "SKILL.md must say how many /batch runs a task needs.")
        self.assertIn(f"Start {route.MAX_BUILDERS} builders at most", SKILL, "SKILL.md must state the builder cap route.py uses.")

    def test_rule_order_matches_the_router(self):
        """The five ordered rules appear in the same order as the branches in route.route()."""
        steps = re.findall(r"^(\d)\. (.+)$", SKILL.split("## 3. Pick the route", 1)[1].split("| Route |", 1)[0], re.M)
        routes = [int(m) for _, text in steps for m in re.findall(r"route (\d)", text)][:6]
        self.assertEqual(routes, [5, 4, 6, 3, 2, 1], f"SKILL.md step 3 rules name routes {routes}; route.py checks 5/4, 6, 3, 2, 1 in that order.")

    def test_runner_ups_match(self):
        """SKILL.md lists each route's runner-up; route.py must give the same ones."""
        line = next(l for l in SKILL.splitlines() if l.startswith("Runner-ups,"))
        pairs = dict((int(a), int(b)) for a, b in __import__("re").findall(r"(\d) to (\d)(?! parts)", line.split("(")[0] + line.split(")")[-1]))
        self.assertEqual(pairs, route.RUNNER_UP, f"SKILL.md runner-ups {pairs} differ from route.RUNNER_UP {route.RUNNER_UP}.")
        self.assertEqual(route.route({"independent": True, "items": 3})["runner_up"], 2, "below 5 parts, route 3's runner-up is 2")
        for s in SCENARIOS:
            got = route.route(s["facts"])
            expected = 2 if got["route"] == 3 and s["facts"].get("items", 1) < route.BATCH_MIN else route.RUNNER_UP[got["route"]]
            self.assertEqual(got["runner_up"], expected, s["id"])

    def test_route_names_match(self):
        for n, name in route.NAMES.items():
            with self.subTest(route=n):
                self.assertIn(f"| {n}. {name} |", SKILL, f"SKILL.md table must name route {n} '{name}' as route.py does.")
                self.assertEqual(check_card.NAMES[n], name.lower(), f"check_card.py names route {n} differently from route.py.")


class CardChecker(unittest.TestCase):
    def run_check(self, name, **kw):
        return {cid: ok for cid, ok, _ in check_card.check((FIXTURES / name).read_text(encoding="utf-8"), **kw)}

    def test_good_cards_pass_every_check(self):
        self.assertTrue(all(self.run_check("good-route3.txt", expect=3).values()))
        self.assertTrue(all(self.run_check("good-high-risk.txt", expect=2, risk="high").values()))
        # Live runs wrote sub-bullets under a part and a "main thread" part; both are valid.
        self.assertTrue(all(self.run_check("good-subbullets.txt", expect=3).values()))

    def test_read_only_route_two_may_have_no_writer(self):
        """A comparison with only reading helpers is valid: routes 1 and 2 allow at most one writer, not exactly one."""
        card = (FIXTURES / "good-high-risk.txt").read_text(encoding="utf-8").replace("| writes |", "| reads |")
        self.assertTrue(dict((c, ok) for c, ok, _ in check_card.check(card))["k-5"])

    def test_reviewer_probes_no_longer_pass(self):
        """False passes an independent review built by hand; each must now fail its check."""
        good = (FIXTURES / "good-route3.txt").read_text(encoding="utf-8")
        hi = (FIXTURES / "good-high-risk.txt").read_text(encoding="utf-8")
        def failed(text, **kw):
            return sorted(c for c, ok, _ in check_card.check(text, **kw) if not ok)
        # A route 1 card that names route 2's longer name.
        self.assertIn("k-2", failed(good.replace("Route: 3. Parallel builders in worktrees.", "Route: 1. Inline plus helper subagents.")))
        # High risk where the only Opus-high part is not a reviewer, and "critic" appears only under Not used.
        probe = hi.replace("- Critic | opus, high | reads | the plan\n", "").replace("- Adversarial review | opus, high | reads | the diff", "- Docs | opus, high | reads | the RFC").replace("Not used:", "Not used: no critic needed;")
        self.assertIn("k-9", failed(probe, risk="high"))
        # A "reviewer" that also writes is not independent.
        writer_review = hi.replace("- Critic | opus, high | reads | the plan\n", "").replace(
            "- Build | opus, medium | writes | auth/login/", "- Build | opus, medium | reads | auth/login/").replace(
            "- Adversarial review | opus, high | reads | the diff", "- Adversarial review | opus, high | writes | the diff")
        self.assertIn("k-9", failed(writer_review, risk="high"))
        # Writers on nested scopes.
        self.assertIn("k-6", failed(good.replace("src/handlers/n-z", "src/handlers/a-m/sub")))
        # Thin checks and a zero budget.
        self.assertIn("k-7", failed(good.replace("Checks: npm test passes; grep finds no old error type; each PR lists its test result", "Checks: yes; no")))
        self.assertIn("k-8", failed(good.replace("Budget: 90 minutes or $15.", "Budget: 0 turns.")))
        # A card that skips the /batch run count route.py requires for 40 items.
        self.assertIn("k-11", failed(good.replace("two /batch runs", "one big run"), facts={"independent": True, "items": 40}))
        # A workflow script with a writer, and a builder route with none.
        self.assertIn("k-5", failed(good.replace("Route: 3. Parallel builders in worktrees.", "Route: 6. Workflow script.")))
        self.assertIn("k-5", failed(good.replace("| writes |", "| reads |")))
        # Closing chatter that starts with "Route:" does not replace the card.
        self.assertEqual(failed(good + "\nRoute: whichever you prefer.\n"), [])

    def test_final_round_false_fails_stay_fixed(self):
        """The last live round exposed three checker false fails: a bare command as a check, and budgets with words
        between the figure and the unit."""
        good = (FIXTURES / "good-route3.txt").read_text(encoding="utf-8")
        def failed(text):
            return sorted(c for c, ok, _ in check_card.check(text) if not ok)
        self.assertEqual(failed(good.replace("Checks: npm test passes;", "Checks: `pytest`;")), [])
        # Round 6: the same command without backticks is still a runnable check; "yes" is not.
        self.assertEqual(failed(good.replace("Checks: npm test passes;", "Checks: pytest;")), [])
        self.assertIn("k-7", failed(good.replace("Checks: npm test passes;", "Checks: yes;")))
        for budget in ("12 builder sessions plus 1 hub, about 3 to 4 days.", "2 helper agents plus about 15 main-thread turns."):
            with self.subTest(budget=budget):
                self.assertEqual(failed(good.replace("90 minutes or $15.", budget)), [])

    def test_live_cards_from_the_final_round_pass(self):
        """Two real cards the checker misread: per-item scopes (handlerN.js) in two /batch runs that say "2 runs",
        and a comparison whose main thread is not one of its 2 to 4 helpers."""
        batch = (FIXTURES / "live-batch-pattern.txt").read_text(encoding="utf-8")
        res = dict((c, ok) for c, ok, _ in check_card.check(batch, expect=3, facts={"independent": True, "items": 40}))
        self.assertTrue(res["k-6"] and res["k-11"], res)
        comp = (FIXTURES / "live-compare-main-thread.txt").read_text(encoding="utf-8")
        res = dict((c, ok) for c, ok, _ in check_card.check(comp, expect=2, facts={"read_only": True, "bulky_output": True, "comparison": True, "items": 3}))
        self.assertTrue(res["k-11"], res)
        # The pattern rule must not hide a real clash: the same concrete file twice still overlaps.
        self.assertIn("k-6", sorted(c for c, ok, _ in check_card.check((FIXTURES / "bad-shared-scope.txt").read_text(encoding="utf-8")) if not ok))

    def test_reads_that_say_no_writing_are_reads(self):
        card = (FIXTURES / "good-high-risk.txt").read_text(encoding="utf-8").replace("| reads | the plan", "| reads (does not write anything) | the plan")
        self.assertEqual(sorted(c for c, ok, _ in check_card.check(card, risk="high") if not ok), [])
        # Round 9: a workflow's merge step said "writes nothing to the repo".
        self.assertFalse(check_card.writes("writes nothing to the repo"))
        self.assertTrue(check_card.writes("writes"))
        merge = (FIXTURES / "good-route3.txt").read_text(encoding="utf-8").replace("- Scout | haiku, low | reads |", "- Scout | no model | writes nothing to the repo |")
        self.assertNotIn("k-4", sorted(c for c, ok, _ in check_card.check(merge) if not ok))

    def test_good_cards_carry_their_requirements(self):
        self.assertTrue(dict((c, ok) for c, ok, _ in check_card.check((FIXTURES / "good-route3.txt").read_text(encoding="utf-8"), facts={"independent": True, "items": 40}))["k-11"])
        self.assertTrue(dict((c, ok) for c, ok, _ in check_card.check((FIXTURES / "good-high-risk.txt").read_text(encoding="utf-8"), facts={"high_risk": True}))["k-11"])

    def test_each_bad_card_fails_only_its_own_check(self):
        """Every broken fixture trips exactly the check it was built to trip, and no other."""
        cases = {
            "bad-missing-field.txt": "k-1", "bad-route-name.txt": "k-2", "bad-runner-same.txt": ["k-12", "k-3"],
            "bad-part-line.txt": "k-4", "bad-route1-two-writers.txt": "k-5", "bad-shared-scope.txt": "k-6",
            "bad-checks-count.txt": "k-7", "bad-budget.txt": "k-8",
            "bad-route2-two-writers.txt": "k-5", "bad-no-failure-cap.txt": "k-8",
        }
        for name, target in cases.items():
            with self.subTest(fixture=name):
                failed = sorted(cid for cid, ok in self.run_check(name).items() if not ok)
                want = target if isinstance(target, list) else [target]
                self.assertEqual(failed, want, f"{name} should fail only {want}, failed {failed}.")
        failed = sorted(cid for cid, ok in self.run_check("bad-high-risk.txt", risk="high").items() if not ok)
        self.assertEqual(failed, ["k-9"])

    def test_wrong_route_fails_expectation_and_accept_rescues_it(self):
        self.assertFalse(self.run_check("good-route3.txt", expect=4)["k-10"])
        self.assertTrue(self.run_check("good-route3.txt", expect=4, accept=(3,))["k-10"])

    def test_semicolons_inside_code_do_not_split_a_check(self):
        """A live card's shell loop held semicolons inside backticks; it is still one check."""
        line = "`for i in $(seq 30); do npm test || break; done` passes; `git diff` is small"
        self.assertEqual(len(check_card.split_checks(line)), 2)

    def test_prose_semicolons_do_not_add_checks(self):
        """Live cards put semicolons in parentheses and inside bulleted checks; neither is a new check."""
        self.assertEqual(len(check_card.split_checks("`pytest` (no tests collected is NOT RUN; not PASS); grep is clean")), 2)
        card = (FIXTURES / "good-route3.txt").read_text(encoding="utf-8").replace(
            "Checks: npm test passes; grep finds no old error type; each PR lists its test result",
            "Checks:\n- npm test before any edit (baseline); NOT RUN so far\n- npm test after\n- grep is clean")
        self.assertTrue(dict((c, ok) for c, ok, _ in check_card.check(card))["k-7"])

    def test_live_scorer_flags_writes_but_not_dev_null(self):
        """The live scorer's s-1 must not mistake 2>/dev/null for a write, and must catch real writes."""
        spec = importlib.util.spec_from_file_location("run", ROOT / "tests" / "live" / "orchestrate" / "run.py")
        run = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(run)
        clean = lambda c: run.WRITES.search(re.sub(r"\d?>\s*/dev/null|\d?>&\d", "", c))
        self.assertIsNone(clean("ls -a; cat CLAUDE.md 2>/dev/null | head -40; ls services 2>&1 | wc -l"))
        for cmd in ("cat x > notes.md", "find . -name '*.tmp' -delete", "echo hi | tee out.txt", "rm -rf build"):
            with self.subTest(cmd=cmd):
                self.assertIsNotNone(clean(cmd), f"s-1 must flag: {cmd}")

    def test_skill_ends_with_the_exact_go_line(self):
        self.assertIn("Go, or change the route?", SKILL, "SKILL.md must give the exact closing line the live scorer looks for.")

    def test_no_card_is_a_failure_not_a_crash(self):
        res = check_card.check("I would just start working on it.")
        self.assertEqual([(cid, ok) for cid, ok, _ in res], [("k-1", False)])

    def test_card_template_in_skill_passes_the_checker_shape(self):
        """The template in SKILL.md names every field check_card.py looks for, in order."""
        block = SKILL.split("## 5. Write the routing card and stop", 1)[1].split("```", 2)[1]
        fields = [m for m in re.findall(r"^([A-Z][\w-]*(?: used)?):", block, re.M)]
        self.assertEqual(fields, check_card.FIELDS, f"SKILL.md card template fields {fields} differ from check_card.FIELDS.")



class AnswersReasoningOutcome(unittest.TestCase):
    """The card shows its working (Answers, Reasoning), and the code checks the working adds up."""

    def setUp(self):
        self.good = (FIXTURES / "good-route3.txt").read_text(encoding="utf-8")

    def failed(self, text, **kw):
        return sorted(c for c, ok, _ in check_card.check(text, **kw) if not ok)

    def test_route_must_follow_from_the_cards_own_answers(self):
        # Flip B to no: the answers now give route 2, but the card still says route 3.
        self.assertIn("k-12", self.failed(self.good.replace("B yes;", "B no;")))
        # Leave out an answer: the card cannot be checked, so it fails.
        self.assertIn("k-12", self.failed(self.good.replace(" order no;", "")))
        # Wrong runner-up for these answers.
        wrong = self.good.replace("Runner-up: 4. One session per task.", "Runner-up: 2. Inline plus helper subagents.")
        self.assertIn("k-12", self.failed(wrong))

    def test_reasoning_is_judged_by_shape_not_sentence_count(self):
        """Rounds 6 and 7: a sentence cap made cards grow to fill it. The shape (rules walked, the one that fired,
        cheaper routes, what would change it) is what the user needs, and a word cap keeps it short."""
        self.assertNotIn("k-13", self.failed(self.good))
        self.assertIn("Rule <n>: fired", SKILL)
        self.assertIn("Keep it under 150 words", SKILL)

    def test_reasoning_cites_the_rule_that_fired(self):
        self.assertIn("k-13", self.failed(self.good.replace("Rule 3: fired", "Rule 4: fired")))
        bare = self.good.split("Reasoning:")[0] + "Reasoning: Rule 3: fired.\n" + "Runner-up:" + self.good.split("Runner-up:", 1)[1]
        self.assertIn("k-13", self.failed(bare))
        essay = self.good.replace("Would change if:", "Would change if: " + "and so on " * 60 + ".")
        self.assertIn("k-13", self.failed(essay))

    def test_rule_numbers_match_skill_step_three(self):
        """route.py's rule number points at the step 3 rule whose text names that route."""
        step3 = SKILL.split("## 3. Pick the route", 1)[1].split("| Route |", 1)[0]
        rules = {int(n): [int(x) for x in re.findall(r"route (\d)", text)] for n, text in re.findall(r"^(\d)\. (.+)$", step3, re.M)}
        for s in SCENARIOS:
            got = route.route(s["facts"])
            with self.subTest(case=s["id"]):
                self.assertIn(got["route"], rules[got["rule"]], f"{s['id']}: rule {got['rule']} in SKILL.md does not name route {got['route']}.")

    def test_skill_card_and_router_explain_agree_on_rules(self):
        self.assertIn("Why: rule 3:", subprocess_explain('{"independent":true,"items":40}'))

    def test_skill_writes_every_prompt_for_every_route(self):
        """Step 6 says how to start each route and gives the helper, builder and hub prompts, so the user writes none."""
        step6 = SKILL.split("## 6. After a yes", 1)[1].split("## 7.", 1)[0]
        for n in range(1, 7):
            with self.subTest(route=n):
                self.assertRegex(step6, re.compile(rf"^\| {n} \|", re.M), f"SKILL.md step 6 has no row for route {n}.")
        for prompt in ("Helper: Objective:", "Builder: Item <id>:", "Hub: /goal"):
            self.assertIn(prompt, step6, f"SKILL.md step 6 lost the '{prompt}' prompt.")
        self.assertIn("you write every brief and prompt the route needs", step6)

    def test_outcome_lines(self):
        good = "- 2026-11-14 /orchestrate outcome: migrate handlers | route 3 (Parallel builders in worktrees) | budget 90 minutes | spent 75 minutes | checks PASS 3, FAIL 0, NOT RUN 0 | route again: yes, because no handler shared a file"
        self.assertTrue(all(ok for _, ok, _ in check_card.check_outcomes(good)))
        for bad in (good.replace(", because no handler shared a file", ""),
                    good.replace("(Parallel builders in worktrees)", "(Workflow script)"),
                    good.replace("checks PASS 3, FAIL 0, NOT RUN 0", "checks all good"),
                    "no outcome here"):
            with self.subTest(line=bad[:60]):
                self.assertFalse(all(ok for _, ok, _ in check_card.check_outcomes(bad)))

    def test_skill_outcome_template_matches_the_checker(self):
        """Fill SKILL.md's outcome template with sample values; the checker must accept it."""
        line = next(l for l in SKILL.splitlines() if "/orchestrate outcome:" in l)
        filled = (line.replace("<YYYY-MM-DD>", "2026-11-14").replace("<task in a few words>", "fix flaky test")
                  .replace("<number>", "1").replace("<name>", "Inline").replace("<figure>", "20 turns")
                  .replace("<n>", "1").replace("<yes|no>", "yes").replace("<reason>", "one writer was enough"))
        self.assertTrue(all(ok for _, ok, _ in check_card.check_outcomes(filled)), filled)



class ReviewFindingsPR8(unittest.TestCase):
    """Findings from the PR #8 review. Each test fails on the checker as it was before the fix."""

    def setUp(self):
        self.good = (FIXTURES / "good-route3.txt").read_text(encoding="utf-8")
        self.hi = (FIXTURES / "good-high-risk.txt").read_text(encoding="utf-8")

    def failed(self, text, **kw):
        return sorted(c for c, ok, _ in check_card.check(text, **kw) if not ok)

    def test_gate_and_comparison_are_required_answers(self):
        for key in (" gate no;", " comparison no;"):
            with self.subTest(dropped=key):
                self.assertIn("k-12", self.failed(self.good.replace(key, "")))

    def test_read_only_sessions_and_hubs_need_no_writer(self):
        """A read-only task on route 4 or 5 is valid with only reading parts, and invalid with a writer."""
        for route, name, runner, ordered in ((4, "One session per task", "3. Parallel builders in worktrees", "no"),
                                             (5, "Hub plus builder sessions", "4. One session per task", "yes")):
            card = (self.good
                    .replace("Route: 3. Parallel builders in worktrees.", f"Route: {route}. {name}.")
                    .replace("Runner-up: 4. One session per task.", f"Runner-up: {runner}.")
                    .replace("A no; B yes; C no; D no; E no; F no; order no; read-only no;",
                             f"A no; B no; C yes; D no; E yes; F no; order {ordered}; read-only yes;")
                    .replace("items 40", "items 3")
                    .replace("Rule 1: skipped, E no. Rule 2: skipped, the handlers are written. Rule 3: fired, B yes: 40 handlers touch different files, none imports another, and each has its own test.",
                             "Rule 1: fired, E yes across 3 audits over several days.")
                    .replace("| writes |", "| reads |"))
            with self.subTest(route=route):
                self.assertNotIn("k-5", self.failed(card))
                self.assertIn("k-5", self.failed(card.replace("- Batch A | sonnet, medium | reads |", "- Batch A | sonnet, medium | writes |")))

    def test_high_risk_is_read_from_the_cards_answers(self):
        """F yes in Answers turns on k-9 without --risk high."""
        stripped = self.hi.replace("- Critic | opus, high | reads | the plan\n", "")
        self.assertIn("k-9", self.failed(stripped))

    def test_both_review_roles_and_the_sign_off_are_required(self):
        no_adversary = self.hi.replace("- Adversarial review | opus, high | reads | the diff\n", "")
        no_critic = self.hi.replace("- Critic | opus, high | reads | the plan\n", "")
        no_signoff = self.hi.replace(", human sign-off", "").replace("and a human signs off", "and the reviewer agrees")
        for name, card in (("adversary", no_adversary), ("critic", no_critic), ("sign-off", no_signoff)):
            with self.subTest(missing=name):
                self.assertIn("k-9", self.failed(card))
        self.assertNotIn("k-9", self.failed(self.hi))
        # A reviewer that also writes is not independent, even with both roles named.
        self.assertIn("k-9", self.failed(self.hi.replace("- Adversarial review | opus, high | reads | the diff", "- Adversarial review | opus, high | writes | the diff")))

    def test_walking_the_rules_is_not_enough_if_the_wrong_one_fires(self):
        """Rules 1 to 3 walked in order, but rule 4 named as fired: the answers fire rule 3, so k-13 fails."""
        wrong = self.good.replace("Rule 3: fired, B yes:", "Rule 3: skipped, maybe. Rule 4: fired, B yes:")
        self.assertIn("k-13", self.failed(wrong))

    def test_reasoning_must_walk_the_rules_before_the_one_that_fired(self):
        short = self.good.replace("Rule 1: skipped, E no. Rule 2: skipped, the handlers are written. ", "")
        self.assertIn("k-13", self.failed(short))

    def test_live_runner_treats_missing_records_as_errors(self):
        run_py = (ROOT / "tests" / "live" / "orchestrate" / "run.py").read_text(encoding="utf-8")
        self.assertIn('else "missing"', run_py, "a missing exit.txt must not count as exit 0")
        self.assertIn("have no transcript", run_py, "--rescore must fail when a requested transcript is missing")

def subprocess_explain(facts):
    import subprocess
    return subprocess.run([sys.executable, "-I", str(SKILL_DIR / "route.py"), "--explain", facts],
                          capture_output=True, text=True, check=True).stdout

if __name__ == "__main__":
    unittest.main()
