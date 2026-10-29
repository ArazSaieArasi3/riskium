"""Keep the candidate branch distinct from the published v0.3.5 reader source."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BASE = '41caeaa78c7a152787d1070540e20ae0c6a2395a'
PUBLISHED = '8a9a95bba17327d04c5560879819b2e61b48ff19'
IMMUTABLE = ('documentation/0.4.1', '.github/README.md',
             'tools/publication/published_documentation.py',
             '.github/workflows/published-documentation.yml',
             'docs/releases', 'docs/versions', 'docs/site')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT).decode().strip()


def verify():
    assert git('merge-base', BASE, 'HEAD') == BASE, 'Not based on reviewed main source'
    changed = git('diff', '--name-only', BASE, 'HEAD', '--').splitlines()
    changed += git('diff', '--name-only', BASE, '--').splitlines()
    changed += git('ls-files', '--others', '--exclude-standard').splitlines()
    assert changed and not any(p == fixed or p.startswith(fixed + '/') for fixed in IMMUTABLE for p in changed), 'Published reader or snapshots changed'
    assert git('cat-file', '-t', PUBLISHED) == 'commit', 'Published source missing'
    selected = json.loads((ROOT / 'releases/selection-v0.3.5.json').read_text())['selected_files_sha256']
    assert len(selected) == 687, 'Selected release inventory changed'
    for path, sha in selected.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha, 'Published input changed: ' + path
    assert hashlib.sha256((ROOT / 'tools/publication/published_documentation.py').read_bytes()).hexdigest() == 'c9cd38e15890f05153953f32762f41b28bd1d3789d04de4b32f01bc658dc3c80', 'Old publisher was widened'
    workflow = (ROOT / '.github/workflows/published-documentation.yml').read_text()
    assert 'branches: [main]' in workflow and 'head_branch == \'main\'' in workflow, 'Old reader workflow could run from development'
    candidate = (ROOT / '.github/workflows/assessment-selection.yml').read_text()
    assert 'branches: [plan/v0.3.6-assessment-selection]' in candidate, 'Candidate workflow not branch scoped'
    assert git('diff', '--name-only', BASE, 'HEAD', '--', *IMMUTABLE) == '', 'Reviewed reader payload changed'
    return dict(status='DEVELOPMENT_READER_BOUNDARY_PASS', published_release='v0.3.5',
                candidate_release='v0.3.6', original_selected_files=687, frozen_snapshots=4,
                published_documentation='0.4.1', main_merge='PENDING_R4_SUCCESSOR_AND_GATE_INTEGRATION',
                native_wiki_and_served_pages='UNCHANGED_FROM_PUBLISHED_SOURCE')


if __name__ == '__main__':
    print(json.dumps(verify()))
