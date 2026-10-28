"""Prepare the 28-component v0.3.4 matrix; never freeze or publish a source release."""
import argparse
import copy
from functools import lru_cache
import json
from pathlib import Path
import subprocess

import build_release_selection as initial

ROOT = Path(__file__).resolve().parents[1]
SOURCE = '70803db8ecf8dd1c16af1c688f08ffacc30d8937'
POLICY = 'releases/preparation-policy-v0.3.4.json'
MATRIX = 'releases/distribution-v0.3.4.json'
OVERLAY = 'releases/prepared-components-v0.3.4.json'
TABLE = 'evaluation/releases/v0.3.4-preparation/components.md'
TOOLING = (POLICY, 'tools/build_prepared_distribution.py', 'tests/test_prepared_distribution.py',
           '.github/workflows/post-release-validation.yml')
INPUTS = ('releases/selection-policy-v0.3.4.json', 'releases/selection-v0.3.4.json',
          'releases/development-components-v0.3.4.json', 'tools/build_release_selection.py',
          'tests/test_release_selection.py', 'evaluation/releases/v0.3.4-selection/completion.json',
          'evaluation/documentation/current-0.3.0/component.json',
          'tools/publication/snapshot-policy-v0.3.4.json', 'tools/publication/snapshot-additions-v0.3.4.json',
          'evaluation/documentation/v0.3.4-snapshot/component.json',
          'evaluation/documentation/v0.3.4-snapshot/completion.json')
PUBLICATION = ('index.html', 'interface-review.html', 'site/index.html',
               'THIRD-PARTY-DOCUMENTATION.txt', 'WIDOCO-Apache-2.0.txt')
DEPS = [dict(id='MODEL', version='0.3.1'), dict(id='DOCUMENTATION', version='0.3.0')]
FUTURE = [
    'Integrate the reviewed v0.3.4 profile, critical screen, notes and this matrix into the exact-source freeze path; run final-source checks and fresh Wiki/Pages readback, then freeze a clean reviewed source.',
    'Publish only after a successful exact freeze and explicit release intent; independently download/verify tag/assets/manifest/Latest and all prior-release preservation before closing #45.'
]
BOUNDARIES = dict(documentation_snapshot_registered=True, documentation_snapshot_selected=True,
                  stable_profile_added_by_this_step=False, source_distribution_frozen_by_this_step=False,
                  publication_requested_by_this_step=False, new_owner_ratings=0,
                  independent_validation_claimed=False, full_original_requirement_acceptance_claimed=False,
                  organizational_admissions='11 WITHHELD unchanged')


def require(ok, code):
    if not ok:
        raise ValueError(code)


def read(path):
    path = initial.safe_path(path)
    target = ROOT / path
    require(target.resolve().is_relative_to(ROOT.resolve()) and not target.is_symlink(), 'PREP-PATH')
    require(target.is_file(), 'PREP-MISSING: ' + path)
    return target.read_bytes()


@lru_cache(maxsize=1024)
def archived(path):
    return subprocess.check_output(['git', 'show', SOURCE + ':' + initial.safe_path(path)], cwd=ROOT)


@lru_cache(maxsize=4)
def archived_initial(matrix_sha, overlay_sha):
    matrix = json.loads(archived('releases/selection-v0.3.4.json'))
    overlay = json.loads(archived('releases/development-components-v0.3.4.json'))
    require(initial.sha(archived('releases/selection-v0.3.4.json')) == matrix_sha
            and initial.sha(archived('releases/development-components-v0.3.4.json')) == overlay_sha, 'PREP-INITIAL-SOURCE')
    initial.validate_selection(matrix, overlay, archived)
    return matrix


def inputs(policy, blob):
    require(policy['schema'] == 'riskium-prepared-distribution-policy-v1' and policy['version'] == '0.1.0'
            and policy['issue'] == 49 and policy['parent_issue'] == 45 and policy['target'] == 'v0.3.4'
            and policy['approved_source'] == SOURCE, 'PREP-POLICY')
    require(policy['initial_selection'] == 'releases/selection-v0.3.4.json'
            and policy['initial_overlay'] == 'releases/development-components-v0.3.4.json', 'PREP-INITIAL-IDENTITY')
    require(set(policy['preserved_inputs_sha256']) == set(INPUTS), 'PREP-PRESERVED-SET')
    for path, digest in policy['preserved_inputs_sha256'].items():
        require(initial.sha(blob(path)) == digest == initial.sha(archived(path)), 'PREP-PRESERVED: ' + path)
    old = archived_initial(policy['preserved_inputs_sha256'][policy['initial_selection']],
                           policy['preserved_inputs_sha256'][policy['initial_overlay']])
    spec = policy['snapshot']
    folder = 'evaluation/documentation/v0.3.4-snapshot/'
    require(spec['id'] == 'DOCUMENTATION_SNAPSHOT' and spec['version'] == '0.1.0'
            and spec['descriptor'] == folder + 'component.json' and spec['completion'] == folder + 'completion.json'
            and spec['depends_on'] == DEPS, 'PREP-SNAPSHOT-IDENTITY')
    require(spec['receipts'] == [folder + p for p in ['completion.json', 'hosted-checks.json', 'software-tests.json',
            'software-tests.log', 'http-readback.json', 'wiki-readback.json']], 'PREP-RECEIPT-SET')
    row = initial.descriptor_row(spec, blob)
    row['scope'] = 'Completed immutable documentation 0.3.0/model 0.3.1 snapshot and exact deployment/tooling/evidence; no source publication or new domain acceptance.'
    completion = json.loads(blob(spec['completion']))
    for path, digest in completion['evidence_sha256'].items():
        require(initial.sha(blob(path)) == digest, 'PREP-RECEIPT-HASH: ' + path)
    require(completion['snapshot_source'] == '868dd543538857bb5c9ffbdfde458c4323981d01'
            and completion['snapshot_files'] == 68 and completion['deployed_snapshots'] == 4
            and completion['source_distribution_published'] is False, 'PREP-SNAPSHOT-COMPLETION')
    return old, row


def documentation(row, blob):
    descriptor = json.loads(blob(row['descriptor_path']))
    require(descriptor['documentation_version'] == '0.3.0' and descriptor['snapshot_files'] == 68
            and descriptor['deployment_entrypoint'] == 'tools/publication/build_snapshot_site.py', 'PREP-DEPLOYMENT-IDENTITY')
    base = json.loads(blob('tools/publication/pages-registry.json'))['releases']
    added = json.loads(blob('tools/publication/snapshot-additions-v0.3.4.json'))['releases']
    require(len(base) == 3 and set(added) == {'v0.3.4'} and not set(base) & set(added), 'PREP-SNAPSHOT-SET')
    snapshots = {**base, **added}
    require(snapshots['v0.3.4']['source_commit'] == descriptor['snapshot_source']
            and snapshots['v0.3.4']['source_tree'] == descriptor['source_tree'], 'PREP-SNAPSHOT-SOURCE')
    current = json.loads(blob('evaluation/documentation/current-0.3.0/component.json'))
    current_files = {p.removeprefix('docs/current/'): h for p, h in current['files_sha256'].items() if p.startswith('docs/current/')}
    require(len(current_files) == 68, 'PREP-CURRENT-FILES')
    folder = 'evaluation/documentation/v0.3.4-snapshot/'
    wiki = json.loads(blob(folder + 'wiki-readback.json'))
    http = json.loads(blob(folder + 'http-readback.json'))
    completion = json.loads(blob(folder + 'completion.json'))
    require(wiki['implementation_source'] == http['implementation_source'] == completion['implementation_source']
            and wiki['native_wiki_files'] == len(wiki['files_sha256']) == 23 and wiki['all_bytes_match'] is True,
            'PREP-CHANNEL-SOURCE')
    require(http['all_body_hashes_match'] is True and http['manifest_matches_local'] is True
            and len(http['files']) == http['actual_http_bodies'] == 311 and http['snapshot_http_bodies'] == 68
            and http['versions_latest_and_snapshot_wording_checked'] is True, 'PREP-CHANNEL-EVIDENCE')
    deployed = {p: h['sha256'] for p, h in http['files'].items()}
    expected = {'current/' + p: h for p, h in current_files.items()}
    for snapshot in snapshots.values():
        for name, digest in snapshot['files_sha256'].items():
            path = initial.safe_path(snapshot['route'] + '/' + name)
            require(initial.sha(blob('docs/' + path)) == digest, 'PREP-FROZEN-FILE: ' + path)
            expected[path] = digest
    require(len(expected) == 305 and all(deployed.get(p) == h for p, h in expected.items()), 'PREP-DEPLOYED-COVERAGE')
    for name, digest in wiki['files_sha256'].items():
        require(initial.sha(blob('docs/wiki/' + initial.safe_path(name))) == digest, 'PREP-WIKI-FILE')
    support = {'docs/' + p: initial.sha(blob('docs/' + p)) for p in PUBLICATION}
    require(all(deployed[p] == support['docs/' + p] for p in PUBLICATION)
            and set(deployed) == set(expected) | set(PUBLICATION) | {'versions/index.html'}, 'PREP-PUBLICATION-SUPPORT')
    require(deployed['versions/index.html'] == descriptor['generated_versions_index_sha256'], 'PREP-VERSION-INDEX')
    selected = {f['path'] for f in row['files']}
    require({'tools/publication/build_snapshot_site.py', '.github/workflows/documentation.yml',
             '.github/workflows/pages.yml'}.issubset(selected), 'PREP-DEPLOYMENT-CLOSURE')
    return dict(documentation_version='0.3.0', snapshot=snapshots['v0.3.4'], frozen_snapshots=snapshots,
        current_files_sha256=current_files, wiki_receipt=folder + 'wiki-readback.json',
        wiki_commit=wiki['wiki_commit'], wiki_files_sha256=wiki['files_sha256'],
        http_receipt=folder + 'http-readback.json', deployed_files_sha256=deployed,
        generated_versions_index_sha256=descriptor['generated_versions_index_sha256'],
        deployment_entrypoint=descriptor['deployment_entrypoint'],
        retained_channel_source=http['implementation_source'],
        channel_evidence_status='RETAINED_CHECKPOINT_NOT_FINAL_SOURCE_FRESHNESS'), support


def parts(policy, blob):
    old, snapshot = inputs(policy, blob)
    rows = copy.deepcopy(old['artifacts']) + [snapshot]
    graph = copy.deepcopy(old['dependencies'])
    graph['DOCUMENTATION_SNAPSHOT'] = copy.deepcopy(DEPS)
    docs, publication = documentation(snapshot, blob)
    tooling = {p: initial.sha(blob(p)) for p in TOOLING}
    preserved = policy['preserved_inputs_sha256']
    support_rows = [dict(id='PREPARATION_INPUTS', files=[dict(path=p, sha256=h) for p, h in preserved.items()]),
                    dict(id='PUBLICATION_SUPPORT', files=[dict(path=p, sha256=h) for p, h in publication.items()])]
    inventory, owners = initial.file_inventory(rows + support_rows, tooling, blob)
    overlay = dict(schema='riskium-prepared-development-overlay-v1', version='0.4.0', target='v0.3.4',
        predecessor=policy['initial_overlay'], predecessor_sha256=preserved[policy['initial_overlay']],
        components=[r for r in rows if r['id'] in initial.REPLACED | initial.ADDED | {'DOCUMENTATION_SNAPSHOT'}],
        dependencies={r['id']: graph[r['id']] for r in rows if r['id'] in initial.REPLACED | initial.ADDED | {'DOCUMENTATION_SNAPSHOT'}})
    return old, rows, graph, docs, publication, tooling, inventory, owners, overlay


def validate(matrix, overlay, blob=read):
    require(matrix['schema'] == 'riskium-successor-component-matrix-v1' and matrix['tag'] == 'v0.3.4'
            and matrix['stage'] == 'COMPONENTS_PREPARED_NOT_FROZEN', 'PREP-STAGE')
    policy = json.loads(blob(POLICY))
    require(matrix['policy_path'] == POLICY and matrix['policy_sha256'] == initial.sha(blob(POLICY))
            and matrix['preparation_issue'] == 49 and matrix['parent_issue'] == 45
            and matrix['approved_source'] == SOURCE, 'PREP-IDENTITY')
    old, rows, graph, docs, publication, tooling, inventory, owners, expected_overlay = parts(policy, blob)
    actual = matrix['artifacts']
    versions = {r['id']: r['version'] for r in actual}
    require(len(actual) == len(versions) == 28 and versions == {r['id']: r['version'] for r in rows}, 'PREP-COMPONENTS')
    require(all(r['compatible_model'] == '0.3.1' for r in actual), 'PREP-COMPATIBILITY')
    initial.dependency_order(versions, matrix['dependencies'])
    position = {r['id']: n for n, r in enumerate(actual)}
    require(all(position[d['id']] < position[i] for i, ds in matrix['dependencies'].items() for d in ds), 'PREP-DEPENDENCY-ORDER')
    require(matrix['dependencies'] == graph, 'PREP-DEPENDENCY-CONTRACT')
    actual_inventory, actual_owners = initial.file_inventory(actual + [
        dict(id='PREPARATION_INPUTS', files=[dict(path=p, sha256=h) for p, h in matrix['source_registers_sha256'].items()]),
        dict(id='PUBLICATION_SUPPORT', files=[dict(path=p, sha256=h) for p, h in matrix['publication_support_sha256'].items()])],
        matrix['selection_tooling_sha256'], blob)
    require(actual[:27] == old['artifacts'] and actual == rows, 'PREP-ROW-CLOSURE')
    require(matrix['source_registers_sha256'] == policy['preserved_inputs_sha256']
            and matrix['publication_support_sha256'] == publication and matrix['selection_tooling_sha256'] == tooling,
            'PREP-SUPPORT-CLOSURE')
    require(matrix['selected_files_sha256'] == inventory == actual_inventory
            and matrix['file_owners'] == owners == actual_owners, 'PREP-INVENTORY')
    require(matrix['documentation'] == docs, 'PREP-DOCUMENTATION')
    require(matrix['scientific_versions'] == old['scientific_versions'] and matrix['model_version'] == '0.3.1'
            and matrix['orsd_revision'] == '0.4.3' and matrix['manuscript_version'] == '7.0.8'
            and matrix['preparation_boundaries'] == BOUNDARIES, 'PREP-SCIENTIFIC-SCOPE')
    require(matrix['preserve_releases'] == old['preserve_releases'] and matrix['sqlite_migration_chain'] == old['sqlite_migration_chain'], 'PREP-PRESERVATION')
    require(matrix['initial_selection'] == policy['initial_selection'] and matrix['baseline_release'] == 'v0.3.3'
            and matrix['future_gates'] == FUTURE, 'PREP-FUTURE-GATES')
    require(overlay == expected_overlay and matrix['overlay_path'] == OVERLAY
            and matrix['overlay_sha256'] == initial.sha(initial.encode(overlay).encode()), 'PREP-OVERLAY')
    summary = dict(components=28, retained_from_initial=27, added_from_initial=1, overlay_components=6,
                   dependency_edges=61, unique_selected_files=len(inventory), documentation_snapshots=4)
    require(matrix['summary'] == summary, 'PREP-SUMMARY')
    return summary


def build():
    policy = json.loads(read(POLICY))
    old, rows, graph, docs, publication, tooling, inventory, owners, overlay = parts(policy, read)
    matrix = dict(schema='riskium-successor-component-matrix-v1', tag='v0.3.4', stage='COMPONENTS_PREPARED_NOT_FROZEN',
        preparation_issue=49, parent_issue=45, approved_source=SOURCE, policy_path=POLICY,
        policy_sha256=initial.sha(read(POLICY)), baseline_release='v0.3.3', initial_selection=policy['initial_selection'],
        model_version='0.3.1', orsd_revision='0.4.3', manuscript_version='7.0.8', scientific_versions=old['scientific_versions'],
        preparation_boundaries=BOUNDARIES, artifacts=rows, dependencies=graph,
        source_registers_sha256=policy['preserved_inputs_sha256'], publication_support_sha256=publication,
        selection_tooling_sha256=tooling, selected_files_sha256=inventory, file_owners=owners,
        documentation=docs, sqlite_migration_chain=old['sqlite_migration_chain'], preserve_releases=old['preserve_releases'],
        overlay_path=OVERLAY, overlay_sha256=initial.sha(initial.encode(overlay).encode()), future_gates=FUTURE,
        summary=dict(components=28, retained_from_initial=27, added_from_initial=1, overlay_components=6,
                     dependency_edges=61, unique_selected_files=len(inventory), documentation_snapshots=4))
    validate(matrix, overlay)
    table = '# Prepared v0.3.4 distribution components\n\n**COMPONENTS_PREPARED_NOT_FROZEN** — #49 under #45. Stable remains v0.3.3.\n\n[Distribution matrix](../../../releases/distribution-v0.3.4.json) · [Policy](../../../releases/preparation-policy-v0.3.4.json) · [Prepared overlay](../../../releases/prepared-components-v0.3.4.json).\n\n| Component | Version | Change from #47 | Declared direct prerequisites | Files |\n| --- | --- | --- | --- | ---: |\n'
    for row in rows:
        deps = ', '.join(d['id'] + ' ' + d['version'] for d in graph[row['id']]) or 'None'
        table += '| ' + row['id'] + ' | ' + row['version'] + ' | ' + ('ADDED' if row['id'] == 'DOCUMENTATION_SNAPSHOT' else 'RETAINED') + ' | ' + deps + ' | ' + str(len(row['files'])) + ' |\n'
    table += '\nAll 27 initial component rows are unchanged. The new snapshot adds its exact descriptor, 75 component files and six retained receipt/log files. The 61 declared prerequisite edges describe selection compatibility, not exhaustive runtime/code dependency discovery. Shared paths require identical hashes and retain all owners. The selected union contains ' + str(len(inventory)) + ' unique files, including preparation inputs/tooling and five publication-support sources.\n\nThe matrix selects four frozen documentation snapshots, current documentation 0.3.0/model 0.3.1, the canonical additive deployment entrypoint/workflow and the generated live version-index hash. The 311-body HTTP and 23-file Wiki receipts remain dated #48 evidence; final-source readback is still required. Earlier profiles/registers are verified at their original source and are not relabeled as fresh freeze evidence. SQLite schemas 2 through 7, all ten prior releases, model/ORSD/DRSD/manuscript versions, eleven WITHHELD admissions and zero independent ratings remain unchanged.\n\nNext integrate the reviewed release profile/critical screen/notes and this matrix into the exact-source freeze path, run final-source checks/fresh channel evidence and freeze; then publish and independently verify actual assets/tag/Latest and prior preservation before closing #45.\n'
    return {MATRIX: initial.encode(matrix), OVERLAY: initial.encode(overlay), TABLE: table}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    outputs = build()
    for path, text in outputs.items():
        target = ROOT / path
        if args.check:
            require(target.is_file() and target.read_text() == text, 'PREP-STALE: ' + path)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)
    matrix = json.loads(outputs[MATRIX])
    print(initial.encode(dict(status='PREPARED_DISTRIBUTION_COMPONENTS_PASS', tag='v0.3.4', stage=matrix['stage'],
                              **matrix['summary'], publication_executed=False)))


if __name__ == '__main__':
    main()
