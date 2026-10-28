"""Bind current documentation 0.3.0 separately from frozen source releases."""
import argparse
import hashlib
import json
from pathlib import Path
from guides import ROOT, entries, wiki_outputs
from site_registry import check_registry

OUT = 'evaluation/documentation/current-0.3.0/component.json'
SOURCES = ['tools/publication/current-status.json', 'tools/publication/guide-registry.json',
           'tools/publication/home.md', 'tools/publication/presentation.py', 'tools/publication/build_portal.py',
           'tools/publication/run_widoco.py', 'tools/publication/build_documentation_component.py',
           'tools/publication/site_registry.py', 'tools/publication/pages-registry.json',
           'tools/publication/build_versioned_site.py', 'tools/publication/audit_portal.py',
           'tools/audit_consistency.py', 'tools/review_distribution.py', 'tests/test_release_v033.py',
           'tests/test_documentation_component.py', 'tests/test_pages_presentation.py',
           'docs/post-release-work.md', 'docs/wiki/README.md', 'tools/publication/README.md',
           'ontology/riskium-model.json', 'ontology/derived/riskium.owl.ttl',
           'evaluation/releases/v0.3.3-publication.json', 'evaluation/relational/source-scenario/completion.json',
           'evaluation/relational/source-scenario-lineage/completion.json',
           'evaluation/relational/qualified-evidence/completion.json']


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def build():
    status = json.loads((ROOT / 'tools/publication/current-status.json').read_text())
    if status['documentation_version'] != '0.3.0' or status['model_version'] != '0.3.1':
        raise ValueError('Unreviewed documentation/model pair')
    if status['latest_release_url'] != 'https://github.com/ArazSaieArasi3/riskium/releases/latest':
        raise ValueError('Latest routing must use the live release destination')
    if status['planned_distribution'] != 'v0.3.4' or status['release_issue'] != 45:
        raise ValueError('Unreviewed successor destination')
    publication = json.loads((ROOT / status['published_checkpoint']['publication_receipt']).read_text())
    if publication['tag'] != status['published_checkpoint']['tag'] or publication['source_commit'] != status['published_checkpoint']['source_commit']:
        raise ValueError('Published checkpoint/source differs')
    registry = check_registry(ROOT, '2bb7c0848a826ba0fba4d22458f43e53736d7b72')
    if status['freeze_registered'] != ('v0.3.4' in registry['releases']):
        raise ValueError('Unexecuted documentation freeze must not be claimed')
    manifest = json.loads((ROOT / 'docs/current/publication-manifest.json').read_text())
    if manifest['documentation_version'] != status['documentation_version'] or manifest['semantic_source_commit'] != '8afe169968b5c1396c02834dbc499af691b894b4':
        raise ValueError('Current documentation manifest/version differs')
    for path, digest in manifest['guide_sources_sha256'].items():
        if sha(path) != digest:
            raise ValueError('Stale guide source: ' + path)
    wiki = wiki_outputs(ROOT)
    for name, content in wiki.items():
        if (ROOT / 'docs/wiki' / name).read_text() != content:
            raise ValueError('Stale Wiki projection: ' + name)
    paths = set(SOURCES) | {row['source'] for row in entries(ROOT)}
    paths |= {p.relative_to(ROOT).as_posix() for p in (ROOT / 'docs/current').rglob('*') if p.is_file()}
    paths |= {'docs/wiki/' + name for name in wiki}
    return dict(schema='riskium-current-documentation-component-v1', id='DOCUMENTATION', version='0.3.0',
                compatible_model='0.3.1', lifecycle='CURRENT_DEVELOPMENT_DOCUMENTATION_NOT_SELECTED_BY_STABLE_DISTRIBUTION',
                execution_issue=46, parent_issue=45, stable_checkpoint=status['published_checkpoint'],
                proposed_distribution='v0.3.4', frozen_snapshot_registered=status['freeze_registered'],
                current_files=sum(p.is_file() for p in (ROOT / 'docs/current').rglob('*')),
                shared_guides=len(entries(ROOT)), native_wiki_files=len(wiki),
                files_sha256={p: sha(p) for p in sorted(paths)},
                preserved_frozen_snapshots=registry['releases'],
                semantic_or_scientific_changes=False, independent_acceptance_claimed=False,
                limits=['File/source binding is separate from live Wiki/Pages publication and fresh readback.',
                        'Published source selections are checked at their actual tag/source; new freezes remain strict about their own current bytes.',
                        'No v0.3.4 source tag/assets/freeze or new scientific/owner/independent acceptance is created by this component.'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    text = json.dumps(data, indent=2) + '\n'
    path = ROOT / OUT
    if args.check:
        if not path.is_file() or path.read_text() != text:
            raise ValueError('Stale current documentation component')
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    print(json.dumps(dict(status='CURRENT_DOCUMENTATION_COMPONENT_PASS', version=data['version'],
                         current_files=data['current_files'], wiki_files=data['native_wiki_files'],
                         frozen_snapshots=len(data['preserved_frozen_snapshots']), source_release_published=False)))


if __name__ == '__main__':
    main()
