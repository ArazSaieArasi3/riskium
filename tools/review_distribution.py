"""Validate explicitly selected successor components and actual Wiki/Pages bytes.

This is release engineering evidence, not a new owner or independent judgment.
Only fixed public project URLs are read. Authentication is neither used nor copied.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://arazsaiearasi3.github.io/riskium/'
WIKI = 'https://github.com/ArazSaieArasi3/riskium.wiki.git'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(root, path):
    return json.loads((Path(root) / path).read_bytes())


def safe_path(path):
    require(isinstance(path, str), 'Invalid component path')
    p = PurePosixPath(path)
    require(path and not p.is_absolute() and str(p) == path and '..' not in p.parts and '\\' not in path,
            'Unsafe component path')
    return path


def validate_matrix(matrix, blob):
    """Same hash/compatibility validation for a checkout and downloaded archive."""
    require(matrix['schema'] == 'riskium-successor-component-matrix-v1', 'Unknown distribution matrix')
    require(matrix['tag'] == 'v0.3.2' and matrix['model_version'] == '0.3.1', 'Unreviewed distribution/model pair')
    rows = matrix['artifacts']
    require(len(rows) == len({x['id'] for x in rows}) == 20, 'Missing/duplicate selected component')
    require(matrix['new_owner_ratings'] == 0 and matrix['independent_validation_claimed'] is False,
            'Unsupported review claim')
    for path, expected in matrix['source_registers_sha256'].items():
        require(sha(blob(safe_path(path))) == expected, 'Selected component register drift: ' + path)
    baseline = json.loads(blob('releases/artifact-matrix.json'))
    overlay = json.loads(blob('releases/development-components.json'))
    require(rows[:10] == baseline['artifacts'] and rows[10:18] == overlay['components'],
            'Selection differs from the accepted baseline/development overlay')
    require(rows[18]['id'] == 'DOCUMENTATION' and rows[18]['version'] == '0.1.0' and
            rows[19]['id'] == 'RIGHTS_AND_MODEL_CITATION', 'Documentation/rights selection mismatch')
    for row in rows:
        require(row['compatible_model'] == matrix['model_version'], 'Incompatible selected component')
        paths = [safe_path(x['path']) for x in row['files']]
        require(len(paths) == len(set(paths)) and paths, 'Empty/duplicate component files')
        for item in row['files']:
            require(sha(blob(item['path'])) == item['sha256'], 'Selected artifact byte drift: ' + item['path'])
    docs = matrix['documentation']
    registry = json.loads(blob('tools/publication/pages-registry.json'))
    require(docs['snapshot'] == registry['releases']['v0.3.1'], 'Frozen documentation selection drift')
    require(docs['wiki_receipt'] == 'evaluation/documentation/versioned-0.1.0/wiki-final-readback.json',
            'Unreviewed Wiki receipt')
    wiki = json.loads(blob(docs['wiki_receipt']))
    require(sha(blob('tools/publication/guide-registry.json')) == wiki['guide_registry_sha256'],
            'Stale Wiki registry receipt')
    for path, expected in wiki['explanatory_sources_sha256'].items():
        require(sha(blob(safe_path(path))) == expected, 'Stale Wiki explanatory source: ' + path)
    for name, expected in wiki['wiki_files_sha256'].items():
        require(sha(blob('docs/wiki/' + safe_path(name))) == expected, 'Stale Wiki projection: ' + name)
    require(len(docs['current_files_sha256']) == 53, 'Incomplete current documentation inventory')
    for name, expected in docs['current_files_sha256'].items():
        require(sha(blob('docs/current/' + safe_path(name))) == expected, 'Current Pages source drift: ' + name)
    require(matrix['preserve_releases'] == ['v0.3.1-rc.' + str(i) for i in range(1, 8)] + ['v0.3.1'],
            'Prior stable/prerelease preservation scope missing')
    return matrix


def validate_distribution(root, profile):
    root = Path(root)
    require(profile['tag'] == 'v0.3.2' and profile['profile'] == 'stable-bounded-research-artifact',
            'Unreviewed successor profile')
    for key in ('publication_requires_clean_exact_head', 'publication_requires_all_checks',
                'publication_requires_no_known_unresolved_critical_findings',
                'publication_requires_new_tag_and_release', 'readback_required'):
        require(profile.get(key) is True, 'Missing successor gate: ' + key)
    require(profile['model_version'] == '0.3.1' and profile['orsd_revision'] == '0.4.3' and
            profile['manuscript_version'] == '7.0.8', 'Unreviewed successor scientific versions')
    require(profile['independent_validation_claimed'] is False and
            profile['full_original_requirement_acceptance_claimed'] is False, 'Unsupported successor claim')
    matrix = read(root, profile['artifact_matrix'])
    validate_matrix(matrix, lambda path: (root / path).read_bytes())
    screen = read(root, profile['critical_screen'])
    require(screen['target'] == profile['tag'] and screen['known_unresolved_critical_findings'] == [] and
            screen['material_scientific_change_since_owner_acceptance'] is False and
            screen['new_owner_responses_generated'] == 0 and screen['independent_semantic_review_claimed'] is False and
            screen['universal_zero_defect_claimed'] is False, 'Invalid successor critical screen')
    require(screen['component_matrix_sha256'] == sha((root / profile['artifact_matrix']).read_bytes()),
            'Critical screen not bound to selected matrix')
    require((root / profile['notes']).is_file(), 'Missing successor notes')
    return matrix


def validate_freshness(matrix, receipt, now=None):
    require(receipt['schema'] == 'riskium-successor-live-readback-v1' and receipt['all_bytes_match'] is True,
            'Missing actual live publication readback')
    require(receipt['component_matrix_sha256'] == sha((json.dumps(matrix, indent=2) + '\n').encode()),
            'Live readback selected-component mismatch')
    require(receipt['wiki_commit'] == matrix['documentation']['wiki_commit'] and
            receipt['wiki_files'] == 23 and receipt['current_files'] == 53 and receipt['frozen_files'] == 53,
            'Incomplete live Wiki/Pages readback')
    docs = matrix['documentation']
    expected = {'current/' + p: h for p, h in docs['current_files_sha256'].items()}
    expected.update({docs['snapshot']['route'] + '/' + p: h for p, h in docs['snapshot']['files_sha256'].items()})
    require(receipt['files_sha256'] == expected, 'Live Pages readback inventory mismatch')
    age = ((now or datetime.now(timezone.utc)) - datetime.fromisoformat(receipt['checked_at_utc'])).total_seconds()
    require(0 <= age < 86400, 'Stale or future live publication readback')


def live_readback(root, profile):
    root = Path(root)
    matrix = validate_distribution(root, profile)
    docs = matrix['documentation']
    wiki_receipt = read(root, docs['wiki_receipt'])
    with tempfile.TemporaryDirectory() as folder:
        subprocess.run(['git', 'clone', '--quiet', '--depth=1', WIKI, folder], check=True,
                       stdout=subprocess.DEVNULL, timeout=90)
        commit = subprocess.check_output(['git', '-C', folder, 'rev-parse', 'HEAD'], text=True).strip()
        actual = {p.name: sha(p.read_bytes()) for p in Path(folder).glob('*.md')}
        require(commit == docs['wiki_commit'] and actual == wiki_receipt['wiki_files_sha256'],
                'Actual native Wiki differs from selected registry/source/projection')
    def fetch(path):
        safe_path(path)
        with urllib.request.urlopen(SITE + path, timeout=30) as response:
            require(response.status == 200 and response.url.startswith(SITE), 'Unexpected Pages response')
            return response.read()
    manifest_bytes = fetch('publication-manifest.json')
    manifest = json.loads(manifest_bytes)
    require(re.fullmatch('[0-9a-f]{40}', manifest['current_source_commit']), 'Invalid deployed source identity')
    require(subprocess.run(['git', 'merge-base', '--is-ancestor', manifest['current_source_commit'], 'HEAD'],
                           cwd=root).returncode == 0, 'Deployed Pages source is not a release ancestor')
    expected = {'current/' + p: h for p, h in docs['current_files_sha256'].items()}
    expected.update({docs['snapshot']['route'] + '/' + p: h for p, h in docs['snapshot']['files_sha256'].items()})
    from concurrent.futures import ThreadPoolExecutor
    def check(item):
        path, expected_sha = item
        require(manifest['files_sha256'].get(path) == expected_sha and sha(fetch(path)) == expected_sha,
                'Actual Pages bytes differ from selected input: ' + path)
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(check, expected.items()))
    receipt = dict(schema='riskium-successor-live-readback-v1', checked_at_utc=datetime.now(timezone.utc).isoformat(),
                   component_matrix_sha256=sha((root / profile['artifact_matrix']).read_bytes()),
                   wiki_commit=commit, wiki_files=len(actual), current_files=53, frozen_files=53,
                   pages_source_commit=manifest['current_source_commit'], pages_manifest_sha256=sha(manifest_bytes),
                   files_sha256=expected, all_bytes_match=True,
                   scope='Fresh native Git clone and actual HTTPS bytes; no new browser or semantic review.')
    validate_freshness(matrix, receipt)
    return receipt


if __name__ == '__main__':
    p = read(ROOT, 'releases/stable-profile-v0.3.2.json')
    receipt = ROOT/'evaluation/releases/v0.3.2-publication.json'
    if receipt.is_file():
        # Current documentation may evolve after a published distribution. Its
        # immutable selection is checked at the recorded/tagged source, not
        # silently rebound to later current-page bytes.
        released = json.loads(receipt.read_bytes())
        commit = released['source_commit']
        require(released['publication_state'] == 'PUBLISHED_AND_INDEPENDENTLY_DOWNLOADED_VERIFIED', 'Unverified published distribution')
        require(subprocess.check_output(['git','rev-parse','v0.3.2^{commit}'],cwd=ROOT,text=True).strip() == commit, 'Published distribution tag moved')
        def blob(path):
            return subprocess.check_output(['git','show',commit+':'+safe_path(path)],cwd=ROOT)
        require((ROOT/p['artifact_matrix']).read_bytes() == blob(p['artifact_matrix']), 'Published selection matrix changed')
        m = json.loads(blob(p['artifact_matrix']))
        validate_matrix(m, blob)
        status = 'PUBLISHED_DISTRIBUTION_EXACT_SOURCE_PASS'
    else:
        m = validate_distribution(ROOT, p)
        status = 'SUCCESSOR_COMPONENT_SELECTION_PASS'
    print(json.dumps({'status': status, 'tag': m['tag'], 'components': len(m['artifacts'])}))
