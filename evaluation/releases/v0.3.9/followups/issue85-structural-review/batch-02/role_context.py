"""Selected responsibility source checks; no ontology engine or instance data."""
IDENTITY_PROVIDERS = {"kind", "collective", "quantity", "quality", "mode", "relator"}
SORTALS = IDENTITY_PROVIDERS | {"subkind", "role", "phase"}


def extract(model, old, selected, context):
    current = {c["id"]: c for c in model["concepts"]}
    before = {c["id"]: c for c in old["concepts"]}
    ancestor_map = {cid: context.lineage(model, cid)[0] for cid in current}
    rows = {}
    for cid in selected:
        c = current[cid]
        ancestry = set(ancestor_map[cid])
        providers = sorted(a for a in ancestry if current[a]["ontouml_stereotype"] in IDENTITY_PROVIDERS)
        descendant_providers = set()
        for other in current:
            if cid in ancestor_map[other]:
                descendant_providers.update(a for a in ancestor_map[other]
                                           if current[a]["ontouml_stereotype"] in IDENTITY_PROVIDERS)
                if current[other]["ontouml_stereotype"] in IDENTITY_PROVIDERS:
                    descendant_providers.add(other)
        dependencies = []
        for edge in model["associations"]:
            if edge["stereotype"] == "mediation" and edge["target"] in ancestry | {cid}:
                dependencies.append({k: edge[k] for k in ("id", "source", "target", "source_end_cardinality", "target_end_cardinality")})
        adjacent = {edge[side] for edge in context.local_edges(model, cid)["generalizations"]
                    for side in ("specific", "general")} - {cid}
        changed = [{"id": other, "changed_fields": sorted(k for k in set(before.get(other, {})) | set(current[other])
                    if before.get(other, {}).get(k) != current[other].get(k))}
                   for other in sorted(adjacent) if before.get(other) != current[other]]
        rows[cid] = {
            "stereotype": c["ontouml_stereotype"], "is_abstract": c["is_abstract"],
            "declared_identity_supplier": c["identity_supplier"],
            "ancestor_identity_providers": providers,
            "ancestor_sortals": sorted(a for a in ancestry if current[a]["ontouml_stereotype"] in SORTALS),
            "descendant_identity_providers": sorted(descendant_providers),
            "inherited_mediations": sorted(dependencies, key=lambda d: d["id"]),
            "changed_generalization_endpoints": changed,
        }
    edges = {e["id"]: {k: e[k] for k in ("id", "source", "target", "predicate", "source_end_cardinality", "target_end_cardinality")}
             for e in model["associations"] if e["id"] in ("R-53", "R-55", "R-56", "R-57")}
    return {"status": "SELECTED_STATIC_SOURCE_CHECKS_NOT_INSTANCE_OR_ENGINE_RESULTS",
            "concepts": rows, "selected_relations": edges,
            "set_policy_sha256": context.digest(model["generalization_set_policy"])}


def check(profile):
    """Check this declared D07 slice against its stated identity/dependency contract."""
    rows = profile["concepts"]
    wanted = {"RKM-C050": "RKM-C014", "RKM-C051": "RKM-C014", "RKM-C059": "RKM-C014",
              "RKM-C055": "RKM-C048", "RKM-C057": "RKM-C048",
              "RKM-C056": "RKM-C049", "RKM-C058": "RKM-C049"}
    for cid, provider in wanted.items():
        if rows[cid]["ancestor_identity_providers"] != [provider] or rows[cid]["declared_identity_supplier"] != provider:
            raise ValueError("responsibility identity contract: " + cid)
    for cid in ("RKM-C047", "RKM-C053", "RKM-C054"):
        r = rows[cid]
        if not r["is_abstract"] or r["ancestor_sortals"] or r["declared_identity_supplier"] is not None:
            raise ValueError("non-sortal identity contract: " + cid)
        if r["descendant_identity_providers"] != ["RKM-C048", "RKM-C049"]:
            raise ValueError("heterogeneous bearer context: " + cid)
    for cid in ("RKM-C053", "RKM-C054", "RKM-C055", "RKM-C056", "RKM-C057", "RKM-C058"):
        r = rows[cid]
        if len(r["inherited_mediations"]) != 1 or r["inherited_mediations"][0]["source_end_cardinality"] != "1..*":
            raise ValueError("mandatory responsibility dependency: " + cid)
    if profile["selected_relations"]["R-53"]["target_end_cardinality"] != "0..1":
        raise ValueError("actor resolution boundary")
    if profile["selected_relations"]["R-55"]["target_end_cardinality"] != "0..1":
        raise ValueError("assignment statement/actual mandate boundary")
