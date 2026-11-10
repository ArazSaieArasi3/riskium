"""Qualify the full pre-publication candidate and source-pinned legacy routing."""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
import curation
import reader
import routing
import selection
import boundary
import compose


def qualify(out, source_ref, mode):
    out = Path(out).resolve()
    curation.need(not out.exists(), 'Use a new qualification destination')
    selected = selection.build(check=True)
    checked_boundary = boundary.check()
    checkout = routing.git('rev-parse', 'HEAD').decode().strip()
    dirty = bool(routing.git('status', '--porcelain', '--untracked-files=all').strip())
    if mode == 'CI':
        curation.need(checkout == source_ref and not dirty, 'CI requires a clean exact checkout')
    out.mkdir(parents=True)
    with tempfile.TemporaryDirectory() as temp:
        temp = Path(temp)
        old = compose.historical(temp / 'historical')
        old_build = old.build(temp / 'baseline-site', temp / 'baseline-wiki')
        old_guard = subprocess.run([sys.executable, '-B', 'tools/check_source_transition.py', '--check'], cwd=old.ROOT, capture_output=True, text=True)
        curation.need(old_guard.returncode == 0, old_guard.stdout + old_guard.stderr)
        old_selection = subprocess.run([sys.executable, '-B', 'tools/releases/v039/selection.py', '--check'], cwd=old.ROOT, capture_output=True, text=True)
        curation.need(old_selection.returncode == 0, old_selection.stdout + old_selection.stderr)
        historical = {'source_commit': routing.HISTORICAL, 'guard': __import__('json').loads(old_guard.stdout),
                      'selection': __import__('json').loads(old_selection.stdout), 'reader': old_build,
                      'prior_oracles_changed': False, 'new_ontology_engine_run': False}
        # Freshly rebuilt predecessor bodies are compared to the archived actual readback, not called fresh HTTP observations.
        prior = curation.load(curation.ROOT / 'evaluation/releases/v0.3.9/channels.json')
        matched = 0
        for row in prior['pages']['files']:
            curation.need(curation.sha((temp / 'baseline-site' / row['path']).read_bytes()) == row['sha256'], 'Predecessor body reconstruction differs: ' + row['path'])
            matched += 1
        historical['archived_pages_receipt_bodies_matched'] = matched
        result = compose.build(out / 'composition', source_ref, temp / 'baseline-site', temp / 'baseline-wiki', old)
        compose.build(temp / 'second', source_ref, temp / 'baseline-site', temp / 'baseline-wiki', old)
        files_a = {p.relative_to(out / 'composition').as_posix(): curation.sha(p.read_bytes()) for p in (out / 'composition').rglob('*') if p.is_file()}
        files_b = {p.relative_to(temp / 'second').as_posix(): curation.sha(p.read_bytes()) for p in (temp / 'second').rglob('*') if p.is_file()}
        differing = sorted(n for n in set(files_a) | set(files_b) if files_a.get(n) != files_b.get(n))
        curation.need(not differing, 'Composed independent builds differ: ' + ', '.join(differing[:20]))
        env = dict(os.environ, RISKIUM_N5A_TEST_COMPOSITION=str(out / 'composition'))
        transcripts, counts = {}, {}
        for pattern in ['test_contracts.py', 'test_n5a.py']:
            test = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', str(Path(__file__).parent), '-p', pattern, '-v'],
                                  cwd=curation.ROOT, capture_output=True, text=True, env=env)
            curation.need(test.returncode == 0, test.stdout + test.stderr)
            transcripts[pattern] = test.stdout + test.stderr
            counts[pattern] = int(re.search(r'Ran (\d+) tests?', test.stderr)[1])
        report = {'schema': 'riskium-n5a-qualification/1', 'status': 'PASS_N5A_CANDIDATE_NOT_PUBLISHED',
                  'source_ref': source_ref, 'environment': mode, 'ci_run_id': os.environ.get('GITHUB_RUN_ID') if mode == 'CI' else None,
                  'source_snapshot': {'checkout_sha': checkout, 'working_tree_dirty': dirty, 'clean_exact_checkout': checkout == source_ref and not dirty},
                  'boundary': checked_boundary, 'selection_sha256': curation.sha(selection.OUT.read_bytes()), 'selection_summary': selected['summary'],
                  'historical_replay': historical, 'composition': result, 'reproducible_files': len(files_a),
                  'composition_manifest_sha256': curation.sha((out / 'composition/site/publication-manifest.json').read_bytes()),
                  'curation_contracts_passed': counts['test_contracts.py'], 'composition_contracts_passed': counts['test_n5a.py'],
                  'inputs_sha256': selected['selected_files_sha256'],
                  'publication': False, 'live_channel_readback': False, 'article_version': '7.2.21',
                  'fresh_ontology_engine_run': False, 'independent_semantic_rating': False, 'next_gate': 'N5b'}
        (out / 'qualification.json').write_text(curation.dump(report))
        (out / 'tests.txt').write_text('\n'.join(transcripts.values()))
        subprocess.run(['git', 'worktree', 'remove', '--force', str(old.ROOT)], cwd=curation.ROOT, check=True, capture_output=True)
    return {k: v for k, v in report.items() if k != 'inputs_sha256'}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--commit', required=True)
    p.add_argument('--mode', choices=['LOCAL', 'CI'], default='LOCAL')
    a = p.parse_args()
    print(curation.dump(qualify(a.output, a.commit, a.mode)))
