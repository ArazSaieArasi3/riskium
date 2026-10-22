"""Build application record metadata profiles without changing Riskium axioms."""
import hashlib
import json

from rdflib import BNode, Graph, Literal, Namespace, OWL, RDF, RDFS, URIRef, XSD
from rdflib.collection import Collection

from build_shacl import ROOT, RISK, SH
from run_shacl import normalize_identity

A = Namespace("https://github.com/ArazSaieArasi3/riskium/shapes/0.3.0#")
AP = Namespace("https://github.com/ArazSaieArasi3/riskium/profiles/catalog/0.3.0#")
DC = Namespace("http://purl.org/dc/terms/")
OUT = ROOT / "ontology/shacl/0.3.0"
POLICY = ROOT / "evaluation/shacl/admission/profile-policy.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render():
    model_path = ROOT / "ontology/riskium-model.json"
    model = json.loads(model_path.read_text())
    policy = json.loads(POLICY.read_text())
    review = json.loads((ROOT / "evaluation/coverage-review.json").read_text())
    native = json.loads((ROOT / "evaluation/native-review-decisions.json").read_text())
    if model["version"] != "0.3.1" or native["source_model_sha256"] != digest(model_path):
        raise ValueError("Reviewed conceptual source changed")
    if policy["source_sha256"] != digest(model_path):
        raise ValueError("Admission policy source changed")
    if policy["contract_sha256"] != digest(ROOT / "evaluation/coverage-review.json"):
        raise ValueError("Admission policy contract changed")
    concepts = {c["id"]: c for c in model["concepts"]}
    core = sorted(c["id"] for c in concepts.values() if c["scope_layer"] == "FORMAL_CORE")
    excluded = sorted(set(concepts) - set(core))
    rows = [r for r in review["obligation_reviews"]
            if r["engine"] == "SHACL" and r["family"] == "Admission and class profile"]
    if len(core) != 77 or len(excluded) != 3 or {r["source_element"] for r in rows} != set(concepts):
        raise ValueError("Admission inventory changed")
    for row in rows:
        encoded = json.dumps(concepts[row["source_element"]], sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        if hashlib.sha256(encoded.encode()).hexdigest() != row["source_element_sha256"]:
            raise ValueError("Source-element digest mismatch: " + row["source_element"])
    g = Graph()
    for p, n in (("ad", A), ("ap", AP), ("dct", DC), ("risk", RISK), ("sh", SH)):
        g.bind(p, n)
    g.add((A.Record, RDF.type, SH.NodeShape))
    g.add((A.Record, SH.nodeKind, SH.IRI))

    def prop(owner, name, path, minimum=None, maximum=None, kind=None):
        node = A[name]
        g.add((owner, SH.property, node)); g.add((node, RDF.type, SH.PropertyShape))
        g.add((node, SH.path, path))
        if minimum is not None: g.add((node, SH.minCount, Literal(minimum)))
        if maximum is not None: g.add((node, SH.maxCount, Literal(maximum)))
        if kind is not None: g.add((node, SH.nodeKind, kind))
        return node

    prop(A.Record, "Candidate", AP.candidate, 1, 1, SH.IRI)
    declared = prop(A.Record, "DeclaredClass", AP.declaredClass, 1, 1, SH.IRI)
    allowed = BNode("allowed-core-classes")
    Collection(g, allowed, [RISK[c] for c in core]); g.add((declared, SH["in"], allowed))
    title = prop(A.Record, "Title", DC.title, 1)
    alternatives = []
    for name, datatype in (("StringTitle", XSD.string), ("LanguageTitle", RDF.langString)):
        alt = A[name]; g.add((alt, SH.datatype, datatype)); alternatives.append(alt)
    head = BNode("title-datatypes"); Collection(g, head, alternatives)
    g.add((title, SH["or"], head)); g.add((title, SH.pattern, Literal(r"\S")))
    prop(A.Record, "Subject", DC.subject, 1, kind=SH.IRI)
    prop(A.Record, "Source", DC.source, 1, kind=SH.IRI)
    task = prop(A.Record, "RequestedTask", AP.requestedTask, maximum=1, kind=SH.IRI)
    head = BNode("supported-tasks"); Collection(g, head, [AP.CatalogInspection])
    g.add((task, SH["in"], head))
    g.add((A.Task, RDF.type, SH.NodeShape))
    prop(A.Task, "RequiredTask", AP.requestedTask, 1)
    for cid in core:
        owner = A["For-" + cid]; g.add((owner, RDF.type, SH.NodeShape))
        expected = prop(owner, "ExpectedClass-" + cid, AP.declaredClass)
        g.add((expected, SH.hasValue, RISK[cid]))
        candidate = prop(owner, "CandidateType-" + cid, AP.candidate)
        g.add((candidate, SH["class"], RISK[cid]))
    return g, dict(profile_version="0.3.0", source_sha256=digest(model_path),
                   contract_sha256=digest(ROOT / "evaluation/coverage-review.json"),
                   policy_sha256=digest(POLICY), core_classes=core, excluded_boundaries=excluded,
                   profiles=["raw", "managed-catalog", "task-catalog-inspection"],
                   scope="Application record metadata and explicit candidate class; not full risk-record readiness")


def compile_request(module, raw, requests, profile, catalog):
    """The caller fixes record targets and expected classes outside the data graph."""
    if profile not in ("raw", "managed-catalog", "task-catalog-inspection"):
        raise ValueError("Unsupported admission profile")
    if not requests:
        raise ValueError("An explicit nonempty focus request is required; empty is not acceptance")
    if profile != "raw":
        if any(str(p).startswith(str(AP) + "focus-") for _, p, _ in raw):
            raise ValueError("Managed input cannot supply reserved external-focus selectors")
        for predicate in (RDFS.subClassOf, RDFS.subPropertyOf, RDFS.domain, RDFS.range,
                          OWL.equivalentClass, OWL.equivalentProperty, OWL.imports):
            if any(raw.triples((None, predicate, None))):
                raise ValueError("Managed input cannot supply schema/import axioms; source taxonomy is pinned")
    expected = {}
    normalized, mapping = (raw, {}) if profile == "raw" else normalize_identity(raw)
    for record, cid in requests:
        if cid not in catalog:
            raise ValueError("Expected class is outside the catalog")
        if not isinstance(record, (URIRef, BNode)):
            raise ValueError("A focus record must be an RDF resource")
        record = URIRef(mapping[str(record)]) if str(record) in mapping else record
        if record in expected and expected[record] != cid:
            raise ValueError("Conflicting expected classes for one normalized focus")
        expected[record] = cid
    if profile == "raw":
        return Graph(), normalized, mapping
    # Retain only reachable requested shapes. Restrict the redundant 77-member
    # allowlist to the externally requested core types; per-record hasValue
    # still fixes each exact declaration. No data-derived class selects a rule.
    source = Graph()
    for t in module: source.add(t)
    allowed = BNode("request-core-classes")
    Collection(source, allowed, sorted({RISK[cid] for cid in expected.values()
        if (A["For-" + cid], RDF.type, SH.NodeShape) in module}, key=str))
    source.set((A.DeclaredClass, SH["in"], allowed if len(Collection(source, allowed)) else RDF.nil))
    shapes = Graph(); seen = set()
    pending = [A.Record] + ([A.Task] if profile == "task-catalog-inspection" else [])
    pending += [A["For-" + cid] for cid in expected.values()
                if (A["For-" + cid], RDF.type, SH.NodeShape) in module]
    while pending:
        node = pending.pop()
        if node in seen: continue
        seen.add(node)
        for t in source.triples((node, None, None)):
            shapes.add(t)
            if any(source.triples((t[2], None, None))): pending.append(t[2])
    def target(owner, record):
        if isinstance(record, BNode):
            # SHACL's meta-schema excludes blank-node sh:targetNode values.
            # A private caller-added targetSubjectsOf selector keeps the blank
            # record visible so its managed IRI constraint can reject it.
            selector = AP["focus-" + str(owner).split("#")[-1]]
            normalized.add((record, selector, Literal(True)))
            shapes.add((owner, SH.targetSubjectsOf, selector))
        else:
            shapes.add((owner, SH.targetNode, record))
    for record, cid in expected.items():
        target(A.Record, record)
        if (A["For-" + cid], RDF.type, SH.NodeShape) in module:
            target(A["For-" + cid], record)
        if profile == "task-catalog-inspection":
            target(A.Task, record)
    return shapes, normalized, mapping


def main():
    graph, receipt = render(); OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "admission.ttl"; graph.serialize(destination=path, format="turtle")
    receipt["shapes_sha256"] = digest(path)
    (OUT / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(dict(core_profiles=77, explicit_exclusions=3, triples=len(graph))))


if __name__ == "__main__":
    main()
