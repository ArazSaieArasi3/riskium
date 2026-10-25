"""Deterministic exploratory projection of the exact released OWL; no inference."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
from rdflib import Graph, RDF, RDFS, OWL, URIRef, BNode
from rdflib.compare import to_canonical_graph

ROOT = Path(__file__).resolve().parents[2]
SOURCE = 'ontology/derived/riskium.owl.ttl'
SOURCE_COMMIT = '8afe169968b5c1396c02834dbc499af691b894b4'
BASE = 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'
HERE = Path(__file__).resolve().parent / 'webvowl'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encode(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()


def project(source):
    graph = Graph().parse(data=source.decode(), format='turtle')
    canonical = to_canonical_graph(graph)
    classes = sorted({s for s in graph.subjects(RDF.type, OWL.Class) if isinstance(s, URIRef)}, key=str)
    props = sorted({s for s in graph.subjects(RDF.type, OWL.ObjectProperty) if isinstance(s, URIRef)}, key=str)
    if not classes:
        raise ValueError('Cannot publish an empty class projection')
    ident = lambda x: str(x).removeprefix(BASE)
    label = lambda x: str(graph.value(x, RDFS.label) or ident(x))
    ids = [ident(x) for x in classes + props]
    if len(set(ids)) != len(ids):
        raise ValueError('Projection identifier collision')
    represented = set()
    result = dict(header=dict(languages=['en'], title={'en': 'Riskium asserted OWL core'},
                              iri=BASE.removesuffix('#'), version='Model 0.3.1; view 0.1.0',
                              description={'en': 'Asserted named classes and property endpoints only; no reasoning.'}),
                  namespace=[{'name': 'risk', 'iri': BASE}], **{'class': [], 'classAttribute': [],
                  'property': [], 'propertyAttribute': []})
    terms = []
    for node in classes:
        result['class'].append({'id': ident(node), 'type': 'owl:Class'})
        row = dict(id=ident(node), iri=str(node), label={'en': label(node)})
        comment = graph.value(node, RDFS.comment)
        if comment is not None:
            row['comment'] = {'en': str(comment)}
            represented.add((node, RDFS.comment, comment))
        result['classAttribute'].append(row)
        represented.add((node, RDF.type, OWL.Class))
        represented.update((node, RDFS.label, x) for x in graph.objects(node, RDFS.label))
        terms.append(dict(id=ident(node), iri=str(node), label=label(node), kind='Class',
                          comment=str(comment or ''), native_anchor=ident(node)))
    omitted = []
    for prop in props:
        domains, ranges = list(graph.objects(prop, RDFS.domain)), list(graph.objects(prop, RDFS.range))
        if len(domains) != 1 or len(ranges) != 1 or domains[0] not in classes or ranges[0] not in classes:
            describe = lambda xs: sorted('[anonymous expression]' if isinstance(x, BNode) else str(x) for x in xs)
            omitted.append(dict(iri=str(prop), domains=describe(domains), ranges=describe(ranges),
                                reason='An exact single asserted named-class domain and range are required.'))
            continue
        result['property'].append({'id': ident(prop), 'type': 'owl:ObjectProperty'})
        result['propertyAttribute'].append(dict(id=ident(prop), iri=str(prop), label={'en': label(prop)},
                                                domain=ident(domains[0]), range=ident(ranges[0])))
        for predicate in [RDF.type, RDFS.label, RDFS.domain, RDFS.range]:
            represented.update((prop, predicate, x) for x in graph.objects(prop, predicate))
        comment = graph.value(prop, RDFS.comment)
        terms.append(dict(id=ident(prop), iri=str(prop), label=label(prop), kind='Object property',
                          comment=str(comment or ''), native_anchor=ident(prop),
                          domain=ident(domains[0]), range=ident(ranges[0])))
    subclasses = sorted([(a, b) for a, b in graph.subject_objects(RDFS.subClassOf)
                         if a in classes and b in classes], key=lambda pair: tuple(map(str, pair)))
    for i, (child, parent) in enumerate(subclasses):
        key = 'subclass-' + str(i)
        result['property'].append({'id': key, 'type': 'rdfs:subClassOf'})
        result['propertyAttribute'].append(dict(id=key, domain=ident(child), range=ident(parent),
                                                label={'en': 'subclass of'}))
        represented.add((child, RDFS.subClassOf, parent))
    result['metrics'] = dict(classCount=len(classes), nodeCount=len(classes), datatypeCount=0,
                             objectPropertyCount=len(props)-len(omitted), datatypePropertyCount=0,
                             propertyCount=len(result['property']), individualCount=0)
    result['riskiumSource'] = dict(commit=SOURCE_COMMIT, path=SOURCE, sha256=sha(source),
                                   projection_version='0.1.0', terms=terms)
    def disposition(triple):
        s, p, o = triple
        if p == OWL.disjointWith or (p == RDF.type and o == OWL.AllDisjointClasses):
            return 'Disjointness is not a relationship edge in this view.'
        if any(isinstance(x, BNode) for x in triple):
            return 'Anonymous axiom/expression is outside this named-endpoint projection.'
        return 'Metadata, annotation or other OWL statement remains in the complete source/reference.'
    # Canonical RDF blank-node identifiers make this exact omission inventory reproducible.
    omitted_triples = [dict(statement=' '.join(x.n3() for x in triple) + ' .', reason=disposition(triple))
                       for triple in canonical if triple not in represented]
    omitted_triples.sort(key=lambda row: row['statement'])
    coverage = dict(schema='riskium-webvowl-projection-v1', projection_version='0.1.0',
                     source_commit=SOURCE_COMMIT, source_path=SOURCE, source_sha256=sha(source),
                     source_triples=len(graph), named_classes=len(classes), declared_object_properties=len(props),
                     rendered_object_properties=len(props)-len(omitted), named_subclass_edges=len(subclasses),
                     omitted_properties=omitted, represented_source_triples=len(represented),
                     omitted_source_triples=len(omitted_triples), omission_inventory=omitted_triples,
                     anonymous_terms=len({x for t in canonical for x in t if isinstance(x, BNode)}),
                     policy='Exact asserted named endpoints only. No invented endpoints, closure, OWL restriction, disjointness, OntoUML cardinality, SHACL/SQL or causal interpretation.',
                     browser_execution=False, independent_semantic_validation=False)
    if coverage['represented_source_triples'] + coverage['omitted_source_triples'] != len(graph):
        raise ValueError('Source triple accounting differs from the exact graph')
    return result, coverage


def build(output, root=ROOT):
    source = subprocess.check_output(['git', 'show', SOURCE_COMMIT + ':' + SOURCE], cwd=root)
    data, coverage = project(source)
    target = Path(output) / 'current/webvowl'
    target.mkdir(parents=True, exist_ok=True)
    for name in ['index.html', 'viewer.js', 'viewer.css']:
        shutil.copyfile(HERE/name, target/name)
    shutil.copytree(root/'vendor/webvowl/1.1.7', target/'vendor', dirs_exist_ok=True)
    (target/'data').mkdir(exist_ok=True)
    (target/'data/riskium.json').write_bytes(encode(data))
    (target/'coverage.json').write_bytes(encode(coverage))
    return coverage


def audit(docs, root=ROOT):
    source = subprocess.check_output(['git', 'show', SOURCE_COMMIT + ':' + SOURCE], cwd=root)
    data, coverage = project(source)
    target = Path(docs)/'current/webvowl'
    if (target/'data/riskium.json').read_bytes() != encode(data) or (target/'coverage.json').read_bytes() != encode(coverage):
        raise ValueError('Stale or changed WebVOWL source projection/omission inventory')
    for name in ['index.html','viewer.js','viewer.css']:
        if (target/name).read_bytes() != (HERE/name).read_bytes():
            raise ValueError('Stale viewer shell: ' + name)
    provenance = json.loads((target/'vendor/provenance.json').read_bytes())
    if provenance['upstream_commit'] != '28e7dd9540622e8cb723dc000824b5eef5ae775f':
        raise ValueError('Unreviewed WebVOWL runtime')
    for name, expected in provenance['assets_sha256'].items():
        if sha((target/'vendor'/name).read_bytes()) != expected or (target/'vendor'/name).read_bytes() != (root/'vendor/webvowl/1.1.7'/name).read_bytes():
            raise ValueError('Changed vendored runtime/license: ' + name)
    if sha((HERE/'readonly.patch').read_bytes()) != provenance['patch_sha256'] or sha((HERE/'package-lock.json').read_bytes()) != provenance['package_lock_sha256']:
        raise ValueError('Runtime build/patch provenance changed')
    if (target/'vendor/provenance.json').read_bytes() != (root/'vendor/webvowl/1.1.7/provenance.json').read_bytes():
        raise ValueError('Stale runtime provenance')
    return dict(status='WEBVOWL_PROJECTION_RUNTIME_PASS', classes=coverage['named_classes'],
                object_properties=coverage['rendered_object_properties'], subclasses=coverage['named_subclass_edges'],
                source_triples_accounted=coverage['source_triples'], browser_execution=False)


if __name__ == '__main__':
    report = build(ROOT/'docs')
    print(json.dumps({k:v for k,v in report.items() if k not in ['omission_inventory', 'omitted_properties']}))
