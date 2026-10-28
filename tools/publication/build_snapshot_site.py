"""Deploy the preserved current portal plus all four registered snapshots."""
import argparse
import json
from pathlib import Path
import shutil
import tempfile

import build_versioned_site as legacy
from audit_versioned_site import audit
import snapshot_registry as snapshots


def build(output, previous_ref='HEAD', root=snapshots.ROOT):
    registry = snapshots.check_additions(root, previous_ref)
    component = snapshots.build_component(root, previous_ref)
    snapshots.require(json.loads(snapshots.read(root, snapshots.COMPONENT)) == component, 'Stale additive snapshot component')
    manifest = legacy.build(output, previous_ref, root)
    shutil.copytree(root / 'docs' / snapshots.ROUTE, output / snapshots.ROUTE)
    (output / 'versions/index.html').write_bytes(snapshots.version_index(registry))
    manifest['releases'] = registry['releases']
    manifest['snapshot_preparation'] = dict(component=snapshots.COMPONENT,
        component_sha256=snapshots.original.sha(snapshots.read(root, snapshots.COMPONENT)),
        reviewed_source=snapshots.SOURCE, selection_refresh_required=True, source_release_published=False)
    manifest['files_sha256'] = {p: snapshots.original.sha(b) for p, b in legacy.file_map(output).items()
                              if p != 'publication-manifest.json'}
    (output / 'publication-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--previous-ref', default='HEAD')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.check:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'site'
            build(output, args.previous_ref)
            result = audit(output)
    else:
        if not args.output:
            parser.error('--output is required unless --check is used')
        build(args.output, args.previous_ref)
        result = audit(args.output)
    result['selection_refresh_required'] = True
    print(json.dumps(result))


if __name__ == '__main__':
    main()
