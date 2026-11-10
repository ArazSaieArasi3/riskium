"""Deterministic source-context extraction, not an ontology reasoner.

Used by the bounded N3b documentary reviews. Preserve source data verbatim and
expose ancestor/neighbor changes that an unchanged local edge would conceal.
"""
import hashlib
import json


def digest(value):
    body = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(body).hexdigest()


def local_edges(model, cid):
    return {key: sorted([edge for edge in model[key] if cid in
            [edge.get("source"), edge.get("target"), edge.get("specific"), edge.get("general")]],
            key=lambda edge: edge["id"]) for key in ("associations", "generalizations")}


def lineage(model, cid):
    parents = {}
    for edge in model["generalizations"]:
        parents.setdefault(edge["specific"], []).append(edge)
    visited, active, edges = set(), set(), {}

    def visit(node):
        if node in active:
            raise ValueError("inheritance cycle: " + node)
        if node in visited:
            return
        active.add(node)
        for edge in parents.get(node, []):
            edges[edge["id"]] = edge
            visit(edge["general"])
        active.remove(node)
        visited.add(node)

    visit(cid)
    return sorted(visited - {cid}), [edges[key] for key in sorted(edges)]


def extract(old, current, cid):
    before = {c["id"]: c for c in old["concepts"]}
    now = {c["id"]: c for c in current["concepts"]}
    ancestors, ancestor_edges = lineage(current, cid)
    old_ancestors, old_ancestor_edges = lineage(old, cid)
    old_local, current_local = local_edges(old, cid), local_edges(current, cid)
    neighbors = sorted({edge[side] for edge in current_local["associations"]
                        for side in ("source", "target")} - {cid})

    def changes(ids):
        return [{"id": node, "changed_fields": sorted(key for key in set(before.get(node, {})) | set(now[node])
                 if before.get(node, {}).get(key) != now[node].get(key)),
                 "old_record_sha256": digest(before[node]) if node in before else None,
                 "current_record_sha256": digest(now[node])}
                for node in ids if before.get(node) != now[node]]

    scope = set(ancestors) | {cid}
    policy = current["generalization_set_policy"]
    retained = [s for s in policy["retained_sets"] if s["parent"] in scope]
    excluded = [s for s in policy["excluded_sets"] if s["parent"] in scope]
    return {
        "concept_id": cid,
        "old_concept_sha256": digest(before[cid]),
        "current_concept_sha256": digest(now[cid]),
        "concept_record_unchanged": before[cid] == now[cid],
        "local_edges_unchanged": old_local == current_local,
        "local_edges_sha256": digest(current_local),
        "direct_association_ids": [edge["id"] for edge in current_local["associations"]],
        "ancestor_ids": ancestors,
        "ancestor_edges": [{k: edge[k] for k in ("id", "specific", "general")} for edge in ancestor_edges],
        "ancestor_edges_sha256": digest(ancestor_edges),
        "ancestor_edges_unchanged": ancestors == old_ancestors and ancestor_edges == old_ancestor_edges,
        "changed_ancestors": changes(ancestors),
        "association_neighbor_ids": neighbors,
        "changed_association_neighbors": changes(neighbors),
        "old_explicit_set_policy_present": "generalization_set_policy" in old,
        "current_set_policy_sha256": digest(policy),
        "applicable_retained_sets": retained,
        "applicable_excluded_sets": excluded,
        "case_application_policy_sha256": digest(current["case_application_profile_policy"]),
        "case_identity_policy": current["case_application_profile_policy"]["case_identity"],
        "constraint_refs": [c["id"] for c in current["constraints"] if c["id"] in ("C-01", "C-11", "C-16")],
        "method_boundary": "Source/graph inventory only; not inferred class satisfiability or independent semantic acceptance."
    }
