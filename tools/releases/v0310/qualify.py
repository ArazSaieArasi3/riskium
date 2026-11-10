"""Reproduce and qualify the prepared N4 component, not a live publication."""
import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
import curation
import guard
import projection
import reader


def qualify(output, source_ref, mode):
    output = Path(output).resolve()
    curation.need(not output.exists(), 'Use an empty qualification destination')
    curation.build(check=True)
    reader.build(check=True)
    preserved = guard.check()
    checkout = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=curation.ROOT, text=True).strip()
    dirty = bool(subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=all'], cwd=curation.ROOT, text=True).strip())
    if mode == 'CI':
        curation.need(source_ref == checkout and not dirty, 'CI must qualify its clean exact checkout')
    with tempfile.TemporaryDirectory() as temp:
        a, b = Path(temp) / 'a', Path(temp) / 'b'
        result = projection.build(a, source_ref)
        projection.build(b, source_ref)
        ma = curation.load(a / 'projection-manifest.json')
        mb = curation.load(b / 'projection-manifest.json')
        curation.need(ma == mb, 'Non-reproducible projection manifest')
        curation.need(all((a / n).read_bytes() == (b / n).read_bytes() for n in ma['files_sha256']), 'Non-reproducible projection bytes')
        tests = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', str(Path(__file__).parent), '-p', 'test_contracts.py', '-v'],
                               cwd=curation.ROOT, capture_output=True, text=True)
        curation.need(tests.returncode == 0, tests.stdout + tests.stderr)
        output.mkdir(parents=True)
        import shutil
        shutil.copytree(a, output / 'projection')
        (output / 'tests.txt').write_text(tests.stdout + tests.stderr)
        report = {'schema': 'riskium-n4-qualification/1', 'status': 'PASS_PREPARED_COMPONENT_NOT_PUBLICATION',
                  'environment': mode, 'source_ref': source_ref, 'exact_commit_ref': ma['exact_commit_ref'],
                  'source_snapshot': {'checkout_sha': checkout, 'working_tree_dirty': dirty,
                                      'clean_exact_checkout': source_ref == checkout and not dirty},
                  'ci_run_id': os.environ.get('GITHUB_RUN_ID') if mode == 'CI' else None,
                  'source_guard': preserved, 'review_summary': curation.load(curation.REVIEW)['summary'],
                  'projection': result, 'reproduction': {'independent_builds': 2, 'identical_files': len(ma['files_sha256']) + 1,
                                                      'projection_manifest_sha256': curation.sha((a / 'projection-manifest.json').read_bytes())},
                  'contracts': {'exit_code': 0, 'passed': int(re.search(r'Ran (\d+) tests?', tests.stderr)[1]),
                                'report_sha256': curation.sha((tests.stdout + tests.stderr).encode())},
                  'inputs_sha256': {str(p.relative_to(curation.ROOT)): curation.sha(p.read_bytes()) for p in
                                    [curation.REVIEW, curation.OUT / 'component.json', reader.OUT / 'manifest.json',
                                     Path(__file__).parent / 'requirements.txt', curation.ROOT / '.github/workflows/curation-v0310.yml'] + sorted(Path(__file__).parent.glob('*.py'))},
                  'boundaries': {'ontology_engine_run': False, 'independent_semantic_rating': False, 'formal_alignment_adopted': False,
                                 'live_publication': False, 'live_channel_readback': False, 'article_changed': False,
                                 'normative_followup_issue': 78, 'independent_review_issue': 23, 'next_gate': 'N5'}}
        (output / 'qualification.json').write_text(curation.dump(report))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--commit', required=True)
    parser.add_argument('--mode', choices=['LOCAL', 'CI'], default='LOCAL')
    args = parser.parse_args()
    print(curation.dump(qualify(args.output, args.commit, args.mode)))
