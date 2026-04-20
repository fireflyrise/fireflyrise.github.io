import re
import os
import pathlib

root = pathlib.Path('.')
html_files = sorted(root.glob('*.html'))
img_refs = set()
pattern = re.compile(r'(?:src|href)=["\']([^"\']+)["\']')
for f in html_files:
    for m in pattern.finditer(f.read_text(encoding='utf-8')):
        img_refs.add(m.group(1))

local_refs = sorted(r for r in img_refs if r.startswith('/images/') or r.startswith('images/'))
missing = []
for r in local_refs:
    p = r.lstrip('/')
    if not os.path.exists(p):
        missing.append(r)
print('Total local image refs:', len(local_refs))
print('Missing files:', missing if missing else 'NONE')

# Also verify internal links resolve
page_refs = set()
for f in html_files:
    for m in pattern.finditer(f.read_text(encoding='utf-8')):
        u = m.group(1)
        if u.endswith('.html') and not u.startswith('http'):
            page_refs.add(u)
missing_pages = []
for r in sorted(page_refs):
    p = r.lstrip('/')
    if not os.path.exists(p):
        missing_pages.append(r)
print('Total page refs:', len(page_refs))
print('Missing pages:', missing_pages if missing_pages else 'NONE')
