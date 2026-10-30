"""Publish the authenticated, already frozen v0.3.7 assets exactly once."""
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import zipfile

REPOSITORY = 'ArazSaieArasi3/riskium'
SOURCE = '86accc6695e4738dd1337d5b9addd73b82c73c3d'
TAG = 'v0.3.7'
ARTIFACT = 12974134738
ZIP_SHA = '5e688437d8fad13d9893243a7b10275d3d341eb370bc418682f41fa70edbc9d2'
ASSETS = {
    'SHA256SUMS.txt': (440, '5cefbc220856e795a01cf094dff91345118a5ab0fef37226a393ce0410af88d5'),
    'artifact-versions.json': (359729, '05183c56f34892cc2253275f9a3e2f23d425037f5af8a23f3b199a8ccc9e6943'),
    'freeze-receipt.json': (396390, 'e8d1a987bfe5f646bed067bf48be424aaf5ca1a12655f6903c886d00fa23ce83'),
    'release-notes.md': (5235, '2ec5a22ee81f49a8f535b273a0882ebf5e7a4c91c9f633b24b4d31d73cab3ff3'),
    'riskium-v0.3.7-source.tar.gz': (15319284, 'a7bc39fc2564d06a1df661245a93ad01256890a9975f665f4f4a962da267c513'),
    'source-manifest.json': (246870, 'fc4786764b594cd8eb1efa17cde1c7b544d33ce5e9cc74e0f5c76c0b428e8cef'),
}


def require(value, message):
    if not value:
        raise ValueError(message)


class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        result = super().redirect_request(req, fp, code, msg, headers, newurl)
        if urllib.parse.urlsplit(req.full_url).netloc != urllib.parse.urlsplit(newurl).netloc:
            result.remove_header('Authorization')
        return result


opener = urllib.request.build_opener(SafeRedirect())


def request(path, method='GET', data=None, raw=None):
    url = path if path.startswith('https://') else 'https://api.github.com/repos/' + REPOSITORY + '/' + path
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'riskium-v037-frozen-publication'}
    if urllib.parse.urlsplit(url).netloc in ('api.github.com', 'uploads.github.com'):
        headers['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
    body = raw
    if data is not None:
        body = json.dumps(data).encode()
        headers['Content-Type'] = 'application/json'
    elif raw is not None:
        headers['Content-Type'] = 'application/octet-stream'
    with opener.open(urllib.request.Request(url, data=body, headers=headers, method=method), timeout=120) as response:
        content = response.read()
    return content


def api(path, **kwargs):
    return json.loads(request(path, **kwargs))


def absent(path):
    try:
        api(path)
    except urllib.error.HTTPError as exc:
        require(exc.code == 404, 'Expected explicit absence: ' + path)
    else:
        raise ValueError('Refusing to overwrite existing target: ' + path)


def inventory(releases):
    return sorted([dict(id=r['id'], tag=r['tag_name'], draft=r['draft'], prerelease=r['prerelease'],
                        published_at=r['published_at'], assets=sorted([
                            {k: a[k] for k in ('id', 'name', 'size', 'digest')} for a in r['assets']
                        ], key=lambda a: a['id'])) for r in releases], key=lambda r: r['id'])


def check_assets(release):
    actual = {a['name']: (a['size'], a['digest'], a['state']) for a in release['assets']}
    require(actual == {name: (size, 'sha256:' + digest, 'uploaded')
                       for name, (size, digest) in ASSETS.items()}, 'Uploaded asset identity mismatch')


def main():
    require(os.environ['GITHUB_REPOSITORY'] == REPOSITORY, 'Wrong repository')
    require(os.environ['GITHUB_REF'] == 'refs/heads/release/v0.3.7-publication', 'Wrong publication branch')
    require(api('git/ref/heads/main')['object']['sha'] == SOURCE, 'Main advanced beyond frozen source')
    require(api('releases/latest')['tag_name'] == 'v0.3.6', 'Latest baseline changed')
    absent('git/ref/tags/' + TAG)
    absent('releases/tags/' + TAG)
    before = api('releases?per_page=100')
    old = json.loads(Path('evaluation/releases/v0.3.7/branch-qualification.json').read_text())['previous_release_inventory']
    old = sorted([dict(r, assets=sorted(r['assets'], key=lambda a: a['id'])) for r in old], key=lambda r: r['id'])
    require(inventory(before) == old and len(before) == 13, 'Prior releases changed')
    prior_tags = {r['tag_name']: api('git/ref/tags/' + r['tag_name'])['object'] for r in before}
    meta = api('actions/artifacts/' + str(ARTIFACT))
    require(meta['digest'] == 'sha256:' + ZIP_SHA and not meta['expired'] and
            meta['workflow_run']['id'] == 41051824077 and meta['workflow_run']['head_sha'] == SOURCE,
            'Artifact source/authenticity mismatch')
    run = api('actions/runs/41051824077')
    require(run['head_sha'] == SOURCE and run['conclusion'] == 'success' and
            run['path'] == '.github/workflows/freeze-v037.yml', 'Freeze run mismatch')
    raw = request('actions/artifacts/' + str(ARTIFACT) + '/zip')
    require(len(raw) == 15640450 and hashlib.sha256(raw).hexdigest() == ZIP_SHA, 'Downloaded artifact mismatch')
    folder = Path(os.environ['RUNNER_TEMP']) / 'frozen-v037'
    folder.mkdir()
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        require(len(archive.namelist()) == 6 and set(archive.namelist()) == set(ASSETS), 'Unexpected ZIP inventory')
        for name, (size, digest) in ASSETS.items():
            data = archive.read(name)
            require(len(data) == size and hashlib.sha256(data).hexdigest() == digest, 'Frozen asset mismatch: ' + name)
            (folder / name).write_bytes(data)
    subprocess.run([sys.executable, '-S', 'tools/releases/v037/freeze.py', 'verify', '--folder', str(folder),
                    '--source', SOURCE], check=True)
    require(api('git/ref/heads/main')['object']['sha'] == SOURCE, 'Main changed before publication')
    require(inventory(api('releases?per_page=100')) == old, 'Inventory changed before publication')
    absent('git/ref/tags/' + TAG)
    absent('releases/tags/' + TAG)
    notes = (folder / 'release-notes.md').read_text()
    notes += ('\n---\n\nExact source: `' + SOURCE + '`. The six attached assets are unchanged from '
              '[authenticated freeze 41051824077](https://github.com/' + REPOSITORY + '/actions/runs/41051824077). '
              '[Publication and live-channel completion](https://github.com/' + REPOSITORY + '/issues/66) '
              'records the subsequent independent public downloads and reader maintenance.\n')
    release = api('releases', method='POST', data=dict(tag_name=TAG, target_commitish=SOURCE,
                  name='v0.3.7 — Versioned risk-nature assertion history', body=notes,
                  draft=True, prerelease=False, make_latest='false'))
    release_id = release['id']
    print(json.dumps(dict(stage='DRAFT_CREATED', release_id=release_id)), flush=True)
    for name in ASSETS:
        uploaded = api('https://uploads.github.com/repos/' + REPOSITORY + '/releases/' + str(release_id)
                       + '/assets?name=' + urllib.parse.quote(name), method='POST', raw=(folder / name).read_bytes())
        require((uploaded['size'], uploaded['digest']) == (ASSETS[name][0], 'sha256:' + ASSETS[name][1]),
                'Upload readback mismatch: ' + name)
    draft = api('releases/' + str(release_id))
    check_assets(draft)
    require(draft['draft'] and draft['target_commitish'] == SOURCE, 'Wrong draft target')
    published = api('releases/' + str(release_id), method='PATCH', data=dict(draft=False, prerelease=False, make_latest='true'))
    check_assets(published)
    require(not published['draft'] and not published['prerelease'], 'Release not stable/public')
    require(api('releases/latest')['id'] == release_id, 'Latest not v0.3.7')
    tag = api('git/ref/tags/' + TAG)['object']
    require(tag['type'] == 'commit' and tag['sha'] == SOURCE, 'Published tag source mismatch')
    after = api('releases?per_page=100')
    require(len(after) == 14 and inventory([r for r in after if r['id'] != release_id]) == old,
            'Prior release inventories changed')
    require({t: api('git/ref/tags/' + t)['object'] for t in prior_tags} == prior_tags, 'Prior tags changed')
    downloads = []
    for asset in published['assets']:
        content = request(asset['browser_download_url'])
        name = asset['name']
        require((len(content), hashlib.sha256(content).hexdigest()) == ASSETS[name], 'Public download mismatch: ' + name)
        downloads.append(dict(name=name, id=asset['id'], bytes=len(content), sha256=hashlib.sha256(content).hexdigest(),
                              public_url=asset['browser_download_url']))
    proof = dict(status='V037_ACTUAL_PUBLICATION_AND_DOWNLOADS_PASS', release=published,
                 source_commit=SOURCE, tag_object=tag, artifact=meta, artifact_zip_sha256=ZIP_SHA,
                 actual_public_downloads=downloads, prior_release_inventory=old, prior_tag_objects=prior_tags,
                 prior_releases_unchanged=13, prior_assets_unchanged=70, channel_reconciliation='PENDING',
                 workflow_run_id=int(os.environ['GITHUB_RUN_ID']))
    output = Path('build/v037-publication.json'); output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(proof, indent=2) + '\n')
    print(json.dumps(dict(status=proof['status'], release_id=release_id, source=SOURCE,
                         actual_public_downloads=6, prior_releases=13, prior_assets=70)))


if __name__ == '__main__':
    main()
