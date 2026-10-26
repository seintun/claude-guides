"""Print one section of the playbook or the cheat sheet, so a session never loads a whole file.

Read can't follow #anchors, and the playbook is about 1,500 lines. Use this instead.

Usage: python3 -I tools/section.py <id> [<id> ...]
       python3 -I tools/section.py --list
Ids:
  9.5, 10, 17A   a numbered section (a whole section, e.g. 9, includes its subsections)
  F, M           a template from §16
  law-7          one of the ten laws in §2
  cs:3           a section of the cheat sheet (playbook/claude-cheat-sheet.md)
Exit code 1 if an id is unknown.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PLAYBOOK = ROOT / "playbook" / "agent-harness-playbook.md"
CHEATSHEET = ROOT / "playbook" / "claude-cheat-sheet.md"


def headings(lines):
    """Yield (index, level, title) for Markdown headings outside code fences."""
    fence = False
    for i, line in enumerate(lines):
        if line.startswith("```"):
            fence = not fence
            continue
        m = re.match(r"(#{1,6}) (.*)", line)
        if m and not fence:
            yield i, len(m.group(1)), m.group(2).strip()


def key_of(title, cheatsheet):
    """The id a heading answers to, or None."""
    if cheatsheet:
        m = re.match(r"(\d+)\.? ", title)
        return f"cs:{m.group(1)}" if m else None
    m = re.match(r"Law (\d+)\.", title)
    if m:
        return f"law-{m.group(1)}"
    m = re.match(r"([A-M])\. ", title)
    if m:
        return m.group(1)
    m = re.match(r"(\d+[A-Z]?(?:\.\d+)?)\.? ", title)
    return m.group(1).upper() if m else None


def index(path, cheatsheet=False):
    lines = path.read_text(encoding="utf-8").splitlines()
    heads = list(headings(lines))
    found = {}
    for n, (i, level, title) in enumerate(heads):
        end = len(lines)
        for j, lvl, _ in heads[n + 1:]:
            if lvl <= level:
                end = j
                break
        key = key_of(title, cheatsheet)
        if key and key not in found:
            found[key] = (title, i, end)
    return lines, found


def main(argv):
    if not argv:
        print(__doc__.strip())
        return 1
    pb_lines, pb = index(PLAYBOOK)
    cs_lines, cs = index(CHEATSHEET, cheatsheet=True)
    if argv == ["--list"]:
        for key, (title, i, end) in list(pb.items()) + list(cs.items()):
            print(f"{key:7} {end - i:4} lines  {title}")
        return 0
    status = 0
    for raw in argv:
        key = raw if raw.startswith(("cs:", "law-")) else raw.upper().lstrip("§")
        lines, table, name = (cs_lines, cs, CHEATSHEET.name) if key.startswith("cs:") else (pb_lines, pb, PLAYBOOK.name)
        if key not in table:
            print(f"unknown section id: {raw} (run with --list)", file=sys.stderr)
            status = 1
            continue
        title, i, end = table[key]
        print(f"<!-- {name} lines {i + 1}-{end}: {title} -->")
        print("\n".join(lines[i:end]).rstrip() + "\n")
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
