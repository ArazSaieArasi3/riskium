"""Selected treatment/policy source contracts; not operational evaluation."""
RELATIONS = {
    "R-19": ("RKM-C041", "RKM-X01", "1"),
    "R-20": ("RKM-C041", "RKM-C042", "1"),
    "R-21": ("RKM-C043", "RKM-X01", "1..*"),
    "R-60": ("RKM-C023", "RKM-C041", "0..*"),
    "R-61": ("RKM-C023", "RKM-C043", "0..*"),
    "R-62": ("RKM-C043", "RKM-C046", "1"),
    "R-63": ("RKM-C041", "RKM-C043", "0..*"),
    "R-64": ("RKM-C044", "RKM-C043", "0..*"),
    "RX-003": ("RKM-X01", "RKM-X02", "1..*"),
    "RX-017": ("RKM-C072", "RKM-C002", "1..*"),
    "RX-018": ("RKM-C072", "RKM-C073", "0..*"),
    "RX-019": ("RKM-C072", "RKM-C074", "0..*"),
    "RX-020": ("RKM-X05", "RKM-C045", "0..1"),
    "RK2-011": ("RKM-C002", "RKM-X02", "0..*"),
    "RK2-014": ("RKM-C041", "RKM-X04", "0..*"),
    "RK2-015": ("RKM-C041", "RKM-C032", "0..*"),
    "RK2-016": ("RKM-C023", "RKM-X05", "0..*"),
    "RK2-022": ("RKM-C033", "RKM-X05", "0..*"),
    "RK2-023": ("RKM-C073", "RKM-C002", "1..*"),
    "RK2-024": ("RKM-C074", "RKM-C002", "1..*"),
}
CONSTRAINTS = {"C-01", "C-02", "C-03", "C-04", "C-05", "C-07", "C-10", "C-11", "C-14", "C-16", "C-17", "C-18", "C-19", "C-25"}
DOCUMENTARY_IDS = ["RKM-C041", "RKM-C042", "RKM-C043", "RKM-C046", "RKM-C072", "RKM-C073", "RKM-C074", "RKM-X02", "RKM-X05"]


def extract(model, context):
    concepts = {c["id"]: c for c in model["concepts"]}
    return {
        "status": "SELECTED_STATIC_SOURCE_CONTRACTS_NOT_INSTANCE_OR_ENGINE_RESULTS",
        "relations": {e["id"]: {k: e[k] for k in ("id", "source", "target", "predicate", "source_end_cardinality", "target_end_cardinality")}
                      for e in model["associations"] if e["id"] in RELATIONS},
        "constraints": {c["id"]: c for c in model["constraints"] if c["id"] in CONSTRAINTS},
        "identity": {cid: {k: concepts[cid][k] for k in ("id", "ontouml_stereotype", "identity_supplier", "scope_layer")}
                     for cid in DOCUMENTARY_IDS + ["RKM-C044", "RKM-C045"]},
        "treatment_activity_ancestors": context.lineage(model, "RKM-C044")[0],
        "case_application_policy": model["case_application_profile_policy"],
    }


def check(facts):
    if set(facts["relations"]) != set(RELATIONS) or set(facts["constraints"]) != CONSTRAINTS:
        raise ValueError("treatment/policy contract coverage")
    for rid, expected in RELATIONS.items():
        edge = facts["relations"][rid]
        if (edge["source"], edge["target"], edge["target_end_cardinality"]) != expected:
            raise ValueError("treatment/policy relation contract: " + rid)
    for cid in DOCUMENTARY_IDS:
        if facts["identity"][cid]["identity_supplier"] != "RKM-C014":
            raise ValueError("documentary identity: " + cid)
    if facts["identity"]["RKM-C044"]["ontouml_stereotype"] != "event" or "RKM-C014" in facts["treatment_activity_ancestors"]:
        raise ValueError("treatment activity/document distinction")
    boundary = facts["identity"]["RKM-C045"]
    if boundary["scope_layer"] != "OPTIONAL_PHENOMENON_BOUNDARY" or boundary["ontouml_stereotype"] is not None:
        raise ValueError("heterogeneous control boundary")
