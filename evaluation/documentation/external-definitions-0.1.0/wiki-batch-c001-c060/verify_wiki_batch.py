"""Read-only native Wiki acceptance for the bounded C001-C060 publication."""
from pathlib import Path
import argparse, hashlib, json, subprocess

def verify(wiki, expected, output):
    def git(*args):
        return subprocess.check_output(['git', *args], cwd=wiki)
    head = git('rev-parse', 'FETCH_HEAD').decode().strip()
    actual = {name: git('show', head + ':' + name)
              for name in git('ls-tree', '--name-only', head).decode().splitlines()
              if name.endswith('.md')}
    target = {p.name: p.read_bytes() for p in expected.glob('*.md')}
    batch = [f'RKM-C{i:03d}.md' for i in range(1, 61)]
    assert len(target) == 106
    assert all(actual.get(name) == target[name] for name in batch), 'Batch content mismatch'
    matched = sorted(name for name, body in target.items() if actual.get(name) == body)
    remaining = sorted(set(target) - set(matched))
    digest = lambda body: hashlib.sha256(body).hexdigest()
    result = {
        'status': 'C001_C060_NATIVE_WIKI_PUBLICATION_PASS',
        'date': '2026-11-05', 'parent_issue': 85, 'batch_issue': 88,
        'source_commit': '488db8a2336ffe963681e91144d7561e16bddded',
        'documentation_version': '0.4.8', 'review_version': '0.1.0',
        'wiki_commit': head, 'batch_count': len(batch), 'batch_all_bytes_equal': True,
        'actual_wiki_files': len(actual), 'expected_wiki_files': len(target),
        'matched_files': len(matched), 'remaining_files': remaining,
        'full_native_wiki_acceptance': not remaining and set(actual) == set(target),
        'matched_bodies': [{'path': name, 'sha256': digest(target[name]),
                           'bytes': len(target[name]), 'actual_equals_expected': True}
                          for name in matched],
        'remaining': [{'path': name, 'expected_sha256': digest(target[name]),
                       'actual_sha256': digest(actual[name]) if name in actual else None}
                      for name in remaining],
        'independent_ratings': 0, 'new_equivalence_axioms': 0,
        'article_changed': False, 'source_release_changed': False,
    }
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['status', 'wiki_commit', 'batch_count',
                    'actual_wiki_files', 'matched_files', 'full_native_wiki_acceptance']}))

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--wiki', type=Path, required=True)
    p.add_argument('--expected', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    verify(a.wiki, a.expected, a.output)
