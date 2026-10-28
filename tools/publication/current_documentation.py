"""Project reviewed documentation 0.4.0 without rewriting older components."""
import argparse
import hashlib
import html
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile
import tempfile
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup
import markdown

import build_publication_status as predecessor
from audit_versioned_site import audit
from presentation import render
from site_registry import file_map

ROOT = Path(__file__).resolve().parents[2]
NAMESPACE = 'documentation/0.4.0'
COMPONENT = 'evaluation/documentation/current-0.4.0/component.json'
REPO = 'https://github.com/ArazSaieArasi3/riskium'
SITE = 'https://arazsaiearasi3.github.io/riskium'
SOURCES = ['tools/publication/current_documentation.py', 'tests/test_current_documentation.py',
           '.github/workflows/current-documentation.yml', '.github/workflows/current-documentation-pages.yml',
           NAMESPACE + '/guide-registry.json', NAMESPACE + '/policy.json', NAMESPACE + '/selection.json',
           NAMESPACE + '/README.md', 'evaluation/consistency/current-0.3.0/component.json',
           'evaluation/consistency/current-0.3.0/report.json', 'implementation/relational/0.7.0/component.json',
           'evaluation/releases/v0.3.4-publication.json', 'releases/distribution-v0.3.4.json']


def require(value, message):
    if not value:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encode(value):
    return json.dumps(value, indent=2, ensure_ascii=False) + '\n'


def read_bytes(root, path):
    return (root / path).read_bytes()


def validate_registry(rows):
    require(len(rows) == 21, 'Lost current guide')
    for key in ('slug', 'wiki_slug', 'source'):
        require(len({r[key] for r in rows}) == len(rows), 'Duplicate guide ' + key)
    for row in rows:
        require(all(re.fullmatch(r'[A-Za-z][A-Za-z0-9-]*', row[k]) for k in ('slug', 'wiki_slug')), 'Unsafe guide slug')
        require(row['source'] == NAMESPACE + '/guides/' + row['slug'] + '.md', 'Guide source escapes reviewed namespace')


def reject_stale(text):
    for pattern in [r'v0\.3\.4 is planned', r'v0\.3\.4 preparation', r'v0\.3\.4 is planned, not frozen',
                    r'(?:latest source distribution|published source distribution) is[^\n]*v0\.3\.[123](?:[^0-9]|$)',
                    r'Next publication #45', r'current documentation component is \*\*0\.3\.0']:
        require(not re.search(pattern, text, re.I), 'Stale active publication prose: ' + pattern)


def review(root=ROOT):
    policy = json.loads(read_bytes(root, NAMESPACE + '/policy.json'))
    selection = json.loads(read_bytes(root, NAMESPACE + '/selection.json'))
    rows = json.loads(read_bytes(root, NAMESPACE + '/guide-registry.json'))['guides']
    validate_registry(rows)
    require(policy['documentation_version'] == selection['documentation_version'] == '0.4.0', 'Wrong documentation version')
    require(policy['model_version'] == '0.3.1' and policy['published_distribution'] == 'v0.3.4' and policy['target_distribution'] == 'v0.3.5', 'Unreviewed version pair')
    source = selection['guide_source_commit']
    require(re.fullmatch(r'[a-f0-9]{40}', source), 'An exact reviewed guide source is required')
    archive = subprocess.check_output(['git', 'archive', source, NAMESPACE], cwd=root)
    with tarfile.open(fileobj=io.BytesIO(archive)) as saved:
        reviewed = {m.name: saved.extractfile(m).read() for m in saved if m.isfile()}
    require(set(policy['guide_sources_sha256']) == {r['source'] for r in rows}, 'Lost reviewed guide binding')
    for path, expected in policy['guide_sources_sha256'].items():
        data = read_bytes(root, path)
        require(sha(data) == expected and data == reviewed[path], 'Changed reviewed guide: ' + path)
        reject_stale(data.decode())
    for path in (NAMESPACE + '/policy.json', NAMESPACE + '/guide-registry.json'):
        require(read_bytes(root, path) == reviewed[path], 'Changed reviewed guide policy/registry')
    matrix = json.loads(read_bytes(root, policy['preserve_published_matrix']))
    require(len(matrix['selected_files_sha256']) == 380, 'Published selection population changed')
    for path, expected in matrix['selected_files_sha256'].items():
        require(sha(read_bytes(root, path)) == expected, 'Prior selected file changed: ' + path)
    return policy, selection, rows


def internal_link(url, rows, wiki=False):
    parsed = urlsplit(url)
    if not url or parsed.scheme or url.startswith(('#', '//')):
        return url
    require('/' not in parsed.path and parsed.path.endswith('.md'), 'Unregistered current guide link: ' + url)
    name = unquote(parsed.path).removesuffix('.md')
    by_slug = {r['slug']: r for r in rows}
    require(name in by_slug, 'Missing current guide destination: ' + url)
    path = by_slug[name]['wiki_slug'] if wiki else name + '.html'
    return path + ('?' + parsed.query if parsed.query else '') + ('#' + parsed.fragment if parsed.fragment else '')


def guide_html(row, rows, root=ROOT):
    body = markdown.markdown(read_bytes(root, row['source']).decode(), extensions=['tables', 'fenced_code', 'toc', 'md_in_html'])
    soup = BeautifulSoup(body, 'html.parser')
    for anchor in soup.find_all('a', href=True):
        anchor['href'] = internal_link(anchor['href'], rows)
    return str(soup)


def wiki_outputs(rows, selection, root=ROOT):
    result = {}
    for row in rows:
        text = read_bytes(root, row['source']).decode()
        text = re.sub(r'(!?\[[^\]\n]*\])\(([^\s)]+)\)', lambda m: m[1] + '(' + internal_link(m[2], rows, wiki=True) + ')', text)
        text += ('\n\n---\n\nDocumentation **0.4.0** · Model **0.3.1** · [Published source v0.3.4](' + REPO + '/releases/tag/v0.3.4)'
                 ' · [Target v0.3.5](' + REPO + '/issues/51) · [Equivalent Pages guide](' + SITE + '/current/guide/' + row['slug'] + '.html).\n\n'
                 'Reviewed explanatory source: [' + row['source'] + '](' + REPO + '/blob/' + selection['guide_source_commit'] + '/' + row['source'] + '). '
                 'Source SHA-256: `' + sha(read_bytes(root, row['source'])) + '`. Actual channel/source closure: [#55](' + REPO + '/issues/55).\n')
        result[row['wiki_slug'] + '.md'] = text
    result['_Sidebar.md'] = '# Riskium\n\nDocumentation **0.4.0** · Model **0.3.1**\n\n' + '\n'.join('- [' + r['title'] + '](' + r['wiki_slug'] + ')' for r in rows) + '\n'
    result['_Footer.md'] = ('Documentation **0.4.0** · [Pages](' + SITE + '/current/index.html) · [Versions](' + SITE + '/versions/index.html)'
                          ' · [Source v0.3.4](' + REPO + '/releases/tag/v0.3.4) · [Target v0.3.5](' + REPO + '/issues/51) · [Limits](Limitations)\n')
    require(len(result) == 23, 'Unexpected Wiki projection population')
    return result


def context(soup):
    return BeautifulSoup('<div class="publication-context"><span>Current documentation <strong>0.4.0</strong> · Model <strong>0.3.1</strong></span><span>'
                        '<a href="' + REPO + '/releases/tag/v0.3.4">v0.3.4 published</a> · <a href="' + REPO + '/releases/latest">Latest published</a> · '
                        '<a href="' + REPO + '/issues/51">v0.3.5 preparation</a></span></div>', 'html.parser').div


def check_header(soup):
    header = soup.select_one('div.publication-context')
    require(header is not None and '0.4.0' in header.get_text(), 'Wrong current documentation header')
    require(header.select_one('a[href="' + REPO + '/releases/tag/v0.3.4"]') is not None, 'Missing published source identity')
    require(header.select_one('a[href="' + REPO + '/issues/51"]') is not None, 'Missing target source identity')
    require(not header.select('a[href$="/issues/45"]'), 'Stale maintained release destination')


def build(output, root=ROOT):
    policy, selection, rows = review(root)
    manifest, old_status = predecessor.build(output, root=root)
    original_manifest_sha = sha((output / 'publication-manifest.json').read_bytes())
    for row in rows:
        path = Path('current/guide/' + row['slug'] + '.html')
        body = guide_html(row, rows, root)
        body += '<p class="meta">Documentation 0.4.0 · <a href="' + REPO + '/blob/' + selection['guide_source_commit'] + '/' + row['source'] + '">Reviewed explanatory source</a> · Source SHA-256: <code>' + policy['guide_sources_sha256'][row['source']] + '</code> · <a href="' + REPO + '/wiki/' + row['wiki_slug'] + '">Equivalent native Wiki</a>.</p>'
        (output / path).write_text(render(path, row['title'], body))
    home = next(r for r in rows if r['slug'] == 'Home')
    soup = BeautifulSoup(guide_html(home, rows, root), 'html.parser')
    for a in soup.find_all('a', href=True):
        if not urlsplit(a['href']).scheme and not a['href'].startswith('#'):
            a['href'] = 'guide/' + a['href']
    (output / 'current/index.html').write_text(render(Path('current/index.html'), 'Riskium documentation', str(soup)))
    versions = '<h1>Documentation versions</h1><p>Current documentation <strong>0.4.0</strong> explains model <strong>0.3.1</strong>. Published source is <a href="' + REPO + '/releases/tag/v0.3.4">v0.3.4</a>; target <a href="' + REPO + '/issues/51">v0.3.5</a> is in preparation. These source versions are distinct from documentation and model identities.</p><h2>Frozen documentation snapshots</h2><ul>'
    for label, row in manifest['releases'].items():
        versions += '<li><a href="../' + html.escape(row['route']) + '/index.html">' + html.escape(label) + '</a> · documentation ' + html.escape(row['documentation_version']) + ' · model ' + html.escape(row['model_version']) + ' · source <a href="' + REPO + '/commit/' + row['source_commit'] + '">' + row['source_commit'][:12] + '</a></li>'
    versions += '</ul><p>All four frozen snapshots retain their original bytes and dated claims. Current documentation 0.3.0 source files remain preserved separately from this successor.</p><p><a href="../current/index.html">Return to current documentation</a></p>'
    (output / 'versions/index.html').write_text(render(Path('versions/index.html'), 'Documentation versions', versions))
    maintained = sorted((output / 'current').rglob('*.html')) + [output / 'versions/index.html']
    require(len(maintained) == 31, 'Maintained HTML population changed')
    for path in maintained:
        soup = BeautifulSoup(path.read_text(), 'html.parser')
        header = soup.select_one('div.publication-context')
        require(header is not None, 'Missing maintained context: ' + str(path))
        header.replace_with(context(soup))
        check_header(soup)
        path.write_text(str(soup) + '\n')
    current_manifest = json.loads((output / 'current/publication-manifest.json').read_text())
    current_manifest.update(documentation_version='0.4.0', guide_source_commit=selection['guide_source_commit'],
                            guide_registry_sha256=sha(read_bytes(root, NAMESPACE + '/guide-registry.json')),
                            guide_sources_sha256=policy['guide_sources_sha256'],
                            publication_checkpoint={'tag': 'v0.3.4', 'source_commit': policy['published_source']},
                            release_routing={'published': REPO + '/releases/tag/v0.3.4', 'latest': REPO + '/releases/latest', 'target': REPO + '/issues/51'},
                            documentation_note='Current 0.4.0 explanation; old sources/snapshots preserved. Exact native Wiki/HTTP closure recorded under #55; no v0.3.5 publication.')
    (output / 'current/publication-manifest.json').write_text(encode(current_manifest))
    tool_path = output / 'current/widoco/tool-provenance.json'
    provenance = json.loads(tool_path.read_text())
    original_provenance = tool_path.read_bytes()
    provenance['maintained_documentation_projection'] = {'documentation_version': '0.4.0', 'guide_source_commit': selection['guide_source_commit'],
         'original_tool_provenance_sha256': sha(original_provenance), 'original_output_sha256': provenance['files_sha256'],
         'scope': 'Shared current navigation/context only. Original generator, semantic graph and serialization receipts retain their original roles.'}
    provenance['files_sha256'] = {p: sha(b) for p, b in file_map(tool_path.parent).items() if p != 'tool-provenance.json'}
    tool_path.write_text(encode(provenance))
    wiki = wiki_outputs(rows, selection, root)
    descriptor = dict(schema='riskium-current-documentation-component-v2', id='DOCUMENTATION', version='0.4.0', compatible_model='0.3.1',
         execution_issue=55, release_issue=51, guide_source_commit=selection['guide_source_commit'], published_source_release='v0.3.4', proposed_distribution='v0.3.5',
         shared_guides=21, native_wiki_files=23, maintained_html_pages=31, frozen_snapshots=4,
         current_files_sha256={p: sha(b) for p, b in file_map(output / 'current').items()},
         versions_index_sha256=sha((output / 'versions/index.html').read_bytes()),
         wiki_files_sha256={p: sha(t.encode()) for p, t in wiki.items()},
         files_sha256={p: sha(read_bytes(root, p)) for p in sorted(set(SOURCES) | set(policy['guide_sources_sha256']))},
         scope='Reviewed shared current guide bodies and projection; actual Wiki Git/HTTP closure remains separate evidence in #55.',
         prior_published_file_bindings_preserved=380, semantic_or_scientific_changes=False, independent_acceptance_claimed=False, new_source_distribution_published=False)
    manifest.update(current_documentation_version='0.4.0', current_documentation_projection={
         'component': COMPONENT, 'documentation_version': '0.4.0', 'guide_source_commit': selection['guide_source_commit'],
         'component_sha256': sha(encode(descriptor).encode()), 'renderer_sha256': descriptor['files_sha256'][SOURCES[0]],
         'predecessor_deployment_manifest_sha256': original_manifest_sha, 'published_source_release': 'v0.3.4', 'target_source_release': 'v0.3.5',
         'scope': 'Current bodies/navigation only; all four frozen snapshots and prior source assets preserved.'})
    manifest['files_sha256'] = {p: sha(b) for p, b in file_map(output).items() if p != 'publication-manifest.json'}
    (output / 'publication-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    result = audit(output)
    return descriptor, wiki, result


def checked_component(descriptor, root=ROOT):
    require(json.loads(read_bytes(root, COMPONENT)) == descriptor, 'Stale documentation 0.4.0 component')


def check_wiki_sources(wiki, root=ROOT):
    folder = root / NAMESPACE / 'wiki'
    require({p.name for p in folder.glob('*.md')} == set(wiki), 'Wiki source inventory differs')
    for name, value in wiki.items():
        require((folder / name).read_text() == value, 'Stale generated Wiki source: ' + name)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--write-component', action='store_true')
    mode.add_argument('--output', type=Path)
    p.add_argument('--wiki-output', type=Path)
    args = p.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        output = args.output or Path(tmp) / 'site'
        descriptor, wiki, result = build(output)
        if args.write_component:
            for name, value in wiki.items():
                path = ROOT / NAMESPACE / 'wiki' / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(value)
            path = ROOT / COMPONENT
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(encode(descriptor))
        else:
            checked_component(descriptor)
            check_wiki_sources(wiki)
        if args.wiki_output:
            args.wiki_output.mkdir(parents=True, exist_ok=True)
            require(not ({x.name for x in args.wiki_output.iterdir()} - set(wiki)), 'Unregistered Wiki output would be lost')
            for name, value in wiki.items():
                (args.wiki_output / name).write_text(value)
    result.update(status='CURRENT_DOCUMENTATION_040_PASS', documentation='0.4.0', guides=21, wiki_files=23,
                  maintained_html_pages=31, prior_selected_file_bindings=380, new_source_release_published=False)
    print(json.dumps(result))


if __name__ == '__main__':
    main()
