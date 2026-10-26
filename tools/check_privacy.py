"""Check that no file in the repository holds private data. The repository is public.

Usage (from the repository root): python3 -I tools/check_privacy.py
Scans every UTF-8 text file that git tracks or would add (git ls-files -co --exclude-standard).
       python3 -I tools/check_privacy.py --files <path> [<path> ...]
Scans only those files, with the same patterns, terms and output. tests/test_harness.py uses this
form to prove the checker still fails on a known-bad file. A named file that does not exist fails.
Flags: absolute home paths, scratch paths, email addresses, and long UUIDs (session ids).
Also reads extra terms, one per line, from the optional git-ignored file .privacy-terms at the
repository root (case-insensitive substring match; blank lines and lines starting with # are skipped).
Keep client names and your own username there, never in a committed file.
The committed file .privacy-public lists the repository's own public addresses (one per line, each
containing "/" or "."), such as owner/repo. A term inside one of those addresses is not flagged; the
same term anywhere else still is.
A line that contains the allow marker is skipped; use it sparingly (the pattern definitions below do).
Exits 1 if anything is flagged.
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TERMS_FILE = ".privacy-terms"
PUBLIC_FILE = ".privacy-public"
ALLOW = "privacy: allow"
SKIP_DIRS = {".git", "build", "node_modules", ".playwright-mcp"}
# Placeholder email addresses that are fine to publish.
OK_EMAIL_DOMAINS = {"example.com", "example.org"}
OK_EMAIL_LOCALS = {"noreply", "no-reply"}
# A path must not continue a longer word or URL (so https://host/home/x/ is not flagged).
NOT_AFTER = r"(?<![\w.~-])"

PATTERNS = [
    ("home path", re.compile(NOT_AFTER + r"/(?:Users|home)/[^/\s\"'`<>]+/")),  # privacy: allow
    ("scratch path", re.compile(r"/private/tmp/|/tmp/claude-")),  # privacy: allow
    ("session id (UUID)", re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b")),
]
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")


def files():
    if explicit is not None:
        return explicit
    try:
        out = subprocess.run(
            ["git", "ls-files", "-co", "--exclude-standard", "-z"],
            cwd=ROOT, capture_output=True, check=True,
        ).stdout.decode("utf-8", "replace")
        names = [n for n in out.split("\0") if n]
    except (OSError, subprocess.CalledProcessError):
        names = []
        for d, dirs, fs in os.walk(ROOT):
            dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
            names += [os.path.relpath(os.path.join(d, f), ROOT) for f in fs]
    return sorted(set(names))


def extra_terms():
    path = os.path.join(ROOT, TERMS_FILE)
    if not os.path.exists(path):
        return []
    terms = []
    for no, line in enumerate(open(path, encoding="utf-8"), 1):
        t = line.strip()
        if t and not t.startswith("#"):
            terms.append((no, t.lower()))
    return terms


def public_addresses():
    """Exact public addresses of this repository; a bare word would hide the term everywhere, so it is refused."""
    path = os.path.join(ROOT, PUBLIC_FILE)
    if not os.path.exists(path):
        return []
    out = []
    for no, line in enumerate(open(path, encoding="utf-8"), 1):
        t = line.strip()
        if not t or t.startswith("#"):
            continue
        if "/" not in t and "." not in t:
            sys.exit(f"FAIL {PUBLIC_FILE}:{no}: '{t}' is not an address (needs '/' or '.'); it would hide a private term everywhere")
        out.append(t.lower())
    return sorted(out, key=len, reverse=True)


def email_ok(addr):
    local, _, domain = addr.rpartition("@")
    return domain.lower() in OK_EMAIL_DOMAINS or local.lower() in OK_EMAIL_LOCALS


def explicit_paths(args):
    """Paths named on the command line, as repo-relative names where possible."""
    names = []
    for a in args:
        full = os.path.abspath(a)
        inside = full == ROOT or full.startswith(ROOT + os.sep)
        names.append(os.path.relpath(full, ROOT) if inside else full)
    return sorted(set(names))


args = sys.argv[1:]
if args and (args[0] != "--files" or len(args) < 2):
    sys.exit("usage: check_privacy.py [--files <path> [<path> ...]]")
explicit = explicit_paths(args[1:]) if args else None

terms = extra_terms()
public = public_addresses()
found, scanned = [], 0
for rel in files():
    path = os.path.join(ROOT, rel)
    if rel in (TERMS_FILE, PUBLIC_FILE):
        continue
    if not os.path.isfile(path):
        if explicit is not None:
            found.append(f"{rel}: not a file")
        continue
    try:
        text = open(path, "rb").read().decode("utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    scanned += 1
    for no, line in enumerate(text.splitlines(), 1):
        if ALLOW in line:
            continue
        for name, rx in PATTERNS:
            if rx.search(line):
                found.append(f"{rel}:{no}: {name}")
        if any(not email_ok(m.group(0)) for m in EMAIL.finditer(line)):
            found.append(f"{rel}:{no}: email address")
        low = line.lower()
        for addr in public:
            low = low.replace(addr, " ")
        for term_no, term in terms:
            if term in low:
                found.append(f"{rel}:{no}: extra term (line {term_no} of {TERMS_FILE})")

for f in found:
    print("FAIL", f)
print(f"{'FAIL' if found else 'PASS'} privacy: {scanned} files scanned" + (f", {len(found)} flagged" if found else ""))
sys.exit(1 if found else 0)
