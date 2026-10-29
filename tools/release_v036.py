"""Select and freeze the v0.3.6 source package; verify all six assets without Git.

Freeze requires a clean current main, authenticated exact-source CI artifacts and
the affected runtime checks. Offline verification proves internal agreement; the
downloaded ZIP digest or another trusted external digest supplies authenticity.
This tool never creates a tag, release or public asset.
"""
import argparse
import copy
from datetime import datetime, timezone
import gzip
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tarfile
import tempfile
from urllib.parse import urlsplit
from urllib.error import HTTPError
from urllib.request import Request, build_opener, HTTPRedirectHandler
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TAG = 'v0.3.6'
REPO = 'ArazSaieArasi3/riskium'
MATRIX = 'releases/selection-v0.3.6.json'
PRIOR = 'releases/selection-v0.3.5.json'
PRIOR_SHA256 = '99405668004b7b11e9b59dec0df93a94f890b4abb7ba22d5ac4b8914e8bcec32'
R4 = 'evaluation/releases/v0.3.6'
BASE = 'd2ed1b1fbbadbbafaba847b4bfe724f1a2c256eb'
SCIENCE = dict(model='0.3.1', orsd='0.4.3', original_drsd='0.1.0', manuscript='7.0.8')
ARCHIVE = 'riskium-v0.3.6-source.tar.gz'
ASSETS = {ARCHIVE, 'source-manifest.json', 'artifact-versions.json', 'freeze-receipt.json',
          'release-notes.md', 'SHA256SUMS.txt'}
SUPPORT = ('tools/release_v036.py', 'tests/test_release_v036.py',
           '.github/workflows/release-v036.yml', 'tools/run_v036_versioned_suite.py',
           '.github/workflows/v036-versioned-suite.yml', 'docs/release-v0.3.6.md')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()


def safe_path(value):
    require(isinstance(value, str) and value and '\\' not in value and '\x00' not in value, 'Unsafe path')
    path = PurePosixPath(value)
    require(path.parts and not path.is_absolute() and str(path) == value
            and all(p not in ('.', '..', '.git') for p in path.parts), 'Unsafe path: ' + value)
    return value


def read(path, root=ROOT):
    path = safe_path(path)
    target = root / path
    require(target.resolve().is_relative_to(root.resolve()) and not target.is_symlink(), 'Unsafe source: ' + path)
    return target.read_bytes()


def load(path, root=ROOT):
    return json.loads(read(path, root))


def checked(bindings, root=ROOT):
    for path, digest in bindings.items():
        require(sha(read(path, root)) == digest, 'Source binding changed: ' + path)


def selection(root=ROOT):
    require(sha(read(PRIOR, root)) == PRIOR_SHA256, 'Predecessor selection identity changed')
    previous = load(PRIOR, root)
    require(previous['target'] == 'v0.3.5' and len(previous['artifacts']) == 29, 'Wrong predecessor matrix')
    require(previous['scientific_versions'] == SCIENCE, 'Scientific versions changed')
    require(len(previous['selected_files_sha256']) == 687, 'Wrong predecessor file population')
    checked(previous['selected_files_sha256'], root)
    artifacts = copy.deepcopy(previous['artifacts'])
    by_id = {row['id']: row for row in artifacts}
    for ident, descriptor in (('CONSISTENCY', 'evaluation/consistency/current-0.4.0/component.json'),
                              ('ASSESSMENT_SELECTION', 'implementation/relational/0.8.0/component.json')):
        desc = load(descriptor, root)
        require(desc['id'] == ident and desc['compatible_model'] == '0.3.1', 'Wrong successor descriptor')
        checked(desc['files_sha256'], root)
        files = {row['path']: row['sha256'] for row in by_id.get(ident, {}).get('files', [])}
        files.update(desc['files_sha256']); files[descriptor] = sha(read(descriptor, root))
        row = dict(id=ident, artifact='Assessment selection' if ident == 'ASSESSMENT_SELECTION' else 'Current traceability',
                   version=desc['version'], compatible_model='0.3.1', status='SELECTED_EXECUTED_COMPONENT',
                   files=[dict(path=p, sha256=h) for p, h in sorted(files.items())],
                   scope='Bounded SQL/application engineering; original checkpoints and scientific populations retained.')
        if ident in by_id:
            artifacts[artifacts.index(by_id[ident])] = row
        else:
            artifacts.append(row)
        by_id[ident] = row
    doc = by_id['DOCUMENTATION']
    files = {r['path']: r['sha256'] for r in doc['files']}
    for ns in ('documentation/0.4.1', 'documentation/0.4.2'):
        for path in (root / ns).rglob('*'):
            if path.is_file():
                name = str(path.relative_to(root)); files[name] = sha(read(name, root))
    for name in ('.github/README.md', 'tools/publication/assessment_documentation.py',
                 'tools/publication/review_assessment_reader.py', 'tools/publication/assessment_main_gate.py',
                 '.github/workflows/assessment-reader-main.yml', 'tests/test_assessment_documentation.py',
                 'tests/test_assessment_main_gate.py', R4 + '/r4-channels.json', R4 + '/r4-reader-review.json',
                 R4 + '/r4-provenance.json'):
        files[name] = sha(read(name, root))
    doc.update(version='0.4.2', status='SELECTED_R4_REVIEWED_CHECKPOINT',
               files=[dict(path=p, sha256=h) for p, h in sorted(files.items())],
               scope='R4 maintained reader checkpoint; its dated prepublication labels remain historical after v0.3.6 publication.')
    provenance = load(R4 + '/r4-provenance.json', root)
    checked(provenance['files_sha256'], root)
    channels = load(R4 + '/r4-channels.json', root)['actual_channels']
    qualitative = load(R4 + '/r4-reader-review.json', root)
    require(channels['status'] == 'ACTUAL_PUBLISHED_READER_CHANNELS_PASS'
            and channels['documentation_source_commit'] == qualitative['source_commit'] == BASE
            and channels['wiki_files'] == 23 and channels['pages_http_responses'] == 314
            and channels['frozen_snapshots'] == 4, 'Wrong R4 channel checkpoint')
    require([r['id'] for r in qualitative['criteria']] == ['ASL-Q%02d' % n for n in range(1, 7)]
            and all(r['status'] == 'PASS' and r['observed'] for r in qualitative['criteria']), 'Incomplete R4 reader review')
    deps = copy.deepcopy(previous['dependencies'])
    for edges in deps.values():
        for edge in edges:
            if edge['id'] in ('CONSISTENCY', 'DOCUMENTATION'):
                edge['version'] = by_id[edge['id']]['version']
    deps['ASSESSMENT_SELECTION'] = [dict(id=ident, version=by_id[ident]['version']) for ident in
        ('MODEL', 'ORSD', 'DATABASE_REQUIREMENTS', 'ASSESSMENT_CORRECTION', 'EVIDENCE_REFERENCE_LIFECYCLE')]
    deps['CONSISTENCY'].append(dict(id='ASSESSMENT_SELECTION', version='0.8.0'))
    require(len(by_id) == len(artifacts) == len(deps) == 30, 'Component closure differs')
    for ident, edges in deps.items():
        for edge in edges:
            require(edge['id'] in by_id and edge['version'] == by_id[edge['id']]['version'], 'Unresolved dependency: ' + ident)
    def visit(ident, path=()):
        require(ident not in path, 'Component dependency cycle')
        for edge in deps[ident]:
            visit(edge['id'], path + (ident,))
    for ident in deps:
        visit(ident)
    # The predecessor also selects delivery/generation inputs outside domain rows.
    all_files = dict(previous['selected_files_sha256'])
    for row in artifacts:
        for f in row['files']:
            require(f['path'] not in all_files or all_files[f['path']] == f['sha256'], 'Conflicting file ownership')
            all_files[f['path']] = f['sha256']
    checked(all_files, root)
    return dict(schema='riskium-v036-source-selection-v1', target=TAG, stage='SELECTED_NOT_FROZEN', issue=61,
                predecessor='v0.3.5', predecessor_selection_sha256=sha(read(PRIOR, root)), r4_source=BASE,
                scientific_versions=SCIENCE, artifacts=artifacts, dependencies=deps,
                selected_files_sha256=dict(sorted(all_files.items())),
                delivery_support_sha256={p: sha(read(p, root)) for p in SUPPORT},
                summary=dict(components=30, retained=27, replaced=2, added=1, selected_files=len(all_files),
                             dependency_edges=sum(map(len, deps.values()))),
                changes=dict(ASSESSMENT_SELECTION='0.8.0 / schema 9', CONSISTENCY='0.4.0 / 460 routes', DOCUMENTATION='0.4.2'),
                historical_checkpoint_states_preserved=True, independent_semantic_validation=False,
                original_requirement_fulfillment=False, organizational_admissions='11 WITHHELD',
                limits='Synthetic engineering and agent reader review; no production, article acceptance or full semantic correctness claim.')


def git(*args, root=ROOT):
    return subprocess.check_output(['git', *args], cwd=root)


class CleanRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        redirected = super().redirect_request(req, fp, code, msg, headers, newurl)
        if redirected and urlsplit(newurl).netloc != urlsplit(req.full_url).netloc:
            redirected.remove_header('Authorization')
        return redirected


def api(path, binary=False):
    require(path and not path.startswith('/') and '..' not in path, 'Unsafe API path')
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'riskium-v036-freeze'}
    if os.environ.get('GH_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
    request = Request('https://api.github.com/repos/' + REPO + '/' + path, headers=headers)
    with build_opener(CleanRedirect()).open(request, timeout=60) as response:
        data = response.read()
    return data if binary else json.loads(data)


def ci_receipt(run_id, source, workflow, artifact_prefix, filename):
    run = api('actions/runs/' + str(run_id))
    require(run['status'] == 'completed' and run['conclusion'] == 'success'
            and run['head_sha'] == source and run['head_branch'] == 'main'
            and run['path'] == '.github/workflows/' + workflow
            and run['repository']['full_name'] == run['head_repository']['full_name'] == REPO,
            'Untrusted CI run')
    records = api('actions/runs/' + str(run_id) + '/artifacts?per_page=100')['artifacts']
    found = [a for a in records if a['name'] == artifact_prefix + source and not a['expired']]
    require(len(found) == 1 and found[0]['workflow_run']['head_sha'] == source, 'Missing exact CI artifact')
    artifact = found[0]
    data = api('actions/artifacts/' + str(artifact['id']) + '/zip', binary=True)
    require('sha256:' + sha(data) == artifact['digest'], 'CI artifact ZIP digest mismatch')
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        require(z.namelist() == [filename], 'Unexpected CI artifact members')
        receipt = json.loads(z.read(filename))
    return receipt, dict(run_id=run_id, artifact_id=artifact['id'], artifact_sha256=sha(data), workflow=workflow)


def prior_inventory():
    wanted = set(load(PRIOR)['preserve_releases']) | {'v0.3.5'}
    releases = api('releases?per_page=100')
    require({r['tag_name'] for r in releases} == wanted and len(wanted) == len(releases) == 12,
            'Previous release inventory changed')
    rows = []
    for release in sorted(releases, key=lambda r:r['tag_name']):
        target = api('git/ref/tags/' + release['tag_name'])['object']
        rows.append(dict(tag=release['tag_name'], release_id=release['id'],
                         draft=release['draft'], prerelease=release['prerelease'],
                         published_at=release['published_at'], body_sha256=sha((release['body'] or '').encode()),
                         tag_object=target, assets=[dict(id=a['id'], name=a['name'], bytes=a['size'], digest=a['digest'])
                                                    for a in release['assets']]))
    return rows


def source_entries(source):
    rows = []
    for line in git('ls-tree', '-r', '-z', source).split(b'\0'):
        if not line:
            continue
        header, path = line.split(b'\t', 1)
        mode, kind, ident = header.split(); path = safe_path(path.decode())
        require(kind == b'blob' and mode in (b'100644', b'100755'), 'Nonregular committed source: ' + path)
        rows.append((path, int(mode, 8) & 0o777, git('cat-file', 'blob', ident.decode())))
    require(rows, 'Empty source tree')
    return rows


def build_assets(folder, source, entries, matrix, evidence, timestamp):
    folder.mkdir(parents=True, exist_ok=True)
    require(not list(folder.iterdir()), 'Asset folder must be empty')
    require(re.fullmatch('[a-f0-9]{40}', source) is not None, 'Invalid source identity')
    manifest = dict(schema='riskium-v036-source-manifest-v1', tag=TAG, source_commit=source,
                    prefix=TAG + '/', files={p: dict(sha256=sha(data), bytes=len(data), mode=mode)
                                            for p, mode, data in entries})
    require(len(manifest['files']) == len(entries), 'Duplicate source entry')
    with (folder / ARCHIVE).open('wb') as raw, gzip.GzipFile(fileobj=raw, mode='wb', mtime=timestamp, filename='') as zipped:
        with tarfile.open(fileobj=zipped, mode='w') as tar:
            for path, mode, data in entries:
                info = tarfile.TarInfo(TAG + '/' + safe_path(path)); info.size=len(data); info.mode=mode; info.mtime=timestamp
                tar.addfile(info, io.BytesIO(data))
    (folder / 'source-manifest.json').write_bytes(encoded(manifest))
    (folder / 'artifact-versions.json').write_bytes(encoded(dict(tag=TAG, source_commit=source, selection=matrix)))
    notes = next(data for path, mode, data in entries if path == 'docs/release-v0.3.6.md')
    (folder / 'release-notes.md').write_bytes(notes)
    receipt = dict(schema='riskium-v036-freeze-receipt-v1', tag=TAG, source_commit=source,
                   stage='FROZEN_NOT_PUBLISHED', publication_executed=False,
                   created_at_utc=datetime.now(timezone.utc).isoformat(), files=len(entries),
                   scientific_versions=SCIENCE, evidence=evidence,
                   payload_sha256={n: sha((folder/n).read_bytes()) for n in
                                   (ARCHIVE, 'source-manifest.json', 'artifact-versions.json', 'release-notes.md')},
                   independent_semantic_validation=False)
    (folder / 'freeze-receipt.json').write_bytes(encoded(receipt))
    (folder / 'SHA256SUMS.txt').write_text(''.join(sha((folder/n).read_bytes()) + '  ' + n + '\n'
                                              for n in sorted(ASSETS - {'SHA256SUMS.txt'})))
    return receipt


def verify_package(folder, expected_source=None):
    folder = Path(folder)
    require({p.name for p in folder.iterdir()} == ASSETS
            and all(p.is_file() and not p.is_symlink() for p in folder.iterdir()), 'Six regular assets required')
    lines = (folder/'SHA256SUMS.txt').read_text().splitlines()
    sums = {}
    for line in lines:
        require(re.fullmatch(r'[a-f0-9]{64}  [A-Za-z0-9.\-]+', line), 'Malformed checksum line')
        digest, name = line.split('  ')
        require(name not in sums and name in ASSETS - {'SHA256SUMS.txt'}, 'Duplicate or unknown checksum')
        sums[name] = digest
    require(set(sums) == ASSETS - {'SHA256SUMS.txt'}, 'Incomplete checksums')
    for name, digest in sums.items():
        require(sha((folder/name).read_bytes()) == digest, 'Asset checksum mismatch: ' + name)
    manifest = json.loads((folder/'source-manifest.json').read_bytes())
    versions = json.loads((folder/'artifact-versions.json').read_bytes())
    receipt = json.loads((folder/'freeze-receipt.json').read_bytes())
    source = manifest['source_commit']
    require(re.fullmatch('[a-f0-9]{40}', source) and manifest['tag'] == versions['tag'] == receipt['tag'] == TAG
            and versions['source_commit'] == receipt['source_commit'] == source
            and (expected_source is None or source == expected_source), 'Version/source identity mismatch')
    require(receipt['scientific_versions'] == SCIENCE and receipt['stage'] == 'FROZEN_NOT_PUBLISHED'
            and not receipt['publication_executed'] and not receipt['independent_semantic_validation'], 'Freeze boundary changed')
    payloads = {}
    require(manifest['prefix'] == TAG + '/', 'Wrong archive prefix')
    with tarfile.open(folder/ARCHIVE, 'r:gz') as tar:
        for item in tar:
            require(item.isfile() and item.name.startswith(TAG + '/'), 'Unsafe archive member')
            path = safe_path(item.name[len(TAG) + 1:])
            require(path not in payloads, 'Duplicate archive member')
            require(item.mode in (0o644, 0o755) and item.uid == item.gid == 0, 'Unexpected archive mode/owner')
            data = tar.extractfile(item).read(); payloads[path] = data
            require(manifest['files'].get(path) == dict(sha256=sha(data), bytes=len(data), mode=item.mode), 'Source manifest mismatch: ' + path)
    require(set(payloads) == set(manifest['files']) and len(payloads) == receipt['files'], 'Incomplete source archive')
    selected = json.loads(payloads[MATRIX])
    require(versions['selection'] == selected and selected['target'] == TAG
            and selected['scientific_versions'] == SCIENCE and selected['summary']['components'] == 30,
            'Archived component selection mismatch')
    for path, digest in {**selected['selected_files_sha256'], **selected['delivery_support_sha256']}.items():
        require(path in payloads and sha(payloads[path]) == digest, 'Archived selected binding mismatch: ' + path)
    prior = json.loads(payloads[PRIOR])
    require(sha(payloads[PRIOR]) == selected['predecessor_selection_sha256'] == PRIOR_SHA256
            and len(prior['selected_files_sha256']) == 687, 'Predecessor selection changed')
    for path, digest in prior['selected_files_sha256'].items():
        require(path in payloads and sha(payloads[path]) == digest, 'Preserved predecessor file changed: ' + path)
    require((folder/'release-notes.md').read_bytes() == payloads['docs/release-v0.3.6.md'], 'Notes differ from committed source')
    require(receipt['payload_sha256'] == {n: sha((folder/n).read_bytes()) for n in
            (ARCHIVE, 'source-manifest.json', 'artifact-versions.json', 'release-notes.md')}, 'Receipt payload binding mismatch')
    evidence = receipt['evidence']
    require(evidence['suite']['status'] == 'VERSIONED_SUITE_PASS'
            and evidence['suite']['source_commit'] == source and evidence['suite']['candidate_tests'] >= 524
            and evidence['suite']['published_reader_tests'] == 10
            and evidence['runtime']['summary'] == {'PASS': 44, 'FAIL': 0, 'ERROR': 0}
            and evidence['channels']['actual_channels']['documentation_source_commit'] == source
            and evidence['channels']['actual_channels']['status'] == 'ACTUAL_PUBLISHED_READER_CHANNELS_PASS',
            'Missing executed final-source evidence')
    return dict(status='V036_SIX_ASSET_OFFLINE_PASS', tag=TAG, source_commit=source,
                source_files=len(payloads), selected_components=30, preserved_previous_files=687,
                external_authenticity_required=True, publication_executed=False)


def freeze(folder, source, reader_run):
    require(git('rev-parse', 'HEAD').decode().strip() == source and not git('status', '--porcelain').strip(), 'Clean exact source required')
    require(git('merge-base', BASE, 'HEAD').decode().strip() == BASE, 'Not descended from reviewed R4')
    require(api('git/ref/heads/main')['object']['sha'] == source, 'Source no longer main')
    require(api('releases/latest')['tag_name'] == 'v0.3.5', 'Predecessor is no longer Latest')
    for endpoint in ('git/ref/tags/' + TAG, 'releases/tags/' + TAG):
        try:
            api(endpoint)
        except HTTPError as exc:
            if exc.code != 404:
                raise
        else:
            raise ValueError('Target tag/release already exists')
    previous_releases = prior_inventory()
    matrix = selection()
    require(read(MATRIX) == encoded(matrix), 'Stale v0.3.6 selection')
    channels, reader_provenance = ci_receipt(reader_run, source, 'assessment-reader-main.yml',
                                           'assessment-actual-channels-', 'actual-reader-channels.json')
    runs = api('actions/runs?head_sha=' + source + '&per_page=100')['workflow_runs']
    suites = [r for r in runs if r['path'] == '.github/workflows/v036-versioned-suite.yml'
              and r['event'] == 'push' and r['head_branch'] == 'main' and r['conclusion'] == 'success']
    require(suites, 'No successful current-main source suite')
    suite, suite_provenance = ci_receipt(max(suites, key=lambda r:r['id'])['id'], source, 'v036-versioned-suite.yml',
                                       'v036-source-suite-', 'versioned-suite.json')
    checks = []
    for args in (['tools/run_assessment_selection.py', '--output', 'build/v036-runtime.json'],
                 ['tools/audit_assessment_alignment.py', '--check'],
                 ['tools/publication/review_assessment_reader.py'], ['tools/audit_consistency.py', '--check']):
        run = subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True)
        require(run.returncode == 0, 'Final-source check failed: ' + ' '.join(args) + '\n' + run.stderr.decode())
        checks.append(dict(args=args, exit_code=0, stdout_sha256=sha(run.stdout)))
    runtime = load('build/v036-runtime.json')
    require(not git('status', '--porcelain').strip(), 'Checks modified source')
    require(api('git/ref/heads/main')['object']['sha'] == source, 'Main advanced during checks')
    timestamp = int(git('show', '-s', '--format=%ct', source))
    evidence = dict(suite=suite, suite_provenance=suite_provenance, channels=channels,
                    previous_releases=previous_releases,
                    reader_provenance=reader_provenance, runtime=runtime, checks=checks)
    build_assets(folder, source, source_entries(source), matrix, evidence, timestamp)
    result = verify_package(folder, source)
    with tempfile.TemporaryDirectory() as tmp:
        temp = Path(tmp)
        with tarfile.open(folder/ARCHIVE, 'r:gz') as tar:
            tar.extractall(temp, filter='data')
        env = dict(os.environ, PATH='/nonexistent')
        command = [sys.executable, str(temp/TAG/'tools/release_v036.py'), 'verify', '--folder', str(folder.resolve()), '--source', source]
        run = subprocess.run(command, env=env, capture_output=True)
        require(run.returncode == 0, 'Extracted no-Git validation failed: ' + run.stderr.decode())
    result['extracted_no_git_validator_passed'] = True
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('select', 'freeze', 'verify'))
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--folder', type=Path)
    parser.add_argument('--source')
    parser.add_argument('--reader-run', type=int)
    args = parser.parse_args()
    if args.mode == 'select':
        data = encoded(selection())
        if args.check:
            require(read(MATRIX) == data, 'Stale v0.3.6 selection')
        else:
            (ROOT/MATRIX).write_bytes(data)
        print(json.dumps({'status':'V036_COMPONENT_SELECTION_PASS', **json.loads(data)['summary']}))
    elif args.mode == 'verify':
        require(args.folder is not None, '--folder required')
        print(json.dumps(verify_package(args.folder, args.source)))
    else:
        require(args.folder is not None and args.source and args.reader_run, 'Freeze requires folder, source and reader run')
        print(json.dumps(freeze(args.folder, args.source, args.reader_run)))


if __name__ == '__main__':
    main()
