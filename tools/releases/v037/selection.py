"""Build the v0.3.7 component closure from pinned, offline-readable sources."""
import argparse
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[3]
POLICY = 'releases/selection-policy-v0.3.7.json'
MATRIX = 'releases/selection-v0.3.7.json'
PRIOR = 'releases/selection-v0.3.6.json'
PRIOR_SHA = 'c4b57867eaed416a3995ce3702b0c6669d0bcd3025ca2fe41eeb779d72aee325'
R4 = 'evaluation/releases/v0.3.7/inputs/r4-completion.json'
R4_SHA = 'c88b82b15de6017c281db21525b1829ea8cdb42604bbbfbafeac14ed2fb9471b'
SCIENCE = dict(model='0.3.1', orsd='0.4.3', original_drsd='0.1.0', manuscript='7.0.8')
SUPPORT = ('tools/releases/v037/selection.py', 'tools/releases/v037/qualify.py',
           'tests/test_release_v037_selection.py', '.github/workflows/release-v037.yml',
           'plans/v0.3.7-packaging.md', 'tools/releases/v037/routing.py',
           'tests/test_release_v037_routing.py', 'releases/routing-v0.3.7.json',
           'docs/release-v0.3.7.md', 'tools/releases/v037/freeze.py',
           'tests/test_release_v037_freeze.py', '.github/workflows/freeze-v037.yml')


def require(value, message):
    if not value:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()


def read(path, root=ROOT):
    require(isinstance(path, str) and path and '\\' not in path and '\x00' not in path, 'Unsafe path')
    p = PurePosixPath(path)
    require(str(p) == path and not p.is_absolute() and not {'.', '..', '.git'} & set(p.parts), 'Unsafe path')
    target = root / path
    require(target.resolve().is_relative_to(root.resolve()) and not target.is_symlink(), 'Unsafe source')
    return target.read_bytes()


def checked(bindings, root):
    for path, digest in bindings.items():
        require(len(digest) == 64 and sha(read(path, root)) == digest, 'Source binding changed: ' + path)


def dependency_order(versions, graph):
    require(set(versions) == set(graph), 'Component dependency set differs')
    for edges in graph.values():
        require(len({e['id'] for e in edges}) == len(edges), 'Duplicate dependency')
        for edge in edges:
            require(edge['id'] in versions and edge['version'] == versions[edge['id']], 'Unresolved dependency')
    remaining = list(versions)
    order = []
    while remaining:
        ready = [i for i in remaining if all(e['id'] in order for e in graph[i])]
        require(ready, 'Component dependency cycle')
        for ident in ready:
            order.append(ident)
            remaining.remove(ident)
    return order


def selection(root=ROOT):
    require(sha(read(PRIOR, root)) == PRIOR_SHA, 'Predecessor selection changed')
    prior = json.loads(read(PRIOR, root))
    policy = json.loads(read(POLICY, root))
    require(policy['target'] == 'v0.3.7' and policy['scientific_versions'] == prior['scientific_versions'] == SCIENCE,
            'Scientific versions or target changed')
    require(set(policy['components']) == {'RISK_NATURE_ASSERTION', 'CONSISTENCY', 'DOCUMENTATION'}, 'Wrong component set')
    old = prior['selected_files_sha256']
    require(len(old) == 780 and len(prior['artifacts']) == 30, 'Wrong predecessor population')
    protected = {p: h for p, h in old.items() if p != '.github/README.md'}
    checked(protected, root)
    require(sha(read('documentation/0.4.1/Repository.md', root)) == old['.github/README.md'], 'Historical landing lost')
    checked(policy['source_support_sha256'], root)
    # R4 proof is the original observed record, not a new qualification claim.
    require(sha(read(R4, root)) == R4_SHA, 'R4 receipt changed')
    r4 = json.loads(read(R4, root))
    require(r4['status'] == 'R4_COMPLETE_R5_READY_NOT_RELEASE_READY'
            and r4['integration_source'] == 'a09ff2d2a460db412ac1a505fef7eb330c0c341e', 'Wrong R4 checkpoint')
    rows = copy.deepcopy(prior['artifacts'])
    for ident, spec in policy['components'].items():
        require(sha(read(spec['descriptor'], root)) == spec['descriptor_sha256'], 'Component descriptor changed')
        desc = json.loads(read(spec['descriptor'], root))
        require(desc['id'] == ident and desc['version'] == spec['version'] and desc['compatible_model'] == '0.3.1',
                'Component identity changed')
        checked(desc['files_sha256'], root)
        previous = next((r for r in rows if r['id'] == ident), None)
        files = {f['path']: f['sha256'] for f in previous['files']} if previous else {}
        files.update(desc['files_sha256'])
        files[spec['descriptor']] = spec['descriptor_sha256']
        if ident == 'DOCUMENTATION':
            require(read('.github/README.md', root) == read('documentation/0.4.4/Repository.md', root), 'Current landing drift')
            files['.github/README.md'] = sha(read('.github/README.md', root))
        if ident == 'RISK_NATURE_ASSERTION':
            declaration = json.loads(read('implementation/relational/0.9.0/declaration-manifest.json', root))
            checked(declaration['files_sha256'], root)
            files.update(declaration['files_sha256'])
        row = dict(id=ident, version=spec['version'], compatible_model='0.3.1',
                   status='SELECTED_NOT_FROZEN', descriptor_path=spec['descriptor'],
                   files=[dict(path=p, sha256=h) for p, h in sorted(files.items())], scope=spec['scope'])
        if previous:
            rows[rows.index(previous)] = row
        else:
            rows.append(row)
    versions = {r['id']: r['version'] for r in rows}
    require(len(versions) == len(rows) == 31, 'Wrong component population')
    deps = copy.deepcopy(prior['dependencies'])
    deps['RISK_NATURE_ASSERTION'] = [dict(id=i, version=versions[i]) for i in
        ('MODEL', 'ORSD', 'DATABASE_REQUIREMENTS', 'ASSESSMENT_SELECTION', 'ASSESSMENT_CORRECTION', 'EVIDENCE_REFERENCE_LIFECYCLE')]
    for ident in ('CONSISTENCY', 'DOCUMENTATION'):
        deps[ident].append(dict(id='RISK_NATURE_ASSERTION', version='0.9.0'))
    for edges in deps.values():
        for edge in edges:
            edge['version'] = versions[edge['id']]
    order = dependency_order(versions, deps)
    inventory = dict(protected)
    def merge(path, digest):
        require(path not in inventory or inventory[path] == digest, 'Conflicting file ownership: ' + path)
        inventory[path] = digest
    for row in rows:
        require(len({f['path'] for f in row['files']}) == len(row['files']), 'Duplicate component file')
        for item in row['files']:
            merge(item['path'], item['sha256'])
    for p, h in policy['source_support_sha256'].items():
        merge(p, h)
    # The retained legacy launch is an explicit routing dependency too.
    routing = json.loads(read('releases/routing-v0.3.7.json', root))
    for p, h in routing['preserved_sha256'].items():
        merge(p, h)
    merge(PRIOR, PRIOR_SHA)
    merge(R4, R4_SHA)
    merge(POLICY, sha(read(POLICY, root)))
    checked(inventory, root)
    return dict(schema='riskium-v037-source-selection-v1', target='v0.3.7', issue=66, stage='SELECTED_NOT_FROZEN',
                predecessor='v0.3.6', predecessor_selection_sha256=PRIOR_SHA, scientific_versions=SCIENCE,
                artifacts=rows, dependencies=deps, dependency_order=order,
                selected_files_sha256=dict(sorted(inventory.items())),
                delivery_support_sha256={p: sha(read(p, root)) for p in SUPPORT},
                summary=dict(components=31, retained=28, replaced=2, added=1, preserved_prior_files=779,
                             selected_files=len(inventory), dependency_edges=sum(map(len, deps.values()))),
                predecessor_landing=dict(original_path='.github/README.md', retained_path='documentation/0.4.1/Repository.md',
                                         sha256=old['.github/README.md']),
                historical_evidence=R4, routing=policy['routing'], freeze_completed=False, release_published=False,
                independent_semantic_acceptance=False, organizational_admissions='11 WITHHELD',
                limits='Bounded synthetic engineering and agent reader inspection; model/OWL remain 0.3.1. Historical pending labels remain dated observations.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    matrix = selection()
    data = encoded(matrix)
    if args.check:
        require(read(MATRIX) == data, 'Selected closure drift; review and regenerate explicitly')
    else:
        (ROOT / MATRIX).write_bytes(data)
    print(json.dumps(dict(status='V037_COMPONENT_SELECTION_PASS', **matrix['summary'], freeze_completed=False, release_published=False)))


if __name__ == '__main__':
    main()
