"""Maintain readable documentation for published v0.3.5 without changing its inputs."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import html
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from urllib.parse import quote, unquote, urlsplit
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
import markdown

import current_documentation as predecessor
from audit_versioned_site import audit
from presentation import GROUPS, render
from site_registry import file_map, safe_path

ROOT = Path(__file__).resolve().parents[2]
NS = 'documentation/0.4.1'
VERSION = '0.4.1'
SOURCE = '8a9a95bba17327d04c5560879819b2e61b48ff19'
REPO = 'https://github.com/ArazSaieArasi3/riskium'
SITE = 'https://arazsaiearasi3.github.io/riskium'
TAG = 'v0.3.5'
RELEASE_ID = 427544469
PUBLICATION_SHA = '72e38e4f10bed8cbeb7c97a3f0c7006a4c7dc4edaae206090558496b8f8e6924'
ASSETS = {'SHA256SUMS.txt', 'artifact-versions.json', 'freeze-receipt.json',
          'release-notes.md', 'riskium-v0.3.5-source.tar.gz', 'source-manifest.json'}
ALLOWED_ADDITIONS = (NS + '/', 'evaluation/documentation/published-v0.3.5/')
ALLOWED_FILES = {'.github/README.md', '.github/workflows/published-documentation.yml',
                 'tools/publication/published_documentation.py', 'tests/test_published_documentation.py'}
INVENTORY = 'evaluation/consistency/inventory.json'


def require(value, message):
    if not value:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encode(value):
    return json.dumps(value, indent=2, ensure_ascii=False) + '\n'


def read(root, path):
    safe_path(path)
    target = root / path
    require(target.resolve().is_relative_to(root.resolve()) and not target.is_symlink(), 'Unsafe reader source')
    return target.read_bytes()


def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root).decode().strip()


def preserved_inputs(root=ROOT):
    """Maintenance may add its namespace, never alter selected release payloads."""
    matrix = json.loads(read(root, 'releases/selection-v0.3.5.json'))
    hashes = matrix['selected_files_sha256']
    require(len(hashes) == 687, 'Selected release population changed')
    for path, expected in hashes.items():
        require(sha(read(root, path)) == expected, 'Published input changed: ' + path)
    changed = git(root, 'diff', '--name-only', SOURCE, '--').splitlines()
    added = git(root, 'ls-files', '--others', '--exclude-standard').splitlines()
    source_paths = set(git(root, 'ls-tree', '-r', '--name-only', SOURCE).splitlines())
    for path in set(changed + added):
        if path == INVENTORY:
            continue
        require(path not in source_paths and
                (path in ALLOWED_FILES or path.startswith(ALLOWED_ADDITIONS)),
                'Outside additive documentation scope: ' + path)
    return len(hashes)


def review(root=ROOT):
    policy = json.loads(read(root, NS + '/policy.json'))
    registry = json.loads(read(root, NS + '/guide-registry.json'))
    rows = registry['guides']
    require(policy['documentation_version'] == registry['documentation_version'] == VERSION,
            'Wrong maintained documentation version')
    require((policy['source_release'], policy['source_commit'], policy['model_version'], policy['issue'])
            == (TAG, SOURCE, '0.3.1', 60), 'Wrong published source identity')
    require(len(rows) == 21, 'Missing reader guide')
    for key in ('slug', 'wiki_slug', 'source'):
        require(len({row[key] for row in rows}) == 21, 'Duplicate guide ' + key)
    old_rows = json.loads(read(root, 'documentation/0.4.0/guide-registry.json'))['guides']
    require([(r['slug'], r['wiki_slug'], r['title']) for r in rows]
            == [(r['slug'], r['wiki_slug'], r['title']) for r in old_rows], 'Guide identity changed')
    for row in rows:
        require(re.fullmatch(r'[A-Za-z][A-Za-z0-9-]*', row['slug'])
                and row['source'] == NS + '/guides/' + row['slug'] + '.md', 'Unsafe guide registry')
    expected_paths = {r['source'] for r in rows} | {NS + '/' + n for n in
        ('guide-registry.json', 'Repository.md', 'publication.json', 'reader.css', 'review-plan.json')}
    require(set(policy['files_sha256']) == expected_paths, 'Reader binding set changed')
    for path, expected in policy['files_sha256'].items():
        require(sha(read(root, path)) == expected, 'Changed reviewed reader source: ' + path)
    require(read(root, '.github/README.md') == read(root, NS + '/Repository.md'), 'Active README drift')
    require(sha(read(root, NS + '/publication.json')) == PUBLICATION_SHA, 'Publication record drift')
    publication = json.loads(read(root, NS + '/publication.json'))
    require(publication['status'] == 'INDEPENDENT_ACTUAL_PUBLIC_SIX_DOWNLOAD_PASS'
            and publication['source_commit'] == SOURCE and publication['release_id'] == RELEASE_ID
            and publication['tag'] == TAG and len(publication['assets']) == 6
            and {a['name'] for a in publication['assets']} == ASSETS
            and publication['all_public_bodies_equal_independently_verified_freeze'] is True
            and publication['independent_semantic_validation'] is False, 'Unverified publication record')
    plan = json.loads(read(root, NS + '/review-plan.json'))
    require(set(plan['audience_paths']) == {'reviewer', 'domain', 'integrator'}
            and len(plan['qualitative_criteria']) == 10, 'Missing declared reader review')
    for journey in plan['audience_paths'].values():
        require(journey[0] == 'Home' and set(journey) <= {r['slug'] for r in rows}, 'Broken audience path')
    preserved_inputs(root)
    return rows, policy, publication


def rewrite_link(url, rows, page, wiki=False):
    parts = urlsplit(url)
    if not url or url.startswith(('#', '//')):
        return url
    if url.startswith(SITE + '/') and not wiki:
        target = unquote(parts.path).removeprefix('/riskium/')
        require(not target.startswith('/') and target != parts.path, 'Unexpected site route')
        result = os.path.relpath(target, Path(page).parent).replace(os.sep, '/')
        return result + ('?' + parts.query if parts.query else '') + ('#' + parts.fragment if parts.fragment else '')
    if parts.scheme:
        return url
    require('/' not in parts.path and parts.path.endswith('.md'), 'Unregistered reader link: ' + url)
    name = unquote(parts.path).removesuffix('.md')
    registered = {r['slug']: r for r in rows}
    require(name in registered, 'Missing reader destination: ' + url)
    target = registered[name]['wiki_slug'] if wiki else os.path.relpath(
        'current/guide/' + name + '.html', Path(page).parent).replace(os.sep, '/')
    return target + ('?' + parts.query if parts.query else '') + ('#' + parts.fragment if parts.fragment else '')


def source_record(row, source, root=ROOT):
    return ('<details class="source-record"><summary>Sources and publication record</summary><p>'
            '<a href="' + REPO + '/blob/' + source + '/' + row['source'] + '">Explanatory source</a> · '
            '<a href="' + REPO + '/wiki/' + row['wiki_slug'] + '">Equivalent Wiki guide</a> · '
            '<a href="' + REPO + '/releases/tag/' + TAG + '">Published source v0.3.5</a>.</p><p>'
            'Documentation ' + VERSION + ' · model 0.3.1. Guide SHA-256: <code>' +
            sha(read(root, row['source'])) + '</code>. <a href="' + REPO +
            '/issues/60">Documentation review and channel verification</a>.</p></details>')


def guide_html(row, rows, page, source, root=ROOT):
    body = markdown.markdown(read(root, row['source']).decode(), extensions=['tables', 'fenced_code', 'toc', 'md_in_html'])
    soup = BeautifulSoup(body, 'html.parser')
    for anchor in soup.find_all('a', href=True):
        anchor['href'] = rewrite_link(anchor['href'], rows, page)
    return str(soup) + source_record(row, source, root)


def wiki_outputs(rows, source, root=ROOT):
    result = {}
    for row in rows:
        text = read(root, row['source']).decode()
        text = re.sub(r'(!?\[[^\]\n]*\])\(([^\s)]+)\)',
                      lambda m: m[1] + '(' + rewrite_link(m[2], rows, '', wiki=True) + ')', text)
        text += ('\n<details>\n<summary>Sources and publication record</summary>\n\n'
                 '[Explanatory source](' + REPO + '/blob/' + source + '/' + row['source'] + ') · '
                 '[Equivalent Pages guide](' + SITE + '/current/guide/' + row['slug'] + '.html) · '
                 '[Published source v0.3.5](' + REPO + '/releases/tag/v0.3.5).\n\n'
                 'Documentation **0.4.1** · Model **0.3.1**. Guide SHA-256: `' + sha(read(root, row['source'])) +
                 '`. [Documentation review and verification](' + REPO + '/issues/60).\n\n</details>\n')
        result[row['wiki_slug'] + '.md'] = text
    by_slug = {r['slug']: r for r in rows}
    sidebar = '**Riskium**\n\n[Home](Home) · [Published v0.3.5](' + REPO + '/releases/tag/v0.3.5)\n\n'
    for group, slugs in GROUPS.items():
        sidebar += '### ' + group + '\n\n' + '\n'.join('- [' + by_slug[s]['title'] + '](' +
                    by_slug[s]['wiki_slug'] + ')' for s in slugs) + '\n\n'
    sidebar += '### Reference tools\n\n[Find a term](' + SITE + '/current/reference/search.html) · '
    sidebar += '[Formal reference](' + SITE + '/current/widoco/index-en.html) · [Versions](' + SITE + '/versions/index.html)\n'
    result['_Sidebar.md'] = sidebar
    result['_Footer.md'] = ('Documentation **0.4.1** · Model **0.3.1** · [Source v0.3.5](' + REPO +
                            '/releases/tag/v0.3.5) · [Pages](' + SITE + '/current/index.html) · '
                            '[Citation](Citation) · [Limitations](Limitations)\n')
    require(len(result) == 23, 'Unexpected Wiki file population')
    return result


def published_context():
    return BeautifulSoup('<div class="publication-context"><span>Documentation <strong>0.4.1</strong> · '
        'Model <strong>0.3.1</strong></span><span><a href="' + REPO + '/releases/tag/v0.3.5">v0.3.5 published</a>'
        ' · <a href="' + REPO + '/releases/latest">Latest release</a></span></div>', 'html.parser').div


def downloads(publication):
    text = '# Downloads\n\n## Published source package\n\n'
    text += '[v0.3.5](' + publication['release_url'] + ') contains the selected research and engineering artifacts. '
    text += 'Download the six assets together and verify the five payload checksums before extracting the archive.\n\n'
    for asset in publication['assets']:
        text += '- [' + asset['name'] + '](' + asset['url'] + ')\n'
    text += '\nThe freeze receipt describes the phase before publication. [The publication record](' + REPO + '/issues/59) '
    text += 'supplies the later independent public-download verification. [Reproduction](../guide/Reproduce.html) gives commands and expected results.\n\n'
    text += '## Model and license files\n\nThe files below retain the unchanged model 0.3.1 semantic source. '
    text += 'Website checksums cover this website subset; they do not replace the source-release checksums above.\n\n'
    for name in ('riskium-model.json', 'riskium.ontouml.json', 'typed-core.json', 'RIGHTS.md', 'LICENSE', 'NOTICE.md', 'CC-BY-4.0.txt', 'MIT.txt'):
        text += '- [' + name + '](' + name + ')\n'
    text += '\n[Website subset checksums](SHA256SUMS.txt). OWL: [Turtle](../widoco/ontology.ttl) · '
    text += '[RDF/XML](../widoco/ontology.owl) · [JSON-LD](../widoco/ontology.jsonld) · [N-Triples](../widoco/ontology.nt).\n\n'
    text += '## Citation and reuse\n\nThe downloadable [CITATION.cff](CITATION.cff) is the historical model-release copy. '
    text += 'For the current artifact citation, identify **source v0.3.5** separately from **model 0.3.1**. '
    text += '[Citation and attribution](../guide/Citation.html) explains the authors, exact-version practice and licenses.\n'
    return markdown.markdown(text, extensions=['tables', 'toc'])


def build(output, root=ROOT):
    rows, policy, publication = review(root)
    _, _, _ = predecessor.build(output, root=root)
    old_manifest = json.loads((output / 'publication-manifest.json').read_text())
    old_manifest_sha = sha((output / 'publication-manifest.json').read_bytes())
    source = git(root, 'rev-parse', 'HEAD')
    require(re.fullmatch('[a-f0-9]{40}', source), 'Missing documentation source commit')
    # Evidence-only follow-ups may advance main without rewriting all Wiki pages.
    # The explanatory sources keep the exact commit which last changed their namespace.
    guide_source = git(root, 'log', '-1', '--format=%H', '--', NS) or source
    for row in rows:
        page = 'current/guide/' + row['slug'] + '.html'
        (output / page).write_text(render(Path(page), row['title'], guide_html(row, rows, page, guide_source, root)))
    home = next(r for r in rows if r['slug'] == 'Home')
    page = 'current/index.html'
    (output / page).write_text(render(Path(page), 'Riskium documentation', guide_html(home, rows, page, guide_source, root)))
    (output / 'current/downloads/index.html').write_text(render(Path('current/downloads/index.html'), 'Downloads', downloads(publication)))
    versions = '<h1>Documentation versions</h1><p>Current documentation <strong>0.4.1</strong> explains model <strong>0.3.1</strong> and '
    versions += '<a href="' + publication['release_url'] + '">published source v0.3.5</a>. It is an editorial/status maintenance view; '
    versions += 'the release retains its documentation 0.4.0 sources. These version numbers describe different artifacts.</p>'
    versions += '<h2>Frozen documentation snapshots</h2><p>Each snapshot retains its original bytes, source and dated claims. '
    versions += 'A snapshot label does not identify the live Latest source release.</p><ul>'
    for label, entry in old_manifest['releases'].items():
        versions += '<li><a href="../' + html.escape(entry['route']) + '/index.html">' + html.escape(label) + '</a> · '
        versions += 'documentation ' + html.escape(entry['documentation_version']) + ' · model ' + html.escape(entry['model_version'])
        versions += ' · <a href="' + REPO + '/commit/' + entry['source_commit'] + '">exact source</a></li>'
    versions += '</ul><p><a href="../current/guide/Publication.html">Release and citation guide</a> · <a href="../current/index.html">Current documentation</a></p>'
    (output / 'versions/index.html').write_text(render(Path('versions/index.html'), 'Documentation versions', versions))
    (output / 'current/assets/reader.css').write_bytes(read(root, NS + '/reader.css'))
    maintained = sorted((output / 'current').rglob('*.html')) + [output / 'versions/index.html']
    require(len(maintained) == 31, 'Maintained HTML scope changed')
    for path in maintained:
        soup = BeautifulSoup(path.read_text(), 'html.parser')
        header = soup.select_one('div.publication-context')
        require(header is not None, 'Missing current context: ' + str(path))
        header.replace_with(published_context())
        css = os.path.relpath(output / 'current/assets/reader.css', path.parent).replace(os.sep, '/')
        soup.head.append(soup.new_tag('link', rel='stylesheet', href=css + '?v=' + sha(read(root, NS + '/reader.css'))[:12]))
        toc = soup.select_one('aside.toc')
        if toc is not None and not toc.select('a[href]'):
            toc.decompose()
        mobile = soup.select_one('details.mobile-navigation > div')
        if mobile is not None:
            for heading in mobile.find_all('h2', recursive=False):
                following = heading.find_next_sibling()
                if heading.get_text(strip=True) == 'On this page' and following is not None and not following.select('a[href]'):
                    following.decompose()
                    heading.decompose()
        for th in soup.select('th'):
            if not th.has_attr('scope'):
                th['scope'] = 'col'
        # Tables retain horizontal scrolling within their own region at narrow widths.
        for table in soup.select('main table'):
            table['tabindex'] = '0'
            table['aria-label'] = 'Scrollable ' + ((table.find_previous(['h1', 'h2']) or soup.title).get_text(' ', strip=True)) + ' table'
        path.write_text(str(soup) + '\n')
    wiki = wiki_outputs(rows, guide_source, root)
    status = dict(schema='riskium-published-reader-status-v1', documentation_version=VERSION, documentation_source_commit=source,
        guide_source_commit=guide_source, source_release=TAG, published_source_commit=SOURCE, release_id=RELEASE_ID, model_version='0.3.1',
        publication_receipt_sha256=PUBLICATION_SHA, native_wiki_files=23,
        wiki_files_sha256={n: sha(t.encode()) for n, t in wiki.items()},
        guide_sources_sha256={r['source']: sha(read(root, r['source'])) for r in rows},
        reader_review_plan=NS + '/review-plan.json', historical_selected_files_preserved=687,
        frozen_snapshots=4, new_source_distribution=False, independent_semantic_acceptance=False)
    (output / 'current/published-status.json').write_text(encode(status))
    current_manifest = json.loads((output / 'current/publication-manifest.json').read_text())
    current_manifest['semantic_release'] = current_manifest['release']
    current_manifest['release'] = TAG
    current_manifest['prior_documentation_projection'] = {k: current_manifest[k] for k in
        ('documentation_version', 'guide_source_commit', 'guide_sources_sha256', 'publication_checkpoint', 'release_routing', 'documentation_note')}
    current_manifest.update(documentation_version=VERSION, guide_source_commit=guide_source,
        guide_sources_sha256=status['guide_sources_sha256'], guide_registry_sha256=sha(read(root, NS + '/guide-registry.json')),
        publication_checkpoint={'tag': TAG, 'source_commit': SOURCE, 'release_id': RELEASE_ID},
        release_routing={'published': publication['release_url'], 'latest': REPO + '/releases/latest', 'target': None},
        documentation_note='Maintained 0.4.1 explanation of published v0.3.5; source inputs and four snapshots preserved.',
        published_status_projection=status)
    (output / 'current/publication-manifest.json').write_text(encode(current_manifest))
    provenance_path = output / 'current/widoco/tool-provenance.json'
    provenance = json.loads(provenance_path.read_text())
    provenance['prior_maintained_documentation_projection'] = provenance['maintained_documentation_projection']
    provenance['maintained_documentation_projection'] = dict(documentation_version=VERSION, documentation_source_commit=source,
        source_release=TAG, original_tool_and_semantic_sources_unchanged=True,
        scope='Current shell, reading/navigation/status and table accessibility only; generated entity commitments unchanged.')
    provenance['files_sha256'] = {p: sha(b) for p, b in file_map(provenance_path.parent).items() if p != 'tool-provenance.json'}
    provenance_path.write_text(encode(provenance))
    manifest = old_manifest
    manifest['prior_current_documentation_projection'] = manifest['current_documentation_projection']
    manifest['prior_publication_status_projection'] = manifest['publication_status_projection']
    manifest['historical_snapshot_preparation'] = manifest.pop('snapshot_preparation')
    manifest['publication_status_projection'] = dict(source_release=TAG, published_source_commit=SOURCE,
        release_id=RELEASE_ID, publication_receipt_sha256=PUBLICATION_SHA,
        documentation_version=VERSION, scope='Current published source identity; historical projections retained separately.')
    manifest.update(current_documentation_version=VERSION, current_documentation_projection=status,
        published_reader_projection=dict(source_release=TAG, published_source_commit=SOURCE,
            documentation_source_commit=source, release_id=RELEASE_ID,
            predecessor_deployment_manifest_sha256=old_manifest_sha,
            source_namespace=NS, prior_selected_files_preserved=687,
            active_repository_readme='.github/README.md', semantic_changes=False))
    manifest['files_sha256'] = {p: sha(b) for p, b in file_map(output).items() if p != 'publication-manifest.json'}
    (output / 'publication-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    result = audit(output)
    result.update(status='PUBLISHED_READER_DOCUMENTATION_PASS', documentation=VERSION, source_release=TAG,
                  shared_guides=21, wiki_files=23, preserved_selected_files=687, maintained_html_pages=31)
    return manifest, wiki, result


def api(path):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'riskium-documentation-verifier'}
    if os.environ.get('GH_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
    with urlopen(Request('https://api.github.com/repos/ArazSaieArasi3/riskium/' + path, headers=headers), timeout=40) as response:
        return json.load(response)


def verify_live_release(publication, source, getter=api):
    latest = getter('releases/latest')
    require((latest['tag_name'], latest['id'], latest['draft'], latest['prerelease']) == (TAG, RELEASE_ID, False, False),
            'Live published release identity changed')
    target = getter('git/ref/tags/' + TAG)['object']
    require(target == dict(sha=SOURCE, type='commit', url=target['url']), 'Published tag source changed')
    require(getter('git/ref/heads/main')['object']['sha'] == source, 'Documentation source is no longer main')
    require(len(latest['assets']) == 6, 'Live asset inventory changed')
    actual = {a['name']: (a['id'], a['size'], a['digest']) for a in latest['assets']}
    expected = {a['name']: (a['id'], a['size'], 'sha256:' + a['sha256']) for a in publication['assets']}
    require(actual == expected, 'Live public asset identity/digest changed')
    return dict(status='LIVE_PUBLISHED_SOURCE_IDENTITY_PASS', tag=TAG, release_id=RELEASE_ID,
                published_source_commit=SOURCE, documentation_source_commit=source, assets=6)


def verify_channels(output, wiki_folder, root=ROOT):
    manifest, wiki, _ = build(output, root)
    expected = manifest['files_sha256']
    paths = sorted(p for p in expected if p != '.nojekyll') + ['publication-manifest.json']
    def fetch(path):
        request = Request(SITE + '/' + quote(path, safe='/') + '?doc=' + manifest['current_source_commit'],
                          headers={'Cache-Control': 'no-cache', 'User-Agent': 'riskium-documentation-readback'})
        with urlopen(request, timeout=45) as response:
            data = response.read()
            require(response.status == 200 and data == (output / path).read_bytes(), 'Actual served byte drift: ' + path)
            return dict(path=path, bytes=len(data), sha256=sha(data), http_status=response.status)
    with ThreadPoolExecutor(max_workers=8) as pool:
        responses = list(pool.map(fetch, paths))
    actual_names = {p.name for p in wiki_folder.glob('*.md')}
    require(actual_names == set(wiki), 'Actual native Wiki inventory drift')
    for name, text in wiki.items():
        require((wiki_folder / name).read_bytes() == text.encode(), 'Actual native Wiki byte drift: ' + name)
    return dict(status='ACTUAL_PUBLISHED_READER_CHANNELS_PASS', checked_at_utc=datetime.now(timezone.utc).isoformat(),
        documentation_source_commit=manifest['current_source_commit'], source_release=TAG, published_source_commit=SOURCE,
        root_manifest_sha256=sha((output / 'publication-manifest.json').read_bytes()),
        wiki_commit=git(wiki_folder, 'rev-parse', 'HEAD'), wiki_files=23, pages_http_responses=len(responses),
        responses=responses, frozen_snapshots=4,
        wiki_files_sha256={n: sha(t.encode()) for n, t in wiki.items()},
        semantic_validation=False, user_study=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--wiki-output', type=Path)
    parser.add_argument('--live-release', action='store_true')
    parser.add_argument('--verify-channels', type=Path, metavar='ACTUAL_WIKI_CLONE')
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    if args.live_release or args.verify_channels:
        require(not git(ROOT, 'status', '--porcelain'), 'Live evidence requires a clean committed documentation source')
    with tempfile.TemporaryDirectory() as tmp:
        output = args.output or Path(tmp) / 'site'
        manifest, wiki, result = build(output)
        if args.live_release:
            result['live_release'] = verify_live_release(json.loads(read(ROOT, NS + '/publication.json')), manifest['current_source_commit'])
        if args.wiki_output:
            args.wiki_output.mkdir(parents=True, exist_ok=True)
            for name, text in wiki.items():
                (args.wiki_output / name).write_text(text)
        if args.verify_channels:
            result['actual_channels'] = verify_channels(output, args.verify_channels)
        if args.receipt:
            args.receipt.parent.mkdir(parents=True, exist_ok=True)
            args.receipt.write_text(encode(result))
        print(json.dumps(result))


if __name__ == '__main__':
    main()
