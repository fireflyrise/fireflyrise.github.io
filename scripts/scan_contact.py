"""
Scan every HTML page for plaintext phone/email outside interactive elements,
excluding the legal pages (privacy-policy + terms-and-conditions, both langs)
where plaintext contact is allowed per the SKILL.
"""
import pathlib
import re
from html.parser import HTMLParser

LEGAL_PATHS = {
    "privacy-policy/index.html",
    "terms-and-conditions/index.html",
    "politica-de-privacidad/index.html",
    "terminos-y-condiciones/index.html",
}

PHONE_PAT = re.compile(r"602[-)]?\s*829")
EMAIL_PAT = re.compile(r"mgarcia4@gmail")


class ContactFinder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        # Stack of currently-open tags; plus a flag "in_interactive"
        self.interactive_depth = 0
        self.skip_depth = 0  # head, script, style
        self.hits = []

    def handle_starttag(self, tag, attrs):
        if tag in ("a", "button"):
            self.interactive_depth += 1
        if tag in ("head", "script", "style", "noscript"):
            self.skip_depth += 1

    def handle_endtag(self, tag):
        if tag in ("a", "button") and self.interactive_depth > 0:
            self.interactive_depth -= 1
        if tag in ("head", "script", "style", "noscript") and self.skip_depth > 0:
            self.skip_depth -= 1

    def handle_data(self, data):
        if self.skip_depth > 0:
            return
        if self.interactive_depth > 0:
            return
        if PHONE_PAT.search(data):
            self.hits.append(("PHONE", data.strip()[:80]))
        if EMAIL_PAT.search(data):
            self.hits.append(("EMAIL", data.strip()[:80]))


root = pathlib.Path(".")
html_files = [f for f in sorted(root.rglob("*.html")) if ".claude" not in f.as_posix()]

violators = []
allowed_hits = []

for f in html_files:
    rel = f.as_posix().lstrip("./")
    parser = ContactFinder()
    parser.feed(f.read_text(encoding="utf-8"))
    for kind, snip in parser.hits:
        if rel in LEGAL_PATHS:
            allowed_hits.append((rel, kind, snip))
        else:
            violators.append((rel, kind, snip))

print("Violations (plaintext contact on non-legal pages):")
for v in violators:
    print(f"  {v}")
print(f"  total: {len(violators)}")

print("\nAllowed (legal pages — plaintext contact is OK here):")
for a in allowed_hits[:10]:
    print(f"  {a}")
print(f"  total: {len(allowed_hits)}")
