"""Reader 0.4.10 adds current documentary comparisons over preserved 0.4.9."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import curation

ROOT = curation.ROOT
OUT = ROOT / 'documentation/0.4.10/reader'
VERSION = '0.4.10'
OLD_BANNER = 'Selected scientific source **0.3.2** for package **v0.3.9**; publication has not yet occurred.'
BANNER = 'Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published.'


def relative(path):
    return os.path.relpath(ROOT / path, OUT).replace(os.sep, '/')


def source_term(tid, packet):
    term = packet['terms'][tid]
    source = packet['sources'][term['source_id']]
    return ['### ' + term['name'], '', '**Selected source meaning (paraphrase):** ' + term['paraphrase'], '',
            '**Source and locator:** [' + source['title'] + '](' + source['url'] + '), ' + source['version'] +
            '; [' + term['locator'] + '](' + term['url'] + '). Inspected ' + source['accessed'] + '.', '',
            '**Inspected scope:** ' + source['inspection_scope'], '']


def section(row, data):
    packet = data['packets'][row['origin']['packet_id']]
    lines = ['## Current documentary comparisons', '',
             '**Disposition:** `' + row['disposition'] + '` · reviewed ' + row['reviewed_on'] + '.', '',
             row['rationale'], '']
    if row.get('context_interpretation') or row.get('boundary'):
        lines += [row.get('context_interpretation', row.get('boundary')), '']
    for tid in row['comparison_term_ids']:
        lines += source_term(tid, packet)
    if row.get('foundation_term_ids'):
        lines += ['### Modeling foundations, separate from the domain comparison', '',
                  'These terms inform the selected modeling pattern; they do not supply a risk-domain definition or an asserted alignment axiom.', '']
        for tid in row['foundation_term_ids']:
            lines += source_term(tid, packet)
    if row['concept_id'] in curation.DEFERRED:
        source = packet['sources']['iso']
        lines += ['**Normative mapping deferred:** [' + source['title'] + '](' + source['url'] + '), ' + source['version'] +
                  '. Only catalogue identity/abstract were inspected; no exact normative term wording or clause is asserted. '
                  '[#78](https://github.com/ArazSaieArasi3/riskium/issues/78) retains legitimate full-source access, edition-specific interpretation and adoption.', '']
    if row.get('illustrations'):
        illustration = row['illustrations']
        lines += ['**Authored illustration, not an executed test:** ' + illustration['positive'], '',
                  '**Interpretation counterexample:** ' + illustration['counterexample'], '']
    lines += ['**Review role:** ' + row['review_method'], '',
              '[Original decision and evidence route](' + relative(row['origin']['path']) + ') · '
              '[Current review component](' + relative('references/concept-definitions/0.2.0/review.json') + ') · '
              '[All 82 dispositions](External-Definitions.md).', '',
              'Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.', '']
    return '\n'.join(lines)


def report(data, model):
    lines = ['# External definitions and documentary dispositions', '', BANNER, '', data['scope'], '',
             '## Method and boundaries', '',
             'The eight review packets preserve authored definitions, current source identities, edition/date/locator, selected paraphrases, context and explicit deferrals. Packet-specific access evidence is retained; a full-response hash, selected passage fingerprint and metadata-only access are different evidence routes. Modeling foundations remain separate from domain comparisons.', '',
             'All **82** concepts have one disposition: **40 RELATED**, **20 CONTRAST**, **19 ANALOGY** and **three NEEDS_LICENSED_SOURCE**. The last three are explicit deferrals to [#78](https://github.com/ArazSaieArasi3/riskium/issues/78), not completed normative mappings. Independent interpretation remains [#23](https://github.com/ArazSaieArasi3/riskium/issues/23). No exhaustive search, absence of other relevant work, formal equivalence or superiority is asserted.', '',
             '[Machine-readable component](' + relative('references/concept-definitions/0.2.0/review.json') + ') · [Earlier model-0.3.1 review](' + relative('documentation/0.4.8/concepts/External-Definitions.md') + ') · [All concepts](README.md).', '']
    by = {r['concept_id']: r for r in data['concepts']}
    for domain in model['domains']:
        lines += ['## ' + domain['id'] + ' ' + domain['title'], '', '| Concept | Disposition | Comparison boundary |', '|---|---|---|']
        for cid in domain['concept_ids']:
            row = by[cid]
            lines.append('| [' + row['title'] + '](' + cid + '.md) | ' + row['disposition'] + ' | ' + row['rationale'].replace('|', '\\|') + ' |')
        lines += ['']
    lines += ['## Source editions and actual inspected portions', '',
              'The same document can have different access evidence in different packets; the entries are not silently flattened into a single freshly verified source.', '']
    for key, packet in data['packets'].items():
        lines += ['### ' + key, '']
        for sid, source in packet['sources'].items():
            lines += ['- [' + source['title'] + '](' + source['url'] + '), ' + source['version'] + '. Accessed ' + source['accessed'] +
                      '. ' + source['inspection_scope'] + ' Recorded access: `' + source.get('access', 'See original packet') + '`.', '']
    return '\n'.join(lines)


def render(data=None):
    data = curation.validate(data)
    model = curation.load(ROOT / curation.MODEL)
    base_manifest = curation.load(curation.BASE_READER / 'manifest.json')
    for name, expected in base_manifest['files_sha256'].items():
        curation.need(curation.sha((curation.BASE_READER / name).read_bytes()) == expected, 'Historical reader drift: ' + name)
    files = {p.name: p.read_text() for p in curation.BASE_READER.iterdir() if p.is_file() and p.name != 'manifest.json'}
    by = {row['concept_id']: row for row in data['concepts']}
    for name, body in list(files.items()):
        if name.endswith('.md'):
            body = body.replace(OLD_BANNER, BANNER).replace('# Riskium selected concept dictionary', '# Riskium concept dictionary')
            body = body.replace('Neither the source label nor this generated page supplies independent semantic acceptance, a sourced external definition or standards equivalence. Term-level external alignment is not inferred here.',
                                'The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.')
            cid = name[:-3]
            if cid in by:
                marker = '## Evidence and alignment boundary'
                curation.need(body.count(marker) == 1, 'Missing source boundary')
                body = body.replace(marker, section(by[cid], data) + '\n' + marker)
            body += '\n[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)\n'
        if name == 'Subdomain-matrix.svg':
            body = body.replace('selected for v0.3.9; publication pending', 'model 0.3.2; prepared reader 0.4.10')
        files[name] = body
    files['External-Definitions.md'] = report(data, model)
    files['Curation-Status.md'] = '# Curation and version status\n\n' + BANNER + '\n\nScientific model 0.3.2 and its prior scientific receipts are preserved. This reader adds documentary review 0.2.0 over reader 0.4.9. The eighty-concept review 0.1.0 remains tied to model 0.3.1. Article 7.2.21 and historical SQL/corpus evidence retain their own bindings.\n\nAll 82 dispositions are recorded, including three normative deferrals. Prepared output is not deployed output; v0.3.9 remains the published package until the separate v0.3.10 publication/readback gate passes.\n\n[Concept index](README.md) · [Current comparisons](External-Definitions.md) · [Versioned review](' + relative('references/concept-definitions/0.2.0/component.json') + ') · [Release roadmap](' + relative('plans/next-releases.md') + ') · [Publication tracking #85](https://github.com/ArazSaieArasi3/riskium/issues/85)\n'
    files['README.md'] += '\n## Current documentary source review\n\n[All 82 dispositions](External-Definitions.md) are recorded without changing authored meanings. Three criteria/appetite/tolerance mappings remain explicitly deferred. [Version and publication status](Curation-Status.md).\n'
    manifest = {'schema': 'riskium-current-curated-reader/1', 'documentation_version': VERSION, 'review_version': '0.2.0',
                'model_version': '0.3.2', 'model_sha256': data['model_sha256'], 'review_sha256': curation.sha(curation.REVIEW.read_bytes()),
                'base_reader_manifest_sha256': curation.sha((curation.BASE_READER / 'manifest.json').read_bytes()),
                'recipe_sha256': curation.sha(Path(__file__).read_bytes()), 'catalog_concepts': 82, 'external_anchors': 1,
                'lifecycle': 'PREPARED_NOT_PUBLISHED', 'files_sha256': {n: curation.sha(t.encode()) for n, t in sorted(files.items())}}
    files['manifest.json'] = curation.dump(manifest)
    return files


def build(check=False):
    curation.build(check=True)
    files = render()
    if check:
        curation.need(OUT.is_dir() and {p.name for p in OUT.iterdir() if p.is_file()} == set(files), 'Reader inventory')
        for name, body in files.items():
            curation.need((OUT / name).read_text() == body, 'Stale curated reader: ' + name)
    else:
        OUT.mkdir(parents=True, exist_ok=True)
        for name, body in files.items():
            (OUT / name).write_text(body)
    return files


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    result = build(parser.parse_args().check)
    print(curation.dump({'reader': VERSION, 'markdown_pages': sum(n.endswith('.md') for n in result), 'published': False}))
