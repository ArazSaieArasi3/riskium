"""Promote qualified documentary bodies only after exact public asset verification."""
import argparse
import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit, unquote
from urllib.request import Request, urlopen
import markdown
from bs4 import BeautifulSoup
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import curation
import reader
import compose
import projection

ROOT = curation.ROOT
REPO, SITE = compose.REPO, compose.SITE
INTENT = ROOT / 'evaluation/releases/v0.3.10/publication-intent.json'
ROLES = 'Package v0.3.10 · model 0.3.2 · documentary review 0.2.0 · reader 0.4.10'


def gh(path):
    return json.loads(subprocess.check_output(['gh', 'api', 'repos/ArazSaieArasi3/riskium/' + path], text=True))


def verify_release(intent, release, latest, tag, run):
    curation.need(release['tag_name'] == latest['tag_name'] == 'v0.3.10' and release['id'] == latest['id']
                 and not release['draft'] and not release['prerelease'] and release['published_at'], 'Release is not current/public')
    curation.need(tag['type'] == 'commit' and tag['sha'] == intent['source_commit'], 'Release tag/source differs')
    curation.need(run['head_sha'] == intent['source_commit'] and run['status'] == 'completed' and run['conclusion'] == 'success', 'Source CI is not successful')
    actual = {a['name']: {'bytes': a['size'], 'sha256': a['digest'].removeprefix('sha256:')} for a in release['assets']}
    curation.need(actual == intent['assets'] and len(actual) == 6, 'Public asset identity differs')
    return True


def public_inputs(folder):
    intent = curation.load(INTENT)
    release, latest = gh('releases/tags/v0.3.10'), gh('releases/latest')
    tag = gh('git/ref/tags/v0.3.10')['object']
    if tag['type'] == 'tag':
        tag = gh('git/tags/' + tag['sha'])['object']
    run = gh('actions/runs/' + str(intent['run_id']))
    verify_release(intent, release, latest, tag, run)
    folder = Path(folder); folder.mkdir(parents=True)
    rows = []
    for asset in sorted(release['assets'], key=lambda a: a['name']):
        # No credentials are sent: these are actual public release URLs.
        with urlopen(Request(asset['browser_download_url'], headers={'User-Agent': 'Riskium-v0310-public-readback'}), timeout=90) as response:
            body = response.read()
        expected = intent['assets'][asset['name']]
        curation.need(len(body) == expected['bytes'] and curation.sha(body) == expected['sha256'], 'Public download differs')
        (folder / asset['name']).write_bytes(body)
        rows.append({'name': asset['name'], 'url': asset['browser_download_url'], **expected})
    subprocess.run([sys.executable, '-I', str(ROOT / 'tools/releases/v0310/package/verify_package.py'), '--assets', str(folder),
                    '--expected-source-commit', intent['source_commit'], '--expected-run-id', str(intent['run_id']),
                    '--report', str(folder.parent / 'public-package-verification.json')], check=True)
    return intent, release, rows


def promoted(text, slug, intent, release):
    banner = 'Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Published source package **v0.3.10**; channel verification is recorded separately.'
    text = text.replace(reader.BANNER, banner)
    text = text.replace('**Prepared package v0.3.10**', '**Published package v0.3.10**')
    text = text.replace('The latest verified public predecessor is v0.3.9; successor publication/readback is tracked separately.', 'The six public assets are verified against their qualified source; maintained-channel observations have their own receipt.')
    text = text.replace('Prepared output is not deployed output; v0.3.9 remains the published package until the separate v0.3.10 publication/readback gate passes.', 'This view selects the public v0.3.10 source package. Actual channel observations are recorded separately from its frozen preparation receipts.')
    text = text.replace('This prepared documentation successor retains the scientific source and adds current documentary comparisons. Actual publication and channel readback remain separately recorded gates.', 'The public source package preserves the scientific source and adds current documentary comparisons. Frozen preparation and maintained-channel observations keep their own evidence bindings.')
    text = text.replace('The prepared selection distinguishes', 'The selected package distinguishes')
    if slug == 'Home':
        text = text.replace('[Published v0.3.9](' + REPO + '/releases/tag/v0.3.9)', '[Published v0.3.10](' + release['html_url'] + ')')
    text = text.replace('The prepared v0.3.10 successor adds qualified current documentary review while preserving the tested 0.3.2 scientific source. Actual publication and channel readback remain the final gate.', 'The public v0.3.10 source package adds qualified current documentary review while preserving the tested 0.3.2 scientific source. Maintained-channel observations are recorded in the release evidence.')
    if slug == 'Publication':
        labels = {'riskium-v0.3.10-source.tar.gz': 'Source archive', 'source-manifest.json': 'Source manifest', 'artifact-versions.json': 'Artifact versions', 'freeze-receipt.json': 'Freeze receipt', 'release-notes.md': 'Release notes', 'SHA256SUMS.txt': 'Checksums'}
        text = '# Publication and verified downloads\n\n[Riskium v0.3.10](' + release['html_url'] + ') publishes scientific source **0.3.2**, documentary review **0.2.0** and reader **0.4.10**. All six attached assets were downloaded from their public URLs and verified against the exact qualified source and checksums.\n\n| Verified asset | Use |\n|---|---|\n'
        for a in sorted(release['assets'], key=lambda a: a['name']):
            text += '| [' + labels[a['name']] + '](' + a['browser_download_url'] + ') | This source-bound asset is checked against the published inventory and standalone verifier. |\n'
        text += '\nThe frozen source is `' + intent['source_commit'] + '`; qualification and package [run ' + str(intent['run_id']) + '](' + REPO + '/actions/runs/' + str(intent['run_id']) + ') retains the 36 source/composition/package controls. The archive binds the exact committed source, eight active component roles and 38 retained predecessor records. Frozen preparation labels are preserved rather than rewritten as live observations.\n\n[Source and channel evidence](' + REPO + '/tree/main/evaluation/releases/v0.3.10) · [Version roles](Artifact-Versions.md) · [Reproduce](Reproduce.md) · [Verified predecessor v0.3.9](' + REPO + '/releases/tag/v0.3.9)\n'
    elif slug == 'Citation':
        text = '# Citation and rights\n\nCite **Riskium v0.3.10: an ontology for ecosystem and enterprise risk knowledge**, by Araz Saie Arasi, Hassan Haghighi and Hossein Azgomi, together with the component version and exact source commit used. This source release selects model 0.3.2, documentary review 0.2.0 and reader 0.4.10. No article publication or DOI is inferred from the GitHub release.\n\nResearch content uses CC BY 4.0 and original code uses MIT, subject to retained third-party notices. The package-bound manuscript 7.2.21 preserves its original evidence role; the separately maintained author manuscript can advance independently.\n\n[Release](' + release['html_url'] + ') · [Repository](' + REPO + ') · [Wiki](' + REPO + '/wiki) · [Pages](' + SITE + '/current/index.html)\n'
    elif slug == 'Reproduce':
        text = '# Reproduce and verify\n\nDownload all six [public assets](Publication.md). Preserve their names and run the standalone standard-library verifier from the source archive:\n\n```sh\npython -I tools/releases/v0310/package/verify_package.py --assets /path/to/six-assets --expected-source-commit ' + intent['source_commit'] + ' --expected-run-id ' + str(intent['run_id']) + '\n```\n\nThe verifier reconstructs the full Git commit/tree and checks the component/source/reader and qualification bindings. Its offline prepared-package status is distinct from actual publication and channel receipts. The source archive retains its original CI preparation state.\n\n[The qualification toolchain](' + REPO + '/tree/' + intent['source_commit'] + '/tools/releases/v0310) reproduces the documentary comparisons, twenty retained guides, paired output and historical preservation. The scientific engine results retain the original [v0.3.9 qualification](' + REPO + '/actions/runs/42776380967); they are not renamed as new engine executions for this documentation release.\n\n[Evidence and publication observations](' + REPO + '/tree/main/evaluation/releases/v0.3.10) · [Version roles](Artifact-Versions.md)\n'
    return text


def build(candidate, output, intent, release, downloads):
    candidate, output = Path(candidate).resolve(), Path(output).resolve()
    curation.need(not output.exists(), 'Publication destination exists')
    old = curation.load(candidate / 'site/publication-manifest.json')
    marker = candidate / 'site/.nojekyll'
    if not marker.exists():
        curation.need(old['files_sha256']['.nojekyll'] == curation.sha(b''), 'Unknown missing marker')
        marker.write_bytes(b'')
    compose.audit(candidate)
    curation.need(old['source_ref'] == intent['source_commit'], 'Candidate belongs to another source')
    qualified = curation.load(candidate.parent / 'qualification.json')
    curation.need(qualified['source_ref'] == intent['source_commit'] and str(qualified['ci_run_id']) == str(intent['run_id'])
                 and qualified['composition_manifest_sha256'] == curation.sha((candidate / 'site/publication-manifest.json').read_bytes()), 'Qualification/composition binding differs')
    shutil.copytree(candidate, output)
    site, wiki = output / 'site', output / 'wiki'
    delivery = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    def resolve(url, source, for_wiki=False):
        p = urlsplit(url)
        if p.scheme or url.startswith('//') or not p.path:
            return url
        frag = '#' + p.fragment if p.fragment else ''
        if p.path.endswith('.md') and '/' not in p.path:
            slug = 'Concept-Index' if p.path == 'README.md' else p.path[:-3]
            return (slug if for_wiki else SITE + '/' + compose.route(slug)) + frag
        target = (source.parent / unquote(p.path)).resolve()
        curation.need(target.is_relative_to(ROOT) and target.is_file(), 'Unknown published source link')
        if target.parent == reader.OUT and target.suffix != '.md' and not for_wiki:
            return SITE + '/current/concepts/' + target.name + frag
        return REPO + '/blob/' + intent['source_commit'] + '/' + target.relative_to(ROOT).as_posix() + frag
    pairs = {}
    for slug, pair in old['pairs'].items():
        source = ROOT / pair['source_path']
        curation.need(curation.sha(source.read_bytes()) == pair['source_sha256'], 'Canonical source changed')
        text = promoted(source.read_text(), slug, intent, release)
        doc = BeautifulSoup(markdown.markdown(text, extensions=compose.FEATURES), 'html.parser')
        for n in doc.select('a[href], img[src]'):
            key = 'href' if n.has_attr('href') else 'src'; n[key] = resolve(n[key], source)
        for n in doc.select('th'):
            n['scope'] = 'col'
        page = BeautifulSoup((site / pair['html']).read_text(), 'html.parser')
        page.main.clear()
        for node in list(doc.contents):
            page.main.append(node)
        for n in page.select('header p, footer p'):
            for t in n.find_all(string=True):
                if 'Prepared package v0.3.10' in t:
                    t.replace_with(str(t).replace('Prepared package v0.3.10', 'Package v0.3.10'))
        for n in page.select('header a'):
            if n.get('href', '').endswith('/releases/tag/v0.3.9'):
                n['href'] = release['html_url']; n.string = 'Published package'
        (site / pair['html']).write_text(str(page) + '\n')
        wt = re.sub(r'\]\(([^)]+)\)', lambda m: '](' + resolve(m[1], source, True) + ')', text)
        (wiki / pair['wiki']).write_text('<!-- BEGIN CURATION BODY -->\n' + wt.rstrip() + '\n<!-- END CURATION BODY -->\n\n---\n\n' + ROLES + ' · [Frozen source](' + REPO + '/blob/' + intent['source_commit'] + '/' + pair['source_path'] + ') · [Pages](' + SITE + '/' + pair['html'] + ') · [Wiki Home](Home) · [Repository](' + REPO + ')\n')
        pairs[slug] = {**pair, 'frozen_source_sha256': pair['source_sha256'], 'plain_text_sha256': curation.sha(projection.plain(text).encode()), 'published_body_sha256': curation.sha(text.encode())}
    for name, source in [('current/index.html', 'current/guide/Home.html'), ('index.html', 'current/guide/Home.html'), ('current/concepts/subdomains.html', 'current/concepts/Subdomains.html'), ('current/downloads/index.html', 'current/guide/Publication.html')]:
        (site / name).write_bytes((site / source).read_bytes())
    for name in ['_Sidebar.md', '_Footer.md']:
        p = wiki / name
        p.write_text(p.read_text().replace('Prepared package v0.3.10', 'Package v0.3.10').replace('Verified predecessor', 'Published package').replace('/releases/tag/v0.3.9', '/releases/tag/v0.3.10'))
    wiki_hashes = {p.name: curation.sha(p.read_bytes()) for p in sorted(wiki.glob('*.md'))}
    state = {'schema': 'riskium-published-reader-0310/1', 'package': 'v0.3.10', 'release_id': release['id'], 'source_commit': intent['source_commit'],
             'documentation_commit': delivery, 'model_version': '0.3.2', 'review_version': '0.2.0', 'reader_version': '0.4.10',
             'source_publication_verified': True, 'source_asset_downloads': downloads, 'channel_receipt': REPO + '/blob/main/evaluation/releases/v0.3.10/channels.json', 'wiki_files_sha256': wiki_hashes}
    (site / 'current/published-status.json').write_text(curation.dump(state))
    shutil.rmtree(site / 'releases/v0.3.10')
    shutil.copytree(site / 'current', site / 'releases/v0.3.10')
    for p in (site / 'releases/v0.3.10').rglob('*.html'):
        p.write_text(p.read_text().replace(SITE + '/current/', SITE + '/releases/v0.3.10/'))
    p = site / 'versions/index.html'
    doc = BeautifulSoup(p.read_text(), 'html.parser')
    doc.main.clear()
    doc.main.append(BeautifulSoup('<h1>Documentation versions</h1><p>Current <a href="' + SITE + '/releases/v0.3.10/index.html">v0.3.10</a> selects review 0.2.0 and reader 0.4.10 for preserved model 0.3.2.</p><ul>' + ''.join('<li><a href="' + SITE + '/releases/' + q.name + '/index.html">' + q.name + '</a> retains its source-bound view.</li>' for q in sorted((site / 'releases').iterdir()) if (q / 'index.html').is_file()) + '</ul>', 'html.parser'))
    p.write_text(str(doc).replace('Prepared package v0.3.10', 'Package v0.3.10').replace('/releases/tag/v0.3.9', '/releases/tag/v0.3.10') + '\n')
    manifest = {**old, 'schema': 'riskium-published-channel-0310/1', 'published': True, 'source_publication_verified': True,
                'release_id': release['id'], 'documentation_commit': delivery, 'pairs': pairs, 'wiki_files_sha256': wiki_hashes,
                'files_sha256': {p.relative_to(site).as_posix(): curation.sha(p.read_bytes()) for p in sorted(site.rglob('*')) if p.is_file() and p.name != 'publication-manifest.json'}}
    (site / 'publication-manifest.json').write_text(curation.dump(manifest))
    result = compose.audit(output, allow_published=True)
    result.update(status='PASS_PUBLISHED_SOURCE_DELIVERY_BUILD', release_id=release['id'], documentation_commit=delivery, actual_channel_readback=False)
    (output / 'build-receipt.json').write_text(curation.dump(result))
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--candidate', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--downloads', type=Path, required=True)
    a = p.parse_args()
    intent, release, downloads = public_inputs(a.downloads)
    print(curation.dump(build(a.candidate, a.output, intent, release, downloads)))
