"""One-shot v0.3.5 publication from authenticated exact-source staged assets."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tarfile
import tempfile
import zipfile

sys.dont_write_bytecode = True
import release_v035_final as release

REPO = 'ArazSaieArasi3/riskium'
ROOT = Path(__file__).resolve().parents[1]
TAG = release.TAG
WORKFLOW = '.github/workflows/final-release-v035.yml'
WORKFLOW_NAME = 'v0.3.5 verified source publication'
BASELINE = 'evaluation/releases/v0.3.5-definition/published-baseline.json'
REQUEST = release.PUBLICATION_REQUEST
PROFILE = release.PUBLICATION_PROFILE
LEGACY = ('.github/workflows/pages.yml', '.github/workflows/publication-status.yml',
          '.github/workflows/current-documentation-pages.yml')
require = release.require
sha = release.sha


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def gh(*args):
    return subprocess.check_output(['gh', *args], text=True)


def api(path, missing_ok=False, method='GET'):
    run = subprocess.run(['gh', 'api', '--method', method, 'repos/' + REPO + '/' + path],
                         capture_output=True, text=True)
    if run.returncode:
        if missing_ok and re.search(r'\(HTTP 404\)', run.stderr):
            return None
        raise ValueError('V035-PUBLISH-API-FAILED: ' + path)
    return release.loads(run.stdout) if run.stdout.strip() else None


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()


def resolve_intent(root, source, getter=None):
    """A retained request has no authority over any later source commit."""
    root = Path(root)
    getter = getter or api
    require(re.fullmatch('[a-f0-9]{40}', source or ''), 'V035-PUBLISH-SOURCE')
    require(git(root, 'rev-parse', 'HEAD') == source, 'V035-PUBLISH-NOT-HEAD')
    changed = git(root, 'log', '-1', '--format=%H', source, '--', REQUEST)
    if changed != source:
        return dict(publish=False, source_commit=source, reason='Request unchanged in this commit')
    release.validate_profile(root)
    config, request = release.validate_publication_config(release.reader(root))
    parents = git(root, 'show', '-s', '--format=%P', source).split()
    require(parents == [request['expected_parent']], 'V035-PUBLISH-UNREVIEWED-PARENT')
    allowed = set(release.TOOLING) | {
        release.MATRIX, release.PROFILE, release.SCREEN, release.REGISTRY,
        release.REQUEST, release.NOTES, 'evaluation/consistency/inventory.json'}
    delta = set(git(root, 'diff', '--name-only', parents[0], source).splitlines())
    require(REQUEST in delta and delta <= allowed, 'V035-PUBLISH-UNREVIEWED-DELTA')
    require(getter('git/ref/heads/main')['object']['sha'] == source, 'V035-PUBLISH-MAIN-ADVANCED')
    return dict(publish=True, source_commit=source, activation_id=request['activation_id'],
                expected_parent=parents[0])


def workflow_origin(run, source):
    require(run['path'] == WORKFLOW and run['name'] == WORKFLOW_NAME
            and run['head_sha'] == source and run['head_branch'] == 'main'
            and run['repository']['full_name'] == REPO
            and run['head_repository']['full_name'] == REPO
            and run['event'] == 'workflow_run'
            and (run['status'] == 'in_progress'
                 or (run['status'] == 'completed' and run['conclusion'] == 'success')),
            'V035-PUBLISH-UNTRUSTED-RUN')


def require_jobs(jobs, required):
    for name in required:
        matches = [j for j in jobs if j['name'] == name]
        require(len(matches) == 1 and matches[0]['status'] == 'completed'
                and matches[0]['conclusion'] == 'success', 'V035-PUBLISH-MISSING-JOB: ' + name)


def authenticated_artifact(run_id, source, artifact_id=None, digest=None, required=('freeze',),
                           getter=None):
    getter = getter or api
    require(type(run_id) is int and run_id > 0, 'V035-PUBLISH-RUN-ID')
    require(getter('git/ref/heads/main')['object']['sha'] == source, 'V035-PUBLISH-MAIN-ADVANCED')
    run = getter('actions/runs/' + str(run_id))
    workflow_origin(run, source)
    require_jobs(getter('actions/runs/' + str(run_id) + '/jobs?per_page=100')['jobs'], required)
    rows = getter('actions/runs/' + str(run_id) + '/artifacts?per_page=100')['artifacts']
    matches = [a for a in rows if a['name'] == 'riskium-v0.3.5-freeze-' + source]
    require(len(matches) == 1, 'V035-PUBLISH-ARTIFACT-AMBIGUOUS')
    item = matches[0]
    require(item['expired'] is False and item['workflow_run']['id'] == run_id
            and item['workflow_run']['head_sha'] == source
            and item['workflow_run']['head_branch'] == 'main'
            and isinstance(item['digest'], str)
            and re.fullmatch('sha256:[a-f0-9]{64}', item['digest']), 'V035-PUBLISH-ARTIFACT-ORIGIN')
    if artifact_id is not None:
        require(item['id'] == artifact_id and item['digest'] == 'sha256:' + digest,
                'V035-PUBLISH-ARTIFACT-REBOUND')
    return item


def download_zip(item, destination):
    with Path(destination).open('wb') as stream:
        subprocess.run(['gh', 'api', 'repos/' + REPO + '/actions/artifacts/' +
                        str(item['id']) + '/zip'], stdout=stream, check=True)
    raw = Path(destination).read_bytes()
    require(len(raw) == item['size_in_bytes'] and sha(raw) == item['digest'].removeprefix('sha256:'),
            'V035-PUBLISH-ORIGINAL-ZIP-DIGEST')


def unpack_assets(archive_path, folder):
    folder = Path(folder)
    folder.mkdir()
    with zipfile.ZipFile(archive_path) as archive:
        items = archive.infolist()
        require(len(items) == 6 and {i.filename for i in items} == release.ASSETS,
                'V035-PUBLISH-ZIP-SIX-ASSETS')
        require(all(not i.is_dir() and not stat.S_ISLNK(i.external_attr >> 16) for i in items),
                'V035-PUBLISH-ZIP-NONREGULAR')
        for item in items:
            (folder / item.filename).write_bytes(archive.read(item))


def verify_git_archive(root, folder, source):
    records = subprocess.check_output(['git', '-C', str(root), 'ls-tree', '-r', '-z', source])
    expected = {}
    for record in records.split(b'\0'):
        if record:
            header, path = record.split(b'\t', 1)
            mode, kind, ident = header.split()
            require(kind == b'blob' and mode in (b'100644', b'100755'), 'V035-PUBLISH-GIT-MODE')
            expected[path.decode()] = (int(mode, 8) & 0o777, ident.decode())
    seen = set()
    with tarfile.open(Path(folder) / 'riskium-v0.3.5-source.tar.gz', 'r:gz') as archive:
        for member in archive:
            prefix = 'riskium-v0.3.5/'
            require(member.isfile() and member.name.startswith(prefix), 'V035-PUBLISH-TAR-MEMBER')
            path = release.safe_path(member.name[len(prefix):])
            require(path in expected and path not in seen, 'V035-PUBLISH-TAR-INVENTORY')
            seen.add(path)
            data = archive.extractfile(member).read()
            mode, ident = expected[path]
            actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            require(actual == ident and member.mode == mode, 'V035-PUBLISH-GIT-BLOB: ' + path)
    require(seen == set(expected), 'V035-PUBLISH-GIT-INCOMPLETE')


def tag_commit(tag, getter=None):
    getter = getter or api
    target = getter('git/ref/tags/' + tag)['object']
    for _ in range(10):
        if target['type'] != 'tag':
            break
        target = getter('git/tags/' + target['sha'])['object']
    require(target['type'] == 'commit', 'V035-PUBLISH-TAG-NONCOMMIT')
    return target['sha']


def normalized_release(value):
    return dict(tag=value['tag_name'], release_id=value['id'], name=value['name'],
                draft=value['draft'], prerelease=value['prerelease'], published_at=value['published_at'],
                url=value['html_url'], assets=sorted([
                    dict(id=a['id'], name=a['name'], size=a['size'], digest=a['digest'],
                         url=a['browser_download_url']) for a in value['assets']], key=lambda x: x['id']))


def previous_inventory(root=ROOT, getter=None, allow_target=False):
    getter = getter or api
    raw = (Path(root) / BASELINE).read_bytes()
    require(sha(raw) == release.support.PRESERVED_INPUTS[BASELINE], 'V035-PUBLISH-BASELINE-DRIFT')
    baseline = release.loads(raw)['releases']
    rows = getter('releases?per_page=100')
    require(isinstance(rows, list), 'V035-PUBLISH-RELEASE-LIST')
    prior = [r for r in rows if r['tag_name'] != TAG]
    require(len(prior) == len(baseline) == 11 and sum(len(r['assets']) for r in prior) == 58,
            'V035-PUBLISH-PRIOR-POPULATION')
    require(len(rows) == (12 if allow_target else 11), 'V035-PUBLISH-TARGET-POPULATION')
    actual = {r['tag_name']: r for r in prior}
    require(set(actual) == {r['tag'] for r in baseline}, 'V035-PUBLISH-PRIOR-TAGS')
    proof = []
    for row in baseline:
        expected = {k: row[k] for k in ('tag', 'release_id', 'name', 'draft', 'prerelease',
                                         'published_at', 'url', 'assets')}
        expected['assets'] = sorted(expected['assets'], key=lambda a: a['id'])
        require(normalized_release(actual[row['tag']]) == expected, 'V035-PUBLISH-PRIOR-CHANGED: ' + row['tag'])
        require(tag_commit(row['tag'], getter) == row['source_commit'],
                'V035-PUBLISH-PRIOR-SOURCE: ' + row['tag'])
        proof.append(dict(expected, source_commit=row['source_commit']))
    return proof


def assert_new(getter=None):
    getter = getter or api
    for path in ('git/ref/tags/' + TAG, 'releases/tags/' + TAG):
        require(getter(path, missing_ok=True) is None, 'V035-PUBLISH-EXISTING-TAG-RELEASE')
    require(not any(r['tag_name'] == TAG for r in getter('releases?per_page=100')),
            'V035-PUBLISH-EXISTING-DRAFT')


@contextmanager
def trusted_package(root, source, run_id, artifact_id=None, digest=None, required=('freeze',)):
    intent = resolve_intent(root, source)
    require(intent['publish'] is True, 'V035-PUBLISH-NO-ONE-SHOT-AUTHORITY')
    item = authenticated_artifact(run_id, source, artifact_id, digest, required)
    with tempfile.TemporaryDirectory() as tmp:
        archive = Path(tmp) / 'freeze.zip'
        folder = Path(tmp) / 'assets'
        download_zip(item, archive)
        unpack_assets(archive, folder)
        freeze, manifest = release.validate_package(folder, source)
        verify_git_archive(root, folder, source)
        # A publication attempt requires current channel evidence as well as
        # the permanent archived proof evaluated at its original freeze time.
        envelope = release.loads((folder / 'artifact-versions.json').read_bytes())['matrix']
        release.validate_freshness(envelope, freeze['publication_freshness'], source)
        yield folder, freeze, manifest, item


def asset_inventory(folder):
    return [dict(name=name, bytes=(Path(folder) / name).stat().st_size,
                 sha256=sha((Path(folder) / name).read_bytes())) for name in sorted(release.ASSETS)]


def verify_download(folder, source, draft=False):
    """Read actual remote bodies and metadata, separately from staged assets."""
    if draft:
        matches = [r for r in api('releases?per_page=100') if r['tag_name'] == TAG]
        require(len(matches) == 1, 'V035-PUBLISH-DRAFT-AMBIGUOUS')
        info = matches[0]
        require(info['draft'] is True and info['target_commitish'] == source,
                'V035-PUBLISH-DRAFT-TARGET')
    else:
        info = api('releases/tags/' + TAG)
        latest = api('releases/latest')
        require(info['draft'] is False and latest['id'] == info['id']
                and latest['tag_name'] == TAG and tag_commit(TAG) == source,
                'V035-PUBLISH-PUBLIC-TAG-LATEST')
    require(info['prerelease'] is False and len(info['assets']) == 6
            and {a['name'] for a in info['assets']} == release.ASSETS,
            'V035-PUBLISH-SIX-PUBLIC-ASSETS')
    with tempfile.TemporaryDirectory() as tmp:
        gh('release', 'download', TAG, '--repo', REPO, '--dir', tmp)
        downloaded = Path(tmp)
        freeze, manifest = release.validate_package(downloaded, source)
        rows = []
        for item in sorted(info['assets'], key=lambda a: a['name']):
            raw = (downloaded / item['name']).read_bytes()
            require(raw == (Path(folder) / item['name']).read_bytes(), 'V035-PUBLISH-DOWNLOADED-BYTES')
            require(item['size'] == len(raw) and item.get('digest') == 'sha256:' + sha(raw),
                    'V035-PUBLISH-PUBLIC-SIZE-DIGEST')
            rows.append(dict(id=item['id'], name=item['name'], size=len(raw), sha256=sha(raw),
                             url=item['browser_download_url']))
        return dict(tag=TAG, release_id=info['id'], source_commit=source,
                    release_url=info['html_url'], published_at=info['published_at'], assets=rows,
                    source_file_count=manifest['file_count'], core_checks=len(freeze['checks']),
                    release_checks=len(freeze['release_specific_checks']),
                    frozen_at_utc=freeze['frozen_at_utc'], checks=freeze['checks'],
                    final_metadata=dict(draft=info['draft'], prerelease=info['prerelease']),
                    actual_downloaded_bytes_match=True, source_inventory_verified=True,
                    tag_commit_verified=not draft, latest_verified=not draft)


def require_actions(run_id):
    require(os.environ.get('GITHUB_ACTIONS') == 'true'
            and os.environ.get('GITHUB_REPOSITORY') == REPO
            and os.environ.get('GITHUB_RUN_ID') == str(run_id), 'V035-PUBLISH-TRUSTED-ACTIONS-ONLY')


def stage(root, source, run_id, record):
    with trusted_package(root, source, run_id) as (folder, freeze, manifest, item):
        proof = dict(schema='riskium-v035-staged-publication-readback-v1', source_commit=source,
                     workflow_run_id=run_id, artifact_id=item['id'], artifact_sha256=item['digest'][7:],
                     complete_package_verified=True, all_git_blobs_and_modes_verified=True,
                     source_file_count=manifest['file_count'], assets=asset_inventory(folder),
                     publication_executed=False)
        write(record, proof)
        output = os.environ.get('GITHUB_OUTPUT')
        if output:
            with open(output, 'a') as stream:
                stream.write('artifact_id=' + str(item['id']) + '\nartifact_sha256=' + item['digest'][7:] + '\n')
        return proof


def publish(root, source, run_id, artifact_id, digest, record):
    require_actions(run_id)
    with trusted_package(root, source, run_id, artifact_id, digest,
                         required=('freeze', 'staged')) as (folder, freeze, manifest, item):
        assert_new()
        previous = previous_inventory(root)
        require(api('releases/latest')['tag_name'] == 'v0.3.4', 'V035-PUBLISH-UNREVIEWED-LATEST')
        attempt = dict(schema='riskium-v035-publication-attempt-v1', source_commit=source,
                       workflow_run_id=run_id, freeze_artifact_id=item['id'],
                       freeze_artifact_sha256=item['digest'][7:], previous_releases=previous)
        write(record, attempt)
        files = [str(folder / name) for name in sorted(release.ASSETS)]
        gh('release', 'create', TAG, *files, '--repo', REPO, '--target', source,
           '--draft', '--prerelease=false', '--latest=false', '--title', 'Riskium ' + TAG,
           '--notes-file', str(folder / 'release-notes.md'))
        draft = verify_download(folder, source, draft=True)
        attempt['draft_download'] = {k: v for k, v in draft.items() if k != 'checks'}
        write(record, attempt)
        require(api('git/ref/heads/main')['object']['sha'] == source, 'V035-PUBLISH-MAIN-ADVANCED')
        previous_inventory(root, allow_target=True)
        # No force/update/delete operation exists on any tag or old release.
        current_tag = api('git/ref/tags/' + TAG, missing_ok=True)
        if current_tag is not None:
            require(tag_commit(TAG) == source, 'V035-PUBLISH-DRAFT-TAG-SOURCE')
        gh('release', 'edit', TAG, '--repo', REPO, '--draft=false', '--prerelease=false', '--latest=true')
        latest = api('releases/latest')
        require(latest['id'] == draft['release_id'] and latest['tag_name'] == TAG,
                'V035-PUBLISH-NOT-LATEST')
        require(tag_commit(TAG) == source, 'V035-PUBLISH-WRONG-TAG-SOURCE')
        require(api('git/ref/heads/main')['object']['sha'] == source, 'V035-PUBLISH-MAIN-ADVANCED')
        previous_inventory(root, allow_target=True)
        attempt.update(publication_executed=True, release_id=draft['release_id'],
                       state='PUBLISHED_REQUIRES_SEPARATE_PUBLIC_READBACK')
        write(record, attempt)
        return {k: v for k, v in attempt.items() if k != 'previous_releases'}


def verify(root, source, run_id, artifact_id, digest, record):
    with trusted_package(root, source, run_id, artifact_id, digest,
                         required=('freeze', 'staged', 'publish')) as (folder, freeze, manifest, item):
        proof = verify_download(folder, source)
        proof.pop('checks')
        full = freeze['checks'][-1]
        summary = re.search(r'Ran ([0-9]+) tests in ([0-9.]+)s', full['stdout'] + full['stderr'])
        require(summary is not None, 'V035-PUBLISH-SOFTWARE-SUMMARY')
        proof.update(schema='riskium-v035-publication-readback-v1',
                     state='PUBLISHED_AND_INDEPENDENTLY_DOWNLOADED_VERIFIED',
                     workflow_run_id=run_id, workflow_url='https://github.com/' + REPO + '/actions/runs/' + str(run_id),
                     freeze_artifact_id=item['id'], freeze_artifact_sha256=item['digest'][7:],
                     full_software_tests=int(summary[1]), full_tests_seconds=float(summary[2]),
                     checked_at_utc=datetime.now(timezone.utc).isoformat(),
                     previous_releases=previous_inventory(root, allow_target=True),
                     publication_executed=True, independent_semantic_validation=False,
                     new_owner_responses_generated=0)
        write(record, proof)
        return proof


def retire(root, source, run_id, record):
    require_actions(run_id)
    require(resolve_intent(root, source)['publish'] is True, 'V035-PUBLISH-NO-AUTHORITY')
    run = api('actions/runs/' + str(run_id))
    workflow_origin(run, source)
    require_jobs(api('actions/runs/' + str(run_id) + '/jobs?per_page=100')['jobs'],
                 ('freeze', 'staged', 'publish', 'verify'))
    require(api('git/ref/heads/main')['object']['sha'] == source
            and api('releases/latest')['tag_name'] == TAG and tag_commit(TAG) == source,
            'V035-PUBLISH-RETIRE-BEFORE-VERIFIED-RELEASE')
    previous_inventory(root, allow_target=True)
    rows = []
    for path in LEGACY:
        name = Path(path).name
        item = api('actions/workflows/' + name)
        require(item['path'] == path and item['state'] in ('active', 'disabled_manually'),
                'V035-PUBLISH-UNEXPECTED-LEGACY-WORKFLOW')
        before = item['state']
        if before == 'active':
            api('actions/workflows/' + str(item['id']) + '/disable', method='PUT')
        after = api('actions/workflows/' + str(item['id']))
        require(after['path'] == path and after['state'] == 'disabled_manually',
                'V035-PUBLISH-LEGACY-NOT-RETIRED')
        rows.append(dict(path=path, id=item['id'], previous_state=before, state=after['state']))
    proof = dict(schema='riskium-v035-deployment-transition-v1', source_commit=source,
                 workflow_run_id=run_id, verified_release=TAG, retired_workflows=rows,
                 preserved_workflow_files=True, next_issue=60,
                 next_gate='Add v0.3.5 current Pages/Wiki projection and actual readback; no v0.3.6 target.')
    write(record, proof)
    return proof


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('intent', 'stage', 'publish', 'verify', 'retire'))
    parser.add_argument('--source-commit', required=True)
    parser.add_argument('--run-id', type=int)
    parser.add_argument('--artifact-id', type=int)
    parser.add_argument('--artifact-sha256')
    parser.add_argument('--record', type=Path)
    args = parser.parse_args()
    require(re.fullmatch('[a-f0-9]{40}', args.source_commit), 'V035-PUBLISH-SOURCE')
    if args.mode == 'intent':
        result = resolve_intent(ROOT, args.source_commit)
        if os.environ.get('GITHUB_OUTPUT'):
            with open(os.environ['GITHUB_OUTPUT'], 'a') as out:
                out.write('publish=' + str(result['publish']).lower() + '\n')
    else:
        require(args.run_id is not None and args.record is not None, 'V035-PUBLISH-MISSING-INPUTS')
        if args.mode in ('publish', 'verify'):
            require(args.artifact_id is not None and re.fullmatch('[a-f0-9]{64}', args.artifact_sha256 or ''),
                    'V035-PUBLISH-ARTIFACT-REFERENCE')
        function = dict(stage=stage, publish=publish, verify=verify, retire=retire)[args.mode]
        if args.mode in ('publish', 'verify'):
            result = function(ROOT, args.source_commit, args.run_id, args.artifact_id,
                              args.artifact_sha256, args.record)
        else:
            result = function(ROOT, args.source_commit, args.run_id, args.record)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
