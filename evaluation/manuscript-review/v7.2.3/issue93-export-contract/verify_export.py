"""Replay B0-4 export, bounded engines and frozen-baseline regression."""
import argparse
import importlib.util
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from rdflib import Graph
from rdflib.namespace import OWL
from jsonschema import Draft202012Validator, FormatChecker
from pyshacl import validate
import export_candidate as export

HERE = export.HERE
ROOT = export.ROOT


def run(argv):
    start = time.monotonic()
    p = subprocess.run([str(a) for a in argv], cwd=ROOT, capture_output=True, text=True, timeout=120)
    return {'exit_code': p.returncode, 'stdout': p.stdout.strip(), 'stderr': p.stderr.strip(),
            'elapsed_ms': round((time.monotonic() - start) * 1000)}


def main(args):
    assert export.digest(args.schema) == '094324d8e6ac4505ef5ae983a45bb9b56a8b3b6960151c57736756a037344d38'
    assert export.digest(args.robot) == '53cd275c8e4c0dad1fc2c1c34174876795cd7d6b6926e1444adcbb0cb3c7ab26'
    contract = json.loads(export.CONTRACT.read_text())
    receipt = export.export(contract)
    export.export(contract, check=True)
    generated = HERE / 'generated'
    native_path = generated / 'candidate.ontouml.json'
    native = json.loads(native_path.read_text())
    errors = [str(e.json_path) + ': ' + e.message for e in Draft202012Validator(
        json.loads(args.schema.read_text()), format_checker=FormatChecker(formats=['date', 'date-time', 'uri'])).iter_errors(native)]
    tests = run([sys.executable, '-m', 'unittest', 'discover', '-s', str(HERE), '-p', 'test_export_contract.py', '-v'])
    regressions = {}
    for pattern in ['test_native_exchange.py', 'test_owl_mapping.py', 'test_source_transition.py']:
        result = run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-p', pattern, '-v'])
        match = re.search(r'Ran (\d+) tests?', result['stderr'])
        result['tests'] = int(match[1]) if match else 0
        regressions[pattern] = result
    sdk = run([args.node, HERE.parent / 'issue93-integration/native_roundtrip.cjs', native_path, args.sdk, generated / 'sdk-roundtrip.json'])
    graph = Graph().parse(generated / 'candidate.owl.ttl', format='turtle')
    graph.serialize(generated / 'candidate.rdf', format='xml')
    hermit = run(['java', '-Xmx512m', '-cp', args.robot, 'org.semanticweb.HermiT.cli.CommandLine', '-k', generated / 'candidate.rdf'])
    profile = run(['java', '-Xmx512m', '-jar', args.robot, 'validate-profile', '--input', generated / 'candidate.owl.ttl', '--profile', 'DL', '--output', generated / 'owl-profile-DL.txt'])
    sys.path.insert(0, str(HERE.parent / 'issue93-evidence-use'))
    spec = importlib.util.spec_from_file_location('export_evidence_cases', HERE.parent / 'issue93-evidence-use/verify_candidate.py')
    evidence = importlib.util.module_from_spec(spec); spec.loader.exec_module(evidence)
    shapes = Graph().parse(export.checked_file(contract['downstream_bindings']['shacl']), format='turtle')
    fixtures = evidence.cases()
    g = evidence.fixture(); g.add((evidence.EX.item, OWL.sameAs, evidence.EX.ref))
    fixtures.append(('aliased-participants', g, False))
    g = evidence.fixture(); g.add((evidence.EX.item, OWL.sameAs, evidence.EX.alias)); g.add((evidence.EX.ref, OWL.sameAs, evidence.EX.alias))
    fixtures.append(('alias-chain-participants', g, False))
    rows = []
    for name, data, expected in fixtures:
        observed, _, _ = validate(data, shacl_graph=shapes, ont_graph=graph, inference='none', advanced=False, do_owl_imports=False)
        rows.append({'case': name, 'expected_conforms': expected, 'observed_conforms': bool(observed), 'pass': bool(observed) == expected})
    sdk_receipt = json.loads((generated / 'sdk-roundtrip.json').read_text()) if sdk['exit_code'] == 0 else {}
    controls = {
        'deterministic_export_check': True,
        'contract_tests': tests['exit_code'] == 0 and 'Ran 14 tests' in tests['stderr'],
        'pinned_native_schema': not errors,
        'sdk_roundtrip': sdk_receipt.get('status') == 'PASS',
        'hermit_consistency': hermit['exit_code'] == 0 and 'is satisfiable.' in hermit['stdout'] and 'not satisfiable' not in hermit['stdout'],
        'owl2_dl_profile': profile['exit_code'] == 0,
        'combined_shacl': len(rows) == 20 and all(r['pass'] for r in rows),
        'baseline_regressions': all(r['exit_code'] == 0 and r['tests'] for r in regressions.values()),
        'frozen_input_hashes_preserved': all(export.digest(export.resolve(e['path'])) == e['sha256'] for e in contract['frozen_inputs']),
    }
    report = {
        'schema': 'riskium-issue93-export-contract-verification-1', 'date_tehran': '2026-11-08',
        'status': 'B04_NATIVE_OWL_CONTRACT_COMPLETE_NOT_PROMOTED' if all(controls.values()) else 'FAIL',
        'source_candidate_commit': 'f3d6b28d32d27721a52470d7e0365ae42f5959de',
        'checks': controls,
        'summary': {'contract_tests': 14, 'contract_tests_passed': 14 if controls['contract_tests'] else 0,
                    'baseline_regression_tests': sum(r['tests'] for r in regressions.values()),
                    'baseline_regression_passed': sum(r['tests'] for r in regressions.values() if r['exit_code'] == 0),
                    'combined_shacl_cases': len(rows), 'combined_shacl_matches': sum(r['pass'] for r in rows),
                    'negative_data_controls': sum(not r['expected_conforms'] for r in rows),
                    'sdk_elements': sdk_receipt.get('checked_elements'), 'native_schema_errors': len(errors),
                    'production_promoted': False},
        'export_receipt': receipt, 'native_schema_errors': errors, 'contract_tests': tests,
        'baseline_regressions': regressions, 'sdk': sdk_receipt,
        'hermit_consistency': hermit, 'owl_profile': profile, 'shacl_cases': rows,
        'boundary': 'P1 native/OWL contract route is complete. Full dictionary/readers/CI reconciliation and P2 database use mapping remain open. No production migration, real-data result, historical test rerun or overall semantic acceptance is inferred.'}
    (HERE / 'verification-report.json').write_text(export.dump(report))
    print(export.dump({'status': report['status'], 'checks': controls, 'summary': report['summary']}))
    if not all(controls.values()):
        raise SystemExit(1)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    for name in ['schema', 'robot', 'sdk', 'node']:
        ap.add_argument('--' + name, type=Path, required=True)
    main(ap.parse_args())
