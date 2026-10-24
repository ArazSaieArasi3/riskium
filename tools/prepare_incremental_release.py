"""Check and package an immutable development candidate; never publish a release."""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[1]


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])


def require_prerelease(tag, model_version):
    if not re.fullmatch(r'v[0-9]+\.[0-9]+\.[0-9]+-rc\.[1-9][0-9]*', tag):
        raise ValueError('Only an explicit vX.Y.Z-rc.N development prerelease is supported')
    if tag.split('-rc.')[0] != 'v' + model_version:
        raise ValueError('Package version must name the evaluated conceptual baseline')


def snapshot(root, ref, output, tag=None, checks=None):
    root, output = Path(root), Path(output)
    commit = git(root, 'rev-parse', '--verify', ref + '^{commit}').decode().strip()
    model = json.loads(git(root, 'show', commit + ':ontology/riskium-model.json'))
    if tag:
        require_prerelease(tag, model['version'])
    name = tag or 'candidate-' + commit[:12]
    if output.resolve().is_relative_to(root.resolve()):
        raise ValueError('Keep release output outside the source checkout')
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise ValueError('Output directory must be empty; existing packages are never overwritten')
    entries, blobs = [], []
    for record in git(root, 'ls-tree', '-r', '-z', commit).split(b'\0'):
        if not record:
            continue
        header, raw_path = record.split(b'\t', 1)
        mode, kind, blob = header.split()
        path = raw_path.decode()
        if kind != b'blob' or mode not in (b'100644', b'100755'):
            raise ValueError('Only regular tracked files can enter the package: ' + path)
        data = git(root, 'cat-file', 'blob', blob.decode())
        entries.append({'path': path, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
        blobs.append((path, int(mode, 8) & 0o777, data))
    archive = output / ('riskium-' + name + '-source.tar.gz')
    # Fixed metadata makes a given source tree and package name reproducible.
    with archive.open('wb') as raw, gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode='w') as tar:
            for path, mode, data in blobs:
                item = tarfile.TarInfo('riskium-' + name + '/' + path)
                item.size, item.mode, item.mtime = len(data), mode, 0
                tar.addfile(item, io.BytesIO(data))
    with tarfile.open(archive) as tar:
        actual = [{'path': i.name.split('/', 1)[1], 'bytes': i.size,
                   'sha256': hashlib.sha256(tar.extractfile(i).read()).hexdigest()} for i in tar]
    if actual != entries:
        raise ValueError('Archive did not reproduce the pinned source inventory')
    manifest = {'schema': 'riskium-incremental-inventory-v1', 'source_commit': commit,
                'file_count': len(entries), 'files': entries,
                'scope': 'Tracked regular files only; no untracked manuscript, private database, external Wiki or new scientific engine run.'}
    (output / 'source-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    receipt = {'schema': 'riskium-incremental-candidate-v1', 'source_commit': commit,
               'model_version': model['version'], 'package_name': name,
               'maturity': 'development-prerelease', 'checks': checks or [],
               'archive_inventory_verified': True, 'publication_executed': False,
               'scientific_engine_receipts': 'Historical source-bound evidence retained; candidate checks explicitly name any fresh scoped replay. Packaging alone is not an engine run.',
               'independent_semantic_acceptance': 'NOT_ESTABLISHED'}
    (output / 'candidate-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    note = ('# Riskium ' + name + '\n\nDevelopment prerelease of conceptual baseline ' + model['version'] +
            '. Exact source commit: `' + commit + '`.\n\n'
            'This package contains the current public evidence and manuscript-review ledger; '
            'author-facing manuscript files and private historical database companions are not included. '
            'The original v0.3.1-rc.1 tag/archive remain unchanged.\n\n'
            'HermiT/SHACL receipts retain their actual versions and outstanding routes. '
            'Full formal/application acceptance, independent semantic adjudication and a stable scientific release are not implied. '
            'Consult docs/incremental-releases.md and the source-bound reports for exact claims and issue mapping.\n\n'
            'All candidate files have a SHA256SUMS inventory. Candidate preparation is distinct from publication.\n')
    if tag:
        note_path = 'docs/prerelease-' + tag + '.md'
        exists = subprocess.run(['git', '-C', str(root), 'cat-file', '-e', commit + ':' + note_path],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
        if exists:
            note = git(root, 'show', commit + ':' + note_path).decode() + '\n\nExact release source commit: `' + commit + '`.\n'
    (output / 'release-notes.md').write_text(note)
    sums = ''.join(hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + p.name + '\n'
                   for p in sorted(output.iterdir()) if p.is_file())
    (output / 'SHA256SUMS.txt').write_text(sums)
    return receipt


CHECKS = [
    ['tools/validate_model.py'], ['tools/build_native.py', '--check'],
    ['tools/build_owl.py', '--check'], ['tools/review_coverage.py'],
    ['tools/review_references.py', '--check'], ['tools/build_quality_report.py', '--check'],
    ['tools/run_cq.py', '--check'], ['tools/build_traceability.py', '--check'],
    ['tools/build_reference.py', '--check'], ['tools/publication/audit_portal.py'],
    ['tools/publication/build_versioned_site.py', '--check'],
    ['tools/run_compatibility_shacl.py', '--check'],
    ['tools/run_comparison_shacl.py', '--check'],
    ['tools/run_relational_history.py', '--check'],
    ['tools/run_source_cq06.py', '--check'],
    ['tools/run_source_cq0708.py', '--check'],
    ['tools/build_final_review.py', '--check'],
    ['tools/check_release_alignment.py'],
    ['tools/run_integrated_validation.py', '--check'],
    ['tools/build_relational_assessment.py', '--check'],
    ['tools/run_relational_assessment.py', '--check'],
    ['tools/check_database_assurance.py', '--check'],
    ['tools/check_research_backlog.py', '--check'],
    ['-m', 'unittest', 'discover', '-s', 'tests', '-v'],
]


def run_checks(root):
    if git(root, 'status', '--porcelain').strip():
        raise ValueError('A checked release candidate requires a clean source checkout')
    results = []
    for args in CHECKS:
        run = subprocess.run([sys.executable, *args], cwd=root, capture_output=True, text=True)
        results.append({'command': ['python', *args], 'exit_code': run.returncode,
                        'stdout': run.stdout, 'stderr': run.stderr})
        if run.returncode:
            raise ValueError('Candidate check failed: ' + ' '.join(args) + '\n' + run.stdout + run.stderr)
    if git(root, 'status', '--porcelain').strip():
        raise ValueError('Checks changed source files; review and commit them before packaging')
    return results


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--ref', default='HEAD')
    p.add_argument('--tag')
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--run-checks', action='store_true')
    a = p.parse_args()
    if a.run_checks and git(ROOT, 'rev-parse', a.ref + '^{commit}') != git(ROOT, 'rev-parse', 'HEAD'):
        p.error('Checks run against HEAD; checkout the intended immutable commit first')
    checks = run_checks(ROOT) if a.run_checks else []
    r = snapshot(ROOT, a.ref, a.output, a.tag, checks)
    print(json.dumps({'source_commit': r['source_commit'], 'package_name': r['package_name'],
                      'passed_checks': len(checks), 'inventory_verified': True,
                      'publication_executed': False}))


if __name__ == '__main__':
    main()
