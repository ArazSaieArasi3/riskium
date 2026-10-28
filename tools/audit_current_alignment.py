"""Bind the current source routes; preserve historical claims and paper identity."""
import argparse
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = 'evaluation/consistency/current-0.3.0'
PROFILES = [('0.4.0', 'source-scenario', 6, 54),
            ('0.5.0', 'source-scenario-lineage', 6, 54),
            ('0.6.0', 'qualified-evidence', 6, 62),
            ('0.7.0', 'evidence-lifecycle', 9, 43)]


def encode(value):
    return json.dumps(value, indent=2, ensure_ascii=False) + '\n'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return digest(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode())


def require(value, message):
    if not value:
        raise ValueError(message)


class Inputs:
    def __init__(self, root, overrides=None):
        self.root = Path(root)
        self.overrides = overrides or {}
        self.bindings = {}

    def data(self, path):
        require(not Path(path).is_absolute() and '..' not in Path(path).parts, 'Unsafe source path')
        data = self.overrides.get(path)
        if data is None:
            data = (self.root / path).read_bytes()
        if isinstance(data, str):
            data = data.encode()
        self.bindings[path] = digest(data)
        return data

    def read(self, path):
        return json.loads(self.data(path))

    def check(self, bindings):
        for path, expected in bindings.items():
            require(digest(self.data(path)) == expected, 'Stale source binding: ' + path)


def validate_report(report, trace, profile, expected_count):
    require(report['profile'] == trace['profile'] == profile, 'Wrong-version report: ' + profile)
    cases = {r['id']: r for r in report['cases']}
    require(len(cases) == len(report['cases']) == expected_count, 'Lost/duplicate actual case: ' + profile)
    require(report['summary']['outcomes'] == {'PASS': expected_count}, 'Promoted/failed case population')
    for case in cases.values():
        require(case['status'] == 'PASS' and case['expected'] == case['observed'], 'Actual oracle mismatch: ' + case['id'])
    linked = set().union(*(set(r['case_ids']) for r in trace['requirements']))
    require(linked == set(cases), 'Orphan or missing executed case: ' + profile)
    require(not report['independent_semantic_validation'], 'Software promoted to independent semantics')
    return cases


def build(root=ROOT, overrides=None):
    src = Inputs(root, overrides)
    policy = src.read(OUT + '/policy.json')
    src.check(policy['preserved_sha256'])
    historical_path = 'evaluation/consistency/traceability.json'
    historical = src.read(historical_path)
    require(len(historical['rows']) == 423, 'Historical denominator changed')
    src.check(historical['input_sha256'])
    model = src.read('ontology/riskium-model.json')
    native = {r['id']: r for key in ('concepts', 'imported_types', 'associations', 'generalizations', 'constraints') for r in model[key]}
    require(model['version'] == '0.3.1' and len(native) == 306, 'Native baseline differs')
    original_ids = {r['id'] for name in ('requirements/requirements.json', 'requirements/scope-requirements.json', 'requirements/competency-questions.json') for r in src.read(name)}
    require(len(original_ids) == 28, 'Original requirement population changed')
    mapping_path = 'evaluation/relational/evidence-lifecycle/mapping-accounting.json'
    mapping = src.read(mapping_path)
    current_native = {r['id']: r for r in mapping['rows']}
    require(len(current_native) == len(mapping['rows']) == 306 and set(current_native) == set(native), 'Lost native disposition')
    for ident, row in current_native.items():
        require(canonical(native[ident]) == row['source_sha256'], 'Native element changed: ' + ident)
    dispositions = dict(Counter(r['disposition'] for r in current_native.values()))
    require(dispositions == mapping['current_dispositions'] and mapping['remaining_deferred'] == 236, 'Native disposition promoted')
    require(dispositions['DEFERRED_NO_COMPLETE_SQL_MAPPING'] == 236 and not mapping['full_mapping_completed'], 'Incomplete mappings hidden')
    responses = src.read('evaluation/independent-review/responses.json')
    require(responses['initial_ratings'] == [], 'Independent review requires separately reviewed ingestion')
    cohort = src.read('evaluation/sources/cq0708/cohort.json')
    admissions = dict(Counter(r['case_admission'] for r in cohort['identity_candidates']))
    require(admissions == {'WITHHELD': 11}, 'Original organizational admission promoted')
    hermit = src.read('evaluation/hermit/report.json')['coverage']['outcomes']
    shacl = src.read('evaluation/shacl/coverage-status.json')['outcomes']
    require(hermit == {'PASS': 281, 'NOT_RUN': 14} and shacl == {'PASS': 341, 'PARTIAL': 1, 'NOT_RUN': 17}, 'Historical scientific denominator changed')
    manuscript = src.read(OUT + '/manuscript-readback.json')
    require(manuscript['status'] == 'ACTUAL_APPROVED_BASELINE_READBACK_PASS', 'Actual paper baseline unverified')
    require(manuscript['manuscript_version'] == '7.0.8' and manuscript['fresh_scientific_engine_runs'] == 0, 'Paper identity promoted')
    require(manuscript['paragraphs_checked'] == 7 and len(manuscript['claim_dispositions']) == 65, 'Paper claim disposition missing')
    require(len(manuscript['tables']) == 5 and len(manuscript['figures']) == 1, 'Paper figure/table accounting missing')
    approved = src.read('evaluation/manuscript-review/v7.0.8/receipt.json')
    require([{k: r[k] for k in ('filename', 'sha256', 'size_bytes')} for r in manuscript['artifacts']] == [{k: r[k] for k in ('filename', 'sha256', 'size_bytes')} for r in approved['artifacts']], 'Actual paper bytes differ from approved delivery')
    amendments = {r['id']: r for r in approved['changes']}
    require(len(manuscript['amendments']) == 7 and {r['id'] for r in manuscript['amendments']} == set(amendments), 'Lost/duplicate approved amendment')
    for row in manuscript['amendments']:
        require(row['text_sha256'] == amendments[row['id']]['new_paragraph_sha256'] and row['matched'] and row['word_location'] == 'P' + str(amendments[row['id']]['paragraph_index']), 'Unmatched approved paragraph')
    paper_claims = {r['id']: r for r in manuscript['claim_dispositions']}
    ledger = src.read('evaluation/manuscript-review/ledger.json')
    require(set(paper_claims) == {r['id'] for r in ledger['rows']}, 'Lost paper claim')
    for row in ledger['rows']:
        current = paper_claims[row['id']]
        require(current['historical_disposition'] == row['disposition'] and current['checked_value'] == row['checked_value'], 'Paper/historical value promoted')
        require(current['word_locations'] and current['pdf_pages'], 'Unlocated paper disposition: ' + row['id'])
    rows = []
    for i, old in enumerate(historical['rows']):
        src.check(old['source_bindings_sha256'])
        for evidence in old['evidence_paths']:
            if isinstance(evidence, str):
                src.data(evidence)
            else:
                require(all(evidence.get(k) for k in ('archive', 'member', 'sha256')), 'Unbound private historical evidence')
        ident = old['source_id']
        paper = {'state': 'NO_ELEMENT_SPECIFIC_PAPER_CLAIM', 'reason': 'General inventories do not establish a paragraph about every term.'}
        if old['family'] == 'MANUSCRIPT':
            paper = paper_claims[ident]
        elif old['family'] == 'AMENDMENT':
            paper = next(r for r in manuscript['amendments'] if r['id'] == ident)
        rows.append(dict(row_id=old['row_id'], family=old['family'], source_id=ident,
                         historical_locator=historical_path + '#/rows/' + str(i), historical_row_sha256=canonical(old),
                         requirements=old['requirements'], native_ids=old['model_elements'], clauses=old['constraint_ids'],
                         representation=current_native[ident]['disposition'] if old['family'] == 'MODEL' else old['implementation'],
                         oracle_ids=old['oracle_ids'], evidence_paths=old['evidence_paths'],
                         retained_claim=old['retained_claim'], limit=old['limit'], manuscript=paper,
                         current_native_locator=mapping_path + '#/rows/' + str(next(j for j, r in enumerate(mapping['rows']) if r['id'] == ident)) if old['family'] == 'MODEL' else None,
                         evidence_status='RETAINED_HISTORICAL_NOT_FRESH_REPLAYED',
                         original_acceptance_unchanged=True))
    claim_rows = {r['id']: r for r in policy['current_claims']}
    require(len(claim_rows) == len(policy['current_claims']) == 12 and set(claim_rows) == {f'FC-{i:02}' for i in range(1, 13)}, 'Lost/duplicate current retained claim')
    paper_groups = {r['id']: r for r in manuscript['current_claim_groups']}
    require(set(paper_groups) == set(claim_rows), 'Missing current claim paper disposition')
    for row in rows:
        if row['family'] == 'RETAINED_CLAIM':
            claim = claim_rows[row['source_id']]
            for path in claim['evidence_paths']:
                src.data(path)
            require(claim['claim'] and claim['limit'] and claim['paper_disposition'], 'Unqualified current claim')
            require([r['location'] for r in paper_groups[row['source_id']]['word_locations']] == ['P' + str(n) for n in claim['paper_disposition']['word_paragraphs']], 'Current claim paper anchors differ')
            row['current_claim'] = claim
            row['manuscript'] = paper_groups[row['source_id']]
            row['retained_claim'] = claim['claim']
            row['limit'] = claim['limit']
    pools = []
    for profile, stem, requirement_count, case_count in PROFILES:
        base = 'implementation/relational/' + profile
        evidence_base = 'evaluation/relational/' + stem
        contract_path, trace_path, report_path = base + '/contract.json', evidence_base + '/traceability.json', evidence_base + '/report.json'
        contract, trace, report = src.read(contract_path), src.read(trace_path), src.read(report_path)
        require(contract['version'] == profile, 'Wrong-version contract')
        src.check(contract['source_sha256'])
        src.check(report['inputs_sha256'])
        src.check(trace.get('inputs_sha256', {}))
        component_path = base + '/component.json'
        component = src.read(component_path)
        require(component['version'] == profile and component['compatible_model'] == '0.3.1', 'Component version mismatch')
        src.check(component.get('files_sha256', {}))
        fixtures = src.read(base + '/fixtures.json')
        declared_cases = set(fixtures['case_ids'] if 'case_ids' in fixtures else (r['id'] for r in fixtures['cases']))
        cases = validate_report(report, trace, profile, case_count)
        require(declared_cases == set(cases), 'Lost fixed control: ' + profile)
        declarations = {r['id']: r for r in contract['requirements']}
        require(len(declarations) == len(trace['requirements']) == requirement_count, 'Lost derived requirement')
        for i, route in enumerate(trace['requirements']):
            req = route['requirement']
            require(req == declarations[req['id']], 'Trace/contract definition mismatch')
            require(set(req['source_requirements'] + route['cqs']) <= original_ids, 'Unknown original requirement/CQ')
            clauses = req.get('constraints', req.get('clauses', []))
            require(set(clauses) <= set(native), 'Unknown native clause')
            implementation = []
            for name in route['implementation']:
                path = name if name.startswith(('tools/', 'implementation/')) else ('tools/' + name if name.endswith('.py') else base + '/' + name)
                require(path in report['inputs_sha256'], 'Code/query absent from actual receipt: ' + path)
                src.data(path)
                implementation.append(path)
            require(route['limit'], 'Unqualified engineering claim')
            rows.append(dict(row_id='DERIVED:' + req['id'], family='DERIVED_REQUIREMENT', source_id=req['id'],
                             source_locator=contract_path + '#/requirements/' + str(i), trace_locator=trace_path + '#/requirements/' + str(i),
                             source_definition_sha256=canonical(req), requirements=req['source_requirements'], cqs=route['cqs'],
                             native_ids=contract.get('native_classes', contract.get('native_scope', {}).get('already_represented_classes', [])), clauses=clauses,
                             native_relations=contract.get('native_relations', contract.get('native_scope', {}).get('already_projected_relations', [])),
                             representation='Supplementary application/SQL behavior; native omissions retained in complete 306-ID accounting.',
                             implementation_paths=implementation, oracle_fixture=base + '/fixtures.json',
                             oracle_ids=route['case_ids'], actual_report=report_path, runtime=report['runtime'],
                             retained_claim=req['accept'], limit=route['limit'],
                             manuscript={'state': 'NOT_CLAIMED_IN_PAPER', 'version': '7.0.8', 'reason': 'Later engineering supplement, outside the evaluated article baseline; conceptual commitments are distinct.'},
                             evidence_status='ACTUAL_SCOPED_ENGINEERING_RECEIPT', original_acceptance_unchanged=True))
        pools.append(dict(profile=profile, report=report_path, runtime=report['runtime'], cases=case_count,
                          categories=dict(Counter(r.get('kind', r.get('category')) for r in cases.values())),
                          controls=[dict(id=r['id'], status=r['status'], expected_observed_equal=r['expected'] == r['observed']) for r in cases.values()]))
    require(len(rows) == len({r['row_id'] for r in rows}) == 450, 'Lost/duplicate current route')
    require({r['source_id'] for r in rows if r['family'] == 'MODEL'} == set(native), 'Orphan native ID')
    declared_claims = {r['row_id'] for r in rows if r['family'] in ('RETAINED_CLAIM', 'DERIVED_REQUIREMENT')}
    require(declared_claims == set(policy['required_current_claim_routes']) and len(declared_claims) == 39, 'Orphan/missing current claim')
    for row in rows:
        require(row['retained_claim'] and row['limit'] and row['manuscript'], 'Unqualified or unlocated route')
        require(set(row['requirements']) <= original_ids and set(row['native_ids'] + row['clauses'] + row.get('native_relations', [])) <= set(native), 'Dangling source identity')
    # The published matrix remains a preserved baseline, not the not-yet-selected v0.3.5 matrix.
    selected = src.read('releases/distribution-v0.3.4.json')
    src.check(selected['selected_files_sha256'])
    selected_count = len(selected['selected_files_sha256'])
    require(selected_count == 380, 'Published selection population changed')
    for path in policy['artifact_paths']:
        src.data(path)
    report = dict(schema='riskium-current-alignment-report-v1', version='0.3.0', execution_issue=54,
                  source_baseline=policy['source_baseline'], target_distribution='v0.3.5',
                  status='CURRENT_SOURCE_AND_PAPER_BASELINE_ACCOUNTING_PASS',
                  summary=dict(routes=450, historical_rows=423, derived_requirements=27, declared_current_claim_routes=39,
                               native_ids=306, remaining_deferred=236, historical_hermit=hermit, historical_shacl=shacl,
                               preserved_published_file_bindings=380, independent_ratings=0, organizational_admissions=admissions,
                               orphan_routes=0, orphan_derived_controls=0, unexplained_in_scope_version_mismatches=0),
                  engineering_populations=pools, manuscript_readback=OUT + '/manuscript-readback.json',
                  current_channel_alignment='PENDING_R5_DOCUMENTATION_0.4.0_AND_ACTUAL_CHANNEL_READBACK',
                  final_release_alignment='PENDING_R6_FINAL_SELECTION_FREEZE_AND_INDEPENDENT_ASSET_VERIFICATION',
                  submission_ready=False, fresh_scientific_engine_runs=0,
                  limits=policy['limits'], input_sha256=dict(sorted(src.bindings.items())))
    register = dict(schema='riskium-current-route-overlay-v1', version='0.3.0', historical_trace=historical_path,
                    historical_rows_changed=False, source_baseline=policy['source_baseline'], rows=rows)
    stream = io.StringIO()
    writer = csv.writer(stream, lineterminator='\n')
    columns = ['row_id', 'source_id', 'family', 'requirements', 'native_ids', 'clauses', 'representation', 'oracle_ids', 'retained_claim', 'limit', 'manuscript', 'evidence_status']
    writer.writerow(columns)
    for row in rows:
        writer.writerow([row[k] if isinstance(row[k], str) else json.dumps(row[k], ensure_ascii=False) for k in columns])
    outputs = {OUT + '/traceability.json': encode(register), OUT + '/traceability.csv': stream.getvalue(), OUT + '/report.json': encode(report)}
    component_paths = ['tools/audit_current_alignment.py', 'tools/read_current_manuscript.py', 'tests/test_current_alignment.py',
                       '.github/workflows/current-alignment.yml', OUT + '/README.md']
    component_bindings = {p: digest(src.data(p)) for p in component_paths}
    component_bindings.update({p: digest(value.encode()) for p, value in outputs.items()})
    component_bindings.update({OUT + '/policy.json': src.bindings[OUT + '/policy.json'], OUT + '/manuscript-readback.json': src.bindings[OUT + '/manuscript-readback.json']})
    outputs[OUT + '/component.json'] = encode(dict(schema='riskium-current-consistency-component-v2', id='CONSISTENCY', version='0.3.0',
                    compatible_model='0.3.1', replaces_version='0.2.0', status='SOURCE_AND_PAPER_BASELINE_CHECKED_NOT_FROZEN_OR_PUBLISHED',
                    historical_rows=423, current_routes=450, independent_acceptance=False, files_sha256=dict(sorted(component_bindings.items())),
                    scope='Version-bound accounting and actual approved-paper readback. Live channels and final v0.3.5 selection/freeze remain separate gates.'))
    return outputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for name, value in build().items():
        path = ROOT / name
        if args.check:
            require(path.is_file() and path.read_text() == value, 'Stale current alignment output: ' + name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(value)
    print(json.dumps(dict(status='CURRENT_SOURCE_AND_PAPER_BASELINE_ACCOUNTING_PASS', routes=450, historical_rows=423,
                          derived_requirements=27, declared_current_claim_routes=39, native_ids=306, remaining_deferred=236,
                          live_channels='R5_PENDING', publication_executed=False)))


if __name__ == '__main__':
    main()
