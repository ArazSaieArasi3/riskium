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
    def read(path): return json.loads(files[path])
    own = 'tools/releases/v039/package/'
    require(own + 'build_package.py' in files, 'Packaging recipe is not in source commit')
    policy = read(own + 'policy.json'); selection = read(policy['source_selection'])
    contract = read(policy['contract']); model = read(policy['model'])
    report = json.loads(qualification_bytes)
    require(mode in {'local-preflight', 'ci'}, 'Unknown package build mode')
    require(report['status'] == policy['qualification_status'], 'Source qualification failed')
    require(report['execution_commit'] == commit, 'Qualification belongs to another commit')
    require(report['source_version'] == model['version'] == policy['source_version'], 'Wrong scientific version')
    require(report['source_sha256'] == digest(files[policy['model']]), 'Wrong model qualification hash')
    require(report['source_contract_sha256'] == digest(files[policy['contract']]), 'Wrong contract qualification hash')
    require(report['selection']['sha256'] == digest(files[policy['source_selection']]), 'Wrong selection qualification hash')
    summary = report['fresh_oracle_summary']
    require(summary['planned_cases'] == summary['cases_executed'] == summary['cases_matched'] == 20,
            'Incomplete exact-source oracle suite')
    require(report['published'] is False and report['maintained_channels_read_back'] is False,
            'Qualification/published roles are confused')
    for path, sha in selection['selected_files_sha256'].items():
        require(path in files and digest(files[path]) == sha, 'Selected source body differs: ' + path)
    require(selection['summary']['active_components'] == policy['active_components'] and
            selection['summary']['historical_components'] == policy['historical_components'], 'Wrong component roles')
    require(contract['source']['sha256'] == digest(files[policy['model']]), 'Contract/source disagreement')
    require(mode != 'ci' or isinstance(run_id, int) and run_id > 0, 'CI package needs a run binding')
    epoch = int(next(x for x in raw.decode().splitlines() if x.startswith('committer ')).rsplit(' ', 2)[1])
    archive = io.BytesIO()
    with gzip.GzipFile(fileobj=archive, mode='wb', filename='', mtime=0) as compressed:
        with tarfile.open(fileobj=compressed, mode='w', format=tarfile.PAX_FORMAT) as tar:
            for row in sorted(rows, key=lambda r: r['path']):
                body = files[row['path']]; info = tarfile.TarInfo(policy['archive_prefix'] + '/' + row['path'])
                info.size = len(body); info.mode = int(row['mode'][-3:], 8)
                info.uid = info.gid = 0; info.uname = info.gname = 'root'; info.mtime = epoch
                tar.addfile(info, io.BytesIO(body))
    manifest = {'schema': 'riskium-v039-source-manifest-1', 'tag': policy['tag'],
        'source_commit': commit, 'source_tree': raw.decode().splitlines()[0].split()[1],
        'commit_object_base64': base64.b64encode(raw).decode(), 'commit_time': epoch,
        'archive_prefix': policy['archive_prefix'], 'file_count': len(rows), 'files': rows,
        'selection_path': policy['source_selection'], 'selection_sha256': digest(files[policy['source_selection']])}
    versions = {'schema': 'riskium-v039-artifact-versions-1', 'tag': policy['tag'],
        'source_commit': commit, 'source_version': policy['source_version'],
        'reader_version': policy['reader_version'], 'manuscript_version': policy['manuscript_version'],
        'selection_sha256': manifest['selection_sha256'], 'components': selection['artifacts'],
        'dependencies': selection['dependencies'], 'dependency_order': selection['dependency_order'],
        'summary': selection['summary'], 'article_binaries_included': False}
    notes = files[own + 'release-notes-template.md'].decode()
    substitutions = {'SOURCE_COMMIT': commit, 'ACTIVE_COMPONENTS': str(policy['active_components']),
        'HISTORICAL_COMPONENTS': str(policy['historical_components']),
        'SELECTED_FILES': str(selection['summary']['selected_files'])}
    for key, value in substitutions.items(): notes = notes.replace('{{' + key + '}}', value)
    assets = {'riskium-v0.3.9-source.tar.gz': archive.getvalue(),
        'source-manifest.json': encoded(manifest), 'artifact-versions.json': encoded(versions),
        'release-notes.md': notes.encode()}
    receipt = {'schema': 'riskium-v039-freeze-receipt-1',
        'status': 'PREPARED_CI_NOT_PUBLISHED' if mode == 'ci' else 'LOCAL_PREFLIGHT_NOT_PUBLISHED',
        'tag': policy['tag'], 'source_commit': commit, 'source_tree': manifest['source_tree'],
        'build_mode': mode, 'workflow_run_id': run_id if mode == 'ci' else None,
        'qualification_report': report, 'qualification_report_sha256': digest(qualification_bytes),
        'bound_assets_sha256': {n: digest(b) for n, b in sorted(assets.items())},
        'scientific_source_sha256': digest(files[policy['model']]),
        'manuscript_version': policy['manuscript_version'], 'public_release_created': False,
        'maintained_channels_read_back': False, 'issues_closed': [],
        'provenance_boundary': 'CI mode consumes the successful prerequisite job artifact in the same workflow. Offline verification checks source/evidence bindings; live GitHub run/artifact provenance is verified separately after download. Local preflight is never called CI evidence.'}
    assets['freeze-receipt.json'] = encoded(receipt)
    assets['SHA256SUMS.txt'] = ''.join(digest(assets[n]) + '  ' + n + '\n' for n in sorted(assets)).encode()
    require(set(assets) == set(policy['assets']), 'Six-asset inventory mismatch')
    return assets

def build(output, qualification, mode):
    require(not output.exists() or not any(output.iterdir()), 'Output directory must be empty')
    require(not git('status', '--porcelain', '--untracked-files=no').strip(), 'Tracked worktree differs from HEAD')
    commit = git('rev-parse', 'HEAD').decode().strip()
    run_id = None
    if mode == 'ci':
        require(os.environ.get('GITHUB_ACTIONS') == 'true' and os.environ.get('GITHUB_SHA') == commit,
                'CI/source environment mismatch')
        run_id = int(os.environ['GITHUB_RUN_ID'])
    assets = render(commit, qualification.read_bytes(), mode, run_id)
    output.mkdir(parents=True, exist_ok=True)
    for name, body in assets.items(): (output / name).write_bytes(body)
    return {'status': 'PACKAGE_PREPARED_NOT_PUBLISHED', 'source_commit': commit,
        'build_mode': mode, 'assets': {name: {'bytes': len(body), 'sha256': digest(body)} for name, body in assets.items()}}

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--qualification', type=Path, required=True)
    ap.add_argument('--mode', choices=['local-preflight', 'ci'], default='local-preflight')
    a = ap.parse_args(); print(json.dumps(build(a.output.resolve(), a.qualification.resolve(), a.mode), indent=2))
