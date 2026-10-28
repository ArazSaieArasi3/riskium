"""Offline v0.3.5 release-support checks; no freeze or publication authority.

The immutable #56 selection is anchored here, independently of a supplied source
manifest. A manifest verifies package integrity; its asserted commit identity still
needs the trusted external digest/commit readback required before publication.
"""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

ROOT = Path(__file__).resolve().parents[1]
TAG = 'v0.3.5'
PROFILE = 'releases/stable-profile-v0.3.5.json'
SCREEN = 'evaluation/finalization/v0.3.5-review.json'
NOTES = 'docs/release-v0.3.5.md'
MATRIX = 'releases/selection-v0.3.5.json'
POLICY = 'releases/selection-policy-v0.3.5.json'
OVERLAY = 'releases/development-components-v0.3.5.json'
SELECTION_SOURCE = 'f8e99423fd1e27f315269c8dab17576ab4779455'
STAGE = 'RELEASE_SUPPORT_NOT_FROZEN'
TOOLING = ('tools/release_v035.py', 'tools/prepare_release_v035.py',
           'tests/test_release_v035.py', '.github/workflows/release-support-v035.yml')
SELECTION_HASHES = {
    MATRIX: '99405668004b7b11e9b59dec0df93a94f890b4abb7ba22d5ac4b8914e8bcec32',
    POLICY: '7f21bdd62afde76f7015655effb470fd5f14b5dc719683ac6153ea93a0ad80fc',
    OVERLAY: '969e77f4f5b8c8a3b013f088f5a3671b3f876a8d8c4a7ce7ce8ee8fd6cce1f6e',
}
PRESERVED_INPUTS = {
    'releases/stable-profiles.json': '8d0e1e48afa33fa0829d59885529a5ac55d7bb36b92f9e6d651588c359c0f393',
    'releases/successor-profiles.json': '9d443a595eea67a347b47faef3f8a183a50fa359ab8abb64ff1ce2a36fe276f9',
    'releases/stable-request.json': '39daa6b6e38e0f36a8349d201ce6487da32c98cfa0306a061cf82b4505d3a86e',
    'releases/stable-request-v0.3.4.json': '203da5c89bd1d57bd3716fb8beefffc797501df80def97d49a48099ca35899fb',
    'releases/development-request.json': '543829689995488eb547bc4c220f03e7a21a4d30f0534d2dd9b7549e3b282c9e',
    'releases/stable-profile-v0.3.1.json': '2d1a4e9e7530fa71eef6b9f21d9c4de09209c501bff980978c3069d4f26fb8d1',
    'releases/stable-profile-v0.3.2.json': '9710df8a93ebd081ce15b614d773c335e7d3a7cd59722da7e09abfdb23353088',
    'releases/stable-profile-v0.3.3.json': 'fcadf833aa615a508bd97a08de83625edb5d866f89a6dc2ddfbe796f0f8425c8',
    'releases/stable-profile-v0.3.4.json': 'da66c5327a88ff89a90783128f9a085909b70f2588e17d6ec25d8dee8d7b8a81',
    'tools/prepare_stable_release.py': '05ccf8a87b91fee50103bfdb549c3006497bbd992c025c6310597ebb7cd14f63',
    'tools/prepare_incremental_release.py': 'e860c2f5250d548ecdc18694a207e642b25f8ee52a226f0ddb55c4b6918b301a',
    '.github/workflows/incremental-release.yml': 'b87d98fea2a6b14244e1a47f1e29ff6ef618a3285e4b40d6dc7b878d29997d93',
    'tools/publish_stable_release.py': '195fbc8b8ace98e50cd54471b6d4c1fad67853a502fefc073a6bfea89e0ffc2f',
    'tools/resolve_release_request.py': 'dfa58857dd1c33a320adf84226e75437be27cfc14e714ef1bb78ec3757def1fc',
    'tools/release_v034.py': '85e55a263e846c9ac5e8bb6e2bd006f49edb8cc9834490b2aa14ef60e51f2d4b',
    'tools/prepare_release_v034.py': '8c688097a778567ae0ae4b1d64ac8162deca2618bd120a3c0aa9a891fa0913eb',
    '.github/workflows/stable-release.yml': 'e3f353895b966c8066faf6718a803c0272c7727c46830b891683427c07f3f23b',
    'evaluation/releases/v0.3.5-definition/published-baseline.json': 'e153ff2e7a54d2f921523e7a5d7f52668386a38f709fb3c6f8894223787810bb',
}
SCIENCE = dict(model='0.3.1', orsd='0.4.3', original_drsd='0.1.0', manuscript='7.0.8')
GATES = ('publication_requires_clean_exact_head', 'publication_requires_all_checks',
         'publication_requires_no_known_unresolved_critical_findings',
         'publication_requires_new_tag_and_release', 'readback_required',
         'package_requires_offline_validation', 'final_source_channel_readback_required')
FUTURE_GATES = (
    'Clean exact source HEAD and complete affected source/full software checks.',
    'Fresh actual documentation 0.4.0 Wiki (23 files) and Pages (311 served files plus root manifest) readback at the final source; preserve four frozen snapshots.',
    'Dry freeze and independent validation of all six staged release assets.',
    'Explicit publication activation only after successful reviewed freeze.',
    'Independent actual public downloads, tag/Latest and all eleven prior release/asset inventories.',
)


class MissingSource(ValueError):
    """A required public source file is absent."""


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(value):
    require(isinstance(value, str) and value and '\\' not in value and '\0' not in value,
            'V035-SUPPORT-UNSAFE-PATH')
    parts = value.split('/')
    require(not value.startswith('/') and all(p not in ('', '.', '..', '.git') for p in parts)
            and PurePosixPath(value).as_posix() == value, 'V035-SUPPORT-UNSAFE-PATH: ' + value)
    return value


def reader(root):
    root = Path(root)
    require(root.is_dir() and not root.is_symlink(), 'V035-SUPPORT-ROOT')

    def read(path):
        path = safe_path(path)
        target = root
        for part in path.split('/'):
            target = target / part
            require(not target.is_symlink(), 'V035-SUPPORT-SYMLINK: ' + path)
        require(target.resolve().is_relative_to(root.resolve()), 'V035-SUPPORT-ESCAPE')
        if not target.exists():
            raise MissingSource('V035-SUPPORT-MISSING: ' + path)
        require(target.is_file(), 'V035-SUPPORT-NONFILE: ' + path)
        return target.read_bytes()
    return read


def read_blob(blob, path):
    path = safe_path(path)
    try:
        data = blob(path)
    except (FileNotFoundError, KeyError) as error:
        raise MissingSource('V035-SUPPORT-MISSING: ' + path) from error
    require(isinstance(data, bytes), 'V035-SUPPORT-NONBYTES: ' + path)
    return data


def hashes(bindings, blob):
    require(isinstance(bindings, dict) and bindings, 'V035-SUPPORT-HASHES')
    for path, digest in bindings.items():
        require(isinstance(digest, str) and re.fullmatch('[a-f0-9]{64}', digest),
                'V035-SUPPORT-DIGEST: ' + str(path))
        require(sha(read_blob(blob, path)) == digest, 'V035-SUPPORT-STALE: ' + path)


def validate_matrix(matrix, blob):
    """Validate the anchored #56 selection using only the supplied source bytes."""
    hashes(SELECTION_HASHES, blob)
    require(matrix == json.loads(read_blob(blob, MATRIX)), 'V035-SUPPORT-MATRIX-VALUE')
    policy = json.loads(read_blob(blob, POLICY))
    overlay = json.loads(read_blob(blob, OVERLAY))
    require(matrix['schema'] == 'riskium-v035-component-selection-v1'
            and matrix['target'] == TAG and matrix['stage'] == 'COMPONENT_SELECTION_NOT_FROZEN'
            and matrix['issue'] == 56 and matrix['parent_issue'] == 51, 'V035-SUPPORT-SELECTION-IDENTITY')
    require(matrix['scientific_versions'] == SCIENCE and policy['scientific_versions'] == SCIENCE,
            'V035-SUPPORT-SCIENCE')
    require(matrix['policy_path'] == POLICY and matrix['policy_sha256'] == SELECTION_HASHES[POLICY]
            and matrix['overlay_path'] == OVERLAY and matrix['overlay_sha256'] == SELECTION_HASHES[OVERLAY]
            and overlay['target'] == TAG, 'V035-SUPPORT-SELECTION-CLOSURE')
    require(matrix['boundaries'] == policy['boundaries']
            and matrix['boundaries']['independent_validation_claimed'] is False
            and matrix['boundaries']['publication_requested'] is False, 'V035-SUPPORT-SELECTION-SCOPE')
    rows = matrix['artifacts']
    versions = {r['id']: r['version'] for r in rows}
    require(len(versions) == len(rows) == 29 and versions['CONSISTENCY'] == '0.3.0'
            and versions['DOCUMENTATION'] == '0.4.0'
            and versions['EVIDENCE_REFERENCE_LIFECYCLE'] == '0.7.0', 'V035-SUPPORT-COMPONENTS')
    require(all(r['compatible_model'] == '0.3.1' for r in rows), 'V035-SUPPORT-COMPATIBILITY')
    graph = matrix['dependencies']
    require(set(graph) == set(versions) and sum(map(len, graph.values())) == 68, 'V035-SUPPORT-DEPENDENCIES')
    active, visited = set(), set()

    def visit(ident):
        require(ident not in active, 'V035-SUPPORT-CYCLE')
        if ident in visited:
            return
        active.add(ident)
        seen = set()
        for dep in graph[ident]:
            require(dep['id'] in versions and versions[dep['id']] == dep['version']
                    and dep['id'] not in seen, 'V035-SUPPORT-DEPENDENCY-VERSION')
            seen.add(dep['id'])
            visit(dep['id'])
        active.remove(ident)
        visited.add(ident)
    for ident in graph:
        visit(ident)
    inventory = matrix['selected_files_sha256']
    require(len(inventory) == 687 and set(matrix['file_owners']) == set(inventory), 'V035-SUPPORT-INVENTORY')
    hashes(inventory, blob)
    for row in rows:
        files = {f['path']: f['sha256'] for f in row['files']}
        require(len(files) == len(row['files']) and all(inventory.get(p) == h for p, h in files.items()),
                'V035-SUPPORT-COMPONENT-FILES')
    hashes(matrix['selection_tooling_sha256'], blob)
    hashes(policy['preserved_registers_sha256'], blob)
    hashes(policy['evidence_receipts_sha256'], blob)
    hashes(policy['documentation_runtime_support_sha256'], blob)
    hashes(policy['frozen_snapshot_files_sha256'], blob)
    require(len(policy['frozen_snapshot_files_sha256']) == 237, 'V035-SUPPORT-FROZEN-SNAPSHOTS')
    old = json.loads(read_blob(blob, matrix['baseline_matrix']))
    require(sha(read_blob(blob, matrix['baseline_matrix'])) == matrix['baseline_matrix_sha256']
            and len(old['selected_files_sha256']) == 380, 'V035-SUPPORT-BASELINE')
    require(all(inventory.get(p) == h for p, h in old['selected_files_sha256'].items()),
            'V035-SUPPORT-BASELINE-PRESERVATION')
    require(matrix['historical_generation_components'] == policy['historical_generation_components']
            and matrix['historical_generation_dependencies'] == policy['historical_generation_dependencies']
            and {(r['id'], r['version']) for r in matrix['historical_generation_components']}
            == {('DOCUMENTATION', '0.3.0'), ('CONSISTENCY', '0.2.0')}, 'V035-SUPPORT-HISTORICAL-GENERATION')
    for row in matrix['historical_generation_components']:
        hashes({f['path']: f['sha256'] for f in row['files']}, blob)
    chain = matrix['sqlite_migration_chain']
    require([s['to_schema'] for s in chain] == [2, 3, 4, 5, 6, 7, 8], 'V035-SUPPORT-MIGRATION-CHAIN')
    previous = 0
    for step in chain:
        require(step['from_schema'] == previous and all(p in inventory for p in
                [step['reader'], *step['migration_files']]), 'V035-SUPPORT-MIGRATION-GAP')
        hashes(step['source_files_sha256'], blob)
        previous = step['to_schema']
    sql = 'implementation/relational/0.7.0/008_evidence_lifecycle.sql'
    require(chain[-1]['schema_migration_ledger_sha256']['8'] == sha(read_blob(blob, sql)),
            'V035-SUPPORT-MIGRATION-LEDGER')
    outputs = matrix['generated_outputs']
    require(outputs['documentation_version'] == '0.4.0' and len(outputs['current_files_sha256']) == 68
            and len(outputs['wiki_files_sha256']) == 23 and len(outputs['all_served_files_sha256']) == 311
            and outputs['historical_source_bound_not_fresh_replayed'] is True, 'V035-SUPPORT-CHANNEL-SCOPE')
    hashes({'documentation/0.4.0/wiki/' + p: h for p, h in outputs['wiki_files_sha256'].items()}, blob)
    require(len(matrix['preserve_releases']) == 11 and matrix['preserve_releases'][-1] == 'v0.3.4',
            'V035-SUPPORT-PRIOR-RELEASES')
    return matrix


def validate_profile_blob(profile, blob):
    require(profile['schema'] == 'riskium-v035-prospective-release-profile-v1'
            and profile['stage'] == STAGE and profile['tag'] == TAG
            and profile['baseline_release'] == 'v0.3.4'
            and profile['selection_source_commit'] == SELECTION_SOURCE, 'V035-SUPPORT-PROFILE')
    for key in ('registered_for_publication', 'publication_executed', 'source_freeze_executed',
                'independent_validation_claimed', 'full_original_requirement_acceptance_claimed'):
        require(profile.get(key) is False, 'V035-SUPPORT-UNSUPPORTED-AUTHORITY: ' + key)
    require(profile['scientific_versions'] == SCIENCE and profile['model_version'] == '0.3.1'
            and profile['orsd_revision'] == '0.4.3' and profile['manuscript_version'] == '7.0.8'
            and profile['reviewed_scope_commit'] == '3afa861b5296addefc98ce401767c7ab7d025d2c'
            and profile['accepted_scope'] == 'evaluation/owner-review/accepted-scope.json', 'V035-SUPPORT-PROFILE-SCIENCE')
    require(all(profile.get(key) is True for key in GATES), 'V035-SUPPORT-MISSING-GATE')
    require(profile['artifact_matrix'] == MATRIX and profile['artifact_matrix_sha256'] == SELECTION_HASHES[MATRIX]
            and profile['critical_screen'] == SCREEN and profile['notes'] == NOTES, 'V035-SUPPORT-PROFILE-PATHS')
    require(set(profile['release_tooling_sha256']) == set(TOOLING), 'V035-SUPPORT-TOOLING-CLOSURE')
    hashes(profile['release_tooling_sha256'], blob)
    hashes({NOTES: profile['notes_sha256']}, blob)
    hashes(PRESERVED_INPUTS, blob)
    for path in ('releases/stable-request-v0.3.5.json', 'releases/successor-request-v0.3.5.json'):
        try:
            read_blob(blob, path)
        except MissingSource:
            continue
        raise ValueError('V035-SUPPORT-PREMATURE-REQUEST: ' + path)
    matrix = validate_matrix(json.loads(read_blob(blob, MATRIX)), blob)
    screen = json.loads(read_blob(blob, SCREEN))
    require(screen['schema'] == 'riskium-v035-release-support-screen-v1' and screen['target'] == TAG
            and screen['stage'] == STAGE and screen['component_matrix_sha256'] == SELECTION_HASHES[MATRIX]
            and screen.get('selection_source_commit') == SELECTION_SOURCE
            and screen['release_tooling_sha256'] == profile['release_tooling_sha256']
            and screen['notes_sha256'] == profile['notes_sha256'], 'V035-SUPPORT-SCREEN')
    require(screen['known_unresolved_critical_findings'] == []
            and screen['new_owner_responses_generated'] == 0
            and screen['independent_semantic_review_claimed'] is False
            and screen['universal_zero_defect_claimed'] is False
            and screen.get('source_freeze_executed') is False
            and screen.get('publication_executed') is False
            and screen['material_scientific_change_since_owner_acceptance'] is False, 'V035-SUPPORT-SCREEN-SCOPE')
    risks = screen['reviewed_risks']
    require(len(risks) >= 8 and len({r['id'] for r in risks}) == len(risks), 'V035-SUPPORT-RISK-SET')
    for risk in risks:
        require(isinstance(risk['id'], str) and risk['id'] and risk['fresh_gate'] and risk['retained_evidence'],
                'V035-SUPPORT-RISK-GATE')
        for path in risk['retained_evidence']:
            require(bool(read_blob(blob, path)), 'V035-SUPPORT-RISK-EVIDENCE')
    require(screen['future_freeze_gates'] == list(FUTURE_GATES), 'V035-SUPPORT-FUTURE-GATES')
    return matrix


def validate_profile(root=ROOT):
    blob = reader(root)
    profile = json.loads(read_blob(blob, PROFILE))
    validate_profile_blob(profile, blob)
    return profile


def required_paths(matrix):
    return set(matrix['selected_files_sha256']) | set(TOOLING) | set(PRESERVED_INPUTS) | set(SELECTION_HASHES) | {PROFILE, SCREEN, NOTES}


def validate_source_manifest(manifest, blob):
    """Check full manifest entries plus immutable required-file closure, offline."""
    require(manifest['schema'] in ('riskium-incremental-inventory-v1', 'riskium-stable-source-inventory-v1'),
            'V035-SUPPORT-MANIFEST-SCHEMA')
    if manifest['schema'] == 'riskium-stable-source-inventory-v1':
        require(manifest.get('tag') == TAG, 'V035-SUPPORT-MANIFEST-TAG')
    require(isinstance(manifest['source_commit'], str)
            and re.fullmatch('[a-f0-9]{40}', manifest['source_commit']), 'V035-SUPPORT-MANIFEST-SOURCE')
    files = manifest['files']
    require(isinstance(files, list) and type(manifest['file_count']) is int
            and manifest['file_count'] == len(files), 'V035-SUPPORT-MANIFEST-COUNT')
    seen = set()
    for entry in files:
        path = safe_path(entry['path'])
        require(path not in seen, 'V035-SUPPORT-MANIFEST-DUPLICATE: ' + path)
        seen.add(path)
        require(type(entry['bytes']) is int and entry['bytes'] >= 0, 'V035-SUPPORT-MANIFEST-SIZE')
        raw = read_blob(blob, path)
        require(len(raw) == entry['bytes'] and isinstance(entry['sha256'], str)
                and re.fullmatch('[a-f0-9]{64}', entry['sha256']) and sha(raw) == entry['sha256'],
                'V035-SUPPORT-MANIFEST-BYTES: ' + path)
    profile = json.loads(read_blob(blob, PROFILE))
    matrix = validate_profile_blob(profile, blob)
    require(required_paths(matrix) <= seen, 'V035-SUPPORT-MANIFEST-CRITICAL-OMISSION')
    return manifest


def validate_unpacked(root, manifest=None):
    """Validate a source-only unpacked tree; with manifest require an exact file set."""
    root = Path(root)
    blob = reader(root)
    actual = set()
    for path in root.rglob('*'):
        relative = path.relative_to(root).as_posix()
        safe_path(relative)
        require(not path.is_symlink(), 'V035-SUPPORT-SYMLINK: ' + relative)
        require(path.is_file() or path.is_dir(), 'V035-SUPPORT-NONREGULAR: ' + relative)
        if path.is_file():
            actual.add(relative)
    profile = json.loads(read_blob(blob, PROFILE))
    matrix = validate_profile_blob(profile, blob)
    if manifest is not None:
        validate_source_manifest(manifest, blob)
        require(actual == {r['path'] for r in manifest['files']}, 'V035-SUPPORT-MANIFEST-FILE-SET')
    return dict(status='V035_RELEASE_SUPPORT_OFFLINE_PASS', tag=TAG, stage=STAGE,
                selected_components=29, selected_files=687, dependency_edges=68,
                source_files=len(actual), complete_manifest_verified=manifest is not None,
                source_commit_authenticated=False, source_freeze_executed=False,
                registered_for_publication=False, publication_executed=False)
