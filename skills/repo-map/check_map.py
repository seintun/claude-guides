#!/usr/bin/env python3
"""Check a repo-map folder (linked notes with flat YAML properties) against the repository it describes.

Usage: python3 check_map.py <map-folder> [--repo <repository root>]

Prints one PASS, FAIL, WARN or NOT RUN line per check and exits 1 if any check fails.
Standard library only, so it runs wherever the skill is installed.
"""
import argparse
import os
import pathlib
import re
import subprocess
import sys

MAX_NOTE_LINES = 60
MAX_HUB_LINES = 200          # index.md and architecture.md
MAX_DIAGRAM_NODES = 15
ARCH_SECTIONS = ("Bird's-eye view", "Diagram", "Boundaries and invariants", "Build and test", "What this map can't see")
SECTIONS = {  # type -> the ## sections its body must have (the templates in assets/ show them)
    "architecture": ARCH_SECTIONS,
    "component": ("What", "Why", "Boundaries and invariants"),
    "decision": ("Context", "Decision", "Why", "Consequences"),
}
KINDS = ("service", "website", "job", "library", "resource")  # what render_map.py colours and SKILL.md lists
INDEX_SECTIONS = {"Components": "component", "Terms": "term", "Decisions": "decision", "Flows": "flow", "Questions": "question"}
INDEX_LINE = re.compile(r"^- \[\[([^\]|#]+)\]\]: \S")
REQUIRED = {  # type -> (folder, required properties)
    "index": ("", ("repo", "commit", "date")),
    "architecture": ("", ()),
    "component": ("components", ("kind", "path", "owner")),
    "term": ("terms", ()),
    "decision": ("decisions", ("status", "source")),
    "flow": ("flows", ("entry", "components")),
    "question": ("questions", ("status", "ask")),
}
SKIP_DIRS = {".git", "node_modules", "vendor", "dist", "build", "target", ".venv", "venv", "__pycache__", ".next", ".tox", ".obsidian"}
MAX_SOURCE_BYTES = 2_000_000
MAX_SOURCE_FILES = 50_000
EXTS = r"md|py|pyi|ts|tsx|js|jsx|mjs|cjs|json|ya?ml|toml|go|rs|java|kt|kts|scala|rb|php|cs|fs|swift|m|c|cc|cpp|h|hpp|sh|bash|txt|cfg|ini|lock|gradle|xml|sql|proto|graphql|tf|vue|svelte|ex|exs|erl|clj|dart|lua|r|html|css|scss"
FILE_EXT = re.compile(rf"^[\w.-]+\.({EXTS})$")
LINE_REF = re.compile(rf"\.({EXTS}):\d+")
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")

results = []
INCOMPLETE = False  # set when the names check could not run (too many files): the verdict is INCOMPLETE, exit 2


def report(status, name, detail=""):
    results.append(status)
    print(f"{status} {name}" + (f": {detail}" if detail else ""))


# ---------- notes ----------

def unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def split_list(inner):
    """Split a flow-list body on commas that sit outside quotes and outside [[...]] links."""
    parts, buf, quote, depth = [], [], None, 0
    for ch in inner:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
            buf.append(ch)
        elif ch == "[":
            depth += 1
            buf.append(ch)
        elif ch == "]":
            depth -= 1
            buf.append(ch)
        elif ch == "," and depth == 0:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    parts.append("".join(buf))
    return parts


def parse_frontmatter(text):
    """Flat YAML only: `key: value`, `key: [a, b]`, or `key:` followed by `- item` lines. Returns (props, body) or (None, text)."""
    m = re.match(r"---\n(.*?)\n---\n?(.*)\Z", text, re.S)
    if not m:
        return None, text
    props, key = {}, None
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        item = re.match(r"^(\s*)-\s+(.*)$", line) or re.match(r"^(\s*)-()$", line)
        # A list item belongs to the last key if it is indented, or at column 0 under a key with no inline value
        # (PyYAML and other tools write `key:` then `- item` without indentation).
        if item and key is not None and (item.group(1) or props[key] == [] or isinstance(props[key], list)):
            if not isinstance(props[key], list):
                props[key] = []
            props[key].append(unquote(item.group(2)))
            continue
        kv = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not kv:
            continue
        key, value = kv.group(1), kv.group(2).strip()
        if value.startswith("[") and value.endswith("]") and not value.startswith("[["):
            props[key] = [unquote(x) for x in split_list(value[1:-1]) if x.strip()]
        else:
            props[key] = unquote(value) if value else []
    return props, m.group(2)


def as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def load_notes(folder):
    notes = {}
    for path in sorted(folder.rglob("*.md")):
        if SKIP_DIRS & set(path.relative_to(folder).parts):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        props, body = parse_frontmatter(text)
        notes[path.relative_to(folder).as_posix()] = {"path": path, "name": path.stem, "text": text, "props": props, "body": body}
    return notes


FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


def strip_fences(text, keep_mermaid=False):
    """Text with fenced code blocks removed, following CommonMark: a block opens with three or more backticks or
    tildes and closes only with the same character, at least as many, and nothing after them. An unclosed block
    runs to the end."""
    out, fence, keep = [], None, False
    for line in text.split("\n"):
        m = FENCE.match(line)
        if fence is None:
            if m and not (m.group(1)[0] == "`" and "`" in m.group(2)):
                fence = m.group(1)
                keep = keep_mermaid and m.group(2).strip().startswith("mermaid")
                if keep:
                    out.append(line)
                continue
            out.append(line)
        else:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not m.group(2).strip():
                fence = None
                if keep:
                    out.append(line)
                continue
            if keep:
                out.append(line)
    return "\n".join(out)


def backticked(text):
    return re.findall(r"`([^`\n]+)`", text)


def looks_like_path(token, repo=None):
    """A backticked token is a path claim when its last part has a file extension, or it has a / and its first
    folder exists in the repository. Dot paths (`./x.md`, `.github/ci.yml`) and absolute file paths are claims too,
    so a missing or outside file fails. Slash commands (`/repo-map`), placeholders, globs, URLs, options, MIME types
    (`application/json`), protocols (`HTTP/1.1`), git refs (`origin/main`) and package names (`@nestjs/core`) are not."""
    if " " in token or token.startswith(("http:", "https:", "-", "$", "[", "~", "@")) or LINE_REF.search(token):
        return False
    if any(c in token for c in "<>*{}"):
        return False
    if token.startswith("./"):
        token = token[2:]
    last = token.rstrip("/").split("/")[-1]
    if FILE_EXT.match(last):
        return True
    if token.startswith("/"):  # an absolute path is a claim only when it names a file; otherwise a slash command
        return False
    if "/" in token:
        return repo is None or (repo / token.split("/")[0]).exists()
    return False


def path_key(token):
    """The path a token claims, without a leading ./ or trailing /."""
    return (token[2:] if token.startswith("./") else token).rstrip("/")


def inside(path, root):
    """True when path resolves inside root (both resolved, so /var and /private/var agree)."""
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


SHA = re.compile(r"^[0-9a-f]{7,40}$")
IDENT = re.compile(r"^[A-Za-z_$][\w$]*(?:(?:\.|::)[A-Za-z_$][\w$]*)*(?:\(\))?$")  # a symbol, Class.method or mod::fn


# ---------- git and source search ----------

def git(repo, *args):
    try:
        out = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return out.stdout.strip() if out.returncode == 0 else None


def in_work_tree(repo):
    return git(repo, "rev-parse", "--is-inside-work-tree") == "true"


def candidate_files(repo, exclude):
    """git's tracked and unignored files when there is a work tree, else a walk; never the map folder."""
    listed = git(repo, "ls-files", "-z", "--cached", "--others", "--exclude-standard") if in_work_tree(repo) else None
    if listed:  # empty when repo sits in an ignored folder: fall back to the walk
        for rel in listed.split("\0"):
            if rel:
                path = repo / rel
                if exclude not in path.resolve().parents and not SKIP_DIRS & set(pathlib.PurePath(rel).parts):
                    yield path
        return
    for dirpath, dirnames, filenames in os.walk(repo):
        here = pathlib.Path(dirpath)
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and (here / d).resolve() != exclude]
        for name in filenames:
            yield here / name


def source_texts(repo, exclude):
    count = 0
    for path in candidate_files(repo, exclude):
        try:
            if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_SOURCE_BYTES:
                continue
            data = path.read_bytes()
        except OSError:
            continue
        if b"\0" in data[:4096]:
            continue
        count += 1
        if count > MAX_SOURCE_FILES:
            raise OverflowError(f"more than {MAX_SOURCE_FILES} source files")
        yield data.decode("utf-8", errors="replace")


# ---------- checks ----------

def check_structure(notes):
    problems = []
    if "index.md" not in notes:
        problems.append("no index.md")
    if "architecture.md" not in notes:
        problems.append("no architecture.md")
    for rel, n in notes.items():
        props = n["props"]
        if props is None:
            problems.append(f"{rel}: no frontmatter")
            continue
        kind = props.get("type")
        if kind not in REQUIRED:
            problems.append(f"{rel}: type '{kind}' is not one of {', '.join(REQUIRED)}")
            continue
        folder, needed = REQUIRED[kind]
        where = pathlib.PurePath(rel).parent.as_posix()
        if (folder or ".") != where:
            problems.append(f"{rel}: a {kind} note belongs in {folder or 'the map root'}/")
        missing = [p for p in needed if p not in props or props[p] in ("", [])]
        if missing:
            problems.append(f"{rel}: missing {', '.join(missing)}")
        if kind == "component" and props.get("kind") and props.get("kind") not in KINDS:
            problems.append(f"{rel}: kind '{props.get('kind')}' is not one of {', '.join(KINDS)}")
    seen = {}
    for rel, n in notes.items():  # Obsidian links by note name or alias, so no two may share one (in any case)
        names = [n["name"]]
        if n["props"] and n["props"].get("type") == "term":
            names += as_list(n["props"].get("aliases"))
        for name in names:
            key = str(name).lower()
            if key in seen and seen[key] != rel:
                problems.append(f"{seen[key]} and {rel} share the name '{name}'; [[links]] to it are ambiguous")
            seen[key] = rel
    for rel, n in notes.items():
        kind = (n["props"] or {}).get("type")
        headings = {h.strip() for h in re.findall(r"^## (.+)$", strip_fences(n["body"]), re.M)}
        missing = [s for s in SECTIONS.get(kind, ()) if s not in headings]
        if missing:
            problems.append(f"{rel}: missing sections " + ", ".join(missing))
        if kind == "flow" and not re.search(r"^\s*1\. \S", n["body"], re.M):
            problems.append(f"{rel}: a flow needs numbered steps starting at 1.")
        if kind in ("term", "question") and not [l for l in n["body"].splitlines() if l.strip() and not l.startswith("#")]:
            problems.append(f"{rel}: a {kind} needs a line of text under its title")
        if kind and kind != "index" and not re.search(r"^# \S", n["body"], re.M):
            problems.append(f"{rel}: no '# Title' line")
    if problems:
        report("FAIL", "notes and properties", "; ".join(problems[:8]))
    else:
        report("PASS", "notes and properties", f"{len(notes)} notes")


def link_targets(notes):
    """Links must name a note. Obsidian's docs do not say a bare [[alias]] resolves (it writes [[Note|alias]]),
    so aliases are for search only: write [[Order|purchase]] to show an alias."""
    return {n["name"].lower() for n in notes.values()}


def alias_owner(notes):
    return {str(a).lower(): n["name"] for n in notes.values() if n["props"] and n["props"].get("type") == "term"
            for a in as_list(n["props"].get("aliases"))}


def check_links(notes):
    known, aliases = link_targets(notes), alias_owner(notes)
    broken = []
    for rel, n in notes.items():
        props_text = " ".join(str(v) for v in (n["props"] or {}).values())
        for target in WIKILINK.findall(strip_fences(n["body"]) + " " + props_text):
            t = target.strip()
            if t.lower() in aliases and t.lower() not in known:
                broken.append(f"{rel} -> [[{t}]] is an alias; write [[{aliases[t.lower()]}|{t}]]")
            elif t.lower() not in known:
                broken.append(f"{rel} -> [[{t}]]")
    if broken:
        report("FAIL", "links resolve", "; ".join(broken[:8]))
    else:
        report("PASS", "links resolve")


def check_index(notes):
    index = notes.get("index.md")
    if not index:
        report("FAIL", "index lists every note", "no index.md")
        return
    # A note counts as listed only through a valid `- [[name]]: summary` line under its type's section; the
    # architecture note may be linked from anywhere (the template links it in the opening line).
    listed = {"architecture"} if re.search(r"\[\[architecture(?:\|[^\]]*)?\]\]", index["body"], re.I) else set()
    problems = []
    counts = {}
    for n in notes.values():
        counts[n["name"].lower()] = counts.get(n["name"].lower(), 0) + 1
    # Only unique names with a known type: duplicates and unknown types are already "notes and properties" failures.
    by_name = {n["name"].lower(): (n["props"] or {}).get("type") for n in notes.values()
               if counts[n["name"].lower()] == 1 and (n["props"] or {}).get("type") in INDEX_SECTIONS.values()}
    section = None
    for line in index["body"].splitlines():
        h = re.match(r"^## (.+)$", line)
        if h:
            section = h.group(1).strip()
            if section not in INDEX_SECTIONS:
                problems.append(f"unknown section '## {section}' (use {', '.join(INDEX_SECTIONS)})")
            continue
        if section is None or not line.strip():
            continue
        m = INDEX_LINE.match(line)
        if not m:
            problems.append(f"under {section}, '{line.strip()[:40]}' is not '- [[name]]: summary'")
            continue
        want = INDEX_SECTIONS.get(section)
        got = by_name.get(m.group(1).strip().lower())
        if want and got and got != want:
            problems.append(f"[[{m.group(1).strip()}]] is a {got} but sits under {section}")
            continue
        if want:
            listed.add(m.group(1).strip().lower())
    problems = [f"not listed: {rel}" for rel, n in notes.items() if rel != "index.md" and n["name"].lower() not in listed] + problems
    if problems:
        report("FAIL", "index lists every note", "; ".join(problems[:8]))
    else:
        report("PASS", "index lists every note")


def component_paths(notes):
    return sorted({path_key(p) for n in notes.values() if n["props"] and n["props"].get("type") == "component"
                   for p in as_list(n["props"].get("path")) if p})


def resolve(p, repo, top):
    """Where a recorded path points: under --repo, or else under the git top-level. Notes record paths from the
    repository root, and --repo may be one system's folder in a monorepo, so both bases are tried."""
    if (repo / p).exists():
        return repo / p
    if top is not None and (top / p).exists():
        return top / p
    return None


def check_paths(notes, repo):
    paths = set(component_paths(notes))
    for n in notes.values():
        props = n["props"] or {}
        paths.update(path_key(p) for p in as_list(props.get("entry")) if p)
        paths.update(path_key(p) for p in as_list(props.get("source")) if looks_like_path(p, repo))
        paths.update(path_key(t) for t in backticked(strip_fences(n["body"])) if looks_like_path(t, repo))
    top_s = git(repo, "rev-parse", "--show-toplevel") if in_work_tree(repo) else None
    top = pathlib.Path(top_s) if top_s else None
    root = top or repo  # a monorepo sub-folder may point at a sibling system
    found = {p: resolve(p, repo, top) for p in paths}
    missing = sorted(p for p, where in found.items() if where is None)
    outside = sorted(p for p, where in found.items() if where is not None and (pathlib.PurePath(p).is_absolute() or not inside(where, root)))
    problems = (["not found: " + ", ".join(missing[:8])] if missing else []) + \
               (["outside the repository: " + ", ".join(outside[:8])] if outside else [])
    if problems:
        report("FAIL", "paths exist", "; ".join(problems))
    else:
        report("PASS", "paths exist", f"{len(paths)} checked")


def check_sources(notes, repo):
    """A decision's source that looks like a commit must be one; one that looks like a path must exist (checked above)."""
    shas = sorted({s for n in notes.values() if (n["props"] or {}).get("type") == "decision"
                   for s in as_list(n["props"].get("source")) if SHA.match(str(s))})
    if not shas:
        report("PASS", "decision sources", "no commit sources to check")
        return
    if not in_work_tree(repo):
        report("NOT RUN", "decision sources", f"{len(shas)} commit source(s); {repo} is not in a git work tree")
        return
    bad = [s for s in shas if git(repo, "rev-parse", "--verify", "--quiet", f"{s}^{{commit}}") is None]
    if bad and git(repo, "rev-parse", "--is-shallow-repository") == "true":
        report("NOT RUN", "decision sources", f"{len(bad)} commit(s) not found in a shallow clone")
    elif bad:
        report("FAIL", "decision sources", "not a single commit here: " + ", ".join(bad))
    else:
        report("PASS", "decision sources", f"{len(shas)} commit(s) found")


def check_stamp(notes, repo):
    props = (notes.get("index.md") or {}).get("props") or {}
    sha, date = str(props.get("commit", "")), str(props.get("date", ""))
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date) or not (sha == "no git" or re.fullmatch(r"[0-9a-f]{7,40}", sha)):
        report("FAIL", "stamp", "index.md needs commit: <sha or no git> and date: <YYYY-MM-DD>")
        return
    if sha == "no git":
        if in_work_tree(repo):
            report("WARN", "stamp", "says 'no git' but the repository is in a git work tree; stamp it with a commit")
        else:
            report("PASS", "stamp", "no git")
        return
    if not in_work_tree(repo):
        report("NOT RUN", "stamp commit", f"{repo} is not in a git work tree")
        return
    if git(repo, "rev-parse", "--verify", "--quiet", f"{sha}^{{commit}}") is None:
        if git(repo, "rev-parse", "--is-shallow-repository") == "true":
            report("NOT RUN", "stamp commit", f"{sha} not found in a shallow clone; fetch more history to check it")
        else:
            report("FAIL", "stamp commit", f"{sha} is not a single commit in this repository (missing or ambiguous); refresh the map")
        return
    report("PASS", "stamp commit", sha)
    paths = component_paths(notes)
    # Root-relative paths that are not under --repo are passed as :(top) pathspecs, so a per-system map still works.
    specs = [p if (repo / p).exists() else f":(top){p}" for p in paths]
    changed = git(repo, "log", "--oneline", f"{sha}..HEAD", "--", *specs) if specs else ""
    if changed is None:  # git failed or timed out: drift is unknown, not zero
        report("WARN", "drift", f"could not read the history since {sha}; drift was not checked")
        return
    n = len(changed.splitlines()) if changed else 0
    if n:
        report("WARN", "drift", f"{n} commit(s) since {sha} touched component paths; refresh the notes they cover")
    else:
        report("PASS", "drift", f"no commits since {sha} touched component paths")


def check_names(notes, repo, folder):
    names = set()
    for n in notes.values():
        props = n["props"] or {}
        names.update(x for x in as_list(props.get("key_names")) + as_list(props.get("seen_as")) if x.strip())
        if props.get("type") == "flow":  # flow steps name the symbols they pass through: check each part of A.b
            for line in n["body"].splitlines():
                if re.match(r"^\s*\d+\. ", line):
                    for token in backticked(line):
                        if IDENT.match(token):
                            names.update(part for part in re.split(r"\.|::", token.rstrip("()")) if part)
    if not names:
        report("FAIL", "names occur in code", "no key_names or seen_as properties to check")
        return
    pending = set(names)
    patterns = {x: re.compile(r"(?<![\w$])" + re.escape(x) + r"(?![\w$])") for x in names}
    try:
        for text in source_texts(repo, folder.resolve()):
            for x in list(pending):
                if patterns[x].search(text):
                    pending.discard(x)
            if not pending:
                break
    except OverflowError as e:
        if pending:
            global INCOMPLETE
            INCOMPLETE = True
            report("NOT RUN", "names occur in code", f"{e}; check {len(pending)} name(s) by hand or point --repo at one system")
            return
    if pending:
        report("FAIL", "names occur in code", "not found: " + ", ".join(sorted(pending)))
    else:
        report("PASS", "names occur in code", f"{len(names)} checked")


def diagram_nodes(block):
    nodes = set()
    for line in block.splitlines()[1:]:
        line = re.sub(r"%%.*", "", line).strip()
        if not line or re.match(r"(subgraph|end|classDef|class|style|linkStyle|click|direction)\b", line):
            continue
        line = re.sub(r"\|[^|]*\|", " ", line)
        line = re.sub(r"[\[\(\{>][^\]\)\}]*[\]\)\}]+", " ", line)
        # Edges start with -- , -. or == (a single hyphen inside an id such as entry-router is not an edge).
        for token in re.split(r"\s*(?:--\s[^>]*?-->|-\.[\w ]*\.?-*>|--+[>ox]?|==+>?|~~~|&)\s*", line):
            m = re.match(r"^([A-Za-z_][\w-]*)", token.strip())
            if m:
                nodes.add(m.group(1))
    return nodes


def check_caps(notes):
    long = []
    for rel, n in notes.items():
        lines = n["text"].count("\n") + (0 if n["text"].endswith("\n") else 1)
        cap = MAX_HUB_LINES if rel in ("index.md", "architecture.md") else MAX_NOTE_LINES
        if lines > cap:
            long.append(f"{rel} {lines}>{cap}")
    if long:
        report("FAIL", "note length", "; ".join(long[:8]))
    else:
        report("PASS", "note length")
    arch = notes.get("architecture.md")
    if not arch:
        report("FAIL", "diagram", "no architecture.md")
        return
    blocks = re.findall(r"^```mermaid\s*\n(.*?)^```", arch["body"], re.S | re.M)
    if len(blocks) != 1:
        report("FAIL", "diagram", f"architecture.md has {len(blocks)} mermaid blocks, want exactly 1")
        return
    nodes = diagram_nodes(blocks[0])
    components = {n["name"] for n in notes.values() if n["props"] and n["props"].get("type") == "component"}
    orphans = sorted(nodes - components)
    if len(components) > MAX_DIAGRAM_NODES:  # the page and the diagram are designed for one system of at most this many
        report("FAIL", "diagram", f"{len(components)} component notes, cap {MAX_DIAGRAM_NODES}: merge some, or make one map per system")
    elif len(nodes) > MAX_DIAGRAM_NODES:
        report("FAIL", "diagram", f"{len(nodes)} nodes, cap {MAX_DIAGRAM_NODES}")
    elif orphans:
        report("FAIL", "diagram", "nodes with no component note: " + ", ".join(orphans))
    else:
        report("PASS", "diagram", f"{len(nodes)} nodes, each a component note")


def check_no_line_refs(notes):
    hits = []
    for rel, n in notes.items():
        # Backticks, properties and plain prose alike: `file.ext:N` anywhere outside code fences.
        for m in LINE_REF.finditer(strip_fences(n["text"])):
            start = strip_fences(n["text"]).rfind(" ", 0, m.start()) + 1
            hits.append(f"{rel}: {strip_fences(n['text'])[start:m.end()].strip('`')}")
        hits += [f"{rel}: {m}" for m in re.findall(r"\]\([^)]*#L\d+[^)]*\)", n["text"])]
    if hits:
        report("FAIL", "no path:line references", "; ".join(hits[:5]))
    else:
        report("PASS", "no path:line references")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("folder", type=pathlib.Path)
    ap.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    args = ap.parse_args(argv)
    folder, repo = args.folder, args.repo
    if not repo.is_dir() or not folder.is_dir():
        print(f"FAIL folders: need an existing map folder and repository (got {folder}, {repo})")
        return 1
    notes = load_notes(folder)
    check_structure(notes)
    check_index(notes)
    check_links(notes)
    check_paths(notes, repo)
    check_sources(notes, repo)
    check_stamp(notes, repo)
    check_names(notes, repo, folder)
    check_caps(notes)
    check_no_line_refs(notes)
    failed = results.count("FAIL")
    verdict, code = ("FAIL", 1) if failed else ("INCOMPLETE", 2) if INCOMPLETE else ("PASS", 0)
    print(f"SUMMARY {verdict}: {failed} failed, {results.count('WARN')} warnings, {results.count('NOT RUN')} not run"
          + ("; names were not checked, so point --repo at one system and run again" if INCOMPLETE and not failed else ""))
    return code


if __name__ == "__main__":
    sys.exit(main())
