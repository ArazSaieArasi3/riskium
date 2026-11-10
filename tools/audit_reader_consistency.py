#!/usr/bin/env python3
"""Bounded source-side check of the proposed repository landing.

Does not claim live Pages/Wiki synchronization, scientific validity, or a
released manuscript. Run again against the exact candidate source.
"""
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit,unquote

ROOT = Path(__file__).resolve().parents[1]
readme = (ROOT / "README.md").read_text(encoding="utf-8")
errors = []

def link_error(target,document):
    parsed=urlsplit(target)
    if not parsed.path:return None
    if parsed.scheme or parsed.netloc:
        prefix='/ArazSaieArasi3/riskium/'
        if parsed.netloc!='github.com' or not parsed.path.startswith(prefix):return None
        rest=parsed.path[len(prefix):]
        if not rest.startswith(('blob/main/','tree/main/')):return None
        local=rest.split('/',2)[2];destination=(ROOT/unquote(local)).resolve()
    else:destination=(ROOT/document.parent/unquote(parsed.path)).resolve()
    if not destination.is_relative_to(ROOT) or not destination.exists():
        return f'broken or escaping link in {document}: {target}'
    return None

for document in (Path('README.md'),Path('.github/README.md')):
    for target in re.findall(r"\]\(([^)]+)\)",(ROOT/document).read_text()):
        problem=link_error(target,document)
        if problem:errors.append(problem)

import json
publication = ROOT / 'evaluation/releases/v0.3.8/publication.json'
promoted = publication.exists()
curated = (ROOT / 'documentation/0.4.8/concepts/manifest.json').exists()
if promoted:
    record=json.loads(publication.read_text())
    if record['status']!='INDEPENDENT_PUBLIC_DOWNLOADS_PASS' or record['tag']!='v0.3.8':errors.append('Invalid source publication record')
    if (ROOT/'.github/README.md').read_text()!=readme:errors.append('Root and GitHub landing differ after promotion')
required = {
    "published source": r"Published source:.*v0\.3\.8" if promoted else r"Published source:.*v0\.3\.7",
    "model version": r"conceptual model and OWL:\*\* 0\.3\.1",
    "reader version": r"published reader:\*\* 0\.4\.8" if curated else r"published reader:\*\* 0\.4\.7" if promoted else r"published reader:\*\* 0\.4\.6",
    "held paper": r"author-held article candidate:.*7\.2\.4" if curated else r"author-held article candidate:.*7\.2\.3",
    "wiki": r"https://github\.com/ArazSaieArasi3/riskium/wiki",
    "pages": r"https://arazsaiearasi3\.github\.io/riskium/current/index\.html",
    "rights": r"\[RIGHTS\.md\]\((?:https://github\.com/ArazSaieArasi3/riskium/blob/main/)?RIGHTS\.md\)",
}
# The successor publication has its own receipt and version roles. Older
# checkouts retain the original branch above and its historical expectations.
publication039 = ROOT / 'evaluation/releases/v0.3.9/publication.json'
if publication039.exists():
    record039=json.loads(publication039.read_text())
    if record039['status']!='INDEPENDENT_PUBLIC_DOWNLOADS_PASS' or record039['source_commit']!='ce0baefa3495d1bc3b42f56ad578154d5bc4f178':
        errors.append('Invalid v0.3.9 publication source binding')
    required.update({
        'published source': r'Published source:.*v0\.3\.9',
        'model version': r'conceptual model and OWL:\*\* 0\.3\.2',
        'reader version': r'published reader:\*\* 0\.4\.9',
        'held paper': r'author-held article candidate:.*7\.2\.21',
    })
for name, pattern in required.items():
    if not re.search(pattern, readme):
        errors.append(f"missing or inconsistent {name}")

import json
receipt = json.loads((ROOT / "evaluation/manuscript-review/v7.2.3/receipt.json").read_text())
if receipt['layout']['pages'] != 10 or not receipt['word_sha256'] or not receipt['pdf_sha256']:
    errors.append("missing current manuscript audit binding")

if errors:
    print("FAIL source landing: " + "; ".join(errors), file=sys.stderr)
    sys.exit(1)
print("PASS source landing links, version roles, rights and author-held receipt (local source only)")
