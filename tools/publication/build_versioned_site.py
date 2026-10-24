"""Assemble the deployable current portal and exact registered frozen snapshots."""
import argparse
import json
from pathlib import Path
import shutil
import tempfile
from site_registry import ROOT, check_registry, file_map, git, sha
from guides import sync_wiki


def build(output, previous_ref='HEAD', root=ROOT):
    registry = check_registry(root, previous_ref)
    sync_wiki(root, check=True)
    if root.resolve().is_relative_to(output.resolve()) or (output.resolve().is_relative_to(root.resolve()) and not output.resolve().is_relative_to((root / 'build').resolve())):
        raise ValueError('Output must be an independent build directory')
    if output.exists():
        if any(output.iterdir()) and not (output / 'publication-manifest.json').is_file():
            raise ValueError('Refusing to replace an unrelated nonempty output directory')
        shutil.rmtree(output)
    output.mkdir(parents=True)
    for folder in ['current', 'versions', 'site', *[r['route'] for r in registry['releases'].values()]]:
        shutil.copytree(root / 'docs' / folder, output / folder)
    for name in ['index.html', 'interface-review.html', 'THIRD-PARTY-DOCUMENTATION.txt', 'WIDOCO-Apache-2.0.txt', '.nojekyll']:
        shutil.copyfile(root / 'docs' / name, output / name)
    commit = git(root, 'rev-parse', 'HEAD').decode().strip()
    manifest = dict(schema='riskium-deployed-documentation-v1', current_source_commit=commit,
        semantic_source_commit='8afe169968b5c1396c02834dbc499af691b894b4', model_version='0.3.1',
        current_route='current', releases=registry['releases'],
        files_sha256={p: sha(b) for p, b in file_map(output).items()},
        scope='Exact documentation deployment; not a new ontology/source release or semantic acceptance.')
    (output / 'publication-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--previous-ref', default='HEAD')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    from audit_versioned_site import audit
    if args.check:
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / 'site'
            build(folder, args.previous_ref)
            result = audit(folder)
    else:
        if not args.output:
            parser.error('--output is required unless --check is used')
        build(args.output, args.previous_ref)
        result = audit(args.output)
    print(json.dumps(result))
