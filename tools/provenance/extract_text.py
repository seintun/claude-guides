import html
import re
import sys

src, dst = sys.argv[1], sys.argv[2]
t = open(src, encoding="utf-8").read()
t = re.sub(r"<style.*?</style>", "", t, flags=re.S)
t = re.sub(
    r"<svg.*?</svg>",
    lambda m: " [diagram: " + " / ".join(re.findall(r">([^<>]{2,})</text>", m.group(0))) + "] ",
    t,
    flags=re.S,
)
t = re.sub(r"<(h2|h3|p|li|tr|figcaption|section)[^>]*>", "\n", t)
t = re.sub(r"<[^>]+>", " ", t)
t = html.unescape(t)
t = re.sub(r"[ \t]+", " ", t)
t = re.sub(r"\n\s*\n+", "\n\n", t)
open(dst, "w", encoding="utf-8").write(t.strip() + "\n")
print(len(t.splitlines()), "lines written")
