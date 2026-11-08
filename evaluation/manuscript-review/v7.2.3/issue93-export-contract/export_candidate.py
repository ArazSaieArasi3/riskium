"""Generate candidate native/OWL through a pinned, additive source contract.

This entry point writes only its own generated directory. It does not update
production exporters, sources, readers, data, or historical evidence packets.
"""
import argparse
import hashlib
import importlib.util
import json
from copy import deepcopy
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CONTRACT = HERE / 'input-contract.json'
VERSION = '0.3.2-structural.2'
TERM_NS = 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'
VERSION_IRI = 'https://github.com/ArazSaieArasi3/riskium/candidates/issue93/generalization-sets'
EVIDENCE_NS = 'https://github.com/ArazSaieArasi3/riskium/candidates/issue93/evidence-use#'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def resolve(path):
    result = (ROOT / path).resolve()
    if not result.is_relative_to(ROOT) or Path(path).is_absolute():
        raise ValueError('Contract path escapes repository')
    return result


def checked_file(entry):
    path = resolve(entry['path'])
    if digest(path) != entry['sha256']:
        raise ValueError('Input digest mismatch: ' + entry['path'])
    return path


def validate_contract(contract):
    if contract['schema'] != 'riskium-candidate-export-contract-1':
        raise ValueError('Unsupported contract schema')
    if contract['source_version'] != VERSION:
        raise ValueError('Unsupported source version')
    if (contract['term_namespace'], contract['version_iri'], contract['evidence_namespace']) != (TERM_NS, VERSION_IRI, EVIDENCE_NS):
        raise ValueError('Namespace/version binding mismatch')
    if contract['ontology_iri'] != TERM_NS.split('/0.3.1#')[0]:
        raise ValueError('Ontology identity mismatch')
    if contract['production_promotion'] is not False:
        raise ValueError('Candidate route cannot promote production')
    source_path = checked_file(contract['source'])
    policy_path = checked_file(contract['policy'])
    for entry in contract['generator_inputs'] + contract['frozen_inputs']:
        checked_file(entry)
    required_generators = {'tools/build_native.py', 'tools/build_owl.py'} | {
        str((HERE.parent / name).relative_to(ROOT)) for name in [
            'issue93-generalization-sets/build_candidate.py',
            'issue93-evidence-use/build_candidate.py',
            'issue93-export-contract/export_candidate.py',
            'issue93-export-contract/candidate_owl.py']}
    if {e['path'] for e in contract['generator_inputs']} != required_generators:
        raise ValueError('Generator dependency binding incomplete')
    required_frozen = {'ontology/riskium-model.json', 'ontology/native/riskium.ontouml.json',
                       'ontology/derived/riskium.owl.ttl', 'evaluation/native-review-decisions.json'}
    if {e['path'] for e in contract['frozen_inputs']} != required_frozen:
        raise ValueError('Frozen dependency binding incomplete')
    if {Path(e['path']).stem for e in contract['downstream_bindings']['definitions']} != {
            'RKM-C014', 'RKM-C047', 'RKM-C065', 'RKM-C066', 'RKM-C075', 'RKM-C076'}:
        raise ValueError('Selected definition binding incomplete')
    for entry in [contract['downstream_bindings']['shacl']] + contract['downstream_bindings']['definitions']:
        checked_file(entry)
    model = json.loads(source_path.read_text())
    policy = json.loads(policy_path.read_text())
    if model['version'] != contract['source_version']:
        raise ValueError('Source/contract version mismatch')
    observed = {k: len(model[k]) for k in ['concepts', 'imported_types', 'associations', 'generalizations', 'constraints']}
    observed.update(formal_classes=sum(c['scope_layer'] == 'FORMAL_CORE' for c in model['concepts']),
                    formal_relations=sum(r['scope_layer'] == 'FORMAL_CORE' for r in model['associations']),
                    retained_sets=len(policy['retained_sets']))
    if observed != contract['inventory']:
        raise ValueError('Inventory mismatch')
    if policy != model['generalization_set_policy']:
        raise ValueError('Source/policy mismatch')
    sets = policy['retained_sets']
    if len({s['id'] for s in sets}) != len(sets) or {'GS-RKM-C014', 'GS-RKM-C047'} & {s['id'] for s in sets}:
        raise ValueError('Invalid explicit set policy')
    if any(s['isComplete'] for s in sets) or sum(bool(s['isDisjoint']) for s in sets) != 3:
        raise ValueError('Unsupported exclusion/covering policy')
    return model, policy


def load_builder():
    path = HERE.parent / 'issue93-generalization-sets/build_candidate.py'
    spec = importlib.util.spec_from_file_location('contract_native_builder', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def render(contract):
    model, policy = validate_contract(contract)
    builder = load_builder()
    # This pure function preserves the explicit set policy; builder.render()
    # is deliberately not called because it rewrites earlier packet outputs.
    native = builder.build_native_with_policy(model, contract['source']['sha256'])
    native_text = dump(native)
    if len(native['elements']) != 596:
        raise ValueError('Unexpected native inventory')
    from candidate_owl import render as render_owl
    binding = deepcopy(contract)
    binding['_receipt_digest'] = hashlib.sha256(dump(contract).encode()).hexdigest()
    owl, receipt = render_owl(model, native, policy, binding, {
        'source': contract['source']['sha256'],
        'policy': contract['policy']['sha256'],
        'native': hashlib.sha256(native_text.encode()).hexdigest()})
    return native_text, owl, receipt


def export(contract, check=False):
    native, owl, mapping = render(contract)
    generated = HERE / 'generated'
    outputs = {'candidate.ontouml.json': native, 'candidate.owl.ttl': owl,
               'mapping-receipt.json': dump(mapping)}
    receipt = {'schema': 'riskium-candidate-export-receipt-1',
               'status': 'CANDIDATE_GENERATED_NOT_PROMOTED',
               'contract_sha256': hashlib.sha256(dump(contract).encode()).hexdigest(),
               'source_version': contract['source_version'],
               'outputs_sha256': {name: hashlib.sha256(value.encode()).hexdigest() for name, value in outputs.items()},
               'downstream_bindings': contract['downstream_bindings'],
               'boundary': 'Bindings identify reviewed candidate inputs, not completed full dictionary/Pages/Wiki publication or database migration.'}
    outputs['export-receipt.json'] = dump(receipt)
    if check:
        if any(not (generated / name).exists() or (generated / name).read_text() != value for name, value in outputs.items()):
            raise ValueError('Candidate outputs or receipt are stale')
    else:
        generated.mkdir(exist_ok=True)
        for name, value in outputs.items():
            (generated / name).write_text(value)
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    print(dump(export(json.loads(CONTRACT.read_text()), check=args.check)))
