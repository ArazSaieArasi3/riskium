"""Build six deterministic assets from committed Git objects, never worktree data."""
from pathlib import Path, PurePosixPath
import argparse, base64, gzip, hashlib, io, json, os, re, subprocess, tarfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
def digest(data): return hashlib.sha256(data).hexdigest()
def encoded(value): return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()
def git(*args): return subprocess.check_output(['git', *args], cwd=ROOT)
def require(ok, message):
    if not ok: raise ValueError(message)

def snapshot(commit):
    require(bool(re.fullmatch('[0-9a-f]{40}', commit)), 'Expected full SHA-1 source commit')
    raw = git('cat-file', 'commit', commit)
    rows = []
    for item in git('ls-tree', '-rz', commit).split(b'\0'):
        if not item: continue
        meta, path = item.split(b'\t', 1)
        mode, kind, sha = meta.decode().split()
        name = path.decode('utf-8'); pp = PurePosixPath(name)
        require(kind == 'blob' and mode in {'100644', '100755'}, 'Unsupported source object')
        require(not pp.is_absolute() and str(pp) == name and '..' not in pp.parts and '\\' not in name,
                'Unsafe source path')
        rows.append({'path': name, 'mode': mode, 'git_blob': sha})
    ids = list(dict.fromkeys(r['git_blob'] for r in rows))
    result = subprocess.run(['git', 'cat-file', '--batch'], cwd=ROOT,
        input=('\n'.join(ids) + '\n').encode(), capture_output=True, check=True).stdout
    bodies = {}; pos = 0
    for sha in ids:
        end = result.index(b'\n', pos); header = result[pos:end].decode().split()
        require(header[:2] == [sha, 'blob'], 'Unexpected Git batch object')
        size = int(header[2]); body = result[end+1:end+1+size]; pos = end+2+size
        require(len(body) == size and result[pos-1:pos] == b'\n', 'Truncated Git body')
        bodies[sha] = body
    files = {r['path']: bodies[r['git_blob']] for r in rows}
    for row in rows:
        row.update(size=len(files[row['path']]), sha256=digest(files[row['path']]))
    return raw, rows, files


def render(commit, qualification_bytes, mode='local-preflight', run_id=None):
    raw, rows, files = snapshot(commit)
    own = 'tools/releases/v0310/package/'
    policy = json.loads(files[own + 'policy.json'])
    selection = json.loads(files[policy['source_selection']])
    report = json.loads(qualification_bytes)
    require(mode in {'local-preflight', 'ci'}, 'Unknown package mode')
    require(report['status'] == 'PASS_N5A_CANDIDATE_NOT_PUBLISHED' and report['source_ref'] == commit,
            'Exact-source candidate qualification required')
    require(report['source_snapshot']['clean_exact_checkout'] is True, 'Qualification is not a clean exact checkout')
    require(report['selection_sha256'] == digest(files[policy['source_selection']]), 'Selection qualification differs')
    require(report['curation_contracts_passed'] == 20 and report['composition_contracts_passed'] >= 8,
            'Incomplete documentary/composition contracts')
    require(report['composition']['paired_bodies'] == 111 and report['composition']['retained_guides'] == 20,
            'Incomplete composed reader')
    require(report['composition']['published'] is False and report['composition']['live_channel_readback'] is False,
            'Qualification/published roles confused')
    for path, expected in report['inputs_sha256'].items():
        require(path in files and digest(files[path]) == expected, 'Qualification source drift: ' + path)
    for path, expected in selection['selected_files_sha256'].items():
        require(path in files and digest(files[path]) == expected, 'Selected source drift: ' + path)
    require(selection['summary']['active_components'] == 8 and selection['summary']['historical_components'] == 38,
            'Component-role denominator differs')
    require(mode != 'ci' or isinstance(run_id, int) and run_id > 0 and report['environment'] == 'CI'
            and report['ci_run_id'] == str(run_id), 'CI package/report run mismatch')
    epoch = int(next(x for x in raw.decode().splitlines() if x.startswith('committer ')).rsplit(' ', 2)[1])
    archive = io.BytesIO()
    with gzip.GzipFile(fileobj=archive, mode='wb', filename='', mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode='w', format=tarfile.PAX_FORMAT) as tar:
            for row in sorted(rows, key=lambda r: r['path']):
                body = files[row['path']]
                info = tarfile.TarInfo('riskium-v0.3.10/' + row['path'])
                info.size = len(body); info.mode = int(row['mode'][-3:], 8)
                info.uid = info.gid = 0; info.uname = info.gname = 'root'; info.mtime = epoch
                tar.addfile(info, io.BytesIO(body))
    manifest = {'schema': 'riskium-v0310-source-manifest/1', 'tag': 'v0.3.10', 'source_commit': commit,
                'source_tree': raw.decode().splitlines()[0].split()[1], 'commit_object_base64': base64.b64encode(raw).decode(),
                'commit_time': epoch, 'archive_prefix': 'riskium-v0.3.10', 'file_count': len(rows), 'files': rows,
                'selection_path': policy['source_selection'], 'selection_sha256': digest(files[policy['source_selection']])}
    versions = {'schema': 'riskium-v0310-artifact-versions/1', 'tag': 'v0.3.10', 'source_commit': commit,
                'source_version': '0.3.2', 'review_version': '0.2.0', 'reader_version': '0.4.10', 'manuscript_version': '7.2.21',
                'components': selection['artifacts'], 'dependencies': selection['dependencies'], 'dependency_order': selection['dependency_order'],
                'summary': selection['summary'], 'selection_sha256': manifest['selection_sha256'], 'article_binaries_included': False}
    notes = files[own + 'release-notes-template.md'].decode().replace('{{SOURCE_COMMIT}}', commit)
    assets = {'riskium-v0.3.10-source.tar.gz': archive.getvalue(), 'source-manifest.json': encoded(manifest),
              'artifact-versions.json': encoded(versions), 'release-notes.md': notes.encode()}
    receipt = {'schema': 'riskium-v0310-freeze-receipt/1', 'tag': 'v0.3.10', 'source_commit': commit,
               'source_tree': manifest['source_tree'], 'status': 'PREPARED_CI_NOT_PUBLISHED' if mode == 'ci' else 'LOCAL_PREFLIGHT_NOT_PUBLISHED',
               'build_mode': mode, 'workflow_run_id': run_id if mode == 'ci' else None,
               'qualification_report': report, 'qualification_report_sha256': digest(qualification_bytes),
               'bound_assets_sha256': {n: digest(b) for n, b in sorted(assets.items())},
               'scientific_source_sha256': digest(files[policy['model']]), 'manuscript_version': '7.2.21',
               'public_release_created': False, 'maintained_channels_read_back': False, 'issues_closed': [],
               'boundary': 'Documentary qualification and offline integrity; prior scientific engine evidence retains its original binding. Actual run/artifact provenance, release downloads and channel bodies require their own readbacks.'}
    assets['freeze-receipt.json'] = encoded(receipt)
    assets['SHA256SUMS.txt'] = ''.join(digest(assets[n]) + '  ' + n + '\n' for n in sorted(assets)).encode()
    require(set(assets) == set(policy['assets']), 'Six-asset inventory differs')
    return assets


def build(output, qualification, mode):
    require(not output.exists(), 'Use an empty package destination')
    require(not git('status', '--porcelain', '--untracked-files=no').strip(), 'Tracked checkout differs')
    commit = git('rev-parse', 'HEAD').decode().strip()
    run_id = None
    if mode == 'ci':
        require(os.environ.get('GITHUB_ACTIONS') == 'true' and os.environ.get('GITHUB_SHA') == commit, 'CI source mismatch')
        run_id = int(os.environ['GITHUB_RUN_ID'])
    assets = render(commit, qualification.read_bytes(), mode, run_id)
    output.mkdir(parents=True)
    for name, body in assets.items():
        (output / name).write_bytes(body)
    return {'status': 'PASS_PACKAGE_PREPARED_NOT_PUBLISHED', 'source_commit': commit, 'mode': mode,
            'assets': {n: {'bytes': len(b), 'sha256': digest(b)} for n, b in assets.items()}}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--qualification', required=True, type=Path)
    p.add_argument('--mode', choices=['local-preflight', 'ci'], default='local-preflight')
    a = p.parse_args()
    print(json.dumps(build(a.output.resolve(), a.qualification.resolve(), a.mode), indent=2))

