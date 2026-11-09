"""Pin active components separately from the 32 historical v0.3.8 references."""
from pathlib import Path
import hashlib, json, subprocess, sys
import source

ROOT = source.ROOT
OUT = ROOT / 'releases/selection-v0.3.9.json'
POLICY = ROOT / 'releases/selection-policy-v0.3.9.json'
RETAINED = ROOT / 'evaluation/releases/v0.3.9/retained-v0.3.8'

def entry(p):
    return {'path': str(p.relative_to(ROOT)), 'sha256': source.sha(p)}

def prior_bindings(write=False):
    prior = json.loads((ROOT / 'releases/selection-v0.3.8.json').read_text())
    policy = json.loads(POLICY.read_text())
    aliases = {}
    for item in prior['artifacts']:
        for f in item['files']:
            path = ROOT / f['path']
            if path.is_file() and source.sha(path) == f['sha256']:
                continue
            dest = RETAINED / f['path']
            if write:
                body = subprocess.check_output(['git', 'show', policy['predecessor_source_commit'] + ':' + f['path']], cwd=ROOT)
                if hashlib.sha256(body).hexdigest() != f['sha256']:
                    raise ValueError('Historical selection differs from predecessor commit')
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(body)
            if not dest.is_file() or source.sha(dest) != f['sha256']:
                raise ValueError('Historical body missing: ' + f['path'])
            aliases[f['path']] = str(dest.relative_to(ROOT))
    historical = []
    for item in prior['artifacts']:
        historical.append({'id': 'HISTORICAL/' + item['id'], 'artifact': item.get('artifact', item.get('description', item['id'])),
            'version': item['version'], 'compatible_model': item['compatible_model'],
            'status': 'HISTORICAL_REFERENCE_NOT_032_REQUALIFIED', 'original_scope': item.get('scope', item.get('description', 'Historical component at its original source binding.')),
            'files': [{'path': aliases.get(f['path'], f['path']), 'sha256': f['sha256'],
                       'original_path': f['path']} for f in item['files']]})
    return prior, historical, aliases

def make(write_aliases=False):
    source.build(check=True)
    prior, historical, aliases = prior_bindings(write_aliases)
    def component(cid, title, version, paths, scope):
        paths = sorted(set(paths))
        return {'id': cid, 'artifact': title, 'version': version, 'compatible_model': source.VERSION,
            'status': 'ACTIVE_SELECTED_NOT_PUBLISHED', 'scope': scope,
            'files': [entry(p) for p in paths]}
    b = source.b2
    code_inputs = [p for p in source.PACKET.glob('issue93-*/*') if p.is_file() and p.suffix in {'.py', '.cjs', '.sql', '.rq'}]
    for name in ['issue93-generalization-sets/set-policy.json', 'issue93-export-contract/input-contract.json',
                 'issue92-impact/proposed-source-delta.json', 'issue92-impact/acceptance-oracles.json',
                 'issue92-impact/input-bindings.json', 'issue92-riskcase/adopted-inputs.json',
                 'issue92-riskcase/input-contract.json']:
        code_inputs.append(source.PACKET / name)
    code_inputs += list(b.HERE.glob('*.py')) + [b.HERE / n for n in source.NAMES]
    old_contract = json.loads(b.prior.CONTRACT.read_text())
    code_inputs += [ROOT / f['path'] for f in old_contract['frozen_inputs'] + old_contract['generator_inputs']]
    code_inputs += [ROOT / n for n in ['tools/relational_history.py',
        'implementation/relational/0.1.0/001_tables.sql', 'implementation/relational/0.1.0/002_guards.sql']]
    active = [
        component('MODEL032', 'Selected scientific source, native and OWL representations', source.VERSION,
            [source.OUT / n for n in source.render()], 'Version metadata promotion of the reviewed 0.3.2-case.1 source; scientific content and logical graph remain unchanged.'),
        component('CASE_TASK_PROFILE010', 'Selected explicit-data task profiles', '0.1.0',
            [b.HERE / 'case_profiles.py', b.IMPACT / 'acceptance-oracles.json'],
            'Analytical and local operational tasks are distinct. Fresh selected-source tests include a bounded legacy SQLite identity/history slice; no full database migration.'),
        component('READER049', 'Exhaustive source reader and publication projection recipes', '0.4.9',
            list((ROOT / 'documentation/0.4.9/reader').glob('*')) + [source.HERE / n for n in ['reader.py', 'projection.py']],
            '82 catalog dossiers, one external anchor, six navigation pages and matching HTML/Wiki projections; deployment remains R2.'),
        component('PROVENANCE032', 'Source derivation and acceptance provenance', '0.3.2-selection.1', code_inputs + [source.HERE / 'source.py'],
            'Hash-bound derivation inputs and predeclared acceptance oracles. Prior results remain tied to their original execution source.'),
        component('QUALIFICATION039', 'Selected-source release qualification', '0.3.9-R1',
            list(source.HERE.glob('*.py')) + [POLICY, ROOT / 'plans/v0.3.9.md', ROOT / 'tools/check_source_transition.py', ROOT / '.github/workflows/issue93-candidate.yml'],
            'Fresh exact-commit qualification and staged projections; no live publication, independent semantic acceptance or production performance claim.')]
    artifacts = active + historical
    deps = {a['id']: [] for a in artifacts}
    deps.update(CASE_TASK_PROFILE010=['MODEL032', 'PROVENANCE032'], READER049=['MODEL032'],
                PROVENANCE032=[], QUALIFICATION039=['MODEL032', 'CASE_TASK_PROFILE010', 'READER049', 'PROVENANCE032'])
    for cid, entries in prior['dependencies'].items():
        deps['HISTORICAL/' + cid] = ['HISTORICAL/' + d['id'] for d in entries]
    versions = {a['id']: a['version'] for a in artifacts}
    dependencies = {cid: [{'id': d, 'version': versions[d]} for d in ds] for cid, ds in deps.items()}
    files = {}
    for a in artifacts:
        for f in a['files']:
            if f['path'] in files and files[f['path']] != f['sha256']:
                raise ValueError('Conflicting selected body: ' + f['path'])
            files[f['path']] = f['sha256']
    order = []
    def visit(cid, stack):
        if cid in stack:
            raise ValueError('Cyclic selected component dependency')
        if cid in order:
            return
        for d in deps[cid]:
            visit(d, stack + [cid])
        order.append(cid)
    for cid in deps:
        visit(cid, [])
    return {'schema': 'riskium-v039-source-selection-1', 'target': 'v0.3.9',
        'stage': 'SELECTED_NOT_FROZEN_OR_PUBLISHED', 'source_version': source.VERSION,
        'predecessor_release': 'v0.3.8', 'manuscript_version': '7.2.21',
        'artifacts': artifacts, 'dependencies': dependencies, 'dependency_order': order,
        'selected_files_sha256': dict(sorted(files.items())), 'historical_delivery_aliases': aliases,
        'summary': {'active_components': len(active), 'historical_components': len(historical),
                    'selected_files': len(files), 'historical_delivery_aliases': len(aliases)},
        'article_binaries_included': False, 'new_real_case_admissions': 0,
        'independent_semantic_acceptance': False, 'full_database_migration': False}

def build(check=False):
    selected = make(write_aliases=not check)
    body = source.dump(selected)
    if check:
        if not OUT.is_file() or OUT.read_text() != body:
            raise ValueError('Stale package selection')
        for path, digest in selected['selected_files_sha256'].items():
            if source.sha(ROOT / path) != digest:
                raise ValueError('Selected hash mismatch: ' + path)
    else:
        OUT.write_text(body)
    return selected

if __name__ == '__main__':
    print(source.dump(build('--check' in sys.argv)['summary']))
