"""Stage reader 0.4.10 as matching HTML and Wiki bodies; never deploy."""
import argparse
import html
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit
import markdown
from bs4 import BeautifulSoup
import curation
import reader

REPO = 'https://github.com/ArazSaieArasi3/riskium'
SITE = 'https://arazsaiearasi3.github.io/riskium'
CSS = 'body{font:16px/1.65 system-ui,sans-serif;color:#203847;max-width:1200px;margin:auto;padding:24px}header{background:#edf3f6;border:1px solid #b5c7d3;padding:18px}nav{display:flex;flex-wrap:wrap;gap:16px;margin:18px 0}a{color:#145d7b;text-underline-offset:.16em}a:focus-visible{outline:3px solid #b87918}h1{line-height:1.25}table{border-collapse:collapse;display:block;max-width:100%;overflow:auto;margin:18px 0}th,td{border:1px solid #b7c8d3;padding:8px;vertical-align:top;text-align:left}th{background:#e7eff4}pre{overflow:auto;background:#f1f5f7;padding:12px}code{overflow-wrap:anywhere}img{max-width:100%;height:auto}footer{border-top:1px solid #c4d1da;margin-top:30px;padding-top:18px}main{min-width:0}.stage{border-left:4px solid #ad701f;padding-left:12px}@media(max-width:650px){body{padding:14px}h1{font-size:1.65rem}}'
FEATURES = ['tables', 'fenced_code', 'toc', 'md_in_html']


def slug(name):
    return 'Concept-Index' if name == 'README.md' else name[:-3]


def route(name):
    return 'index.html' if name == 'README.md' else name[:-3] + '.html'


def plain(text):
    return ' '.join(BeautifulSoup(markdown.markdown(text, extensions=FEATURES), 'html.parser').get_text(' ', strip=True).split())


def build(output, source_ref):
    output = Path(output).resolve()
    curation.need(not output.exists(), 'Use an empty projection destination')
    curation.need(re.fullmatch(r'[A-Za-z0-9._/-]+', source_ref) is not None, 'Invalid source ref')
    files = reader.build(check=True)
    site, wiki = output / 'site/current/concepts', output / 'wiki'
    site.mkdir(parents=True)
    wiki.mkdir(parents=True)
    pairs = {}

    def resolve(url, for_wiki=False):
        parsed = urlsplit(url)
        if parsed.scheme or url.startswith('//') or not parsed.path:
            return url
        target = (reader.OUT / unquote(parsed.path)).resolve()
        curation.need(target.is_relative_to(curation.ROOT) and target.is_file(), 'Missing source route: ' + url)
        frag = '#' + parsed.fragment if parsed.fragment else ''
        if target.parent == reader.OUT and target.name in files:
            if target.suffix == '.md':
                return (slug(target.name) if for_wiki else route(target.name)) + frag
            if not for_wiki:
                return target.name + frag
        return REPO + '/blob/' + source_ref + '/' + target.relative_to(curation.ROOT).as_posix() + frag

    for name, text in files.items():
        if not name.endswith('.md'):
            (site / name).write_text(text)
            continue
        doc = BeautifulSoup(markdown.markdown(text, extensions=FEATURES), 'html.parser')
        for tag in doc.select('a[href]'):
            tag['href'] = resolve(tag['href'])
        for tag in doc.select('img[src]'):
            tag['src'] = resolve(tag['src'])
        for th in doc.select('th'):
            th['scope'] = 'col'
        title = doc.h1.get_text(' ', strip=True) if doc.h1 else name
        source_url = REPO + '/blob/' + source_ref + '/' + (reader.OUT / name).relative_to(curation.ROOT).as_posix()
        body = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + html.escape(title) + ' | Riskium</title><style>' + CSS + '</style></head><body><header><strong>Riskium</strong><p>Model 0.3.2 · documentary review 0.2.0 · reader 0.4.10</p><p class="stage">Prepared for v0.3.10; not published. This is a staged source-bound projection.</p></header><nav><a href="index.html">Concept index</a><a href="Subdomains.html">Subdomains</a><a href="External-Definitions.html">Source comparisons</a><a href="Curation-Status.html">Version status</a><a href="' + REPO + '">Repository</a></nav><main>' + str(doc) + '</main><footer><a href="' + source_url + '">Source dossier</a> · <a href="' + REPO + '/wiki">Published baseline Wiki</a> · <a href="' + SITE + '/current/index.html">Published baseline Pages</a><p>Normative adoption and independent interpretation retain their separate scope. Article 7.2.21 is unchanged.</p></footer></body></html>\n'
        (site / route(name)).write_text(body)
        wt = re.sub(r'\]\(([^)]+)\)', lambda m: '](' + resolve(m[1], True) + ')', text)
        wiki_body = '<!-- BEGIN CURATION BODY -->\n' + wt.rstrip() + '\n<!-- END CURATION BODY -->\n\n---\n\nPrepared reader **0.4.10**, review **0.2.0**; not published. [Source dossier](' + source_url + ') · [Concept index](Concept-Index) · [Wiki Home](Home) · [Repository](' + REPO + ')\n'
        (wiki / (slug(name) + '.md')).write_text(wiki_body)
        pairs[name] = {'html': 'site/current/concepts/' + route(name), 'wiki': 'wiki/' + slug(name) + '.md',
                       'source_sha256': curation.sha(text.encode()), 'plain_text_sha256': curation.sha(plain(text).encode())}
    (wiki / 'Home.md').write_text('# Prepared Riskium curation reader\n\nReader **0.4.10** and review **0.2.0** for model **0.3.2**, prepared for v0.3.10; not published.\n\n[Concept index](Concept-Index) · [Source comparisons](External-Definitions) · [Version status](Curation-Status) · [Repository](' + REPO + ') · [Published baseline Pages](' + SITE + '/current/index.html)\n')
    (wiki / '_Sidebar.md').write_text('[Home](Home)\n\n- [Concept index](Concept-Index)\n- [Subdomains](Subdomains)\n- [Source comparisons](External-Definitions)\n- [Version status](Curation-Status)\n\n[Repository](' + REPO + ') · [Published baseline Pages](' + SITE + '/current/index.html)\n')
    (wiki / '_Footer.md').write_text('Prepared reader 0.4.10; not published. [Home](Home) · [Concept index](Concept-Index) · [Repository](' + REPO + ') · [Published baseline Pages](' + SITE + '/current/index.html)\n')
    manifest = {'schema': 'riskium-curation-staged-projection/1', 'package_target': 'v0.3.10', 'documentation_version': '0.4.10',
                'review_version': '0.2.0', 'source_ref': source_ref, 'exact_commit_ref': bool(re.fullmatch('[a-f0-9]{40}', source_ref)),
                'model_sha256': curation.load(curation.REVIEW)['model_sha256'], 'review_sha256': curation.sha(curation.REVIEW.read_bytes()),
                'reader_manifest_sha256': curation.sha((reader.OUT / 'manifest.json').read_bytes()),
                'published': False, 'live_channel_readback': False, 'pairs': pairs,
                'files_sha256': {p.relative_to(output).as_posix(): curation.sha(p.read_bytes()) for p in sorted(output.rglob('*')) if p.is_file()}}
    (output / 'projection-manifest.json').write_text(curation.dump(manifest))
    return audit(output)


def audit(output):
    output = Path(output).resolve()
    m = curation.load(output / 'projection-manifest.json')
    actual = {p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file()}
    curation.need(actual == set(m['files_sha256']) | {'projection-manifest.json'}, 'Projection inventory')
    curation.need(m['published'] is False and m['live_channel_readback'] is False, 'Premature publication claim')
    for name, expected in m['files_sha256'].items():
        curation.need(curation.sha((output / name).read_bytes()) == expected, 'Projection body changed: ' + name)
    cache, links = {}, 0

    def soup(path):
        if path not in cache:
            text = path.read_text()
            cache[path] = BeautifulSoup(markdown.markdown(text, extensions=FEATURES) if path.suffix == '.md' else text, 'html.parser')
        return cache[path]

    for name in m['files_sha256']:
        path = output / name
        if path.suffix not in ('.html', '.md'):
            continue
        doc = soup(path)
        if path.suffix == '.html':
            curation.need(doc.html and doc.html.get('lang') == 'en' and doc.select_one('meta[name=viewport]')
                         and 'not published' in doc.select_one('.stage').get_text(), 'HTML context/language')
        for tag in doc.select('a[href], img[src]'):
            url = tag.get('href', tag.get('src'))
            parsed = urlsplit(url)
            if parsed.scheme or url.startswith('//'):
                continue
            dest = unquote(parsed.path)
            target = (path.parent / (dest + ('.md' if path.suffix == '.md' and dest else ''))).resolve() if dest else path
            curation.need(target.is_relative_to(output) and target.is_file(), 'Broken staged route: ' + url)
            if parsed.fragment:
                curation.need(soup(target).find(id=unquote(parsed.fragment)) is not None, 'Broken staged anchor: ' + url)
            links += 1
    for name, pair in m['pairs'].items():
        hp, wp = output / pair['html'], output / pair['wiki']
        ht = ' '.join(soup(hp).main.get_text(' ', strip=True).split())
        wt = wp.read_text().split('<!-- BEGIN CURATION BODY -->\n', 1)[1].split('\n<!-- END CURATION BODY -->', 1)[0]
        curation.need(curation.sha(ht.encode()) == pair['plain_text_sha256'] == curation.sha(plain(wt).encode()), 'HTML/Wiki/source text parity: ' + name)
    return {'status': 'PASS_STAGED_CURATED_READER_NOT_PUBLICATION', 'paired_bodies': len(m['pairs']),
            'html_pages': len(list((output / 'site').rglob('*.html'))), 'wiki_pages': len(list((output / 'wiki').glob('*.md'))),
            'local_links_checked': links, 'source_ref': m['source_ref'], 'published': False, 'live_channel_readback': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--commit', default='planning/v0.3.10-curation')
    parser.add_argument('--audit', action='store_true')
    args = parser.parse_args()
    print(curation.dump(audit(args.output) if args.audit else build(args.output, args.commit)))
