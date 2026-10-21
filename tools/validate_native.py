"""Check the exchange schema and source fidelity; no domain-validity claim."""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from build_native import TARGET, generalization_sets

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_SHA256 = '094324d8e6ac4505ef5ae983a45bb9b56a8b3b6960151c57736756a037344d38'


def check_fidelity(model, native):
    errors = []
    es = native.get('elements', [])
    by = {e['id']: e for e in es}
    if len(by) != len(es):
        errors.append('duplicate native identifier')
    classes = {e['id']: e for e in es if e['type'] == 'Class'}
    concepts = {c['id']: c for c in model['concepts'] if c['scope_layer'] == 'FORMAL_CORE'}
    concepts.update({c['id']: c for c in model['imported_types']})
    if set(classes) != set(concepts):
        errors.append('typed class allocation mismatch')
    for i, c in concepts.items():
        e = classes.get(i, {})
        checks = [(e.get('name', {}).get('en'), c['title']),
                  (e.get('description', {}).get('en'), c['definition']),
                  (e.get('stereotype'), c['ontouml_stereotype']),
                  (e.get('isAbstract'), c['is_abstract']),
                  (e.get('customProperties', {}).get('identitySupplier'), c.get('identity_supplier'))]
        if any(a != b for a, b in checks):
            errors.append('class semantics changed: ' + i)
    relations = {r['id']: r for r in model['associations'] if r['scope_layer'] == 'FORMAL_CORE'}
    encoded = {e['id']: e for e in es if e['type'] == 'BinaryRelation'}
    if set(encoded) != set(relations):
        errors.append('typed relation allocation mismatch')
    for i, r in relations.items():
        e = encoded.get(i, {})
        if e.get('name', {}).get('en') != r['predicate'] or e.get('stereotype') != r.get('stereotype'):
            errors.append('relation meaning changed: ' + i)
        expected_ends = [i + ':source', i + ':target']
        if e.get('properties') != expected_ends:
            errors.append('relation end order changed: ' + i)
        for end in ('source', 'target'):
            p = by.get(i + ':' + end, {})
            if p.get('type') != 'Property' or p.get('propertyType') != r[end] or p.get('cardinality') != r[end + '_end_cardinality']:
                errors.append('relation endpoint/cardinality changed: ' + i + ':' + end)
    expected_property_ids = {i + ':' + end for i in relations for end in ('source', 'target')}
    if {e['id'] for e in es if e['type'] == 'Property'} != expected_property_ids:
        errors.append('relation property allocation mismatch')
    generals = {g['id']: g for g in model['generalizations']}
    encoded_g = {e['id']: e for e in es if e['type'] == 'Generalization'}
    if set(encoded_g) != set(generals):
        errors.append('generalization allocation mismatch')
    for i, g in generals.items():
        if any(encoded_g.get(i, {}).get(k) != g[k] for k in ('specific', 'general')):
            errors.append('generalization direction changed: ' + i)
    expected_sets = {s['id']: s for s in generalization_sets(model)}
    encoded_sets = {e['id']: e for e in es if e['type'] == 'GeneralizationSet'}
    if set(expected_sets) != set(encoded_sets):
        errors.append('generalization-set allocation mismatch')
    for i, s in expected_sets.items():
        e = encoded_sets.get(i, {})
        if any(e.get(k) != s[k] for k in ('generalizations', 'isDisjoint', 'isComplete')):
            errors.append('generalization-set decision changed: ' + i)
    for c in model['constraints']:
        e = by.get(c['id'], {})
        if e.get('type') != 'Note' or not e.get('text', {}).get('en', '').startswith(c['statement']):
            errors.append('constraint note changed: ' + c['id'])
    for c in model['concepts']:
        if c['scope_layer'] != 'FORMAL_CORE' and by.get(c['id'], {}).get('type') != 'Note':
            errors.append('boundary promoted or lost: ' + c['id'])
    for r in model['associations']:
        if r['scope_layer'] == 'FORMAL_CORE':
            continue
        e = by.get(r['id'], {})
        expected = {'source': r['source'], 'target': r['target'],
                    'sourceCardinality': r['source_end_cardinality'], 'targetCardinality': r['target_end_cardinality']}
        if e.get('type') != 'Note' or any(e.get('customProperties', {}).get(k) != v for k, v in expected.items()):
            errors.append('bridge disposition changed: ' + r['id'])
    for e in es:
        for key in ('properties', 'contents', 'generalizations'):
            if any(i not in by for i in e.get(key, [])):
                errors.append('unresolved native reference: ' + e['id'] + ':' + key)
        for key in ('propertyType', 'specific', 'general', 'categorizer'):
            if e.get(key) is not None and e[key] not in by:
                errors.append('unresolved native reference: ' + e['id'] + ':' + key)
    for d in model['domains']:
        contents = set(by.get(d['id'], {}).get('contents', []))
        wanted = {i for i in d['concept_ids'] if i in concepts}
        if not wanted <= contents:
            errors.append('native domain membership lost: ' + d['id'])
    return sorted(set(errors))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--schema', type=Path, required=True, help='Pinned upstream schema file; see native-model-review.md.')
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    from jsonschema import Draft202012Validator, FormatChecker
    raw = args.schema.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SCHEMA_SHA256:
        raise SystemExit('Schema digest does not match the reviewed upstream dependency.')
    schema = json.loads(raw)
    Draft202012Validator.check_schema(schema)
    checker = FormatChecker(formats=['date', 'date-time', 'uri'])
    model_path = ROOT / 'ontology/riskium-model.json'
    model = json.loads(model_path.read_text())
    path = ROOT / TARGET
    native = json.loads(path.read_text())
    schema_errors = [str(e.json_path) + ': ' + e.message[:200]
                     for e in Draft202012Validator(schema, format_checker=checker).iter_errors(native)]
    errors = check_fidelity(model, native)
    report = {
        'scope': 'OntoUML exchange-schema conformance and source fidelity; not full semantic, editor, HermiT or SHACL validation.',
        'status': 'failed' if schema_errors or errors else 'passed',
        'schema_id': schema['$id'], 'schema_sha256': SCHEMA_SHA256,
        'source_model_sha256': hashlib.sha256(model_path.read_bytes()).hexdigest(),
        'native_file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'schema_errors': schema_errors, 'fidelity_errors': errors,
        'element_counts': dict(sorted(Counter(e['type'] for e in native['elements']).items())),
        'formal_constraints_executable': 0, 'native_editor_import_executed': False,
    }
    if args.write and report['status'] == 'passed':
        (ROOT / 'evaluation/native-exchange-checks.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return int(report['status'] != 'passed')


if __name__ == '__main__':
    raise SystemExit(main())
