"""Check the bounded editorial corpus and render its public source/use register.

This is an offline provenance/integrity check, not a standards conformance test.
External reading is recorded by the reviewer; this command does not re-fetch it.
"""
from pathlib import Path
import argparse
from collections import Counter
import hashlib
import json
import subprocess
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CORPUS = 'references/corpus.json'
MODEL = 'ontology/riskium-model.json'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def render():
    raw = (ROOT / CORPUS).read_bytes()
    data = json.loads(raw)
    model_bytes = (ROOT / MODEL).read_bytes()
    model = json.loads(model_bytes)
    frozen = subprocess.check_output(['git', 'show', data['semantic_source_commit'] + ':' + MODEL], cwd=ROOT)
    if model_bytes != frozen or sha(model_bytes) != data['model_sha256']:
        raise ValueError('Reference review no longer targets the frozen conceptual model')
    ids = {r['id'] for family in ['concepts', 'associations', 'generalizations', 'constraints', 'domains', 'imported_types'] for r in model[family]}
    sources = data['sources']
    source_ids = {s['id'] for s in sources}
    if len(source_ids) != len(sources):
        raise ValueError('Duplicate source identity')
    for s in sources:
        for key in ['id', 'citation', 'version', 'category', 'inspected', 'finding', 'actual_use', 'limits', 'observations']:
            if not s.get(key):
                raise ValueError('Missing source field: ' + key)
        if s['category'] not in {'method', 'standard-framework', 'prior-art'}:
            raise ValueError('Unknown source category')
        if s['full_work_reviewed'] is not False or s['redistribution'] != 'metadata-and-original-paraphrase-only':
            raise ValueError('This batch cannot assert full-work review or distribute third-party text')
        for o in s['observations']:
            if urlsplit(o['url']).scheme != 'https' or not o['locator'] or o['checked_on'] != data['review_date']:
                raise ValueError('Incomplete dated source locator')
    comparisons = data['interpretations']
    if len({r['id'] for r in comparisons}) != len(comparisons):
        raise ValueError('Duplicate interpretation identity')
    for r in comparisons:
        if not r['source_ids'] or not set(r['source_ids']) <= source_ids or not r['targets'] or not set(r['targets']) <= ids:
            raise ValueError('Unresolved source/model identity in ' + r['id'])
        if r['disposition'] not in {'METHOD_USE', 'VOCABULARY_CORRESPONDENCE', 'SEMANTIC_DIVERGENCE', 'SCOPE_BOUNDARY', 'NOT_ASSESSED'}:
            raise ValueError('Unknown interpretation disposition')
        if not r['interpretation'] or not r['restriction'] or r['equivalence_asserted'] is not False or r['compliance_asserted'] is not False:
            raise ValueError('Missing interpretation limit')
    if {s['id'] for s in sources} != {i for r in comparisons for i in r['source_ids']}:
        raise ValueError('Every retained source must have a recorded actual use')
    for gap in data['open_limits']:
        if not gap['owner_issues'] or not gap['limitation']:
            raise ValueError('Unowned limit')
    lines = ['# Sources, standards and prior-art interpretation', '',
             'Post-prerelease editorial review dated **' + data['review_date'] + '**, against conceptual design **0.3.1** at `' + data['semantic_source_commit'] + '`. ' + data['scope'], '',
             'The machine-readable [corpus](corpus.json) owns source identities, reading locators, uses, interpretations and remaining limits. The [integrity receipt](../evaluation/references/report.json) checks this register against the model; it does not assess the truth of the external sources or establish semantic correctness.', '',
             '## Review method and selection', '', data['selection_method'], '', data['historical_boundary'], '',
             '| Search family | Queries / route | Selection |', '| --- | --- | --- |']
    for r in data['search_log']:
        lines.append('| ' + ' | '.join([r['family'], r['query'], r['disposition']]) + ' |')
    lines += ['', '## Verified source identities and inspected portions', '']
    for s in sources:
        lines += ['### ' + s['id'] + ' — ' + s['short_title'], '', s['citation'], '',
                  '**Version:** ' + s['version'], '', '**Inspected:** ' + s['inspected'], '',
                  '**Source finding (paraphrase):** ' + s['finding'], '', '**Actual use in Riskium:** ' + s['actual_use'], '',
                  '**Access and interpretation limits:** ' + s['limits'], '', 'Primary reading locators:', '']
        for o in s['observations']:
            lines.append('- [' + o['locator'] + '](' + o['url'] + '), checked ' + o['checked_on'] + '.')
        lines.append('')
    lines += ['## Retained comparison findings', '',
              'These are author-side interpretations of inspected portions, not independently adjudicated mappings. Correspondence is thematic or representational; divergence preserves distinct meanings. No row asserts OWL equivalence, universal terminology identity or compliance.', '',
              '| ID / source | Disposition / model targets | Interpretation | Restriction |', '| --- | --- | --- | --- |']
    for r in comparisons:
        cells = [r['id'] + ' / ' + ', '.join(r['source_ids']), r['disposition'] + ': ' + ', '.join(r['targets']), r['interpretation'], r['restriction']]
        lines.append('| ' + ' | '.join(c.replace('|', '&#124;').replace('\n', ' ') for c in cells) + ' |')
    lines += ['', '## Open limits and claim ceiling', '']
    for gap in data['open_limits']:
        owners = ', '.join('[#' + str(i) + '](https://github.com/ArazSaieArasi3/riskium/issues/' + str(i) + ')' for i in gap['owner_issues'])
        lines.append('- ' + gap['id'] + ': ' + gap['limitation'] + ' Follow-up: ' + owners + '.')
    lines += ['', data['claim_ceiling'], '', '## Reproduce the register check', '',
              '```sh', 'python3 tools/review_references.py --check', '```', '',
              'Run without `--check` only after deliberately reviewing a corpus change. The command checks source/model identifiers and frozen model bytes, requires dated locators and explicit access/equivalence/compliance limits, then regenerates this page and the integrity receipt. It does not repeat online reading or run HermiT, SHACL or an expert review.', '',
              '## Rights', '',
              'Only bibliographic metadata, source links and original Riskium synthesis are distributed here. Third-party papers, standards, code and diagrams retain their own terms; public access alone grants no relicensing permission. No full third-party work, standard clause set or external ontology implementation is copied into this corpus. Riskium scientific synthesis remains under CC BY 4.0; the checking tool is under MIT.']
    outputs = {'references/README.md': '\n'.join(lines) + '\n'}
    report = {'status': 'PASS', 'scope': 'Offline editorial provenance and register integrity only; not standards compliance, external-source revalidation or independent semantic acceptance.',
              'review_date': data['review_date'], 'semantic_source_commit': data['semantic_source_commit'],
              'inputs_sha256': {CORPUS: sha(raw), MODEL: sha(model_bytes), 'tools/review_references.py': sha(Path(__file__).read_bytes())},
              'counts': {'sources': len(sources), 'source_categories': dict(sorted(Counter(s['category'] for s in sources).items())),
                         'interpretations': len(comparisons), 'dispositions': dict(sorted(Counter(r['disposition'] for r in comparisons).items())),
                         'dated_primary_locators': sum(len(s['observations']) for s in sources), 'open_limits': len(data['open_limits']),
                         'equivalence_assertions': 0, 'compliance_assertions': 0, 'full_work_review_claims': 0},
              'online_reading': 'Recorded editorial observations, not re-executed by this command.',
              'limitations': [x['limitation'] for x in data['open_limits']]}
    outputs['evaluation/references/report.json'] = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + '\n'
    return outputs, report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    outputs, report = render()
    for name, content in outputs.items():
        p = ROOT / name
        if args.check:
            if not p.exists() or p.read_text() != content:
                raise SystemExit('Stale editorial projection: ' + name)
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content)
    print(json.dumps({'status': report['status'], 'counts': report['counts'], 'mode': 'check' if args.check else 'write'}, sort_keys=True))
