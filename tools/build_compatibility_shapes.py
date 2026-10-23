"""C-08 application metadata policy; no new native ontology relation or axiom."""
import hashlib
import json

from rdflib import BNode, Graph, Literal, Namespace, OWL, RDF, RDFS, URIRef, XSD
from rdflib.collection import Collection
from build_shacl import ROOT, RISK, SH
from build_coherence_shapes import prepare as prepare_base

C = Namespace("https://github.com/ArazSaieArasi3/riskium/shapes/0.6.0#")
CP = Namespace("https://github.com/ArazSaieArasi3/riskium/profiles/compatibility/0.6.0#")
OUT = ROOT / "ontology/shacl/0.6.0"
POLICY = ROOT / "evaluation/shacl/compatibility/profile-policy.json"
SIGNATURES = {"RX-025": ("RKM-C070", "RKM-C069"), "RK2-020": ("RKM-C070", "RKM-C036"),
              "RK2-019": ("RKM-C036", "RKM-C039"), "RX-006": ("RKM-C015", "RKM-C014")}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare(raw, profile, targets):
    if profile not in ("raw", "dual-anchor-metadata"):
        raise ValueError("Unsupported compatibility profile")
    if not targets or any(not isinstance(t, URIRef) for t in targets):
        raise ValueError("Explicit nonempty named threshold focus is required")
    if profile != "raw":
        for predicate in (OWL.sameAs, OWL.differentFrom):
            for a, b in raw.subject_objects(predicate):
                if any(str(x).startswith((str(C), str(CP))) for x in (a, b)):
                    raise ValueError("Instance identity cannot rewrite reserved compatibility vocabulary")
    return prepare_base(raw, "raw" if profile == "raw" else "managed")


def render():
    model_path = ROOT / "ontology/riskium-model.json"
    model = json.loads(model_path.read_text()); policy = json.loads(POLICY.read_text())
    contract_path = ROOT / "evaluation/coverage-review.json"
    native = json.loads((ROOT / "evaluation/native-review-decisions.json").read_text())
    if model["version"] != "0.3.1" or native["source_model_sha256"] != digest(model_path):
        raise ValueError("Reviewed native source changed")
    if policy["source_sha256"] != digest(model_path) or policy["contract_sha256"] != digest(contract_path):
        raise ValueError("Compatibility policy source binding changed")
    rels = {r["id"]: r for r in model["associations"]}
    for rid, pair in SIGNATURES.items():
        if (rels[rid]["source"], rels[rid]["target"]) != pair or rels[rid]["scope_layer"] != "FORMAL_CORE":
            raise ValueError("Reviewed relation signature changed: " + rid)
    source = next(c for c in model["constraints"] if c["id"] == "C-08")
    row = next(r for r in json.loads(contract_path.read_text())["obligation_reviews"]
               if r["engine"] == "SHACL" and r["source_element"] == "C-08")
    source_hash = hashlib.sha256(json.dumps(source, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
    if source_hash != row["source_element_sha256"]:
        raise ValueError("C-08 contract changed")
    g = Graph()
    for prefix, ns in (("cp", CP), ("co", C), ("risk", RISK), ("sh", SH)):
        g.bind(prefix, ns)
    owners = [C.Threshold]
    g.add((C.Threshold, RDF.type, SH.NodeShape)); g.add((C.Threshold, SH["class"], RISK["RKM-C070"]))
    g.add((C.Threshold, SH.nodeKind, SH.IRI))

    def prop(name, path, minimum=1, cls=None, allowed=None):
        p = C[name]; g.add((C.Threshold, SH.property, p)); g.add((p, RDF.type, SH.PropertyShape))
        if len(path) == 1: route = path[0]
        else:
            route = BNode(name + "-path"); Collection(g, route, path)
        g.add((p, SH.path, route)); g.add((p, SH.minCount, Literal(minimum)))
        g.add((p, SH.maxCount, Literal(1))); g.add((p, SH.nodeKind, SH.IRI))
        if cls: g.add((p, SH["class"], RISK[cls]))
        if allowed:
            head = BNode(name + "-allowed"); Collection(g, head, allowed); g.add((p, SH["in"], head))

    prop("Indicator", [RISK["RX-025"]], cls="RKM-C069")
    prop("Scale", [RISK["RK2-020"]], cls="RKM-C036")
    for side, anchor in (("Indicator", RISK["RX-025"]), ("Scale", RISK["RK2-020"])):
        prop(side + "Version", [anchor, CP.scaleVersion], cls="RKM-C015")
        prop(side + "VersionTarget", [anchor, CP.scaleVersion, RISK["RX-006"]], cls="RKM-C036")
        prop(side + "Dimension", [anchor, CP.dimension if side == "Indicator" else RISK["RK2-019"]], cls="RKM-C039")
        prop(side + "Kind", [anchor, CP.kind], allowed=[CP.Numeric, CP.Qualitative])
        prop(side + "Source", [anchor, CP.source])
        for field in ("unit", "scheme", "termSet"):
            prop(side + field.title(), [anchor, CP[field]], minimum=0)

    prefix = "PREFIX risk: <" + str(RISK) + ">\nPREFIX cp: <" + str(CP) + ">\n"
    anchors = "$this risk:RX-025 ?indicator ; risk:RK2-020 ?scale .\n"
    def query(name, body, message):
        owner, q = C[name], C[name + "Query"]; owners.append(owner)
        g.add((owner, RDF.type, SH.NodeShape)); g.add((owner, SH.sparql, q))
        g.add((q, RDF.type, SH.SPARQLConstraint)); g.add((q, SH.message, Literal(message)))
        g.add((q, SH.select, Literal(prefix + "SELECT DISTINCT $this WHERE {\n" + anchors + body + "\n}")))

    distinct = "FILTER EXISTS { ?a <" + str(OWL.differentFrom) + "> ?b }"
    unresolved = "FILTER NOT EXISTS { ?a <" + str(OWL.differentFrom) + "> ?b }"
    for name, left, right in (("VersionMatch", "cp:scaleVersion", "cp:scaleVersion"),
                              ("DimensionMatch", "cp:dimension", "risk:RK2-019"),
                              ("KindMatch", "cp:kind", "cp:kind")):
        body = f"?indicator {left} ?a . ?scale {right} ?b . FILTER (?a != ?b)\n"
        query(name, body + ("" if name == "KindMatch" else distinct), "Declared interpretations must agree under this exact-match policy; distinctness requires explicit evidence except for the two policy-defined kinds.")
        if name != "KindMatch": query("Unresolved" + name, body + unresolved, "Different IRIs without identity/distinctness evidence are unresolved, not proven incompatible.")
    binding = "{ ?indicator cp:scaleVersion ?v } UNION { ?scale cp:scaleVersion ?v }\n?v risk:RX-006 ?target . FILTER (?target != ?scale)\n"
    query("VersionBinding", binding + "FILTER EXISTS { ?target <" + str(OWL.differentFrom) + "> ?scale }",
          "Both declared scale versions must identify the actual threshold scale.")
    query("UnresolvedVersionBinding", binding + "FILTER NOT EXISTS { ?target <" + str(OWL.differentFrom) + "> ?scale }", "The version target cannot be equated to or distinguished from the actual scale.")
    numeric = "?indicator cp:kind cp:Numeric . ?scale cp:kind cp:Numeric .\n"
    qualitative = "?indicator cp:kind cp:Qualitative . ?scale cp:kind cp:Qualitative .\n"
    query("MissingNumericUnit", numeric + "FILTER (NOT EXISTS { ?indicator cp:unit ?a } || NOT EXISTS { ?scale cp:unit ?b })", "Numeric compatibility requires explicit canonical unit IRIs on both declarations.")
    units = numeric + "?indicator cp:unit ?a . ?scale cp:unit ?b . FILTER (?a != ?b)\n"
    query("UnitMatch", units + distinct, "Distinct unit declarations fail this exact-match policy; this is not a physical non-convertibility verdict.")
    query("UnresolvedUnitMatch", units + unresolved, "Unresolved unit mapping is not ready; no equivalence or conversion is guessed.")
    for field in ("scheme", "termSet"):
        label = field[0].upper() + field[1:]
        query("Missing" + label, qualitative + f"FILTER (NOT EXISTS {{ ?indicator cp:{field} ?a }} || NOT EXISTS {{ ?scale cp:{field} ?b }})", "Qualitative compatibility requires an explicit scheme and term-set identity.")
        body = qualitative + f"?indicator cp:{field} ?a . ?scale cp:{field} ?b . FILTER (?a != ?b)\n"
        query(label + "Match", body + distinct, "Distinct scheme/term-set declarations fail the exact-match policy.")
        query("Unresolved" + label + "Match", body + unresolved, "Scheme/term-set mapping is unresolved; labels do not settle it.")
    query("QualitativeNoUnit", "{ ?indicator cp:kind cp:Qualitative ; cp:unit ?u } UNION { ?scale cp:kind cp:Qualitative ; cp:unit ?u }", "Qualitative boundaries must not invent numeric units.")
    return g, dict(profile_version="0.6.0", source_sha256=digest(model_path), contract_sha256=digest(contract_path),
        policy_sha256=digest(POLICY), source_element="C-08", obligation_id=row["obligation_id"],
        source_element_sha256=source_hash, relation_signatures=SIGNATURES,
        target_owners=[str(o) for o in owners], native_semantics_changed=False,
        scope="Caller-selected dual-anchor declaration compatibility; not threshold-value evaluation or full risk readiness")


def main():
    g, receipt = render(); OUT.mkdir(parents=True, exist_ok=True)
    g.serialize(destination=OUT / "compatibility.ttl", format="turtle")
    receipt["shapes_sha256"] = digest(OUT / "compatibility.ttl")
    (OUT / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"profile": "0.6.0", "triples": len(g), "source_element": "C-08"}))


if __name__ == "__main__": main()
