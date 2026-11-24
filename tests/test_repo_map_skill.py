"""Deterministic tests for /repo-map: the map checker and the rules SKILL.md must keep.

Run this file:  python3 -I tests/test_repo_map_skill.py
Where the default temp folder is not writable, set TEST_TMP to a writable folder.
"""
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "repo-map"
CHECK = SKILL_DIR / "check_map.py"
FIXTURES = ROOT / "tests" / "fixtures" / "repo-map"
SPEC_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}


def clean_env():
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def run_check(folder, repo):
    out = subprocess.run([sys.executable, "-I", str(CHECK), str(folder), "--repo", str(repo)],
                         capture_output=True, text=True, env=clean_env(), timeout=60)
    return out.returncode, out.stdout


def failed_checks(stdout):
    return sorted({l[5:].split(": ", 1)[0].strip() for l in stdout.splitlines() if l.startswith("FAIL ")})


class Base(unittest.TestCase):
    def tmp(self):
        path = tempfile.mkdtemp(prefix="repomap-", dir=os.environ.get("TEST_TMP") or None)
        self.addCleanup(shutil.rmtree, path, True)
        return pathlib.Path(path)

    def copy_good(self):
        base = self.tmp()
        shutil.copytree(FIXTURES / "repo", base / "repo")
        shutil.copytree(FIXTURES / "good", base / "map")
        return base / "map", base / "repo"

    def edit(self, path, old, new):
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text, f"fixture changed: '{old}' not in {path.name}")
        path.write_text(text.replace(old, new, 1), encoding="utf-8")


class CheckerTests(Base):
    def test_good_map_passes(self):
        """The reference map of the fixture repository passes every check."""
        code, out = run_check(FIXTURES / "good", FIXTURES / "repo")
        self.assertEqual(code, 0, out)
        self.assertIn("SUMMARY PASS", out)

    def test_each_broken_map_fails_exactly_its_check(self):
        """Each kind of wrong map is caught, by the right check and only that one."""
        cases = {
            "invented path": ("components/worker.md", "path: worker/", "path: workers/", ["paths exist"]),
            "invented key name": ("components/api.md", "create_order,", "create_orders,", ["names occur in code"]),
            "invented seen_as": ("terms/Customer.md", "seen_as: [Customer]", "seen_as: [Client]", ["names occur in code"]),
            "broken link": ("terms/Customer.md", "[[Order|purchase]]", "[[basket2]]", ["links resolve"]),
            "note not in index": ("index.md", "- [[shared]]: data types used by both\n", "", ["index lists every note"]),
            "missing property": ("decisions/queue-between-api-and-worker.md", "source: api/server.py\n", "", ["notes and properties"]),
            "unknown type": ("questions/which-broker.md", "type: question", "type: todo", ["notes and properties"]),
            "missing section": ("architecture.md", "## What this map can't see", "## Notes", ["notes and properties"]),
            "bad stamp": ("index.md", "date: 2026-11-23", "date: soon", ["stamp"]),
            "line reference": ("components/worker.md", "imports from `api/`", "imports from `api/server.py:3`", ["no path:line references"]),
            "two diagrams": ("architecture.md", "## Boundaries", "```mermaid\nflowchart LR\n  api --> worker\n```\n\n## Boundaries", ["diagram"]),
            "big diagram": ("architecture.md", "  api -.queue.-> worker", "  api -.queue.-> worker\n" + "\n".join(f"  n{i} --> n{i + 1}" for i in range(14)), ["diagram"]),
            "node with no note": ("architecture.md", "  api -.queue.-> worker", "  api -.queue.-> worker\n  api --> db", ["diagram"]),
            "long note": ("flows/place-an-order.md", "# Place an order", "# Place an order\n" + "\n" * 60, ["note length"]),
        }
        for label, (name, old, new, want) in cases.items():
            with self.subTest(label):
                folder, repo = self.copy_good()
                self.edit(folder / name, old, new)
                code, out = run_check(folder, repo)
                self.assertEqual(code, 1, f"{label}: the checker passed a broken map.\n{out}")
                self.assertEqual(failed_checks(out), want, f"{label}: wrong checks failed.\n{out}")

    def test_structure_rules_from_the_templates(self):
        """Sections, index line format and placement, flow steps and alias uniqueness are enforced."""
        cases = {
            "component without Why": ("components/api.md", "## Why\n", "## Reason\n", ["notes and properties"]),
            "decision without Consequences": ("decisions/queue-between-api-and-worker.md", "## Consequences", "## After", ["notes and properties"]),
            "flow without steps": ("flows/place-an-order.md", "1. `OrderService", "- `OrderService", ["notes and properties"]),
            "alias equals a note name": ("terms/Order.md", "aliases: [purchase, basket]", "aliases: [purchase, api]", ["notes and properties"]),
            "index line without summary": ("index.md", "- [[api]]: accepts orders and queues receipt jobs", "- [[api]]", ["index lists every note"]),
            "note under the wrong index section": ("index.md", "## Terms\n- [[Order]]", "## Terms\n- [[api]]: dup\n- [[Order]]", ["index lists every note"]),
            "unknown index section": ("index.md", "## Questions", "## Misc", ["index lists every note"]),
        }
        for label, (name, old, new, want) in cases.items():
            with self.subTest(label):
                folder, repo = self.copy_good()
                self.edit(folder / name, old, new)
                code, out = run_check(folder, repo)
                self.assertEqual(failed_checks(out), want, f"{label}\n{out}")

    def test_hyphenated_component_ids_in_the_diagram(self):
        """`entry-router --> x` is two nodes, not three: a hyphen inside an id is not an edge."""
        folder, repo = self.copy_good()
        (folder / "components" / "api.md").rename(folder / "components" / "order-api.md")
        for rel in ("architecture.md", "index.md", "components/worker.md", "components/shared.md", "flows/place-an-order.md",
                    "decisions/queue-between-api-and-worker.md", "terms/Order.md"):
            p = folder / rel
            p.write_text(re.sub(r"(?<![-\w])api(?![-\w/])", "order-api", p.read_text(encoding="utf-8")), encoding="utf-8")
        code, out = run_check(folder, repo)
        self.assertIn("PASS diagram: 3 nodes", out)
        self.assertEqual(code, 0, out)

    def test_slash_commands_and_placeholders_are_not_paths(self):
        folder, repo = self.copy_good()
        self.edit(folder / "components" / "shared.md", "No I/O.", "No I/O. Run `/repo-map check`; digests are `news/<YYYY>-W<ww>.md`; globs like `src/**/*.py`.")
        code, out = run_check(folder, repo)
        self.assertEqual(code, 0, out)

    def test_bare_file_names_must_be_full_paths(self):
        """`server.py` is not at the root, so it fails: SKILL.md asks for full paths from the root."""
        folder, repo = self.copy_good()
        self.edit(folder / "components" / "shared.md", "No I/O.", "No I/O. See `server.py`.")
        code, out = run_check(folder, repo)
        self.assertEqual(failed_checks(out), ["paths exist"], out)

    def test_note_in_wrong_folder_fails(self):
        folder, repo = self.copy_good()
        (folder / "questions" / "which-broker.md").rename(folder / "terms" / "which-broker.md")
        code, out = run_check(folder, repo)
        self.assertEqual(failed_checks(out), ["notes and properties"], out)

    def test_duplicate_note_names_fail(self):
        """A term and a component with the same name (any case) make [[links]] ambiguous in Obsidian."""
        folder, repo = self.copy_good()
        (folder / "terms" / "API.md").write_text("---\ntype: term\n---\n# API\n\nThe orders interface.\n", encoding="utf-8")
        self.edit(folder / "index.md", "## Decisions", "- [[API]]: the orders interface\n\n## Decisions")
        code, out = run_check(folder, repo)
        self.assertEqual(failed_checks(out), ["notes and properties"], out)
        self.assertIn("share the name", out)

    def test_aliases_are_shown_with_piped_links(self):
        """[[Order|purchase]] passes; a bare [[purchase]] fails with the fix, because Obsidian's docs don't say it resolves."""
        code, out = run_check(FIXTURES / "good", FIXTURES / "repo")
        self.assertIn("PASS links resolve", out)
        self.assertIn("[[Order|purchase]]", (FIXTURES / "good" / "terms" / "Customer.md").read_text(encoding="utf-8"))
        folder, repo = self.copy_good()
        self.edit(folder / "terms" / "Customer.md", "[[Order|purchase]]", "[[purchase]]")
        code, out = run_check(folder, repo)
        self.assertEqual(failed_checks(out), ["links resolve"], out)
        self.assertIn("write [[Order|purchase]]", out)

    def test_column_zero_block_lists_are_read(self):
        """`key:` then `- item` at column 0 is valid YAML (PyYAML writes it): an invented item must still fail."""
        folder, repo = self.copy_good()
        self.edit(folder / "components" / "api.md", 'depends_on: ["[[shared]]"]', 'depends_on:\n- "[[shared]]"\n- "[[NoSuchNote]]"')
        self.edit(folder / "components" / "api.md", "key_names: [OrderService, create_order, enqueue_receipt]",
                  "key_names:\n- InventedGateway\n- OrderService")
        code, out = run_check(folder, repo)
        self.assertEqual(failed_checks(out), ["links resolve", "names occur in code"], out)

    def test_flow_step_symbols_and_prose_line_refs_are_checked(self):
        folder, repo = self.copy_good()
        self.edit(folder / "flows" / "place-an-order.md", "3. [[worker]]",
                  "3. `InventedGateway.charge_card` charges the card.\n4. [[worker]]")
        code, out = run_check(folder, repo)
        self.assertEqual(failed_checks(out), ["names occur in code"], out)
        self.assertIn("InventedGateway", out)
        folder, repo = self.copy_good()
        self.edit(folder / "flows" / "place-an-order.md", "3. [[worker]]", "3. see api/server.py:12, then [[worker]]")
        code, out = run_check(folder, repo)
        self.assertEqual(failed_checks(out), ["no path:line references"], out)

    def test_mime_types_protocols_refs_and_packages_are_not_paths(self):
        folder, repo = self.copy_good()
        self.edit(folder / "components" / "shared.md", "No I/O.",
                  "No I/O. Sends `application/json` over `HTTP/1.1`; deploys from `origin/main`; uses `@nestjs/core` and `and/or`.")
        code, out = run_check(folder, repo)
        self.assertEqual(code, 0, out)

    def test_absolute_paths_fail(self):
        """An absolute path that exists (here, the fixture repo's own file, by absolute path) is still not a repo path."""
        folder, repo = self.copy_good()
        target = (repo / "shared" / "models.py").resolve()
        self.edit(folder / "components" / "shared.md", "path: shared/models.py", f"path: {target}")
        code, out = run_check(folder, repo)
        self.assertEqual(failed_checks(out), ["paths exist"], out)
        self.assertIn("outside the repository", out)

    def test_huge_repo_is_incomplete_not_pass(self):
        """When names cannot be searched (too many files), the verdict is INCOMPLETE with exit 2, never PASS.
        Runs the checker in-process with the file cap lowered to 1, instead of writing 50,000 files."""
        import contextlib
        import importlib
        import io
        folder, repo = self.copy_good()
        sys.path.insert(0, str(SKILL_DIR))
        cm = importlib.reload(importlib.import_module("check_map"))
        cm.MAX_SOURCE_FILES = 1
        buf = io.StringIO()
        old_env = {k: os.environ.pop(k) for k in list(os.environ) if k.startswith("GIT_")}
        try:
            with contextlib.redirect_stdout(buf):
                code = cm.main([str(folder), "--repo", str(repo)])
        finally:
            os.environ.update(old_env)
            importlib.reload(cm)
        out = buf.getvalue()
        self.assertEqual(code, 2, out)
        self.assertIn("NOT RUN names occur in code", out)
        self.assertIn("SUMMARY INCOMPLETE", out)

    def test_block_list_properties_parse(self):
        """`key:` followed by `- item` lines is a list, as Obsidian writes it."""
        folder, repo = self.copy_good()
        self.edit(folder / "components" / "api.md", "key_names: [OrderService, create_order, enqueue_receipt]",
                  "key_names:\n  - OrderService\n  - create_order\n  - enqueue_receipt")
        code, out = run_check(folder, repo)
        self.assertEqual(code, 0, out)
        self.assertIn("names occur in code: 6 checked", out)

    def test_every_link_in_a_list_property_is_checked(self):
        """A broken second link in `components: ["[[api]]", "[[nope]]"]` must not slip through the list parser."""
        folder, repo = self.copy_good()
        self.edit(folder / "flows" / "place-an-order.md", '"[[worker]]"]', '"[[nope]]"]')
        code, out = run_check(folder, repo)
        self.assertEqual(failed_checks(out), ["links resolve"], out)

    def test_fenced_examples_are_not_claims(self):
        folder, repo = self.copy_good()
        self.edit(folder / "flows" / "place-an-order.md", "1. ", "```text\n`no/such/path.py` and [[nowhere]]\n```\n\n1. ")
        code, out = run_check(folder, repo)
        self.assertEqual(code, 0, out)

    def test_map_inside_the_repo_does_not_vouch_for_itself(self):
        """In the default layout (docs/repo-map/ inside the repo) an invented name must not be found in the notes themselves."""
        folder, repo = self.copy_good()
        inside = repo / "docs" / "repo-map"
        shutil.copytree(folder, inside)
        self.edit(inside / "components" / "worker.md", "key_names: [send_receipt]", "key_names: [InventedThing]")
        code, out = run_check(inside, repo)
        self.assertEqual(failed_checks(out), ["names occur in code"], out)

    def test_whole_names_only(self):
        """`OrderServ` must not pass just because `OrderService` exists."""
        folder, repo = self.copy_good()
        self.edit(folder / "components" / "api.md", "[OrderService,", "[OrderServ,")
        code, out = run_check(folder, repo)
        self.assertEqual(failed_checks(out), ["names occur in code"], out)

    def test_ports_and_image_tags_are_not_line_references(self):
        folder, repo = self.copy_good()
        self.edit(folder / "components" / "shared.md", "No I/O.", "No I/O. Tests use `postgres:16` on `localhost:5432` in `node:20-alpine`.")
        code, out = run_check(folder, repo)
        self.assertEqual(code, 0, out)

    def test_diagram_counts_ampersand_and_labelled_edges(self):
        folder, repo = self.copy_good()
        self.edit(folder / "architecture.md", "  api -.queue.-> worker", "  api -.queue.-> worker\n  api & worker -->|reads| shared[(Shared)]")
        code, out = run_check(folder, repo)
        self.assertIn("PASS diagram: 3 nodes", out)

    def test_names_in_dependency_folders_do_not_count(self):
        folder, repo = self.copy_good()
        (repo / "node_modules").mkdir()
        (repo / "node_modules" / "x.js").write_text("send_invoice()", encoding="utf-8")
        self.edit(folder / "components" / "worker.md", "[send_receipt]", "[send_invoice]")
        code, out = run_check(folder, repo)
        self.assertEqual(failed_checks(out), ["names occur in code"], out)


class RenderTests(Base):
    RENDER = SKILL_DIR / "render_map.py"

    def render(self, folder, out):
        r = subprocess.run([sys.executable, "-I", str(self.RENDER), str(folder), "--out", str(out)],
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return out.read_text(encoding="utf-8")

    def data(self, page):
        import json
        m = re.search(r"^const D = (.*);$", page, re.M)
        self.assertTrue(m, "map.html lost its embedded data line.")
        return json.loads(m.group(1).replace("<\\/", "</"))

    def test_page_holds_every_note_and_the_graph(self):
        page = self.render(FIXTURES / "good", self.tmp() / "map.html")
        d = self.data(page)
        self.assertEqual(sorted(n["rel"] for n in d["notes"]),
                         sorted(p.relative_to(FIXTURES / "good").as_posix() for p in (FIXTURES / "good").rglob("*.md")))
        self.assertEqual(sorted(n["name"] for n in d["graph"]["nodes"]), ["api", "shared", "worker"])
        self.assertEqual(sorted(map(tuple, d["graph"]["edges"])), [("api", "shared"), ("worker", "shared")])
        self.assertEqual(d["commit"], "no git")

    def test_page_is_self_contained_and_escapes_note_text(self):
        """No scripts or libraries fetched (Google Fonts is the only outside host); note text cannot close the script or inject markup."""
        folder, repo = self.copy_good()
        self.edit(folder / "terms" / "Order.md", "A customer's request", "</script><img src=x onerror=alert(1)> A customer's request")
        page = self.render(folder, self.tmp() / "map.html")
        self.assertNotRegex(page, r"<script[^>]+src=|@import", "map.html must not load scripts or imported styles.")
        hosts = set(re.findall(r"https?://([^/\"'\s)]+)", page))
        self.assertLessEqual(hosts, {"fonts.googleapis.com", "fonts.gstatic.com"}, f"unexpected hosts: {hosts}")
        self.assertEqual(page.count("</script>"), 1, "note text closed the script block early.")
        outside_data = re.sub(r"^const D = .*;$", "", page, flags=re.M)
        self.assertNotIn("<img src=x", outside_data, "note text reached the markup unescaped.")
        data_line = re.search(r"^const D = (.*);$", page, re.M).group(1)
        self.assertNotIn("<", data_line, "the data line must escape every '<' so note text cannot end or re-open the script.")
        self.assertIn("var esc", page)
        self.assertIn('<meta name="referrer" content="no-referrer">', page)

    def test_comment_then_script_in_a_note_cannot_blank_the_page(self):
        """`<!--` followed by `<script ` inside the data would put the HTML parser in a state where the real
        </script> no longer ends the script. With every < escaped, the data holds neither."""
        folder, repo = self.copy_good()
        self.edit(folder / "components" / "api.md", "Accepts orders", "Legacy layout opens <!--[if IE]> and loads a <script async> tag. Accepts orders")
        page = self.render(folder, self.tmp() / "map.html")
        script = page[page.index("<script>") + len("<script>"):]
        self.assertNotIn("<!--", script.split("</script>")[0])
        self.assertNotRegex(script.split("</script>")[0], r"<script[\s>]")
        self.assertTrue(script.rstrip().endswith("</script></body></html>"), "the page's own </script> must close the script.")

    def test_unique_ids_for_unicode_and_punctuation_variants(self):
        folder, repo = self.copy_good()
        for name in ("注文", "顧客", "Order-Item", "order_item"):
            (folder / "terms" / f"{name}.md").write_text(f"---\ntype: term\n---\n# {name}\n\nA test term.\n", encoding="utf-8")
        d = self.data(self.render(folder, self.tmp() / "map.html"))
        ids = [n["id"] for n in d["notes"]]
        self.assertEqual(len(ids), len(set(ids)), f"duplicate ids: {sorted(ids)}")
        self.assertIn("n-注文", ids)

    def test_no_outbound_request_but_fonts(self):
        """By default the page makes no request at all; with --fonts it may reach only Google Fonts."""
        page = re.sub(r"^const D = .*;$", "", self.render_with("--fonts"), flags=re.M)
        for pattern in (r"sendBeacon", r"\bfetch\s*\(", r"XMLHttpRequest", r"new\s+Image\s*\(", r"WebSocket", r"EventSource",
                        r"import\s*\(", r"<iframe", r"<script[^>]+src=", r"@import", r"window\.open", r"location\s*=\s*['\"]http"):
            self.assertNotRegex(page, pattern, f"map.html contains an outbound request: {pattern}")
        urls = re.findall(r"""(?:href|src|action)\s*=\s*["']([^"'#][^"']*)["']|url\(\s*["']?([^)"']+)""", page)
        targets = {u for pair in urls for u in pair if u and not u.startswith("#")}  # in-page anchors and SVG marker refs
        hosts = {re.sub(r"^(https?:)?//", "", t).split("/")[0] for t in targets if t.startswith(("http", "//"))}
        self.assertLessEqual(hosts, {"fonts.googleapis.com", "fonts.gstatic.com"}, f"unexpected hosts: {hosts}")
        self.assertFalse({t for t in targets if not t.startswith(("http", "//"))}, "relative or data URLs in the template")
        default = re.sub(r"^const D = .*;$", "", self.render(FIXTURES / "good", self.tmp() / "map.html"), flags=re.M)
        self.assertNotRegex(default, r"https?://|//[a-z0-9.-]+\.[a-z]{2,}/", "by default the page must make no network request at all.")
        legacy = re.sub(r"^const D = .*;$", "", self.render_with("--offline"), flags=re.M)
        self.assertNotRegex(legacy, r"https?://", "--offline must still mean no network request.")

    def render_with(self, flag):
        out = self.tmp() / "map.html"
        r = subprocess.run([sys.executable, "-I", str(self.RENDER), str(FIXTURES / "good"), "--out", str(out), flag],
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return out.read_text(encoding="utf-8")

    def test_page_has_the_four_themes_sizes_and_a_phone_layout(self):
        page = self.render(FIXTURES / "good", self.tmp() / "map.html")
        for needle in (":root {", "@media (prefers-color-scheme: dark)", ':root[data-theme="dark"]', ':root[data-theme="paper"]',
                       ':root[data-size="lg"]', "@media (max-width: 560px)", "prefers-reduced-motion", 'value="system"'):
            self.assertIn(needle, page)

    def test_learning_features_are_present(self):
        """Flow walkthrough, guided path, read marks, flashcards, filter and the two-step reset."""
        page = self.render(FIXTURES / "good", self.tmp() / "map.html")
        for needle in ("function stepTo", "data-step", "ArrowRight", "Guided path", "data-done", 'id="qnext"', 'id="filter"', 'id="resetYes"'):
            self.assertIn(needle, page)
        self.assertIn("try { state = JSON.parse(localStorage", page, "storage access must be wrapped in try/catch.")

    def test_refuses_a_folder_without_an_index(self):
        empty = self.tmp()
        r = subprocess.run([sys.executable, "-I", str(self.RENDER), str(empty)], capture_output=True, text=True, timeout=60)
        self.assertEqual(r.returncode, 1)
        self.assertIn("no index.md", r.stdout)

    def test_graph_labels_are_never_below_12px(self):
        page = self.render(FIXTURES / "good", self.tmp() / "map.html")
        sizes = [int(x) for x in re.findall(r"\.s-(?:t|sub) \{[^}]*font-size: (\d+)px", page)]
        self.assertEqual(len(sizes), 2, "lost the graph label styles")
        self.assertGreaterEqual(min(sizes), 12)
        self.assertNotIn("width: 100%", re.search(r"figure\.viz svg \{[^}]*\}", page).group(0), "the graph must not shrink to fit")


def deep_chain_map(base, n=15):
    """A map of n components in a single dependency chain (c00 -> c01 -> ... ), the shape that broke the old layout."""
    repo, folder = base / "repo", base / "map"
    (repo / "src").mkdir(parents=True)
    (repo / "src" / "chain.py").write_text("".join(f"def step_{i:02d}():\n    pass\n" for i in range(n)), encoding="utf-8")
    (folder / "components").mkdir(parents=True)
    names = [f"c{i:02d}" for i in range(n)]
    for i, name in enumerate(names):
        deps = f'depends_on: ["[[{names[i + 1]}]]"]\n' if i + 1 < n else ""
        (folder / "components" / f"{name}.md").write_text(
            f"---\ntype: component\nkind: library\npath: src/chain.py\nowner: UNKNOWN\n{deps}provides: step {i}\n"
            f"key_names: [step_{i:02d}]\n---\n# {name}\n\n## What\nStep {i}.\n\n## Why\nUNKNOWN.\n\n## Boundaries and invariants\nNone.\n",
            encoding="utf-8")
    diagram = "\n".join(f"  {names[i]} --> {names[i + 1]}" for i in range(n - 1))
    (folder / "architecture.md").write_text(
        "---\ntype: architecture\n---\n# chain: architecture\n\n## Bird's-eye view\n\nA chain.\n\n## Diagram\n\n```mermaid\nflowchart LR\n"
        f"{diagram}\n  class {','.join(names)} internal-link;\n```\n\n## Boundaries and invariants\n\n- None.\n\n## Build and test\n\n- None.\n\n"
        "## What this map can't see\n\n- Nothing.\n", encoding="utf-8")
    (folder / "index.md").write_text(
        "---\ntype: index\nrepo: chain\ncommit: no git\ndate: 2026-11-23\n---\n# chain: repo map\n\nStart with [[architecture]].\n\n"
        "## Components\n" + "".join(f"- [[{x}]]: a step\n" for x in names), encoding="utf-8")
    return folder, repo, names


@unittest.skipUnless(shutil.which("node"), "NOT RUN: node is not installed, so the page's layout function cannot be run")
class LayoutTests(Base):
    """Runs the page's own JS layout() in node at phone and desktop widths, on the deep chain that used to be unreadable."""
    RENDER = SKILL_DIR / "render_map.py"

    def run_layout(self, page, width):
        js_src = page[page.index("<script>") + len("<script>"):page.rindex("</script>")]
        start = js_src.index("  function layout(names) {")
        end = js_src.index("  /* opts:")
        data = re.search(r"^const D = (.*);$", js_src, re.M).group(1)
        program = (f"const D = {data};\nconst document = {{ getElementById: () => ({{ clientWidth: {width} }}) }};\n"
                   "var GX = 40, GY = 56;\n" + js_src[start:end] +
                   "\nconst names = D.graph.nodes.map(n => n.name);\nconsole.log(JSON.stringify(layout(names)));\n")
        script = self.tmp() / "layout.js"
        script.write_text(program, encoding="utf-8")
        r = subprocess.run(["node", str(script)], capture_output=True, text=True, timeout=60)
        self.assertEqual(r.returncode, 0, r.stderr)
        import json
        return json.loads(r.stdout)

    def test_deep_chain_wraps_to_the_width_and_reads_in_order(self):
        folder, repo, names = deep_chain_map(self.tmp())
        code, out = run_check(folder, repo)
        self.assertNotIn("FAIL", out, "the generated 15-component map must itself pass the checker")
        page = RenderTests.render(self, folder, self.tmp() / "map.html")
        for width, per in ((343, 1), (848, 3)):
            with self.subTest(width=width):
                L = self.run_layout(page, width)
                xs = sorted({p["x"] for p in L["pos"].values()})
                self.assertEqual(len(xs), per, f"at {width}px expected {per} boxes per row")
                self.assertLessEqual(L["W"], max(width, 224) + 24, "the graph is wider than the column")
                order = sorted(names, key=lambda n: (L["pos"][n]["y"], L["pos"][n]["x"]))
                self.assertEqual(order, names, "a dependant must come before what it depends on, in reading order")
                self.assertEqual(len({(p["x"], p["y"]) for p in L["pos"].values()}), len(names), "boxes overlap")

    def test_sixteen_components_fail_the_checker(self):
        folder, repo, names = deep_chain_map(self.tmp(), n=16)
        code, out = run_check(folder, repo)
        self.assertIn("16 component notes, cap 15", out)


@unittest.skipUnless(shutil.which("git"), "NOT RUN: git is not installed")
class GitTests(Base):
    def git(self, repo, *args):
        env = clean_env()
        env.update(GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.invalid",  # privacy: allow
                   GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@example.invalid")  # privacy: allow
        out = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, env=env, timeout=30)
        self.assertEqual(out.returncode, 0, out.stderr)
        return out.stdout.strip()

    def committed_repo(self):
        folder, repo = self.copy_good()
        # The git dir lives beside the checkout: sandboxes often refuse writes to .git/config.
        self.git(repo, "init", "-q", "--template=", f"--separate-git-dir={repo.parent / 'repo.gitdir'}")
        self.git(repo, "add", "-A")
        self.git(repo, "commit", "-qm", "init")
        sha = self.git(repo, "rev-parse", "--short=12", "HEAD")
        self.edit(folder / "index.md", "commit: no git", f"commit: {sha}")
        return folder, repo

    def test_real_stamp_passes_with_no_drift(self):
        folder, repo = self.committed_repo()
        code, out = run_check(folder, repo)
        self.assertEqual(code, 0, out)
        self.assertIn("PASS drift", out)

    def test_later_commit_to_a_component_path_warns(self):
        """Drift is a warning, not a failure: the notes may still be right."""
        folder, repo = self.committed_repo()
        (repo / "api" / "server.py").write_text("# changed\n" + (repo / "api" / "server.py").read_text(), encoding="utf-8")
        self.git(repo, "commit", "-qam", "change api")
        code, out = run_check(folder, repo)
        self.assertEqual(code, 0, out)
        self.assertIn("WARN drift: 1 commit", out)

    def test_paths_climbing_out_of_the_work_tree_fail(self):
        folder, repo = self.committed_repo()
        (repo.parent / "outside.txt").write_text("x", encoding="utf-8")
        self.edit(folder / "components" / "shared.md", "path: shared/models.py", "path: ../outside.txt")
        code, out = run_check(folder, repo)
        self.assertEqual(failed_checks(out), ["paths exist"], out)
        self.assertIn("outside the repository", out)

    def test_decision_commit_source_is_checked(self):
        folder, repo = self.committed_repo()
        sha = self.git(repo, "rev-parse", "--short=12", "HEAD")
        self.edit(folder / "decisions" / "queue-between-api-and-worker.md", "source: api/server.py", f"source: {sha}")
        code, out = run_check(folder, repo)
        self.assertIn("PASS decision sources: 1 commit(s) found", out)
        self.edit(folder / "decisions" / "queue-between-api-and-worker.md", f"source: {sha}", "source: deadbeefcafe")
        code, out = run_check(folder, repo)
        self.assertEqual(failed_checks(out), ["decision sources"], out)

    def test_unknown_commit_fails(self):
        folder, repo = self.committed_repo()
        sha = re.search(r"commit: (\w+)", (folder / "index.md").read_text()).group(1)
        self.edit(folder / "index.md", sha, "deadbee")
        code, out = run_check(folder, repo)
        self.assertEqual(failed_checks(out), ["stamp commit"], out)


class SkillTextTests(unittest.TestCase):
    def setUp(self):
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        m = re.match(r"---\n(.*?)\n---\n(.*)\Z", text, re.S)
        self.assertTrue(m, "skills/repo-map/SKILL.md has no frontmatter between --- lines.")
        self.front, self.body = m.group(1), m.group(2)
        self.check_src = CHECK.read_text(encoding="utf-8")

    def test_frontmatter_stays_within_the_agent_skills_spec(self):
        """Fields outside the spec make claude.ai uploads and other agents reject the skill."""
        fields = set(re.findall(r"^([A-Za-z][\w-]*):", self.front, re.M))
        self.assertLessEqual(fields, SPEC_FIELDS, f"non-spec fields: {sorted(fields - SPEC_FIELDS)}")
        self.assertIn("name: repo-map", self.front)
        desc = re.search(r"^description: (.*)$", self.front, re.M).group(1)
        self.assertLessEqual(len(desc), 1024, "description is over the spec's 1024 characters.")

    def test_five_modes(self):
        for mode in ("map", "page", "ask", "quiz", "check"):
            self.assertIn(f"## Mode: {mode}", self.body)

    def test_asks_before_writing_and_never_edits_agent_files(self):
        self.assertIn("Ask before the first write", self.body)
        self.assertRegex(self.body, r"Never edit the repository's code, `CLAUDE.md`, `AGENTS.md`")
        self.assertIn("## Mode: check\n\nWrite nothing", self.body)
        self.assertIn("Write only on a yes", self.body)

    def test_caps_match_the_checker(self):
        """SKILL.md and check_map.py must state the same limits."""
        def get(name):
            return re.search(rf"{name} = (\d+)", self.check_src).group(1)
        self.assertIn(f"A note is at most {get('MAX_NOTE_LINES')} lines", self.body)
        self.assertIn(f"`index.md` and `architecture.md` at most {get('MAX_HUB_LINES')}", self.body)
        self.assertIn(f"The diagram has at most {get('MAX_DIAGRAM_NODES')} nodes", self.body)

    def test_every_note_type_has_a_template_that_matches_the_checker(self):
        """The templates are what keep runs consistent: each must carry its type's properties and sections, in order."""
        sys.path.insert(0, str(SKILL_DIR))
        import check_map
        for kind, (folder, needed) in check_map.REQUIRED.items():
            with self.subTest(kind):
                path = SKILL_DIR / "assets" / f"{kind}.md"
                self.assertTrue(path.is_file(), f"no template assets/{kind}.md")
                self.assertIn(f"`{kind}.md`", self.body, f"SKILL.md does not point to the {kind} template.")
                props, body = check_map.parse_frontmatter(path.read_text(encoding="utf-8"))
                self.assertEqual(props.get("type"), kind)
                for p in needed:
                    self.assertTrue(props.get(p), f"assets/{kind}.md lacks property {p}")
                headings = re.findall(r"^## (.+)$", check_map.strip_fences(body), re.M)
                want = list(check_map.SECTIONS.get(kind, ()))
                self.assertEqual([h for h in headings if h in want], want, f"assets/{kind}.md sections are missing or out of order")
        index_props, index_body = check_map.parse_frontmatter((SKILL_DIR / "assets" / "index.md").read_text(encoding="utf-8"))
        sections = re.findall(r"^## (.+)$", index_body, re.M)
        self.assertEqual(sections, list(check_map.INDEX_SECTIONS), "the index template's sections differ from the checker's")


if __name__ == "__main__":
    unittest.main()
