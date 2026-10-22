"""Build a bounded application profile for C-11/C-12; never change OWL."""
import hashlib
import json

from rdflib import BNode, Graph, Literal, Namespace, RDF, XSD
from rdflib.collection import Collection

from build_shacl import ROOT, RISK, SH

Q = Namespace("https://github.com/ArazSaieArasi3/riskium/profiles/qualification/0.5.0#")
S = Namespace("https://github.com/ArazSaieArasi3/riskium/shapes/0.5.0#")
DC = Namespace("http://purl.org/dc/terms/")
OUT = ROOT / "ontology/shacl/0.5.0"
ROWS = {"C-11": "SHACL-0626", "C-12": "SHACL-0628"}
SIGNATURES = {"R-05": ("RKM-C019", "RKM-C018"),
              "R-68": ("RKM-C065", "RKM-C014"),
              "RX-021": ("RKM-C065", "RKM-C066")}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def vocabulary_ids(model):
    parent = {g["specific"]: g["general"] for g in model["generalizations"]}
    def descends(cid, ancestor):
        while cid in parent:
            if cid == ancestor: return True
            cid = parent[cid]
        return cid == ancestor
    return sorted(c["id"] for c in model["concepts"] if descends(c["id"], "RKM-C017")), {
        c["id"] for c in model["concepts"] if descends(c["id"], "RKM-C019")}


def render():
    model_path = ROOT / "ontology/riskium-model.json"
    review_path = ROOT / "evaluation/coverage-review.json"
    model = json.loads(model_path.read_text())
    review = json.loads(review_path.read_text())
    native = json.loads((ROOT / "evaluation/native-review-decisions.json").read_text())
    if model["version"] != "0.3.1" or native["source_model_sha256"] != digest(model_path):
        raise ValueError("Conceptual source changed")
    relations = {r["id"]: r for r in model["associations"]}
    for rid, pair in SIGNATURES.items():
        if (relations[rid]["source"], relations[rid]["target"], relations[rid]["scope_layer"]) != (*pair, "FORMAL_CORE"):
            raise ValueError("Relation signature changed: " + rid)
    constraints = {c["id"]: c for c in model["constraints"]}
    rows = []
    for cid, oid in ROWS.items():
        row = next(r for r in review["obligation_reviews"] if r["obligation_id"] == oid)
        encoded = json.dumps(constraints[cid], sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        if row["source_element"] != cid or hashlib.sha256(encoded.encode()).hexdigest() != row["source_element_sha256"]:
            raise ValueError("Source constraint changed: " + cid)
        rows.append(dict(id=oid, source_element=cid, source_element_sha256=row["source_element_sha256"]))
    vocabulary, classified = vocabulary_ids(model)
    graph = Graph()
    for prefix, ns in (("q", Q), ("qs", S), ("risk", RISK), ("sh", SH), ("dct", DC)):
        graph.bind(prefix, ns)

    def node(name):
        owner = S[name]; graph.add((owner, RDF.type, SH.NodeShape))
        graph.add((owner, SH.nodeKind, SH.IRI))
        return owner

    def prop(owner, name, predicate, *, cls=None, kind=None, minimum=1, maximum=1, datatype=None, pattern=None, values=None):
        p = S[name]; graph.add((owner, SH.property, p)); graph.add((p, RDF.type, SH.PropertyShape))
        graph.add((p, SH.path, predicate))
        if minimum is not None: graph.add((p, SH.minCount, Literal(minimum)))
        if maximum is not None: graph.add((p, SH.maxCount, Literal(maximum)))
        if cls: graph.add((p, SH["class"], RISK[cls]))
        if kind: graph.add((p, SH.nodeKind, kind))
        if datatype: graph.add((p, SH.datatype, datatype))
        if pattern: graph.add((p, SH.pattern, Literal(pattern)))
        if values:
            head = BNode("values-" + name); Collection(graph, head, values)
            graph.add((p, SH["in"], head))
        return p

    def sparql(owner, name, query, message):
        q = S[name]; graph.add((owner, SH.sparql, q))
        graph.add((q, RDF.type, SH.SPARQLConstraint))
        graph.add((q, SH.select, Literal("PREFIX q: <" + str(Q) + ">\nPREFIX risk: <" + str(RISK) + ">\n" + query)))
        graph.add((q, SH.message, Literal(message)))

    vocab = node("VocabularyRecord")
    prop(vocab, "VocabCandidate", Q.candidate, cls="RKM-C017", kind=SH.IRI)
    prop(vocab, "VocabScheme", Q.scheme, kind=SH.IRI)
    prop(vocab, "VocabEdition", Q.edition, kind=SH.IRI)
    prop(vocab, "VocabCode", Q.localCode, datatype=XSD.string, pattern=r"\S")
    prop(vocab, "VocabLabel", DC.title, datatype=XSD.string, pattern=r"\S", maximum=None)
    sparql(vocab, "DuplicateKey", """SELECT $this WHERE {
        $this q:candidate ?term ; q:scheme ?scheme ; q:edition ?edition ; q:localCode ?code .
        ?other q:candidate ?otherTerm ; q:scheme ?scheme ; q:edition ?edition ; q:localCode ?code .
        FILTER (?other != $this && ?otherTerm != ?term)
    }""", "Two distinct candidates cannot share a scheme/edition/code application key.")
    classified_shape = node("ClassifiedTerm")
    sparql(classified_shape, "SchemeAgreement", """SELECT $this WHERE {
        $this q:candidate ?term ; q:scheme ?scheme .
        FILTER NOT EXISTS { ?term risk:R-05 ?scheme }
    }""", "The qualified scheme must match the explicit belongsToScheme pair.")
    evidence = node("EvidenceRecord")
    prop(evidence, "EvidenceCandidate", Q.candidate, cls="RKM-C065", kind=SH.IRI)
    prop(evidence, "EvidenceItem", Q.item, cls="RKM-C066", kind=SH.IRI)
    prop(evidence, "EvidenceTarget", Q.target, cls="RKM-C014", kind=SH.IRI)
    prop(evidence, "EvidenceSource", DC.source, kind=SH.IRI)
    prop(evidence, "EvidenceRole", Q.role, kind=SH.IRI, values=[Q.Support, Q.Challenge, Q.Context])
    sparql(evidence, "ItemAgreement", """SELECT $this WHERE {
        $this q:candidate ?ref ; q:item ?item . FILTER NOT EXISTS { ?ref risk:RX-021 ?item }
    }""", "The reference must explicitly point to the qualified evidence item.")
    sparql(evidence, "RoleAgreement", """SELECT $this WHERE {
        $this q:candidate ?ref ; q:target ?target ; q:role ?role .
        FILTER ((?role = q:Support && NOT EXISTS { ?ref risk:R-68 ?target }) ||
                ((?role = q:Challenge || ?role = q:Context) && EXISTS { ?ref risk:R-68 ?target }))
    }""", "Support requires the explicit support pair; challenge/context cannot silently assert it for the same target.")
    return graph, dict(version="0.5.0", source_sha256=digest(model_path), contract_sha256=digest(review_path),
                       obligations=rows, vocabulary_classes=vocabulary, classified_term_classes=sorted(classified),
                       relation_signatures=SIGNATURES, profiles=["raw", "managed"],
                       limits="Application metadata and explicit graph checks; no domain truth or global identity inference")


def main():
    graph, receipt = render(); OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "qualification.ttl"; path.write_text(graph.serialize(format="turtle").rstrip() + "\n")
    receipt["shapes_sha256"] = digest(path)
    (OUT / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(dict(vocabulary=len(receipt["vocabulary_classes"]), triples=len(graph))))


if __name__ == "__main__": main()
