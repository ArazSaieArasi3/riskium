"""Create the unadjudicated semantic-review inventory; never infer review passes."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def main():
    destination=ROOT/"evaluation/semantic-review-register.json"
    if destination.exists():
        previous=json.loads(destination.read_text())
        if any(g.get("status")!="NOT_REVIEWED" or g.get("independent_ratings") or
               g.get("evidence_locators") or g.get("adjudication") for g in previous.get("groups",[])):
            raise SystemExit("Refusing to overwrite reviewer annotations; reconcile register changes explicitly")
    model_path=ROOT/"ontology/riskium-model.json"
    m=json.loads(model_path.read_text())
    groups=[]
    def add(source, identifier, family, claim, aspects, cohort="core"):
        groups.append(dict(id="SEM-"+identifier,source_element=identifier,family=family,cohort=cohort,
            source_sha256=hashlib.sha256(json.dumps(source,sort_keys=True,ensure_ascii=False).encode()).hexdigest(),
            claim=claim,review_aspects=aspects,status="NOT_REVIEWED",independent_ratings=[],
            evidence_locators=[],adjudication=None))
    for c in m["concepts"]+m["imported_types"]:
        typed=c.get("scope_layer")=="FORMAL_CORE"
        add(c,c["id"],"Concept",c["title"]+": "+c["definition"],
            ["definition and scope","UFO/OntoUML category","identity and dependence","domain placement"],
            "core" if typed else "boundary")
    for r in m["associations"]:
        if r["scope_layer"]=="FORMAL_CORE":
            add(r,r["id"],"Relation",r["predicate"]+": "+r["rationale"],
                ["intended relationship","endpoint kinds and direction","source-end multiplicity",
                 "target-end multiplicity","relation stereotype"])
    for g in m["generalizations"]:
        add(g,g["id"],"Generalization",g["specific"]+" specializes "+g["general"],
            ["subsumption meaning","inherited identity/dependence","stereotype compatibility"])
    for c in m["constraints"]:
        add(c,c["id"],"Constraint",c["statement"],
            ["source-backed intended rule","scope and exceptions","positive and prohibited instances",
             "adequacy of formal or application disposition"])
    for filename, key in (("requirements.json","requirement"),("competency-questions.json","question")):
        for r in json.loads((ROOT/"requirements"/filename).read_text()):
            add(r,r["id"],"Requirement" if key=="requirement" else "Competency question",r[key],
                ["domain/user relevance","expected answer or acceptance oracle","traceability and case evidence"],
                "acceptance")
    if len({g["id"] for g in groups})!=len(groups):raise ValueError("Duplicate semantic group")
    counts={c:sum(x["cohort"]==c for x in groups) for c in ("core","boundary","acceptance")}
    if counts!={"core":295,"boundary":4,"acceptance":20}:raise ValueError(counts)
    report=dict(status="REVIEW_INVENTORY_ONLY_NO_SEMANTIC_RESULTS",model_version=m["version"],
        model_sha256=hashlib.sha256(model_path.read_bytes()).hexdigest(),
        counting_unit="Element review group, not an atomic truth claim; all listed aspects require disposition",
        cohorts=counts,reviewed_core_groups=0,core_review_completion_percent=0,
        overall_semantic_correctness_percent=None,
        limitation="No independent ratings are recorded in this new register. Zero completion does not mean zero correctness.",
        groups=groups)
    destination.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(dict(cohorts=counts,total=len(groups),semantic_correctness=None)))


if __name__=="__main__":main()
