#!/usr/bin/env python3
"""Build exact package and matrix views of cross-subdomain associations."""
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
MATRIX = ROOT / 'diagrams/subdomain-relationships-matrix.svg'


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


def package_view():
    # The validated matrix builder checks the source model and all pair counts.
    build()
    model = json.loads(MODEL.read_text())
    receipt = json.loads(REPORT.read_text())
    positions = {'D01': (1350, 455), 'D02': (150, 945), 'D03': (950, 210),
                 'D04': (950, 455), 'D05': (150, 700), 'D06': (550, 700),
                 'D07': (950, 945), 'D08': (550, 455), 'D09': (550, 945),
                 'D10': (550, 210), 'D11': (1350, 210)}
    positions = {k: (x, 200 + (y - 210) * 220 / 245) for k, (x, y) in positions.items()}
    pairs = receipt['association_pairs']
    E = html.escape
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="180mm" height="123.6mm" viewBox="0 0 1500 1030" role="img" aria-labelledby="title desc">',
           '<title id="title">Riskium: relationships between its eleven subdomains</title>',
           '<desc id="desc">Package overview of a single ontology domain. All 23 unordered cross-subdomain association pairs are shown, aggregating 55 concept-level associations. Edge labels greater than one count those associations; an unlabelled edge represents one. Lines do not imply process order, causation, import or dependency. Inheritance is excluded and optional boundary bridges are included.</desc>',
           '<rect width="1500" height="1030" fill="white"/>',
           '<rect x="16" y="16" width="1468" height="998" rx="14" fill="#fafcfd" stroke="#c7d4dd" stroke-width="2"/>',
           '<text x="48" y="67" font-family="Arial,Helvetica,sans-serif" font-size="36" font-weight="700" fill="#143b52">Riskium</text>',
           '<text x="215" y="67" font-family="Arial,Helvetica,sans-serif" font-size="30" fill="#34566a">Subdomain relationship map</text>',
           '<text x="48" y="102" font-family="Arial,Helvetica,sans-serif" font-size="21" fill="#506979">One ontology domain · eleven subdomains · model-derived association links</text>',
           '<path d="M48 126H1452" stroke="#d3dfe6" stroke-width="2"/>']
    segments = []
    for pair in pairs:
        a, b, n = pair['source'], pair['target'], pair['relations']
        x1, y1 = positions[a]; x2, y2 = positions[b]
        dx, dy = x2 - x1, y2 - y1
        scale = min(122 / abs(dx) if dx else float('inf'), 57 / abs(dy) if dy else float('inf'))
        s = (x1 + dx * scale, y1 + dy * scale)
        t = (x2 - dx * scale, y2 - dy * scale)
        segments.append((a, b, n, s, t))
    # White under-strokes make unavoidable crossings distinguishable in print.
    for a, b, n, s, t in segments:
        color = '#387e89' if a == 'D01' else '#738797'
        width = 3.4 if n > 1 else 2.5
        path = f'M{s[0]:.2f} {s[1]:.2f}L{t[0]:.2f} {t[1]:.2f}'
        out += [f'<g id="edge-{a}-{b}" data-associations="{n}"><title>{a} and {b}: {n} concept-level association(s)</title>',
                f'<path d="{path}" stroke="white" stroke-width="10" fill="none"/>',
                f'<path d="{path}" stroke="{color}" stroke-width="{width}" fill="none" stroke-linecap="round"/></g>']
    labels = []
    for a, b, n, s, t in segments:
        if n == 1:
            continue
        # Select a legible point clear of cards, edge crossings and other labels.
        choices = []
        for f in (.5, .35, .65, .25, .75):
            x, y = s[0] + (t[0] - s[0]) * f, s[1] + (t[1] - s[1]) * f
            clearance = min(((x - lx)**2 + (y - ly)**2)**.5 for lx, ly in labels) if labels else 1000
            for aa, bb, nn, p, q in segments:
                if (aa, bb) == (a, b):
                    continue
                vx, vy = q[0] - p[0], q[1] - p[1]
                z = max(0, min(1, ((x - p[0]) * vx + (y - p[1]) * vy) / (vx * vx + vy * vy)))
                clearance = min(clearance, ((x - p[0] - z * vx)**2 + (y - p[1] - z * vy)**2)**.5)
            choices.append((clearance, x, y))
        _, x, y = max(choices)
        labels.append((x, y))
        out += [f'<circle cx="{x:.2f}" cy="{y:.2f}" r="17" fill="white" stroke="#b7c9d4" stroke-width="1.5"/>',
                f'<text x="{x:.2f}" y="{y+8:.2f}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="23" font-weight="700" fill="#24576c">{n}</text>']
    for domain in model['domains']:
        ident = domain['id']; x, y = positions[ident]
        left, top = x - 120, y - 53
        title = domain['title'].removeprefix('Risk ')
        out += [f'<g id="subdomain-{ident}"><title>{E(domain["title"])}</title>',
                f'<rect x="{left}" y="{top}" width="240" height="106" rx="9" fill="white" stroke="#52758b" stroke-width="2.2"/>',
                f'<rect x="{left}" y="{top-17}" width="74" height="29" rx="5" fill="#24576c"/>',
                f'<text x="{left+37}" y="{top+4}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="20" font-weight="700" fill="white">{ident}</text>',
                f'<text x="{x}" y="{y-7}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="22" fill="#506979">Risk</text>',
                f'<text x="{x}" y="{y+29}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="28" font-weight="700" fill="#173f55">{E(title)}</text></g>']
    out += ['<path d="M48 946H1452" stroke="#d3dfe6" stroke-width="2"/>',
            '<text x="48" y="977" font-family="Arial,Helvetica,sans-serif" font-size="20" fill="#415f72">Line = association pair · number = association count · unlabelled line = 1 · no implied direction</text>',
            '<text x="48" y="1003" font-family="Arial,Helvetica,sans-serif" font-size="17" fill="#506979">All 23 pairs / 55 associations · optional boundary bridges included · inheritance excluded</text>',
            '<metadata>All 23 pairs / 55 associations; inheritance excluded; optional boundary bridges included; model SHA-256: ' + receipt['model_sha256'] + '</metadata>',
            '</svg>']
    return '\n'.join(out) + '\n'


def main():
    outputs = {TARGET: package_view(), MATRIX: build()}
    for path, content in outputs.items():
        if '--check' in sys.argv:
            if not path.exists() or path.read_text() != content:
                raise SystemExit('Subdomain SVG is stale: ' + str(path))
        else:
            path.write_text(content)
    print('PASS: 11 subdomains, 23 pairs, 55 associations; package and matrix SVGs current')


if __name__ == '__main__':
    main()
