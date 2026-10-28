"""Add the reviewed v0.3.4 snapshot without rewriting the #46/#47 checkpoints."""
import argparse
import copy
import html
import json
from pathlib import Path
import subprocess

import site_registry as original

ROOT = original.ROOT
POLICY = 'tools/publication/snapshot-policy-v0.3.4.json'
ADDITIONS = 'tools/publication/snapshot-additions-v0.3.4.json'
COMPONENT = 'evaluation/documentation/v0.3.4-snapshot/component.json'
SOURCE = '868dd543538857bb5c9ffbdfde458c4323981d01'
LABEL = 'v0.3.4'
VERSION = '0.3.0'
ROUTE = 'releases/' + LABEL
SOURCES = [POLICY, ADDITIONS, 'tools/publication/snapshot_registry.py',
           'tools/publication/build_snapshot_site.py', 'tests/test_documentation_snapshot.py',
           '.github/workflows/documentation.yml', '.github/workflows/pages.yml']
PRESERVED = {original.REGISTRY, 'evaluation/documentation/current-0.3.0/component.json',
             'evaluation/documentation/current-0.3.0/completion.json',
             'releases/selection-policy-v0.3.4.json', 'releases/selection-v0.3.4.json',
             'releases/development-components-v0.3.4.json', 'tools/build_release_selection.py',
             'tests/test_release_selection.py', 'evaluation/releases/v0.3.4-selection/completion.json'}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def encode(value):
    return json.dumps(value, indent=2) + '\n'


def read(root, path):
    original.safe_path(path)
    target = root / path
    require(target.resolve().is_relative_to(root.resolve()) and not target.is_symlink(), 'Unsafe snapshot source path')
    require(target.is_file(), 'Missing snapshot source: ' + path)
    return target.read_bytes()


def review(root=ROOT):
    policy = json.loads(read(root, POLICY))
    require(policy['schema'] == 'riskium-documentation-snapshot-policy-v1'
            and policy['version'] == '0.1.0' and policy['issue'] == 48 and policy['parent_issue'] == 45,
            'Unreviewed snapshot policy identity')
    require((policy['label'], policy['documentation_version'], policy['model_version'], policy['source_commit'])
            == (LABEL, VERSION, '0.3.1', SOURCE), 'Unreviewed snapshot compatibility')
    require(policy['semantic_source_commit'] == original.SEMANTIC_COMMIT
            and policy['source_path'] == 'docs/current' and policy['rendering'] == 'FROZEN_GUIDE_REFS_V1',
            'Unreviewed snapshot rendering/semantic source')
    require(policy['boundaries'] == dict(source_distribution_published=False, stable_profile_registered=False,
            selection_refresh_required=True, independent_acceptance_claimed=False, new_scientific_executions=0),
            'Unreviewed snapshot scope')
    require(set(policy['preserved_files_sha256']) == PRESERVED, 'Preserved checkpoint binding omitted')
    for path, digest in policy['preserved_files_sha256'].items():
        require(original.sha(read(root, path)) == digest, 'Preserved checkpoint changed: ' + path)
        require(read(root, path) == original.git(root, 'show', SOURCE + ':' + path), 'Checkpoint source differs: ' + path)
    selection = json.loads(read(root, 'releases/selection-v0.3.4.json'))
    for path, digest in selection['selected_files_sha256'].items():
        require(original.sha(read(root, path)) == digest, 'Selected checkpoint file changed: ' + path)
    selection_policy = json.loads(read(root, selection['policy_path']))
    for path, digest in selection_policy['preserved_registers_sha256'].items():
        require(original.sha(read(root, path)) == digest, 'Original release register changed: ' + path)
    tree = original.git(root, 'rev-parse', SOURCE + ':docs/current').decode().strip()
    require(tree == policy['source_tree'], 'Reviewed snapshot source tree differs')
    inputs = original.tree_files(root, SOURCE, 'docs/current')
    require(original.file_map(root / 'docs/current') == inputs, 'Current documentation differs from reviewed source')
    require(original.sha(inputs['publication-manifest.json']) == policy['source_manifest_sha256'], 'Reviewed source manifest differs')
    manifest = json.loads(inputs['publication-manifest.json'])
    require(manifest['model_version'] == '0.3.1' and manifest['documentation_version'] == VERSION
            and manifest['semantic_source_commit'] == original.SEMANTIC_COMMIT, 'Source documentation/model pair differs')
    return policy, inputs


def expected_row(policy, inputs):
    outputs = original.freeze_files(inputs, LABEL, SOURCE, VERSION)
    return dict(route=ROUTE, documentation_version=VERSION, model_version='0.3.1',
                semantic_source_commit=original.SEMANTIC_COMMIT, source_commit=SOURCE,
                source_path='docs/current', source_tree=policy['source_tree'], rendering='FROZEN_GUIDE_REFS_V1',
                files_sha256={p: original.sha(b) for p, b in outputs.items()}), outputs


def guard(previous, current):
    require(previous == current, 'Registered snapshot addition cannot be replaced or removed')


def expected_additions(root, policy, row):
    return dict(schema='riskium-documentation-snapshot-additions-v1', version='0.1.0',
                predecessor_registry=original.REGISTRY,
                predecessor_sha256=policy['preserved_files_sha256'][original.REGISTRY],
                policy_path=POLICY, policy_sha256=original.sha(read(root, POLICY)),
                releases={LABEL: row}, stage='SNAPSHOT_REGISTERED_NOT_SOURCE_FROZEN',
                source_distribution_published=False, selection_refresh_required=True)


def check_additions(root=ROOT, previous_ref='HEAD'):
    policy, inputs = review(root)
    predecessor = original.check_registry(root, previous_ref)
    require(len(predecessor['releases']) == 3 and LABEL not in predecessor['releases'], 'Original snapshot register differs')
    row, outputs = expected_row(policy, inputs)
    actual = json.loads(read(root, ADDITIONS))
    require(actual == expected_additions(root, policy, row), 'Snapshot addition identity/source/output differs')
    if previous_ref:
        before = subprocess.run(['git', 'show', previous_ref + ':' + ADDITIONS], cwd=root, capture_output=True)
        if before.returncode == 0:
            guard(json.loads(before.stdout), actual)
    require(original.file_map(root / 'docs' / ROUTE) == outputs, 'Frozen successor snapshot bytes changed')
    combined = copy.deepcopy(predecessor)
    combined['releases'].update(actual['releases'])
    return combined


def register(label, source, version, root=ROOT):
    require((label, source, version) == (LABEL, SOURCE, VERSION), 'Unreviewed snapshot request')
    policy, inputs = review(root)
    original.check_registry(root)
    require(not (root / ADDITIONS).exists() and not (root / 'docs' / ROUTE).exists(), 'Snapshot addition/route already exists')
    target = root / 'docs' / ROUTE
    require(all(not p.is_symlink() for p in [target, *target.parents] if p.is_relative_to(root)), 'Unsafe snapshot route')
    row, outputs = expected_row(policy, inputs)
    for name, content in outputs.items():
        original.safe_path(name)
        path = target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    (root / ADDITIONS).write_text(encode(expected_additions(root, policy, row)))
    return row


def version_index(registry):
    from presentation import render
    links = ''.join('<li><a href="../' + html.escape(row['route']) + '/index.html">'
        + html.escape(label) + '</a> · documentation ' + html.escape(row['documentation_version'])
        + ' · model ' + html.escape(row['model_version']) + ' · source <a href="' + original.REPO
        + '/commit/' + row['source_commit'] + '">' + row['source_commit'][:12] + '</a>'
        + (' · documentation snapshot; source release preparation remains open' if label == LABEL else '') + '</li>'
        for label, row in registry['releases'].items())
    body = '<h1>Documentation versions</h1><p>Current documentation is maintained separately from immutable snapshots. Each snapshot pins its documentation version, model and exact source.</p>'
    body += '<h2>Source distributions</h2><p>Use <a href="' + original.REPO + '/releases/latest">Latest published source release</a> for the live destination. The published checkpoint on 28 October 2026 is <a href="' + original.REPO + '/releases/tag/v0.3.3">v0.3.3</a>. Model <strong>0.3.1</strong> is unchanged.</p>'
    body += '<p>The v0.3.4 entry below is a frozen documentation snapshot of documentation <strong>0.3.0</strong>. It does not publish a source distribution, tag or assets. <a href="' + original.REPO + '/issues/45">v0.3.4 preparation</a> still requires selection refresh, final-source checks/freeze and independently verified publication.</p>'
    body += '<h2>Frozen documentation snapshots</h2><ul>' + links + '</ul><p>The legacy rc.1 route retains its declared historical layout and bytes.</p><p><a href="../current/index.html">Return to current documentation</a></p>'
    return render(Path('versions/index.html'), 'Documentation versions', body).encode()


def build_component(root=ROOT, previous_ref='HEAD'):
    registry = check_additions(root, previous_ref)
    additions = json.loads(read(root, ADDITIONS))
    row = additions['releases'][LABEL]
    files = set(SOURCES) | {'docs/' + ROUTE + '/' + p for p in row['files_sha256']}
    return dict(schema='riskium-documentation-snapshot-component-v1', id='DOCUMENTATION_SNAPSHOT', version='0.1.0',
                issue=48, parent_issue=45, target=LABEL, documentation_version=VERSION, compatible_model='0.3.1',
                snapshot_source=SOURCE, source_tree=row['source_tree'], snapshot_files=len(row['files_sha256']),
                rendering=row['rendering'], stage=additions['stage'], original_snapshots_preserved=3,
                original_documentation_component='evaluation/documentation/current-0.3.0/component.json',
                original_selection_checkpoint='releases/selection-v0.3.4.json',
                files_sha256={p: original.sha(read(root, p)) for p in sorted(files)},
                generated_versions_index_sha256=original.sha(version_index(registry)),
                deployment_entrypoint='tools/publication/build_snapshot_site.py',
                selection_refresh_required=True, source_distribution_published=False,
                independent_acceptance_claimed=False,
                limits=['Original #46 documentation 0.3.0 and #47 selection are preserved dated checkpoints.',
                        'The additive snapshot/tooling component needs explicit selection before a final source-distribution freeze.',
                        'Legacy three-snapshot assembly remains reproducible; the additive entrypoint is required for the deployed four-snapshot site.',
                        'No new scientific execution, owner admission, independent rating or source tag/assets is created.'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--register', action='store_true')
    mode.add_argument('--write-component', action='store_true')
    mode.add_argument('--check', action='store_true')
    parser.add_argument('--label')
    parser.add_argument('--source')
    parser.add_argument('--documentation-version')
    args = parser.parse_args()
    if args.register:
        row = register(args.label, args.source, args.documentation_version)
        print(encode(dict(status='ADDITIVE_DOCUMENTATION_SNAPSHOT_REGISTERED', files=len(row['files_sha256']),
                          source_commit=SOURCE, source_release_published=False)))
        return
    component = build_component()
    if args.write_component:
        path = ROOT / COMPONENT
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(encode(component))
    else:
        require(json.loads(read(ROOT, COMPONENT)) == component, 'Stale additive snapshot component')
    print(encode(dict(status='DOCUMENTATION_SNAPSHOT_COMPONENT_PASS', target=LABEL, snapshot_files=component['snapshot_files'],
                      preserved_snapshots=3, total_snapshots=4, selection_refresh_required=True, source_release_published=False)))


if __name__ == '__main__':
    main()
