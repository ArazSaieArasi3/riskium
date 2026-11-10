#!/usr/bin/env python3
"""Qualify and render a declared N3b documentary batch; no scientific edits."""
import sys
sys.dont_write_bytecode = True
import argparse
import collections
import copy
import csv
import hashlib
import io
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import context
import evidence_monitoring_context

HERE = Path(__file__).resolve().parent.parent
ROOT = HERE.parents[4]
BASE_INPUTS = ["ontology/riskium-model.json", "ontology/0.3.2/riskium-model.json",
    "references/concept-definitions/0.1.0/review.json",
    "evaluation/releases/v0.3.9/followups/issue85-impact/impact.json",
    "evaluation/releases/v0.3.9/followups/issue85-reuse-review/remaining-batches.json"]


def sha(body):
    return hashlib.sha256(body).hexdigest()


def load(path):
    return json.loads(path.read_text())


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def validate(review, folder, override=None, evidence_override=None):
    local = [str((folder / name).relative_to(ROOT)) for name in
             ("source-access.json", "passage-checks.json", "contexts.json", "evidence-monitoring-checks.json")]
    paths = BASE_INPUTS + review["prior_packets"] + local
    need(set(review["inputs"]) == set(paths), "input coverage")
    for path, digest in review["inputs"].items():
        need(sha((ROOT / path).read_bytes()) == digest, "stale source input: " + path)
    old, current, previous, impact, allocation = [load(ROOT / p) for p in BASE_INPUTS]
    declarations = {b["execution"]: b for b in allocation["batches"]}
    declared = declarations[review["execution"]]
    ids = set(declared["concept_ids"])
    rows = review["concepts"]
    need(len(rows) == len(ids) and {r["concept_id"] for r in rows} == ids, "declared batch coverage")
    prior_rows = [r for path in review["prior_packets"] for r in load(ROOT / path)["concepts"]]
    earlier = {r["concept_id"] for r in prior_rows}
    need(len(earlier) == len(prior_rows) and not earlier & ids, "duplicate accepted population")
    now = {c["id"]: c for c in current["concepts"]}
    prior = {r["concept_id"]: r for r in previous["concepts"]}
    effects = {r["id"]: r for r in impact["rows"]}
    remaining = set(now) - earlier - ids
    need(len(now) == 82 and earlier | ids | remaining == set(now), "catalog population")
    contexts = override if override is not None else load(folder / "contexts.json")
    expected = {cid: context.extract(old, current, cid) for cid in declared["concept_ids"]}
    need(contexts == expected, "structural context mismatch")
    contracts = evidence_override if evidence_override is not None else load(folder / "evidence-monitoring-checks.json")
    need(contracts == evidence_monitoring_context.extract(old, current, context), "evidence/monitoring context mismatch")
    evidence_monitoring_context.check(contracts)
    access, passages = load(folder / "source-access.json"), load(folder / "passage-checks.json")
    term_ids = {tid for r in rows for tid in r["comparison_term_ids"]}
    need(term_ids == set(review["terms"]) == set(passages), "term/passage coverage")
    source_ids = {t["source_id"] for t in review["terms"].values()}
    need(source_ids == set(review["sources"]) == set(access), "source coverage")
    for sid, source in review["sources"].items():
        for field in ("url", "document_sha256", "accessed", "direct_access", "same_response_as_prior"):
            need(source[field] == access[sid][field], "source access binding")
        need(source["version"] == previous["sources"][sid]["version"] and source["inspection_scope"], "source edition status")
        need(source["direct_access"] == "SUCCESS" and source["same_response_as_prior"] is True, "source inspection")
        need(source["document_sha256"] == previous["sources"][sid]["document_sha256"], "source edition/body change needs review")
    for tid, term in review["terms"].items():
        source, passage = review["sources"][term["source_id"]], passages[tid]
        need(term["url"].startswith(source["url"]) and term["locator"] == previous["terms"][tid]["locator"], "source locator/attribution")
        need(passage["source_document_sha256"] == source["document_sha256"] and passage["url"] == term["url"]
             and passage["locator"] == term["locator"] and len(passage["selected_text_sha256"]) == 64, "selected passage binding")
        expected_kinds = {"derivation": "PROVENANCE_CLASS", "result": "SOSA_RESULT_CLASS",
            "metric": "DATASET_QUALITY_PATTERN_CLASS", "observable": "OBSERVABLE_PROPERTY_CLASS"}
        need(term["target_kind"] == expected_kinds[tid], "source term kind")
    for row in rows:
        cid = row["concept_id"]
        concept, pr, facts = now[cid], prior[cid], contexts[cid]
        need(row["impact_category"] == effects[cid]["category"] == "STRUCTURAL_CONTEXT_RECHECK", "impact category")
        need(row["source_concept_sha256"] == context.digest(concept), "concept binding")
        need(row["authored_definition"] == concept["definition"] and row["authored_definition_sha256"] == sha(concept["definition"].encode()), "authored definition")
        need(row["previous_review_sha256"] == context.digest(pr), "historical review binding")
        need(row["context_sha256"] == context.digest(facts), "review/context binding")
        need(set(row["constraint_ids"]) <= set(contracts["constraints"]) and row["constraint_ids"], "constraint route")
        guards = row["evidence_monitoring_guards"]
        need(set(guards) == {"citation_proves_claim_truth", "reference_pointer_proves_grounded_use", "signal_proves_occurrence",
             "indicator_specification_is_reported_value", "threshold_requires_both_anchors", "qualitative_boundary_requires_invented_numeric_unit"}
             and all(value is False for value in guards.values()), "unsupported evidence/monitoring inference")
        need(row["title"] == concept["display_title"] and row["subdomain_id"] == concept["domain_id"]
             and concept["domain_id"] in declared["subdomain_ids"], "concept identity")
        need(row["previous_disposition"] == pr["disposition"] and row["disposition"] in
             ("RELATED", "ANALOGY", "CONTRAST", "NO_DIRECT_EQUIVALENT_REVIEWED"), "documentary disposition")
        need(row["comparison_term_ids"] == pr["term_ids"] and row["followup_issues"] == pr["followup_issues"], "prior route preserved")
        need(row["rationale"] and row["context_interpretation"] and row["accepted_as_documentary_decision"] is True, "missing documentary judgment")
        guards = row["interpretation_guards"]
        need(set(guards) == {"sibling_exclusivity_inferred_from_parenthood", "exhaustive_coverage_inferred_from_parenthood",
             "register_acceptance_required_for_riskcase_existence", "retained_set_semantic_approval_inferred"}
             and all(value is False for value in guards.values()), "unsupported policy inference")
        need(row["formal_alignment"] == "UNASSESSED" and row["independent_validation"] == "NOT_PERFORMED", "unsupported semantic acceptance")
    summary = {"this_batch": len(ids), "prior_documentary_dispositions": len(earlier),
        "cumulative_documentary_dispositions": len(earlier | ids), "population": 82, "remaining": len(remaining),
        "dispositions": dict(collections.Counter(r["disposition"] for r in rows)),
        "disposition_labels_changed": sum(r["disposition"] != r["previous_disposition"] for r in rows),
        "unchanged_local_edges": sum(c["local_edges_unchanged"] for c in contexts.values()),
        "changed_ancestor_context": sum(bool(c["changed_ancestors"]) for c in contexts.values()),
        "changed_association_neighbor_context": sum(bool(c["changed_association_neighbors"]) for c in contexts.values())}
    need(review["summary"] == summary, "summary mismatch")
    need(review["status"] == "BOUNDED_BATCH_COMPLETE_FULL_CURATION_PENDING" and review["model_version"] == "0.3.2", "scope status")
    need(all(review["boundaries"][key] is False for key in ("scientific_source_modified", "historical_curation_modified",
         "published", "formal_alignment_axioms_added")) and review["boundaries"]["engine_runs"] == 0
         and review["boundaries"]["independent_validation"] == "NOT_PERFORMED", "premature claim")
    return now, contexts, allocation, earlier, remaining


def render(review, folder):
    concepts, contexts, allocation, earlier, remaining = validate(review, folder)
    base = "https://github.com/ArazSaieArasi3/riskium/blob/" + review["baseline_commit"] + "/"
    output = {}
    for row in review["concepts"]:
        cid = row["concept_id"]
        c, facts = concepts[cid], contexts[cid]
        lines = [f"# {row['title']} — {review['execution']} documentary preview", "", "**Planning preview; not deployed or independently validated.**", "", "## Authored definition, unchanged", "", row["authored_definition"], "", f"[Source model 0.3.2]({base}ontology/0.3.2/riskium-model.json); subdomain {row['subdomain_id']}; stereotype {c['ontouml_stereotype']}; identity supplier {c['identity_supplier']}.", "", "Identity basis: " + c["identity_basis"], "", "Authored verification status, preserved verbatim: " + c["verification_status"], "", "Later bounded qualification/publication evidence is in the [v0.3.9 receipt](" + base + "evaluation/releases/v0.3.9/R2b-outcome.md). Source labels and documentary comparisons are not independent semantic ratings.", "", "## Documentary comparison", "", f"**{row['previous_disposition']} → {row['disposition']}**.", "", row["rationale"], "", "| Selected term | Source kind and locator |", "|---|---|"]
        for tid in row["comparison_term_ids"]:
            term = review["terms"][tid]
            lines.append(f"| [{term['name']}]({term['url']}) | {term['target_kind']}; {term['locator']} |")
        lines += ["", "## Current structural context", "", row["context_interpretation"], "", f"Source continuity: concept record unchanged={facts['concept_record_unchanged']}; local association/generalization records unchanged={facts['local_edges_unchanged']}; inherited edges unchanged={facts['ancestor_edges_unchanged']}. Ancestor and neighbor changes are reported separately.", "", "| Observation | Source-bound result |", "|---|---|"]
        lines.append("| Inheritance path | " + "; ".join(f"{e['id']}: {e['specific']} → {e['general']}" for e in facts["ancestor_edges"]) + " |")
        lines.append("| Source constraint route | " + ", ".join(row["constraint_ids"]) + " — [selected source statements](../evidence-monitoring-checks.json) |")
        for field, label in (("changed_ancestors", "Changed ancestor"), ("changed_association_neighbors", "Changed relation neighbor")):
            values = facts[field]
            lines.append("| " + label + " | " + ("; ".join(v["id"] + ": " + ", ".join(v["changed_fields"]) for v in values) or "None in this selected context") + " |")
        lines.append("| Excluded blanket sets | " + (", ".join(s["id"] for s in facts["applicable_excluded_sets"]) or "None in this selected ancestry") + " |")
        for group in facts["applicable_retained_sets"]:
            lines.append(f"| Retained {group['id']} | isDisjoint={group['isDisjoint']}; isComplete={group['isComplete']}; {group['criterion_status']} |")
        lines += ["", review["context_guard_note"], "", f"Complete source observations are in [contexts.json](../contexts.json). Context SHA-256: `{row['context_sha256']}`.", "", f"Authored definition SHA-256: `{row['authored_definition_sha256']}`.", "", "No formal alignment axiom, new ontology-engine execution or independent expert rating is supplied. Documentary batch accounting is complete; full component qualification and actual publication/readback retain their separate gates. #23 and #78 remain separate.", ""]
        output[f"previews/{cid}.md"] = "\n".join(lines).encode()
    buf = io.StringIO(newline="")
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(["concept_id", "title", "disposition", "rationale", "context_interpretation"])
    for r in review["concepts"]:
        writer.writerow([r["concept_id"], r["title"], r["disposition"], r["rationale"], r["context_interpretation"]])
    output["decisions.csv"] = buf.getvalue().encode()
    progress = {"status": "DOCUMENTARY_CURATION_ONLY_NOT_RELEASED", "completed": len(concepts) - len(remaining),
        "population": len(concepts), "remaining": len(remaining), "batches": []}
    for batch in allocation["batches"]:
        progress["batches"].append({**batch, "status": "DOCUMENTARY_DECISIONS_RECORDED" if not (set(batch["concept_ids"]) & remaining) else "PENDING",
                                    "remaining_concept_ids": [cid for cid in batch["concept_ids"] if cid in remaining]})
    all_rows = []
    packets = review["prior_packets"] + [str((folder / "review.json").relative_to(ROOT))]
    for path in packets:
        for row in load(ROOT / path)["concepts"]:
            cid = row["concept_id"]
            need(row["source_concept_sha256"] == context.digest(concepts[cid])
                 and row["authored_definition_sha256"] == sha(concepts[cid]["definition"].encode())
                 and row["accepted_as_documentary_decision"] is True, "inventory current-source binding")
            all_rows.append({"concept_id": cid, "title": concepts[cid]["display_title"], "subdomain_id": concepts[cid]["domain_id"],
                "disposition": row["disposition"], "review_path": path, "review_record_sha256": context.digest(row),
                "source_concept_sha256": row["source_concept_sha256"], "followup_issues": row["followup_issues"]})
    need(len(all_rows) == 82 and {r["concept_id"] for r in all_rows} == set(concepts) and not remaining, "inventory exact population")
    deferred = [r for r in all_rows if r["disposition"] == "NEEDS_LICENSED_SOURCE"]
    need({r["concept_id"] for r in deferred} == {"RKM-C072", "RKM-C073", "RKM-C074"}
         and all(r["followup_issues"] == [78] for r in deferred), "inventory normative deferrals")
    progress.update(explicit_normative_deferrals=len(deferred), remaining_documentary_batches=0,
                    component_qualification="PENDING_N4", publication_readback="PENDING_N5")
    output["progress.json"] = (json.dumps(progress, indent=2) + "\n").encode()
    inventory = {"status": "DOCUMENTARY_DISPOSITION_INVENTORY_NOT_COMPONENT_QUALIFICATION", "population": 82,
        "disposition_counts": dict(collections.Counter(r["disposition"] for r in all_rows)),
        "explicit_normative_deferrals": len(deferred), "concepts": sorted(all_rows, key=lambda r: r["concept_id"])}
    output["coverage.json"] = (json.dumps(inventory, indent=2) + "\n").encode()
    lines = [f"# {review['execution']} — structural-context documentary review", "", "Date: " + review["date"] + ". Planning target v0.3.10; #85 remains open.", "", f"**This batch is complete: {len(review['concepts'])} concepts. Current-source documentary coverage is {progress['completed']}/{progress['population']} ({100*progress['completed']/progress['population']:.1f}%); {progress['remaining']} remain.** This fraction is not overall research completion, semantic correctness or independent acceptance.", "", "## What was reviewed", "", "The selected current concept definitions, direct associations/generalizations, complete ancestry, changed ancestor records, changed association-neighbor records, applicable explicit set policy and analytical-case application policy were compared with the historical source. Primary source editions, locators and selected passages were checked separately. An unchanged edge does not hide the change in its endpoint's meaning.", "", "| Concept | Disposition | Current-context interpretation |", "|---|---|---|"]
    for r in review["concepts"]:
        lines.append(f"| [{r['title']}](previews/{r['concept_id']}.md) | {r['disposition']} | {r['context_interpretation']} |")
    lines += ["", "[Complete 82-concept disposition inventory](coverage.json): exact population and source/packet routes, including three explicit normative deferrals; not component qualification or publication.", "", "## Findings and limits", ""]
    for paragraph in review["batch_findings"]:
        lines += [paragraph, ""]
    lines += ["## Primary sources", ""]
    for source in review["sources"].values():
        lines.append(f"- [{source['title']}]({source['url']}) — {source['version']}; accessed {source['accessed']}. {source['inspection_scope']}")
    lines += ["", review["source_access_note"], "", "## Verification and reproduction", "", "From the repository root:", "", "```sh", "python -B evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-06/build.py --batch " + folder.name, "python -B evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-06/build.py --batch " + folder.name + " --check", "```", "", "The validator binds raw source/prior/allocation/passage/context files; recomputes the structural context; checks the declared population and disjoint cumulative coverage; preserves authored definitions and separates comparison targets and policy conclusions. validation.json records local negative integrity controls; reproduction.json records separate-process byte equality. These are not CI, HermiT, SHACL or independent expert results.", "", "## Next execution", "", review["next_execution_note"], ""]
    output["README.md"] = "\n".join(lines).encode()
    return output


def verify(expected, actual):
    need(set(expected) == set(actual), "output coverage")
    for name, body in expected.items():
        need(actual[name] == body, "rendered body mismatch: " + name)


def controls(review, folder):
    tests = []
    edits = [
        ("missing_record", lambda r: r["concepts"].pop(), "declared batch coverage"),
        ("stale_scientific_source", lambda r: r["inputs"].update({BASE_INPUTS[1]: "0" * 64}), "stale source input"),
        ("inferred_sibling_exclusivity", lambda r: r["concepts"][0]["interpretation_guards"].update(sibling_exclusivity_inferred_from_parenthood=True), "unsupported policy inference"),
        ("unsupported_equivalence", lambda r: r["concepts"][0].update(formal_alignment="EQUIVALENT"), "unsupported semantic acceptance"),
    ]
    edits += [
        ("working_group_note_promoted_to_recommendation", lambda r: r["sources"]["dqv"].update(version="W3C Recommendation"), "source edition status"),
        ("observable_quality_promoted_to_information_specification", lambda r: r["terms"]["observable"].update(target_kind="INFORMATION_SPECIFICATION_CLASS"), "source term kind"),
    ]
    for name, mutate, reason in edits:
        r = copy.deepcopy(review)
        mutate(r)
        try:
            validate(r, folder)
        except ValueError as exc:
            need(reason in str(exc), "wrong rejection: " + str(exc))
            tests.append({"control": name, "rejected": True, "reason": str(exc)})
        else:
            raise ValueError("escaped mutation: " + name)
    original = load(folder / "contexts.json")
    first = review["concepts"][0]["concept_id"]
    ancestor_id = next(cid for cid, v in original.items() if v["ancestor_edges"])
    neighbor_id = next(cid for cid, v in original.items() if v["changed_association_neighbors"])
    excluded_id = next(cid for cid, v in original.items() if v["applicable_excluded_sets"])
    context_edits = [
        ("missing_ancestor_edge", lambda x: x[ancestor_id]["ancestor_edges"].pop()),
        ("missing_changed_neighbor", lambda x: x[neighbor_id].update(changed_association_neighbors=[])),
        ("missing_excluded_set_policy", lambda x: x[excluded_id].update(applicable_excluded_sets=[])),
    ]
    for name, mutate in context_edits:
        altered = copy.deepcopy(original)
        mutate(altered)
        need(altered != original, "mutation did not apply: " + name)
        try:
            validate(review, folder, altered)
        except ValueError as exc:
            need("structural context mismatch" in str(exc), "wrong context rejection")
            tests.append({"control": name, "rejected": True, "reason": str(exc)})
        else:
            raise ValueError("escaped context mutation: " + name)
    original_contracts = load(folder / "evidence-monitoring-checks.json")
    for name, mutate in [
        ("missing_reference_role_specialization", lambda x: x["reference_local_edge_delta"].update(generalizations=[])),
        ("threshold_forced_to_have_indicator", lambda x: x["relations"]["RX-025"].update(target_end_cardinality="1")),
        ("signal_linked_to_occurrence_instead_of_result", lambda x: x["relations"]["RX-026"].update(target="RKM-C004")),
        ("unqualified_reference_substituted_for_mediated_role", lambda x: x["relations"]["RE-002"].update(target="RKM-C065")),
    ]:
        altered_contracts = copy.deepcopy(original_contracts)
        mutate(altered_contracts)
        try:
            validate(review, folder, evidence_override=altered_contracts)
        except ValueError as exc:
            need("evidence/monitoring context mismatch" in str(exc), "wrong boundary rejection")
            tests.append({"control": name, "rejected": True, "reason": str(exc)})
        else:
            raise ValueError("escaped evidence/monitoring mutation: " + name)
    for guard in ("citation_proves_claim_truth", "signal_proves_occurrence", "qualitative_boundary_requires_invented_numeric_unit"):
        altered_review = copy.deepcopy(review)
        altered_review["concepts"][0]["evidence_monitoring_guards"][guard] = True
        try:
            validate(altered_review, folder)
        except ValueError as exc:
            need("unsupported evidence/monitoring inference" in str(exc), "wrong evidence rejection")
            tests.append({"control": guard, "rejected": True, "reason": str(exc)})
        else:
            raise ValueError("escaped evidence/monitoring inference: " + guard)
    expected = render(review, folder)
    altered = dict(expected)
    key = "previews/" + first + ".md"
    altered[key] = altered[key].replace(review["concepts"][0]["authored_definition"].encode(), b"Edited definition.", 1)
    need(altered[key] != expected[key], "preview mutation did not apply")
    try:
        verify(expected, altered)
    except ValueError as exc:
        need("rendered body mismatch" in str(exc), "wrong preview rejection")
        tests.append({"control": "changed_preview_definition", "rejected": True, "reason": str(exc)})
    else:
        raise ValueError("escaped preview mutation")
    return tests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", default="batch-06", choices=["batch-06"])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.batch.startswith("batch-") and "/" not in args.batch and ".." not in args.batch, "batch path")
    folder = HERE / args.batch
    review = load(folder / "review.json")
    outputs = render(review, folder)
    report = {"status": "PASS_LOCAL_DOCUMENTARY_BATCH_NOT_PUBLICATION", "execution": review["execution"],
        "runtime": "LOCAL_PYTHON_NOT_CI_OR_ONTOLOGY_ENGINE", "summary": review["summary"],
        "review_sha256": sha((folder / "review.json").read_bytes()),
        "builder_sha256": sha(Path(__file__).read_bytes()), "context_extractor_sha256": sha((HERE / "context.py").read_bytes()), "evidence_monitoring_extractor_sha256": sha((folder / "evidence_monitoring_context.py").read_bytes()),
        "negative_controls": controls(review, folder), "outputs": {k: sha(v) for k, v in sorted(outputs.items())}}
    outputs["validation.json"] = (json.dumps(report, indent=2) + "\n").encode()
    if args.check:
        verify(outputs, {key: (folder / key).read_bytes() for key in outputs})
        need({str(p.relative_to(folder)) for p in (folder / "previews").rglob("*") if p.is_file()} ==
             {name for name in outputs if name.startswith("previews/")}, "unexpected preview file")
    else:
        for name, body in outputs.items():
            path = folder / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
    print(json.dumps({"status": report["status"], "mode": "check" if args.check else "build",
                      "records": len(review["concepts"]), "negative_controls_rejected": len(report["negative_controls"]), "outputs": len(outputs)}))


if __name__ == "__main__":
    main()
