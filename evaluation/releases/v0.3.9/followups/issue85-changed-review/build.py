#!/usr/bin/env python3
"""Validate an authored partial curation packet and render documentary previews.

No source model, historical curation or deployed reader is modified. The mutation
controls exercise documentary integrity, not ontology engines or expert judgment.
"""
import argparse
import copy
import csv
import hashlib
import io
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
MODEL = "ontology/0.3.2/riskium-model.json"
OLD = "references/concept-definitions/0.1.0/review.json"
IMPACT = "evaluation/releases/v0.3.9/followups/issue85-impact/impact.json"
EXPECTED = {
    "RKM-C014": ("RELATED", []),
    "RKM-C015": ("CONTRAST", []),
    "RKM-C048": ("RELATED", []),
    "RKM-C049": ("RELATED", []),
    "RKM-C066": ("RELATED", ["ontouml_role"]),
    "RKM-X01": ("CONTRAST", []),
    "RKM-C075": ("ANALOGY", ["ontouml_relator"]),
    "RKM-C076": ("CONTRAST", ["ontouml_role"]),
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def load(path):
    return json.loads(path.read_text())


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(review):
    require(review["status"] == "N2_COMPLETE_FULL_CURRENT_CURATION_PENDING", "scope status")
    require(review["model_version"] == "0.3.2", "model version")
    mandatory = {MODEL, OLD, IMPACT, str((HERE / "source-access.json").relative_to(ROOT))}
    mandatory.update(f"documentation/0.4.9/reader/{cid}.md" for cid in EXPECTED)
    require(set(review["inputs"]) == mandatory, "input coverage")
    for path, expected in review["inputs"].items():
        require(sha((ROOT / path).read_bytes()) == expected, f"stale input: {path}")
    model, old, impact = load(ROOT / MODEL), load(ROOT / OLD), load(ROOT / IMPACT)
    concepts = {c["id"]: c for c in model["concepts"]}
    previous = {c["concept_id"]: c for c in old["concepts"]}
    impacts = {r["id"]: r for r in impact["rows"]}
    rows = review["concepts"]
    require(len(rows) == len(EXPECTED) and {r["concept_id"] for r in rows} == set(EXPECTED), "eight-record coverage")
    require(len(concepts) == 82 and len(previous) == 80, "source populations")
    require(review["remaining"] == {"STRUCTURAL_CONTEXT_RECHECK": 57, "REUSE_CANDIDATE": 17}, "remaining scope")
    access = load(HERE / "source-access.json")
    require(set(review["sources"]) == {"prov", "role", "relator"} == set(access), "source coverage")
    for key, source in review["sources"].items():
        for field in ("url", "document_sha256", "accessed", "access"):
            require(source[field] == access[key][field], f"source access: {key}/{field}")
        require(source["access"] == "DIRECT_HTTP_AND_SELECTED_WEB_TEXT" and len(source["document_sha256"]) == 64, "source inspection scope")
        require(source["version"] and source["inspection_scope"], "source metadata")
    for term in review["terms"].values():
        source = review["sources"][term["source_id"]]
        require(term["url"].startswith(source["url"]) and term["locator"].strip(), "source locator")
        require(term["quotation"] is False, "paraphrase boundary")
    for row in rows:
        cid = row["concept_id"]
        concept, effect, prior = concepts[cid], impacts[cid], previous.get(cid)
        require(row["source_concept_sha256"] == sha(canonical(concept)), f"concept binding: {cid}")
        require(row["authored_definition"] == concept["definition"], f"authored definition: {cid}")
        require(row["authored_definition_sha256"] == sha(concept["definition"].encode()), f"definition binding: {cid}")
        require(row["previous_review_sha256"] == (sha(canonical(prior)) if prior else None), "prior binding")
        require(row["previous_disposition"] == (prior["disposition"] if prior else None), "prior disposition")
        require(row["impact_category"] == effect["category"] and row["changed_fields"] == effect["changed_fields"], "impact binding")
        require(row["title"] == concept["display_title"] and row["subdomain_id"] == concept["domain_id"], "source identity")
        disposition, foundation = EXPECTED[cid]
        require(row["disposition"] == disposition and row["foundation_term_ids"] == foundation, "decision contract")
        require(row["formal_alignment"] == "UNASSESSED" and row["independent_validation"] == "NOT_PERFORMED", "unsupported alignment or rating")
        require(row["accepted_as_documentary_decision"] is True, "documentary disposition")
        require(row["review_status"] == "CURRENT_SOURCE_DOCUMENTARY_DISPOSITION_RECORDED", "review status")
        for tid in row["comparison_term_ids"] + foundation:
            require(tid in review["terms"], "unknown term")
        require(row["rationale"].strip() and row["comparison_term_ids"], "decision rationale")
        require(row["illustrations"]["status"] == "AUTHORED_ILLUSTRATIONS_NOT_EXECUTED_TESTS", "illustration status")
        require(row["illustrations"]["positive"] and row["illustrations"]["counterexample"], "illustration coverage")
    relations = {r["id"]: r for r in model["associations"]}
    for rid, target in (("RE-001", "RKM-C066"), ("RE-002", "RKM-C076")):
        r = relations[rid]
        require(r["source"] == "RKM-C075" and r["target"] == target and r["stereotype"] == "mediation", "mediation anchor")
        require(r["source_end_cardinality"] == "1..*" and r["target_end_cardinality"] == "1", "mandatory role dependency")
    by_id = {r["concept_id"]: r for r in rows}
    require(by_id["RKM-C075"]["relation_ids"] == ["RE-001", "RE-002", "RE-003"], "use-relation coverage")
    require(by_id["RKM-C066"]["relation_ids"] == ["RE-001"] and by_id["RKM-C076"]["relation_ids"] == ["RE-002"], "role-relation coverage")
    edges = {(g["specific"], g["general"]) for g in model["generalizations"]}
    require(("RKM-C076", "RKM-C065") in edges and ("RKM-C065", "RKM-C014") in edges and ("RKM-C066", "RKM-C014") in edges, "documentary identity path")
    require(all(concepts[cid]["identity_supplier"] == "RKM-C014" for cid in ("RKM-C066", "RKM-C076")), "role identity supplier")
    require("C-26" in by_id["RKM-C075"]["rationale"] and "additional Riskium" in by_id["RKM-C075"]["rationale"], "distinctness boundary")
    boundaries = review["boundaries"]
    require(boundaries["model_edit"] is False and boundaries["formal_alignment_axioms_added"] is False and boundaries["published_current_curation"] is False and boundaries["engine_runs_in_this_packet"] == 0, "scope boundary")
    return concepts


def render(review):
    concepts = validate(review)
    base = "https://github.com/ArazSaieArasi3/riskium/blob/" + review["baseline_commit"] + "/"
    result = {}
    for row in review["concepts"]:
        cid = row["concept_id"]
        c = concepts[cid]
        text = [f"# {c['display_title']} — current-source curation preview", "", "**N2 documentary preview; not a deployed reader or independent validation.**", "", "## Authored source, preserved verbatim", "", c["definition"], "", f"- Source: [{cid}, model 0.3.2]({base}{MODEL})", f"- Subdomain: {c['domain_id']} — {c['domain']}", f"- Stereotype: {c['ontouml_stereotype']}; identity supplier: {c['identity_supplier']}", f"- Identity basis: {c['identity_basis']}", f"- Typing rationale: {c['typing_rationale']}", f"- Authored verification status: {c['verification_status']}", "", "Historical source status strings are retained. The [publication receipt](" + base + review['boundaries']['qualification_receipt'] + ") separately records the actual bounded qualification and delivery; neither is an independent semantic rating.", "", "## Documentary decision", "", f"**{row['disposition']}**, replacing/retaining the prior disposition `{row['previous_disposition'] or 'NO_PRIOR_ROW'}`.", "", row["rationale"], "", "| Purpose | Selected term / locator |", "|---|---|"]
        for field, label in (("comparison_term_ids", "External comparison"), ("foundation_term_ids", "Modeling foundation")):
            for tid in row[field]:
                t = review["terms"][tid]
                text.append(f"| {label} | [{t['name']}]({t['url']}) — {t['locator']} |")
        text += ["", "## Illustrations, not executed tests", "", "Illustration: " + row["illustrations"]["positive"], "", "Counterexample: " + row["illustrations"]["counterexample"], "", "## Traceability and limits", "", f"Authored concept SHA-256: `{row['source_concept_sha256']}`.", "", f"Definition SHA-256: `{row['authored_definition_sha256']}`.", "", "Formal alignment remains unassessed; no equivalence or subclass axiom is emitted. Independent validation was not performed in this packet. Exact normative crosswalks remain separate in #78; #23 owns independent review. Full current curation still needs the other 74 dispositions and publication/readback.", ""]
        result[f"previews/{cid}.md"] = "\n".join(text).encode()
    table = io.StringIO(newline="")
    writer = csv.writer(table, lineterminator="\n")
    writer.writerow(["concept_id", "title", "prior", "disposition", "comparison_terms", "foundation_terms", "rationale", "formal_alignment", "independent_validation"])
    for r in review["concepts"]:
        writer.writerow([r["concept_id"], r["title"], r["previous_disposition"] or "NEW", r["disposition"], ";".join(r["comparison_term_ids"]), ";".join(r["foundation_term_ids"]), r["rationale"], r["formal_alignment"], r["independent_validation"]])
    result["decisions.csv"] = table.getvalue().encode()
    text = ["# N2 — changed and new concept curation", "", "Date: 10 November 2026. Planning target: v0.3.10; issue #85. **The eight-record N2 scope is complete. Full current curation and publication are pending.**", "", "## Result", "", "Selected primary passages were inspected for six changed concepts and two new concepts against model 0.3.2. Each authored definition is preserved verbatim, its complete concept record is hashed, and the prior review and N1 impact inventory are bound. These are assistant-supported documentary decisions, not independent expert ratings or formal alignment axioms.", "", "| Concept | Previous → current documentary disposition | Decision |", "|---|---|---|"]
    for r in review["concepts"]:
        text.append(f"| [{r['title']}](previews/{r['concept_id']}.md) | {r['previous_disposition'] or 'NEW'} → {r['disposition']} | {r['rationale']} |")
    text += ["", "## Primary-source scope", ""]
    for s in review["sources"].values():
        text.append(f"- [{s['title']}]({s['url']}) — {s['version']}; accessed {s['accessed']}. {s['inspection_scope']}")
    text += ["", "Source response-body digests and sizes are in source-access.json; the packet does not redistribute the source documents. Selected term locators and short paraphrases are in review.json. A response digest binds the retrieved page, not every future edition or the truth of a proposed alignment.", "", "## Important interpretation boundaries", "", "- RiskCase remains an analytical item whose existence does not require organizational register acceptance. The revised disposition is a scoped contrast with a generic provenance entity, not an absence or superiority claim.", "- Artifact versions and qualified revision relationships remain distinct. Contextual evidence roles do not follow from a citation alone.", "- OntoUML relator C2 counts the sum of minimum multiplicities. The requirement for two distinct participants comes additionally from Riskium C-26; counting two ends alone does not prove distinctness.", "- Carried source labels such as ISOLATED_CANDIDATE remain verbatim. The existing v0.3.9 publication/qualification receipt provides the later bounded execution context. These historical labels are not silently upgraded, and independent semantic acceptance is not inferred.", "- Exact PRINCE2/ISACA/ISO clause adoption remains #78; no licensed normative full text is claimed inspected here. #23 remains independent. The 0.1.0 curation, scientific source, reader 0.4.9, released v0.3.9 and article 7.2.21 are unchanged.", "", "## Verification", "", "Run from the repository root:", "", "```sh", "python evaluation/releases/v0.3.9/followups/issue85-changed-review/build.py", "python evaluation/releases/v0.3.9/followups/issue85-changed-review/build.py --check", "```", "", "The builder checks the exact eight-record population, source/definition/prior/impact/reader digests, selected locators, identity inheritance and mediation anchors, plus claim boundaries. Eight negative controls include a separately tampered rendered preview. These are documentary integrity controls; the examples in the previews are authored illustrations, not HermiT/SHACL runs. Rebuilding is deterministic. validation.json records the actual local controls and output digests; reproduction.json records the separate byte-equality check. No CI run is invented.", "", "## Next finite steps", "", "1. N3a: confirm the 17 reuse candidates with edition/locator and comparison-scope checks. N3b: recheck the 57 structural-context records in bounded subdomain batches. Only after those 74 decisions can the current 82-concept curation be called complete.", "2. Qualify and select a complete successor curation component, retaining the historical review and its deferrals. Repair any status presentation through the documented source policy rather than editing frozen scientific bytes.", "3. Publish the selected v0.3.10 documentation package and read back affected repository/Wiki/Pages bodies. Close #85 only after this endpoint. N2 preview pages do not count as deployed bodies.", ""]
    result["README.md"] = "\n".join(text).encode()
    return result


def verify_outputs(expected, actual):
    require(set(expected) == set(actual), "rendered output coverage")
    for name in expected:
        require(expected[name] == actual[name], f"rendered body mismatch: {name}")


def controls(review):
    tests = []
    mutations = [
        ("missing_concept", lambda d: d["concepts"].pop(), "eight-record coverage"),
        ("stale_model_digest", lambda d: d["inputs"].update({MODEL: "0" * 64}), "stale input"),
        ("changed_concept_binding", lambda d: d["concepts"][0].update(source_concept_sha256="0" * 64), "concept binding"),
        ("unsupported_equivalence", lambda d: d["concepts"][0].update(formal_alignment="EQUIVALENT"), "unsupported alignment"),
        ("wrong_role_foundation", lambda d: d["concepts"][-1].update(foundation_term_ids=["entity"]), "decision contract"),
        ("missing_grounding_relation", lambda d: d["concepts"][-2].update(relation_ids=["RE-001", "RE-002"]), "use-relation coverage"),
        ("missing_source_locator", lambda d: d["terms"]["usage"].update(locator=""), "source locator"),
    ]
    for name, mutate, reason in mutations:
        mutant = copy.deepcopy(review)
        mutate(mutant)
        try:
            validate(mutant)
        except ValueError as exc:
            require(reason in str(exc), f"wrong rejection for {name}: {exc}")
            tests.append({"control": name, "rejected": True, "reason": str(exc)})
        else:
            raise ValueError(f"mutation escaped: {name}")
    expected = render(review)
    mutant = dict(expected)
    key = "previews/RKM-X01.md"
    mutant[key] = mutant[key].replace(review["concepts"][5]["authored_definition"].encode(), b"Changed definition.", 1)
    require(mutant[key] != expected[key], "preview mutation did not apply")
    try:
        verify_outputs(expected, mutant)
    except ValueError as exc:
        require("rendered body mismatch" in str(exc), "wrong preview rejection")
        tests.append({"control": "changed_preview_definition", "rejected": True, "reason": str(exc)})
    else:
        raise ValueError("preview mutation escaped")
    return tests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    review = load(HERE / "review.json")
    expected = render(review)
    receipt = {
        "status": "PASS_DOCUMENTARY_PACKET_NOT_FULL_CURATION_OR_PUBLICATION",
        "execution": "LOCAL_PYTHON_NOT_CI_OR_ONTOLOGY_ENGINE",
        "review_sha256": sha((HERE / "review.json").read_bytes()),
        "builder_sha256": sha(Path(__file__).read_bytes()),
        "reviewed_records": len(review["concepts"]),
        "remaining_records": 74,
        "negative_controls": controls(review),
        "outputs": {k: sha(v) for k, v in sorted(expected.items())},
    }
    expected["validation.json"] = (json.dumps(receipt, indent=2, ensure_ascii=False) + "\n").encode()
    if args.check:
        actual = {name: (HERE / name).read_bytes() for name in expected}
        actual_preview_names = {str(p.relative_to(HERE)) for p in (HERE / "previews").rglob("*") if p.is_file()}
        require(actual_preview_names == {p for p in expected if p.startswith("previews/")}, "unexpected preview file")
        verify_outputs(expected, actual)
    else:
        for name, body in expected.items():
            target = HERE / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body)
    print(json.dumps({"status": receipt["status"], "mode": "check" if args.check else "build", "records": 8, "negative_controls_rejected": len(receipt["negative_controls"]), "rendered_files": len(expected)}))


if __name__ == "__main__":
    main()
