"""Selected registration/workflow source contracts; not executable workflow tests."""
RELATIONS = {
    "R-01": ("RKM-C022", "RKM-X01", "1"),
    "R-33": ("RKM-C023", "RKM-C022", "1"),
    "RX-008": ("RKM-C022", "RKM-C030", "1"),
    "RX-010": ("RKM-C025", "RKM-C010", "0..1"),
    "R-23": ("RKM-C023", "RKM-C062", "0..*"),
    "R-31": ("RKM-C062", "RKM-C060", "0..1"),
    "R-32": ("RKM-C062", "RKM-C061", "0..1"),
    "RX-029": ("RKM-C064", "RKM-C061", "1"),
    "RX-030": ("RKM-C064", "RKM-C063", "1"),
    "RX-031": ("RKM-C064", "RKM-C023", "1"),
    "RX-032": ("RKM-C062", "RKM-C064", "0..1"),
}
CONSTRAINTS = {"C-01", "C-02", "C-03", "C-05", "C-09", "C-11", "C-16", "C-17", "C-19", "C-24"}


def extract(model, context):
    concepts = {c["id"]: c for c in model["concepts"]}
    return {
        "status": "SELECTED_STATIC_SOURCE_CONTRACTS_NOT_INSTANCE_OR_ENGINE_RESULTS",
        "relations": {e["id"]: {k: e[k] for k in ("id", "source", "target", "predicate", "source_end_cardinality", "target_end_cardinality")}
                      for e in model["associations"] if e["id"] in RELATIONS},
        "constraints": {c["id"]: c for c in model["constraints"] if c["id"] in CONSTRAINTS},
        "identity": {cid: {k: concepts[cid][k] for k in ("id", "ontouml_stereotype", "identity_supplier")}
                     for cid in ("RKM-C022", "RKM-C023", "RKM-C030", "RKM-C062", "RKM-C064")},
        "workflow_assignment_ancestors": context.lineage(model, "RKM-C064")[0],
        "case_application_policy": model["case_application_profile_policy"],
    }


def check(facts):
    if set(facts["relations"]) != set(RELATIONS) or set(facts["constraints"]) != CONSTRAINTS:
        raise ValueError("registration contract coverage")
    for rid, expected in RELATIONS.items():
        edge = facts["relations"][rid]
        if (edge["source"], edge["target"], edge["target_end_cardinality"]) != expected:
            raise ValueError("registration relation contract: " + rid)
    if facts["relations"]["R-01"]["source_end_cardinality"] != "0..*":
        raise ValueError("case need not have a register entry")
    for cid in ("RKM-C022", "RKM-C030", "RKM-C062"):
        if facts["identity"][cid]["identity_supplier"] != "RKM-C014":
            raise ValueError("documentary identity: " + cid)
    if facts["identity"]["RKM-C023"]["identity_supplier"] != "RKM-C015":
        raise ValueError("entry revision identity")
    if facts["identity"]["RKM-C064"]["ontouml_stereotype"] != "situation" or "RKM-C014" in facts["workflow_assignment_ancestors"]:
        raise ValueError("workflow situation/document distinction")
