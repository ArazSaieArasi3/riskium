"""Check every deployed HTML route/fragment and manifest byte, including snapshots."""
from pathlib import Path
import argparse
import json
from urllib.parse import unquote, urlsplit
from bs4 import BeautifulSoup
from site_registry import sha, file_map


def audit(folder):
    files = file_map(folder)
    manifest = json.loads(files['publication-manifest.json'])
    actual = {p: sha(b) for p, b in files.items() if p != 'publication-manifest.json'}
    if actual != manifest['files_sha256']:
        raise ValueError('Deployed manifest file inventory/digests differ')
    pages = {p: BeautifulSoup(b.decode(), 'html.parser') for p, b in files.items() if p.endswith('.html')}
    ids = {}
    links = 0
    for name, soup in pages.items():
        if soup.html is None or soup.html.get('lang') != 'en' or not soup.select('meta[name="viewport"]'):
            raise ValueError('Missing HTML language/viewport: ' + name)
        found = [n['id'] for n in soup.select('[id]')]
        if len(found) != len(set(found)):
            raise ValueError('Duplicate HTML identifier: ' + name)
        ids[name] = set(found)
        if soup.select('input[type="file"], form, object, embed'):
            raise ValueError('Unexpected upload/embed surface: ' + name)
        for node in soup.find_all(True):
            if any(k.lower().startswith('on') for k in node.attrs):
                raise ValueError('Inline handler: ' + name)
            for attr in ['src', 'poster']:
                url = node.get(attr, '')
                if urlsplit(url).scheme or url.startswith('//'):
                    raise ValueError('Remote runtime asset: ' + name)
        for script in soup.find_all('script'):
            viewer_script = name.endswith('/webvowl/index.html') and script.get('src') in ['vendor/d3.min.js','vendor/webvowl.js','viewer.js']
            if script.get('type') != 'application/ld+json' and not viewer_script and not script.get('src', '').endswith('filter.js'):
                raise ValueError('Unexpected runtime script: ' + name)
    for name, soup in pages.items():
        for node in soup.find_all(['a', 'link', 'img', 'script', 'iframe']):
            url = node.get('href') or node.get('src') or ''
            parts = urlsplit(url)
            if not url or parts.scheme or url.startswith('//'):
                continue
            links += 1
            path = ((folder / name).parent / unquote(parts.path)).resolve() if parts.path else (folder / name).resolve()
            if not path.is_relative_to(folder.resolve()):
                raise ValueError('Deployed link escapes root: ' + name + ' -> ' + url)
            target = path.relative_to(folder.resolve()).as_posix()
            if target not in files:
                raise ValueError('Missing deployed target: ' + name + ' -> ' + url)
            if parts.fragment and target in ids and unquote(parts.fragment) not in ids[target]:
                raise ValueError('Missing deployed fragment: ' + name + ' -> ' + url)
    for entry in manifest['releases'].values():
        if any(sha(files[entry['route'] + '/' + p]) != digest for p, digest in entry['files_sha256'].items()):
            raise ValueError('Frozen deployed byte mismatch')
    return dict(status='VERSIONED_DOCUMENTATION_PASS', source_commit=manifest['current_source_commit'],
                files=len(files), html_pages=len(pages), local_links=links,
                frozen_snapshots=len(manifest['releases']), browser_execution=False, new_release_published=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    print(json.dumps(audit(parser.parse_args().folder)))
