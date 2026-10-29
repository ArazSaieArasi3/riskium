"""Check preimplementation risk-nature sources and literal oracles, never its runtime."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

from rdflib import Dataset, RDF, URIRef

ROOT = Path(__file__).resolve().parents[1]
NS = 'implementation/relational/0.9.0'
RISK = 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'
N = 'urn:riskium:nature37:'
RUNTIME_PATHS = (NS + '/010_risk_nature.sql', 'tools/relational_risk_nature.py',
                 'tools/run_relational_risk_nature.py')
DECLARATION_FILES = tuple(NS + '/' + name for name in (
    'README.md', 'contract.json', 'execution-fixture.json', 'fixtures.json', 'negative-inputs.json', 'query-oracles.json',
    'native-oracles.trig', 'native-query.rq', 'prior-population.json', 'proposed-design.md')) + (
    'plans/v0.3.7.md', 'tools/check_risk_nature_declaration.py', 'tests/test_risk_nature_declaration.py')


def require(value, message):
    if not value:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(root, name):
    return json.loads((root / name).read_text())


def check_sources(contract, root=ROOT):
    for name, expected in contract['source_sha256'].items():
        require(not Path(name).is_absolute() and '..' not in Path(name).parts, 'Unsafe source path')
        require(sha((root / name).read_bytes()) == expected, 'Source binding drift: ' + name)


def validate_native_routes(model, contract):
    native = {r['id']: r for family in ('concepts', 'imported_types', 'associations', 'generalizations', 'constraints')
              for r in model[family]}
    require(len(native) == 306 and model['version'] == '0.3.1', 'Wrong native source population')
    routes = contract['native_routes']
    require(len(routes) == len({r['id'] for r in routes}) == 31, 'Native route denominator')
    for row in routes:
        value = native[row['id']]
        require(row['source_structure'] == value, 'Native structure drift: ' + row['id'])
        require(row['sha256'] == sha(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()),
                'Native route hash drift: ' + row['id'])
        require(row['disposition'] == 'PROSPECTIVE_SCOPED_ROUTE_NOT_EXECUTED', 'Promoted native route')
    expected = {'R-41': ('RKM-C005', 'RKM-X01', '0..*', '1'),
                'R-42': ('RKM-C005', 'RKM-C006', '0..*', '1'),
                'R-43': ('RKM-C005', 'RKM-C002', '0..*', '0..1'),
                'R-44': ('RKM-C023', 'RKM-C005', '1..*', '0..*'),
                'R-05': ('RKM-C019', 'RKM-C018', '0..*', '1'),
                'RK2-011': ('RKM-C002', 'RKM-X02', '0..*', '0..*')}
    for ident, shape in expected.items():
        require(tuple(native[ident][key] for key in ('source', 'target', 'source_end_cardinality', 'target_end_cardinality')) == shape,
                'Unsupported finite route: ' + ident)
    require(contract['native_model_revision_required'] is False, 'Scope requires native revision')
    return native


def canonical(value):
    require(isinstance(value, str), 'Nontext time')
    parsed = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
    require(parsed.strftime('%Y-%m-%dT%H:%M:%SZ') == value, 'Noncanonical time')


def validate_semantics(model, contract, fixtures, inputs, oracles, dataset, prior):
    native = validate_native_routes(model, contract)
    require(contract['status'] == 'DECLARED_NOT_IMPLEMENTED' and contract['prospective_distribution'] == 'v0.3.7'
            and contract['proposed_schema_version'] == 10, 'Declaration status drift')
    require(fixtures['declared_before_runtime_implementation'] is True
            and fixtures['status'] == 'DECLARED_NOT_EXECUTED'
            and fixtures['observed_runtime_results'] == 0, 'Promoted runtime results')
    requirements = {r['id']: r for r in contract['requirements']}
    require(set(requirements) == {'NRA-%02d' % n for n in range(1, 11)}, 'Requirement denominator')
    cases = fixtures['cases']
    require(contract['fixed_controls'] == fixtures['controls'] == len(cases) == 60
            and [r['id'] for r in cases] == ['NRA-F%02d' % n for n in range(1, 61)], 'Control denominator')
    for row in cases:
        require(row['observed'] is None and row['status'] == 'NOT_RUN' and row['expected'], 'Promoted/missing fixed outcome')
        require(row['requirements'] and set(row['requirements']) <= set(requirements), 'Unlinked control')
    for ident, requirement in requirements.items():
        require(requirement['fixed_cases'] == [r['id'] for r in cases if ident in r['requirements']], 'Control coverage drift')
        require(requirement['source_requirements'] and requirement['database_requirements'], 'Missing source requirement route')
    assurance = contract['database_assurance']
    groups = [set(assurance[name]) for name in ('affected', 'inherited_no_new_claim', 'deferred')]
    require(set.union(*groups) == {'DBR-%02d' % n for n in range(1, 29)}
            and sum(map(len, groups)) == 28, 'Database assurance loss/overlap')
    require(set(assurance['affected']) == {x for r in requirements.values() for x in r['database_requirements']},
            'Affected assurance coverage drift')
    require(all(r['status'] == 'NOT_REVIEWED' and r['observed'] is None for r in contract['reader_acceptance'])
            and len(contract['reader_acceptance']) == 6, 'Promoted reader review')
    require([r['status'] for r in contract['release_gates']] == ['PENDING_READBACK'] + ['NOT_RUN'] * 4,
            'Promoted release gate')

    sources = {r['record_id']: r['original_json'] for r in inputs['sources']}
    require(len(sources) == len(inputs['sources']) == 10, 'Source fixture denominator')
    for original in sources.values():
        require(json.loads(original)['synthetic'] is True, 'Unqualified source fixture')
    supports = {r['version_id']: r for r in inputs['support_versions']}
    contexts = {r['version_id']: r for r in inputs['context_versions']}
    initial = inputs['assertions']
    assertions = initial + [inputs['later_unlinked_bundle']['assertion']]
    revisions = inputs['recording_revisions'] + inputs['later_unlinked_bundle']['recording_revisions']
    entries = {r['entry_id']: r for r in inputs['entries']}
    cases_by_id = {r['case_id']: r for r in inputs['cases']}
    version_rows = list(supports.values()) + list(contexts.values()) + assertions + revisions
    version_ids = [r['version_id'] for r in version_rows]
    artifact_ids = {r['artifact_id'] for r in list(supports.values()) + list(contexts.values()) + assertions} | set(entries) | {inputs['register']['artifact_id']}
    require(len(version_ids) == len(set(version_ids)), 'Duplicate fixture version identity')
    require(not (set(version_ids) & artifact_ids or set(version_ids) & set(cases_by_id) or artifact_ids & set(cases_by_id)),
            'Fixture identity family collision')
    for row in version_rows:
        require(row['source_record_id'] in sources, 'Fixture source missing')
        canonical(row['recorded_at'])
    for row in list(supports.values()) + list(contexts.values()) + assertions:
        require(all(isinstance(row[k], str) and row[k].strip() for k in ('narrative', 'source_locator', 'interpretation_origin')),
                'Fixture provenance missing')
    require(len(supports) == 11 and len(contexts) == 3 and len(assertions) == 8, 'Concrete fixture denominator')
    for row in supports.values():
        if row['native_class'] == 'RKM-C006':
            require(supports[row['scheme_version_id']]['native_class'] == 'RKM-C018', 'Term scheme target type')
    for row in contexts.values():
        pins = row['objective_version_ids']
        require(pins == sorted(set(pins)), 'Duplicate/unsorted objective pin')
        require(all(supports[p]['native_class'] == 'RKM-X02' for p in pins), 'Objective target type')

    require(set(oracles['get']) == {r['version_id'] for r in assertions}, 'Literal version oracle denominator')
    for row in assertions:
        answer = oracles['get'][row['version_id']]
        for key in ('version_id', 'artifact_id', 'case_id', 'term_version_id', 'context_version_id', 'narrative',
                    'source_record_id', 'source_locator', 'interpretation_origin', 'recorded_at'):
            require(answer[key] == row[key], 'Literal answer/input disagreement: ' + row['version_id'] + '/' + key)
        term = supports[row['term_version_id']]
        scheme = supports[term['scheme_version_id']]
        context = contexts[row['context_version_id']] if row['context_version_id'] else None
        require(term['native_class'] == 'RKM-C006' and row['case_id'] in cases_by_id, 'Mandatory native target missing')
        require(answer['term_id'] == term['artifact_id'] and answer['scheme_id'] == scheme['artifact_id']
                and answer['scheme_version_id'] == scheme['version_id'], 'Literal term/scheme pin disagreement')
        require(answer['context_id'] == (context['artifact_id'] if context else None)
                and answer['objective_version_ids'] == (context['objective_version_ids'] if context else []),
                'Literal objective/context pin disagreement')
        expected_readiness = ('NOT_READY_CONTEXT_UNRECORDED' if context is None else
                              'NOT_READY_OBJECTIVES_UNRECORDED' if not context['objective_version_ids'] else
                              'READY_FOR_DECLARED_RETRIEVAL')
        require(answer['readiness'] == expected_readiness, 'Literal missingness/readiness disagreement')
        recorders = [r for r in revisions if row['version_id'] in r['nature_version_ids']]
        require(recorders and answer['recording_entry_version_ids'] == sorted(r['version_id'] for r in recorders),
                'Recording revision ownership disagreement')
        for recorder in recorders:
            require(entries[recorder['entry_id']]['case_id'] == row['case_id'], 'Recording revision case disagreement')
        require(all(supports[p]['recorded_at'] <= row['recorded_at'] for p in
                    [row['term_version_id'], term['scheme_version_id']]), 'Fixture dependency issued later')
    for case_id, expected in oracles['by_case'].items():
        require(expected == sorted(r['version_id'] for r in initial if r['case_id'] == case_id), 'Literal case filter disagreement')
    for case_id, expected in oracles['after_later_by_case'].items():
        require(expected == sorted(r['version_id'] for r in assertions if r['case_id'] == case_id), 'Literal later case filter disagreement')

    corrections = {r['corrected_version_id']: r for r in inputs['corrections']}
    require(len(corrections) == len(inputs['corrections']) == 2, 'Correction fixture denominator')
    for root, expected in oracles['family'].items():
        depths = {root: 0}
        for _ in range(len(assertions)):
            for child, edge in corrections.items():
                if edge['prior_version_id'] in depths:
                    depths[child] = depths[edge['prior_version_id']] + 1
        rows = [[v, depth, corrections[v]['prior_version_id'] if v in corrections else None]
                for v, depth in sorted(depths.items(), key=lambda item: (item[1], item[0]))]
        require(rows == expected, 'Literal correction family disagreement')

    require(oracles['status'] == 'EXPECTED_NOT_OBSERVED', 'Promoted literal outcomes')
    graphs = {str(g.identifier): g for g in dataset.graphs() if len(g)}
    require(set(graphs) == set(oracles['get']) == set(oracles['rdf_rows']) and len(graphs) == 8, 'Native graph denominator')
    relation_ids = {r['id'] for r in model['associations']}
    generalizations = {r['specific']: r['general'] for r in model['generalizations']}
    allowed_predicates = {RDF.type} | {URIRef(RISK + r) for r in ('R-41','R-42','R-43','R-44','R-05','RK2-011','RX-006','R-33','R-01','RX-008')}
    query = (ROOT / NS / 'native-query.rq').read_text()
    for ident, graph in graphs.items():
        answer = oracles['get'][ident]
        assertion = URIRef(answer['artifact_id'])
        require(set(graph.predicates()) <= allowed_predicates, 'Unexpected native predicate')
        require(not list(graph.subjects(RDF.type, URIRef(RISK + 'RKM-C004'))), 'Invented occurrence')
        require((URIRef(ident), RDF.type, URIRef(RISK + 'RKM-C005')) not in graph, 'Version mis-typed as assertion')
        for subject, predicate, obj in graph:
            require(all(isinstance(x, URIRef) for x in (subject, predicate, obj)), 'Unexpected literal/blank native term')
            if predicate == RDF.type:
                cls = str(obj).removeprefix(RISK)
                require(cls in native, 'New native class')
                if cls in generalizations:
                    require((subject, RDF.type, URIRef(RISK + generalizations[cls])) in graph, 'Missing inherited native type')
            else:
                rel_id = str(predicate).removeprefix(RISK)
                require(rel_id in relation_ids, 'New native relation')
                rel = native[rel_id]
                require((subject, RDF.type, URIRef(RISK + rel['source'])) in graph
                        and (obj, RDF.type, URIRef(RISK + rel['target'])) in graph, 'Wrong native relation endpoint')
        require(len(list(graph.objects(assertion, URIRef(RISK + 'R-41')))) == 1
                and len(list(graph.objects(assertion, URIRef(RISK + 'R-42')))) == 1
                and len(list(graph.objects(assertion, URIRef(RISK + 'R-43')))) <= 1
                and len(list(graph.subjects(URIRef(RISK + 'R-44'), assertion))) >= 1,
                'Native mandatory/optional multiplicity')
        rows = [[str(x) if x is not None else None for x in row]
                for row in dataset.query(query, initBindings={'graph': URIRef(ident)})]
        require(rows == oracles['rdf_rows'][ident], 'Literal RDF/query answer disagreement: ' + ident)
        require(len(rows) == len(answer['recording_entry_version_ids']) * max(1, len(answer['objective_version_ids'])),
                'RDF row multiplicity disagreement')
        for row in rows:
            expected_prefix = [ident, answer['artifact_id'], answer['case_id'], answer['term_id'], answer['term_version_id'],
                               answer['scheme_id'], answer['scheme_version_id'], answer['context_id'], answer['context_version_id']]
            require(row[:9] == expected_prefix, 'RDF/query literal pin disagreement')
            require(row[-1] in answer['recording_entry_version_ids'], 'RDF recording pin disagreement')
            require(row[-2] in answer['objective_version_ids'] if answer['objective_version_ids'] else row[-2] is None,
                    'RDF objective pin disagreement')

    require(prior['scope'] == 'ACTUAL_EXISTING_SCHEMA9_BASELINE_ONLY_NO_NEW_RUNTIME'
            and prior['schema_version'] == 9 and len(prior['table_counts']) == 28
            and prior['table_counts']['assessment_selection_event'] == 6
            and set(prior['native_views']) == {'v_native_facts','v_assessment_quads','v_evidence_quads','v_knowledge_quads'},
            'Prior population reference drift')
    return dict(derived_requirements=10, fixed_runtime_controls=60, runtime_controls_executed=0,
                native_source_routes=31, literal_graphs=8, literal_quads=sum(len(g) for g in graphs.values()),
                literal_rdf_query_rows=sum(len(x) for x in oracles['rdf_rows'].values()), independent_ratings=0)


def check(root=ROOT, require_no_runtime=False):
    manifest = read(root, NS + '/declaration-manifest.json')
    require(set(manifest['files_sha256']) == set(DECLARATION_FILES), 'Declaration binding population drift')
    for path, expected in manifest['files_sha256'].items():
        require(not Path(path).is_absolute() and '..' not in Path(path).parts, 'Unsafe declaration path')
        require(sha((root / path).read_bytes()) == expected, 'Declaration binding drift: ' + path)
    contract = read(root, NS + '/contract.json')
    check_sources(contract, root)
    negatives = read(root, NS + '/negative-inputs.json')
    require(negatives['status'] == 'PREIMPLEMENTATION_INPUTS_AND_EXPECTED_REJECTIONS'
            and negatives['variant_count'] == len(negatives['variants'])
            and len({r['id'] for r in negatives['variants']}) == len(negatives['variants']) >= 40,
            'Missing concrete negative variants')
    fixed = {r['id']:r for r in read(root, NS + '/fixtures.json')['cases']}
    for row in negatives['variants']:
        require(row['control'] in fixed and row['expected']['rejected'] is True
                and row['expected']['all_preoperation_state_preserved'] is True,
                'Unbound concrete negative variant')
    dataset = Dataset()
    dataset.parse(root / NS / 'native-oracles.trig', format='trig')
    summary = validate_semantics(read(root, 'ontology/riskium-model.json'), contract,
                                 read(root, NS + '/fixtures.json'), read(root, NS + '/execution-fixture.json'),
                                 read(root, NS + '/query-oracles.json'), dataset, read(root, NS + '/prior-population.json'))
    for version, total in (('0.3.5', 687), ('0.3.6', 780)):
        selected = read(root, 'releases/selection-v' + version + '.json')['selected_files_sha256']
        require(len(selected) == total, 'Published selected population drift')
        for path, expected in selected.items():
            actual_path = 'documentation/0.4.1/Repository.md' if version == '0.3.6' and path == '.github/README.md' else path
            require(sha((root / actual_path).read_bytes()) == expected, 'Published component drift: ' + path)
    accounting = read(root, 'evaluation/relational/evidence-lifecycle/mapping-accounting.json')
    require(len(accounting['rows']) == 306
            and sum(r['disposition'] == 'DEFERRED_NO_COMPLETE_SQL_MAPPING' for r in accounting['rows']) == 236,
            'Historical mapping population changed')
    present = [p for p in RUNTIME_PATHS if (root / p).exists()]
    if require_no_runtime:
        require(not present, 'Runtime preceded declaration readback')
    return dict(status='RISK_NATURE_DECLARATION_VALID', scope='SOURCE_AND_LITERAL_ORACLE_VALIDATION_ONLY',
                **summary, concrete_negative_variants=negatives['variant_count'],
                protected_v035_files=687, protected_v036_files_except_live_README=779,
                prospective_runtime_paths_present=present, files_sha256=manifest['files_sha256'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-no-runtime', action='store_true')
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    result = check(require_no_runtime=args.require_no_runtime)
    if args.receipt:
        require(not subprocess.check_output(['git','status','--porcelain'], cwd=ROOT).strip(), 'Receipt requires clean source')
        result.update(source_commit=subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip(),
                      observed_at=datetime.now(timezone.utc).isoformat(), no_runtime_required=args.require_no_runtime)
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'files_sha256'}, sort_keys=True))


if __name__ == '__main__':
    main()
