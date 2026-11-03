#!/usr/bin/env python3
"""Generate source-bound concept dossiers and subdomain navigation from model 0.3.1."""
from collections import Counter, defaultdict
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / 'ontology/riskium-model.json'
REPORT = ROOT / 'evaluation/manuscript-review/v7.1.0/supplement/structural-report.json'
OUT = ROOT / 'documentation/concepts/0.3.1'


def safe(text):
    return str(text).replace('|', '\\|').replace('\n', ' ')


def build():
    raw = MODEL.read_bytes()
    model = json.loads(raw)
    receipt = json.loads(REPORT.read_text())
    digest = hashlib.sha256(raw).hexdigest()
    if model['version'] != '0.3.1' or digest != receipt['model_sha256']:
        raise ValueError('Model/receipt version or digest mismatch')
    concepts = {x['id']: x for x in model['concepts']}
    domains = {x['id']: x for x in model['domains']}
    if len(concepts) != 80 or len(domains) != 11:
        raise ValueError('Catalog count changed')
    if sum(len(d['concept_ids']) for d in domains.values()) != 80:
        raise ValueError('Subdomain allocation is not a partition')
    for d in domains.values():
        if [c['id'] for c in model['concepts'] if c['domain_id'] == d['id']] != d['concept_ids']:
            raise ValueError('Domain membership differs from source: ' + d['id'])
    pair_counts = Counter()
    neighbors = defaultdict(list)
    for a in model['associations']:
        x, y = a['source'], a['target']
        if x in concepts: neighbors[x].append((a, y, 'source'))
        if y in concepts: neighbors[y].append((a, x, 'target'))
        if x in concepts and y in concepts and concepts[x]['domain_id'] != concepts[y]['domain_id']:
            pair_counts[tuple(sorted((concepts[x]['domain_id'], concepts[y]['domain_id'])))] += 1
    expected = {(p['source'], p['target']): p['relations'] for p in receipt['association_pairs']}
    if pair_counts != expected or len(pair_counts) != 23 or sum(pair_counts.values()) != 55:
        raise ValueError('Association pair population changed')
    parents, children = defaultdict(list), defaultdict(list)
    for g in model['generalizations']:
        if g['specific'] in concepts: parents[g['specific']].append(g['general'])
        if g['general'] in concepts: children[g['general']].append(g['specific'])

    files = {}
    def link(ident):
        if ident in concepts:
            return '[' + safe(concepts[ident]['display_title']) + '](' + ident + '.md)'
        return safe(ident) + ' (external anchor; [source catalog](../../../ontology/riskium-model.json))'

    index = ['# Riskium concept dictionary', '',
             'Model **0.3.1** · **80 catalog concepts** in **11 subdomains** of one general organizational risk-knowledge domain. '
             'The imported foundational anchor `EXT-OBJECT` is outside this count. '
             'Each page is generated from the authoritative [model catalog](../../../ontology/riskium-model.json); '
             'the pharmaceutical literature is a development case, not the ontology’s domain.', '',
             '[Subdomain purposes and relationships](Subdomains.md) · [Package relationship map](../../../diagrams/subdomain-relationships.svg) · [Exact matrix](../../../diagrams/subdomain-relationships-matrix.svg) '
             '· [Current reader](https://arazsaiearasi3.github.io/riskium/current/index.html) · [Wiki](https://github.com/ArazSaieArasi3/riskium/wiki)', '',
             'Concept status: the source records an authored definition and bounded verification status. '
             'No term-specific external definition or standards equivalence is inferred merely from a general reference. '
             '[Source register](../../../references/README.md) and [evidence limits](../../../evaluation/quality/README.md) explain the inspected portions and unresolved validation.', '']
    sub = ['# Subdomains and their relationships', '',
           'Riskium has **one general domain** and eleven catalog **subdomains**. The table below is generated from model 0.3.1. '
           'Concept pages retain stable source identifiers and explicit membership.', '',
           '[Package map SVG](../../../diagrams/subdomain-relationships.svg) · [Matrix SVG](../../../diagrams/subdomain-relationships-matrix.svg) · [Concept index](README.md)', '',
           '| ID and subdomain | Purpose | Concepts | Direct neighbor subdomains |',
           '| --- | --- | --- | --- |']
    for d in model['domains']:
        ids = d['concept_ids']
        if d['concept_count'] != len(ids): raise ValueError('Domain count mismatch')
        index += ['## ' + d['id'] + ' · ' + d['title'], '', safe(d['objective']), '',
                  ' · '.join(link(i) for i in ids), '']
        adjacent = sorted((b if a == d['id'] else a, n) for (a,b),n in pair_counts.items() if d['id'] in (a,b))
        sub.append('| ' + d['id'] + ' · ' + safe(d['title']) + ' | ' + safe(d['objective']) +
                   ' | ' + ', '.join(link(i) for i in ids) +
                   ' | ' + ', '.join('[' + q + '](#' + q.lower() + '--' + re.sub('[^a-z0-9-]','',domains[q]['title'].lower().replace(' ','-')) + ') (' + str(n) + ')' for q,n in adjacent) + ' |')
    sub += ['', '## How to read the package map and matrix', '',
            'The package map shows one card per subdomain and a line for every directly associated pair. '
            'An edge label counts concept-level associations; an unlabelled line means one. '
            'Package notation organizes the catalog without claiming a formal module import or dependency.', '',
            'The upper triangle contains **23 unordered subdomain pairs** representing **55 distinct concept-level associations**. '
            'A number in a cell counts direct associations between concepts in that pair; the diagonal marks self-comparison. '
            'It does not count generalizations, rank importance, prescribe process order, or assign navigability. '
            'Optional catalog boundary bridges are included. Blank upper cells have no direct association in this catalog version; '
            'they do not prove that the topics are unrelated. The short reading path in the figure is explanatory, not a formal edge direction.', '',
            '## Relationship evidence', '',
            '| Pair | Distinct associations |', '| --- | ---: |']
    sub += ['| ' + a + ' · ' + safe(domains[a]['title']) + ' ↔ ' + b + ' · ' + safe(domains[b]['title']) + ' | ' + str(n) + ' |'
            for (a,b),n in sorted(pair_counts.items())]
    sub += ['', '[Structural receipt](../../../evaluation/manuscript-review/v7.1.0/supplement/structural-report.json) '
            '· [Model source](../../../ontology/riskium-model.json) · [Diagram generator](../../../tools/build_subdomain_relationships.py).', '']
    files['README.md'] = '\n'.join(index) + '\n'
    files['Subdomains.md'] = '\n'.join(sub) + '\n'

    for c in model['concepts']:
        cid = c['id']
        text = ['# ' + safe(c['display_title']), '',
                '**Source ID:** `' + cid + '` · **Subdomain:** [' + c['domain_id'] + ' · ' +
                safe(domains[c['domain_id']]['title']) + '](Subdomains.md) · **Layer:** `' + safe(c['scope_layer']) + '`', '',
                '## Current authored definition', '', c['definition'], '',
                '## Identity and modeling', '',
                '- OntoUML stereotype: `' + safe(c['ontouml_stereotype']) + '`; abstract: `' + str(c['is_abstract']).lower() + '`.',
                '- Identity supplier: ' + (link(c['identity_supplier']) if c['identity_supplier'] in concepts else '`' + safe(c['identity_supplier']) + '`') + '.',
                '- Identity basis: ' + safe(c['identity_basis']),
                '- Typing rationale: ' + safe(c['typing_rationale']), '',
                '## Direct source relations', '',
                '| ID | Source reading | Endpoint | Cardinalities |', '| --- | --- | --- | --- |']
        for a, other, direction in sorted(neighbors[cid], key=lambda z:z[0]['id']):
            text.append('| `' + safe(a['id']) + '` | ' + ('outgoing `' if direction == 'source' else 'incoming `') + safe(a['predicate']) + '` | ' + link(other) + ' | '
                        + safe(a['source_end_cardinality']) + ' → ' + safe(a['target_end_cardinality']) + ' |')
        if not neighbors[cid]: text.append('| — | No direct catalog association | — | — |')
        text += ['', 'Generalizes: ' + (', '.join(link(x) for x in parents[cid]) or 'none recorded') + '.  ',
                'Specialized by: ' + (', '.join(link(x) for x in children[cid]) or 'none recorded') + '.', '',
                '## External definition and alignment status', '',
                'No separately sourced external definition or term-level standards equivalence is recorded for this identifier '
                'in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof '
                'of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, '
                'reviewer and rationale; absent that record, status is **unassessed**.', '',
                '## Evidence and limits', '', safe(c['verification_status']),
                'The authored definition and link inventory are source facts; they do not constitute independent semantic validation. '
                '[Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.', '',
                '[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)', '']
        files[cid + '.md'] = '\n'.join(text)
    manifest = {'schema':'riskium-concept-dictionary-v1','model_version':model['version'],
                'model_sha256':digest,'concept_pages':len(concepts),'subdomains':len(domains),
                'cross_subdomain_pairs':len(pair_counts),'cross_subdomain_associations':sum(pair_counts.values()),
                'pages_sha256':{name:hashlib.sha256(value.encode()).hexdigest() for name,value in sorted(files.items())},
                'external_definition_status':'UNASSESSED_UNLESS_EXPLICITLY_SOURCED'}
    files['manifest.json'] = json.dumps(manifest, indent=2, ensure_ascii=False) + '\n'
    return files


def main():
    files=build()
    if '--check' in sys.argv:
        if {p.name for p in OUT.iterdir() if p.is_file()} != set(files):
            raise SystemExit('Dictionary inventory mismatch')
        for name,value in files.items():
            if (OUT/name).read_text()!=value: raise SystemExit('Stale dictionary page: '+name)
            if name.endswith('.md'):
                for target in re.findall(r'\]\(([^)]+)\)', value):
                    if target.startswith(('https://', 'http://', '#')):
                        continue
                    path = target.split('#', 1)[0]
                    if not (OUT/path).resolve().is_relative_to(ROOT) or not (OUT/path).exists():
                        raise SystemExit('Broken dictionary link: ' + name + ' → ' + target)
        print('PASS: 80 concept dossiers, 11 subdomains, 23 relationship pairs')
    else:
        OUT.mkdir(parents=True, exist_ok=True)
        for name,value in files.items(): (OUT/name).write_text(value)
        print('Wrote',len(files),'dictionary files to',OUT)


if __name__ == '__main__':main()
