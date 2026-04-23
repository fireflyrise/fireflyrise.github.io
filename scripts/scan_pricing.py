import re
import pathlib

root = pathlib.Path(".")
html_files = [f for f in sorted(root.rglob("*.html")) if ".claude" not in f.as_posix()]

patterns = [
    (re.compile(r"\$\d"), "$ followed by digit"),
    (re.compile(r"\bprice[sd]?\b", re.I), "price/priced/prices"),
    (re.compile(r"\bpricing\b", re.I), "pricing"),
    (re.compile(r"\bcost per\b", re.I), "cost per"),
    (re.compile(r"\bad spend\b", re.I), "ad spend"),
    (re.compile(r"\bad budget\b", re.I), "ad budget"),
    (re.compile(r"\bbudget(s|ing)?\b", re.I), "budget"),
    (re.compile(r"\bdollar(s)?\b", re.I), "dollar/dollars"),
    (re.compile(r"precio(s)?", re.I), "precio"),
    (re.compile(r"presupuesto(s)?", re.I), "presupuesto"),
    (re.compile(r"costo(s)?", re.I), "costo"),
    (re.compile(r"\bgasto(s)?\b", re.I), "gasto"),
]

hits = []
for f in html_files:
    txt = f.read_text(encoding="utf-8")
    for pat, label in patterns:
        for m in pat.finditer(txt):
            start = max(0, m.start() - 40)
            end = min(len(txt), m.end() + 60)
            snip = txt[start:end].replace("\n", " ")
            hits.append((str(f), label, snip.strip()))

for page, label, snip in hits[:80]:
    print(f"{page} [{label}]")
    print(f"  ...{snip}...")
print(f"\nTotal flagged: {len(hits)}")
