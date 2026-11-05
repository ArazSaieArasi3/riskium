"""Qualify bounded documentary dispositions and generate source-preserving dossiers."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
import build_concept_dictionary as original

ROOT = Path(__file__).resolve().parents[1]
REVIEW = 'references/concept-definitions/0.1.0/review.json'
OUT = ROOT / 'documentation/0.4.8/concepts'
sha = lambda b: hashlib.sha256(b).hexdigest()
encode = lambda v: json.dumps(v, ensure_ascii=False, indent=2) + '\n'
ALLOWED = {'RELATED', 'ANALOGY', 'CONTRAST', 'NO_DIRECT_EQUIVALENT_REVIEWED', 'NEEDS_LICENSED_SOURCE'}


def require(test, message):
    if not test:
        raise ValueError(message)


def validate(data=None, model=None):
    data = json.loads((ROOT / REVIEW).read_text()) if data is None else data
    raw = (ROOT / 'ontology/riskium-model.json').read_bytes()
    model = json.loads(raw) if model is None else model
    require(data['schema'] == 'riskium-external-definition-review-v1' and data['version'] == '0.1.0', 'Review identity differs')
    require(data['model_sha256'] == sha(raw) and data['model_version'] == model['version'] == '0.3.1', 'Model binding differs')
    concepts = {c['id']: c for c in model['concepts']}
    rows = data['concepts']
    require(len(rows) == len(concepts) == 80 and {r['concept_id'] for r in rows} == set(concepts), 'Lost or duplicated concept disposition')
    require(len({r['rationale'] for r in rows}) == 80, 'Repeated generic rationale')
    for sid, source in data['sources'].items():
        url = urlsplit(source['url'])
        require(url.scheme == 'https' and url.netloc in {'www.w3.org', 'nvlpubs.nist.gov', 'ontouml.readthedocs.io', 'www.iso.org'}, 'Unreviewed source authority')
        require(source['version'] and source['inspection_scope'] and source['accessed'] == data['date'], 'Missing source version/scope')
        require(source['document_sha256'] is None or re.fullmatch('[a-f0-9]{64}', source['document_sha256']), 'Invalid response binding')
    for tid, term in data['terms'].items():
        require(term['source_id'] in data['sources'] and term['locator'] and term['paraphrase'], 'Unresolved term source/locator')
        source = data['sources'][term['source_id']]
        require(source['access'] == 'SELECTED_TEXT_INSPECTED', 'Definition claimed from unread source')
        require(term['url'].startswith(source['url'] + '#'), 'Term escaped inspected document')
        require(term['quotation'] is False, 'Unreviewed verbatim quotation')
    for row in rows:
        c = concepts[row['concept_id']]
        require(row['subdomain_id'] == c['domain_id'] and row['authored_definition_sha256'] == sha(c['definition'].encode()), 'Authored meaning or allocation changed')
        require(row['disposition'] in ALLOWED and len(row['rationale'].split()) >= 10, 'Missing explicit comparison decision')
        require(row['review_status'] == 'DOCUMENTARY_DISPOSITION_RECORDED' and row['formal_alignment'] == 'UNASSESSED' and row['independent_validation'] == 'NOT_PERFORMED', 'Documentary curation relabeled semantic acceptance')
        require(row['reviewed_on'] == data['date'] and 'Assistant-supported' in row['review_method'], 'Unattributed documentary review')
        require(set(row['source_ids']) <= set(data['sources']), 'Unknown source')
        if row['disposition'] == 'NEEDS_LICENSED_SOURCE':
            require(not row['term_ids'] and row['source_ids'] == ['iso'] and 78 in row['followup_issues'] and row['source_locator_status'] == 'METADATA_ONLY_NO_NORMATIVE_TERM_LOCATOR', 'Unread normative definition invented')
        else:
            require(row['term_ids'] and set(row['term_ids']) <= set(data['terms']), 'Missing external evidence route')
            require(set(row['source_ids']) == {data['terms'][t]['source_id'] for t in row['term_ids']}, 'Term/source disagreement')
    summary = dict(concepts=80, subdomains=len({r['subdomain_id'] for r in rows}), dispositions=dict(Counter(r['disposition'] for r in rows)), formal_equivalences=0, independent_ratings=0)
    require(summary == data['summary'] and summary['subdomains'] == 11, 'Disposition denominator differs')
    return data, model


def section(row, data):
    lines = ['## External definition and alignment status', '',
             '**Documentary disposition:** `' + row['disposition'] + '` · reviewed ' + row['reviewed_on'] + '.', '',
             '**Authored comparison:** ' + row['rationale'], '']
    for tid in row['term_ids']:
        term = data['terms'][tid]; source = data['sources'][term['source_id']]
        lines += ['### ' + term['name'], '',
                  '**External source definition (paraphrase):** ' + term['paraphrase'], '',
                  '**Source:** ' + source['title'] + '. ' + source['version'] + '. [' + term['locator'] + '](' + term['url'] + '). Accessed ' + source['accessed'] + '.', '',
                  '**Inspected scope:** ' + source['inspection_scope'], '']
    if not row['term_ids']:
        source = data['sources']['iso']
        lines += ['**Source identity only:** [' + source['title'] + '](' + source['url'] + '), ' + source['version'] + '. Accessed ' + source['accessed'] + '.', '',
                  'No normative term definition or clause locator is claimed from catalogue metadata.', '']
    if row['followup_issues']:
        lines += ['**Separate follow-up:** ' + ', '.join('[#' + str(n) + '](https://github.com/ArazSaieArasi3/riskium/issues/' + str(n) + ')' for n in row['followup_issues']) + '.', '']
    lines += ['Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.', '',
              '[Review method, source register and all 80 decisions](External-Definitions.md).', '']
    return '\n'.join(lines)


def build():
    data, model = validate()
    files = original.build()
    files.pop('manifest.json')
    by = {r['concept_id']: r for r in data['concepts']}
    # Only the external-definition section changes. Authored text and relations are reused exactly.
    for cid, row in by.items():
        body = files[cid + '.md']
        start = body.index('## External definition and alignment status')
        end = body.index('## Evidence and limits', start)
        files[cid + '.md'] = body[:start] + section(row, data) + '\n' + body[end:]
    files['README.md'] += '\n## Documentary source review\n\nAll 80 concepts have a bounded source-comparison disposition. [Method, source register and decisions](External-Definitions.md) distinguish relevant definitions, analogies, contrasts, scoped non-equivalence decisions and unread normative terms. No verified equivalence is asserted.\n'
    report = ['# External definitions and documentary dispositions', '',
              'Review **0.1.0** · ' + data['date'] + ' · model **0.3.1** · [Tracking #85](https://github.com/ArazSaieArasi3/riskium/issues/85).', '',
              data['scope'], '',
              '## Review method', '',
              'Each authored definition and modeling identity was read against the named selected primary-source passages. The record retains version/date, exact term or section locator, a short paraphrase, a concept-specific comparison and any follow-up. This is assistant-supported documentary curation, not a human independent rating. No exhaustive search or absence of other relevant ontologies is asserted. Existing COVER/IRISPortal comparisons retain their own inspected scope.', '',
              'No definition in the authoritative model is replaced. No external class is imported; no equivalence, subclass or SKOS match axiom is generated. Normative adoption remains in [#78](https://github.com/ArazSaieArasi3/riskium/issues/78); independent interpretation remains in [#23](https://github.com/ArazSaieArasi3/riskium/issues/23).', '',
              '## Decision vocabulary', '', '| Disposition | Meaning | Count |', '| --- | --- | ---: |']
    for key, meaning in data['relation_vocabulary'].items():
        report.append('| ' + key + ' | ' + meaning + ' | ' + str(data['summary']['dispositions'].get(key, 0)) + ' |')
    report += ['', 'Formal equivalences: **0**. Independent ratings: **0**. All 80 documentary decisions are recorded; the three licensed-source deferrals are not claimed as completed normative mappings.', '', '## Sources and inspected portions', '']
    for sid, source in data['sources'].items():
        report += ['### ' + sid, '', '[' + source['title'] + '](' + source['url'] + '). ' + source['version'] + '. Accessed ' + source['accessed'] + '.', '',
                   source['inspection_scope'], '', 'Response-body SHA-256: `' + source['document_sha256'] + '`.' if source['document_sha256'] else 'No response-body hash claimed; the access route and its limit are documented above.', '']
    for domain in model['domains']:
        report += ['## ' + domain['id'] + ' ' + domain['title'], '', '| Concept | Decision | Source-comparison rationale |', '| --- | --- | --- |']
        for cid in domain['concept_ids']:
            c = next(c for c in model['concepts'] if c['id'] == cid); row = by[cid]
            report.append('| [' + c['display_title'] + '](' + cid + '.md) | ' + row['disposition'] + ' | ' + row['rationale'] + ' |')
        report.append('')
    files['External-Definitions.md'] = '\n'.join(report) + '\n'
    manifest = dict(schema='riskium-reviewed-dictionary-v1', dictionary_version='0.1.0', model_version='0.3.1', model_sha256=data['model_sha256'], review_sha256=sha((ROOT / REVIEW).read_bytes()), source_registry=REVIEW, summary=data['summary'], pages_sha256={n: sha(t.encode()) for n,t in sorted(files.items())})
    files['manifest.json'] = encode(manifest)
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    files = build()
    if args.check:
        require({p.name for p in OUT.iterdir() if p.is_file()} == set(files), 'Reviewed dictionary inventory differs')
        for name, text in files.items():
            require((OUT / name).read_text() == text, 'Stale reviewed dossier: ' + name)
    else:
        OUT.mkdir(parents=True, exist_ok=True)
        for name, text in files.items():
            (OUT / name).write_text(text)
    print(encode(dict(status='EXTERNAL_DEFINITION_DOCUMENTARY_REVIEW_PASS', **validate()[0]['summary'])))


if __name__ == '__main__':
    main()
