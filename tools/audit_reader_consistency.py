#!/usr/bin/env python3
"""Bounded source-side check of the proposed repository landing.

Does not claim live Pages/Wiki synchronization, scientific validity, or a
released manuscript. Run again against the exact candidate source.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
readme = (ROOT / "README.md").read_text(encoding="utf-8")
errors = []

for target in re.findall(r"\]\(([^)]+)\)", readme):
    if target.startswith(("https://", "http://", "mailto:")) or target.startswith("#"):
        continue
    destination = (ROOT / target.split("#", 1)[0]).resolve()
    if not destination.is_relative_to(ROOT) or not destination.exists():
        errors.append(f"broken or escaping relative link: {target}")

required = {
    "published source": r"Published source:.*v0\.3\.7",
    "model version": r"conceptual model and OWL:\*\* 0\.3\.1",
    "reader version": r"published reader:\*\* 0\.4\.5",
    "held paper": r"author-held article candidate:.*7\.2\.1",
    "wiki": r"https://github\.com/ArazSaieArasi3/riskium/wiki",
    "pages": r"https://arazsaiearasi3\.github\.io/riskium/current/index\.html",
    "rights": r"\[RIGHTS\.md\]\(RIGHTS\.md\)",
}
for name, pattern in required.items():
    if not re.search(pattern, readme):
        errors.append(f"missing or inconsistent {name}")

receipt = (ROOT / "evaluation/manuscript-review/v7.2.1/README.md").read_text(encoding="utf-8")
for field in ("ten A4 pages", "Word SHA-256", "PDF SHA-256"):
    if field not in receipt:
        errors.append(f"missing paper receipt field: {field}")

if errors:
    print("FAIL source landing: " + "; ".join(errors), file=sys.stderr)
    sys.exit(1)
print("PASS source landing links, version roles, rights and author-held receipt (local source only)")
