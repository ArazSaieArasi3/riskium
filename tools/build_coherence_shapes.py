"""Encode source C-23/C-24 as explicit graph checks, without materialization."""
import hashlib
import json

from rdflib import Graph, Literal, Namespace, OWL, RDF, RDFS, XSD
from build_shacl import ROOT, RISK, SH
from build_admission_shapes import A, AP, DC
from run_shacl import normalize_identity

C = Namespace("https://github.com/ArazSaieArasi3/riskium/shapes/0.4.0#")
OUT = ROOT / "ontology/shacl/0.4.0"
SIGNATURES = {"R-35": ("RKM-X01", "RKM-C002"), "RX-001": ("RKM-X01", "RKM-C002"),
              "R-33": ("RKM-C023", "RKM-C022"), "R-34": ("RKM-C023", "RKM-C023"),
              "RX-006": ("RKM-C015", "RKM-C014")}
CONSTRAINTS = {"C-23": "SHACL-0650", "C-24": "SHACL-0652"}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare(raw, profile):
    if profile == "raw":
        g = Graph()
        for t in raw: g.add(t)
        return g, {}
    if profile != "managed": raise ValueError("Unsupported coherence profile")
    reserved = tuple(map(str, (RISK, C, A, AP, DC, RDF, RDFS, OWL, SH, XSD)))
    for p in (RDFS.subClassOf, RDFS.subPropertyOf, RDFS.domain, RDFS.range,
              OWL.equivalentClass, OWL.equivalentProperty, OWL.imports):
        if any(raw.triples((None, p, None))): raise ValueError("Instance input cannot supply schema/import axioms")
    for p in (OWL.sameAs, OWL.differentFrom):
        for a, b in raw.subject_objects(p):
            if str(a).startswith(reserved) or str(b).startswith(reserved):
                raise ValueError("Instance identity cannot rewrite reserved vocabulary")
    return normalize_identity(raw)


def render():
    path = ROOT / "ontology/riskium-model.json"; model = json.loads(path.read_text())
    review_path = ROOT / "evaluation/coverage-review.json"
    review = json.loads(review_path.read_text())
    native = json.loads((ROOT / "evaluation/native-review-decisions.json").read_text())
    if model["version"] != "0.3.1" or native["source_model_sha256"] != digest(path):
        raise ValueError("Reviewed model changed")
    rels = {r["id"]: r for r in model["associations"]}
    for rid, pair in SIGNATURES.items():
        r = rels[rid]
        if (r["source"], r["target"]) != pair or r["scope_layer"] != "FORMAL_CORE":
            raise ValueError("Reviewed relation signature changed: " + rid)
    constraints = {r["id"]: r for r in model["constraints"]}
    rows = []
    for cid, oid in CONSTRAINTS.items():
        row = next(r for r in review["obligation_reviews"] if r["obligation_id"] == oid)
        encoded = json.dumps(constraints[cid], sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        if row["source_element"] != cid or hashlib.sha256(encoded.encode()).hexdigest() != row["source_element_sha256"]:
            raise ValueError("Constraint contract changed: " + cid)
        rows.append(dict(id=oid, source_element=cid, source_element_sha256=row["source_element_sha256"]))
    g = Graph()
    for prefix, ns in (("co", C), ("risk", RISK), ("sh", SH)): g.bind(prefix, ns)

    def node(name, cls, subjects=(), objects=()):
        n = C[name]; g.add((n, RDF.type, SH.NodeShape)); g.add((n, SH.targetClass, RISK[cls]))
        g.add((n, SH["class"], RISK[cls]))
        for p in subjects: g.add((n, SH.targetSubjectsOf, RISK[p]))
        for p in objects: g.add((n, SH.targetObjectsOf, RISK[p]))
        return n

    def prop(owner, name, path, cls, minimum=None, maximum=None):
        p = C[name]; g.add((owner, SH.property, p)); g.add((p, RDF.type, SH.PropertyShape))
        g.add((p, SH.path, RISK[path])); g.add((p, SH["class"], RISK[cls]))
        if minimum is not None: g.add((p, SH.minCount, Literal(minimum)))
        if maximum is not None: g.add((p, SH.maxCount, Literal(maximum)))
        return p

    def sparql(owner, name, text, message):
        q = C[name]; g.add((owner, SH.sparql, q)); g.add((q, RDF.type, SH.SPARQLConstraint))
        g.add((q, SH.select, Literal("PREFIX risk: <" + str(RISK) + ">\n" + text)))
        g.add((q, SH.message, Literal(message)))

    n = node("C23Case", "RKM-X01", ("R-35", "RX-001"))
    prop(n, "C23AnalyzedType", "R-35", "RKM-C002")
    prop(n, "C23ContextType", "RX-001", "RKM-C002")
    sparql(n, "C23Inclusion", """SELECT $this WHERE {
        $this risk:R-35 ?context . FILTER NOT EXISTS { $this risk:RX-001 ?context }
    }""", "Each explicit analysis-context pair requires its matching general-context pair.")
    n = node("C24Revision", "RKM-C023", ("R-33", "R-34"), ("R-34",))
    p = prop(n, "C24Entry", "R-33", "RKM-C022", 1, 1)
    g.add((p, SH.equals, RISK["RX-006"]))
    prop(n, "C24VersionEntry", "RX-006", "RKM-C022", 1, 1)
    prop(n, "C24Previous", "R-34", "RKM-C023", maximum=1)
    # Separate source shapes make cycle and lineage failures distinguishable
    # even though both use the SPARQL constraint component.
    for owner in (C.C24Acyclic, C.C24Lineage):
        g.add((owner, RDF.type, SH.NodeShape))
        for predicate in (SH.targetClass, SH.targetSubjectsOf, SH.targetObjectsOf):
            for target in g.objects(n, predicate): g.add((owner, predicate, target))
    sparql(C.C24Acyclic, "C24Cycle", """SELECT $this WHERE { $this risk:R-34+ $this }
    """, "previousRevision must be irreflexive and acyclic at every recorded path length.")
    sparql(C.C24Lineage, "C24SameEntry", """SELECT $this WHERE {
        $this risk:R-34 ?previous ; risk:R-33 ?entry .
        FILTER NOT EXISTS { ?previous risk:R-33 ?entry }
    }""", "A predecessor must explicitly identify the same entry.")
    return g, dict(version="0.4.0", source_sha256=digest(path), contract_sha256=digest(review_path),
        obligations=rows, relation_signatures=SIGNATURES, profiles=["raw", "managed"],
        limits="C-23/C-24 static graph conformance; not historical immutability or full managed-record admission")


def main():
    graph, receipt = render(); OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "coherence.ttl"; graph.serialize(destination=path, format="turtle")
    receipt["shapes_sha256"] = digest(path)
    (OUT / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(dict(constraints=list(CONSTRAINTS), triples=len(graph))))


if __name__ == "__main__": main()
