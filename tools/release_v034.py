"""Reviewed v0.3.4 release gates; original published profile contracts stay intact."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import copy
import json
from pathlib import Path
import re
import subprocess
import tempfile
import urllib.request

import build_prepared_distribution as prepared
import prepare_stable_release as stable

ROOT = prepared.ROOT
TAG = 'v0.3.4'
REGISTRY = 'releases/successor-profiles.json'
PROFILE = 'releases/stable-profile-v0.3.4.json'
REQUEST = 'releases/stable-request-v0.3.4.json'
SCREEN = 'evaluation/finalization/v0.3.4-review.json'
NOTES = 'docs/release-v0.3.4.md'
SITE = 'https://arazsaiearasi3.github.io/riskium/'
WIKI = 'https://github.com/ArazSaieArasi3/riskium.wiki.git'
TOOLING = ('tools/release_v034.py', 'tools/prepare_release_v034.py',
           'tools/prepare_stable_release.py', 'tools/publish_stable_release.py',
           'tests/test_release_v034.py', '.github/workflows/stable-release.yml')
EXTRA_CHECKS = [['tools/build_prepared_distribution.py', '--check'],
                ['tools/publication/snapshot_registry.py', '--check'],
                ['tools/publication/build_snapshot_site.py', '--check'],
                ['tools/prepare_release_v034.py', '--check-profile'],
                ['tools/run_relational_source_scenario.py', '--check'],
                ['tools/build_source_scenario_inventory.py', '--check'],
                ['tools/run_relational_source_scenario_lineage.py', '--check'],
                ['tools/build_source_scenario_lineage_inventory.py', '--check'],
                ['tools/run_relational_evidence.py', '--check'],
                ['tools/build_evidence_inventory.py', '--check']]

require = stable.require
sha = stable.sha


def profile_path(root, tag=TAG):
    require(tag == TAG, 'Unreviewed v0.3.4 profile tag')
    registry = json.loads((Path(root) / REGISTRY).read_bytes())
    require(registry['schema'] == 'riskium-reviewed-successor-profiles-v1'
            and registry['profiles'].get(TAG) == PROFILE, 'Unregistered v0.3.4 profile')
    return PROFILE


def validate_matrix(matrix, blob):
    """Self-contained archive checks: no Git history or network is required."""
    require(matrix['schema'] == 'riskium-successor-component-matrix-v1' and matrix['tag'] == TAG
            and matrix['stage'] == 'COMPONENTS_PREPARED_NOT_FROZEN', 'Unreviewed prepared matrix')
    policy = json.loads(blob(prepared.POLICY))
    require(matrix['policy_path'] == prepared.POLICY and matrix['policy_sha256'] == sha(blob(prepared.POLICY))
            and policy['approved_source'] == prepared.SOURCE and policy['target'] == TAG
            and policy['issue'] == 49 and policy['parent_issue'] == 45, 'Prepared policy/source mismatch')
    require(set(policy['preserved_inputs_sha256']) == set(prepared.INPUTS), 'Missing prepared source bindings')
    require(matrix['source_registers_sha256'] == policy['preserved_inputs_sha256'], 'Prepared input closure mismatch')
    for path, digest in policy['preserved_inputs_sha256'].items():
        require(sha(blob(prepared.initial.safe_path(path))) == digest, 'Preserved prepared input drift: ' + path)
    old = json.loads(blob(policy['initial_selection']))
    snapshot = prepared.initial.descriptor_row(policy['snapshot'], blob)
    snapshot['scope'] = 'Completed immutable documentation 0.3.0/model 0.3.1 snapshot and exact deployment/tooling/evidence; no source publication or new domain acceptance.'
    rows = copy.deepcopy(old['artifacts']) + [snapshot]
    require(matrix['artifacts'] == rows and len(rows) == len({r['id'] for r in rows}) == 28, 'Prepared component selection differs')
    require(all(r['compatible_model'] == '0.3.1' for r in rows), 'Prepared component model differs')
    graph = copy.deepcopy(old['dependencies']); graph['DOCUMENTATION_SNAPSHOT'] = copy.deepcopy(prepared.DEPS)
    require(matrix['dependencies'] == graph and policy['snapshot']['depends_on'] == prepared.DEPS, 'Prepared dependency graph differs')
    prepared.initial.dependency_order({r['id']:r['version'] for r in rows}, graph)
    position = {r['id']:i for i,r in enumerate(rows)}
    require(all(position[d['id']] < position[i] for i,ds in graph.items() for d in ds), 'Prepared dependency order differs')
    docs, publication = prepared.documentation(snapshot, blob)
    require(matrix['documentation'] == docs and matrix['publication_support_sha256'] == publication, 'Prepared deployment selection differs')
    tooling = {p:sha(blob(p)) for p in prepared.TOOLING}
    require(matrix['selection_tooling_sha256'] == tooling, 'Prepared tooling drift')
    support = [dict(id='PREPARATION_INPUTS',files=[dict(path=p,sha256=h) for p,h in policy['preserved_inputs_sha256'].items()]),
               dict(id='PUBLICATION_SUPPORT',files=[dict(path=p,sha256=h) for p,h in publication.items()])]
    inventory, owners = prepared.initial.file_inventory(rows + support, tooling, blob)
    require(matrix['selected_files_sha256'] == inventory and matrix['file_owners'] == owners
            and len(inventory) == 380, 'Prepared inventory differs')
    require(matrix['model_version'] == '0.3.1' and matrix['orsd_revision'] == '0.4.3'
            and matrix['manuscript_version'] == '7.0.8' and matrix['scientific_versions'] == old['scientific_versions']
            and matrix['preparation_boundaries'] == prepared.BOUNDARIES, 'Unreviewed scientific scope')
    require(matrix['preserve_releases'] == ['v0.3.1-rc.'+str(n) for n in range(1,8)] + ['v0.3.1','v0.3.2','v0.3.3']
            and matrix['sqlite_migration_chain'] == old['sqlite_migration_chain'], 'Incomplete previous release/schema preservation')
    overlay = json.loads(blob(prepared.OVERLAY))
    expected_overlay = dict(schema='riskium-prepared-development-overlay-v1',version='0.4.0',target=TAG,
        predecessor=policy['initial_overlay'],predecessor_sha256=policy['preserved_inputs_sha256'][policy['initial_overlay']],
        components=[r for r in rows if r['id'] in prepared.initial.REPLACED | prepared.initial.ADDED | {'DOCUMENTATION_SNAPSHOT'}],
        dependencies={r['id']:graph[r['id']] for r in rows if r['id'] in prepared.initial.REPLACED | prepared.initial.ADDED | {'DOCUMENTATION_SNAPSHOT'}})
    require(overlay == expected_overlay and matrix['overlay_path'] == prepared.OVERLAY
            and matrix['overlay_sha256'] == sha(blob(prepared.OVERLAY)), 'Prepared overlay differs')
    require(matrix['future_gates'] == prepared.FUTURE and matrix['summary'] == dict(components=28,
        retained_from_initial=27,added_from_initial=1,overlay_components=6,dependency_edges=61,
        unique_selected_files=380,documentation_snapshots=4), 'Prepared scope summary differs')
    return matrix


def validate_profile_blob(profile, blob):
    require(profile['schema'] == 'riskium-stable-profile-v2' and profile['profile'] == 'stable-bounded-research-artifact'
            and profile['tag'] == TAG and profile['artifact_matrix'] == prepared.MATRIX
            and profile['critical_screen'] == SCREEN and profile['notes'] == NOTES, 'Unreviewed v0.3.4 profile')
    registry = json.loads(blob(REGISTRY))
    require(registry['schema'] == 'riskium-reviewed-successor-profiles-v1'
            and registry['profiles'].get(TAG) == PROFILE, 'Unregistered v0.3.4 profile')
    require(profile['model_version'] == '0.3.1' and profile['orsd_revision'] == '0.4.3'
            and profile['manuscript_version'] == '7.0.8'
            and profile['reviewed_scope_commit'] == '3afa861b5296addefc98ce401767c7ab7d025d2c'
            and profile['accepted_scope'] == 'evaluation/owner-review/accepted-scope.json', 'Unreviewed v0.3.4 scientific scope')
    for key in ('publication_requires_clean_exact_head','publication_requires_all_checks',
                'publication_requires_no_known_unresolved_critical_findings','publication_requires_new_tag_and_release','readback_required'):
        require(profile.get(key) is True, 'Missing v0.3.4 gate: ' + key)
    require(profile['independent_validation_claimed'] is False and profile['full_original_requirement_acceptance_claimed'] is False,
            'Unsupported v0.3.4 acceptance')
    require(set(profile['release_tooling_sha256']) == set(TOOLING), 'Missing release tooling closure')
    for path,digest in profile['release_tooling_sha256'].items():
        require(sha(blob(path)) == digest, 'Release tooling drift: ' + path)
    matrix = json.loads(blob(prepared.MATRIX))
    require(sha(blob(prepared.MATRIX)) == profile['artifact_matrix_sha256'], 'Profile/matrix hash differs')
    validate_matrix(matrix, blob)
    screen = json.loads(blob(SCREEN))
    require(screen['target'] == TAG and screen['component_matrix_sha256'] == profile['artifact_matrix_sha256']
            and screen['known_unresolved_critical_findings'] == []
            and screen['material_scientific_change_since_owner_acceptance'] is False
            and screen['new_owner_responses_generated'] == 0 and screen['independent_semantic_review_claimed'] is False
            and screen['universal_zero_defect_claimed'] is False, 'Unresolved/unreviewed v0.3.4 critical screen')
    require(screen['release_tooling_sha256'] == profile['release_tooling_sha256'] and len(screen['reviewed_risks']) >= 8,
            'Incomplete v0.3.4 engineering screen')
    for risk in screen['reviewed_risks']:
        require(risk['retained_evidence'] and risk['fresh_gate'], 'Unexplained v0.3.4 release risk')
        for path in risk['retained_evidence']:
            require(bool(blob(prepared.initial.safe_path(path))), 'Missing v0.3.4 retained evidence')
    require(bool(blob(NOTES)), 'Missing v0.3.4 release notes')
    return matrix


def validate_profile(root=ROOT):
    root = Path(root)
    profile_path(root)
    blob = lambda p:(root / prepared.initial.safe_path(p)).read_bytes()
    profile = json.loads(blob(PROFILE))
    matrix = validate_profile_blob(profile, blob)
    prepared.validate(matrix, json.loads(blob(prepared.OVERLAY)), blob)
    stable.validate_profile(root, 'v0.3.1')
    return profile


def validate_freshness(matrix, receipt, now=None):
    require(receipt['schema'] == 'riskium-v034-live-readback-v1' and receipt['all_bytes_match'] is True,
            'Missing actual v0.3.4 readback')
    require(receipt['component_matrix_sha256'] == sha(prepared.initial.encode(matrix).encode()), 'Freshness matrix differs')
    require(receipt['files_sha256'] == matrix['documentation']['deployed_files_sha256']
            and len(receipt['files_sha256']) == receipt['pages_files'] == 311
            and receipt['documentation_snapshots'] == 4 and receipt['wiki_files'] == 23
            and receipt['wiki_commit'] == matrix['documentation']['wiki_commit'], 'Incomplete v0.3.4 channel readback')
    age = ((now or datetime.now(timezone.utc)) - datetime.fromisoformat(receipt['checked_at_utc'])).total_seconds()
    require(0 <= age < 86400, 'Stale/future v0.3.4 channel readback')
    require(re.fullmatch('[a-f0-9]{40}',receipt['pages_source_commit']) and receipt['pages_source_is_ancestor'] is True,
            'Unrelated v0.3.4 Pages source')


def live_readback(root, profile):
    root = Path(root); matrix = json.loads((root / profile['artifact_matrix']).read_bytes())
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(['git','clone','--quiet','--depth=1',WIKI,tmp],check=True,timeout=90)
        commit = subprocess.check_output(['git','-C',tmp,'rev-parse','HEAD'],text=True).strip()
        wiki = {p.name:sha(p.read_bytes()) for p in Path(tmp).glob('*.md')}
        require(commit == matrix['documentation']['wiki_commit'] and wiki == matrix['documentation']['wiki_files_sha256'],
                'Actual Wiki differs from selected v0.3.4 projection')
    def fetch(path):
        path = prepared.initial.safe_path(path)
        with urllib.request.urlopen(SITE + path,timeout=30) as response:
            require(response.status == 200 and response.url.startswith(SITE), 'Unexpected v0.3.4 Pages response')
            return response.read()
    manifest_bytes = fetch('publication-manifest.json'); manifest = json.loads(manifest_bytes)
    source = manifest['current_source_commit']
    require(re.fullmatch('[a-f0-9]{40}',source), 'Invalid deployed source')
    require(subprocess.run(['git','merge-base','--is-ancestor',source,'HEAD'],cwd=root).returncode == 0,
            'Pages source is not a release ancestor')
    expected = matrix['documentation']['deployed_files_sha256']
    def check(item):
        path,digest = item
        require(manifest['files_sha256'].get(path) == digest and sha(fetch(path)) == digest,
                'Actual v0.3.4 Pages bytes differ: ' + path)
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(check,expected.items()))
    receipt = dict(schema='riskium-v034-live-readback-v1',checked_at_utc=datetime.now(timezone.utc).isoformat(),
        component_matrix_sha256=sha((root/profile['artifact_matrix']).read_bytes()),all_bytes_match=True,
        wiki_commit=commit,wiki_files=23,pages_files=311,documentation_snapshots=4,files_sha256=expected,
        pages_source_commit=source,pages_source_is_ancestor=True,pages_manifest_sha256=sha(manifest_bytes),
        scope='Fresh actual native Wiki clone and every selected current/frozen/system HTTP body; not independent semantic review.')
    validate_freshness(matrix,receipt)
    return receipt


def validate_release_checks(checks):
    require([c['command'] for c in checks] == [['python',*args] for args in EXTRA_CHECKS]
            and all(c['exit_code'] == 0 for c in checks), 'Missing/failed v0.3.4 release checks')


def resolve_intent(root,event,ref,before,after,inputs=None):
    inputs = inputs or {}; root = Path(root)
    if event == 'workflow_dispatch' and inputs.get('release_tag') == TAG:
        require(ref == 'refs/heads/main', 'v0.3.4 intent requires main')
        profile_path(root)
        return dict(publish=inputs.get('publish') in (True,'true'),release_tag=TAG)
    if event == 'push' and re.fullmatch('[a-f0-9]{40}',before or '') and set(before) != {'0'}:
        paths = stable.git(root,'diff','--name-only',before,after).decode().splitlines()
        if REQUEST in paths:
            require(ref == 'refs/heads/main', 'v0.3.4 intent requires main')
            request = json.loads(stable.git(root,'show',after+':'+REQUEST))
            require(request['schema'] == 'riskium-reviewed-successor-request-v1' and request['tag'] == TAG
                    and request['profile'] == 'stable-bounded-research-artifact' and type(request['publish']) is bool,
                    'Explicit v0.3.4 release intent required')
            profile_path(root)
            if request['publish']:
                reviewed = request.get('reviewed_source_commit','')
                require(re.fullmatch('[a-f0-9]{40}',reviewed or ''), 'Reviewed implementation source required')
                require(subprocess.run(['git','merge-base','--is-ancestor',reviewed,after],cwd=root).returncode == 0,
                        'Reviewed implementation is not an ancestor')
                delta = set(stable.git(root,'diff','--name-only',reviewed,after).decode().splitlines())
                require(delta.issubset({REQUEST,'evaluation/consistency/inventory.json'}), 'Unreviewed changes after dry freeze')
            return dict(publish=request['publish'],release_tag=TAG)
        if ref == 'refs/heads/main' and any(p in set(TOOLING) | {PROFILE,REGISTRY,SCREEN,NOTES,prepared.MATRIX} for p in paths):
            profile_path(root)
            return dict(publish=False,release_tag=TAG)
    return stable.resolve_intent(root,event,ref,before,after,inputs)
