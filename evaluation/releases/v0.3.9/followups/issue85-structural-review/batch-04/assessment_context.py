"""Selected assessment source contracts; static checks, not instance evaluation."""
RELATIONS = {
    "R-11": ("RKM-C032", "RKM-X01", "1"),
    "R-12": ("RKM-C032", "RKM-C033", "1"),
    "R-13": ("RKM-C032", "RKM-C034", "0..*"),
    "R-14": ("RKM-C034", "RKM-C036", "0..1"),
    "R-15": ("RKM-C034", "RKM-C038", "0..1"),
    "R-16": ("RKM-C038", "RKM-C036", "1"),
    "R-17": ("RKM-C032", "RKM-C037", "0..*"),
    "R-18": ("RKM-C037", "RKM-C034", "0..*"),
    "R-26": ("RKM-C031", "RKM-C032", "0..*"),
    "R-45": ("RKM-C032", "RKM-C002", "0..1"),
    "R-46": ("RKM-C032", "RKM-C035", "0..1"),
    "R-47": ("RKM-C032", "RKM-C040", "0..1"),
    "R-48": ("RKM-C034", "RKM-C039", "1"),
    "R-49": ("RKM-C035", "RKM-C036", "0..*"),
    "R-50": ("RKM-C037", "RKM-C035", "1"),
    "RX-004": ("RKM-X03", "RKM-X01", "1"),
    "RX-011": ("RKM-X04", "RKM-X01", "1"),
    "RX-012": ("RKM-X04", "RKM-C032", "1..*"),
    "RX-013": ("RKM-X04", "RKM-C015", "1"),
    "RX-014": ("RKM-C032", "RKM-C015", "1"),
    "RX-015": ("RKM-C032", "RKM-C015", "0..1"),
    "RX-016": ("RKM-C034", "RKM-C015", "0..1"),
    "RK2-012": ("RKM-X03", "RKM-C002", "0..1"),
    "RK2-013": ("RKM-C032", "RKM-X03", "0..*"),
    "RK2-018": ("RKM-C035", "RKM-C039", "0..*"),
    "RK2-019": ("RKM-C036", "RKM-C039", "1"),
    "RK2-022": ("RKM-C033", "RKM-X05", "0..*"),
}
CONSTRAINTS = {"C-01", "C-02", "C-03", "C-04", "C-05", "C-11", "C-13", "C-16", "C-17", "C-18", "C-21", "C-25"}
DOCUMENTARY_IDS = ["RKM-C032", "RKM-C033", "RKM-C034", "RKM-C035", "RKM-C036", "RKM-C037", "RKM-C038", "RKM-C039", "RKM-C040", "RKM-X03", "RKM-X04"]


def extract(model, context):
    concepts = {c["id"]: c for c in model["concepts"]}
    return {
        "status": "SELECTED_STATIC_SOURCE_CONTRACTS_NOT_INSTANCE_OR_ENGINE_RESULTS",
        "relations": {e["id"]: {k: e[k] for k in ("id", "source", "target", "predicate", "source_end_cardinality", "target_end_cardinality")}
                      for e in model["associations"] if e["id"] in RELATIONS},
        "constraints": {c["id"]: c for c in model["constraints"] if c["id"] in CONSTRAINTS},
        "identity": {cid: {k: concepts[cid][k] for k in ("id", "ontouml_stereotype", "identity_supplier")}
                     for cid in DOCUMENTARY_IDS + ["RKM-C031", "RKM-C015"]},
        "assessment_activity_ancestors": context.lineage(model, "RKM-C031")[0],
        "case_application_policy": model["case_application_profile_policy"],
    }


def check(facts):
    if set(facts["relations"]) != set(RELATIONS) or set(facts["constraints"]) != CONSTRAINTS:
        raise ValueError("assessment contract coverage")
    for rid, expected in RELATIONS.items():
        edge = facts["relations"][rid]
        if (edge["source"], edge["target"], edge["target_end_cardinality"]) != expected:
            raise ValueError("assessment relation contract: " + rid)
    for cid in DOCUMENTARY_IDS:
        if facts["identity"][cid]["identity_supplier"] != "RKM-C014":
            raise ValueError("documentary identity: " + cid)
    if facts["identity"]["RKM-C031"]["ontouml_stereotype"] != "event" or "RKM-C014" in facts["assessment_activity_ancestors"]:
        raise ValueError("assessment activity/document distinction")
    if facts["identity"]["RKM-C015"]["identity_supplier"] != "RKM-C015":
        raise ValueError("artifact version identity")
