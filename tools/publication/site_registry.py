"""Registered documentation snapshots: safe routes, exact inputs and immutable bytes."""
from pathlib import Path, PurePosixPath
import hashlib
import html
import io
import json
import posixpath
import re
import subprocess
import tarfile
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = 'tools/publication/pages-registry.json'
SEMANTIC_COMMIT = '8afe169968b5c1396c02834dbc499af691b894b4'
REPO = 'https://github.com/ArazSaieArasi3/riskium'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root)


def safe_path(value):
    p = PurePosixPath(value)
    if not value or p.is_absolute() or str(p) != value or '..' in p.parts or '\\' in value:
        raise ValueError('Unsafe publication path: ' + value)
    return p


def file_map(folder):
    out = {}
    for p in sorted(folder.rglob('*')):
        if p.is_symlink():
            raise ValueError('Publication symlink is forbidden: ' + str(p))
        if p.is_file():
            out[p.relative_to(folder).as_posix()] = p.read_bytes()
    return out


def tree_files(root, commit, path):
    if not re.fullmatch('[a-f0-9]{40}', commit):
        raise ValueError('Snapshot requires an exact commit')
    safe_path(path)
    payload = git(root, 'archive', commit, path)
    out = {}
    prefix = path + '/'
    with tarfile.open(fileobj=io.BytesIO(payload)) as archive:
        for member in archive.getmembers():
            safe_path(member.name)
            if member.isdir():
                continue
            if not member.isfile() or not member.name.startswith(prefix):
                raise ValueError('Unsafe snapshot member: ' + member.name)
            name = member.name.removeprefix(prefix)
            safe_path(name)
            out[name] = archive.extractfile(member).read()
    if not out:
        raise ValueError('Empty documentation source tree')
    return out


def freeze_files(inputs, label, source, documentation_version):
    """Presentation-only projection; internal references stay within the snapshot."""
    output = dict(inputs)
    route = 'releases/' + label
    for name, data in inputs.items():
        if not name.endswith('.html'):
            continue
        soup = BeautifulSoup(data.decode(), 'html.parser')
        for node in soup.find_all(['a', 'link', 'img', 'script']):
            attr = 'src' if node.name in ('img', 'script') else 'href'
            url = node.get(attr, '')
            parts = urlsplit(url)
            if not url or parts.scheme or url.startswith(('#', '//')):
                continue
            target = posixpath.normpath(posixpath.join('current', posixpath.dirname(name), unquote(parts.path)))
            if target.startswith('current/'):
                continue
            safe_path(target)
            rebased = posixpath.relpath(target, posixpath.join(route, posixpath.dirname(name)))
            node[attr] = rebased + ('?' + parts.query if parts.query else '') + ('#' + parts.fragment if parts.fragment else '')
        for node in soup.find_all('a', href=True):
            node['href'] = node['href'].replace(REPO + '/blob/main/', REPO + '/blob/' + source + '/').replace(REPO + '/tree/main/', REPO + '/tree/' + source + '/')
        banner = soup.new_tag('aside', attrs={'class': 'publication-context', 'aria-label': 'Frozen documentation identity'})
        banner.append(BeautifulSoup('Frozen documentation <strong>' + html.escape(documentation_version) + '</strong> for model v0.3.1 · <a href="' + REPO + '/commit/' + source + '">source ' + source[:12] + '</a> · <a href="' + posixpath.relpath('versions/index.html', posixpath.join(route, posixpath.dirname(name))) + '">Documentation versions</a>', 'html.parser'))
        soup.body.insert(0, banner)
        old = soup.select_one('div.publication-context')
        if old:
            old.clear()
            old.append('Frozen documentation ' + documentation_version + ' · published model v0.3.1 · explanatory source ' + source[:12])
        output[name] = (str(soup) + '\n').encode()
    manifest = json.loads(inputs['publication-manifest.json'])
    manifest['documentation_snapshot'] = dict(version=documentation_version, route=route, source_commit=source,
        policy='Frozen presentation/source-reference projection; no semantic changes or new scientific execution.')
    output['publication-manifest.json'] = (json.dumps(manifest, indent=2, sort_keys=True) + '\n').encode()
    tool_path = 'widoco/tool-provenance.json'
    tool = json.loads(inputs[tool_path])
    tool['frozen_presentation_projection'] = dict(source_commit=source, renderer='tools/publication/site_registry.py',
        original_tool_provenance_sha256=sha(inputs[tool_path]), original_output_hashes=tool['files_sha256'],
        note='Only documentation banners and source/root-relative navigation changed; original generator and graph receipts remain identifiable.')
    tool['files_sha256'] = {p.removeprefix('widoco/'): sha(b) for p, b in output.items() if p.startswith('widoco/') and p != tool_path}
    output[tool_path] = (json.dumps(tool, indent=2, sort_keys=True) + '\n').encode()
    return output


def read_registry(root=ROOT):
    value = json.loads((root / REGISTRY).read_text())
    if value['schema'] != 'riskium-documentation-routes-v1':
        raise ValueError('Unknown documentation registry')
    if value['current_route'] != 'current' or value['version_index'] != 'versions/index.html':
        raise ValueError('Unreviewed current/system route')
    seen = set()
    for label, row in value['releases'].items():
        if not re.fullmatch(r'v\d+\.\d+\.\d+(?:-rc\.[1-9]\d*)?', label) or row['route'] != 'releases/' + label:
            raise ValueError('Invalid or colliding snapshot route')
        safe_path(row['route'])
        if row['route'] in seen:
            raise ValueError('Duplicate snapshot route')
        seen.add(row['route'])
        for p in row['files_sha256']:
            safe_path(p)
    return value


def guard(previous, current):
    for key in ('schema', 'current_route', 'version_index'):
        if previous[key] != current[key]:
            raise ValueError('Publication system route changed')
    for label, row in previous['releases'].items():
        if current['releases'].get(label) != row:
            raise ValueError('Registered frozen snapshot cannot be replaced or removed: ' + label)


def check_registry(root=ROOT, previous_ref='HEAD'):
    value = read_registry(root)
    if previous_ref:
        previous = subprocess.run(['git', 'show', previous_ref + ':' + REGISTRY], cwd=root, capture_output=True)
        if previous.returncode == 0:
            guard(json.loads(previous.stdout), value)
    for label, row in value['releases'].items():
        actual_tree = git(root, 'rev-parse', row['source_commit'] + ':' + row['source_path']).decode().strip()
        if actual_tree != row['source_tree']:
            raise ValueError('Snapshot source tree mismatch: ' + label)
        inputs = tree_files(root, row['source_commit'], row['source_path'])
        expected = inputs if row['rendering'] == 'EXACT_SOURCE_COPY' else freeze_files(inputs, label, row['source_commit'], row['documentation_version']) if row['rendering'] == 'FROZEN_GUIDE_REFS_V1' else None
        if expected is None:
            raise ValueError('Unknown snapshot rendering policy')
        digests = {p: sha(b) for p, b in expected.items()}
        if digests != row['files_sha256']:
            raise ValueError('Snapshot registered output mismatch: ' + label)
        actual = file_map(root / 'docs' / row['route'])
        if {p: sha(b) for p, b in actual.items()} != digests:
            raise ValueError('Frozen documentation bytes changed: ' + label)
        semantic = json.loads(inputs['publication-manifest.json'])
        if semantic['semantic_source_commit'] != row['semantic_source_commit'] or semantic['model_version'] != row['model_version']:
            raise ValueError('Snapshot semantic identity mismatch: ' + label)
    return value


def write_version_index(docs, root=ROOT):
    value = read_registry(root)
    links = ''.join('<li><a href="../' + html.escape(row['route']) + '/index.html">' + html.escape(label) + '</a> · documentation ' + html.escape(row['documentation_version']) + ' · model ' + html.escape(row['model_version']) + ' · source <a href="' + REPO + '/commit/' + row['source_commit'] + '">' + row['source_commit'][:12] + '</a></li>' for label, row in value['releases'].items())
    try:
        from .presentation import render
    except ImportError:
        from presentation import render
    body = '<h1>Documentation versions</h1><p>Use the current documentation for the maintained reading experience. Frozen snapshots preserve the pages as recorded at their declared source; their older layout is part of that historical record.</p><h2>Current model and source distribution</h2><p>Ontology model <strong>0.3.1</strong> is unchanged. The latest source distribution is <a href="'+REPO+'/releases/tag/v0.3.2">v0.3.2</a>, including separately versioned engineering and documentation components. <a href="../current/guide/Publication.html">Read the version policy</a>.</p><h2>Frozen documentation snapshots</h2><ul>'+links+'</ul><p>The legacy rc.1 route preserves the website as observed on 24 October 2026. It does not imply that earlier explanatory guides had always been immutable.</p><p><a href="../current/index.html">Return to current documentation</a></p>'
    page = render(Path('versions/index.html'), 'Documentation versions', body)
    (docs / 'versions').mkdir(parents=True, exist_ok=True)
    (docs / 'versions/index.html').write_text(page)
