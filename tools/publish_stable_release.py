"""Publish a new reviewed stable package or independently verify its downloaded assets.

Only the release workflow supplies GH_TOKEN. It is never read or printed here;
GitHub CLI uses its ordinary environment authentication.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tarfile
import tempfile

from prepare_stable_release import require, validate_checks

TAG = 'v0.3.1'
ASSETS = {'riskium-v0.3.1-source.tar.gz', 'source-manifest.json', 'freeze-receipt.json',
          'artifact-versions.json', 'release-notes.md', 'SHA256SUMS.txt'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def gh(repo, *args):
    return subprocess.check_output(['gh', *args], text=True)


def api(repo, path, missing_ok=False):
    run = subprocess.run(['gh', 'api', 'repos/' + repo + '/' + path], capture_output=True, text=True)
    if run.returncode:
        if missing_ok and 'HTTP 404' in run.stderr:
            return None
        raise ValueError('GitHub API read failed closed: ' + path)
    return json.loads(run.stdout)


def assert_new(repo, getter=api):
    for path in ('git/ref/tags/' + TAG, 'releases/tags/' + TAG):
        require(getter(repo, path, missing_ok=True) is None, 'Existing stable tag/release is never overwritten: ' + path)
    releases = getter(repo, 'releases?per_page=100')
    require(isinstance(releases, list) and not any(r['tag_name'] == TAG for r in releases), 'Existing draft stable release is never overwritten')


def tag_commit(repo, tag):
    target = api(repo, 'git/ref/tags/' + tag)['object']
    for _ in range(10):
        if target['type'] != 'tag':
            break
        target = api(repo, 'git/tags/' + target['sha'])['object']
    require(target['type'] == 'commit', 'Tag does not resolve to a commit')
    return target['sha']


def previous_releases(repo):
    rows = []
    for n in range(1, 8):
        tag = f'v0.3.1-rc.{n}'
        release = api(repo, 'releases/tags/' + tag)
        rows.append({'tag': tag, 'commit': tag_commit(repo, tag), 'release_id': release['id'],
                     'draft': release['draft'], 'prerelease': release['prerelease'],
                     'assets': [{'id': a['id'], 'name': a['name'], 'size': a['size'], 'digest': a.get('digest')} for a in sorted(release['assets'], key=lambda a: a['name'])]})
    return rows


def validate_package(folder, source_commit):
    folder = Path(folder)
    require({p.name for p in folder.iterdir()} == ASSETS, 'Missing or unexpected stable asset')
    freeze = json.loads((folder / 'freeze-receipt.json').read_text())
    require(freeze['tag'] == TAG and freeze['source_commit'] == source_commit, 'Wrong frozen tag/source commit')
    require(freeze['maturity'] == 'stable-bounded-research-artifact' and freeze['model_version'] == '0.3.1', 'Wrong stable profile/model')
    require(freeze['clean_exact_head'] is True and freeze['archive_inventory_verified'] is True, 'Missing clean source/inventory gates')
    require(freeze['known_unresolved_critical_findings'] == [] and freeze['accepted_publication_condition'] == 'TECHNICAL_FREEZE_GATES_SATISFIED_BEFORE_PUBLICATION', 'Unsatisfied final technical condition')
    require(freeze['passed_checks'] == len(freeze['checks']), 'Freeze check count mismatch')
    require(freeze['new_owner_responses_generated'] == 0 and freeze['independent_validation'] is False, 'Unsupported owner/independence claim')
    validate_checks(freeze['checks'])
    sums = {}
    for line in (folder / 'SHA256SUMS.txt').read_text().splitlines():
        expected, name = line.split('  ', 1)
        require(name in ASSETS - {'SHA256SUMS.txt'} and name not in sums and re.fullmatch('[0-9a-f]{64}', expected), 'Invalid checksum inventory')
        require(digest((folder / name).read_bytes()) == expected, 'Asset digest mismatch: ' + name)
        sums[name] = expected
    require(set(sums) == ASSETS - {'SHA256SUMS.txt'}, 'Incomplete checksum inventory')
    manifest = json.loads((folder / 'source-manifest.json').read_text())
    require(manifest['tag'] == TAG and manifest['source_commit'] == source_commit, 'Wrong source inventory binding')
    with tarfile.open(folder / 'riskium-v0.3.1-source.tar.gz') as tar:
        actual = []
        for member in tar:
            require(member.isfile() and member.name.startswith('riskium-' + TAG + '/') and '..' not in Path(member.name).parts, 'Unsafe/unexpected archive member')
            actual.append({'path': member.name.split('/', 1)[1], 'bytes': member.size, 'sha256': digest(tar.extractfile(member).read())})
    require(actual == manifest['files'] and len(actual) == manifest['file_count'], 'Downloaded source archive inventory mismatch')
    matrix = json.loads((folder / 'artifact-versions.json').read_text())
    require(matrix['tag'] == TAG and matrix['source_commit'] == source_commit and len(matrix['matrix']['artifacts']) == 10, 'Frozen artifact matrix mismatch')
    indexed = {row['path']: row for row in actual}
    require(indexed['releases/stable-profile-v0.3.1.json']['sha256'] == freeze['profile_sha256'], 'Archived stable profile mismatch')
    require(indexed['evaluation/finalization/v0.3.1-review.json']['sha256'] == freeze['critical_screen_sha256'], 'Archived critical screen mismatch')
    require(indexed['releases/artifact-matrix.json']['sha256'] == matrix['matrix_sha256'], 'Artifact matrix not bound to archived source')
    require(digest((json.dumps(matrix['matrix'], indent=2, ensure_ascii=False) + '\n').encode()) == matrix['matrix_sha256'], 'Frozen matrix content changed')
    require(source_commit in (folder / 'release-notes.md').read_text(), 'Notes not bound to source commit')
    return freeze, manifest


def verify_download(repo, expected_folder, source_commit, allow_draft=False):
    with tempfile.TemporaryDirectory() as temp:
        gh(repo, 'release', 'download', TAG, '--repo', repo, '--dir', temp)
        folder = Path(temp)
        freeze, manifest = validate_package(folder, source_commit)
        for name in ASSETS:
            require((folder / name).read_bytes() == (Path(expected_folder) / name).read_bytes(), 'Downloaded bytes differ: ' + name)
        if allow_draft:
            matches = [r for r in api(repo, 'releases?per_page=100') if r['tag_name'] == TAG]
            require(len(matches) == 1, 'Draft release lookup is ambiguous or missing')
            release = matches[0]
        else:
            release = api(repo, 'releases/tags/' + TAG)
        require(release['prerelease'] is False and (allow_draft or release['draft'] is False), 'Wrong final release designation')
        if allow_draft:
            require(release['target_commitish'] == source_commit, 'Draft target differs from frozen source')
        else:
            require(tag_commit(repo, TAG) == source_commit, 'Final tag points to wrong source')
        require({a['name'] for a in release['assets']} == ASSETS and len(release['assets']) == len(ASSETS), 'Uploaded asset inventory mismatch')
        assets = []
        for asset in sorted(release['assets'], key=lambda a: a['name']):
            data = (folder / asset['name']).read_bytes()
            actual_sha = digest(data)
            require(asset['size'] == len(data) and asset.get('digest') == 'sha256:' + actual_sha, 'GitHub asset digest/size mismatch')
            assets.append({'id': asset['id'], 'name': asset['name'], 'size': len(data), 'sha256': actual_sha, 'url': asset['browser_download_url']})
        return {'tag': TAG, 'release_id': release['id'], 'published_at': release['published_at'],
                'source_commit': source_commit, 'release_url': release['html_url'], 'assets': assets,
                'source_file_count': manifest['file_count'], 'passed_checks': freeze['passed_checks'],
                'regression_summary': next(c['stderr'].splitlines()[-3:] for c in freeze['checks'] if c['command'][1:3] == ['-m', 'unittest']),
                'final_metadata': {'draft': release['draft'], 'prerelease': release['prerelease']},
                'downloaded_bytes_match': True, 'archive_inventory_verified': True,
                'artifact_matrix_verified': True, 'tag_commit_verified': not allow_draft}


def publish(repo, folder, source_commit, record):
    validate_package(folder, source_commit)
    require(os.environ.get('GITHUB_REF') == 'refs/heads/main' and os.environ.get('GITHUB_SHA') == source_commit, 'Stable publication requires reviewed exact main run')
    require(api(repo, 'git/ref/heads/main')['object']['sha'] == source_commit, 'Main advanced after freeze; review a fresh candidate')
    assert_new(repo)
    previous = previous_releases(repo)
    record.parent.mkdir(parents=True, exist_ok=True)
    record.write_text(json.dumps({'source_commit': source_commit, 'tag': TAG, 'previous_releases': previous}, indent=2) + '\n')
    files = [str(Path(folder) / name) for name in sorted(ASSETS)]
    gh(repo, 'release', 'create', TAG, *files, '--repo', repo, '--target', source_commit,
       '--draft', '--prerelease=false', '--latest=false', '--title', 'Riskium v0.3.1', '--notes-file', str(Path(folder) / 'release-notes.md'))
    verify_download(repo, folder, source_commit, allow_draft=True)
    gh(repo, 'release', 'edit', TAG, '--repo', repo, '--draft=false', '--prerelease=false', '--latest=true')
    require(api(repo, 'releases/latest')['tag_name'] == TAG, 'Final release not designated latest')
    require(previous_releases(repo) == previous, 'A previous prerelease changed')
    print(json.dumps({'status': 'STABLE_PUBLISHED_REQUIRES_SEPARATE_READBACK', 'tag': TAG, 'source_commit': source_commit}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('publish', 'verify'))
    parser.add_argument('--repo', required=True)
    parser.add_argument('--folder', type=Path, required=True)
    parser.add_argument('--source-commit', required=True)
    parser.add_argument('--record', type=Path, required=True)
    args = parser.parse_args()
    require(re.fullmatch('[0-9a-f]{40}', args.source_commit), 'Exact source commit required')
    if args.mode == 'publish':
        publish(args.repo, args.folder, args.source_commit, args.record)
    else:
        previous = json.loads(args.record.read_text())
        receipt = verify_download(args.repo, args.folder, args.source_commit)
        require(api(args.repo, 'releases/latest')['tag_name'] == TAG, 'Latest release mismatch')
        require(previous['source_commit'] == args.source_commit and previous_releases(args.repo) == previous['previous_releases'], 'Previous prerelease preservation failed')
        receipt.update(schema='riskium-stable-publication-v1', publication_state='PUBLISHED_AND_INDEPENDENTLY_DOWNLOADED_VERIFIED',
                       previous_releases=previous['previous_releases'], workflow_run=int(os.environ['GITHUB_RUN_ID']),
                       workflow_url='https://github.com/' + args.repo + '/actions/runs/' + os.environ['GITHUB_RUN_ID'],
                       latest_verified=True, no_new_owner_response=True, independent_semantic_validation=False)
        args.record.with_name('v0.3.1-publication.json').write_text(json.dumps(receipt, indent=2) + '\n')
        print('STABLE_PUBLICATION_READBACK=' + json.dumps(receipt))


if __name__ == '__main__':
    main()
