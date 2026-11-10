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
import treatment_policy_context

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


def validate(review, folder, override=None, treatment_override=None):
    local = [str((folder / name).relative_to(ROOT)) for name in
             ("source-access.json", "passage-checks.json", "contexts.json", "treatment-policy-checks.json", "metadata-checks.json")]
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
    contracts = treatment_override if treatment_override is not None else load(folder / "treatment-policy-checks.json")
    need(contracts == treatment_policy_context.extract(current, context), "treatment/policy context mismatch")
    treatment_policy_context.check(contracts)
    access, passages = load(folder / "source-access.json"), load(folder / "passage-checks.json")
    term_ids = {tid for r in rows for tid in r["comparison_term_ids"]}
    need(term_ids == set(review["terms"]) == set(passages), "term/passage coverage")
    metadata = load(folder / "metadata-checks.json")
    metadata_ids = {sid for r in rows for sid in r["metadata_source_ids"]}
    need(metadata_ids == set(metadata) == {"iso"}, "metadata coverage")
    iso = metadata["iso"]
    need(iso["observed_reference"] == "ISO 31073:2022" and iso["observed_edition"] == 1
         and iso["observed_publication_date"] == "2022-02" and iso["normative_term_text_inspected"] is False
         and iso["exact_crosswalk_adopted"] is False and iso["followup_issue"] == 78
         and iso["fresh_catalogue_response_sha256"] is None
         and iso["historical_catalogue_response_sha256"] == previous["sources"]["iso"]["document_sha256"]
         and len(iso["selected_metadata_sha256"]) == 64, "metadata/term boundary")
    source_ids = {t["source_id"] for t in review["terms"].values()} | metadata_ids
    need(source_ids == set(review["sources"]) == set(access), "source coverage")
    for sid, source in review["sources"].items():
        for field in ("url", "document_sha256", "accessed", "direct_access", "same_response_as_prior"):
            need(source[field] == access[sid][field], "source access binding")
        need(source["version"] == previous["sources"][sid]["version"] and source["inspection_scope"], "source edition status")
        if sid == "nist":
            need(source["direct_access"] == "WEB_SELECTED_PAGES_SUCCESS_DIRECT_HTTP_FAILED"
                 and source["document_sha256"] is None and source["same_response_as_prior"] is None
                 and source["historical_document_sha256"] == previous["sources"][sid]["document_sha256"]
                 and source["fresh_full_body_hash_verified"] is False, "PDF access boundary")
        elif sid == "iso":
            need(source["direct_access"] == "OFFICIAL_CATALOGUE_METADATA_ONLY"
                 and source["document_sha256"] is None and source["same_response_as_prior"] is None
                 and source["historical_document_sha256"] == previous["sources"][sid]["document_sha256"]
                 and source["normative_term_text_inspected"] is False
                 and source["fresh_full_body_hash_verified"] is False
                 and iso["url"] == source["url"], "metadata source boundary")
        else:
            need(source["direct_access"] == "SUCCESS" and source["same_response_as_prior"] is True, "source inspection")
            need(source["document_sha256"] == previous["sources"][sid]["document_sha256"], "source edition/body change needs review")
    for tid, term in review["terms"].items():
        source, passage = review["sources"][term["source_id"]], passages[tid]
        need(term["url"].startswith(source["url"]) and term["locator"] == previous["terms"][tid]["locator"], "source locator/attribution")
        need(passage["source_document_sha256"] == source["document_sha256"] and passage["url"] == term["url"]
             and passage["locator"] == term["locator"] and len(passage["selected_text_sha256"]) == 64, "selected passage binding")
        expected_kinds = {"response": "SECURITY_RISK_RESPONSE_PROCESS_TERM", "controls": "SECURITY_SAFEGUARD_TERM",
            "entity": "PROVENANCE_CLASS", "plan": "PROVENANCE_CLASS", "concept": "VOCABULARY_CLASS"}
        need(term["target_kind"] == expected_kinds[tid], "source term kind")
        if term["source_id"] == "nist":
            need(passage["source_document_sha256"] is None
                 and passage["historical_document_sha256"] == source["historical_document_sha256"]
                 and passage["selector"]["kind"] == "WEB_PDF_TEXT_LINES"
                 and passage["selector"]["visual_page_checked"] is True, "selected PDF passage boundary")
    for row in rows:
        cid = row["concept_id"]
        concept, pr, facts = now[cid], prior[cid], contexts[cid]
        need(row["impact_category"] == effects[cid]["category"] == "STRUCTURAL_CONTEXT_RECHECK", "impact category")
        need(row["source_concept_sha256"] == context.digest(concept), "concept binding")
        need(row["authored_definition"] == concept["definition"] and row["authored_definition_sha256"] == sha(concept["definition"].encode()), "authored definition")
        need(row["previous_review_sha256"] == context.digest(pr), "historical review binding")
        need(row["context_sha256"] == context.digest(facts), "review/context binding")
        need(set(row["constraint_ids"]) <= set(contracts["constraints"]) and row["constraint_ids"], "constraint route")
        guards = row["treatment_policy_guards"]
        need(set(guards) == {"decision_proves_execution", "plan_proves_effectiveness", "unresolved_reference_proves_control",
             "tolerance_meanings_silently_equated", "metadata_proves_normative_term", "appetite_statement_proves_universal_authorization"}
             and all(value is False for value in guards.values()), "unsupported treatment/policy inference")
        need(row["title"] == concept["display_title"] and row["subdomain_id"] == concept["domain_id"]
             and concept["domain_id"] in declared["subdomain_ids"], "concept identity")
        need(row["previous_disposition"] == pr["disposition"] and row["disposition"] in
             ("RELATED", "ANALOGY", "CONTRAST", "NO_DIRECT_EQUIVALENT_REVIEWED", "NEEDS_LICENSED_SOURCE"), "documentary disposition")
        need(row["comparison_term_ids"] == pr["term_ids"] and row["followup_issues"] == pr["followup_issues"], "prior route preserved")
        need(row["normative_term_text_inspected"] is False and row["exact_normative_mapping_adopted"] is False
             and row["normative_term_locator"] is None, "normative deferral route")
        if cid in ("RKM-C072", "RKM-C073", "RKM-C074"):
            need(row["disposition"] == "NEEDS_LICENSED_SOURCE" and row["comparison_term_ids"] == []
                 and row["metadata_source_ids"] == ["iso"] and row["followup_issues"] == [78]
                 and row["source_locator_status"] == "METADATA_ONLY_NO_NORMATIVE_TERM_LOCATOR", "normative deferral route")
        else:
            need(row["comparison_term_ids"] and row["metadata_source_ids"] == [], "comparison route")
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
        "deferred_normative_dispositions": sum(r["disposition"] == "NEEDS_LICENSED_SOURCE" for r in rows),
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
        if not row["comparison_term_ids"]:
            del lines[-2:]
            lines += [review["normative_deferral_note"], "", "| Metadata source | Inspected scope |", "|---|---|"]
            for sid in row["metadata_source_ids"]:
                source = review["sources"][sid]
                lines.append(f"| [{source['title']}]({source['url']}) | {source['version']}; official identity/abstract only; exact term text deferred to [#78](https://github.com/ArazSaieArasi3/riskium/issues/78). |")
        for tid in row["comparison_term_ids"]:
            term = review["terms"][tid]
            lines.append(f"| [{term['name']}]({term['url']}) | {term['target_kind']}; {term['locator']} |")
        lines += ["", "## Current structural context", "", row["context_interpretation"], "", f"Source continuity: concept record unchanged={facts['concept_record_unchanged']}; direct edges unchanged={facts['local_edges_unchanged']}; inherited edges unchanged={facts['ancestor_edges_unchanged']}. Ancestor and neighbor changes are reported separately.", "", "| Observation | Source-bound result |", "|---|---|"]
        lines.append("| Inheritance path | " + "; ".join(f"{e['id']}: {e['specific']} → {e['general']}" for e in facts["ancestor_edges"]) + " |")
        lines.append("| Source constraint route | " + ", ".join(row["constraint_ids"]) + " — [selected source statements](../treatment-policy-checks.json) |")
        for field, label in (("changed_ancestors", "Changed ancestor"), ("changed_association_neighbors", "Changed relation neighbor")):
            values = facts[field]
            lines.append("| " + label + " | " + ("; ".join(v["id"] + ": " + ", ".join(v["changed_fields"]) for v in values) or "None in this selected context") + " |")
        lines.append("| Excluded blanket sets | " + (", ".join(s["id"] for s in facts["applicable_excluded_sets"]) or "None in this selected ancestry") + " |")
        for group in facts["applicable_retained_sets"]:
            lines.append(f"| Retained {group['id']} | isDisjoint={group['isDisjoint']}; isComplete={group['isComplete']}; {group['criterion_status']} |")
        lines += ["", review["context_guard_note"], "", f"Complete source observations are in [contexts.json](../contexts.json). Context SHA-256: `{row['context_sha256']}`.", "", f"Authored definition SHA-256: `{row['authored_definition_sha256']}`.", "", "No formal alignment axiom, new ontology-engine execution or independent expert rating is supplied. Remaining documentary batches, full component qualification and actual publication/readback retain their separate gates. #23 and #78 remain separate.", ""]
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
    output["progress.json"] = (json.dumps(progress, indent=2) + "\n").encode()
    lines = [f"# {review['execution']} — structural-context documentary review", "", "Date: " + review["date"] + ". Planning target v0.3.10; #85 remains open.", "", f"**This batch is complete: {len(review['concepts'])} concepts. Current-source documentary coverage is {progress['completed']}/{progress['population']} ({100*progress['completed']/progress['population']:.1f}%); {progress['remaining']} remain.** This fraction is not overall research completion, semantic correctness or independent acceptance.", "", "## What was reviewed", "", "The selected current concept definitions, direct associations/generalizations, complete ancestry, changed ancestor records, changed association-neighbor records, applicable explicit set policy and analytical-case application policy were compared with the historical source. Primary source editions, locators and selected passages were checked separately. An unchanged edge does not hide the change in its endpoint's meaning.", "", "| Concept | Disposition | Current-context interpretation |", "|---|---|---|"]
    for r in review["concepts"]:
        lines.append(f"| [{r['title']}](previews/{r['concept_id']}.md) | {r['disposition']} | {r['context_interpretation']} |")
    lines += ["", "## Findings and limits", ""]
    for paragraph in review["batch_findings"]:
        lines += [paragraph, ""]
    lines += ["## Primary sources", ""]
    for source in review["sources"].values():
        lines.append(f"- [{source['title']}]({source['url']}) — {source['version']}; accessed {source['accessed']}. {source['inspection_scope']}")
    lines += ["", review["source_access_note"], "", "## Verification and reproduction", "", "From the repository root:", "", "```sh", "python -B evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-05/build.py --batch " + folder.name, "python -B evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-05/build.py --batch " + folder.name + " --check", "```", "", "The validator binds raw source/prior/allocation/passage/context files; recomputes the structural context; checks the declared population and disjoint cumulative coverage; preserves authored definitions and separates comparison targets and policy conclusions. validation.json records local negative integrity controls; reproduction.json records separate-process byte equality. These are not CI, HermiT, SHACL or independent expert results.", "", "## Next execution", "", review["next_execution_note"], ""]
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
    deferred_index = next(i for i, row in enumerate(review["concepts"]) if row["concept_id"] == "RKM-C072")
    edits += [
        ("catalogue_promoted_to_normative_term_access", lambda r: r["sources"]["iso"].update(normative_term_text_inspected=True), "metadata source boundary"),
        ("unretrieved_full_pdf_hash_claimed_current", lambda r: r["sources"]["nist"].update(document_sha256=r["sources"]["nist"]["historical_document_sha256"]), "source access binding"),
        ("lost_normative_followup", lambda r: r["concepts"][deferred_index].update(followup_issues=[]), "prior route preserved"),
        ("deferred_comparison_claimed_accepted", lambda r: r["concepts"][deferred_index].update(disposition="RELATED"), "normative deferral route"),
        ("invented_normative_clause", lambda r: r["concepts"][deferred_index].update(normative_term_locator="invented clause"), "normative deferral route"),
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
    original_contracts = load(folder / "treatment-policy-checks.json")
    for name, mutate in [
        ("unresolved_control_reference_forced_resolved", lambda x: x["relations"]["RX-020"].update(target_end_cardinality="1")),
        ("plan_substituted_for_actual_treatment_event", lambda x: x["relations"]["R-64"].update(source="RKM-C043")),
        ("heterogeneous_control_promoted_to_core_class", lambda x: x["identity"]["RKM-C045"].update(scope_layer="FORMAL_CORE")),
    ]:
        altered_contracts = copy.deepcopy(original_contracts)
        mutate(altered_contracts)
        try:
            validate(review, folder, treatment_override=altered_contracts)
        except ValueError as exc:
            need("treatment/policy context mismatch" in str(exc), "wrong boundary rejection")
            tests.append({"control": name, "rejected": True, "reason": str(exc)})
        else:
            raise ValueError("escaped treatment/policy mutation: " + name)
    for guard in ("plan_proves_effectiveness", "tolerance_meanings_silently_equated", "appetite_statement_proves_universal_authorization"):
        altered_review = copy.deepcopy(review)
        altered_review["concepts"][0]["treatment_policy_guards"][guard] = True
        try:
            validate(altered_review, folder)
        except ValueError as exc:
            need("unsupported treatment/policy inference" in str(exc), "wrong policy rejection")
            tests.append({"control": guard, "rejected": True, "reason": str(exc)})
        else:
            raise ValueError("escaped treatment/policy inference: " + guard)
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
    parser.add_argument("--batch", default="batch-05", choices=["batch-05"])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.batch.startswith("batch-") and "/" not in args.batch and ".." not in args.batch, "batch path")
    folder = HERE / args.batch
    review = load(folder / "review.json")
    outputs = render(review, folder)
    report = {"status": "PASS_LOCAL_DOCUMENTARY_BATCH_NOT_PUBLICATION", "execution": review["execution"],
        "runtime": "LOCAL_PYTHON_NOT_CI_OR_ONTOLOGY_ENGINE", "summary": review["summary"],
        "review_sha256": sha((folder / "review.json").read_bytes()),
        "builder_sha256": sha(Path(__file__).read_bytes()), "context_extractor_sha256": sha((HERE / "context.py").read_bytes()), "treatment_policy_extractor_sha256": sha((folder / "treatment_policy_context.py").read_bytes()),
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
