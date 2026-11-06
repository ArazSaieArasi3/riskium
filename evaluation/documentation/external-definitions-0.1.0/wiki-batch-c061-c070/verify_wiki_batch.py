"""Read-only acceptance for the ten-body C061-C070 native Wiki publication."""
from pathlib import Path
import argparse, hashlib, json, subprocess

SOURCE = '488db8a2336ffe963681e91144d7561e16bddded'
PREVIOUS = '9858df83390cafa07249ad8ac6469d9d3b6df440'

def verify(wiki, expected, status_path, output):
    def git(*args):
        return subprocess.check_output(['git', *args], cwd=wiki)
    digest = lambda body: hashlib.sha256(body).hexdigest()
    head = git('rev-parse', 'FETCH_HEAD').decode().strip()
    target = {p.name: p.read_bytes() for p in expected.glob('*.md')}
    status = json.loads(status_path.read_text())
    assert status['documentation_source_commit'] == SOURCE
    assert status['documentation_version'] == '0.4.8'
    assert len(target) == 106
    assert {n: digest(b) for n, b in target.items()} == status['wiki_files_sha256']
    actual = {name: git('show', head + ':' + name)
              for name in git('ls-tree', '--name-only', head).decode().splitlines()
              if name.endswith('.md')}
    batch = [f'RKM-C{i:03d}.md' for i in range(61, 71)]
    prior_names = git('ls-tree', '--name-only', PREVIOUS).decode().splitlines()
    prior_matched = sorted(n for n in prior_names if n in target
                           and git('show', PREVIOUS + ':' + n) == target[n])
    assert len(prior_matched) == 80, 'Unexpected previous acceptance checkpoint'
    assert all(actual.get(n) == target[n] for n in batch), 'New batch body mismatch'
    assert all(actual.get(n) == target[n] for n in prior_matched), 'Previous content changed'
    changed = sorted(git('diff', '--name-only', PREVIOUS, head).decode().splitlines())
    assert changed == sorted(batch), 'Changes outside the ten-body scope'
    matched = sorted(n for n, body in target.items() if actual.get(n) == body)
    remaining = sorted(set(target) - set(matched))
    result = {
        'status': 'C061_C070_NATIVE_WIKI_PUBLICATION_PASS',
        'date': '2026-11-06', 'parent_issue': 85, 'batch_issue': 89,
        'source_commit': SOURCE, 'documentation_version': '0.4.8',
        'review_version': '0.1.0', 'previous_wiki_commit': PREVIOUS,
        'wiki_commit': head, 'batch_count': len(batch),
        'batch_all_bytes_equal': True, 'previous_equal_bodies_preserved': len(prior_matched),
        'changed_paths': changed, 'ci_projection_manifest_match': True,
        'actual_wiki_files': len(actual), 'expected_wiki_files': len(target),
        'matched_files': len(matched), 'concept_dossiers_matched': sum(n.startswith('RKM-') for n in matched),
        'remaining_files': remaining,
        'full_native_wiki_acceptance': not remaining and set(actual) == set(target),
        'matched_bodies': [{'path': n, 'sha256': digest(target[n]),
                           'bytes': len(target[n]), 'actual_equals_expected': True} for n in matched],
        'remaining': [{'path': n, 'expected_sha256': digest(target[n]),
                       'actual_sha256': digest(actual[n]) if n in actual else None} for n in remaining],
        'independent_ratings': 0, 'new_equivalence_axioms': 0,
        'article_changed': False, 'source_release_changed': False,
    }
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['status', 'wiki_commit', 'batch_count',
                     'previous_equal_bodies_preserved', 'matched_files', 'full_native_wiki_acceptance']}))

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--wiki', type=Path, required=True)
    p.add_argument('--expected', type=Path, required=True)
    p.add_argument('--published-status', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    verify(a.wiki, a.expected, a.published_status, a.output)
