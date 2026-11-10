"""Select documentary successor components and retain every predecessor binding."""
import argparse
import copy
from pathlib import Path
import curation
import reader
import routing

ROOT = curation.ROOT
OUT = ROOT / 'releases/selection-v0.3.10.json'
RETAINED = ROOT / 'evaluation/releases/v0.3.10/retained-v0.3.9'
ACTIVE = ['MODEL032', 'PROVENANCE032', 'CASE_TASK_PROFILE010', 'CURATION020', 'READER0410', 'DELIVERY0310', 'QUALIFICATION0310', 'PACKAGE0310']


def make(write_aliases=False):
    curation.build(check=True)
    reader.build(check=True)
    prior_path = ROOT / 'releases/selection-v0.3.9.json'
    prior = curation.load(prior_path)
    aliases = {}
    for path, digest in prior['selected_files_sha256'].items():
        if curation.sha((ROOT / path).read_bytes()) == digest:
            continue
        alias = RETAINED / path
        if write_aliases:
            body = routing.git('show', routing.HISTORICAL + ':' + path)
            curation.need(curation.sha(body) == digest, 'Predecessor binding not recoverable: ' + path)
            alias.parent.mkdir(parents=True, exist_ok=True)
            alias.write_bytes(body)
        curation.need(alias.is_file() and curation.sha(alias.read_bytes()) == digest, 'Missing predecessor alias: ' + path)
        aliases[path] = alias.relative_to(ROOT).as_posix()
    old_by = {a['id']: a for a in prior['artifacts']}
    retained = []
    for old in prior['artifacts']:
        item = copy.deepcopy(old)
        item['id'] = 'PRIOR039/' + old['id']
        item['status'] = 'RETAINED_AT_ORIGINAL_VERSION_AND_SOURCE'
        item['original_status'] = old['status']
        for f in item['files']:
            f['predecessor_path'] = f['path']
            f['path'] = aliases.get(f['path'], f['path'])
        retained.append(item)
    def comp(cid, title, version, paths, scope):
        return {'id': cid, 'artifact': title, 'version': version, 'compatible_model': '0.3.2',
                'status': 'PREPARED_NOT_PUBLISHED', 'scope': scope,
                'files': [{'path': p.relative_to(ROOT).as_posix(), 'sha256': curation.sha(p.read_bytes())} for p in sorted(set(paths))]}
    def previous_paths(cid):
        return [ROOT / aliases.get(f['path'], f['path']) for f in old_by[cid]['files']]
    here = Path(__file__).parent
    data = curation.load(curation.REVIEW)
    review_inputs = [ROOT / n for n in data['inputs_sha256']]
    python = sorted(here.glob('*.py')) + sorted((here / 'publication').glob('*.py'))
    package = sorted(p for p in (here / 'package').glob('*') if p.is_file())
    active = [
        comp('MODEL032', 'Preserved scientific source', '0.3.2', previous_paths('MODEL032'), 'Scientific bytes and prior engine receipts are preserved; documentary successor qualification is separate.'),
        comp('PROVENANCE032', 'Preserved scientific derivation and oracles', old_by['PROVENANCE032']['version'], previous_paths('PROVENANCE032'), 'Original source derivation, predeclared oracles and their execution bindings remain unchanged.'),
        comp('CASE_TASK_PROFILE010', 'Preserved explicit-data task profile', '0.1.0', previous_paths('CASE_TASK_PROFILE010'), 'Analytical and local operational task boundaries remain distinct; no new database population is admitted.'),
        comp('CURATION020', 'Current documentary curation', '0.2.0', list(curation.OUT.glob('*')) + review_inputs + [here / 'curation.py'], '82 documentary dispositions, including three normative deferrals; no formal equivalence or independent semantic rating.'),
        comp('READER0410', 'Current source-qualified concept reader', '0.4.10', list(reader.OUT.glob('*')) + [here / 'reader.py', here / 'projection.py'], 'Preserved authored bodies plus current comparisons and separate foundations.'),
        comp('DELIVERY0310', 'Composed full-site and native Wiki candidate', '0.3.10-N5a', list((here / 'guides').glob('*.md')) + list((here / 'wiki-history').glob('*.md')) + [here / 'compose.py', ROOT / 'releases/routing-v0.3.10.json', ROOT / '.github/workflows/publication-v0310.yml'] + [ROOT / routing.CURRENT], 'Retained guides/history and current reader are composed without deployment; legacy writes are disabled and read-only replay is source-pinned. The publication adapter is gated by an exact later release intent and actual public assets.'),
        comp('QUALIFICATION0310', 'Documentary candidate qualification', '0.3.10-N5a', python + [here / 'requirements.txt', here / 'requirements-n5a.txt', ROOT / routing.CURRENT], 'Exact-source integrity, source-pinned replay, paired full-channel output, preserved snapshots and reproducibility; no new engine or expert claim.'),
        comp('PACKAGE0310', 'Deterministic package and offline verifier', '0.3.10-N5a', package, 'Six committed-source assets with separately executable offline integrity and provenance checks. Actual release publication remains N5b.')]
    artifacts = retained + active
    deps = {'PRIOR039/' + cid: ['PRIOR039/' + d['id'] for d in entries] for cid, entries in prior['dependencies'].items()}
    deps.update(MODEL032=[], PROVENANCE032=[], CASE_TASK_PROFILE010=['MODEL032', 'PROVENANCE032'],
                CURATION020=['MODEL032'], READER0410=['MODEL032', 'CURATION020'], DELIVERY0310=['READER0410'],
                QUALIFICATION0310=['CURATION020', 'READER0410', 'DELIVERY0310'], PACKAGE0310=['QUALIFICATION0310'])
    by = {a['id']: a for a in artifacts}
    order = []
    def visit(cid, stack):
        curation.need(cid not in stack and cid in by, 'Invalid component dependency')
        if cid in order:
            return
        for dep in deps[cid]:
            visit(dep, stack + [cid])
        order.append(cid)
    for cid in by:
        visit(cid, [])
    bindings = {}
    for a in artifacts:
        for f in a['files']:
            curation.need(f['path'] not in bindings or bindings[f['path']] == f['sha256'], 'Conflicting selected hash')
            bindings[f['path']] = f['sha256']
    for p in [prior_path, ROOT / 'releases/routing-v0.3.10.json']:
        bindings[p.relative_to(ROOT).as_posix()] = curation.sha(p.read_bytes())
    return {'schema': 'riskium-v0310-source-selection/1', 'target': 'v0.3.10', 'stage': 'PREPARED_NOT_PUBLISHED',
            'source_version': '0.3.2', 'review_version': '0.2.0', 'reader_version': '0.4.10', 'manuscript_version': '7.2.21',
            'predecessor_release': 'v0.3.9', 'predecessor_commit': routing.HISTORICAL,
            'predecessor_selection_sha256': curation.sha(prior_path.read_bytes()),
            'artifacts': artifacts, 'active_component_ids': ACTIVE,
            'dependencies': {cid: [{'id': d, 'version': by[d]['version']} for d in ds] for cid, ds in deps.items()},
            'dependency_order': order, 'historical_delivery_aliases': aliases,
            'selected_files_sha256': dict(sorted(bindings.items())),
            'summary': {'active_components': len(active), 'historical_components': len(retained), 'selected_files': len(bindings), 'historical_aliases': len(aliases)},
            'article_binaries_included': False, 'new_formal_alignments': 0, 'independent_semantic_acceptance': False,
            'full_database_migration': False, 'publication': False, 'live_channel_readback': False}


def build(check=False):
    data = make(not check)
    if check:
        curation.need(curation.load(OUT) == data, 'Stale v0.3.10 component selection')
    else:
        OUT.write_text(curation.dump(data))
    return data


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--check', action='store_true')
    print(curation.dump(build(p.parse_args().check)['summary']))
