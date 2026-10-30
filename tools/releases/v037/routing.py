"""Bind v0.3.7 qualification to main while retaining immutable legacy diagnostics."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
POLICY = 'releases/routing-v0.3.7.json'
REPO = 'ArazSaieArasi3/riskium'
PATHS = dict(qualification='release-v037.yml', suite='v036-versioned-suite.yml',
             reader='released-reader-main.yml', legacy='incremental-release.yml')
PRESERVED = {
    '.github/workflows/incremental-release.yml': 'b87d98fea2a6b14244e1a47f1e29ff6ef618a3285e4b40d6dc7b878d29997d93',
    'tools/prepare_incremental_release.py': 'e860c2f5250d548ecdc18694a207e642b25f8ee52a226f0ddb55c4b6918b301a',
    'tools/publication/nature_main_gate.py': '460be166e34073f4133422dead2992399b1208d9bf2ff0477d78c8faa8a904c8',
    '.github/workflows/released-reader-main.yml': 'f15cf1773fcab3c0762e51d15dde56c8c77c50ce7971152173f6b098727fe145',
}
ERRORS = ('Published README drift', 'Active README drift',
          'test_assessment_documentation.CandidateReader',
          'test_published_documentation.PublishedReaderDocumentation',
          'test_released_documentation.PublishedReader')


def require(value, message):
    if not value:
        raise ValueError(message)


def check(root=ROOT):
    policy = json.loads((root / POLICY).read_bytes())
    require(policy['schema'] == 'riskium-v037-main-routing-v1'
            and policy['legacy_role'] == 'RETAINED_HISTORICAL_DIAGNOSTIC_NOT_A_V037_RELEASE_GATE'
            and policy['required_success'] == ['qualification', 'suite', 'reader']
            and policy['legacy_expected_errors'] == list(ERRORS)
            and policy['preserved_sha256'] == PRESERVED, 'Routing policy changed')
    for path, digest in policy['preserved_sha256'].items():
        require(hashlib.sha256((root / path).read_bytes()).hexdigest() == digest,
                'Preserved publisher/gate changed: ' + path)
    workflow = (root / '.github/workflows/release-v037.yml').read_text()
    require('branches: [main, plan/v0.3.7-packaging]' in workflow
            and 'python tools/releases/v037/routing.py --check' in workflow,
            'Successor qualification is not connected to main')
    return policy


def validate_runs(evidence):
    source = evidence['source_commit']
    require(len(source) == 40 and all(c in '0123456789abcdef' for c in source), 'Invalid source')
    require(set(evidence['runs']) == set(PATHS), 'Missing source gate')
    for role, filename in PATHS.items():
        run = evidence['runs'][role]
        require(run['head_sha'] == source and run['head_branch'] == 'main'
                and run['path'] == '.github/workflows/' + filename
                and run['repository']['full_name'] == run['head_repository']['full_name'] == REPO
                and run['event'] == ('workflow_run' if role == 'reader' else 'push'),
                'Untrusted source gate: ' + role)
        require(run['status'] == 'completed', 'Unsettled source gate: ' + role)
        require(run['conclusion'] == ('failure' if role == 'legacy' else 'success'),
                'Unexpected source gate result: ' + role)
    require(all(message in evidence['legacy_job_log'] for message in ERRORS), 'Unexpected legacy failure')
    # Require the legacy failure to be exactly the three historical setup errors.
    log = evidence['legacy_job_log']
    require('FAILED (errors=3)' in log and 'FAILED (failures=' not in log,
            'Legacy has additional failures')
    return dict(status='V037_MAIN_ROUTING_AND_QUALIFICATION_PASS', source_commit=source,
                legacy_role='RETAINED_HISTORICAL_DIAGNOSTIC_NOT_A_V037_RELEASE_GATE',
                required_gates_passed=['qualification', 'suite', 'reader'],
                frozen_or_published=False, next_gate='FINAL_EXACT_SOURCE_FREEZE')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--evidence-json', type=Path)
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    check()
    result = dict(status='V037_MAIN_ROUTING_SOURCE_CHECK_PASS', actual_main_runs_verified=False)
    if args.evidence_json:
        result = validate_runs(json.loads(args.evidence_json.read_bytes()))
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
