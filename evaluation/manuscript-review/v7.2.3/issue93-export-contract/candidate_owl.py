"""Additive candidate OWL renderer derived from the frozen baseline mapping.
The original exporter and its guards remain unchanged. All inputs are supplied
by export_candidate.py after strict contract validation; no baseline graph is patched.
"""
import json,re,hashlib
REVIEWED_PROPERTY_INCLUSIONS = (("R-35", "RX-001", "C-23"), ("R-33", "RX-006", "C-24"))
VERSION_TARGETS = (("RX-014", "RKM-C002"), ("RX-015", "RKM-C035"), ("RX-016", "RKM-C036"), ("RX-013", "RKM-C072"))

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


def render(model, native, policy, contract, hashes):
    """Project only the source accepted by the independently pinned input contract."""
    BASE = contract["term_namespace"]
    ONTOLOGY_IRI = contract["ontology_iri"]
    review = {"generalization_sets": policy["retained_sets"]}
    classes = [c for c in model["concepts"] if c["scope_layer"] == "FORMAL_CORE"]
    anchors = model["imported_types"]
    relations = [r for r in model["associations"] if r["scope_layer"] == "FORMAL_CORE"]
    generals = model["generalizations"]
    if (len(classes), len(anchors), len(relations), len(generals)) != (79, 1, 130, 67):
        raise ValueError("Reviewed coverage counts changed")
    by_id = {c["id"]: c for c in classes + anchors}
    if len(by_id) != 80 or any(r[k] not in by_id for r in relations for k in ("source", "target")):
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
    if {e['id'] for e in native['elements'] if e['type'] == 'GeneralizationSet'} != {s['id'] for s in sets}:
        raise ValueError('Native set inventory differs from explicit policy')
    if len(sets) != 8 or any(s["isComplete"] for s in sets):
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
    for prop, artifact in VERSION_TARGETS:
        r = relation_by_id[prop]
        if r["target"] != "RKM-C015" or not subtype(artifact, relation_by_id["RX-006"]["target"]):
            raise ValueError(f"Incompatible version target: {prop} -> {artifact}")
    for prop, target in (("RX-025", "RKM-C069"), ("RK2-020", "RKM-C036"),
                         ("R-56", "RKM-C053"), ("R-57", "RKM-C054")):
        if relation_by_id[prop]["target"] != target:
            raise ValueError(f"Conditional constraint endpoint changed: {prop}")

    out = [
        "# Generated by the additive issue93 export contract route; not the production exporter.",
        "# OWL 2 open-world mapping; no HermiT or SHACL execution is implied.",
        f"@prefix risk: <{BASE}> .",
        "@prefix owl: <http://www.w3.org/2002/07/owl#> .",
        "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .",
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .", "",
        f"<{ONTOLOGY_IRI}> a owl:Ontology ;",
        f'  owl:versionIRI <{contract["version_iri"]}> ;',
        f"  rdfs:label {literal('Riskium candidate typed-core mapping '+model['version'])} ;",
        f"  rdfs:comment {literal('Local proxy for the external object anchor; no external ontology import closure is asserted. OWL restrictions use open-world semantics.')} ;",
        f"  risk:sourceDigest {literal(hashes["source"])} ;",
        f"  risk:nativeDigest {literal(hashes["native"])} ;",
        f"  risk:reviewDigest {literal(hashes["policy"])} .", "",
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
    out.append("risk:RE-001 owl:propertyDisjointWith risk:RE-002 . # C-26 distinct participants")
    out.append(f'<{contract["evidence_namespace"]}purpose> a owl:DatatypeProperty .')
    out.append(f'<{contract["evidence_namespace"]}context> a owl:ObjectProperty .')
    out.append("")
    for sub, sup, constraint in REVIEWED_PROPERTY_INCLUSIONS:
        out.append(f"{iri(sub)} rdfs:subPropertyOf {iri(sup)} . # {constraint}")
    out.append("")
    # C-06: a relator cannot mediate the very same individual in both roles.
    # Distinct named witnesses are still an explicit-data admission obligation.
    out.append("risk:R-56 owl:propertyDisjointWith risk:R-57 . # C-06")
    # C-08: either anchor exists in every OWL interpretation, possibly anonymously.
    out.append("risk:RKM-C070 rdfs:subClassOf [ a owl:Class ; owl:unionOf ("
               " [ a owl:Restriction ; owl:onProperty risk:RX-025 ; owl:someValuesFrom risk:RKM-C069 ]"
               " [ a owl:Restriction ; owl:onProperty risk:RK2-020 ; owl:someValuesFrom risk:RKM-C036 ]"
               " ) ] . # C-08")
    # C-25: each selected version must version an artifact of the specified kind.
    # No class disjointness or direct artifact/version join is inferred here.
    for prop, artifact in VERSION_TARGETS:
        source = relation_by_id[prop]["source"]
        out.append(f"{iri(source)} rdfs:subClassOf [ a owl:Restriction ; owl:onProperty {iri(prop)} ;"
                   f" owl:allValuesFrom [ a owl:Restriction ; owl:onProperty risk:RX-006 ;"
                   f" owl:someValuesFrom {iri(artifact)} ] ] . # C-25")
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
        "inputs_sha256": hashes,
        "input_contract_sha256": contract["_receipt_digest"],
        "version_iri": contract["version_iri"],
        "coverage": {"typed_classes": len(classes), "local_anchor_proxy": len(anchors),
                     "generalizations": len(generals), "typed_object_properties": len(relations),
                     "cardinality_restrictions": len(restrictions),
                     "reviewed_property_inclusions": len(REVIEWED_PROPERTY_INCLUSIONS),
                     "reviewed_property_disjointness": 2,
                     "evidence_context_object_properties": 1,
                     "evidence_purpose_data_properties": 1,
                     "conditional_anchor_unions": 1,
                     "qualified_version_target_rules": len(VERSION_TARGETS),
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


