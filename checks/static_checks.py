"""Static checks on the Orchestrating Claude page source.

Usage: python3 -I checks/static_checks.py <page.html> <urls-baseline.txt>
Prints PASS, FAIL or INFO per check and exits 1 if any check fails.
"""
import re
import sys

# Selectors allowed to use the loop-back colour (orange). Anything else is a colour-role clash.
LOOP_ALLOW = {
    ".d-edge.loop", ".d-arrow.loop", ".d-label.loop", ".k-line.loop",
}
# Hosts the artifact runtime allows scripts from.
SCRIPT_HOSTS = ("cdnjs.cloudflare.com", "cdn.jsdelivr.net", "unpkg.com", "cdn.tailwindcss.com", "code.jquery.com")

page_path, baseline_path = sys.argv[1], sys.argv[2]
src = open(page_path, encoding="utf-8").read()
results = []


def report(cid, name, fails, info=""):
    status = "FAIL" if fails else "PASS"
    detail = f"{len(fails)} fail: " + " | ".join(fails[:8]) if fails else info
    results.append(status)
    print(f"{status} {cid} {name}" + (f" — {detail}" if detail else ""))


# static-1: the loop colour appears only on loop-back marks.
styles = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", src, re.S))
fails = []
for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", styles):
    if "var(--loop)" not in body:
        continue
    for s in (x.strip() for x in sel.split(",")):
        if s and s not in LOOP_ALLOW:
            fails.append(s)
outside = len(re.findall(r"var\(--loop\)", src)) - len(re.findall(r"var\(--loop\)", styles))
if outside:
    fails.append(f"{outside} use(s) outside <style> (inline attributes or script)")
report("static-1", "Loop colour only on loop-back marks", fails)

# static-2: the extra data-series tokens are gone.
n = len(re.findall(r"--series-", src))
report("static-2", "No --series-* tokens", [f"{n} occurrences"] if n else [])

# static-3: artifact page contract.
fails = []
for tag in ("<!doctype", "<html", "<body", "<head"):
    if re.search(re.escape(tag) + r"[\s>]", src, re.I):
        fails.append(f"contains {tag}")
if not re.search(r"<title>[^<]+</title>", src):
    fails.append("no <title>")
for url in re.findall(r'<script[^>]+src="([^"]+)"', src):
    if not any(h in url for h in SCRIPT_HOSTS):
        fails.append(f"script host not allowed: {url}")
report("static-3", "Artifact page contract (no doctype/html/body, title, script hosts)", fails)

# static-4: every external link opens in a new tab with noopener.
fails = []
for tag in re.findall(r"<a\s[^>]*href=\"https?://[^\"]+\"[^>]*>", src):
    if 'target="_blank"' not in tag or "noopener" not in tag:
        fails.append(re.search(r'href="([^"]+)"', tag).group(1))
report("static-4", "External links open in a new tab with noopener", fails)

# static-5: no evidence or source URL from the baseline has been dropped.
current = set(u.replace("&amp;", "&") for u in re.findall(r'href="(https?://[^"]+)"', src))
current = {u for u in current if "fonts.g" not in u}
baseline = {l.strip() for l in open(baseline_path, encoding="utf-8") if l.strip()}
missing = sorted(baseline - current)
added = sorted(current - baseline)
report("static-5", "Every baseline source URL is still linked", missing, f"{len(current)} URLs; {len(added)} added")
for u in added:
    print(f"INFO static-5 added {u}")

sys.exit(1 if "FAIL" in results else 0)
