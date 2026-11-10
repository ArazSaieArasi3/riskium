"""Selected evidence/monitoring source contracts; no inference or instance tests."""
RELATIONS = {
    "R-68": ("RKM-C065", "RKM-C014", "1..*"),
    "R-69": ("RKM-C065", "RKM-C004", "0..*"),
    "R-70": ("RKM-C065", "RKM-C047", "0..*"),
    "R-71": ("RKM-C065", "RKM-C031", "0..*"),
    "R-72": ("RKM-C065", "RKM-C044", "0..*"),
    "RX-021": ("RKM-C065", "RKM-C066", "1"),
    "RX-022": ("RKM-C067", "RKM-C068", "0..*"),
    "RX-023": ("RKM-C068", "RKM-C069", "1"),
    "RX-024": ("RKM-C068", "RKM-X01", "1"),
    "RX-025": ("RKM-C070", "RKM-C069", "0..1"),
    "RX-026": ("RKM-C071", "RKM-C068", "1..*"),
    "RX-027": ("RKM-C071", "RKM-C070", "0..*"),
    "RX-028": ("RKM-C071", "RKM-X01", "0..*"),
    "RK2-017": ("RKM-C023", "RKM-C068", "0..*"),
    "RK2-020": ("RKM-C070", "RKM-C036", "0..1"),
    "RK2-026": ("RKM-C068", "RKM-C002", "0..1"),
    "RE-001": ("RKM-C075", "RKM-C066", "1"),
    "RE-002": ("RKM-C075", "RKM-C076", "1"),
    "RE-003": ("RKM-C075", "RKM-C014", "1"),
}
CONSTRAINTS = {"C-01", "C-02", "C-03", "C-04", "C-05", "C-08", "C-11", "C-12", "C-13", "C-16", "C-17", "C-18", "C-26"}
DOCUMENTARY_IDS = ["RKM-C065", "RKM-C068", "RKM-C069", "RKM-C070", "RKM-C071"]


def extract(old, model, context):
    concepts = {c["id"]: c for c in model["concepts"]}
    before, after = context.local_edges(old, "RKM-C065"), context.local_edges(model, "RKM-C065")
    def changes(key):
        a, b = {e["id"]: e for e in before[key]}, {e["id"]: e for e in after[key]}
        return [{"id": rid, "old": a.get(rid), "current": b.get(rid)}
                for rid in sorted(set(a) | set(b)) if a.get(rid) != b.get(rid)]
    return {
        "status": "SELECTED_STATIC_SOURCE_CONTRACTS_NOT_INSTANCE_OR_ENGINE_RESULTS",
        "relations": {e["id"]: {k: e[k] for k in ("id", "source", "target", "predicate", "source_end_cardinality", "target_end_cardinality")}
                      for e in model["associations"] if e["id"] in RELATIONS},
        "constraints": {c["id"]: c for c in model["constraints"] if c["id"] in CONSTRAINTS},
        "identity": {cid: {k: concepts[cid][k] for k in ("id", "ontouml_stereotype", "identity_supplier", "verification_status")}
                     for cid in DOCUMENTARY_IDS + ["RKM-C066", "RKM-C067", "RKM-C075", "RKM-C076"]},
        "reference_local_edge_delta": {key: changes(key) for key in ("associations", "generalizations")},
        "reference_role_ancestors": context.lineage(model, "RKM-C076")[0],
        "observation_activity_ancestors": context.lineage(model, "RKM-C067")[0],
        "case_application_policy": model["case_application_profile_policy"],
    }


def check(facts):
    if set(facts["relations"]) != set(RELATIONS) or set(facts["constraints"]) != CONSTRAINTS:
        raise ValueError("evidence/monitoring contract coverage")
    for rid, expected in RELATIONS.items():
        edge = facts["relations"][rid]
        if (edge["source"], edge["target"], edge["target_end_cardinality"]) != expected:
            raise ValueError("evidence/monitoring relation contract: " + rid)
    for cid in DOCUMENTARY_IDS + ["RKM-C066", "RKM-C076"]:
        if facts["identity"][cid]["identity_supplier"] != "RKM-C014":
            raise ValueError("documentary bearer identity: " + cid)
    if facts["identity"]["RKM-C067"]["ontouml_stereotype"] != "event" or "RKM-C014" in facts["observation_activity_ancestors"]:
        raise ValueError("observation activity/result distinction")
    if facts["identity"]["RKM-C075"]["ontouml_stereotype"] != "relator" or facts["identity"]["RKM-C076"]["ontouml_stereotype"] != "role":
        raise ValueError("evidential-use relationship/participation")
    delta = facts["reference_local_edge_delta"]
    if delta["associations"] or len(delta["generalizations"]) != 1:
        raise ValueError("reference edge delta")
    change = delta["generalizations"][0]
    edge = change["current"]
    if change["id"] != "GE-001" or change["old"] is not None or (edge["specific"], edge["general"], edge["status"]) != ("RKM-C076", "RKM-C065", "ISOLATED_CANDIDATE"):
        raise ValueError("reference role specialization")
    if "RKM-C065" not in facts["reference_role_ancestors"]:
        raise ValueError("reference role ancestry")
