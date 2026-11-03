#!/usr/bin/env python3
"""Build a print-readable, exact cross-subdomain association matrix."""
from collections import Counter
from pathlib import Path
import hashlib
import html
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / 'ontology/riskium-model.json'
REPORT = ROOT / 'evaluation/manuscript-review/v7.1.0/supplement/structural-report.json'
TARGET = ROOT / 'diagrams/subdomain-relationships.svg'


def build():
    raw = MODEL.read_bytes()
    model = json.loads(raw)
    receipt = json.loads(REPORT.read_text())
    digest = hashlib.sha256(raw).hexdigest()
    if model['version'] != '0.3.1' or digest != receipt['model_sha256']:
        raise ValueError('Source model and structural receipt differ')
    domains = model['domains']
    if len(domains) != 11 or len(model['concepts']) != 80:
        raise ValueError('The declared catalog population changed')
    owners = {row['id']: row['domain_id'] for row in model['concepts']}
    pairs = Counter()
    for relation in model['associations']:
        if relation['source'] not in owners or relation['target'] not in owners:
            continue  # Imported foundational anchor has no catalog subdomain.
        a, b = owners[relation['source']], owners[relation['target']]
        if a != b:
            pairs[tuple(sorted((a, b)))] += 1
    recorded = {(r['source'], r['target']): r['relations'] for r in receipt['association_pairs']}
    if dict(pairs) != recorded or len(pairs) != 23 or sum(pairs.values()) != 55:
        raise ValueError('Aggregated association pairs differ from the source-bound receipt')

    E = html.escape
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="170mm" height="112mm" viewBox="0 0 940 620" role="img" aria-labelledby="title desc">',
           '<title id="title">Riskium subdomain relationships</title>',
           '<desc id="desc">Upper-triangular matrix of eleven catalog subdomains. Twenty-three colored cells enumerate all fifty-five cross-subdomain associations, collapsed by unordered domain pair. Inheritance is excluded; optional boundary bridges are included. The reading path is illustrative and does not assert direction for the associations.</desc>',
           '<rect width="940" height="620" fill="#ffffff"/>',
           '<rect x="24" y="22" width="892" height="576" rx="18" fill="#f7f9fb" stroke="#cfd9e2"/>',
           '<path d="M48 103H892" stroke="#d8e2e8"/>',
           '<text x="48" y="62" fill="#142f43" font-family="Arial,Helvetica,sans-serif" font-size="27" font-weight="700">Riskium · Subdomain relationships</text>',
           '<text x="48" y="88" fill="#456071" font-family="Arial,Helvetica,sans-serif" font-size="15">A single ontology domain organized into eleven catalog subdomains</text>',
           '<text x="48" y="132" fill="#203f55" font-family="Arial,Helvetica,sans-serif" font-size="14" font-weight="700" letter-spacing="1">SUBDOMAIN</text>',
           '<text x="478" y="132" fill="#203f55" font-family="Arial,Helvetica,sans-serif" font-size="14" font-weight="700" letter-spacing="1">ASSOCIATION PAIRS</text>']
    ids = [d['id'] for d in domains]
    x0, y0, cell = 486, 162, 32
    for j, domain in enumerate(domains):
        x = x0 + j * cell + cell / 2
        out.append(f'<text x="{x:g}" y="151" text-anchor="middle" fill="#354e60" font-family="Arial,Helvetica,sans-serif" font-size="12" font-weight="700">{E(domain["id"])}</text>')
    for i, domain in enumerate(domains):
        y = y0 + i * cell
        if i == 0:
            out.append(f'<rect x="42" y="{y+2}" width="419" height="28" rx="7" fill="#dfeff0"/>')
        elif i % 2:
            out.append(f'<rect x="42" y="{y+2}" width="419" height="28" rx="7" fill="#edf2f5"/>')
        out.append(f'<text x="54" y="{y+21}" fill="#17394c" font-family="Arial,Helvetica,sans-serif" font-size="14" font-weight="700">{E(domain["id"])}</text>')
        out.append(f'<text x="108" y="{y+21}" fill="#213d50" font-family="Arial,Helvetica,sans-serif" font-size="15">{E(domain["title"])}</text>')
        for j in range(11):
            x = x0 + j * cell
            if i == j:
                out.append(f'<rect x="{x+1}" y="{y+1}" width="30" height="30" rx="5" fill="#254f63"/>')
                out.append(f'<circle cx="{x+16}" cy="{y+16}" r="3" fill="#ffffff"/>')
            elif i < j:
                n = pairs.get((ids[i], ids[j]), 0)
                fill = '#e9eef1' if not n else '#cbe5e3' if n == 1 else '#91c8c6' if n <= 3 else '#4c969c' if n <= 5 else '#245c72'
                out.append(f'<rect x="{x+1}" y="{y+1}" width="30" height="30" rx="5" fill="{fill}" stroke="#ffffff"/>')
                if n:
                    ink = '#ffffff' if n >= 4 else '#153e4d'
                    out.append(f'<text x="{x+16}" y="{y+21}" text-anchor="middle" fill="{ink}" font-family="Arial,Helvetica,sans-serif" font-size="15" font-weight="700">{n}</text>')
            else:
                out.append(f'<rect x="{x+1}" y="{y+1}" width="30" height="30" rx="5" fill="#f7f9fb"/>')
    out += ['<path d="M48 527H892" stroke="#d8e2e8"/>',
            '<text x="48" y="552" fill="#203f55" font-family="Arial,Helvetica,sans-serif" font-size="13" font-weight="700">READING PATH</text>',
            '<text x="169" y="552" fill="#31566a" font-family="Arial,Helvetica,sans-serif" font-size="14">Phenomena · Registration · Assessment · Treatment</text>',
            '<text x="48" y="578" fill="#456071" font-family="Arial,Helvetica,sans-serif" font-size="12">Cell = number of distinct concept-level associations; 55 relations form 23 unordered pairs.</text>',
            '<text x="48" y="594" fill="#456071" font-family="Arial,Helvetica,sans-serif" font-size="12">Includes optional boundary bridges; excludes inheritance. Blank upper cell = no direct association in this model.</text>',
            '<text x="891" y="578" text-anchor="end" fill="#456071" font-family="Arial,Helvetica,sans-serif" font-size="12">Model 0.3.1</text>',
            '</svg>']
    return '\n'.join(out) + '\n'


def main():
    content = build()
    if '--check' in sys.argv:
        if not TARGET.exists() or TARGET.read_text() != content:
            raise SystemExit('Subdomain SVG is stale')
        print('PASS: 11 subdomains, 23 pairs, 55 associations; SVG current')
    else:
        TARGET.write_text(content)
        print('Wrote', TARGET)


if __name__ == '__main__':
    main()
