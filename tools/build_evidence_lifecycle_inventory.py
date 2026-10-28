"""Bind actual ELC results to unchanged source identities and the new component."""
import argparse
from collections import Counter
import copy
import hashlib
import json

import relational_evidence_lifecycle as x

ROOT = x.ROOT
OUT = ROOT / 'evaluation/relational/evidence-lifecycle'


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def encode(value):
    return json.dumps(value, indent=2) + '\n'


def build():
    contract = x.contract()
    report = json.loads((OUT / 'report.json').read_text())
    fixture = json.loads((x.OUT / 'fixtures.json').read_text())
    for path, value in report['inputs_sha256'].items():
        if sha(path) != value:
            raise ValueError('Stale lifecycle evidence: ' + path)
    cases = {r['id']: r for r in report['cases']}
    if len(cases) != 43 or report['summary']['outcomes'] != {'PASS': 43}:
        raise ValueError('Incomplete lifecycle execution')
    if {r['id'] for r in fixture['cases']} != set(cases):
        raise ValueError('Lost frozen expectation')
    for row in fixture['cases']:
        if row['observed'] is not None or row['execution_status'] != 'NOT_RUN' or cases[row['id']]['expected'] != row['expected']:
            raise ValueError('Frozen declaration changed: ' + row['id'])
    if len(report['supplementary_controls']) != 1 or any(r['status'] != 'PASS' for r in report['supplementary_controls']):
        raise ValueError('Weakened-rule sensitivity not demonstrated')
    requirement_ids = {r['id'] for r in json.loads((ROOT / 'requirements/requirements.json').read_text())}
    requirements = []
    implementation = ['implementation/relational/0.7.0/008_evidence_lifecycle.sql',
                      'implementation/relational/0.7.0/queries/family.sql',
                      'implementation/relational/0.7.0/queries/selection.sql',
                      'tools/relational_evidence_lifecycle.py']
    for req in contract['requirements']:
        if not set(req['source_requirements']) <= requirement_ids or not req['cases'] or not set(req['cases']) <= set(cases):
            raise ValueError('Broken original requirement/case binding')
        requirements.append(dict(requirement=req, cqs=['RQ-CQ06', 'RQ-CQ07', 'RQ-CQ08'],
                                 case_ids=req['cases'], implementation=implementation,
                                 status='SCOPED_EXECUTED_ENGINEERING',
                                 retained_claim=req['accept'],
                                 limit='C065 documentary/application lifecycle only; no global authority, truth or whole-model/independent acceptance.'))
    if set().union(*(set(r['case_ids']) for r in requirements)) != set(cases):
        raise ValueError('Orphan actual lifecycle case')
    baseline = 'evaluation/relational/qualified-evidence/mapping-accounting.json'
    old = json.loads((ROOT / baseline).read_text())
    rows = copy.deepcopy(old['rows'])
    model = json.loads((ROOT / 'ontology/riskium-model.json').read_text())
    native = {r['id']: r for key in ('concepts', 'imported_types', 'associations', 'generalizations', 'constraints') for r in model[key]}
    if len(native) != 306 or set(native) != {r['id'] for r in rows}:
        raise ValueError('Lost native identities')
    for row in rows:
        source = hashlib.sha256(json.dumps(native[row['id']], sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
        if row['source_sha256'] != source:
            raise ValueError('Native source changed: ' + row['id'])
        row['evidence_lifecycle_overlay'] = ('Scoped supplementary C065 version/decision history; no new complete native mapping'
                                           if row['id'] in ('RKM-C065', 'C-03', 'C-12', 'C-17') else 'NO_ADDITIONAL_MAPPING')
    dispositions = dict(Counter(r['disposition'] for r in rows))
    if dispositions != old['current_dispositions'] or dispositions.get('DEFERRED_NO_COMPLETE_SQL_MAPPING') != 236:
        raise ValueError('Historical native dispositions changed')
    accounting = dict(schema='riskium-evidence-lifecycle-accounting-v1', profile='0.7.0',
                      baseline_path=baseline, baseline_sha256=sha(baseline), source_elements=306,
                      source_sha256=sha('ontology/riskium-model.json'), current_dispositions=dispositions,
                      remaining_deferred=236, new_native_classes=0, new_native_predicates=0,
                      new_complete_mapping_routes=0, full_mapping_completed=False, rows=rows)
    trace = dict(schema='riskium-evidence-lifecycle-trace-v1', execution_issue=53, release_issue=51,
                 profile='0.7.0', original_drsd='0.1.0 unchanged; ELC-01..09 derived supplement',
                 declaration_commit='cb996241553fc8ae858acb38622009ed3a08f450', requirements=requirements,
                 scope='New ELC claims only; release R3/current whole-manuscript reconciliation remains open.',
                 independent_ratings=0, organizational_admissions='All eleven WITHHELD')
    outputs = {'evaluation/relational/evidence-lifecycle/mapping-accounting.json': encode(accounting),
               'evaluation/relational/evidence-lifecycle/traceability.json': encode(trace)}
    paths = set(report['inputs_sha256']) | set(contract['source_sha256']) | {
        'evaluation/relational/evidence-lifecycle/report.json',
        'evaluation/relational/evidence-lifecycle/README.md',
        'evaluation/relational/evidence-lifecycle/software-tests.json',
        'evaluation/relational/evidence-lifecycle/software-tests.log',
        'implementation/relational/0.7.0/README.md',
        'implementation/relational/0.7.0/schema-dictionary.md',
        'tools/build_evidence_lifecycle_inventory.py', 'tests/test_evidence_lifecycle.py',
        '.github/workflows/evidence-lifecycle.yml'}
    inputs = {p: sha(p) for p in sorted(paths)}
    component = dict(schema='riskium-evidence-lifecycle-component-v1', id='EVIDENCE_REFERENCE_LIFECYCLE',
                     version='0.7.0', schema_version=8, compatible_model='0.3.1', baseline_sql_profile='0.6.0',
                     status='DEVELOPMENT_EXECUTED_NOT_FROZEN_OR_PUBLISHED', proposed_source_distribution='v0.3.5',
                     latest_published_distribution='v0.3.4', execution_issue=53, summary=report['summary'],
                     original_requirement_priorities_changed=False, full_mapping_completed=False,
                     independent_semantic_validation=False,
                     files_sha256=dict(inputs, **{p: hashlib.sha256(text.encode()).hexdigest() for p, text in outputs.items()}))
    outputs['implementation/relational/0.7.0/component.json'] = encode(component)
    return outputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for name, text in build().items():
        path = ROOT / name
        if args.check:
            if not path.is_file() or path.read_text() != text:
                raise ValueError('Stale lifecycle accounting: ' + name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
    print(json.dumps(dict(status='EVIDENCE_LIFECYCLE_ACCOUNTING_PASS', requirements=9, cases=43,
                          native_elements=306, remaining_deferred=236, new_complete_native_routes=0)))


if __name__ == '__main__':
    main()
