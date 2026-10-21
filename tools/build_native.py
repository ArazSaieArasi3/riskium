"""Build the OntoUML 1.0.2 exchange representation without changing the source model."""
import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = 'ontology/native/riskium.ontouml.json'
REVIEW = 'evaluation/native-review-decisions.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generalization_sets(model):
    by_parent = defaultdict(list)
    for g in model['generalizations']:
        by_parent[g['general']].append(g)
    result = []
    for parent, group in by_parent.items():
        if len(group) < 2:
            continue
        disjoint = parent in {'RKM-C053', 'RKM-C054'}
        result.append({
            'id': 'GS-' + parent, 'parent': parent,
            'generalizations': [g['id'] for g in group],
            'isDisjoint': disjoint, 'isComplete': False,
            'rationale': ('The current person and organization role specializations inherit distinct human/social-entity identity; other bearer kinds are not ruled out.'
                          if disjoint else 'No blanket exclusivity or covering constraint is imposed on this sibling group.'),
            'example': ('A human and an organization are separate role bearers.' if disjoint
                        else 'A person may be both responsible and authorizing in different assignments; an artifact may also play an evidential role.'),
            'counterexample': ('The same individual cannot be both the human bearer and the organization bearer under these definitions.' if disjoint
                               else 'Do not classify every sibling pair as disjoint or assume these listed specializations exhaust the parent.'),
        })
    kinds = [g['id'] for g in model['generalizations']
             if g['general'] == 'RKM-C047' and g['specific'] in {'RKM-C048', 'RKM-C049'}]
    result.append({'id': 'GS-AgentKinds', 'parent': 'RKM-C047',
                   'generalizations': kinds, 'isDisjoint': True, 'isComplete': False,
                   'rationale': 'Person is defined as a human individual; Organization is an organized social entity. The current model does not close Agent to these two kinds.',
                   'example': 'A person and an employing organization are different agents.',
                   'counterexample': 'An organization must not be merged with a human representative; an unmodeled agent kind is not excluded by a covering axiom.'})
    return result


def build(model, source_sha):
    elements = []

    def named(identifier, kind, name=None, description=None, custom=None):
        return {'id': identifier, 'type': kind, 'created': model['date_local'], 'modified': None,
                'name': {'en': name} if name else None, 'description': {'en': description} if description else None,
                'alternativeNames': [], 'editorialNotes': [], 'creators': [], 'contributors': [],
                'customProperties': custom or {}}

    def package(identifier, title):
        p = named(identifier, 'Package', title)
        p['contents'] = []
        elements.append(p)
        return p

    root = package('RISK-IUM-ROOT', 'Riskium')
    packages = {d['id']: package(d['id'], d['title']) for d in model['domains']}
    foundation = package('PKG-FOUNDATION', 'Foundational anchor')
    rules = package('PKG-CONSTRAINTS', 'Interpretation constraints')
    bridges = package('PKG-BOUNDARIES', 'Optional boundaries')
    root['contents'] = list(packages) + [foundation['id'], rules['id'], bridges['id']]
    all_concepts = {c['id']: c for c in model['concepts'] + model['imported_types']}
    core = [c for c in model['concepts'] if c['scope_layer'] == 'FORMAL_CORE']
    typed_relations = [r for r in model['associations'] if r['scope_layer'] == 'FORMAL_CORE']

    def owner(identifier):
        c = all_concepts[identifier]
        return packages[c['domain_id']] if 'domain_id' in c else foundation

    def nature(c):
        stereotype = c['ontouml_stereotype']
        return {'event': ['event'], 'situation': ['situation'], 'abstract': ['abstract'],
                'mode': ['intrinsic-mode'], 'relator': ['relator']}.get(
                    stereotype, ['functional-complex', 'collective', 'quantity']
                    if c['id'] == 'EXT-OBJECT' else ['functional-complex'])

    for c in core + model['imported_types']:
        e = named(c['id'], 'Class', c['title'], c['definition'], {
            'scopeLayer': c['scope_layer'], 'identitySupplier': c.get('identity_supplier'),
            'identityBasis': c.get('identity_basis'), 'sourceModelSha256': source_sha})
        e.update(stereotype=c['ontouml_stereotype'], isDerived=None,
                 isAbstract=c['is_abstract'], properties=[], literals=[],
                 restrictedTo=nature(c), isPowertype=None, order='1')
        elements.append(e)
        owner(c['id'])['contents'].append(e['id'])

    for r in typed_relations:
        ends = []
        for end in ('source', 'target'):
            p = named(r['id'] + ':' + end, 'Property', custom={'sourceEnd': end})
            p.update(stereotype=None, isDerived=None, subsettedProperties=[],
                     redefinedProperties=[], aggregationKind='NONE',
                     cardinality=r[end + '_end_cardinality'], isOrdered=None,
                     isReadOnly=None, propertyType=r[end])
            elements.append(p)
            ends.append(p['id'])
        e = named(r['id'], 'BinaryRelation', r['predicate'], r.get('basis', r.get('rationale')), {
            'semanticReading': 'source to target; no navigability assertion',
            'multiplicityScope': r.get('multiplicity_scope', 'Managed Riskium profile'), 'sourceModelSha256': source_sha})
        e.update(stereotype=r.get('stereotype'), isDerived=None, isAbstract=None, properties=ends)
        elements.append(e)
        owner(r['source'])['contents'].append(e['id'])

    for g in model['generalizations']:
        e = named(g['id'], 'Generalization')
        e.update(specific=g['specific'], general=g['general'])
        elements.append(e)
        owner(g['specific'])['contents'].append(e['id'])

    sets = generalization_sets(model)
    for s in sets:
        e = named(s['id'], 'GeneralizationSet', description=s['rationale'])
        e.update(isDisjoint=s['isDisjoint'], isComplete=s['isComplete'],
                 generalizations=s['generalizations'], categorizer=None)
        elements.append(e)
        owner(s['parent'])['contents'].append(e['id'])

    for c in model['constraints']:
        e = named(c['id'], 'Note', c['title'], custom={'executionStatus': 'NOT_IMPLEMENTED'})
        e['text'] = {'en': c['statement'] + ' This note records an interpretation constraint; it is not an executable formal encoding.'}
        elements.append(e)
        rules['contents'].append(e['id'])
    for c in model['concepts']:
        if c['scope_layer'] != 'FORMAL_CORE':
            e = named(c['id'], 'Note', c['title'], custom={'scopeLayer': c['scope_layer']})
            e['text'] = {'en': c['definition'] + ' Optional catalog boundary; not a typed-core class.'}
            elements.append(e)
            bridges['contents'].append(e['id'])
    for r in model['associations']:
        if r['scope_layer'] != 'FORMAL_CORE':
            e = named(r['id'], 'Note', r['predicate'], custom={'scopeLayer': r['scope_layer'], 'source': r['source'], 'target': r['target'],
                                                                     'sourceCardinality': r['source_end_cardinality'], 'targetCardinality': r['target_end_cardinality']})
            e['text'] = {'en': r['source_title'] + ' ' + r['predicate'] + ' ' + r['target_title'] + '. Optional external bridge; excluded from the typed relation set.'}
            elements.append(e)
            bridges['contents'].append(e['id'])

    project = named('RISK-IUM-PROJECT', 'Project', 'Riskium',
                    'OntoUML exchange representation of the current conceptual design; bounded validation and review limits are documented separately.')
    project.pop('customProperties')
    project.update(elements=elements, root=root['id'], publisher=None, designedForTasks=[],
                   license=None, accessRights=[], themes=[], contexts=[], ontologyTypes=[],
                   representationStyle=None, namespace=None,
                   landingPages=['https://github.com/ArazSaieArasi3/riskium'], sources=[],
                   bibliographicCitations=[], keywords=[{'en': 'risk knowledge'}],
                   acronyms=['Riskium'], languages=['en'])
    return project


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    model = json.loads((ROOT / 'ontology/riskium-model.json').read_text())
    target = ROOT / TARGET
    serialized = json.dumps(build(model, sha(ROOT / 'ontology/riskium-model.json')), indent=2) + '\n'
    if args.check:
        if not target.exists() or target.read_text() != serialized:
            raise SystemExit('Native exchange is stale or missing.')
        print('Native exchange matches the current generator and source.')
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(serialized)
        print('Wrote ' + TARGET)


if __name__ == '__main__':
    main()
