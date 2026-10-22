"""Reconcile C-14 source, exports and prior admission evidence without rerunning SHACL."""
import gzip
import hashlib
import json
from pathlib import Path

from rdflib import Graph, OWL, RDF, URIRef

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evaluation/c14-boundary-review.json"
IRI = "https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#"
PAIRS = {
    "RKM-C007": "RKM-X06",  # source / source reference
    "RKM-C010": "RKM-C025",  # outcome / consequence statement
    "RKM-C045": "RKM-X05",  # control / control reference
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    paths = {
        "source": ROOT / "ontology/riskium-model.json",
        "native": ROOT / "ontology/native/riskium.ontouml.json",
        "typed": ROOT / "ontology/derived/typed-core.json",
        "owl": ROOT / "ontology/derived/riskium.owl.ttl",
        "admission": ROOT / "evaluation/shacl/admission/report.json.gz",
        "coverage": ROOT / "evaluation/coverage-review.json",
    }
    model = json.loads(paths["source"].read_text())
    typed = json.loads(paths["typed"].read_text())
    native = {x["id"]: x for x in json.loads(paths["native"].read_text())["elements"]}
    receipt = json.loads(gzip.decompress(paths["admission"].read_bytes()))
    ledger = json.loads(paths["coverage"].read_text())
    owl = Graph().parse(paths["owl"], format="turtle")
    concepts = {x["id"]: x for x in model["concepts"]}
    typed_classes = {x["id"] for x in typed["concepts"]}
    typed_relations = {x["id"] for x in typed["associations"]}
    associations = {x["id"]: x for x in model["associations"]}
    cases = {x["id"]: x for x in receipt["cases"]}
    obligations = {x["source_element"]: x for x in receipt["obligations"]}
    reviewed = {(x["engine"], x["source_element"]): x for x in ledger["obligation_reviews"]}
    constraint = next(x for x in model["constraints"] if x["id"] == "C-14")
    verify(constraint["status"] == "IMPLEMENTED_DESIGN_BOUNDARY", "C-14 source disposition changed")
    verify(receipt["inputs"]["ontology/riskium-model.json"] == digest(paths["source"]), "Admission source drift")
    verify(receipt["inputs"]["evaluation/coverage-review.json"] == digest(paths["coverage"]), "Admission contract drift")
    bridges = {x["id"] for x in associations.values() if x["scope_layer"] == "OPTIONAL_EXTERNAL_BRIDGE"}
    verify(len(bridges) == 7, "Optional bridge inventory changed")
    verify(bridges.isdisjoint(typed_relations), "An optional bridge entered typed core")
    verify(all(native[x]["type"] == "Note" for x in bridges), "An optional bridge entered native formal relations")
    verify(all((URIRef(IRI + x), RDF.type, OWL.ObjectProperty) not in owl for x in bridges),
           "An optional bridge entered OWL")
    verify(set(PAIRS) == {x["id"] for x in model["concepts"] if x["scope_layer"] == "OPTIONAL_PHENOMENON_BOUNDARY"},
           "Optional boundary inventory changed")
    verify(all(g["specific"] not in PAIRS and g["general"] not in PAIRS for g in model["generalizations"]),
           "A boundary entered a generalization")
    rows = []
    for boundary, reference in PAIRS.items():
        verify(concepts[boundary]["scope_layer"] == "OPTIONAL_PHENOMENON_BOUNDARY", "Boundary scope changed")
        verify(concepts[reference]["scope_layer"] == "FORMAL_CORE", "Reference scope changed")
        verify(boundary not in typed_classes and reference in typed_classes, "Typed class mismatch")
        verify(native[boundary]["type"] == "Note" and native[reference]["type"] == "Class", "Native type mismatch")
        verify((URIRef(IRI + boundary), RDF.type, OWL.Class) not in owl, "Boundary exported as OWL class")
        verify((URIRef(IRI + reference), RDF.type, OWL.Class) in owl, "Reference missing from OWL")
        verify(obligations[boundary]["disposition"] == "OPTIONAL_CORE_EXCLUSION" and
               obligations[boundary]["outcome"] == "PASS", "Boundary admission outcome changed")
        verify(obligations[reference]["outcome"] == "PASS", "Reference admission outcome changed")
        selected = [boundary + suffix for suffix in
                    ("-RAW-BOUNDARY", "-CORE-EXCLUSION", "-PROMOTION-ATTEMPT")]
        selected.append(reference + "-MANAGED")
        for case_id in selected:
            case = cases[case_id]
            verify(case["engine_executed"] and case["status"] == "PASS" and
                   {tuple(v) for v in case["violations"]} == {tuple(v) for v in case["expected_findings"]},
                   "Prior admission oracle mismatch: " + case_id)
        verify(reviewed[("SHACL", boundary)]["obligation_id"] == obligations[boundary]["id"],
               "Boundary obligation mismatch")
        verify(reviewed[("SHACL", "C-14")]["obligation_id"] == "SHACL-0632", "C-14 obligation changed")
        rows.append({"boundary": boundary, "reference": reference, "prior_admission_cases": selected,
                     "optional_bridges": sorted(x for x in bridges if boundary in
                                                (associations[x]["source"], associations[x]["target"]))})
    result = {
        "constraint": "C-14", "review_type": "STRUCTURAL_RECONCILIATION_OF_EXISTING_EVIDENCE",
        "source_version": model["version"],
        "inputs_sha256": {str(p.relative_to(ROOT)): digest(p) for p in paths.values()},
        "boundary_reference_pairs": rows, "excluded_bridges": sorted(bridges),
        "prior_admission_cases_checked": sum(len(r["prior_admission_cases"]) for r in rows),
        "new_shacl_executions": 0,
        "shacl_0632_status": "NOT_RUN_IN_FIXED_LEDGER",
        "hermit_0631_status": "NOT_RUN_IN_FIXED_LEDGER",
        "finding": "The three broad catalog notions and seven bridges remain outside formal exports; the three documentary representations remain typed, admitted core classes.",
        "limits": ["Structural exclusion and catalog admission do not prove real-world source, outcome or control existence.",
                   "External bridge/import, reference resolution and independent semantic acceptance require separate review.",
                   "This review reuses prior admission cases; it adds no engine run or PASS to either fixed denominator."],
    }
    rendered = json.dumps(result, indent=2) + "\n"
    OUT.write_text(rendered)
    print(f"C-14 reviewed: {len(rows)} boundaries, {len(bridges)} bridges, "
          f"{result['prior_admission_cases_checked']} prior cases, 0 new engine runs")


if __name__ == "__main__":
    main()
