"""Assemble current documentary decisions without importing alignment axioms."""
import argparse
import copy
from collections import Counter
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[3]
MODEL = 'ontology/0.3.2/riskium-model.json'
BASE_READER = ROOT / 'documentation/0.4.9/reader'
OUT = ROOT / 'references/concept-definitions/0.2.0'
REVIEW = OUT / 'review.json'
BASELINE = '8e63a88717f3e9efe804004a678adb61e6500510'
PACKET_ROOT = 'evaluation/releases/v0.3.9/followups/'
PACKETS = {'N2': PACKET_ROOT + 'issue85-changed-review/review.json',
           'N3a': PACKET_ROOT + 'issue85-reuse-review/review.json',
           **{f'N3b-{i}': PACKET_ROOT + f'issue85-structural-review/batch-0{i}/review.json' for i in range(1, 7)}}
EXPECTED = {'RELATED': 40, 'CONTRAST': 20, 'ANALOGY': 19, 'NEEDS_LICENSED_SOURCE': 3}
DEFERRED = {'RKM-C072', 'RKM-C073', 'RKM-C074'}
AUTHORITIES = {'www.w3.org', 'nvlpubs.nist.gov', 'ontouml.readthedocs.io', 'www.iso.org'}


def sha(body):
    return hashlib.sha256(body).hexdigest()


def dump(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def digest(value):
    return sha(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode())


def load(path):
    return json.loads(Path(path).read_text())


def need(value, message):
    if not value:
        raise ValueError(message)


def assemble():
    model_raw = (ROOT / MODEL).read_bytes()
    model = json.loads(model_raw)
    concepts = {c['id']: c for c in model['concepts']}
    packets, rows, inputs = {}, [], {MODEL: sha(model_raw)}
    for key, path in PACKETS.items():
        raw = (ROOT / path).read_bytes()
        packet = json.loads(raw)
        need(packet['model_version'] == '0.3.2', 'Packet model version')
        inputs[path] = sha(raw)
        for name, expected in packet['inputs'].items():
            need((ROOT / name).is_file() and sha((ROOT / name).read_bytes()) == expected, 'Packet input drift: ' + name)
            need(name not in inputs or inputs[name] == expected, 'Conflicting source binding')
            inputs[name] = expected
        packets[key] = {'review_path': path, 'review_sha256': sha(raw), 'original_schema': packet['schema'],
                        'date': packet['date'], 'sources': copy.deepcopy(packet['sources']),
                        'terms': copy.deepcopy(packet['terms']), 'boundaries': copy.deepcopy(packet['boundaries'])}
        for original in packet['concepts']:
            row = copy.deepcopy(original)
            cid = row['concept_id']
            need(cid in concepts and row['source_concept_sha256'] == digest(concepts[cid])
                 and row['authored_definition'] == concepts[cid]['definition']
                 and row['authored_definition_sha256'] == sha(concepts[cid]['definition'].encode()), 'Current concept binding')
            need(row['accepted_as_documentary_decision'] is True and row['formal_alignment'] == 'UNASSESSED'
                 and row['independent_validation'] == 'NOT_PERFORMED', 'Unsupported semantic acceptance')
            row['origin'] = {'packet_id': key, 'path': path, 'record_sha256': digest(original)}
            rows.append(row)
    need(len(rows) == 82 and {r['concept_id'] for r in rows} == set(concepts), 'Lost or duplicated concept disposition')
    need(dict(Counter(r['disposition'] for r in rows)) == EXPECTED, 'Disposition denominator')
    need({r['concept_id'] for r in rows if r['disposition'] == 'NEEDS_LICENSED_SOURCE'} == DEFERRED, 'Normative deferral population')
    for row in rows:
        packet = packets[row['origin']['packet_id']]
        for tid in row['comparison_term_ids'] + row.get('foundation_term_ids', []):
            need(tid in packet['terms'], 'Lost term route')
            term = packet['terms'][tid]
            source = packet['sources'][term['source_id']]
            need(term['locator'] and term['paraphrase'] and term['quotation'] is False, 'Source locator/paraphrase')
            need(term['url'].startswith(source['url']) and urlsplit(source['url']).netloc in AUTHORITIES, 'Source authority')
        if row['concept_id'] in DEFERRED:
            need(not row['comparison_term_ids'] and row['followup_issues'] == [78]
                 and row['normative_term_text_inspected'] is False and row['exact_normative_mapping_adopted'] is False
                 and row['normative_term_locator'] is None, 'Metadata promoted to normative term')
    for p in BASE_READER.iterdir():
        if p.is_file():
            inputs[p.relative_to(ROOT).as_posix()] = sha(p.read_bytes())
    return {'schema': 'riskium-current-documentary-curation/2', 'version': '0.2.0', 'model_version': '0.3.2',
            'model_sha256': sha(model_raw), 'date': '2026-11-10', 'intended_package': 'v0.3.10',
            'lifecycle': 'PREPARED_NOT_PUBLISHED', 'scope': 'Assistant-supported current-source documentary dispositions; no exhaustive search, formal alignment or independent semantic rating.',
            'inputs_sha256': dict(sorted(inputs.items())), 'packets': packets,
            'concepts': sorted(rows, key=lambda r: r['concept_id']),
            'summary': {'concepts': 82, 'subdomains': 11, 'dispositions': EXPECTED,
                        'explicit_normative_deferrals': 3, 'formal_equivalences': 0, 'independent_ratings': 0},
            'boundaries': {'scientific_source_modified': False, 'historical_curation_modified': False,
                           'published': False, 'independent_review_issue': 23, 'exact_normative_adoption_issue': 78}}


def validate(data=None):
    data = load(REVIEW) if data is None else data
    expected = assemble()
    need(data == expected, 'Curation differs from qualified packet/source bindings or scope')
    return data


def component(data):
    return {'schema': 'riskium-documentary-component/1', 'artifact': 'Current source-qualified concept comparisons',
            'version': '0.2.0', 'compatible_model': '0.3.2', 'intended_package': 'v0.3.10',
            'lifecycle': 'PREPARED_NOT_PUBLISHED', 'review_sha256': sha(dump(data).encode()),
            'depends_on': [{'artifact': 'Scientific model', 'version': '0.3.2', 'sha256': data['model_sha256']}],
            'historical_component': {'path': 'references/concept-definitions/0.1.0/review.json',
                                     'sha256': data['inputs_sha256']['references/concept-definitions/0.1.0/review.json'],
                                     'model_version': '0.3.1', 'role': 'PRESERVED_HISTORICAL_NOT_RELABELLED'},
            'recipe': 'tools/releases/v0310/curation.py', 'recipe_sha256': sha(Path(__file__).read_bytes()),
            'publication_readback': 'PENDING_N5'}


def build(check=False):
    data = assemble()
    files = {'review.json': dump(data), 'component.json': dump(component(data)),
             'README.md': '# Current documentary curation 0.2.0\n\nPrepared for v0.3.10; not published. All 82 current model-0.3.2 concepts have one source-bound documentary disposition: 40 RELATED, 20 CONTRAST, 19 ANALOGY and three explicit normative deferrals to [#78](https://github.com/ArazSaieArasi3/riskium/issues/78). Independent interpretation remains [#23](https://github.com/ArazSaieArasi3/riskium/issues/23).\n\nThe [review](review.json) preserves each original row and separates packet-specific source/edition/access and modeling foundations from domain comparisons. Historical [review 0.1.0](../0.1.0/review.json) retains its model-0.3.1 population. No source meaning or alignment axiom is changed.\n\n[Reader 0.4.10](../../../documentation/0.4.10/reader/README.md) · [Rebuild and check](../../../tools/releases/v0310/curation.py) · [Release roadmap](../../../plans/next-releases.md)\n'}
    if check:
        need(OUT.is_dir() and {p.name for p in OUT.iterdir() if p.is_file()} == set(files), 'Curation component inventory')
        for name, body in files.items():
            need((OUT / name).read_text() == body, 'Stale curation component: ' + name)
    else:
        OUT.mkdir(parents=True, exist_ok=True)
        for name, body in files.items():
            (OUT / name).write_text(body)
    validate(data)
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    print(dump(build(parser.parse_args().check)['summary']))
