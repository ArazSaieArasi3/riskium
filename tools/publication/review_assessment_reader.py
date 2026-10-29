"""Review source-bound candidate guides; public channel readback is a later gate."""
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup
import markdown

ROOT = Path(__file__).resolve().parents[2]
NS = 'documentation/0.4.2'


def verify(root=ROOT):
    root = Path(root)
    policy = json.loads((root / NS / 'policy.json').read_text())
    registry = json.loads((root / NS / 'guide-registry.json').read_text())
    plan = json.loads((root / NS / 'review-plan.json').read_text())
    assert policy['documentation_version'] == registry['documentation_version'] == plan['documentation_version'] == '0.4.2'
    assert policy['source_release'] == 'v0.3.5' and policy['candidate_release'] == 'v0.3.6'
    assert policy['candidate_sql'] == '0.8.0' and policy['model_version'] == '0.3.1'
    assert policy['reader_status'] == 'PENDING_ACTUAL_WIKI_AND_PAGES_READBACK'
    paths = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in (root / NS).rglob('*') if p.is_file() and p.name != 'policy.json'}
    assert paths == policy['files_sha256'], 'Candidate source binding drift'
    prior = json.loads((root / 'documentation/0.4.1/guide-registry.json').read_text())['guides']
    rows = registry['guides']
    assert len(rows) == 21 and [(r['slug'], r['wiki_slug'], r['title']) for r in rows] == [(r['slug'], r['wiki_slug'], r['title']) for r in prior]
    assert len({r['source'] for r in rows}) == 21
    assert [r['id'] for r in plan['candidate_reader_criteria']] == [f'ASL-Q{i:02}' for i in range(1, 7)]
    assert all(r['status'] == 'PENDING_ACTUAL_CHANNEL_REVIEW' for r in plan['candidate_reader_criteria'])
    slugs = {r['slug'] for r in rows}
    for name, journey in plan['audience_paths'].items():
        assert journey[0] == 'Home' and set(journey) <= slugs, 'Broken ' + name + ' journey'
    links = 0
    for row in rows:
        assert row['source'] == NS + '/guides/' + row['slug'] + '.md'
        body = (root / row['source']).read_text()
        soup = BeautifulSoup(markdown.markdown(body, extensions=['tables', 'fenced_code', 'toc', 'md_in_html']), 'html.parser')
        for a in soup.find_all('a', href=True):
            parts = urlsplit(a['href'])
            if parts.scheme or a['href'].startswith('//'):
                assert parts.scheme == 'https', 'Insecure external source: ' + a['href']
                continue
            if parts.path:
                target = unquote(parts.path)
                assert re.fullmatch(r'[A-Za-z][A-Za-z0-9-]*\.md', target), 'Invalid internal link: ' + target
                ident = target[:-3]
                assert ident in slugs, 'Missing guide: ' + ident
                source = next(r['source'] for r in rows if r['slug'] == ident)
                target_soup = BeautifulSoup(markdown.markdown((root / source).read_text(), extensions=['tables', 'fenced_code', 'toc', 'md_in_html']), 'html.parser')
            else:
                target_soup = soup
            if parts.fragment:
                assert target_soup.find(id=unquote(parts.fragment)), 'Missing fragment: ' + a['href']
            links += 1
    home = (root / NS / 'guides/Home.md').read_text()
    database = (root / NS / 'guides/Database-Assurance.md').read_text()
    trace = (root / NS / 'guides/Traceability.md').read_text()
    limits = (root / NS / 'guides/Limitations.md').read_text()
    for value in ('v0.3.5', 'v0.3.6', 'reviewer', 'Domain specialist', 'Developer or integrator'):
        assert value.lower() in home.lower(), 'Opening/version path missing: ' + value
    for value in ('A-v1', 'A-v2', 'A-v3', 'context X', 'context Y', 'WITHDRAWN', 'NO_SELECTION', 'all results owned', 'as-of ledger sequence'):
        assert value.lower() in database.lower(), 'Assessment example missing: ' + value
    assert '460 accounted routes' in trace and 'NOT_CLAIMED_IN_PAPER' in trace
    assert 'six qualitative reader criteria' in limits.lower() and 'v0.3.6 development' in limits
    selected = json.loads((root / 'releases/selection-v0.3.5.json').read_text())['selected_files_sha256']
    assert len(selected) == 687 and all(hashlib.sha256((root / p).read_bytes()).hexdigest() == h for p, h in selected.items())
    return dict(status='CANDIDATE_READER_SOURCE_PASS', guides=21, guide_links=links,
                reader_criteria='SIX_PENDING_ACTUAL_CHANNEL_REVIEW', published_release='v0.3.5',
                candidate_release='v0.3.6', original_selected_files=687)


if __name__ == '__main__':
    print(json.dumps(verify()))
