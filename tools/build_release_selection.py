"""Select the next distribution's exact components; never freeze, tag or publish."""
import argparse
from collections import Counter
import copy
from functools import lru_cache
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess

import review_distribution as published

ROOT = Path(__file__).resolve().parents[1]
POLICY = 'releases/selection-policy-v0.3.4.json'
MATRIX = 'releases/selection-v0.3.4.json'
OVERLAY = 'releases/development-components-v0.3.4.json'
CONSISTENCY = 'evaluation/consistency/current-0.2.0/component.json'
DELTA = 'evaluation/consistency/current-0.2.0/source-comparison.json'
TABLE = 'evaluation/releases/v0.3.4-selection/components.md'
REPLACED = {'CONSISTENCY', 'DOCUMENTATION'}
ADDED = {'SOURCE_SCENARIO', 'SOURCE_SCENARIO_LINEAGE', 'QUALIFIED_EVIDENCE'}
TOOLING = (POLICY, 'tools/build_release_selection.py', 'tests/test_release_selection.py')
FUTURE_GATES = ['Register the new documentation snapshot from an exact reviewed committed source.',
                'Refresh the provisional selection after snapshot/source changes; run final-source checks and fresh channel readbacks.',
                'Register/freeze the reviewed final distribution and publish/independently verify tag/assets/Latest and prior-release preservation.']


def require(ok, code):
    if not ok:
        raise ValueError(code)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encode(data):
    return json.dumps(data, indent=2) + '\n'


def safe_path(value):
    require(isinstance(value, str) and value, 'SEL-PATH')
    path = PurePosixPath(value)
    require(bool(path.parts) and not path.is_absolute() and str(path) == value and '..' not in path.parts
            and '\\' not in value and path.parts[0] != '.git', 'SEL-PATH')
    return value


def reader(path):
    path = safe_path(path)
    target = ROOT / path
    require(target.resolve().is_relative_to(ROOT.resolve()) and not target.is_symlink(), 'SEL-PATH')
    require(target.is_file(), 'SEL-MISSING: ' + path)
    return target.read_bytes()


@lru_cache(maxsize=1024)
def frozen(path, source='3380b6b31f4830417946105e17f023118c7be6ee'):
    require(re.fullmatch('[0-9a-f]{40}', source), 'SEL-BASELINE-SOURCE')
    return subprocess.check_output(['git', 'show', source + ':' + safe_path(path)], cwd=ROOT)


@lru_cache(maxsize=4)
def checked_baseline(path, source, digest):
    data = frozen(path, source)
    require(sha(data) == digest, 'SEL-BASELINE')
    baseline = json.loads(data)
    published.validate_matrix(baseline, lambda p: frozen(p, source))
    return data


def load_baseline(policy, read):
    source = subprocess.check_output(['git', 'rev-parse', 'v0.3.3^{commit}'], cwd=ROOT, text=True).strip()
    require(source == policy['baseline_source'] == '3380b6b31f4830417946105e17f023118c7be6ee', 'SEL-BASELINE-TAG')
    require(sha(read(policy['baseline_matrix'])) == policy['baseline_matrix_sha256'], 'SEL-BASELINE')
    data = checked_baseline(policy['baseline_matrix'], source, policy['baseline_matrix_sha256'])
    require(read(policy['baseline_matrix']) == data, 'SEL-BASELINE')
    return json.loads(data)


def consistency_outputs(policy, read):
    spec = policy['current_consistency']
    path = spec['path']
    old = json.loads(frozen(path, policy['baseline_source']))
    data = read(path)
    current = json.loads(data)
    require(current['rows'] == old['rows'] and len(current['rows']) == 423, 'SEL-CONSISTENCY-ROWS')
    require(read('evaluation/consistency/traceability.csv') == frozen('evaluation/consistency/traceability.csv'), 'SEL-CONSISTENCY-CSV')
    changes = sorted(k for k in set(old) | set(current) if old.get(k) != current.get(k))
    require(changes == sorted(spec['allowed_metadata_changes']), 'SEL-CONSISTENCY-METADATA')
    require(sha(data) == spec['source_sha256'], 'SEL-CONSISTENCY-SOURCE')
    require(current['latest_published_distribution'] == 'v0.3.3' and current['planned_distribution'] == 'v0.3.4'
            and current['current_documentation'] == '0.3.0', 'SEL-CONSISTENCY-METADATA')
    for path, digest in current['input_sha256'].items():
        require(sha(read(path)) == digest, 'SEL-CONSISTENCY-INPUT: ' + path)
    delta = dict(schema='riskium-consistency-metadata-comparison-v1', version='0.2.0',
                 original_source=policy['baseline_source'], current_source=policy['approved_development_source'],
                 old_trace_sha256=sha(frozen(spec['path'])), current_trace_sha256=sha(data),
                 historical_rows=423, rows_identical=True, historical_csv_bytes_identical=True, changed_top_level_keys=changes,
                 historical_summary_unchanged=current['summary'] == old['summary'],
                 new_scientific_executions=0, independent_acceptance_claimed=False,
                 limit='Original row semantics/populations unchanged; only current routing and input-binding metadata advance.')
    paths = ['evaluation/consistency/completion.json', 'evaluation/consistency/findings.json',
             'evaluation/consistency/traceability.json', 'evaluation/consistency/traceability.csv',
             'docs/traceability.md', 'tools/audit_consistency.py']
    component = dict(schema='riskium-current-consistency-component-v1', id='CONSISTENCY', version='0.2.0',
                     compatible_model='0.3.1', replaces_version='0.1.0', historical_rows=423,
                     row_semantics_changed=False, scientific_or_owner_versions_changed=False,
                     files_sha256={**{p: sha(read(p)) for p in paths}, DELTA: sha(encode(delta).encode())},
                     scope='Current metadata/source binding over the unchanged 423-row historical trace; original #39 completion is retained historical evidence, not a new semantic acceptance.')
    return {DELTA: encode(delta), CONSISTENCY: encode(component)}


def descriptor_row(spec, read):
    descriptor = read(spec['descriptor'])
    require(sha(descriptor) == spec['descriptor_sha256'], 'SEL-DESCRIPTOR-SOURCE: ' + spec['id'])
    data = json.loads(descriptor)
    require(data['id'] == spec['id'] and data['version'] == spec['version'] and data['compatible_model'] == '0.3.1', 'SEL-DESCRIPTOR')
    completion_bytes = read(spec['completion'])
    require(sha(completion_bytes) == spec['completion_sha256'], 'SEL-COMPLETION-SOURCE')
    completion = json.loads(completion_bytes)
    require(completion['status'] == 'COMPLETED' and completion['component_version'] == spec['version']
            and completion['model_version'] == '0.3.1', 'SEL-COMPLETION')
    source = completion['implementation_source']
    folder = str(PurePosixPath(spec['completion']).parent)
    software = json.loads(read(folder + '/software-tests.json'))
    hosted = json.loads(read(folder + '/hosted-checks.json'))
    outcome = software.get('outcome', software.get('status'))
    require(software['source_commit'] == hosted['source_commit'] == source and outcome == 'PASS'
            and software['tests'] > 0 and not software.get('failures', 0) and not software.get('errors', 0), 'SEL-EVIDENCE-SOURCE')
    for critical in (spec['descriptor'], folder + '/software-tests.json', folder + '/hosted-checks.json'):
        require(completion['evidence_sha256'][critical] == sha(read(critical)), 'SEL-COMPLETION-EVIDENCE')
    require(len(hosted['workflows']) == 7 and all(w['conclusion'] == 'success' and w['status'] == 'completed'
            for w in hosted['workflows']), 'SEL-HOSTED-EVIDENCE')
    if hosted['schema'] == 'riskium-source-scenario-hosted-checks-v1':
        # The original #42 receipt binds the source at its top level and stores
        # the actual candidate log, without per-workflow head_sha fields. Keep
        # that historical format; do not invent retrospective receipt fields.
        require(hosted['all_workflows_passed'] is True, 'SEL-HOSTED-EVIDENCE')
        candidates = [json.loads(line[line.index('{'):]) for line in hosted['candidate_evidence'] if '{' in line]
        require(len(candidates) == 1 and candidates[0]['source_commit'] == source, 'SEL-EVIDENCE-SOURCE')
        candidate = candidates[0]
    else:
        require(all(w['head_sha'] == source for w in hosted['workflows']), 'SEL-HOSTED-EVIDENCE')
        candidate = hosted['candidate']
    require(candidate['passed_checks'] == 28 and candidate['publication_executed'] is False, 'SEL-RETAINED-CANDIDATE')
    files = dict(data['files_sha256'])
    files[spec['descriptor']] = sha(descriptor)
    files.update({p: sha(read(p)) for p in spec['receipts']})
    return dict(id=data['id'], version=data['version'], compatible_model='0.3.1',
                descriptor_path=spec['descriptor'], completion_record=spec['completion'],
                files=[dict(path=p, sha256=h) for p, h in sorted(files.items())],
                scope='Exact completed development component and retained final-source engineering receipts; no new domain/independent acceptance.')


def expected_rows(policy, read):
    baseline = load_baseline(policy, read)
    rows = {r['id']: copy.deepcopy(r) for r in baseline['artifacts'] if r['id'] not in REPLACED}
    for spec in policy['approved_components']:
        rows[spec['id']] = descriptor_row(spec, read)
    data = json.loads(read(CONSISTENCY))
    rows['CONSISTENCY'] = dict(id='CONSISTENCY', version='0.2.0', compatible_model='0.3.1', descriptor_path=CONSISTENCY,
                               files=[dict(path=p, sha256=h) for p, h in sorted({**data['files_sha256'], CONSISTENCY: sha(read(CONSISTENCY))}.items())],
                               scope=data['scope'])
    return rows, baseline


def dependency_order(versions, graph):
    require(set(graph) == set(versions), 'SEL-DEPENDENCY-SET')
    for ident, dependencies in graph.items():
        require(len({d['id'] for d in dependencies}) == len(dependencies), 'SEL-DEPENDENCY-DUPLICATE')
        for dependency in dependencies:
            require(dependency['id'] in versions, 'SEL-DEPENDENCY-MISSING')
            require(dependency['version'] == versions[dependency['id']], 'SEL-DEPENDENCY-VERSION')
    remaining = list(versions)
    done = []
    while remaining:
        ready = [ident for ident in remaining if all(d['id'] in done for d in graph[ident])]
        require(ready, 'SEL-DEPENDENCY-CYCLE')
        for ident in ready:
            done.append(ident)
            remaining.remove(ident)
    return done


def file_inventory(rows, support, read):
    inventory = {}
    owners = {}
    for row in rows + [dict(id='SELECTION_TOOLING', files=[dict(path=p, sha256=h) for p, h in support.items()])]:
        paths = [safe_path(f['path']) for f in row['files']]
        require(paths and len(paths) == len(set(paths)), 'SEL-FILE-DUPLICATE')
        for item in row['files']:
            p, digest = item['path'], item['sha256']
            require(isinstance(digest, str) and re.fullmatch('[0-9a-f]{64}', digest), 'SEL-HASH-FORMAT')
            require(p not in inventory or inventory[p] == digest, 'SEL-FILE-CONFLICT: ' + p)
            inventory[p] = digest
            owners.setdefault(p, []).append(row['id'])
    for path, digest in inventory.items():
        require(sha(read(path)) == digest, 'SEL-FILE-HASH: ' + path)
    return dict(sorted(inventory.items())), dict(sorted(owners.items()))


def sqlite_chain(policy, inventory, read):
    import relational_assessment as a
    import relational_correction as c
    import relational_source_scenario as k
    import relational_source_scenario_lineage as l
    import relational_evidence as e
    ledger = {1: sha(read('implementation/relational/0.1.0/001_tables.sql')),
              2: sha(read('implementation/relational/0.1.0/002_guards.sql')),
              3: a.migration_hash(), 4: c.digest(), 5: k.digest(), 6: l.digest(), 7: e.digest()}
    rows = []
    previous = 0
    for step in policy['sqlite_chain']:
        require(step['from_schema'] == previous and step['to_schema'] > previous, 'SEL-MIGRATION-CHAIN')
        require(step['reader'] in inventory and all(p in inventory for p in step['migration_files']), 'SEL-MIGRATION-SOURCE')
        rows.append(dict(step, source_files_sha256={p: sha(read(p)) for p in [step['reader'], *step['migration_files']]},
                         schema_migration_ledger_sha256={str(n): ledger[n] for n in range(previous + 1, step['to_schema'] + 1)}))
        previous = step['to_schema']
    require(previous == 7 and [r['to_schema'] for r in rows] == [2, 3, 4, 5, 6, 7], 'SEL-MIGRATION-CHAIN')
    return rows


def validate_selection(matrix, overlay, read=reader):
    policy = json.loads(read(POLICY))
    require(matrix['schema'] == 'riskium-successor-component-selection-v1' and matrix['target'] == 'v0.3.4'
            and matrix['stage'] == 'COMPONENT_SELECTION_NOT_FROZEN', 'SEL-STAGE')
    require(matrix['policy_sha256'] == sha(read(POLICY)), 'SEL-POLICY')
    require(matrix['policy_path'] == POLICY and matrix['overlay_path'] == OVERLAY
            and matrix['issue'] == 47 and matrix['parent_issue'] == 45, 'SEL-SELECTION-IDENTITY')
    require(matrix['source_baseline'] == policy['approved_development_source']
            and matrix['baseline_release'] == policy['baseline_release']
            and matrix['baseline_matrix'] == policy['baseline_matrix']
            and matrix['baseline_matrix_sha256'] == policy['baseline_matrix_sha256'], 'SEL-SOURCE-IDENTITY')
    require(matrix['scientific_versions'] == policy['scientific_versions'] and matrix['boundaries'] == policy['boundaries'], 'SEL-SCOPE')
    require(matrix['future_gates'] == FUTURE_GATES and matrix['limits'] == policy['limits'], 'SEL-FUTURE-GATES')
    for path, digest in policy['preserved_registers_sha256'].items():
        require(sha(read(path)) == digest, 'SEL-PRESERVED-REGISTER: ' + path)
    require(set(matrix['selection_tooling_sha256']) == set(TOOLING), 'SEL-TOOLING')
    require('v0.3.4' not in json.loads(read('releases/stable-profiles.json'))['profiles'], 'SEL-PUBLICATION-REGISTRATION')
    require('v0.3.4' not in json.loads(read('tools/publication/pages-registry.json'))['releases'], 'SEL-SNAPSHOT-REGISTRATION')
    rows = matrix['artifacts']
    versions = {r['id']: r['version'] for r in rows}
    expected_versions = {r['id']: r['version'] for r in policy['components']}
    require(len(rows) == len(versions) == 27 and set(versions) == set(expected_versions), 'SEL-COMPONENT-SET')
    require(versions == expected_versions, 'SEL-VERSION')
    require(all(r['compatible_model'] == '0.3.1' for r in rows), 'SEL-COMPATIBILITY')
    dependency_order(versions, matrix['dependencies'])
    position = {r['id']: n for n, r in enumerate(rows)}
    require(all(position[d['id']] < position[ident] for ident, ds in matrix['dependencies'].items() for d in ds), 'SEL-DEPENDENCY-ORDER')
    require(matrix['dependencies'] == {p['id']: p['depends_on'] for p in policy['components']}, 'SEL-DEPENDENCY-CONTRACT')
    inventory, owners = file_inventory(rows, matrix['selection_tooling_sha256'], read)
    require(inventory == matrix['selected_files_sha256'] and owners == matrix['file_owners'], 'SEL-INVENTORY')
    for path, expected in consistency_outputs(policy, read).items():
        require(read(path) == expected.encode(), 'SEL-CONSISTENCY-DESCRIPTOR')
    expected, baseline = expected_rows(policy, read)
    require(matrix['preserve_releases'] == policy['preserve_releases'] == baseline['preserve_releases'] + ['v0.3.3'], 'SEL-RELEASE-PRESERVATION')
    require(all(row == expected[row['id']] for row in rows), 'SEL-DESCRIPTOR-CLOSURE')
    expected_overlay = dict(schema='riskium-successor-development-overlay-v1', overlay_version='0.3.0', target='v0.3.4',
                            stage=matrix['stage'], baseline_release='v0.3.3', baseline_source=policy['baseline_source'],
                            previous_development_overlay='releases/development-components.json',
                            previous_development_overlay_sha256=sha(read('releases/development-components.json')),
                            components=[r for r in rows if r['id'] in REPLACED | ADDED],
                            dependency_requirements={r['id']: matrix['dependencies'][r['id']] for r in rows if r['id'] in REPLACED | ADDED},
                            scope='Five new/revised selection entries over the retained published baseline; not a replacement of prior matrices, publication or scientific acceptance.')
    require(overlay == expected_overlay and matrix['overlay_sha256'] == sha(encode(overlay).encode()), 'SEL-OVERLAY')
    require(matrix['sqlite_migration_chain'] == sqlite_chain(policy, inventory, read), 'SEL-MIGRATION-CHAIN')
    require(matrix['changes'] == dict(retained=[r['id'] for r in baseline['artifacts'] if r['id'] not in REPLACED],
            replaced=[dict(id=i, from_version=next(r['version'] for r in baseline['artifacts'] if r['id']==i), to_version=expected_versions[i]) for i in sorted(REPLACED)],
            added=sorted(ADDED)), 'SEL-CHANGE-ACCOUNTING')
    require(matrix['summary'] == dict(components=27, retained=22, replaced=2, added=3, selected_unique_files=len(inventory),
                                     overlay_components=5, dependency_edges=sum(map(len, matrix['dependencies'].values()))), 'SEL-SUMMARY')
    return matrix['summary']


def build():
    policy = json.loads(reader(POLICY))
    outputs = consistency_outputs(policy, reader)
    def read(path):
        return outputs[path].encode() if path in outputs else reader(path)
    expected, baseline = expected_rows(policy, read)
    versions = {p['id']: p['version'] for p in policy['components']}
    graph = {p['id']: p['depends_on'] for p in policy['components']}
    rows = [expected[i] for i in dependency_order(versions, graph)]
    support = {p: sha(read(p)) for p in TOOLING}
    inventory, owners = file_inventory(rows, support, read)
    overlay = dict(schema='riskium-successor-development-overlay-v1', overlay_version='0.3.0', target='v0.3.4',
                   stage=policy['stage'], baseline_release='v0.3.3', baseline_source=policy['baseline_source'],
                   previous_development_overlay='releases/development-components.json',
                   previous_development_overlay_sha256=sha(read('releases/development-components.json')),
                   components=[r for r in rows if r['id'] in REPLACED | ADDED],
                   dependency_requirements={r['id']: graph[r['id']] for r in rows if r['id'] in REPLACED | ADDED},
                   scope='Five new/revised selection entries over the retained published baseline; not a replacement of prior matrices, publication or scientific acceptance.')
    matrix = dict(schema='riskium-successor-component-selection-v1', target='v0.3.4', stage=policy['stage'], issue=47, parent_issue=45,
                  policy_path=POLICY, policy_sha256=sha(read(POLICY)), source_baseline=policy['approved_development_source'],
                  scientific_versions=policy['scientific_versions'], boundaries=policy['boundaries'],
                  baseline_release='v0.3.3', baseline_matrix=policy['baseline_matrix'], baseline_matrix_sha256=policy['baseline_matrix_sha256'],
                  preserve_releases=policy['preserve_releases'],
                  overlay_path=OVERLAY, overlay_sha256=sha(encode(overlay).encode()), artifacts=rows, dependencies=graph,
                  changes=dict(retained=[r['id'] for r in baseline['artifacts'] if r['id'] not in REPLACED],
                               replaced=[dict(id=i, from_version=next(r['version'] for r in baseline['artifacts'] if r['id']==i), to_version=versions[i]) for i in sorted(REPLACED)], added=sorted(ADDED)),
                  selection_tooling_sha256=support, selected_files_sha256=inventory, file_owners=owners,
                  sqlite_migration_chain=sqlite_chain(policy, inventory, read),
                  summary=dict(components=27, retained=22, replaced=2, added=3, selected_unique_files=len(inventory), overlay_components=5, dependency_edges=sum(map(len, graph.values()))),
                  future_gates=FUTURE_GATES,
                  limits=policy['limits'])
    validate_selection(matrix, overlay, read)
    outputs[OVERLAY] = encode(overlay)
    outputs[MATRIX] = encode(matrix)
    table = '# Selected components for v0.3.4\n\n**COMPONENT_SELECTION_NOT_FROZEN** — child #47 under #45. No new snapshot, stable profile, tag, assets or publication request is created. Stable remains v0.3.3.\n\n[Machine-readable selection](../../../releases/selection-v0.3.4.json) · [Declared policy](../../../releases/selection-policy-v0.3.4.json) · [Successor overlay](../../../releases/development-components-v0.3.4.json).\n\n| Component | Version | Change | Direct declared prerequisites | Selected file entries |\n| --- | --- | --- | --- | ---: |\n'
    for row in rows:
        ident=row['id'];kind='ADDED' if ident in ADDED else 'REPLACED' if ident in REPLACED else 'RETAINED'
        deps=', '.join(d['id']+' '+d['version'] for d in graph[ident]) or 'None'
        table+='| '+ident+' | '+row['version']+' | '+kind+' | '+deps+' | '+str(len(row['files']))+' |\n'
    table+='\nThere are 27 selected components: 22 retained, two revised and three added. Duplicate shared file paths must bind identical bytes; the union is hashed once and records all owners. The declared prerequisite graph has '+str(matrix['summary']['dependency_edges'])+' edges and is ordered before dependents. It is not a complete runtime/static code ontology.\n\n## SQLite reader and migration chain\n\n| Profile | Schema transition | Reader |\n| --- | --- | --- |\n'
    for row in matrix['sqlite_migration_chain']:
        table+='| '+row['id']+' '+row['version']+' | '+str(row['from_schema'])+' → '+str(row['to_schema'])+' | '+row['reader']+' |\n'
    table+='\nEach step pins selected SQL/reader source hashes and the original ledger digest(s). This is compatibility/selection validation; it is not a new populated database or PostgreSQL/private migration execution. Older exact-schema readers still reject newer schemas. Original executed SQL receipts remain source-bound.\n\n## Consistency and future gates\n\nCONSISTENCY advances from 0.1.0 to 0.2.0 because current routing/input-binding metadata changed during #46. The original 423 rows are identical; [comparison](../../consistency/current-0.2.0/source-comparison.json) preserves the old source and explicitly lists the four changed top-level metadata keys. DOCUMENTATION advances from frozen 0.2.0 to completed current 0.3.0. Previous release matrices and component bytes are not rewritten.\n\nThe documentation component and its 23-file Wiki/243-body HTTP receipts remain the completed #46 checkpoint. Those receipts do not establish freshness for a later source freeze. The next action under #45 is a new documentation snapshot, followed by explicit selection refresh/final-source checks, freeze and independently verified publication. Model 0.3.1, ORSD 0.4.3, original DRSD 0.1.0 and article 7.0.8 remain unchanged; all eleven admissions stay WITHHELD and independent ratings remain zero.\n'
    outputs[TABLE] = table
    return outputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    outputs = build()
    for name, data in outputs.items():
        path = ROOT / name
        if args.check:
            require(path.is_file() and path.read_text() == data, 'SEL-STALE-OUTPUT: ' + name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(data)
    matrix = json.loads(outputs[MATRIX])
    print(json.dumps(dict(status='SUCCESSOR_COMPONENT_SELECTION_PASS', target='v0.3.4', stage=matrix['stage'],
                          **matrix['summary'], publication_executed=False)))


if __name__ == '__main__':
    main()
