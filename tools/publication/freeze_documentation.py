"""Register one new documentation snapshot from an exact committed current tree."""
import argparse
import json
import re
from site_registry import ROOT, REGISTRY, check_registry, git, tree_files, freeze_files, sha


def freeze(label, source, version):
    if not re.fullmatch(r'v\d+\.\d+\.\d+', label) or not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise ValueError('Invalid snapshot/model or documentation version')
    registry = check_registry()
    if label in registry['releases']:
        raise ValueError('Existing snapshot cannot be replaced')
    inputs = tree_files(ROOT, source, 'docs/current')
    m = json.loads(inputs['publication-manifest.json'])
    registered_successor = label == 'v0.3.3' and version == '0.2.0' and m['model_version'] == '0.3.1'
    if (label != 'v' + m['model_version'] and not registered_successor) or m['semantic_source_commit'] != '8afe169968b5c1396c02834dbc499af691b894b4':
        raise ValueError('Unreviewed model/documentation compatibility')
    outputs = freeze_files(inputs, label, source, version)
    route = 'releases/' + label
    target = ROOT / 'docs' / route
    if target.exists():
        raise ValueError('Unregistered route collision')
    row = dict(route=route, documentation_version=version, model_version=m['model_version'],
               semantic_source_commit=m['semantic_source_commit'], source_commit=source, source_path='docs/current',
               source_tree=git(ROOT, 'rev-parse', source + ':docs/current').decode().strip(), rendering='FROZEN_GUIDE_REFS_V1',
               files_sha256={p: sha(b) for p, b in outputs.items()})
    for path, content in outputs.items():
        p = target / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(content)
    registry['releases'][label] = row
    (ROOT / REGISTRY).write_text(json.dumps(registry, indent=2) + '\n')
    return row


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--label', required=True)
    parser.add_argument('--source', required=True)
    parser.add_argument('--documentation-version', required=True)
    args = parser.parse_args()
    row = freeze(args.label, args.source, args.documentation_version)
    print(json.dumps({'status': 'DOCUMENTATION_SNAPSHOT_REGISTERED', 'route': row['route'], 'files': len(row['files_sha256']), 'source_commit': row['source_commit'], 'new_source_release_published': False}))
