"""Reader 0.4.8 adds reviewed source comparisons over the immutable 0.4.7 reader."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from bs4 import BeautifulSoup
import dictionary_documentation as projection
from presentation import render
from site_registry import file_map
from audit_versioned_site import audit

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import build_external_definitions as definitions
VERSION = '0.4.8'
BASELINE = '9cfc399229d4a65d6372b4bef6586b5b10ae5c89'
sha = lambda b: hashlib.sha256(b).hexdigest()
encode = definitions.encode


def build(out, wikiout):
    out, wikiout = out.resolve(), wikiout.resolve()
    source = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    # Execute the original generator from its own exact checkout, preserving all its bindings.
    with tempfile.TemporaryDirectory(prefix='riskium-reader047-') as temporary:
        old = Path(temporary) / 'source'
        subprocess.run(['git', 'worktree', 'add', '--detach', str(old), BASELINE], cwd=ROOT, check=True, capture_output=True)
        try:
            subprocess.run([sys.executable, str(old / 'tools/publication/v038_documentation.py'), '--output', str(out), '--wiki-output', str(wikiout)], cwd=old, check=True, capture_output=True)
        finally:
            subprocess.run(['git', 'worktree', 'remove', '--force', str(old)], cwd=ROOT, check=True, capture_output=True)
    before = file_map(out)
    previous_wiki = {p.name: p.read_bytes() for p in wikiout.glob('*.md')}
    files = definitions.build()
    model = json.loads((ROOT / 'ontology/riskium-model.json').read_text())
    wiki = {n:b.decode() for n,b in previous_wiki.items()}
    for name, text in files.items():
        if not name.endswith('.md'):
            continue
        if name == 'Subdomains.md':
            for d in model['domains']:
                text += '\n## ' + d['id'] + ' ' + d['title'] + '\n\n' + d['objective'] + '\n'
        page = 'current/concepts/' + projection.route(name)
        body = projection.project(text, source)
        if name == 'Subdomains.md':
            body = '<p><img class="subdomain-map" src="../assets/subdomain-relationships.svg" alt="Eleven subdomains and 23 association pairs; inheritance excluded"></p><p><a href="../assets/subdomain-relationships.svg">Package SVG</a> · <a href="../assets/subdomain-relationships-matrix.svg">Exact association matrix SVG</a></p>' + body
        slug = 'Concept-Index' if name == 'README.md' else name[:-3]
        source_url = projection.REPO + '/blob/' + source + '/documentation/0.4.8/concepts/' + name
        body += '<p>Reader 0.4.8 · documentary review 0.1.0 · <a href="' + source_url + '">Source dossier</a> · <a href="' + projection.REPO + '/wiki/' + slug + '">Equivalent Wiki page</a>.</p>'
        (out / page).write_text(render(Path(page), 'Concept dictionary' if name == 'README.md' else name[:-3], body))
        wiki[slug + '.md'] = projection.project(text, source, True) + '\n\nReader **0.4.8** · documentary review **0.1.0** · [Source dossier](' + source_url + ') · [Equivalent Pages page](' + projection.SITE + '/' + page + ') · [Repository](' + projection.REPO + ') · [Wiki Home](Home)\n'
    context = '<div class="publication-context">Reader <strong>0.4.8</strong> · model <strong>0.3.1</strong> · <a href="' + projection.REPO + '/releases/tag/v0.3.8">Published source v0.3.8</a> · <a href="' + projection.REPO + '/wiki">Wiki</a></div>'
    for path in list((out / 'current').rglob('*.html')) + [out / 'versions/index.html']:
        soup = BeautifulSoup(path.read_text(), 'html.parser')
        old_context = soup.select_one('.publication-context')
        if old_context:
            old_context.replace_with(BeautifulSoup(context, 'html.parser'))
        target = os.path.relpath('current/concepts/External-Definitions.html', path.relative_to(out).parent).replace(os.sep, '/')
        for nav in soup.select('aside.sidebar, details.mobile-navigation > div'):
            if not nav.find('a', href=target):
                group = nav.find('ul')
                if group:
                    group.append(BeautifulSoup('<li><a href="' + target + '">External definitions and decisions</a></li>', 'html.parser'))
        if path.relative_to(out).as_posix() in ['current/index.html', 'current/guide/Home.html']:
            main = soup.select_one('main'); heading = main.find('h1')
            heading.insert_after(BeautifulSoup('<p>Reader 0.4.8 adds <a href="' + target + '">source-comparison decisions for all 80 concepts</a> over the published 0.4.7 guide checkpoint. Normative mappings and independent semantic acceptance retain their separate status.</p>', 'html.parser'))
        if path.relative_to(out).as_posix() == 'versions/index.html':
            first = soup.select_one('main p')
            first.replace_with(BeautifulSoup('<p>Maintained reader <strong>0.4.8</strong> adds documentary review 0.1.0 over the exact 0.4.7 guide checkpoint. Published source remains v0.3.8, model/OWL 0.3.1. Earlier frozen snapshots retain their original bytes and dated claims.</p>', 'html.parser'))
        for th in soup.select('th'):
            th['scope'] = 'col'
        for table in soup.select('main table'):
            table['tabindex'] = '0'
        path.write_text(str(soup) + '\n')
    wiki['Home.md'] = 'Reader **0.4.8** · [External definitions and decisions](External-Definitions) · [Concept index](Concept-Index). The following guide retains its dated 0.4.7 source-release checkpoint.\n\n' + wiki['Home.md']
    wiki['_Sidebar.md'] = '- [External definitions and decisions](External-Definitions)\n\n' + wiki['_Sidebar.md']
    wiki['_Footer.md'] = 'Reader **0.4.8** · [Repository](' + projection.REPO + ') · [Pages](' + projection.SITE + '/current/index.html) · [Concept index](Concept-Index) · [Source review](External-Definitions) · [Published source v0.3.8](' + projection.REPO + '/releases/tag/v0.3.8)\n'
    for name, text in wiki.items():
        (wikiout / name).write_text(text)
    (out / 'current/concepts/external-definition-review.json').write_bytes((ROOT / definitions.REVIEW).read_bytes())
    review_manifest = json.loads(files['manifest.json'])
    (out / 'current/concepts/review-manifest.json').write_text(encode(review_manifest))
    status = json.loads((out / 'current/published-status.json').read_text())
    status.update(documentation_version=VERSION, documentation_source_commit=source, guide_content_version='0.4.7', guide_source_commit=BASELINE, dictionary_source_commit=source, dictionary_source_namespace='documentation/0.4.8/concepts', dictionary_review=review_manifest, native_wiki_files=len(wiki), wiki_files_sha256={n:sha(t.encode()) for n,t in wiki.items()}, new_source_distribution=False, current_author_held_manuscript='7.2.4', source_release_manuscript_review_checkpoint='7.2.3')
    (out / 'current/published-status.json').write_text(encode(status))
    current = json.loads((out / 'current/publication-manifest.json').read_text())
    current.update(documentation_version=VERSION, documentation_source_commit=source, guide_content_version='0.4.7', guide_source_commit=BASELINE, dictionary_source_commit=source, documentation_note='Reader 0.4.8: source-qualified documentary dispositions; no model or normative equivalence change.')
    (out / 'current/publication-manifest.json').write_text(encode(current))
    manifest = json.loads((out / 'publication-manifest.json').read_text())
    manifest.update(current_source_commit=source, documentation_version=VERSION, published_reader_projection=dict(source_release='v0.3.8', published_source_commit=status['published_source_commit'], documentation_source_commit=source, source_namespace='documentation/0.4.8', semantic_changes=False))
    manifest['publication_status_projection']['documentation_version'] = VERSION
    (out / 'dictionary-validation.json').unlink()
    manifest['files_sha256'] = {n:sha(b) for n,b in file_map(out).items() if n != 'publication-manifest.json'}
    (out / 'publication-manifest.json').write_text(encode(manifest))
    result = audit(out)
    result.update(documentation_version=VERSION, concept_pages=80, reviewed_dispositions=80, wiki_files=len(wiki), external_definition_review_sha256=sha((ROOT / definitions.REVIEW).read_bytes()), formal_equivalences=0)
    (out / 'dictionary-validation.json').write_text(encode(result))
    manifest['files_sha256']['dictionary-validation.json'] = sha((out / 'dictionary-validation.json').read_bytes())
    (out / 'publication-manifest.json').write_text(encode(manifest))
    audit(out)
    for name, data in before.items():
        if name.startswith('releases/'):
            definitions.require((out / name).read_bytes() == data, 'Frozen snapshot changed')
    for name, data in previous_wiki.items():
        if not name.startswith('RKM-') and name not in ['Home.md', '_Sidebar.md', '_Footer.md', 'Concept-Index.md', 'Subdomains.md']:
            definitions.require((wikiout / name).read_bytes() == data, 'Dated guide body changed: ' + name)
    definitions.require(len(wiki) == 106, 'Wiki projection inventory differs')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--wiki-output', type=Path, default=Path('build/wiki'))
    args = parser.parse_args()
    print(encode(build(args.output, args.wiki_output)))
