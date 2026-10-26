"""Check every relative link in the repository's Markdown: the target exists and any #anchor matches a heading.

Usage (from the repository root): python3 -I tools/check_links.py [paths...]
Skips links inside code fences and inline code, external URLs, and mailto links.
Anchors follow GitHub's heading slugs. Exits 1 if any link is broken.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", "build", "node_modules", ".playwright-mcp"}
# Test fixtures are quoted material; .claude/worktrees holds other checkouts of this repo.
SKIP_PATHS = {os.path.join(ROOT, "tests", "fixtures"), os.path.join(ROOT, ".claude", "worktrees")}


def slugs(path, cache={}):
    if path in cache:
        return cache[path]
    seen, out, fence = {}, set(), False
    for line in open(path, encoding="utf-8"):
        if line.strip().startswith("```"):
            fence = not fence
            continue
        m = None if fence else re.match(r"^#{1,6}\s+(.*?)\s*#*\s*$", line)
        if not m:
            continue
        text = re.sub(r"`([^`]*)`", r"\1", m.group(1))
        text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
        s = re.sub(r"[^\w\- ]", "", text.strip().lower(), flags=re.UNICODE).replace(" ", "-")
        n = seen.get(s, 0)
        out.add(s if n == 0 else f"{s}-{n}")
        seen[s] = n + 1
    cache[path] = out
    return out


def markdown_files(paths):
    if paths:
        yield from paths
        return
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS and os.path.join(d, x) not in SKIP_PATHS]
        for f in files:
            if f.endswith(".md") or f == "llms.txt":
                yield os.path.join(d, f)


broken, checked = [], 0
for md in markdown_files(sys.argv[1:]):
    md = os.path.abspath(md)
    fence = False
    for no, line in enumerate(open(md, encoding="utf-8"), 1):
        if line.strip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        line = re.sub(r"`[^`]*`", "", line)
        for target in re.findall(r"\]\(([^)\s]+)\)", line):
            if re.match(r"(https?|mailto):", target):
                continue
            checked += 1
            file_part, _, anchor = target.partition("#")
            dest = md if not file_part else os.path.normpath(os.path.join(os.path.dirname(md), file_part))
            rel = os.path.relpath(md, ROOT)
            if not os.path.exists(dest):
                broken.append(f"{rel}:{no}: missing file {file_part}")
                continue
            if anchor and dest.endswith(".md") and anchor not in slugs(dest):
                broken.append(f"{rel}:{no}: no heading #{anchor} in {os.path.relpath(dest, ROOT)}")

for b in broken:
    print("FAIL", b)
print(f"{'FAIL' if broken else 'PASS'} links: {checked} checked, {len(broken)} broken")
sys.exit(1 if broken else 0)
