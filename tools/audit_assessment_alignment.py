"""Check a versioned ASL route overlay against unchanged current and paper baselines."""
import argparse
from collections import Counter
import csv
import io
import json
from pathlib import Path

import audit_current_alignment as prior

ROOT = Path(__file__).resolve().parents[1]
OUT = 'evaluation/consistency/current-0.4.0'
BASE = 'implementation/relational/0.8.0'
EVIDENCE = 'evaluation/relational/assessment-selection'


def build(root=ROOT, overrides=None):
    src = prior.Inputs(root, overrides)
    before = prior.build(root, overrides)
    for path, value in before.items():
        prior.require(src.data(path) == value.encode(), 'Changed predecessor current overlay: ' + path)
    policy = src.read(OUT + '/policy.json')
    old_report = src.read(prior.OUT + '/report.json')
    old_trace = src.read(prior.OUT + '/traceability.json')
    contract = src.read(BASE + '/contract.json')
    fixtures = src.read(BASE + '/fixtures.json')
    component = src.read(BASE + '/component.json')
    evidence = src.read(EVIDENCE + '/report.json')
    trace = src.read(EVIDENCE + '/traceability.json')
    legacy = src.read(EVIDENCE + '/legacy-regressions.json')
    src.check(contract['source_sha256'])
    src.check(component['files_sha256'])
    src.check(evidence['source_sha256'])
    prior.require(contract['version'] == component['version'] == fixtures['version'] == '0.8.0'
                  and component['schema_version'] == 9 and component['native_changes'] is False,
                  'Wrong assessment component version or native change')
    prior.require(component['status'] == 'DEVELOPMENT_EXECUTED_NOT_RELEASED'
                  and contract['status'] == 'DECLARED_NOT_IMPLEMENTED' and fixtures['status'] == 'DECLARED_NOT_RUN',
                  'Declaration/runtime state was rewritten')
    prior.require(prior.digest(src.data(BASE + '/fixtures.json')) == contract['fixtures_sha256'],
                  'Prospective oracle hash changed')
    prior.require(component['declaration_commit'] == evidence['declaration_commit']
                  and component['input_commit'] == evidence['input_commit'], 'Declaration/input provenance differs')
    prior.require(evidence['summary'] == {'PASS': 44, 'FAIL': 0, 'ERROR': 0}
                  and not evidence['independent_semantic_validation']
                  and evidence['reader_criteria'] == 'NOT_REVIEWED_ON_LIVE_CHANNELS',
                  'Actual result or reader status promoted')
    controls = {r['id']: r for r in evidence['controls']}
    declared = {r['id']: r for r in fixtures['cases']}
    prior.require(len(controls) == len(declared) == len(evidence['controls']) == len(fixtures['cases']) == 44
                  and set(controls) == set(declared), 'Missing or duplicate fixed control')
    for ident, row in controls.items():
        expected = declared[ident]
        prior.require(row['expected'] == expected['expected'] == row['observed']
                      and row['status'] == 'PASS' and row['requirements'] == expected['requirements']
                      and expected['observed'] is None and expected['status'] == 'NOT_RUN',
                      'Fixed oracle or actual control differs: ' + ident)
    model = src.read('ontology/riskium-model.json')
    native = {r['id'] for key in ('concepts', 'imported_types', 'associations', 'generalizations', 'constraints')
              for r in model[key]}
    original = {r['id'] for name in ('requirements/requirements.json', 'requirements/scope-requirements.json',
                                   'requirements/competency-questions.json') for r in src.read(name)}
    database = {r['id'] for r in src.read('requirements/relational-requirements.json')['requirements']}
    requirements = {r['id']: r for r in contract['requirements']}
    routes = {r['id']: r for r in trace['rows']}
    wanted = policy['derived_routes']
    prior.require(policy['version'] == '0.4.0' and policy['predecessor'] == prior.OUT
                  and len(wanted) == len(set(wanted)) == len(requirements) == len(routes) == 10
                  and set(wanted) == set(requirements) == set(routes), 'Missing/duplicate ASL route')
    previous_claims = {r['source_id'] for r in old_trace['rows'] if r['family'] == 'RETAINED_CLAIM'}
    prior.require(set(policy['affected_retained_claim_groups']) == {'FC-05', 'FC-06', 'FC-10', 'FC-12'}
                  and set(policy['affected_retained_claim_groups']) <= previous_claims,
                  'Affected claim group changed')
    prior.require(policy['manuscript_version'] == '7.0.8'
                  and policy['new_manuscript_disposition'] == 'NOT_CLAIMED_IN_PAPER'
                  and policy['published_release'] == 'v0.3.5' and policy['candidate_release'] == 'v0.3.6',
                  'Paper or release identity promoted')
    prior.require(old_report['summary']['routes'] == len(old_trace['rows']) == 450
                  and old_report['summary']['native_ids'] == len(native) == 306
                  and old_report['summary']['remaining_deferred'] == 236
                  and old_report['summary']['independent_ratings'] == 0
                  and old_report['summary']['organizational_admissions'] == {'WITHHELD': 11},
                  'Original source, native or research disposition changed')
    rows = list(old_trace['rows'])
    for i, ident in enumerate(wanted):
        req, route = requirements[ident], routes[ident]
        prior.require(route['source_requirements'] == req['source_requirements']
                      and route['database_requirements'] == req['database_requirements']
                      and route['clauses'] == req['clauses']
                      and route['fixed_controls'] == req['fixed_cases']
                      and route['reader_criteria'] == req['reader_criteria']
                      and route['manuscript_disposition'] == policy['new_manuscript_disposition']
                      and route['reader_status'] == 'PENDING_R4', 'Trace and contract differ: ' + ident)
        prior.require(set(req['source_requirements']) <= original
                      and set(req['database_requirements']) <= database and set(req['clauses']) <= native,
                      'Dangling original source/native clause: ' + ident)
        prior.require(all(ident in controls[c]['requirements'] for c in req['fixed_cases'])
                      and (req['fixed_cases'] or req['reader_criteria']) and req['accept'],
                      'Unwitnessed scoped claim: ' + ident)
        rows.append(dict(row_id='DERIVED:' + ident, family='DERIVED_REQUIREMENT', source_id=ident,
                         source_locator=BASE + '/contract.json#/requirements/' + str(i),
                         trace_locator=EVIDENCE + '/traceability.json#/rows/' + str(i),
                         source_definition_sha256=prior.canonical(req), requirements=req['source_requirements'],
                         database_requirements=req['database_requirements'], cqs=contract['source_cqs'],
                         native_ids=['RKM-C032', 'RKM-C034'], clauses=req['clauses'],
                         representation='Supplementary SQL/application selection of an issued assessment bundle; no new native predicate.',
                         implementation_paths=[BASE + '/009_assessment_selection.sql', BASE + '/queries/selection.sql',
                                               'tools/relational_assessment_selection.py'],
                         oracle_fixture=BASE + '/fixtures.json', oracle_ids=req['fixed_cases'],
                         actual_report=EVIDENCE + '/report.json', runtime=evidence['runtime'],
                         retained_claim=req['accept'], limit='Synthetic engineering scope only; no automatic comparability, scientific correctness, or independent assessment.',
                         reader_criteria=req['reader_criteria'], reader_status='PENDING_R4',
                         manuscript={'state': 'NOT_CLAIMED_IN_PAPER', 'version': '7.0.8',
                                     'reason': 'Later SQL/application engineering outside the approved article baseline.'},
                         evidence_status='ACTUAL_SCOPED_ENGINEERING_RECEIPT' if req['fixed_cases'] else 'PENDING_QUALITATIVE_READER_REVIEW',
                         original_acceptance_unchanged=True))
    prior.require(len(rows) == len({r['row_id'] for r in rows}) == 460, 'Lost/duplicate combined route')
    linked = {v for req in requirements.values() for v in req['fixed_cases']}
    prior.require(linked == set(controls), 'Orphan actual ASL control')
    prior.require({v for req in requirements.values() for v in req['reader_criteria']}
                  == {r['id'] for r in contract['reader_acceptance']} and len(contract['reader_acceptance']) == 6,
                  'Orphan reader criterion')
    # Every dependency used above is hash bound, including the unchanged predecessor projections.
    for path in (BASE + '/execution-fixture.json', EVIDENCE + '/README.md', EVIDENCE + '/legacy-regressions.json',
                 'releases/selection-v0.3.5.json', 'documentation/0.4.1/policy.json',
                 'tools/publication/published_documentation.py', '.github/workflows/published-documentation.yml'):
        src.data(path)
    selected = src.read('releases/selection-v0.3.5.json')['selected_files_sha256']
    prior.require(len(selected) == 687, 'Published selected population changed')
    src.check(selected)
    old_paper = src.read(prior.OUT + '/manuscript-readback.json')
    prior.require(old_paper['manuscript_version'] == '7.0.8' and len(old_paper['claim_dispositions']) == 65,
                  'Original paper baseline changed')
    report = dict(schema='riskium-assessment-selection-current-report-v1', version='0.4.0', status='CANDIDATE_CURRENT_ALIGNMENT_PASS',
                  release_issue=61, published_release='v0.3.5', target_release='v0.3.6',
                  summary=dict(routes=460, historical_rows=423, prior_derived=27, new_derived=10,
                               current_claim_routes=49, native_ids=306, deferred=236,
                               previous_engineering_controls=213, new_engineering_controls=44,
                               pending_reader_criteria=6, independent_semantic_ratings=0,
                               organizational_admissions={'WITHHELD': 11}, original_paper_claim_dispositions=65,
                               orphan_routes=0, orphan_controls=0),
                  affected_retained_claim_groups=policy['affected_retained_claim_groups'],
                  manuscript=dict(version='7.0.8', new_routes='NOT_CLAIMED_IN_PAPER',
                                  original_receipt=prior.OUT + '/manuscript-readback.json', edited=False),
                  documentation=dict(published='0.4.1', candidate='PENDING_R4',
                                     boundary=policy['development_reader_boundary']),
                  engineering_runtime=evidence['runtime'], legacy_regressions=legacy,
                  submission_ready=False, limits=policy['limits'], input_sha256=dict(sorted(src.bindings.items())))
    overlay = dict(schema='riskium-current-route-overlay-v2', version='0.4.0',
                   previous_trace=prior.OUT + '/traceability.json', previous_rows_changed=False,
                   published_source=contract['published_source_commit'], rows=rows)
    stream = io.StringIO()
    cols = ['row_id', 'source_id', 'family', 'requirements', 'native_ids', 'clauses', 'representation', 'oracle_ids', 'retained_claim', 'limit', 'manuscript', 'evidence_status']
    writer = csv.writer(stream, lineterminator='\n'); writer.writerow(cols)
    for row in rows:
        writer.writerow([row[k] if isinstance(row[k], str) else json.dumps(row[k], ensure_ascii=False) for k in cols])
    output = {OUT + '/report.json': prior.encode(report), OUT + '/traceability.json': prior.encode(overlay),
              OUT + '/traceability.csv': stream.getvalue()}
    files = ['tools/audit_assessment_alignment.py', 'tools/publication/check_development_boundary.py',
             'tests/test_assessment_alignment.py', '.github/workflows/assessment-alignment.yml',
             OUT + '/README.md', OUT + '/policy.json']
    bindings = {p: prior.digest(src.data(p)) for p in files}
    bindings.update({p: prior.digest(v.encode()) for p, v in output.items()})
    output[OUT + '/component.json'] = prior.encode(dict(schema='riskium-current-consistency-component-v3',
        id='CONSISTENCY', version='0.4.0', compatible_model='0.3.1', predecessor='0.3.0',
        status='DEVELOPMENT_ALIGNED_NOT_PUBLISHED', routes=460, paper_version='7.0.8',
        independent_acceptance=False, files_sha256=dict(sorted(bindings.items()))))
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for name, value in build().items():
        path = ROOT / name
        if args.check:
            prior.require(path.is_file() and path.read_text() == value, 'Stale assessment alignment: ' + name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(value)
    print(json.dumps({'status': 'CANDIDATE_CURRENT_ALIGNMENT_PASS', 'routes': 460,
                      'new_derived': 10, 'paper': '7.0.8', 'reader': 'PENDING_R4'}))


if __name__ == '__main__':
    main()
