"""Check the live repository entry point independently of frozen reader checkpoints."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
import markdown

ROOT = Path(__file__).resolve().parents[2]
NS = 'documentation/0.4.3'
REPO = 'https://github.com/ArazSaieArasi3/riskium'
SOURCE = '58ff468ec4e8f3500ace6869601a25ea263c3d9f'


def require(value, message):
    if not value:
        raise ValueError(message)


def verify(live=False):
    policy = json.loads((ROOT / NS / 'landing.json').read_text())
    for path, digest in policy['files_sha256'].items():
        require(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, 'Landing source drift: ' + path)
    body = (ROOT / '.github/README.md').read_text()
    require(body == (ROOT / NS / 'Repository.md').read_text(), 'Live README differs from reviewed landing')
    require(policy['source_commit'] == SOURCE and policy['release'] == 'v0.3.6', 'Wrong source release')
    require(policy['scope'] == 'LANDING_ONLY_WIKI_PAGES_PENDING', 'Unverified channel completion')
    for label in ('Start with your task', 'What v0.3.6 adds', 'Artifacts and versions',
                  'Current status and next work', 'Evidence, citation and reuse'):
        require('## ' + label in body, 'Missing reader route: ' + label)
    require('Wiki and Pages still serve documentation 0.4.2' in body, 'Missing live channel boundary')
    prior_count = 0
    for tag, expected_count in [('v0.3.5', 687), ('v0.3.6', 780)]:
        path = 'releases/selection-' + tag + '.json'
        data = (ROOT / path).read_bytes()
        require(data == subprocess.check_output(['git', 'show', SOURCE + ':' + path], cwd=ROOT),
                'Published component selection changed')
        bindings = json.loads(data)['selected_files_sha256']
        require(len(bindings) == expected_count, 'Published selection population changed')
        for name, digest in bindings.items():
            if name == '.github/README.md':
                require(tag == 'v0.3.6' and hashlib.sha256((ROOT / 'documentation/0.4.1/Repository.md').read_bytes()).hexdigest() == digest,
                        'Previous landing no longer preserved')
                continue
            require(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, 'Versioned source changed: ' + name)
        if tag == 'v0.3.6':
            prior_count = len(bindings) - 1
    publication = json.loads((ROOT / NS / 'publication.json').read_text())
    require(publication['id'] == 428331704 and publication['source'] == SOURCE
            and publication['exactly_six_uploaded_assets'] and publication['public_archive_no_git_passed']
            and publication['no_authorization_header'] and len(publication['assets']) == 6,
            'Missing actual v0.3.6 publication evidence')
    urls = sorted({a['href'] for a in BeautifulSoup(markdown.markdown(body, extensions=['tables']),
                                                 'html.parser').find_all('a', href=True)})
    for url in urls:
        require(urlsplit(url).scheme == 'https', 'Unsafe landing link')
        if url.startswith(REPO + '/blob/') or url.startswith(REPO + '/tree/'):
            ref, path = url.removeprefix(REPO + '/').split('/', 1)[1].split('/', 1)
            path = unquote(urlsplit(path).path)
            if ref == 'main':
                require((ROOT / path).is_file(), 'Missing current source link: ' + path)
            else:
                require(ref == SOURCE, 'Unpinned released source link')
                subprocess.run(['git', 'cat-file', '-e', ref + ':' + path], cwd=ROOT, check=True)
    checked = []
    if live:
        def fetch(url):
            with urlopen(Request(url, headers={'User-Agent': 'riskium-landing-link-review'}), timeout=45) as response:
                require(response.status == 200, 'Broken landing URL: ' + url)
                response.read()
                return dict(url=url, final_url=response.url, status=response.status)
        with ThreadPoolExecutor(max_workers=6) as pool:
            checked = list(pool.map(fetch, urls))
    return dict(status='REPOSITORY_LANDING_PASS', release='v0.3.6', source_commit=SOURCE,
                links=len(urls), live_links=checked, preserved_v035_files=687,
                preserved_other_v036_files=prior_count, mutable_entrypoint='.github/README.md',
                wiki_pages='0.4.2_PREPUBLICATION_CHECKPOINT_PENDING_63', next_proposed_release='v0.3.7')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live-links', action='store_true')
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    result = verify(args.live_links)
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'live_links'}))
