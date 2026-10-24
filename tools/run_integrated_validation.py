"""Execute fixed shared-graph controls and replay source-bound graph receipts."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import gzip
import hashlib
import importlib.metadata
import json
import subprocess
import sys

from rdflib import Graph, RDF, URIRef
from rdflib.util import from_n3
from rdflib.compare import isomorphic, to_canonical_graph

from build_shacl import ROOT, SH
from run_admission_shacl import graph_snapshot
from validate_integrated import POLICY, compile_graph, digest, execute_compiled, load_policy

OUT = ROOT / 'evaluation/integration'
INPUTS = ['implementation/validation/0.1.0/policy.json', 'evaluation/integration/cases.json',
          'evaluation/integration/fixtures.ttl', 'tools/validate_integrated.py',
          'tools/run_integrated_validation.py', 'tools/run_shacl.py', 'tools/build_shacl.py',
          'tools/build_admission_shapes.py', 'tools/build_endpoint_shapes.py',
          'tools/build_comparison_shapes.py', 'tools/build_qualification_shapes.py',
          'tools/run_admission_shacl.py', 'tools/run_endpoint_shacl.py', 'tools/requirements-shacl.txt']


def snapshot(graph, registry):
    # These fixed fixtures have named data/focus nodes. Canonical blank-node
    # labels deduplicate identical composed shapes across separately parsed
    # module graphs; this changes no RDF statement or engine input.
    return graph_snapshot(to_canonical_graph(graph), registry)


def fixture(case, cohort):
    graph = Graph().parse(OUT / 'fixtures.ttl', format='turtle')
    for triple in case['remove']:
        terms = tuple(map(from_n3, triple))
        if terms not in graph:
            raise ValueError('Fixture removal is not present: ' + case['id'])
        graph.remove(terms)
    for triple in case['insert']:
        graph.add(tuple(map(from_n3, triple)))
    requests = json.loads(json.dumps(cohort['requests']))
    requests.update(case['request_patch'])
    return graph, requests


def execute(case, cohort, graphs):
    graph, requests = fixture(case, cohort)
    row = {k: v for k, v in case.items() if k not in ('remove', 'insert', 'request_patch')}
    row.update(requests=requests, raw_graph=snapshot(graph, graphs), task_admissible=False)
    try:
        data, shapes, aliases = compile_graph(graph, requests, case['profile'])
    except ValueError as exc:
        row.update(decision='PROFILE_REJECTED', error=str(exc), findings=[], engine_executed=False)
        aliases = {}
    else:
        if case['mutation']:
            triple = tuple(URIRef(x) for x in case['mutation']['remove'])
            if triple not in shapes:
                raise ValueError('Mutation rule not present: ' + case['id'])
            shapes.remove(triple)
        row.update(data_graph=snapshot(data, graphs), shapes_graph=snapshot(shapes, graphs), identity_map=aliases)
        if case['profile'] == 'raw':
            if set(data) != set(graph) or len(shapes):
                raise ValueError('Raw staging was altered or given shapes')
            row.update(decision='STAGING_ONLY', findings=[], engine_executed=False, raw_preserved=True)
        else:
            result, result_graph = execute_compiled(data, shapes, case['profile'])
            row.update(result, result_graph=snapshot(result_graph, graphs))
    expected = sorted({(s, c, aliases.get(f, f)) for s, c, f in case['expected_findings']})
    row['expected_findings'] = expected
    row['status'] = 'PASS' if row['decision'] == case['expected_decision'] and row['findings'] == expected and row['engine_executed'] == case['expected_engine_executed'] else 'FAIL'
    return row


def run():
    policy = load_policy()
    cohort = json.loads((OUT / 'cases.json').read_text())
    if cohort['policy_sha256'] != digest(POLICY) or cohort['fixture_sha256'] != digest(OUT / 'fixtures.ttl'):
        raise ValueError('Fixed policy/fixture binding changed')
    cases = cohort['cases']
    if len({c['id'] for c in cases}) != len(cases):
        raise ValueError('Duplicate integration case identity')
    graphs = {}
    rows = [execute(case, cohort, graphs) for case in cases]
    failed = [r for r in rows if r['status'] != 'PASS']
    if failed:
        for r in failed:
            print(json.dumps({k: r.get(k) for k in ('id', 'decision', 'expected_decision', 'findings', 'expected_findings', 'error')}), flush=True)
        raise ValueError('Integration fixture/oracle mismatch')
    inputs = sorted(set(INPUTS) | set(policy['frozen_inputs']))
    return dict(schema='riskium-integrated-validation-evidence-v1', generated_at_utc=datetime.now(timezone.utc).isoformat(),
        source_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        source_commit_role='Execution checkout; all evaluated inputs separately SHA-256 bound; receipt may be committed later.',
        oracle_predeclaration_commit='6243411579029120459cdd914a17b6006c7cdbbf',
        profile_version='0.1.0', compatible_model='0.3.1', inputs={p: digest(ROOT / p) for p in inputs},
        runtime_python=sys.version.split()[0], engine={p: importlib.metadata.version(p) for p in ('pyshacl', 'rdflib', 'owlrl')},
        inference='none; pinned native subclass triples only', imports=False,
        summary=dict(scenarios=len(rows), engine_executions=sum(r['engine_executed'] for r in rows),
            preflight_rejections=sum(r['decision'] == 'PROFILE_REJECTED' for r in rows),
            staging_cases=sum(r['decision'] == 'STAGING_ONLY' for r in rows), mutation_controls=sum(bool(r['mutation']) for r in rows),
            module_families=len(policy['modules']), selected_relations=len(policy['endpoint_relations']),
            statuses=dict(Counter(r['status'] for r in rows)), decisions=dict(Counter(r['decision'] for r in rows))),
        native_semantics_changed=False, historical_engine_outcomes_changed=False,
        new_owner_decision=False, independent_semantic_acceptance=False,
        graphs=graphs, cases=rows, limits=policy['limits'])


def verify_saved(stored, fresh):
    for key in ('schema', 'oracle_predeclaration_commit', 'profile_version', 'compatible_model', 'inputs', 'summary',
                'inference', 'imports', 'native_semantics_changed', 'historical_engine_outcomes_changed',
                'new_owner_decision', 'independent_semantic_acceptance', 'limits'):
        if stored[key] != fresh[key]:
            raise ValueError('Saved integration receipt differs: ' + key)
    for key, graph in stored['graphs'].items():
        if hashlib.sha256(graph['text'].encode()).hexdigest() != key:
            raise ValueError('Saved integration graph hash mismatch')
    if len(stored['cases']) != len(fresh['cases']):
        raise ValueError('Saved integration cohort differs')
    for old, new in zip(stored['cases'], fresh['cases']):
        for key in ('id', 'profile', 'requests', 'mutation', 'decision', 'expected_decision', 'findings',
                    'expected_findings', 'engine_executed', 'status', 'task_admissible'):
            if json.dumps(old[key], sort_keys=True) != json.dumps(new[key], sort_keys=True):
                raise ValueError('Saved integration oracle differs: ' + new['id'] + ' ' + key)
        for field in ('raw_graph', 'data_graph', 'shapes_graph'):
            if field in old or field in new:
                if field not in old or field not in new or not isomorphic(
                    Graph().parse(data=stored['graphs'][old[field]]['text'], format='nt'),
                    Graph().parse(data=fresh['graphs'][new[field]]['text'], format='nt')):
                    raise ValueError('Saved integration effective graph differs: ' + new['id'])
        if old['engine_executed']:
            graph = Graph().parse(data=stored['graphs'][old['result_graph']]['text'], format='nt')
            root = next(graph.subjects(RDF.type, SH.ValidationReport))
            findings = sorted({(str(graph.value(n, SH.sourceShape)), str(graph.value(n, SH.sourceConstraintComponent)), str(graph.value(n, SH.focusNode))) for n in graph.objects(root, SH.result)})
            if json.dumps(findings) != json.dumps(old['findings']) or graph.value(root, SH.conforms).toPython() != old['conforms']:
                raise ValueError('Saved integration result graph contradicts receipt')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    report = run()
    path = OUT / 'report.json.gz'
    if args.check:
        verify_saved(json.loads(gzip.decompress(path.read_bytes())), report)
    else:
        path.write_bytes(gzip.compress((json.dumps(report, indent=2) + '\n').encode(), mtime=0))
        lines = ['# Shared-graph validation profile 0.1.0', '',
            'Executed engineering supplement after stable v0.3.1. Seven module families run together; 29 selected relation pairs. This does not rewrite historical engine outcomes or grant full native/task acceptance.', '',
            'The [fixed graph](fixtures.ttl), [exact expected findings](cases.json) and [policy](../../implementation/validation/0.1.0/policy.json) were committed before the validator. The two joint rules prevent separately admissible threshold/comparison declarations from silently using different scales or versions.', '',
            'Summary: ' + json.dumps(report['summary']) + '.', '',
            'Mutation controls deliberately remove one rule; admitting their bad inputs demonstrates sensitivity, not acceptable domain data. Raw staging and catalog metadata acceptance never become task acceptance.', '',
            '[Full graph/input/result receipt](report.json.gz). Replay: `python tools/run_integrated_validation.py --check`.', '',
            '| Case | Expected | Observed | Engine | Control | Result |', '| --- | --- | --- | --- | --- | --- |']
        for row in report['cases']:
            lines.append(f"| {row['id']} | {row['expected_decision']} | {row['decision']} | {row['engine_executed']} | {'mutation' if row['mutation'] else 'fixed'} | {row['status']} |")
        (OUT / 'README.md').write_text('\n'.join(lines) + '\n')
    print(json.dumps(report['summary']), flush=True)


if __name__ == '__main__':
    main()
