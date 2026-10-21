"""Deterministic, bounded OWL 2 mapping of the reviewed Riskium typed core.

This exporter does not perform reasoning or data validation. Its three inputs are
the structured source, native OntoUML exchange and reviewed set policy.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "ontology/riskium-model.json"
NATIVE = ROOT / "ontology/native/riskium.ontouml.json"
POLICY = ROOT / "evaluation/native-review-decisions.json"
OUTPUT = ROOT / "ontology/derived/riskium.owl.ttl"
RECEIPT = ROOT / "evaluation/owl-mapping-receipt.json"
BASE = "https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#"
ONTOLOGY_IRI = "https://github.com/ArazSaieArasi3/riskium/ontologies/riskium"
REVIEWED_PROPERTY_INCLUSIONS = (("R-35", "RX-001", "C-23"), ("R-33", "RX-006", "C-24"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def literal(value):
    return json.dumps(str(value), ensure_ascii=False)


def iri(identifier):
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", identifier):
        raise ValueError(f"Unsafe source identifier: {identifier}")
    return f"risk:{identifier}"


def cardinality(value):
    m = re.fullmatch(r"(\d+)(?:\.\.(\d+|\*))?", value)
    if not m:
        raise ValueError(f"Invalid multiplicity: {value}")
    lo = int(m[1])
    hi = lo if m[2] is None else (None if m[2] == "*" else int(m[2]))
    if hi is not None and hi < lo:
        raise ValueError(f"Reversed multiplicity: {value}")
    return lo, hi


def restriction(property_iri, class_iri, multiplicity, inverse=False):
    lo, hi = cardinality(multiplicity)
    prop = f"[ owl:inverseOf {property_iri} ]" if inverse else property_iri
    predicates = [f"owl:onProperty {prop}"]
    if lo and lo == hi:
        predicates.append(f'owl:qualifiedCardinality "{lo}"^^xsd:nonNegativeInteger')
    else:
        if lo:
            predicates.append(f'owl:minQualifiedCardinality "{lo}"^^xsd:nonNegativeInteger')
        if hi is not None:
            predicates.append(f'owl:maxQualifiedCardinality "{hi}"^^xsd:nonNegativeInteger')
    if len(predicates) == 1:
        return None
    predicates.append(f"owl:onClass {class_iri}")
    return "[ a owl:Restriction ; " + " ; ".join(predicates) + " ]"


def render():
    model = json.loads(SOURCE.read_text())
    native = json.loads(NATIVE.read_text())
    review = json.loads(POLICY.read_text())
    if model["version"] != "0.3.1" or review["source_model_sha256"] != digest(SOURCE):
        raise ValueError("Source version or reviewed digest changed")
    classes = [c for c in model["concepts"] if c["scope_layer"] == "FORMAL_CORE"]
    anchors = model["imported_types"]
    relations = [r for r in model["associations"] if r["scope_layer"] == "FORMAL_CORE"]
    generals = model["generalizations"]
    if (len(classes), len(anchors), len(relations), len(generals)) != (77, 1, 127, 66):
        raise ValueError("Reviewed coverage counts changed")
    by_id = {c["id"]: c for c in classes + anchors}
    if len(by_id) != 78 or any(r[k] not in by_id for r in relations for k in ("source", "target")):
        raise ValueError("Unresolved typed class or relation endpoint")
    if any(g[k] not in by_id for g in generals for k in ("specific", "general")):
        raise ValueError("Unresolved generalization")
    general_by_id = {g["id"]: g for g in generals}
    native_by_id = {e["id"]: e for e in native["elements"]}
    if set(by_id) - set(native_by_id) or set(general_by_id) - set(native_by_id):
        raise ValueError("Structured/native identity mismatch")
    if any(native_by_id[c["id"]]["type"] != "Class" for c in classes + anchors):
        raise ValueError("Native class typing mismatch")
    for c in classes + anchors:
        n = native_by_id[c["id"]]
        if (n.get("stereotype"), n.get("isAbstract"), n.get("name", {}).get("en"),
                n.get("description", {}).get("en")) != (
                c["ontouml_stereotype"], bool(c.get("is_abstract")), c["title"], c["definition"]):
            raise ValueError(f"Native class fidelity mismatch: {c['id']}")
    if any(native_by_id[g["id"]].get("specific") != g["specific"] or
           native_by_id[g["id"]].get("general") != g["general"] for g in generals):
        raise ValueError("Native generalization direction mismatch")
    for r in relations:
        n = native_by_id.get(r["id"])
        if not n or n["type"] != "BinaryRelation" or n["properties"] != [r["id"] + ":source", r["id"] + ":target"] or n.get("name", {}).get("en") != r["predicate"] or n.get("stereotype") != r.get("stereotype"):
            raise ValueError(f"Native relation mismatch: {r['id']}")
        for end in ("source", "target"):
            p = native_by_id[n["properties"][0 if end == "source" else 1]]
            if p["propertyType"] != r[end] or p["cardinality"] != r[end + "_end_cardinality"]:
                raise ValueError(f"Native relation end mismatch: {r['id']}:{end}")
    sets = review["generalization_sets"]
    if len(sets) != 10 or any(s["isComplete"] for s in sets):
        raise ValueError("Unexpected generalization-set policy")
    for s in sets:
        n = native_by_id[s["id"]]
        if (n["type"], n["generalizations"], n["isDisjoint"], n["isComplete"]) != (
                "GeneralizationSet", s["generalizations"], s["isDisjoint"], s["isComplete"]):
            raise ValueError(f"Native set policy mismatch: {s['id']}")
        if any(general_by_id[g]["general"] != s["parent"] for g in s["generalizations"]):
            raise ValueError(f"Set parent mismatch: {s['id']}")
    if sum(bool(s["isDisjoint"]) for s in sets) != 3:
        raise ValueError("Reviewed disjointness policy changed")
    relation_by_id = {r["id"]: r for r in relations}
    if not {c["id"] for c in model["constraints"]}.issuperset(x[2] for x in REVIEWED_PROPERTY_INCLUSIONS):
        raise ValueError("Missing source constraint for reviewed property inclusion")
    # Narrower relation endpoints must fit the broader signature through the
    # declared class hierarchy. These are only the two source-backed rules.
    parents = {g["specific"]: set() for g in generals}
    for g in generals:
        parents.setdefault(g["specific"], set()).add(g["general"])
    def subtype(narrow, broad):
        pending, seen = [narrow], set()
        while pending:
            item = pending.pop()
            if item == broad:
                return True
            if item not in seen:
                seen.add(item)
                pending.extend(parents.get(item, ()))
        return False
    for sub, sup, _ in REVIEWED_PROPERTY_INCLUSIONS:
        a, b = relation_by_id[sub], relation_by_id[sup]
        if not subtype(a["source"], b["source"]) or not subtype(a["target"], b["target"]):
            raise ValueError(f"Incompatible property inclusion: {sub} -> {sup}")

    out = [
        "# Generated by tools/build_owl.py from three pinned, reviewed inputs.",
        "# OWL 2 open-world mapping; no HermiT or SHACL execution is implied.",
        f"@prefix risk: <{BASE}> .",
        "@prefix owl: <http://www.w3.org/2002/07/owl#> .",
        "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .",
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .", "",
        f"<{ONTOLOGY_IRI}> a owl:Ontology ;",
        f"  owl:versionIRI <{BASE[:-1]}> ;",
        f"  rdfs:label {literal('Riskium typed-core mapping 0.3.1')} ;",
        f"  rdfs:comment {literal('Local proxy for the external object anchor; no external ontology import closure is asserted. OWL restrictions use open-world semantics.')} ;",
        f"  risk:sourceDigest {literal(digest(SOURCE))} ;",
        f"  risk:nativeDigest {literal(digest(NATIVE))} ;",
        f"  risk:reviewDigest {literal(digest(POLICY))} .", "",
    ]
    for p in ("sourceId", "ontoumlStereotype", "isAbstractInSource", "sourceDigest",
              "nativeDigest", "reviewDigest", "sourceEndCardinality", "targetEndCardinality",
              "relationStereotype", "scopeNote"):
        out.append(f"risk:{p} a owl:AnnotationProperty .")
    out.append("")
    for c in sorted(classes + anchors, key=lambda x: x["id"]):
        bits = ["a owl:Class", f"risk:sourceId {literal(c['id'])}",
                f"rdfs:label {literal(c['title'])}",
                f"rdfs:comment {literal(c['definition'])}",
                f"risk:ontoumlStereotype {literal(c['ontouml_stereotype'])}",
                f'risk:isAbstractInSource "{str(bool(c.get("is_abstract"))).lower()}"^^xsd:boolean']
        if c["id"] == "EXT-OBJECT":
            bits.append(f"risk:scopeNote {literal('Local proxy only; externally supplied kind identities and import remain unresolved')}")
        out.extend([f"{iri(c['id'])} " + " ;\n  ".join(bits) + " .", ""])
    for g in sorted(generals, key=lambda x: x["id"]):
        out.append(f"{iri(g['specific'])} rdfs:subClassOf {iri(g['general'])} .")
    out.append("")
    restrictions = []
    for r in sorted(relations, key=lambda x: x["id"]):
        prop = iri(r["id"])
        bits = ["a owl:ObjectProperty", f"risk:sourceId {literal(r['id'])}",
                f"rdfs:label {literal(r['predicate'])}",
                f"rdfs:domain {iri(r['source'])}", f"rdfs:range {iri(r['target'])}",
                f"risk:sourceEndCardinality {literal(r['source_end_cardinality'])}",
                f"risk:targetEndCardinality {literal(r['target_end_cardinality'])}",
                f"risk:relationStereotype {literal(r.get('stereotype') or 'ordinary')}" ]
        out.extend([f"{prop} " + " ;\n  ".join(bits) + " .", ""])
        # A target-end label counts targets per source. A source-end label
        # counts sources per target, using an inverse property expression.
        forward = restriction(prop, iri(r["target"]), r["target_end_cardinality"])
        backward = restriction(prop, iri(r["source"]), r["source_end_cardinality"], True)
        if forward:
            out.append(f"{iri(r['source'])} rdfs:subClassOf {forward} .")
            restrictions.append((r["id"], "target"))
        if backward:
            out.append(f"{iri(r['target'])} rdfs:subClassOf {backward} .")
            restrictions.append((r["id"], "source"))
    out.append("")
    for sub, sup, constraint in REVIEWED_PROPERTY_INCLUSIONS:
        out.append(f"{iri(sub)} rdfs:subPropertyOf {iri(sup)} . # {constraint}")
    out.append("")
    for s in sorted(sets, key=lambda x: x["id"]):
        if s["isDisjoint"]:
            children = [iri(general_by_id[g]["specific"]) for g in s["generalizations"]]
            out.append("[] a owl:AllDisjointClasses ; owl:members ( " + " ".join(children) + " ) .")
    out.append("")
    rendered = "\n".join(out)
    receipt = {
        "status": "MAPPING_GENERATED_AND_STRUCTURALLY_CHECKED_NOT_REASONED",
        "model_version": model["version"], "namespace": BASE,
        "inputs_sha256": {str(p.relative_to(ROOT)): digest(p) for p in (SOURCE, NATIVE, POLICY)},
        "coverage": {"typed_classes": len(classes), "local_anchor_proxy": len(anchors),
                     "generalizations": len(generals), "typed_object_properties": len(relations),
                     "cardinality_restrictions": len(restrictions),
                     "reviewed_property_inclusions": len(REVIEWED_PROPERTY_INCLUSIONS),
                     "reviewed_generalization_sets": len(sets), "disjoint_sets": 3,
                     "optional_boundaries_as_classes": 0},
        "limitations": ["No external owl:imports: external object anchor is a local proxy.",
                        "No covering axiom, unique-name assumption, key, global equivalence or implicit sibling disjointness.",
                        "Qualified cardinalities constrain OWL interpretations under an open world; missing values can be anonymous and excessive named values can be equal.",
                        "Temporal, version-join, provenance, calculation and application-admission rules require separately reviewed encodings.",
                        "Syntax, reasoning, satisfiability, instance validity and semantic adequacy are distinct checks."],
        "output_sha256": hashlib.sha256(rendered.encode()).hexdigest(),
    }
    return rendered, receipt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="Fail if generated outputs differ")
    args = ap.parse_args()
    output, receipt = render()
    receipt_text = json.dumps(receipt, indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if OUTPUT.read_text() != output or RECEIPT.read_text() != receipt_text:
            raise SystemExit("OWL export or receipt is stale")
    else:
        OUTPUT.write_text(output)
        RECEIPT.write_text(receipt_text)
    print(json.dumps(receipt["coverage"], sort_keys=True))


if __name__ == "__main__":
    main()
