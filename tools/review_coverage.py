"""Audit the formal coverage design. This tool never runs HermiT or SHACL."""
import argparse
import csv
import hashlib
import io
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUTS = {
    'model': 'ontology/riskium-model.json',
    'requirements': 'requirements/requirements.json',
    'questions': 'requirements/competency-questions.json',
    'scope': 'requirements/scope-requirements.json',
    'contract': 'evaluation/coverage-contract.json',
    'rows': 'requirements/test-obligations.csv',
}
CLASS = 'Class satisfiability'
GENERAL = 'Declared subclass entailment'
RELATION = 'Relation mapping'
ENDPOINT = 'Managed-profile endpoint cardinality'
ADMISSION = 'Admission and class profile'
CONSTRAINT = 'Constraint encoding disposition'
REQUIREMENT = 'Requirement acceptance'
QUESTION = 'Competency question'


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     ensure_ascii=False).encode()).hexdigest()


def load_inputs(root=ROOT):
    data = {}
    hashes = {}
    for key, path in INPUTS.items():
        raw = (root / path).read_bytes()
        hashes[path] = hashlib.sha256(raw).hexdigest()
        data[key] = (list(csv.DictReader(io.StringIO(raw.decode())))
                     if key == 'rows' else json.loads(raw))
    data['input_hashes'] = hashes
    return data


def bounds(card):
    parts = card.split('..')
    return int(parts[0]), (None if parts[-1] == '*' else int(parts[-1]))


def audit(data):
    model, rows, contract = data['model'], data['rows'], data['contract']
    errors, reviews = [], []
    concepts = {x['id']: x for x in model['concepts']}
    anchors = {x['id']: x for x in model['imported_types']}
    relations = {x['id']: x for x in model['associations']}
    generals = {x['id']: x for x in model['generalizations']}
    constraints = {x['id']: x for x in model['constraints']}
    req = {x['id']: x for x in data['requirements']}
    cq = {x['id']: x for x in data['questions']}
    scope = {x['id']: x for x in data['scope']}
    decisions = {x['id']: x for x in contract['constraint_dispositions']}
    core = {i for i, c in concepts.items() if c['scope_layer'] == 'FORMAL_CORE'}
    typed_relations = {i for i, r in relations.items() if r['scope_layer'] == 'FORMAL_CORE'}
    expected = Counter()

    def add(engine, family, ids):
        expected.update((engine, family, i) for i in ids)

    add('HermiT', CLASS, core)
    add('HermiT', GENERAL, generals)
    add('HermiT', RELATION, typed_relations)
    add('SHACL', ENDPOINT, [i + ':' + e for i in typed_relations for e in ('source', 'target')])
    add('SHACL', ADMISSION, concepts)
    for engine in ('HermiT', 'SHACL'):
        add(engine, CONSTRAINT, constraints)
    add('Combined', REQUIREMENT, req)
    add('Combined', QUESTION, cq)
    actual = Counter((r['engine'], r['family'], r['model_element']) for r in rows)
    if expected != actual:
        errors.append('obligation allocation mismatch: missing=%d extra=%d' % (
            sum((expected - actual).values()), sum((actual - expected).values())))
    if len({r['test_id'] for r in rows}) != len(rows):
        errors.append('duplicate obligation identifier')
    if set(decisions) != set(constraints) or len(decisions) != len(contract['constraint_dispositions']):
        errors.append('constraint disposition allocation mismatch')
    if contract['source_model_sha256'] != data['input_hashes'][INPUTS['model']]:
        errors.append('source model digest mismatch')
    if contract['source_model_version'] != model['version']:
        errors.append('source model version mismatch')
    for cid, c in constraints.items():
        d = decisions.get(cid)
        if not d:
            continue
        if d['source_statement'] != c['statement']:
            errors.append('stale constraint disposition: ' + cid)
        for field in ('owl_route', 'shacl_route', 'outside_engine_obligation',
                      'positive_case', 'prohibited_case', 'non_entailment_case'):
            if not d.get(field, '').strip():
                errors.append('missing constraint disposition field: ' + cid + ':' + field)
        if d.get('execution_state') != 'NOT_IMPLEMENTED':
            errors.append('unverified execution in constraint disposition: ' + cid)

    for row in rows:
        oid, family, element = row['test_id'], row['family'], row['model_element']
        key = (row['engine'], family, element)
        if key not in expected:
            continue
        if row['status'] != 'NOT_IMPLEMENTED' or row['execution_receipt']:
            errors.append('unverified formal execution claim: ' + oid)
        item = {'obligation_id': oid, 'engine': row['engine'], 'family': family,
                'source_element': element, 'review_state': 'REVIEWED_FOR_PLANNING',
                'formal_execution_state': 'NOT_IMPLEMENTED'}
        source_path = INPUTS['model']
        cases, source = {}, None
        if family == CLASS:
            source = concepts[element]
            cases = {
                'positive': 'The mapped class for %s (%s) is satisfiable.' % (element, source['title']),
                'negative_control': 'A temporary probe in this class and its complement must be unsatisfiable; this checks the oracle, not a domain rule.',
                'boundary': 'An abstract conceptual class is not made unsatisfiable merely because it is abstract.',
            }
        elif family == GENERAL:
            source = generals[element]
            cases = {
                'positive': '%s is a subclass of %s under the reviewed mapping.' % (source['specific'], source['general']),
                'prohibited': 'Removing the mapped axiom must lose the entailment unless another justified path entails it; otherwise record an equivalent mutation.',
                'non_entailment': 'Test the reverse inclusion only after checking the complete hierarchy; a specific/general distinction is not an automatic disjointness assertion.',
            }
        elif family == RELATION:
            source = relations[element]
            cases = {
                'positive': 'Map %s from %s to %s with semantic reading %s; review its property and domain/range axioms before fixing entailment probes.' % (element, source['source'], source['target'], source['predicate']),
                'prohibited': 'Reject reversed endpoints or an unreviewed symmetric, functional, inverse-functional or identity-producing encoding.',
                'boundary': 'Association multiplicities belong to the declared managed profile; do not turn absent explicit values into OWL inconsistency.',
            }
        elif family == ENDPOINT:
            rid, end = element.rsplit(':', 1)
            source = relations[rid]
            opposite = 'target' if end == 'source' else 'source'
            path = 'inverse' if end == 'source' else 'direct'
            direction = opposite + '; ' + path + ' property path'
            if row['direction'] != direction or row['profile'] != 'managed':
                errors.append('endpoint direction/profile mismatch: ' + oid)
            lower, upper = bounds(source[end + '_end_cardinality'])
            valid = {lower, lower + 1 if upper is None else upper}
            cases = {
                'focus_class': source[opposite], 'counted_class': source[end],
                'property': source['predicate'], 'property_path': path,
                'minimum': lower, 'maximum': upper,
                'valid_counts': sorted(valid),
                'below_minimum': {'count': lower - 1, 'expected': 'VIOLATION'} if lower else {
                    'expected': 'NOT_APPLICABLE', 'reason': 'Zero is allowed; a negative node count cannot be constructed.'},
                'above_maximum': {'count': upper + 1, 'expected': 'VIOLATION'} if upper is not None else {
                    'expected': 'NOT_APPLICABLE', 'reason': 'The upper bound is unbounded.'},
                'oracle': 'A negative fixture must identify this focus/path/count rule; other violations must not mask the result.',
            }
        elif family == ADMISSION:
            source = concepts[element]
            if element in core:
                cases = {'positive': 'Retain incomplete input as raw; admit a complete %s only under its declared managed or task-ready profile.' % source['title'],
                         'prohibited': 'Reject an unsupported readiness claim when identity, title, subject, provenance or task-specific inputs are missing.',
                         'boundary': 'The scalar profile vocabulary and task-required inputs must be reviewed before executable shapes are approved.'}
            else:
                cases = {'positive': 'Keep %s as an optional catalog boundary, outside typed-core admission.' % source['title'],
                         'prohibited': 'Reject generation of a managed typed-core class or a core admission shape from this boundary.',
                         'boundary': 'This is an export-boundary test, not satisfiability or admission of an actual referent.'}
        elif family == CONSTRAINT:
            source = constraints[element]
            d = decisions.get(element)
            if not d:
                continue
            cases = {k: d[k] for k in ('positive_case', 'prohibited_case', 'non_entailment_case')}
            item['encoding_route'] = d['owl_route' if row['engine'] == 'HermiT' else 'shacl_route']
            item['outside_engine_obligation'] = d['outside_engine_obligation']
            item['disposition_sha256'] = digest(d)
        elif family == REQUIREMENT:
            source, source_path = req[element], INPUTS['requirements']
            cases = {'positive': source['acceptance_criterion'], 'prohibited': source['negative_acceptance_criterion'],
                     'constraint_ids': source['constraint_ids'],
                     'boundary': 'End-to-end acceptance is separate from allocated elements and engine conformance.'}
            if row['positive_case'] != source['acceptance_criterion'] or row['negative_or_nonentailment_case'] != source['negative_acceptance_criterion']:
                errors.append('stale requirement expectation: ' + oid)
        elif family == QUESTION:
            source, source_path = cq[element], INPUTS['questions']
            cases = {'question': source['question'], 'positive': source['expected_result'], 'prohibited': source['rejection'],
                     'population': source['population'],
                     'boundary': 'Bind exact answer sets, including expected absences, to independent fixtures before execution.'}
            if row['positive_case'] != source['expected_result'] or row['negative_or_nonentailment_case'] != source['rejection']:
                errors.append('stale question expectation: ' + oid)
        item.update(source_file=source_path, source_element_sha256=digest(source), cases=cases)
        reviews.append(item)

    known = set(concepts) | set(anchors) | set(relations) | set(generals) | set(constraints) | set(scope)
    for family in contract['supplementary_families']:
        for key in ('name', 'engine', 'positive', 'negative', 'boundary'):
            if not family.get(key):
                errors.append('incomplete supplementary family: ' + family.get('name', 'unnamed'))
        if not set(family['source_ids']) <= known:
            errors.append('unknown supplementary source: ' + family['name'])
    scope_family = next((x for x in contract['supplementary_families'] if x['name'] == 'Scope requirement acceptance'), {})
    if set(scope_family.get('source_ids', [])) != set(scope):
        errors.append('scope requirement allocation mismatch')

    return {
        'status': 'failed' if errors else 'passed',
        'scope': 'Coverage-design allocation and oracle planning only; not formal execution or independent semantic validation.',
        'errors': sorted(set(errors)), 'contract_version': contract['contract_version'],
        'input_file_sha256': data['input_hashes'],
        'summary': {'baseline_obligations': len(rows), 'reviewed_rows': len(reviews),
                    'by_engine': dict(sorted(Counter(r['engine'] for r in rows).items())),
                    'constraint_routes': len(decisions),
                    'supplementary_families': len(contract['supplementary_families']),
                    'scope_requirements_outside_baseline': len(scope),
                    'formal_cases_implemented': 0, 'formal_cases_executed': 0,
                    'formal_cases_passed': 0},
        'obligation_reviews': reviews,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Regenerate the coverage design review.')
    args = parser.parse_args()
    report = audit(load_inputs())
    target = ROOT / 'evaluation/coverage-review.json'
    serialized = json.dumps(report, indent=2) + '\n'
    if args.write and not report['errors']:
        target.write_text(serialized)
    elif not args.write and (not target.exists() or target.read_text() != serialized):
        report['errors'].append('stored coverage review is missing or stale; run with --write after review')
        report['status'] = 'failed'
    print(json.dumps({k: v for k, v in report.items() if k != 'obligation_reviews'}, indent=2))
    return int(bool(report['errors']))


if __name__ == '__main__':
    raise SystemExit(main())
