"""Compose the current reader and retained guides without publishing any channel."""
import argparse
import importlib.util
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urlsplit, unquote
import markdown
from bs4 import BeautifulSoup
import curation
import reader
import projection
import routing

ROOT = curation.ROOT
GUIDES = Path(__file__).parent / 'guides'
REPO, SITE = projection.REPO, projection.SITE
FEATURES = projection.FEATURES


def historical(root):
    root = Path(root).resolve()
    curation.need(not root.exists(), 'Historical destination already exists')
    subprocess.run(['git', 'worktree', 'add', '--detach', str(root), routing.HISTORICAL], cwd=ROOT, check=True, capture_output=True)
    spec = importlib.util.spec_from_file_location('riskium_v039_retained_delivery', root / 'tools/releases/v039/delivery/build_reader.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def route(slug):
    if slug == 'Concept-Index':
        return 'current/concepts/index.html'
    if slug in {'Subdomains', 'Relations', 'Generalizations', 'Constraints', 'Set-policy', 'External-Definitions', 'Curation-Status'} or slug.startswith(('RKM-', 'EXT-')):
        return 'current/concepts/' + slug + '.html'
    return 'current/guide/' + slug + '.html'


def build(out, source_ref, baseline_site, baseline_wiki, shell_module):
    out = Path(out).resolve()
    curation.need(not out.exists() and re.fullmatch(r'[a-zA-Z0-9._/-]+', source_ref), 'Empty destination/valid source ref required')
    bodies = reader.build(check=True)
    site, wiki = out / 'site', out / 'wiki'
    shutil.copytree(baseline_site, site)
    shutil.copytree(baseline_wiki, wiki)
    historical_wiki = {}
    for p in (Path(__file__).parent / 'wiki-history').glob('*.md'):
        shutil.copyfile(p, wiki / p.name)
        historical_wiki[p.name] = curation.sha(p.read_bytes())
    curation.need(historical_wiki == {'References.md': curation.load(ROOT / 'evaluation/releases/v0.3.9/channels.json')['wiki']['historical_reference_sha256']}, 'Historical native Wiki reference differs')
    frozen = {p.relative_to(site).as_posix(): curation.sha(p.read_bytes()) for p in sorted((site / 'releases').rglob('*')) if p.is_file()}
    old_guides = {p.name for p in Path(baseline_wiki).glob('*.md') if p.name not in {'_Sidebar.md', '_Footer.md'}
                  and not p.name.startswith(('RKM-', 'EXT-')) and p.stem not in {'Concept-Index', 'Subdomains', 'Relations', 'Generalizations', 'Constraints', 'Set-policy', 'External-Definitions'}}
    curation.need({p.name for p in GUIDES.glob('*.md')} == old_guides, 'A retained guide is missing')
    nav = [(g, list(items)) for g, items in shell_module.NAV]
    for _, items in nav:
        for i, (key, label) in enumerate(items):
            if key == 'External-Definitions':
                items[i] = (key, 'Current source comparisons')
    if not any(k == 'Curation-Status' for k, _ in nav[1][1]):
        nav[1][1].append(('Curation-Status', 'Curation and version status'))
    shell_module.NAV = nav
    shell_module.roles = lambda: 'Prepared package v0.3.10 · model 0.3.2 · documentary review 0.2.0 · reader 0.4.10'
    shell_module.page_route = route
    pairs = {}
    def emit(slug, text, source_path, base):
        target = site / route(slug)
        source_url = REPO + '/blob/' + source_ref + '/' + source_path
        def resolve(url, for_wiki=False):
            parsed = urlsplit(url)
            if parsed.scheme or url.startswith('//') or not parsed.path:
                return url
            frag = '#' + parsed.fragment if parsed.fragment else ''
            if parsed.path.endswith('.md') and '/' not in parsed.path:
                dest = 'Concept-Index' if parsed.path == 'README.md' else parsed.path[:-3]
                curation.need((reader.OUT / parsed.path).is_file() or (GUIDES / parsed.path).is_file(), 'Missing reader/guide source: ' + url)
                return (dest if for_wiki else SITE + '/' + route(dest)) + frag
            file = (base / unquote(parsed.path)).resolve()
            curation.need(file.is_relative_to(ROOT) and file.is_file(), 'Missing source route: ' + url)
            if file.parent == reader.OUT and file.suffix != '.md' and not for_wiki:
                return SITE + '/current/concepts/' + file.name + frag
            return REPO + '/blob/' + source_ref + '/' + file.relative_to(ROOT).as_posix() + frag
        doc = BeautifulSoup(markdown.markdown(text, extensions=FEATURES), 'html.parser')
        for node in doc.select('a[href], img[src]'):
            key = 'href' if node.has_attr('href') else 'src'
            node[key] = resolve(node[key])
        for th in doc.select('th'):
            th['scope'] = 'col'
        title = doc.h1.get_text(' ', strip=True) if doc.h1 else slug
        html = shell_module.shell(title, str(doc), slug, source_url)
        html = html.replace('>Published package</a>', '>Verified predecessor v0.3.9</a>')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html)
        wt = re.sub(r'\]\(([^)]+)\)', lambda m: '](' + resolve(m[1], True) + ')', text)
        (wiki / (slug + '.md')).write_text('<!-- BEGIN CURATION BODY -->\n' + wt.rstrip() + '\n<!-- END CURATION BODY -->\n\n---\n\n' + shell_module.roles() + ' · [Source](' + source_url + ') · [Equivalent Pages page](' + SITE + '/' + route(slug) + ') · [Wiki Home](Home) · [Repository](' + REPO + ')\n')
        pairs[slug] = {'html': route(slug), 'wiki': slug + '.md', 'source_path': source_path,
                       'source_sha256': curation.sha(text.encode()), 'plain_text_sha256': curation.sha(projection.plain(text).encode())}
    for name, text in bodies.items():
        if name.endswith('.md'):
            emit(projection.slug(name), text, (reader.OUT / name).relative_to(ROOT).as_posix(), reader.OUT)
        else:
            (site / 'current/concepts' / name).write_text(text)
    for file in sorted(GUIDES.glob('*.md')):
        emit(file.stem, file.read_text(), file.relative_to(ROOT).as_posix(), GUIDES)
    for name, source in [('current/index.html', 'current/guide/Home.html'), ('index.html', 'current/guide/Home.html'),
                         ('current/concepts/subdomains.html', 'current/concepts/Subdomains.html'),
                         ('current/downloads/index.html', 'current/guide/Publication.html')]:
        (site / name).write_bytes((site / source).read_bytes())
    (wiki / '_Sidebar.md').write_text('# Riskium\n\n' + ''.join('## ' + g + '\n\n' + ''.join('- [' + label + '](' + key + ')\n' for key, label in items) + '\n' for g, items in nav) + '[Repository](' + REPO + ') · [Pages](' + SITE + '/current/index.html) · [Verified predecessor](' + REPO + '/releases/tag/v0.3.9)\n')
    (wiki / '_Footer.md').write_text(shell_module.roles() + ' · [Home](Home) · [Concept index](Concept-Index) · [Repository](' + REPO + ') · [Pages](' + SITE + '/current/index.html)\n')
    status = {'schema': 'riskium-prepared-channel-0310/1', 'package': 'v0.3.10', 'source_commit': source_ref,
              'model_version': '0.3.2', 'curation_version': '0.2.0', 'reader_version': '0.4.10',
              'last_verified_release': 'v0.3.9', 'published': False, 'live_channel_readback': False,
              'wiki_files_sha256': {p.name: curation.sha(p.read_bytes()) for p in sorted(wiki.glob('*.md'))}}
    (site / 'current/published-status.json').write_text(curation.dump(status))
    version = site / 'releases/v0.3.10'
    curation.need(not version.exists(), 'Successor snapshot already exists')
    shutil.copytree(site / 'current', version)
    for file in version.rglob('*.html'):
        file.write_text(file.read_text().replace(SITE + '/current/', SITE + '/releases/v0.3.10/'))
    (site / 'versions/index.html').write_text(shell_module.shell('Documentation versions', '<h1>Documentation versions</h1><p>Prepared <a href="' + SITE + '/releases/v0.3.10/index.html">v0.3.10 reader 0.4.10</a> adds current documentary review 0.2.0 without changing model 0.3.2. Publication and actual readback remain a separate gate.</p><p><a href="' + SITE + '/releases/v0.3.9/index.html">Verified v0.3.9 snapshot</a> and all earlier snapshots retain their original bytes.</p>', 'Publication', REPO + '/blob/' + source_ref + '/tools/releases/v0310/compose.py'))
    curation.need(all(curation.sha((site / n).read_bytes()) == h for n, h in frozen.items()), 'Historical snapshot changed')
    (site / 'delivery-validation.json').unlink(missing_ok=True)
    (site / 'publication-manifest.json').unlink(missing_ok=True)
    manifest = {'schema': 'riskium-v0310-composed-candidate/1', 'source_ref': source_ref, 'package': 'v0.3.10',
                'baseline_commit': routing.HISTORICAL, 'reader_version': '0.4.10', 'curation_version': '0.2.0',
                'published': False, 'live_channel_readback': False, 'pairs': pairs, 'retained_guides': sorted(old_guides),
                'frozen_snapshot_sha256': frozen, 'historical_wiki_sha256': historical_wiki, 'files_sha256': {p.relative_to(site).as_posix(): curation.sha(p.read_bytes()) for p in sorted(site.rglob('*')) if p.is_file()},
                'wiki_files_sha256': status['wiki_files_sha256']}
    (site / 'publication-manifest.json').write_text(curation.dump(manifest))
    return audit(out)


def audit(out):
    out = Path(out).resolve()
    site, wiki = out / 'site', out / 'wiki'
    m = curation.load(site / 'publication-manifest.json')
    curation.need(not m['published'] and not m['live_channel_readback'], 'Premature channel acceptance')
    actual = {p.relative_to(site).as_posix() for p in site.rglob('*') if p.is_file()}
    curation.need(actual == set(m['files_sha256']) | {'publication-manifest.json'}, 'Composed site inventory differs')
    curation.need({p.name for p in wiki.glob('*.md')} == set(m['wiki_files_sha256']), 'Composed Wiki inventory differs')
    for names, root in [(m['files_sha256'], site), (m['wiki_files_sha256'], wiki)]:
        for name, digest in names.items():
            curation.need(curation.sha((root / name).read_bytes()) == digest, 'Composed body changed: ' + name)
    for name, digest in m['frozen_snapshot_sha256'].items():
        curation.need(curation.sha((site / name).read_bytes()) == digest, 'Frozen snapshot changed: ' + name)
    for name, digest in m['historical_wiki_sha256'].items():
        curation.need(curation.sha((wiki / name).read_bytes()) == digest, 'Historical Wiki reference changed')
    cache, id_cache, html_links, wiki_links = {}, {}, 0, 0
    def soup(p):
        if p not in cache:
            cache[p] = BeautifulSoup(markdown.markdown(p.read_text(), extensions=FEATURES) if p.suffix == '.md' else p.read_text(), 'html.parser')
        return cache[p]
    def has_id(p, value):
        if p not in id_cache:
            id_cache[p] = {n['id'] for n in soup(p).select('[id]')}
        return value in id_cache[p]
    current_routes = {p['html'] for p in m['pairs'].values()} | {'current/index.html', 'current/concepts/subdomains.html', 'current/downloads/index.html'}
    checked = [site / n for n in sorted(current_routes)] + [site / n.replace('current/', 'releases/v0.3.10/', 1) for n in sorted(current_routes)] + [site / 'index.html', site / 'versions/index.html']
    for p in checked:
        doc = soup(p)
        curation.need(doc.html and doc.html.get('lang') == 'en' and doc.select_one('meta[name=viewport]'), 'HTML language/viewport')
        for tag in doc.select('a[href], img[src]'):
            url = tag.get('href', tag.get('src'))
            parsed = urlsplit(url)
            if url.startswith(SITE + '/'):
                target = (site / unquote(parsed.path[len('/riskium/'):])).resolve()
            elif parsed.scheme or url.startswith('//'):
                continue
            else:
                target = (p.parent / unquote(parsed.path)).resolve() if parsed.path else p
            curation.need(target.is_relative_to(site) and target.is_file(), 'Missing composed HTML target: ' + url)
            if parsed.fragment and target.suffix == '.html':
                curation.need(has_id(target, unquote(parsed.fragment)), 'Missing composed HTML anchor: ' + url)
            html_links += 1
    for p in wiki.glob('*.md'):
        for url in re.findall(r'\]\(([^)]+)\)', p.read_text()):
            parsed = urlsplit(url)
            if parsed.scheme or url.startswith('//'):
                continue
            target = wiki / (unquote(parsed.path) + '.md') if parsed.path else p
            curation.need(target.is_file(), 'Missing composed Wiki target: ' + url)
            if parsed.fragment:
                curation.need(has_id(target, unquote(parsed.fragment)), 'Missing composed Wiki anchor: ' + url)
            wiki_links += 1
    for slug, pair in m['pairs'].items():
        html = ' '.join(soup(site / pair['html']).main.get_text(' ', strip=True).split())
        wt = (wiki / pair['wiki']).read_text().split('<!-- BEGIN CURATION BODY -->\n', 1)[1].split('\n<!-- END CURATION BODY -->', 1)[0]
        curation.need(curation.sha(html.encode()) == pair['plain_text_sha256'] == curation.sha(projection.plain(wt).encode()), 'Composed HTML/Wiki/source text parity: ' + slug)
    return {'status': 'PASS_FULL_COMPOSED_CANDIDATE_NOT_PUBLISHED', 'source_ref': m['source_ref'],
            'paired_bodies': len(m['pairs']), 'wiki_files': len(m['wiki_files_sha256']), 'retained_guides': len(m['retained_guides']),
            'pages_files': len(actual), 'html_bodies_checked': len(checked), 'html_local_links': html_links, 'wiki_local_links': wiki_links,
            'frozen_snapshot_files_preserved': len(m['frozen_snapshot_sha256']), 'historical_wiki_files_preserved': len(m['historical_wiki_sha256']),
            'published': False, 'live_channel_readback': False}
