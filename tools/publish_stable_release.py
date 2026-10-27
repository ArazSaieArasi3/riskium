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
def assets(tag):
    require(re.fullmatch(r'v[0-9]+\.[0-9]+\.[0-9]+', tag), 'Invalid stable tag')
    return {'riskium-' + tag + '-source.tar.gz', 'source-manifest.json', 'freeze-receipt.json',
            'artifact-versions.json', 'release-notes.md', 'SHA256SUMS.txt'}


ASSETS = assets(TAG)


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


def assert_new(repo, getter=api, tag=TAG):
    for path in ('git/ref/tags/' + tag, 'releases/tags/' + tag):
        require(getter(repo, path, missing_ok=True) is None, 'Existing stable tag/release is never overwritten: ' + path)
    releases = getter(repo, 'releases?per_page=100')
    require(isinstance(releases, list) and not any(r['tag_name'] == tag for r in releases), 'Existing draft stable release is never overwritten')


def tag_commit(repo, tag):
    target = api(repo, 'git/ref/tags/' + tag)['object']
    for _ in range(10):
        if target['type'] != 'tag':
            break
        target = api(repo, 'git/tags/' + target['sha'])['object']
    require(target['type'] == 'commit', 'Tag does not resolve to a commit')
    return target['sha']


def previous_releases(repo, target=TAG):
    rows = []
    tags = [f'v0.3.1-rc.{n}' for n in range(1, 8)]
    if target != TAG:
        tags.append(TAG)
    if target == 'v0.3.3':
        tags.append('v0.3.2')
    for tag in tags:
        release = api(repo, 'releases/tags/' + tag)
        rows.append({'tag': tag, 'commit': tag_commit(repo, tag), 'release_id': release['id'],
                     'draft': release['draft'], 'prerelease': release['prerelease'],
                     'assets': [{'id': a['id'], 'name': a['name'], 'size': a['size'], 'digest': a.get('digest')} for a in sorted(release['assets'], key=lambda a: a['name'])]})
    return rows


def validate_package(folder, source_commit):
    folder = Path(folder)
    require(len(list(folder.iterdir())) == 6, 'Missing or unexpected stable asset')
    require((folder / 'freeze-receipt.json').is_file(), 'Missing or unexpected stable asset')
    freeze = json.loads((folder / 'freeze-receipt.json').read_text())
    tag = freeze.get('tag', '')
    selected_assets = assets(tag)
    require({p.name for p in folder.iterdir()} == selected_assets, 'Missing or unexpected stable asset')
    require(freeze['tag'] == tag and freeze['source_commit'] == source_commit, 'Wrong frozen tag/source commit')
    require(freeze['maturity'] == 'stable-bounded-research-artifact' and freeze['model_version'] == '0.3.1', 'Wrong stable profile/model')
    require(freeze['clean_exact_head'] is True and freeze['archive_inventory_verified'] is True, 'Missing clean source/inventory gates')
    condition = 'TECHNICAL_FREEZE_GATES_SATISFIED_BEFORE_PUBLICATION' if tag == TAG else 'REVIEWED_SUCCESSOR_COMPONENT_GATES_SATISFIED_BEFORE_PUBLICATION'
    require(freeze['known_unresolved_critical_findings'] == [] and freeze['accepted_publication_condition'] == condition, 'Unsatisfied final technical condition')
    require(freeze['passed_checks'] == len(freeze['checks']), 'Freeze check count mismatch')
    require(freeze['new_owner_responses_generated'] == 0 and freeze['independent_validation'] is False, 'Unsupported owner/independence claim')
    validate_checks(freeze['checks'])
    sums = {}
    for line in (folder / 'SHA256SUMS.txt').read_text().splitlines():
        expected, name = line.split('  ', 1)
        require(name in selected_assets - {'SHA256SUMS.txt'} and name not in sums and re.fullmatch('[0-9a-f]{64}', expected), 'Invalid checksum inventory')
        require(digest((folder / name).read_bytes()) == expected, 'Asset digest mismatch: ' + name)
        sums[name] = expected
    require(set(sums) == selected_assets - {'SHA256SUMS.txt'}, 'Incomplete checksum inventory')
    manifest = json.loads((folder / 'source-manifest.json').read_text())
    require(manifest['tag'] == tag and manifest['source_commit'] == source_commit, 'Wrong source inventory binding')
    blobs = {}
    with tarfile.open(folder / ('riskium-' + tag + '-source.tar.gz')) as tar:
        actual = []
        for member in tar:
            require(member.isfile() and member.name.startswith('riskium-' + tag + '/') and '..' not in Path(member.name).parts, 'Unsafe/unexpected archive member')
            path = member.name.split('/', 1)[1]
            require(path not in blobs and str(Path(path)) == path, 'Duplicate/noncanonical archive member')
            blobs[path] = tar.extractfile(member).read()
            actual.append({'path': path, 'bytes': member.size, 'sha256': digest(blobs[path])})
    require(actual == manifest['files'] and len(actual) == manifest['file_count'], 'Downloaded source archive inventory mismatch')
    matrix = json.loads((folder / 'artifact-versions.json').read_text())
    expected_components = {'v0.3.1': 10, 'v0.3.2': 20, 'v0.3.3': 24}
    require(tag in expected_components and matrix['tag'] == tag and matrix['source_commit'] == source_commit and len(matrix['matrix']['artifacts']) == expected_components[tag], 'Frozen artifact matrix mismatch')
    indexed = {row['path']: row for row in actual}
    require(indexed[freeze.get('profile_path', 'releases/stable-profile-v0.3.1.json')]['sha256'] == freeze['profile_sha256'], 'Archived stable profile mismatch')
    require(indexed[freeze.get('critical_screen_path', 'evaluation/finalization/v0.3.1-review.json')]['sha256'] == freeze['critical_screen_sha256'], 'Archived critical screen mismatch')
    require(indexed[freeze.get('artifact_matrix_path', 'releases/artifact-matrix.json')]['sha256'] == matrix['matrix_sha256'], 'Artifact matrix not bound to archived source')
    require(digest((json.dumps(matrix['matrix'], indent=2, ensure_ascii=False) + '\n').encode()) == matrix['matrix_sha256'], 'Frozen matrix content changed')
    registry = json.loads(blobs['releases/stable-profiles.json'])
    require(registry['profiles'].get(tag) == freeze['profile_path'], 'Unregistered frozen stable profile')
    profile = json.loads(blobs[freeze['profile_path']])
    require(profile['tag'] == tag and profile['artifact_matrix'] == freeze['artifact_matrix_path'] and
            profile['critical_screen'] == freeze['critical_screen_path'], 'Frozen profile route mismatch')
    require(blobs[freeze['artifact_matrix_path']] == (json.dumps(matrix['matrix'], indent=2, ensure_ascii=False) + '\n').encode(), 'Archived/asset matrix mismatch')
    if tag != TAG:
        from review_distribution import validate_matrix, validate_freshness
        validate_matrix(matrix['matrix'], blobs.__getitem__)
        validate_freshness(matrix['matrix'], freeze['publication_freshness'])
        screen = json.loads(blobs[freeze['critical_screen_path']])
        require(screen['target'] == tag and screen['known_unresolved_critical_findings'] == [] and
                screen['component_matrix_sha256'] == matrix['matrix_sha256'] and
                screen['new_owner_responses_generated'] == 0 and
                screen['material_scientific_change_since_owner_acceptance'] is False,
                'Archived successor critical screen mismatch')
    require(source_commit in (folder / 'release-notes.md').read_text(), 'Notes not bound to source commit')
    return freeze, manifest


def verify_download(repo, expected_folder, source_commit, allow_draft=False):
    local_freeze, _ = validate_package(expected_folder, source_commit)
    tag = local_freeze['tag']
    selected_assets = assets(tag)
    with tempfile.TemporaryDirectory() as temp:
        gh(repo, 'release', 'download', tag, '--repo', repo, '--dir', temp)
        folder = Path(temp)
        freeze, manifest = validate_package(folder, source_commit)
        for name in selected_assets:
            require((folder / name).read_bytes() == (Path(expected_folder) / name).read_bytes(), 'Downloaded bytes differ: ' + name)
        if allow_draft:
            matches = [r for r in api(repo, 'releases?per_page=100') if r['tag_name'] == tag]
            require(len(matches) == 1, 'Draft release lookup is ambiguous or missing')
            release = matches[0]
        else:
            release = api(repo, 'releases/tags/' + tag)
        require(release['prerelease'] is False and (allow_draft or release['draft'] is False), 'Wrong final release designation')
        if allow_draft:
            require(release['target_commitish'] == source_commit, 'Draft target differs from frozen source')
        else:
            require(tag_commit(repo, tag) == source_commit, 'Final tag points to wrong source')
        require({a['name'] for a in release['assets']} == selected_assets and len(release['assets']) == len(selected_assets), 'Uploaded asset inventory mismatch')
        asset_rows = []
        for asset in sorted(release['assets'], key=lambda a: a['name']):
            data = (folder / asset['name']).read_bytes()
            actual_sha = digest(data)
            require(asset['size'] == len(data) and asset.get('digest') == 'sha256:' + actual_sha, 'GitHub asset digest/size mismatch')
            asset_rows.append({'id': asset['id'], 'name': asset['name'], 'size': len(data), 'sha256': actual_sha, 'url': asset['browser_download_url']})
        return {'tag': tag, 'release_id': release['id'], 'published_at': release['published_at'],
                'source_commit': source_commit, 'release_url': release['html_url'], 'assets': asset_rows,
                'source_file_count': manifest['file_count'], 'passed_checks': freeze['passed_checks'],
                'regression_summary': next(c['stderr'].splitlines()[-3:] for c in freeze['checks'] if c['command'][1:3] == ['-m', 'unittest']),
                'final_metadata': {'draft': release['draft'], 'prerelease': release['prerelease']},
                'downloaded_bytes_match': True, 'archive_inventory_verified': True,
                'artifact_matrix_verified': True, 'tag_commit_verified': not allow_draft}


def publish(repo, folder, source_commit, record):
    freeze, _ = validate_package(folder, source_commit)
    tag = freeze['tag']
    selected_assets = assets(tag)
    require(os.environ.get('GITHUB_REF') == 'refs/heads/main' and os.environ.get('GITHUB_SHA') == source_commit, 'Stable publication requires reviewed exact main run')
    require(api(repo, 'git/ref/heads/main')['object']['sha'] == source_commit, 'Main advanced after freeze; review a fresh candidate')
    assert_new(repo, tag=tag)
    previous = previous_releases(repo, tag)
    record.parent.mkdir(parents=True, exist_ok=True)
    record.write_text(json.dumps({'source_commit': source_commit, 'tag': tag, 'previous_releases': previous}, indent=2) + '\n')
    files = [str(Path(folder) / name) for name in sorted(selected_assets)]
    gh(repo, 'release', 'create', tag, *files, '--repo', repo, '--target', source_commit,
       '--draft', '--prerelease=false', '--latest=false', '--title', 'Riskium ' + tag, '--notes-file', str(Path(folder) / 'release-notes.md'))
    verify_download(repo, folder, source_commit, allow_draft=True)
    gh(repo, 'release', 'edit', tag, '--repo', repo, '--draft=false', '--prerelease=false', '--latest=true')
    require(api(repo, 'releases/latest')['tag_name'] == tag, 'Final release not designated latest')
    require(previous_releases(repo, tag) == previous, 'A previous prerelease changed')
    print(json.dumps({'status': 'STABLE_PUBLISHED_REQUIRES_SEPARATE_READBACK', 'tag': tag, 'source_commit': source_commit}))


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
        require(api(args.repo, 'releases/latest')['tag_name'] == receipt['tag'], 'Latest release mismatch')
        tag = receipt['tag']
        require(previous['source_commit'] == args.source_commit and previous_releases(args.repo, tag) == previous['previous_releases'], 'Previous prerelease preservation failed')
        receipt.update(schema='riskium-stable-publication-v1', publication_state='PUBLISHED_AND_INDEPENDENTLY_DOWNLOADED_VERIFIED',
                       previous_releases=previous['previous_releases'], workflow_run=int(os.environ['GITHUB_RUN_ID']),
                       workflow_url='https://github.com/' + args.repo + '/actions/runs/' + os.environ['GITHUB_RUN_ID'],
                       latest_verified=True, no_new_owner_response=True, independent_semantic_validation=False)
        args.record.with_name(tag + '-publication.json').write_text(json.dumps(receipt, indent=2) + '\n')
        print('STABLE_PUBLICATION_READBACK=' + json.dumps(receipt))


if __name__ == '__main__':
    main()
