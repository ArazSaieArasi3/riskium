"""Select the reviewed B2 source as version 0.3.2; no live promotion occurs here."""
from pathlib import Path
from copy import deepcopy
import hashlib, json, sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PACKET = ROOT / 'evaluation/manuscript-review/v7.2.3'
_import_path = sys.path[:]
sys.path.insert(0, str(PACKET / 'issue92-riskcase'))
try:
    import build_candidate as b2
finally:
    sys.path[:] = _import_path

VERSION = '0.3.2'
OUT = ROOT / 'ontology' / VERSION
CONTRACT = OUT / 'source-contract.json'
NAMES = {'candidate-model.json': 'riskium-model.json',
         'candidate.ontouml.json': 'riskium.ontouml.json',
         'candidate.owl.ttl': 'riskium.owl.ttl',
         'input-contract.json': 'source-contract.json',
         'mapping-receipt.json': 'mapping-receipt.json'}
dump = b2.dump
sha = b2.sha
resolve = b2.resolve

def render():
    # B2's prior input is reconstructed and hash-checked, never assumed present.
    b2.build(check=True)
    m = deepcopy(b2.derive())
    m['version'] = VERSION
    m['publication_profile'].update(
        source_design_version=VERSION,
        representation='Selected scientific source for coordinated package v0.3.9; live promotion is a separate publication action')
    original = b2.derive()
    restored = deepcopy(m)
    restored['version'] = original['version']
    restored['publication_profile'] = original['publication_profile']
    if restored != original:
        raise ValueError('Version selection changed scientific content')
    old = json.loads(b2.CONTRACT.read_text())
    dependencies = [b2.HERE / n for n in NAMES] + [HERE / 'source.py']
    c = {'schema': 'riskium-selected-scientific-source-1',
         'source_version': VERSION, 'package_target': 'v0.3.9',
         'stage': 'SELECTED_NOT_PUBLISHED',
         'source': {'path': str((OUT / NAMES['candidate-model.json']).relative_to(ROOT)),
                    'sha256': hashlib.sha256(dump(m).encode()).hexdigest()},
         'term_namespace': old['term_namespace'], 'ontology_iri': old['ontology_iri'],
         'version_iri': 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/' + VERSION,
         'evidence_namespace': old['evidence_namespace'], 'inventory': old['inventory'],
         'policy': old['policy'], 'dependencies': [b2.pin(p) for p in dependencies],
         'frozen_inputs': old['frozen_inputs'], 'production_promotion': False,
         'predecessor_source': old['source'],
         'namespace_policy': 'Existing 0.3.1# term IRIs remain compatibility identifiers. The ontology versionIRI, scientific source version and source digest identify this selected 0.3.2 representation. No term renaming or equivalence axiom is introduced.',
         'boundary': 'Only version/publication metadata differs from the B2 source. Core analytical identity is separate from explicit task readiness and local operational eligibility. Historical SQL/cohort results retain their original source bindings.'}
    builder = b2.prior.load_builder()
    n = builder.build_native_with_policy(m, c['source']['sha256'])
    native = dump(n)
    binding = deepcopy(c)
    binding['_receipt_digest'] = hashlib.sha256(dump(c).encode()).hexdigest()
    owl, receipt = b2.candidate_owl.render(m, n, m['generalization_set_policy'], binding,
        {'source': c['source']['sha256'], 'policy': c['policy']['sha256'],
         'native': hashlib.sha256(native.encode()).hexdigest()})
    old_label = 'Riskium candidate typed-core mapping ' + VERSION
    if owl.count(old_label) != 1:
        raise ValueError('Unexpected ontology label')
    owl = owl.replace(old_label, 'Riskium selected typed-core mapping ' + VERSION)
    receipt['output_sha256'] = hashlib.sha256(owl.encode()).hexdigest()
    return {'riskium-model.json': dump(m), 'riskium.ontouml.json': native,
            'riskium.owl.ttl': owl, 'source-contract.json': dump(c),
            'mapping-receipt.json': dump(receipt)}

def build(check=False):
    files = render()
    if check:
        if not OUT.is_dir() or {p.name for p in OUT.iterdir() if p.is_file()} != set(files):
            raise ValueError('Selected scientific inventory differs')
        for name, body in files.items():
            if (OUT / name).read_text() != body:
                raise ValueError('Stale selected scientific artifact: ' + name)
    else:
        OUT.mkdir(parents=True, exist_ok=True)
        for name, body in files.items():
            (OUT / name).write_text(body)
    return files

def validate_contract(c):
    if c != json.loads(render()['source-contract.json']):
        raise ValueError('Selected source contract mismatch')
    for entry in c['dependencies'] + c['frozen_inputs'] + [c['policy'], c['source']]:
        b2.checked(entry)
    m = json.loads(resolve(c['source']['path']).read_text())
    return m, m['generalization_set_policy']

if __name__ == '__main__':
    print(dump({'version': VERSION, 'files': list(build('--check' in sys.argv)), 'published': False}))
