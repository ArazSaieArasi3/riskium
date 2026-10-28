"""Select exact v0.3.5 component/source bindings; never freeze or publish."""
import argparse
import copy
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import subprocess

import build_release_selection as shared

ROOT = Path(__file__).resolve().parents[1]
POLICY = 'releases/selection-policy-v0.3.5.json'
MATRIX = 'releases/selection-v0.3.5.json'
OVERLAY = 'releases/development-components-v0.3.5.json'
TABLE = 'evaluation/releases/v0.3.5-selection/components.md'
BASE = 'cc02e45749995b8710802822ae709d49e0a83993'
BASE_MATRIX = 'releases/distribution-v0.3.4.json'
REPLACED = {'CONSISTENCY': '0.3.0', 'DOCUMENTATION': '0.4.0'}
ADDED = {'EVIDENCE_REFERENCE_LIFECYCLE': '0.7.0'}
SCIENCE = dict(model='0.3.1', orsd='0.4.3', original_drsd='0.1.0', manuscript='7.0.8')
BOUNDARIES = dict(new_owner_ratings=0, independent_validation_claimed=False,
                  full_original_requirement_acceptance_claimed=False,
                  organizational_admissions='11 WITHHELD unchanged',
                  new_snapshot_registered=False, stable_profile_registered=False,
                  source_freeze_executed=False, publication_requested=False)
FUTURE = ['Select/register the final compatible v0.3.5 release profile and any separately reviewed snapshot/publication support.',
          'Replay affected artifact/manuscript/channel checks on the final selected clean source and freeze its exact identity.',
          'Publish only the new v0.3.5 tag/six assets; independently verify downloads/tag/manifest/Latest and all eleven prior releases.']


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encode(value):
    return json.dumps(value, indent=2) + '\n'


def reader(path):
    path = shared.safe_path(path)
    target = ROOT / path
    require(target.resolve().is_relative_to(ROOT.resolve()) and not target.is_symlink(), 'V035-PATH')
    require(target.is_file(), 'V035-MISSING: ' + path)
    return target.read_bytes()


@lru_cache(maxsize=1024)
def frozen(path):
    return subprocess.check_output(['git', 'show', BASE + ':' + shared.safe_path(path)], cwd=ROOT)


def checked_hashes(bindings, read):
    require(isinstance(bindings, dict), 'V035-HASH-REGISTER')
    for path, expected in bindings.items():
        shared.safe_path(path)
        require(isinstance(expected, str) and len(expected) == 64, 'V035-HASH-FORMAT')
        require(sha(read(path)) == expected, 'V035-STALE: ' + path)


def baseline(policy, read):
    require(policy['baseline_release'] == 'v0.3.4' and policy['baseline_source'] == BASE
            and policy['baseline_matrix'] == BASE_MATRIX, 'V035-BASELINE-IDENTITY')
    tag = subprocess.check_output(['git', 'rev-parse', 'v0.3.4^{commit}'], cwd=ROOT, text=True).strip()
    require(tag == BASE, 'V035-BASELINE-TAG')
    raw = frozen(BASE_MATRIX)
    require(sha(raw) == policy['baseline_matrix_sha256'] and raw == read(BASE_MATRIX), 'V035-BASELINE-MATRIX')
    value = json.loads(raw)
    require(len(value['artifacts']) == 28 and len(value['selected_files_sha256']) == 380, 'V035-BASELINE-POPULATION')
    checked_hashes(value['selected_files_sha256'], read)
    # Check historical payloads at their original source as well as current preservation.
    for path, expected in value['selected_files_sha256'].items():
        require(sha(frozen(path)) == expected, 'V035-BASELINE-PAYLOAD: ' + path)
    return value


def generated_outputs(policy, read, descriptor):
    refs = policy['current_documentation_receipts']
    wiki, http = (json.loads(read(refs[k])) for k in ('wiki', 'http'))
    require(wiki['all_bytes_match'] is True and wiki['files'] == 23
            and wiki['documentation_version'] == '0.4.0' and wiki['published_source'] == 'v0.3.4'
            and wiki['target_source'] == 'v0.3.5', 'V035-WIKI-RECEIPT')
    require(http['all_bytes_match'] is True and http['documentation_version'] == '0.4.0'
            and http['files'] == 311 and http['current_headers'] == 31 and http['frozen_snapshots'] == 4
            and http['published_source'] == 'v0.3.4' and http['target_source'] == 'v0.3.5',
            'V035-HTTP-RECEIPT')
    require(wiki['source_commit'] == http['source_commit'] == policy['source_baseline']
            and wiki['guide_source_commit'] == http['guide_source_commit'] == descriptor['guide_source_commit'],
            'V035-CHANNEL-SOURCE')
    wiki_hashes = {r['file']: r['sha256'] for r in wiki['checks']}
    require(len(wiki_hashes) == len(wiki['checks']) == 23
            and wiki_hashes == descriptor['wiki_files_sha256']
            and all(r['exact_match'] is True for r in wiki['checks']), 'V035-WIKI-INVENTORY')
    served = {r['path']: r['sha256'] for r in http['checks']}
    require(len(served) == len(http['checks']) == 311
            and all(r['status'] == 200 and r['matches_exact_source_and_manifest'] is True for r in http['checks']),
            'V035-HTTP-INVENTORY')
    current = {'current/' + p: h for p, h in descriptor['current_files_sha256'].items()}
    require(len(current) == 68 and all(served.get(p) == h for p, h in current.items()), 'V035-GENERATED-CURRENT')
    require(served.get('versions/index.html') == descriptor['versions_index_sha256'], 'V035-GENERATED-VERSIONS')
    return dict(schema='riskium-v035-generated-output-selection-v1', documentation_version='0.4.0',
                source_commit=wiki['source_commit'], guide_source_commit=descriptor['guide_source_commit'],
                wiki_commit=wiki['wiki_commit'], actual_wiki_receipt=refs['wiki'], actual_http_receipt=refs['http'],
                current_files_sha256=descriptor['current_files_sha256'], versions_index_sha256=descriptor['versions_index_sha256'],
                wiki_files_sha256=wiki_hashes, all_served_files_sha256=served,
                root_manifest_sha256=http['manifest_sha256'], historical_source_bound_not_fresh_replayed=True,
                scope='Generated deployment paths are not the preserved docs/current repository paths. Final candidate needs fresh readback.')


def checked_descriptor(spec, read):
    data = read(spec['descriptor'])
    require(sha(data) == spec['descriptor_sha256'], 'V035-DESCRIPTOR-SOURCE: ' + spec['id'])
    desc = json.loads(data)
    require(desc['version'] == spec['version'] and desc['id'] == spec['id']
            and desc['compatible_model'] == '0.3.1', 'V035-DESCRIPTOR-IDENTITY')
    # Check the original descriptor map before merging independently bound closures.
    # A later correct receipt hash must not conceal an internally stale descriptor.
    checked_hashes(desc['files_sha256'], read)
    return data, desc


def check_lifecycle_metadata(desc, report):
    require(desc['schema_version'] == 8 and desc['baseline_sql_profile'] == '0.6.0'
            and desc['summary']['outcomes'] == {'PASS': 43} and desc['full_mapping_completed'] is False
            and desc['independent_semantic_validation'] is False
            and report['profile'] == '0.7.0' and report['schema_version'] == 8 and report['execution_issue'] == 53
            and report['summary']['outcomes'] == {'PASS': 43}, 'V035-LIFECYCLE-SCOPE')


def current_rows(policy, read):
    expected_versions = dict(REPLACED, **ADDED)
    specs = {r['id']: r for r in policy['descriptor_components']}
    require(len(specs) == len(policy['descriptor_components']) == 3 and set(specs) == set(expected_versions), 'V035-DESCRIPTOR-SET')
    rows = {}
    generated = None
    for ident, version in expected_versions.items():
        spec = specs[ident]
        data, desc = checked_descriptor(spec, read)
        require(desc['version'] == version, 'V035-DESCRIPTOR-IDENTITY')
        files = dict(desc['files_sha256'])
        files[spec['descriptor']] = sha(data)
        for path in spec['receipt_paths']:
            require(path in policy['evidence_receipts_sha256'], 'V035-UNBOUND-RECEIPT: ' + path)
            files[path] = sha(read(path))
        if ident == 'CONSISTENCY':
            report_path = 'evaluation/consistency/current-0.3.0/report.json'
            report = json.loads(read(report_path))
            require(report['version'] == '0.3.0' and report['target_distribution'] == 'v0.3.5'
                    and report['status'] == 'CURRENT_SOURCE_AND_PAPER_BASELINE_ACCOUNTING_PASS'
                    and report['summary']['routes'] == 450 and report['summary']['historical_rows'] == 423
                    and report['summary']['declared_current_claim_routes'] == 39
                    and report['summary']['native_ids'] == 306 and report['summary']['remaining_deferred'] == 236
                    and report['summary']['independent_ratings'] == 0
                    and report['summary']['organizational_admissions'] == {'WITHHELD': 11}, 'V035-CONSISTENCY-SCOPE')
            require(desc['historical_rows'] == 423 and desc['current_routes'] == 450
                    and desc['independent_acceptance'] is False, 'V035-CONSISTENCY-SCOPE')
            checked_hashes(report['input_sha256'], read)
            files.update(report['input_sha256'])
        elif ident == 'DOCUMENTATION':
            require(desc['shared_guides'] == 21 and desc['native_wiki_files'] == 23
                    and desc['maintained_html_pages'] == 31 and desc['frozen_snapshots'] == 4
                    and desc['semantic_or_scientific_changes'] is False
                    and desc['independent_acceptance_claimed'] is False
                    and desc['new_source_distribution_published'] is False
                    and desc['published_source_release'] == 'v0.3.4' and desc['proposed_distribution'] == 'v0.3.5',
                    'V035-DOCUMENTATION-SCOPE')
            support = policy['documentation_runtime_support_sha256']
            required_support = {'tools/publication/build_publication_status.py',
                'evaluation/releases/v0.3.4-publication-status/component.json', '.github/workflows/publication-status.yml',
                'tests/test_publication_status.py', 'tools/publication/guides.py', 'tools/publication/requirements.txt'}
            require(required_support <= set(support), 'V035-DOCUMENTATION-RUNTIME')
            checked_hashes(support, read)
            status = json.loads(read('evaluation/releases/v0.3.4-publication-status/component.json'))
            checked_hashes(status['files_sha256'], read)
            files.update(status['files_sha256'])
            files.update(support)
            registries = ['tools/publication/pages-registry.json', 'tools/publication/snapshot-additions-v0.3.4.json']
            snapshots = {}
            for registry_path in registries:
                require(read(registry_path) == frozen(registry_path), 'V035-SNAPSHOT-REGISTRY')
                register = json.loads(read(registry_path))['releases']
                require(not (set(snapshots) & set(register)), 'V035-SNAPSHOT-DUPLICATE')
                snapshots.update(register)
                files[registry_path] = sha(read(registry_path))
            require(len(snapshots) == 4, 'V035-SNAPSHOT-POPULATION')
            frozen_files = {'docs/' + row['route'] + '/' + path: digest
                            for row in snapshots.values() for path, digest in row['files_sha256'].items()}
            require(policy['frozen_snapshot_files_sha256'] == frozen_files, 'V035-SNAPSHOT-INVENTORY')
            checked_hashes(frozen_files, read)
            files.update(frozen_files)
            generated = generated_outputs(policy, read, desc)
            require(all(generated['all_served_files_sha256'].get(p.removeprefix('docs/')) == digest
                        for p, digest in frozen_files.items()), 'V035-SNAPSHOT-GENERATED-EVIDENCE')
            for name, expected in desc['wiki_files_sha256'].items():
                files['documentation/0.4.0/wiki/' + shared.safe_path(name)] = expected
        else:
            report = json.loads(read('evaluation/relational/evidence-lifecycle/report.json'))
            check_lifecycle_metadata(desc, report)
            checked_hashes(report['inputs_sha256'], read)
            files.update(report['inputs_sha256'])
        checked_hashes(files, read)
        rows[ident] = dict(id=ident, version=version, compatible_model='0.3.1', descriptor_path=spec['descriptor'],
                          evidence_receipts=spec['receipt_paths'],
                          files=[dict(path=p, sha256=h) for p, h in sorted(files.items())],
                          scope='Exact current component and source-bound evidence; not final release or independent semantic acceptance.')
    return rows, generated


def expected_graph(policy, old, versions):
    graph = copy.deepcopy(old['dependencies'])
    for ident in graph:
        graph[ident] = [dict(id=d['id'], version=versions[d['id']]) for d in graph[ident]]
    # Archived generation consumed DOCUMENTATION0.3, but current assembly only copies the immutable packet.
    graph['DOCUMENTATION_SNAPSHOT'] = [dict(id='MODEL', version='0.3.1')]
    for ident, dependencies in {
        'EVIDENCE_REFERENCE_LIFECYCLE': ['QUALIFIED_EVIDENCE', 'DATABASE_REQUIREMENTS'],
        'CONSISTENCY': ['SOURCE_SCENARIO', 'SOURCE_SCENARIO_LINEAGE', 'QUALIFIED_EVIDENCE', 'EVIDENCE_REFERENCE_LIFECYCLE'],
        'DOCUMENTATION': ['EVIDENCE_REFERENCE_LIFECYCLE', 'DOCUMENTATION_SNAPSHOT'],
    }.items():
        existing = graph.setdefault(ident, [])
        existing_ids = {d['id'] for d in existing}
        existing.extend(dict(id=d, version=versions[d]) for d in dependencies if d not in existing_ids)
    require(policy['dependencies'] == graph, 'V035-DEPENDENCY-CONTRACT')
    return graph


def migration_chain(old, inventory, read):
    import relational_evidence_lifecycle as lifecycle
    chain = copy.deepcopy(old['sqlite_migration_chain'])
    step = dict(id='EVIDENCE_REFERENCE_LIFECYCLE', version='0.7.0', from_schema=7, to_schema=8,
                reader='tools/relational_evidence_lifecycle.py',
                migration_files=['implementation/relational/0.7.0/008_evidence_lifecycle.sql'])
    step['source_files_sha256'] = {p: sha(read(p)) for p in [step['reader'], *step['migration_files']]}
    step['schema_migration_ledger_sha256'] = {'8': lifecycle.digest()}
    require(step['schema_migration_ledger_sha256']['8'] == sha(read(step['migration_files'][0])), 'V035-MIGRATION-HASH')
    chain.append(step)
    require([r['to_schema'] for r in chain] == [2, 3, 4, 5, 6, 7, 8], 'V035-MIGRATION-CHAIN')
    previous = 0
    for row in chain:
        require(row['from_schema'] == previous, 'V035-MIGRATION-GAP')
        require(all(p in inventory for p in [row['reader'], *row['migration_files']]), 'V035-MIGRATION-SOURCE')
        checked_hashes(row['source_files_sha256'], read)
        previous = row['to_schema']
    return chain


def inputs(read):
    policy = json.loads(read(POLICY))
    require(policy['schema'] == 'riskium-v035-selection-policy-v1' and policy['target'] == 'v0.3.5'
            and policy['stage'] == 'COMPONENT_SELECTION_NOT_FROZEN' and policy['parent_issue'] == 51
            and policy['issue'] == 56,
            'V035-POLICY-IDENTITY')
    require(policy['source_baseline'] == '1f8610657b3d9ab3c50589d3d76be7cffd8c7099', 'V035-SOURCE-IDENTITY')
    require(policy['scientific_versions'] == SCIENCE and policy['boundaries'] == BOUNDARIES, 'V035-POLICY-SCOPE')
    old = baseline(policy, read)
    checked_hashes(policy['preserved_registers_sha256'], read)
    checked_hashes(policy['evidence_receipts_sha256'], read)
    checkpoints = json.loads(read('evaluation/releases/v0.3.5-selection/inputs/completed-checkpoints.json'))['issues']
    require(len(checkpoints) == 3 and {r['issue'] for r in checkpoints} == {53, 54, 55}
            and all(r['state'] == 'closed' and r['state_reason'] == 'completed' for r in checkpoints), 'V035-CHECKPOINT-COMPLETION')
    for name, source, tests in [
        ('lifecycle-candidate.json', '9a92ac92b29a127b1c38e6d0c052f8dc230dcb47', 395),
        ('alignment-candidate.json', 'ccc89a184a618ccc2c107ccbf27a15232060557e', 409),
        ('documentation-candidate.json', '1f8610657b3d9ab3c50589d3d76be7cffd8c7099', 417),
    ]:
        receipt = json.loads(read('evaluation/releases/v0.3.5-selection/inputs/' + name))
        if name == 'lifecycle-candidate.json':
            # Preserve the original checkpoint schema; do not fabricate newer fields.
            require(receipt['schema'] == 'riskium-lifecycle-final-candidate-readback-v1'
                    and receipt['source_commit'] == source and receipt['actual_full_software_tests'] == tests
                    and receipt['all_asset_sums_match'] is True
                    and receipt['all_archive_files_match_manifest_and_git'] is True
                    and receipt['aggregate_checks'] == 28 and receipt['publication_executed'] is False,
                    'V035-CANDIDATE-RECEIPT')
        else:
            require(receipt['status'] == 'DOWNLOADED_CANDIDATE_EXACT_SOURCE_PASS'
                    and receipt['source_commit'] == source and receipt['full_software_tests'] == tests
                    and receipt['all_git_blobs_equal'] is True and receipt['candidate_gates'] == 28
                    and receipt['publication_executed'] is False
                    and receipt['independent_semantic_acceptance'] == 'NOT_ESTABLISHED', 'V035-CANDIDATE-RECEIPT')
    rows = {r['id']: copy.deepcopy(r) for r in old['artifacts'] if r['id'] not in REPLACED}
    replacements, generated = current_rows(policy, read)
    rows.update(replacements)
    require(len(rows) == 29, 'V035-COMPONENT-SET')
    versions = {ident: row['version'] for ident, row in rows.items()}
    graph = expected_graph(policy, old, versions)
    support_files = [POLICY, 'tools/select_release_v035.py', 'tests/test_release_v035_selection.py', *policy.get('support_files', [])]
    support = {path: sha(read(path)) for path in support_files}
    ordered = [rows[ident] for ident in shared.dependency_order(versions, graph)]
    inventory, owners = shared.file_inventory(ordered, support, read)
    require(set(old['selected_files_sha256']) <= set(inventory), 'V035-PRESERVED-FILE-OMISSION')
    require(policy['preserve_releases'] == old['preserve_releases'] + ['v0.3.4'], 'V035-RELEASE-PRESERVATION')
    require('v0.3.5' not in json.loads(read('releases/successor-profiles.json'))['profiles'], 'V035-PROFILE-REGISTERED')
    return policy, old, ordered, graph, support, inventory, owners, generated


def assemble(read=reader):
    policy, old, rows, graph, support, inventory, owners, generated = inputs(read)
    historical = {ident: copy.deepcopy(old['dependencies'][ident]) for ident in ('DOCUMENTATION_SNAPSHOT', 'DOCUMENTATION', 'CONSISTENCY')}
    historical_components = [copy.deepcopy(next(r for r in old['artifacts'] if r['id'] == ident)) for ident in ('DOCUMENTATION', 'CONSISTENCY')]
    require(policy['historical_generation_dependencies'] == historical
            and policy['historical_generation_components'] == historical_components, 'V035-HISTORICAL-POLICY')
    overlay = dict(schema='riskium-v035-development-selection-v1', target='v0.3.5', stage=policy['stage'],
                   baseline_release='v0.3.4', components=[r for r in rows if r['id'] in REPLACED | ADDED],
                   dependency_requirements={i: graph[i] for i in [r['id'] for r in rows if r['id'] in REPLACED | ADDED]},
                   scope='Three current component entries over the immutable baseline; no source freeze/publication.')
    matrix = dict(schema='riskium-v035-component-selection-v1', target='v0.3.5', stage=policy['stage'], issue=policy['issue'], parent_issue=51,
        policy_path=POLICY, policy_sha256=sha(read(POLICY)), source_baseline=policy['source_baseline'], baseline_release='v0.3.4',
        baseline_source=BASE, baseline_matrix=BASE_MATRIX, baseline_matrix_sha256=policy['baseline_matrix_sha256'],
        scientific_versions=SCIENCE, boundaries=BOUNDARIES, artifacts=rows, dependencies=graph,
        historical_generation_dependencies=historical, historical_generation_components=historical_components,
        historical_generation_scope='Exact v0.3.4 snapshot generation prerequisite records. Current assembly copies frozen bytes and does not rebuild old documentation against new consistency.',
        generated_outputs=generated, selection_tooling_sha256=support, selected_files_sha256=inventory, file_owners=owners,
        sqlite_migration_chain=migration_chain(old, inventory, read), preserve_releases=policy['preserve_releases'],
        changes=dict(retained=[r['id'] for r in old['artifacts'] if r['id'] not in REPLACED],
                     replaced=[dict(id=i, from_version=next(r['version'] for r in old['artifacts'] if r['id'] == i), to_version=REPLACED[i]) for i in sorted(REPLACED)], added=sorted(ADDED)),
        overlay_path=OVERLAY, overlay_sha256=sha(encode(overlay).encode()),
        summary=dict(components=29, retained=26, replaced=2, added=1, selected_unique_files=len(inventory),
                     dependency_edges=sum(map(len, graph.values())), historical_generation_components=2,
                     generated_current_files=len(generated['current_files_sha256']), generated_wiki_files=23),
        future_gates=FUTURE,
        limits=policy['limits'])
    return matrix, overlay


def validate_selection(matrix, overlay, read=reader):
    require(matrix['target'] == 'v0.3.5' and matrix['stage'] == 'COMPONENT_SELECTION_NOT_FROZEN', 'V035-STAGE')
    require(matrix['boundaries'] == BOUNDARIES and matrix['scientific_versions'] == SCIENCE, 'V035-SCOPE')
    rows = matrix['artifacts']
    versions = {r['id']: r['version'] for r in rows}
    require(len(rows) == len(versions) == 29, 'V035-COMPONENT-SET')
    require(all(r['compatible_model'] == '0.3.1' for r in rows), 'V035-COMPATIBILITY')
    shared.dependency_order(versions, matrix['dependencies'])
    positions = {r['id']: n for n, r in enumerate(rows)}
    require(all(positions[d['id']] < positions[i] for i, ds in matrix['dependencies'].items() for d in ds), 'V035-DEPENDENCY-ORDER')
    inventory, owners = shared.file_inventory(rows, matrix['selection_tooling_sha256'], read)
    require(inventory == matrix['selected_files_sha256'] and owners == matrix['file_owners'], 'V035-INVENTORY')
    expected, expected_overlay = assemble(read)
    require(matrix['dependencies'] == expected['dependencies'], 'V035-DEPENDENCY-CONTRACT')
    require(matrix['historical_generation_dependencies'] == expected['historical_generation_dependencies']
            and matrix['historical_generation_components'] == expected['historical_generation_components'], 'V035-HISTORICAL-GENERATION')
    require(matrix['artifacts'] == expected['artifacts'], 'V035-DESCRIPTOR-CLOSURE')
    require(matrix['generated_outputs'] == expected['generated_outputs'], 'V035-GENERATED-OUTPUTS')
    require(overlay == expected_overlay and matrix['overlay_sha256'] == sha(encode(overlay).encode()), 'V035-OVERLAY')
    require(matrix == expected, 'V035-SELECTION-CONTRACT')
    return matrix['summary']


def build():
    matrix, overlay = assemble()
    validate_selection(matrix, overlay)
    table = '# Selected components for v0.3.5\n\n**COMPONENT_SELECTION_NOT_FROZEN**. Source remains v0.3.4 published; final profile, selected-source replay, freeze and publication are future gates.\n\n[Exact selection](../../../releases/selection-v0.3.5.json) · [Declared policy](../../../releases/selection-policy-v0.3.5.json).\n\n| Component | Version | Change | Current assembly prerequisites | File entries |\n| --- | --- | --- | --- | ---: |\n'
    for row in matrix['artifacts']:
        ident = row['id']
        kind = 'REPLACED' if ident in REPLACED else 'ADDED' if ident in ADDED else 'RETAINED'
        dependencies = ', '.join(d['id'] + ' ' + d['version'] for d in matrix['dependencies'][ident]) or 'None'
        table += '| ' + ident + ' | ' + row['version'] + ' | ' + kind + ' | ' + dependencies + ' | ' + str(len(row['files'])) + ' |\n'
    table += '\n29 current components: 26 retained byte-for-byte, two revised and one added. The exact old documentation 0.3 / consistency 0.2 rows and generation dependency slices are archived separately; the frozen snapshot is assembled by copying its original packet, never by silently rebuilding it against current documentation 0.4.\n\nGenerated current-site hashes are separate output evidence, not hashes of the preserved docs/current source files. All 23 committed Wiki projections and current descriptor/runtime/input closures are selected. Shared paths must name the same exact bytes; the union records every owner. Migration coverage ends at schema 8, with prior steps unchanged.\n\nNo new snapshot, stable profile, release intent, tag, assets, publication, scientific execution, case admission or independent semantic rating is created. Final candidate/channel/critical-screen/freeze/publication checks remain required under #51.\n'
    return {MATRIX: encode(matrix), OVERLAY: encode(overlay), TABLE: table}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--check', action='store_true')
    args = p.parse_args()
    outputs = build()
    for path, text in outputs.items():
        target = ROOT / path
        if args.check:
            require(target.is_file() and target.read_text() == text, 'V035-STALE-OUTPUT: ' + path)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)
    print(json.dumps(dict(status='V035_COMPONENT_SELECTION_PASS', **json.loads(outputs[MATRIX])['summary'], publication_executed=False)))


if __name__ == '__main__':
    main()
