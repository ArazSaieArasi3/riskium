"""Compose frozen profiles on one caller-selected graph; never grant global admission.

No document type, missing native type, provenance, selector or identity decision is
created from a catalog envelope. The two cross-module joins are engineering task
rules, not additions to the native ontology. Public validation has no rule switch.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

from pyshacl import validate
from rdflib import BNode, Graph, Literal, Namespace, OWL, RDF, RDFS, URIRef, XSD

from build_shacl import ROOT, RISK, SH, S
from build_admission_shapes import A, AP, DC, compile_request
from build_endpoint_shapes import E
from build_comparison_shapes import SP, SELECTORS
from build_qualification_shapes import Q, S as QS
from run_shacl import normalize_identity
from run_endpoint_shacl import extract

POLICY = ROOT / 'implementation/validation/0.1.0/policy.json'
IP = Namespace('https://github.com/ArazSaieArasi3/riskium/profiles/integration/0.1.0#')
IS = Namespace('https://github.com/ArazSaieArasi3/riskium/shapes/integration/0.1.0#')
PROJECT = 'https://github.com/ArazSaieArasi3/riskium/'
RESERVED = (str(RISK), PROJECT + 'shapes/', PROJECT + 'profiles/',
            str(RDF), str(RDFS), str(OWL), str(SH), str(XSD), str(DC))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_policy():
    policy = json.loads(POLICY.read_text())
    for path, expected in policy['frozen_inputs'].items():
        if digest(ROOT / path) != expected:
            raise ValueError('Frozen integration input changed: ' + path)
    return policy


def named(value):
    if not isinstance(value, str) or not re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:', value):
        raise ValueError('Caller focus must be an absolute named IRI')
    if any(c.isspace() or c in '<>"{}|^`\\' for c in value) or value.startswith(RESERVED):
        raise ValueError('Caller focus cannot be malformed or reserved vocabulary')
    return URIRef(value)


def merge(destination, source, label):
    """Blank-node labels have graph-local scope, even across separately parsed files."""
    mapping = {}
    def scoped(node):
        if isinstance(node, BNode):
            return mapping.setdefault(node, BNode(label + '-' + str(node)))
        return node
    for s, p, o in source:
        destination.add((scoped(s), scoped(p), scoped(o)))


def joint_shapes(request):
    graph = Graph()
    prefix = ('PREFIX ip: <' + str(IP) + '>\nPREFIX sp: <' + str(SP) +
              '>\nPREFIX cp: <' + PROJECT + 'profiles/compatibility/0.6.0#>\n' +
              'PREFIX risk: <' + str(RISK) + '>\n')
    shared = ('$this ip:threshold ?threshold ; sp:leftResult ?left ; sp:rightResult ?right .\n'
              '?threshold risk:RK2-020 ?scale .\n')
    queries = {
        'SharedThresholdScale': shared + '?left risk:R-14 ?ls . ?right risk:R-14 ?rs . FILTER (?scale != ?ls || ?scale != ?rs)',
        'SharedThresholdScaleVersion': shared + '?scale cp:scaleVersion ?v . ?left risk:RX-016 ?lv . ?right risk:RX-016 ?rv . FILTER (?v != ?lv || ?v != ?rv)',
    }
    for name, query in queries.items():
        owner, constraint = IS[name], IS[name + 'Query']
        graph.add((owner, RDF.type, SH.NodeShape))
        graph.add((owner, SH.targetNode, request))
        graph.add((owner, SH.sparql, constraint))
        graph.add((constraint, RDF.type, SH.SPARQLConstraint))
        graph.add((constraint, SH.message, Literal('The caller-selected joint task requires exact normalized scale/version joins.')))
        graph.add((constraint, SH.select, Literal(prefix + 'SELECT $this WHERE {\n' + query + '\n}')))
    return graph


def compile_graph(raw, requests, profile):
    """Return isolated effective data/shapes and identity map without running SHACL."""
    policy = load_policy()
    if profile not in policy['profiles']:
        raise ValueError('Unsupported integration profile')
    data = Graph()
    for triple in raw:
        data.add(triple)
    if profile == 'raw':
        return data, Graph(), {}
    if not isinstance(requests, dict) or set(requests) - {'catalog', 'thresholds', 'comparison', 'vocabulary', 'evidence', 'publication'}:
        raise ValueError('Unexpected external request fields')
    for s, p, o in raw:
        if str(p).startswith((str(SH), str(IP), str(AP) + 'focus-')) or p in SELECTORS:
            raise ValueError('Input cannot supply shapes or caller focus selectors')
        if p in (RDFS.subClassOf, RDFS.subPropertyOf, RDFS.domain, RDFS.range) or str(p).startswith(str(OWL)) and p not in (OWL.sameAs, OWL.differentFrom):
            raise ValueError('Input cannot supply schema/import axioms')
        if p == RDF.type and (str(o).startswith(str(SH)) or o in (OWL.Class, OWL.Ontology, OWL.ObjectProperty, OWL.DatatypeProperty)):
            raise ValueError('Input cannot declare schema/shape resources')
        if p in (OWL.sameAs, OWL.differentFrom) and any(str(x).startswith(RESERVED) for x in (s, o)):
            raise ValueError('Identity cannot rewrite any participating reserved vocabulary')
    data, aliases = normalize_identity(data)
    def focus(value):
        n = named(value)
        return URIRef(aliases.get(str(n), str(n)))
    model = json.loads((ROOT / 'ontology/riskium-model.json').read_text())
    core = {c['id'] for c in model['concepts'] if c['scope_layer'] == 'FORMAL_CORE'}
    catalog = requests.get('catalog', [])
    if not isinstance(catalog, list) or not catalog:
        raise ValueError('Nonempty external catalog focus is required')
    for item in catalog:
        if not isinstance(item, list) or len(item) != 2 or item[1] not in core:
            raise ValueError('Catalog focus must name a supported core class')
    catalog = [(focus(record), cid) for record, cid in catalog]
    candidates = set()
    for record, cid in catalog:
        candidates.update(data.objects(record, AP.candidate))
    typed = {n for n, cls in data.subject_objects(RDF.type) if str(cls).removeprefix(str(RISK)) in core}
    if not typed.issubset(candidates):
        raise ValueError('Native participant lacks caller-selected catalog envelope')
    modules = {name: Graph().parse(ROOT / path, format='turtle') for name, path in policy['modules'].items()}
    shapes, data, _ = compile_request(modules['admission'], data, catalog, 'managed-catalog', core)
    for generalization in model['generalizations']:
        data.add((RISK[generalization['specific']], RDFS.subClassOf, RISK[generalization['general']]))
    if profile == 'managed-catalog':
        return data, shapes, aliases
    comparison = requests.get('comparison', [])
    if not isinstance(comparison, list) or len(comparison) != 5:
        raise ValueError('Joint task requires five comparison focus identities')
    request, left_assessment, left_result, right_assessment, right_result = map(focus, comparison)
    thresholds = requests.get('thresholds', [])
    if not isinstance(thresholds, list) or len(thresholds) != 1:
        raise ValueError('Joint task requires exactly one threshold focus')
    threshold = focus(thresholds[0])
    for key in ('vocabulary', 'evidence', 'publication'):
        if not isinstance(requests.get(key), list) or not requests[key]:
            raise ValueError('Joint task requires nonempty ' + key + ' focus')
    if not {left_assessment, left_result, right_assessment, right_result, threshold}.issubset(candidates):
        raise ValueError('Selected task focus lacks catalog envelope')
    merge(shapes, modules['conditional'], 'conditional')
    merge(shapes, modules['coherence'], 'coherence')
    merge(shapes, modules['qualification'], 'qualification')
    merge(shapes, modules['compatibility'], 'compatibility')
    merge(shapes, modules['comparison'], 'comparison')
    endpoints = extract(modules['endpoints'], [E[r + '-' + end] for r in policy['endpoint_relations'] for end in ('source', 'target')])
    merge(shapes, endpoints, 'endpoints')
    for value in requests['publication']:
        shapes.add((S.C09PublishedDescription, SH.targetNode, focus(value)))
    qualification = json.loads((ROOT / 'ontology/shacl/0.5.0/receipt.json').read_text())
    for item in requests['vocabulary']:
        if not isinstance(item, list) or len(item) != 2 or item[1] not in qualification['vocabulary_classes']:
            raise ValueError('Unsupported vocabulary focus')
        record, cid = item
        shapes.add((QS.VocabularyRecord, SH.targetNode, focus(record)))
        if cid in qualification['classified_term_classes']:
            shapes.add((QS.ClassifiedTerm, SH.targetNode, focus(record)))
    for value in requests['evidence']:
        shapes.add((QS.EvidenceRecord, SH.targetNode, focus(value)))
    compatibility = json.loads((ROOT / 'ontology/shacl/0.6.0/receipt.json').read_text())
    for owner in compatibility['target_owners']:
        shapes.add((URIRef(owner), SH.targetNode, threshold))
    comparison_policy = json.loads((ROOT / 'ontology/shacl/0.7.0/receipt.json').read_text())
    for owner in comparison_policy['target_owners']['selection']:
        for result in (left_result, right_result):
            shapes.add((URIRef(owner), SH.targetNode, result))
    for owner in comparison_policy['target_owners']['comparison']:
        shapes.add((URIRef(owner), SH.targetNode, request))
    for predicate, value in zip(SELECTORS, (left_assessment, left_result, right_assessment, right_result)):
        data.add((request, predicate, value))
    data.add((request, IP.threshold, threshold))
    merge(shapes, joint_shapes(request), 'joint')
    return data, shapes, aliases


def execute_compiled(data, shapes, profile):
    """Run exactly one engine validation on the composed graph."""
    conforms, result, _ = validate(data_graph=data, shacl_graph=shapes, inference='none',
        meta_shacl=True, do_owl_imports=False, advanced=False, abort_on_first=False, inplace=False)
    root = next(result.subjects(RDF.type, SH.ValidationReport))
    findings = sorted({(str(result.value(n, SH.sourceShape)), str(result.value(n, SH.sourceConstraintComponent)),
                       str(result.value(n, SH.focusNode))) for n in result.objects(root, SH.result)})
    if bool(conforms) != (not findings):
        raise RuntimeError('SHACL report conformance contradicts its findings')
    decision = ('CATALOG_ACCEPTED' if conforms else 'CATALOG_NOT_ADMITTED') if profile == 'managed-catalog' else (
        'SCOPED_TASK_ADMISSIBLE' if conforms else 'NOT_ADMISSIBLE_FOR_SCOPED_TASK')
    return dict(decision=decision, conforms=bool(conforms), findings=findings, engine_executed=True,
                task_admissible=decision == 'SCOPED_TASK_ADMISSIBLE'), result


def validate_graph(raw, requests, profile='scoped-comparison'):
    """Engine errors propagate; profile rejection, staging and admission stay distinct."""
    try:
        data, shapes, _ = compile_graph(raw, requests, profile)
    except ValueError as exc:
        return dict(decision='PROFILE_REJECTED', error=str(exc), findings=[], engine_executed=False, task_admissible=False)
    if profile == 'raw':
        return dict(decision='STAGING_ONLY', findings=[], engine_executed=False, task_admissible=False)
    return execute_compiled(data, shapes, profile)[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('graph', type=Path)
    parser.add_argument('request', type=Path, help='Caller-owned JSON focus request, separate from graph')
    parser.add_argument('--profile', default='scoped-comparison')
    args = parser.parse_args()
    # Explicit local Turtle input only; this CLI does not follow RDF imports/JSON-LD contexts.
    result = validate_graph(Graph().parse(args.graph, format='turtle'), json.loads(args.request.read_text()), args.profile)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['decision'] in ('STAGING_ONLY', 'CATALOG_ACCEPTED', 'SCOPED_TASK_ADMISSIBLE') else 1)


if __name__ == '__main__':
    main()
