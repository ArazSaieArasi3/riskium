#!/usr/bin/env python3
"""Offline integrity checks and rendering for the authored N3a documentary review."""
import argparse
import collections
import copy
import csv
import hashlib
import io
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
PREFIX = str(HERE.relative_to(ROOT)) + "/"
FILES = ["ontology/riskium-model.json", "ontology/0.3.2/riskium-model.json",
         "references/concept-definitions/0.1.0/review.json",
         "evaluation/releases/v0.3.9/followups/issue85-impact/impact.json",
         "evaluation/releases/v0.3.9/followups/issue85-changed-review/review.json",
         PREFIX + "source-access.json", PREFIX + "passage-checks.json",
         PREFIX + "remaining-batches.json"]
EXPECTED_DISPOSITIONS = {"RKM-C004": "CONTRAST", "RKM-C007": "ANALOGY", "RKM-C008": "RELATED",
    "RKM-C009": "CONTRAST", "RKM-C010": "CONTRAST", "RKM-C011": "RELATED", "RKM-C012": "ANALOGY",
    "RKM-C013": "CONTRAST", "RKM-C016": "RELATED", "RKM-C023": "CONTRAST", "RKM-C031": "CONTRAST",
    "RKM-C044": "ANALOGY", "RKM-C045": "ANALOGY", "RKM-C052": "RELATED", "RKM-C063": "CONTRAST",
    "RKM-C064": "CONTRAST", "RKM-C067": "RELATED"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canon(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def load(path):
    return json.loads(path.read_text())


def need(condition, message):
    if not condition:
        raise ValueError(message)


def neighborhood(model, cid):
    return {k: sorted([x for x in model[k] if cid in
            [x.get("source"), x.get("target"), x.get("specific"), x.get("general")]], key=lambda x: x["id"])
            for k in ("associations", "generalizations")}


def check_batches(batches, expected):
    ids = [cid for batch in batches["batches"] for cid in batch["concept_ids"]]
    need(len(ids) == 57 and len(set(ids)) == 57 and set(ids) == expected, "remaining batch coverage")
    need(all(b["status"] == "NOT_REVIEWED_IN_N3A" for b in batches["batches"]), "planned status")


def validate(review):
    need(set(review["inputs"]) == set(FILES), "input coverage")
    for name, digest in review["inputs"].items():
        need(sha((ROOT / name).read_bytes()) == digest, "stale input: " + name)
    old, current, prior, impact, n2, access, passages, batches = [load(ROOT / p) for p in FILES]
    a = {c["id"]: c for c in old["concepts"]}
    b = {c["id"]: c for c in current["concepts"]}
    p = {r["concept_id"]: r for r in prior["concepts"]}
    selected = {r["id"] for r in impact["rows"] if r["category"] == "REUSE_CANDIDATE"}
    rows = review["concepts"]
    need(len(rows) == 17 and {r["concept_id"] for r in rows} == selected == set(EXPECTED_DISPOSITIONS), "seventeen-record coverage")
    earlier = {r["concept_id"] for r in n2["concepts"]}
    remaining = {r["id"] for r in impact["rows"] if r["category"] == "STRUCTURAL_CONTEXT_RECHECK"}
    check_batches(batches, remaining)
    need(all(b[cid]["domain_id"] in batch["subdomain_ids"]
             for batch in batches["batches"] for cid in batch["concept_ids"]), "batch subdomain allocation")
    need(len(earlier) == 8 and not selected & earlier and not remaining & (selected | earlier)
         and selected | earlier | remaining == set(b) and len(b) == 82, "current population partition")
    need(set(review["sources"]) == set(access) == {"nist", "mode", "prov", "relator", "skos", "sosa"}, "source coverage")
    term_ids = {t for r in rows for t in r["passage_ids"]}
    need(term_ids == set(review["terms"]) == set(passages), "selected passage coverage")
    for sid, source in review["sources"].items():
        for field in ("url", "document_sha256", "accessed", "direct_access", "same_response_as_prior"):
            need(source[field] == access[sid][field], "access binding: " + sid)
        need(source["direct_access"] == "SUCCESS" and source["version"] and len(source["document_sha256"]) == 64, "source identity")
    for tid, term in review["terms"].items():
        source = review["sources"][term["source_id"]]
        passage = passages[tid]
        need(term["url"].startswith(source["url"]) and term["locator"].strip(), "term locator")
        need(passage["url"] == term["url"] and passage["locator"] == term["locator"]
             and passage["source_document_sha256"] == source["document_sha256"]
             and passage["inspection"] == "SELECTED_PASSAGE_INSPECTED", "passage binding")
        need(len(passage["selected_text_sha256"]) == 64 and passage["selected_text_chars"] > 0, "passage digest")
        # Preserve the glossary's displayed attribution without claiming those original works were reread.
        if term["source_id"] == "nist":
            need(term["locator"] == prior["terms"][tid]["locator"], "glossary attribution")
    for r in rows:
        cid = r["concept_id"]
        c, previous = b[cid], p[cid]
        need(a[cid] == c and neighborhood(old, cid) == neighborhood(current, cid), "incompatible source/context: " + cid)
        need(r["source_concept_sha256"] == sha(canon(c)), "concept digest")
        need(r["authored_definition"] == c["definition"] and r["authored_definition_sha256"] == sha(c["definition"].encode()), "authored definition")
        need(r["previous_review_sha256"] == sha(canon(previous)), "prior binding")
        need(r["local_neighborhood_sha256"] == sha(canon(neighborhood(current, cid))), "neighborhood binding")
        need(r["source_record_unchanged"] is True and r["local_neighborhood_unchanged"] is True and r["impact_category"] == "REUSE_CANDIDATE", "reuse qualification")
        need(r["title"] == c["display_title"] and r["subdomain_id"] == c["domain_id"], "concept identity")
        need(r["previous_disposition"] == previous["disposition"] and r["disposition"] == EXPECTED_DISPOSITIONS[cid], "decision contract")
        need(r["formal_alignment"] == "UNASSESSED" and r["independent_validation"] == "NOT_PERFORMED", "unsupported acceptance")
        need(r["followup_issues"] == previous["followup_issues"], "follow-up preserved")
        need(r["accepted_as_documentary_decision"] is True and r["rationale"] and r["boundary"], "documentary rationale")
        need(set(r["comparison_term_ids"] + r["foundation_term_ids"]) == set(r["passage_ids"]) == set(previous["term_ids"]), "comparison/foundation coverage")
        need(set(r["foundation_term_ids"]) == set(previous["term_ids"]) & {"mode", "relator"}, "foundation boundary")
    expected_summary = {"this_packet": 17, "prior_n2": 8, "cumulative_documentary_dispositions": 25,
        "population": 82, "remaining": 57, "dispositions": dict(collections.Counter(r["disposition"] for r in rows)),
        "scoped_labels_clarified": sum(r["disposition"] != r["previous_disposition"] for r in rows)}
    need(review["summary"] == expected_summary and expected_summary["scoped_labels_clarified"] == 3, "summary")
    need(review["status"] == "N3A_COMPLETE_FULL_CURRENT_CURATION_PENDING" and review["model_version"] == "0.3.2", "scope status")
    for field in ("scientific_source_modified", "historical_curation_modified", "published", "formal_alignment_axioms_added"):
        need(review["boundaries"][field] is False, "premature claim")
    need(review["boundaries"]["engine_runs"] == 0 and review["boundaries"]["independent_validation"] == "NOT_PERFORMED", "execution boundary")
    return b, batches


def render(review):
    concepts, batches = validate(review)
    base = "https://github.com/ArazSaieArasi3/riskium/blob/" + review["baseline_commit"] + "/"
    output = {}
    for r in review["concepts"]:
        c = concepts[r["concept_id"]]
        lines = [f"# {r['title']} — compatible-reuse preview", "", "**Planning documentary preview; not deployed or independently validated.**", "", "## Authored definition, unchanged", "", r["authored_definition"], "", f"[Scientific source 0.3.2]({base}ontology/0.3.2/riskium-model.json). Subdomain {r['subdomain_id']}. Stereotype: {c['ontouml_stereotype'] or 'no universal stereotype asserted'}.", "", "Identity basis: " + c["identity_basis"], "", "Authored verification status, preserved verbatim: " + c["verification_status"], "", "Later bounded qualification/publication evidence is recorded separately in the [v0.3.9 receipt](" + base + "evaluation/releases/v0.3.9/R2b-outcome.md). A carried source label is not an independent semantic rating.", "", "## Current-source documentary decision", "", f"**{r['previous_disposition']} → {r['disposition']}**; {r['decision_kind']}.", "", r["rationale"], "", r["boundary"], "", "| Evidence purpose | Selected source term and locator |", "|---|---|"]
        for field, purpose in (("comparison_term_ids", "External comparison"), ("foundation_term_ids", "Modeling foundation")):
            for tid in r[field]:
                t = review["terms"][tid]
                lines.append(f"| {purpose} | [{t['name']}]({t['url']}) — {t['locator']} |")
        lines += ["", "## Traceability and acceptance boundary", "", "Complete concept and direct association/generalization records match the historical source. This limited context check does not establish that every global or indirect semantic dependency is unchanged.", "", f"Concept SHA-256: `{r['source_concept_sha256']}`. Definition SHA-256: `{r['authored_definition_sha256']}`.", "", f"Direct neighborhood SHA-256: `{r['local_neighborhood_sha256']}`.", "", "No formal equivalence, imported restriction, or independent expert rating is emitted. The full current curation still requires 57 structural-context decisions and qualification/publication/readback. Existing #23 and #78 work remains separate.", ""]
        output[f"previews/{r['concept_id']}.md"] = "\n".join(lines).encode()
    buf = io.StringIO(newline="")
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(["concept_id", "title", "prior", "current", "decision", "rationale", "boundary"])
    for r in review["concepts"]:
        writer.writerow([r["concept_id"], r["title"], r["previous_disposition"], r["disposition"], r["decision_kind"], r["rationale"], r["boundary"]])
    output["decisions.csv"] = buf.getvalue().encode()
    lines = ["# N3a — compatible reuse confirmed for 17 concepts", "", "Date: 10 November 2026. Planning target v0.3.10; #85 remains open. **N3a is complete; full current curation is not yet complete.**", "", "## Result and scope", "", "All 17 reuse candidates have current-source documentary dispositions: eight CONTRAST, five RELATED and four ANALOGY. Fourteen disposition labels are retained; three scoped absence labels (C010/C013/C064) are clarified as explicit contrasts with the selected terms. No authored definition or scientific identity rule changes.", "", "Together with N2, 25 of 82 current catalog concepts now have recorded current-source documentary dispositions (30.5% of this curation population). The remaining 57 are structural-context checks. This fraction is not overall research completion, semantic correctness or independent expert acceptance.", "", "| Concept | Previous → current | Documentary decision |", "|---|---|---|"]
    for r in review["concepts"]:
        lines.append(f"| [{r['title']}](previews/{r['concept_id']}.md) | {r['previous_disposition']} → {r['disposition']} | {r['rationale']} |")
    lines += ["", "## Primary evidence and qualifications", ""]
    for sid, source in review["sources"].items():
        lines.append(f"- [{source['title']}]({source['url']}) — {source['version']}; accessed {source['accessed']}. {source['inspection_scope']}")
    lines += ["", "All six source responses were retrieved directly. Five prior non-null response hashes match exactly. The Mode source now also has a direct-response hash; the older failed-access/null-hash history remains intact. Selected PDF page/HTML anchor evidence is fingerprinted in passage-checks.json. It records inspected passages without redistributing the documents. Glossary attributions identify what SP 800-30 itself attributes; they do not claim that the attributed originals were independently reread.", "", "Modeling foundations (Mode and Relator) are kept separate from domain comparisons. A relator cardinality-minimum sum alone does not establish distinct individuals. For Observation, the selected definition is used without importing displayed SOSA/SSN restrictions. NIST security-specific readings are not silently generalized to all ecosystem/enterprise risk.", "", "## Verification", "", "From the repository root:", "", "```sh", "python evaluation/releases/v0.3.9/followups/issue85-reuse-review/build.py", "python evaluation/releases/v0.3.9/followups/issue85-reuse-review/build.py --check", "```", "", "The validator checks source/prior/impact/N2 bindings, all 17 unchanged concept/direct-neighborhood records, selected evidence routes, source attribution and the complete disjoint 8 + 17 + 57 population. Negative controls exercise documentary integrity, not ontology engines. validation.json records those checks; reproduction.json records a separate byte-identical rebuild. No CI or new HermiT/SHACL execution is claimed.", "", "## Remaining finite batches", "", "These are planned, not reviewed by N3a:", "", "| Execution | Subdomains | Concepts |", "|---|---|---|"]
    for batch in batches["batches"]:
        lines.append(f"| {batch['execution']} | {', '.join(batch['subdomain_ids'])} | {len(batch['concept_ids'])} |")
    lines += ["", "Exact IDs are in remaining-batches.json. N3b-1 (D01/D03, 11 concepts) is next. After all 82 decisions, qualify the successor curation component, select the package, then publish/read back repository/Wiki/Pages. Close #85 only after its final gate. Main, published v0.3.9, reader 0.4.9, historical curation 0.1.0 and article 7.2.21 are unchanged by this planning packet. Exact normative adoption remains #78 and independent semantic review remains #23.", ""]
    output["README.md"] = "\n".join(lines).encode()
    return output


def equal(expected, actual):
    need(set(expected) == set(actual), "output coverage")
    for key, body in expected.items():
        need(actual[key] == body, "rendered body mismatch: " + key)


def negative_controls(review):
    tests = []
    cases = [
        ("missing_record", lambda x: x["concepts"].pop(), "seventeen-record coverage"),
        ("stale_source", lambda x: x["inputs"].update({FILES[1]: "0" * 64}), "stale input"),
        ("changed_definition", lambda x: x["concepts"][0].update(authored_definition="An edited definition."), "authored definition"),
        ("stale_neighborhood", lambda x: x["concepts"][0].update(local_neighborhood_sha256="0" * 64), "neighborhood binding"),
        ("lost_glossary_attribution", lambda x: x["terms"]["vulnerability"].update(locator="Appendix B"), "passage binding"),
        ("unsupported_equivalence", lambda x: x["concepts"][0].update(formal_alignment="EQUIVALENT"), "unsupported acceptance"),
        ("premature_publication", lambda x: x["boundaries"].update(published=True), "premature claim"),
    ]
    for name, mutate, reason in cases:
        x = copy.deepcopy(review)
        mutate(x)
        try:
            validate(x)
        except ValueError as exc:
            need(reason in str(exc), "unexpected rejection: " + str(exc))
            tests.append({"control": name, "rejected": True, "reason": str(exc)})
        else:
            raise ValueError("escaped mutation: " + name)
    batches = load(HERE / "remaining-batches.json")
    remaining_ids = {cid for batch in batches["batches"] for cid in batch["concept_ids"]}
    batches["batches"][0]["concept_ids"][0] = batches["batches"][0]["concept_ids"][1]
    try:
        check_batches(batches, remaining_ids)
    except ValueError as exc:
        need("remaining batch coverage" in str(exc), "wrong batch rejection")
        tests.append({"control": "duplicated_future_allocation", "rejected": True, "reason": str(exc)})
    else:
        raise ValueError("escaped future-allocation mutation")
    expected = render(review)
    actual = dict(expected)
    key = "previews/RKM-C004.md"
    actual[key] = actual[key].replace(review["concepts"][0]["authored_definition"].encode(), b"Different definition.", 1)
    need(actual[key] != expected[key], "preview mutation not applied")
    try:
        equal(expected, actual)
    except ValueError as exc:
        need("rendered body mismatch" in str(exc), "wrong preview rejection")
        tests.append({"control": "changed_preview", "rejected": True, "reason": str(exc)})
    else:
        raise ValueError("escaped preview mutation")
    return tests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    review = load(HERE / "review.json")
    output = render(review)
    receipt = {"status": "PASS_LOCAL_DOCUMENTARY_REUSE_NOT_FULL_CURATION", "execution": "LOCAL_PYTHON_NOT_CI_OR_ONTOLOGY_ENGINE",
               "builder_sha256": sha(Path(__file__).read_bytes()), "review_sha256": sha((HERE / "review.json").read_bytes()),
               "summary": review["summary"], "negative_controls": negative_controls(review),
               "outputs": {name: sha(body) for name, body in sorted(output.items())}}
    output["validation.json"] = (json.dumps(receipt, indent=2) + "\n").encode()
    if args.check:
        actual = {name: (HERE / name).read_bytes() for name in output}
        need({str(p.relative_to(HERE)) for p in (HERE / "previews").rglob("*") if p.is_file()} ==
             {name for name in output if name.startswith("previews/")}, "unexpected preview file")
        equal(output, actual)
    else:
        for name, body in output.items():
            path = HERE / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
    print(json.dumps({"status": receipt["status"], "mode": "check" if args.check else "build",
                      "records": 17, "negative_controls_rejected": len(receipt["negative_controls"]), "outputs": len(output)}))


if __name__ == "__main__":
    main()
