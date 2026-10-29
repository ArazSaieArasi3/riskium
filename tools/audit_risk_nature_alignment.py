"""Reconcile immutable R2 observations with a new bounded integration overlay."""
import argparse
from collections import Counter
import csv
import io
import json
from pathlib import Path

from rdflib import Dataset, URIRef
import audit_assessment_alignment as predecessor
import audit_current_alignment as common

ROOT = Path(__file__).resolve().parents[1]
OUT = 'evaluation/consistency/current-0.5.0'
INTEGRATION = 'evaluation/integration/v0.3.7'
RECEIPT = INTEGRATION + '/inputs/r2-completion.json'
RECEIPT_SHA = 'cb01769bcf4d2e5f9d4bf7baeeb5ad0fe5313ac987c8c215ce086766ea02b268'
SOURCE = '7f3f8440b22690d28cea750bd441dde78b1e0337'
DECLARATION = '805b1edecff254f1e21131aa6fd098344affb398'
BASE = 'implementation/relational/0.9.0'
NATIVE = 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'
TYPE = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'
require = common.require


def triples(graph):
    return sorted([str(s), str(p), str(o)] for s, p, o in graph)


def resolve(value, oracles, graphs):
    """Resolve R1 literal references without importing the implementation/runner."""
    if isinstance(value, str) and value.startswith('query-oracles.json#/'):
        item = oracles
        for part in value.split('#/', 1)[1].split('/'):
            item = item[part]
        return item
    if isinstance(value, str) and value.startswith('native-oracles.trig#'):
        return triples(graphs.graph(URIRef(value.split('#', 1)[1])))
    if isinstance(value, list):
        return [resolve(v, oracles, graphs) for v in value]
    if isinstance(value, dict):
        return {(k[:-4] if k.endswith('_ref') else k): resolve(v, oracles, graphs) for k, v in value.items()}
    return value


def validate_observations(bundle, fixtures, negative, oracles, graphs, inputs):
    """Check complete vectors, not just PASS labels or rounded coverage totals."""
    runtime = bundle['actual_hosted_and_independent_completion']
    full = bundle['actual_local_full_vectors']
    require(bundle['implementation_source'] == runtime['source_commit'] == full['source_commit'] == SOURCE
            and bundle['declaration_source'] == runtime['declaration_commit'] == DECLARATION
            and runtime['working_tree_clean'] and full['clean_source'], 'R2 executed source differs')
    require(runtime['summary'] == dict(PASS=60, FAIL=0, ERROR=0, PENDING_EXTERNAL_READBACK=0)
            and runtime['native_semantic_acceptance'] is False and runtime['independent_ratings'] == 0,
            'R2 outcome or acceptance promoted')
    actual = {r['id']: r for r in runtime['controls']}
    fixed = {r['id']: r for r in fixtures['cases']}
    require(len(actual) == len(runtime['controls']) == len(fixed) == 60 and set(actual) == set(fixed),
            'Missing or duplicate fixed control')
    for ident, case in fixed.items():
        row = actual[ident]
        require(case['status'] == 'NOT_RUN' and case['observed'] is None
                and row['requirements'] == case['requirements'] and row['status'] == 'PASS'
                and row['expected'] == row['observed'] == resolve(case['expected'], oracles, graphs),
                'Fixed observation differs: ' + ident)
    variants = {r['id']: r for r in runtime['negative_variants']}
    require(len(variants) == len(runtime['negative_variants']) == len(negative['variants']) == 51
            and set(variants) == {r['id'] for r in negative['variants']}, 'Lost negative variant')
    for case in negative['variants']:
        row = variants[case['id']]
        require(row['control'] == case['control'] and row['status'] == 'PASS'
                and row['expected'] == row['observed'] == case['expected'], 'Negative answer differs: ' + case['id'])
    download = runtime['independent_readback']
    suite = download['suite']
    require(download['artifact_id'] == 12941506372 and download['run_id'] == 40971993707
            and download['zip_bytes'] == 13243
            and download['zip_sha256'] == '60fb7b592bbfbb6025f24c833e0708e43ffccab65585ed49aa2cabff13236c54'
            and suite['source_commit'] == download['declaration']['source_commit'] == SOURCE
            and suite['status'] == 'VERSIONED_SUITE_PASS' and suite['candidate_tests'] == 550
            and suite['historical_reader_tests'] == 12, 'Independent R2 receipt differs')
    require(full['all_full_vectors_match'] and set(full['exact_queries']) == set(full['native_graphs'])
            == set(oracles['get']) and len(oracles['get']) == 8, 'Full vector population differs')
    records = {r['version_id']: r for key in ('support_versions', 'context_versions', 'assertions', 'recording_revisions')
               for r in inputs[key]}
    later = inputs['later_unlinked_bundle']
    records[later['assertion']['version_id']] = later['assertion']
    records.update({r['version_id']: r for r in later['recording_revisions']})
    originals = {r['record_id']: r for r in inputs['sources']}
    corrections = {r['corrected_version_id']: r for r in inputs['corrections']}
    for version, answer in full['exact_queries'].items():
        require(answer['row'] == oracles['get'][version], 'Full exact row differs: ' + version)
        require({k: answer[k] for k in oracles['envelope']} == oracles['envelope'], 'Envelope promoted')
        row = answer['row']
        roles = dict(assertion=[version], term=[row['term_version_id']], scheme=[row['scheme_version_id']],
                     context=[row['context_version_id']] if row['context_version_id'] else [],
                     objective=row['objective_version_ids'], recording=row['recording_entry_version_ids'])
        expected_sources = {role: [originals[records[v]['source_record_id']] for v in versions]
                            for role, versions in roles.items()}
        expected_sources['correction'] = [originals[corrections[version]['source_record_id']]] if version in corrections else []
        require(answer['sources'] == expected_sources, 'Verbatim source vector differs: ' + version)
        expected_dependencies = {}
        for role, versions in roles.items():
            if role == 'assertion':
                continue
            values = []
            for v in versions:
                original = records[v]
                item = {k: value for k, value in original.items()
                        if k not in ('label', 'nature_version_ids', 'objective_version_ids')}
                if role in ('term', 'scheme', 'objective'):
                    item.setdefault('code', None)
                    item.setdefault('scheme_version_id', None)
                values.append(item)
            expected_dependencies['objectives' if role == 'objective' else role] = values
        require(answer['dependencies'] == expected_dependencies, 'Exact dependency vector differs: ' + version)
        native = full['native_graphs'][version]
        require(len(native) == len({tuple(t) for t in native})
                and sorted(native) == triples(graphs.graph(URIRef(version))), 'Native triple vector differs: ' + version)
        require(native, 'Empty native graph')
    require(sum(len(t) for t in full['native_graphs'].values()) == 306, 'RDF quad population changed')
    return actual


def witnesses(element, full):
    rows = []
    for version, native in full['native_graphs'].items():
        if 'specific' in element:
            specific = {s for s, p, o in native if p == TYPE and o == NATIVE + element['specific']}
            general = {s for s, p, o in native if p == TYPE and o == NATIVE + element['general']}
            hits = sorted(specific & general)
            kind = 'EXPLICIT_PAIRED_TYPES_NOT_GENERALIZATION_VALIDATION'
        else:
            hits = [t for t in native if t[1] == NATIVE + element['id']
                    or (t[1] == TYPE and t[2] == NATIVE + element['id'])]
            kind = 'EXPLICIT_TYPE_OR_ASSOCIATION_TRIPLES'
        if hits:
            rows.append(dict(version_id=version, kind=kind, observed=hits,
                             locator=RECEIPT + '#/actual_local_full_vectors/native_graphs/' + version))
    return rows


def build(root=ROOT, overrides=None):
    src = common.Inputs(root, overrides)
    # Run the predecessor's actual binding checks; preserve every old row byte-for-byte in JSON value terms.
    for name, value in predecessor.build(root, overrides).items():
        require(src.data(name) == value.encode(), 'Changed predecessor alignment: ' + name)
    policy = src.read(OUT + '/policy.json')
    require(policy['version'] == '0.5.0' and policy['predecessor'] == predecessor.OUT
            and policy['published_release'] == 'v0.3.6' and policy['candidate_release'] == 'v0.3.7'
            and policy['manuscript_version'] == '7.0.8' and policy['new_manuscript_disposition'] == 'NOT_CLAIMED_IN_PAPER'
            and policy['reader'] == 'PENDING_R4' and policy['distribution'] == 'PENDING_R5',
            'Policy release, paper or pending gate promoted')
    raw = src.data(RECEIPT)
    require(len(raw) == 317022 and common.digest(raw) == RECEIPT_SHA, 'Published R2 evidence bytes differ')
    bundle = json.loads(raw)
    contract, fixture, inputs, oracle, negative = [src.read(BASE + '/' + p) for p in (
        'contract.json', 'fixtures.json', 'execution-fixture.json', 'query-oracles.json', 'negative-inputs.json')]
    graphs = Dataset()
    graphs.parse(data=src.data(BASE + '/native-oracles.trig').decode(), format='trig')
    controls = validate_observations(bundle, fixture, negative, oracle, graphs, inputs)
    runtime = bundle['actual_hosted_and_independent_completion']
    src.check(contract['source_sha256'])
    src.check(runtime['runtime_source_sha256'])
    src.check({BASE + '/' + p: h for p, h in runtime['input_sha256'].items()})
    src.check(runtime['independent_readback']['declaration']['files_sha256'])
    component = src.read(BASE + '/component.json')
    src.check(component['files_sha256'])
    require(component['version'] == '0.9.0' and component['schema_version'] == 10
            and component['native_changes'] is False and contract['status'] == 'DECLARED_NOT_IMPLEMENTED',
            'Runtime or original declaration boundary changed')
    query = src.data(BASE + '/native-query.rq').decode()
    for version, native in bundle['actual_local_full_vectors']['native_graphs'].items():
        ds = Dataset()
        for s, p, o in native:
            ds.graph(URIRef(version)).add((URIRef(s), URIRef(p), URIRef(o)))
        observed = [[str(v) if v is not None else None for v in row]
                    for row in ds.query(query, initBindings={'graph': URIRef(version)})]
        require(observed == oracle['rdf_rows'][version], 'Exact named-graph query answer differs: ' + version)
    old = src.read(predecessor.OUT + '/traceability.json')
    historical = src.read('evaluation/relational/evidence-lifecycle/mapping-accounting.json')
    model = src.read('ontology/riskium-model.json')
    native = {r['id']: r for key in ('concepts', 'imported_types', 'associations', 'generalizations', 'constraints') for r in model[key]}
    original = {r['id']: r for name in ('requirements/requirements.json', 'requirements/scope-requirements.json',
                                      'requirements/competency-questions.json') for r in src.read(name)}
    drsd = src.read('requirements/relational-requirements.json')
    database = {r['id']: r for r in drsd['requirements']}
    trace = src.read('evaluation/relational/risk-nature/traceability.json')
    routes = {r['requirement']['id']: r for r in trace['requirements']}
    requirements = {r['id']: r for r in contract['requirements']}
    require(len(requirements) == len(routes) == len(policy['derived_routes']) == 10
            and set(requirements) == set(routes) == set(policy['derived_routes']), 'Missing derived requirement route')
    selected = {r['id']: r for r in contract['native_routes']}
    require(len(native) == len(historical['rows']) == 306 and len(selected) == len(contract['native_routes']) == 31
            and set(selected) <= set(native), 'Native population or selected routes differ')
    native_rows = []
    for oldrow in historical['rows']:
        ident = oldrow['id']
        require(common.canonical(native[ident]) == oldrow['source_sha256'], 'Native definition differs: ' + ident)
        hits = witnesses(native[ident], bundle['actual_local_full_vectors']) if ident in selected else []
        if ident in selected:
            require(selected[ident]['source_structure'] == native[ident]
                    and selected[ident]['sha256'] == common.canonical(native[ident]) and hits,
                    'Missing source-bound native witness: ' + ident)
        native_rows.append(dict(id=ident, source_definition_sha256=common.canonical(native[ident]),
            historical=oldrow, current_task='SCOPED_EXECUTED_ROUTE' if hits else 'NO_NEW_NATURE_MAPPING_CLAIM',
            witnesses=hits, native_semantic_acceptance=False, additional_complete_mapping_claim=False,
            limit='Documentary task and finite synthetic projection only. Historical disposition retained; no full native or generalization acceptance.'))
    require(Counter(r['historical']['disposition'] for r in native_rows) == historical['current_dispositions']
            and sum(r['historical']['disposition'] == 'DEFERRED_NO_COMPLETE_SQL_MAPPING' for r in native_rows) == 236,
            'Historical native disposition promoted')
    rows = list(old['rows'])
    for i, req in enumerate(contract['requirements']):
        ident = req['id']
        route = routes[ident]
        require(route['requirement'] == req and set(route['selected_native_routes']) <= set(selected)
                and set(req['source_requirements']) <= set(original) and set(req['database_requirements']) <= set(database)
                and set(req['clauses']) <= set(native), 'Dangling original or native route: ' + ident)
        require(all(ident in controls[c]['requirements'] for c in req['fixed_cases']), 'Control does not witness requirement: ' + ident)
        rows.append(dict(row_id='DERIVED:' + ident, family='DERIVED_REQUIREMENT', source_id=ident,
            source_locator=BASE + '/contract.json#/requirements/' + str(i), source_definition_sha256=common.canonical(req),
            requirements=req['source_requirements'], database_requirements=req['database_requirements'],
            cqs=contract['source_cqs'], cq_limits=contract['source_cq_limits'],
            task_questions=contract['derived_task_questions'],
            native_ids=route['selected_native_routes'], clauses=req['clauses'],
            original_requirement_acceptance_changed=False,
            representation='Supplementary SQLite 0.9.0/schema 10 documentary retrieval and pinned native projection.',
            implementation_paths=[route['migration'], route['runtime']] + route['queries'],
            oracle_fixture=BASE + '/fixtures.json', oracle_ids=req['fixed_cases'],
            actual_report=RECEIPT, executed_source=SOURCE, runtime=runtime['runtime'],
            observed_control_locators=[RECEIPT + '#/actual_hosted_and_independent_completion/controls/' + str(int(c[-2:]) - 1) for c in req['fixed_cases']],
            retained_claim=req['accept'], software_evidence='ACTUAL_SCOPED_ENGINEERING_RECEIPT',
            completion='PARTIAL_PENDING_R4_R5' if ident == 'NRA-10' else 'BOUNDED_ENGINEERING_RECONCILED',
            reader_status='PENDING_R4', distribution_status='PENDING_R5',
            limit='Synthetic engineering evidence only; no truth selection, independent semantics, production readiness or whole original-requirement acceptance.',
            manuscript=dict(state='NOT_CLAIMED_IN_PAPER', version='7.0.8', edited=False),
            evidence_status='ACTUAL_SCOPED_ENGINEERING_RECEIPT', original_acceptance_unchanged=True))
    require(len(rows) == len({r['row_id'] for r in rows}) == 470 and rows[:460] == old['rows'], 'Lost or rewritten combined route')
    require({c for req in requirements.values() for c in req['fixed_cases']} == set(controls), 'Orphan fixed control')
    assurance = contract['database_assurance']
    require(set(assurance['affected']) | set(assurance['inherited_no_new_claim']) | set(assurance['deferred']) == set(database)
            and len(database) == 28 and drsd['document_version'] == '0.1.0', 'Original DRSD population differs')
    db_rows = []
    for ident, definition in database.items():
        linked = [r for r in requirements.values() if ident in r['database_requirements']]
        require(ident not in assurance['affected'] or linked, 'Unwitnessed affected DBR: ' + ident)
        db_rows.append(dict(id=ident, original_definition=definition, original_definition_sha256=common.canonical(definition),
            disposition='SCOPED_ADDITIONAL_ENGINEERING' if ident in assurance['affected'] else
                        ('INHERITED_NO_NEW_CLAIM' if ident in assurance['inherited_no_new_claim'] else 'DEFERRED'),
            derived_routes=[r['id'] for r in linked],
            fixed_controls=sorted({c for r in linked for c in r['fixed_cases']}),
            reason=assurance['inherited_no_new_claim'].get(ident, assurance['deferred'].get(ident,
                'Only the linked finite nature-task evidence. Original DRSD acceptance is unchanged.')),
            original_acceptance_changed=False))
    paper = src.read(common.OUT + '/manuscript-readback.json')
    require(len(paper['claim_dispositions']) == 65 and paper['manuscript_version'] == '7.0.8', 'Paper population differs')
    groups = {r['id']: r for r in paper['current_claim_groups']}
    require(policy['affected_retained_claim_groups'] == ['FC-05', 'FC-06', 'FC-10', 'FC-12'], 'Affected claim groups differ')
    manuscript = dict(schema='riskium-nature-manuscript-dispositions-v1', manuscript_version='7.0.8', edited=False,
        approved_original_receipt=common.OUT + '/manuscript-readback.json', original_claim_dispositions=paper['claim_dispositions'],
        affected_retained_groups=[dict(original=groups[i], additional_engineering='NOT_CLAIMED_IN_PAPER',
            reason='Nature retrieval is later supplementary engineering; original paragraph and PDF locations retain their approved meaning.')
            for i in policy['affected_retained_claim_groups']],
        derived_dispositions=[dict(id=r['id'], state='NOT_CLAIMED_IN_PAPER',
            supported_engineering_wording=policy['supported_engineering_wording'][r['id']],
            actual_receipt=RECEIPT, fixed_controls=r['fixed_cases'],
            future_manuscript_change='Requires a separately reviewed amendment and exact document readback.') for r in contract['requirements']],
        submission_ready=False, independent_semantic_ratings=0)
    for name in ('releases/selection-v0.3.6.json', 'documentation/0.4.3/policy.json',
                 INTEGRATION + '/README.md', INTEGRATION + '/next-steps.md'):
        src.data(name)
    current03 = src.read(common.OUT + '/report.json')
    require(current03['summary']['organizational_admissions'] == {'WITHHELD': 11}
            and current03['summary']['independent_ratings'] == 0, 'Research disposition promoted')
    report = dict(schema='riskium-nature-current-alignment-report-v1', version='0.5.0', status='R3_ALIGNMENT_PASS',
        published_release='v0.3.6', target_release='v0.3.7', executed_runtime_source=SOURCE,
        evidence_origin=dict(issue=65, receipt=RECEIPT, sha256=RECEIPT_SHA, size_bytes=317022),
        summary=dict(routes=470, previous_routes_unchanged=460, new_derived_requirements=10,
            native_ids=306, bounded_native_routes=31, historical_deferred_unchanged=236,
            selected_routes_previously_deferred=sum(r['id'] in selected and r['disposition'] == 'DEFERRED_NO_COMPLETE_SQL_MAPPING' for r in historical['rows']),
            original_drsd_requirements=28, fixed_controls=60, negative_variants=51,
            full_exact_rows=8, named_graphs=8, rdf_quads=306, rdf_query_rows=9,
            original_paper_claim_dispositions=65, pending_reader_criteria=6,
            orphan_routes=0, orphan_controls=0, independent_semantic_ratings=0, organizational_admissions={'WITHHELD': 11}),
        r2_software_suite=runtime['independent_readback']['suite'],
        source_roles=dict(native_model='0.3.1', owl='0.3.1', orsd='0.4.3', original_drsd='0.1.0',
            manuscript='7.0.8', development_sql='0.9.0/schema 10', maintained_reader='0.4.3/main'),
        gates=dict(R1='COMPLETE_ISSUE_64', R2='COMPLETE_ISSUE_65', R3='ALIGNMENT_PASS', R4='PENDING', R5='PENDING'),
        full_native_mapping_completed=False, source_release_published=False, submission_ready=False,
        fresh_scientific_engine_runs=0, limits=policy['limits'], input_sha256=dict(sorted(src.bindings.items())))
    overlay = dict(schema='riskium-nature-current-route-overlay-v1', version='0.5.0',
                   predecessor=predecessor.OUT + '/traceability.json', previous_rows_changed=False, rows=rows)
    mapping = dict(schema='riskium-nature-bounded-native-accounting-v1', native_model_version='0.3.1',
        historical_source='evaluation/relational/evidence-lifecycle/mapping-accounting.json',
        historical_dispositions=historical['current_dispositions'], historical_deferred_unchanged=236,
        full_mapping_completed=False, bounded_routes=31, rows=native_rows)
    stream = io.StringIO()
    cols = ['row_id', 'source_id', 'family', 'requirements', 'native_ids', 'clauses', 'representation',
            'oracle_ids', 'retained_claim', 'limit', 'manuscript', 'evidence_status']
    writer = csv.writer(stream, lineterminator='\n')
    writer.writerow(cols)
    for row in rows:
        writer.writerow([row[k] if isinstance(row[k], str) else json.dumps(row[k], ensure_ascii=False) for k in cols])
    output = {OUT + '/report.json': common.encode(report), OUT + '/traceability.json': common.encode(overlay),
        OUT + '/traceability.csv': stream.getvalue(), OUT + '/native-accounting.json': common.encode(mapping),
        OUT + '/database-requirements.json': common.encode(dict(original_drsd_version='0.1.0', rows=db_rows)),
        OUT + '/manuscript-dispositions.json': common.encode(manuscript)}
    files = ['tools/audit_risk_nature_alignment.py', 'tests/test_risk_nature_alignment.py',
             OUT + '/README.md', OUT + '/policy.json', INTEGRATION + '/README.md', INTEGRATION + '/next-steps.md']
    bindings = {p: common.digest(src.data(p)) for p in files}
    bindings.update({p: common.digest(v.encode()) for p, v in output.items()})
    output[OUT + '/component.json'] = common.encode(dict(schema='riskium-current-consistency-component-v4',
        id='CONSISTENCY', version='0.5.0', compatible_model='0.3.1', predecessor='0.4.0',
        status='DEVELOPMENT_ALIGNED_NOT_PUBLISHED', routes=470, paper_version='7.0.8',
        independent_acceptance=False, files_sha256=dict(sorted(bindings.items()))))
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    output = build()
    for name, value in output.items():
        path = ROOT / name
        if args.check:
            require(path.is_file() and path.read_text() == value, 'Stale risk-nature alignment: ' + name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(value)
    result = dict(status='R3_ALIGNMENT_PASS', routes=470, native_ids=306, bounded_native_routes=31,
                  fixed_controls=60, negative_variants=51, R4='PENDING', R5='PENDING',
                  output_sha256={p: common.digest(v.encode()) for p, v in output.items()})
    if args.receipt:
        import subprocess
        result['source_commit'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
        result['working_tree_clean'] = not subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT, text=True).strip()
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(common.encode(result))
    print(common.encode(result))


if __name__ == '__main__':
    main()
