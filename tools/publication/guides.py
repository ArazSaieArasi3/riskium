"""One source registry and URL policy for the Wiki and Pages explanations."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = 'tools/publication/guide-registry.json'
REPO = 'https://github.com/ArazSaieArasi3/riskium'
SITE = 'https://arazsaiearasi3.github.io/riskium'
SEMANTIC_COMMIT = '8afe169968b5c1396c02834dbc499af691b894b4'


def entries(root=ROOT):
    rows = json.loads((root / REGISTRY).read_text())['guides']
    for key in ('slug', 'wiki_slug', 'source'):
        if len({r[key] for r in rows}) != len(rows):
            raise ValueError('Duplicate guide ' + key)
    for row in rows:
        if not all(re.fullmatch(r'[A-Za-z][A-Za-z0-9-]*', row[k]) for k in ('slug', 'wiki_slug')):
            raise ValueError('Unsafe guide slug')
        target = (root / row['source']).resolve()
        if not target.is_relative_to(root.resolve()) or not target.is_file() or target.suffix != '.md':
            raise ValueError('Invalid guide source: ' + row['source'])
    return rows


def source_ref(path, root=ROOT):
    """A path's existence at the release is not evidence of byte equality."""
    old = subprocess.run(['git', 'show', SEMANTIC_COMMIT + ':' + path], cwd=root, capture_output=True)
    target = root / path
    return SEMANTIC_COMMIT if old.returncode == 0 and target.is_file() and old.stdout == target.read_bytes() else 'main'


def wiki_link(url, source, rows, root=ROOT):
    parts = urlsplit(url)
    if not url or parts.scheme or url.startswith(('#', '//')):
        return url
    target = ((root / source).parent / unquote(parts.path)).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError('Guide link escapes repository: ' + url)
    by_source = {(root / r['source']).resolve(): r for r in rows}
    if target in by_source:
        result = by_source[target]['wiki_slug']
    else:
        rel = target.relative_to(root.resolve()).as_posix()
        result = REPO + ('/tree/' if target.is_dir() else '/blob/') + source_ref(rel, root) + '/' + rel
    return result + ('?' + parts.query if parts.query else '') + ('#' + parts.fragment if parts.fragment else '')


def explanatory_markdown(row, root=ROOT):
    text = (root / row['source']).read_text()
    if row.get('context_note'):
        heading, separator, rest = text.partition('\n')
        text = heading + '\n\n> ' + row['context_note'] + '\n' + separator + rest
    return text


def project_wiki(row, rows, root=ROOT):
    text = explanatory_markdown(row, root)
    # Preserve scientific text and Markdown; only project ordinary inline URLs.
    text = re.sub(r'(!?\[[^\]\n]*\])\(([^\s)]+)\)',
                  lambda m: m[1] + '(' + wiki_link(m[2], row['source'], rows, root) + ')', text)
    digest = hashlib.sha256((root / row['source']).read_bytes()).hexdigest()
    footer = ('\n\n---\n\n[Equivalent Pages guide](' + SITE + '/current/guide/' + row['slug'] + '.html)'
              ' · [WIDOCO](' + SITE + '/current/widoco/index-en.html)'
              ' · [OWL explorer](' + SITE + '/current/explore/index.html)'
              ' · [Published v0.3.1](' + REPO + '/releases/tag/v0.3.1).\n\n'
              'Explanatory source: [' + row['source'] + '](' + REPO + '/blob/main/' + row['source'] + '). '
              'Source SHA-256: `' + digest + '`. This current explanation and later development evidence '
              'are separate from the immutable v0.3.1 source assets.\n')
    return text.rstrip() + footer


def wiki_outputs(root=ROOT):
    rows = entries(root)
    outputs = {r['wiki_slug'] + '.md': project_wiki(r, rows, root) for r in rows}
    outputs['_Sidebar.md'] = '# Riskium\n\n' + '\n'.join('- [' + r['title'] + '](' + r['wiki_slug'] + ')' for r in rows) + '\n'
    outputs['_Footer.md'] = ('[Pages](' + SITE + '/current/index.html) · [Documentation versions](' + SITE + '/versions/index.html)'
                             ' · [Repository](' + REPO + ') · [Citation](Citation) · [Limits](Limitations)\n')
    return outputs


def sync_wiki(root=ROOT, check=False):
    out = root / 'docs/wiki'
    expected = wiki_outputs(root)
    actual = {p.name for p in out.glob('*.md') if p.name != 'README.md'}
    extra = actual - set(expected)
    if extra:
        raise ValueError('Unregistered Wiki pages need an explicit preservation decision: ' + ', '.join(sorted(extra)))
    for name, text in expected.items():
        path = out / name
        if check:
            if not path.exists() or path.read_text() != text:
                raise ValueError('Stale Wiki projection: ' + name)
        else:
            out.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
    return len(entries(root))
