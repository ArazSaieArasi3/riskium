"""Execute scoped SHACL profiles with retained inputs, exact oracles and receipts."""
import hashlib
import importlib.metadata
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from pyshacl import validate
from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef

from build_shacl import ROOT, RISK, S, SH, VERSION_RULES

EX = Namespace("urn:riskium:fixture:")
OUT = ROOT / "evaluation/shacl"
PROFILE_DIR = ROOT / "ontology/shacl/0.1.0"


def digest(value):
    return hashlib.sha256(value.encode() if isinstance(value, str) else value).hexdigest()


def copy_graph(source):
    g = Graph()
    for t in source:
        g.add(t)
    return g


def normalize_identity(raw):
    """Only asserted sameAs closure; never infer equality from labels or names."""
    parents = {}
    def root(x):
        parents.setdefault(x, x)
        if parents[x] != x:
            parents[x] = root(parents[x])
        return parents[x]
    for a, b in raw.subject_objects(OWL.sameAs):
        if not isinstance(a, URIRef) or not isinstance(b, URIRef):
            raise ValueError("Identity profile accepts named IRIs only")
        ra, rb = root(a), root(b)
        if ra != rb:
            parents[max(ra, rb, key=str)] = min(ra, rb, key=str)
    g = Graph()
    for a, p, b in raw:
        aa, bb = root(a) if a in parents else a, root(b) if b in parents else b
        g.add((aa, p, bb))
    for a, b in list(g.subject_objects(OWL.differentFrom)):
        if a == b:
            raise ValueError("sameAs/differentFrom identity conflict")
        g.add((b, OWL.differentFrom, a))
    return g, {str(k): str(root(k)) for k in sorted(parents, key=str)}


def fixture_specs():
    cases = []
    def add(cid, constraint, triples, expected="CONFORMS", shapes=(), profile="managed",
            published=(), note="", mutation=None):
        g = Graph()
        for a, p, b in triples:
            g.add((a, p, b))
        components = {}
        for shape in shapes:
            component = "ClassConstraintComponent"
            if shape == "C06Distinct" or shape.endswith("Agreement"):
                component = "SPARQLConstraintComponent"
            elif shape in ("C06Bearer", "C06Authority"):
                component = ("ClassConstraintComponent" if "WRONG" in cid else
                             "MaxCountConstraintComponent" if "EXCESS" in cid else "MinCountConstraintComponent")
            elif shape == "C08Anchor": component = "OrConstraintComponent"
            elif shape in ("C08Indicator","C08Scale") and "TWO-" in cid: component = "MaxCountConstraintComponent"
            elif shape == "C09Aboutness": component = "MinCountConstraintComponent"
            elif shape.startswith("C25") and shape.endswith("Link"):
                component = "ClassConstraintComponent" if "UNTYPED-VERSION" in cid else "NodeConstraintComponent"
            components[shape] = component
        cases.append(dict(id=cid, constraint=constraint, profile=profile, raw=g,
                          expected=expected, expected_shapes=sorted(shapes),
                          expected_components=components,
                          publication_targets=list(published), note=note, mutation=mutation))
    def typ(node, cls):
        return (node, RDF.type, RISK[cls])
    r, a, b, alias = EX.relator, EX.bearer, EX.authority, EX.alias
    c06 = [typ(r,"RKM-C052"),typ(a,"RKM-C053"),typ(b,"RKM-C054"),
           (r,RISK["R-56"],a),(r,RISK["R-57"],b),(a,OWL.differentFrom,b)]
    add("S-C06-DISTINCT", "C-06", c06)
    add("S-C06-SUBTYPE-BEARER", "C-06",[x for x in c06 if x!=typ(a,"RKM-C053")]+[typ(a,"RKM-C055")])
    for label,actor,cls,shape in (("BEARER",a,"RKM-C053","C06Bearer"),
                                 ("AUTHORITY",b,"RKM-C054","C06Authority")):
        add("S-C06-WRONG-"+label+"-TYPE","C-06",[x for x in c06 if x!=typ(actor,cls)]+[typ(actor,"RKM-C047")],
            "VIOLATES",[shape])
    add("S-C06-REVERSE-DIFFERENCE", "C-06",
        [t for t in c06 if t[1]!=OWL.differentFrom]+[(b,OWL.differentFrom,a)])
    add("S-C06-UNRESOLVED-NAMES", "C-06", [t for t in c06 if t[1]!=OWL.differentFrom],
        "VIOLATES", ["C06Distinct"], note="Different IRIs alone are insufficient difference evidence.")
    same = [typ(r,"RKM-C052"),typ(a,"RKM-C053"),typ(a,"RKM-C054"),
            (r,RISK["R-56"],a),(r,RISK["R-57"],a)]
    add("S-C06-SAME-ACTOR", "C-06", same, "VIOLATES", ["C06Distinct"])
    add("S-C06-ALIASED-SAME-ACTOR", "C-06",
        same[:-1]+[(r,RISK["R-57"],alias),(alias,OWL.sameAs,a)], "VIOLATES", ["C06Distinct"])
    add("S-C06-ALIAS-CHAIN", "C-06", same[:-1]+[(r,RISK["R-57"],alias),
        (alias,OWL.sameAs,EX.middle),(EX.middle,OWL.sameAs,a)], "VIOLATES", ["C06Distinct"])
    add("S-C06-IDENTITY-CONFLICT", "C-06", c06+[(a,OWL.sameAs,b)], "IDENTITY_CONFLICT")
    add("S-C06-RAW-IDENTITY-CONFLICT", "C-06", c06+[(a,OWL.sameAs,b)], profile="raw",
        note="Raw staging preserves conflicting identity assertions without managed admission.")
    for label, rel, shape in (("BEARER","R-56","C06Bearer"),("AUTHORITY","R-57","C06Authority")):
        add("S-C06-MISSING-"+label,"C-06",[t for t in c06 if not(t[0]==r and t[1]==RISK[rel])],
            "VIOLATES",[shape])
    for label, rel, cls, shape, other in (("BEARER","R-56","RKM-C053","C06Bearer",b),
                                        ("AUTHORITY","R-57","RKM-C054","C06Authority",a)):
        add("S-C06-EXCESS-"+label,"C-06",c06+[typ(EX.extra,cls),(r,RISK[rel],EX.extra),
            (EX.extra,OWL.differentFrom,other)],"VIOLATES",[shape])
    add("S-C06-INFORMATION-ONLY", "C-06", [typ(EX.assignment,"RKM-C051")],
        note="Information alone is outside the relator focus population.")
    add("S-C06-RAW-INCOMPLETE", "C-06", [typ(r,"RKM-C052")], profile="raw")
    add("S-C06-MANAGED-INCOMPLETE", "C-06", [typ(r,"RKM-C052")], "VIOLATES",["C06Bearer","C06Authority"])

    t,i,s = EX.threshold,EX.indicator,EX.scale
    threshold = [typ(t,"RKM-C070")]
    indicator = [typ(i,"RKM-C069"),(t,RISK["RX-025"],i)]
    scale = [typ(s,"RKM-C036"),(t,RISK["RK2-020"],s)]
    add("S-C08-INDICATOR-ONLY","C-08",threshold+indicator)
    add("S-C08-SCALE-ONLY","C-08",threshold+scale)
    add("S-C08-DUAL-STRUCTURAL","C-08",threshold+indicator+scale,
        note="Checks structure only; no unit/scale compatibility verdict.")
    add("S-C08-NO-ANCHOR","C-08",threshold,"VIOLATES",["C08Anchor"])
    add("S-C08-RAW-NO-ANCHOR","C-08",threshold,profile="raw")
    add("S-C08-WRONG-INDICATOR-TYPE","C-08",threshold+[(t,RISK["RX-025"],i),typ(i,"RKM-C036")],
        "VIOLATES",["C08Indicator"])
    add("S-C08-WRONG-SCALE-TYPE","C-08",threshold+[(t,RISK["RK2-020"],s),typ(s,"RKM-C069")],
        "VIOLATES",["C08Scale"])
    add("S-C08-TWO-INDICATORS","C-08",threshold+indicator+[typ(EX.indicator2,"RKM-C069"),
        (t,RISK["RX-025"],EX.indicator2)],"VIOLATES",["C08Indicator"])
    add("S-C08-TWO-SCALES","C-08",threshold+scale+[typ(EX.scale2,"RKM-C036"),
        (t,RISK["RK2-020"],EX.scale2)],"VIOLATES",["C08Scale"])
    add("S-C08-TASK-DUAL-UNKNOWN","C-08",threshold+indicator+scale,"BLOCKED",profile="task-ready",
        note="Compatibility schema is unapproved; cannot claim task-ready admission.")
    add("S-C08-DELETED-ANCHOR-RULE","C-08",threshold,mutation="remove-c08-or",
        note="Control: removing the alternative requirement admits the previously invalid no-anchor graph.")

    d = EX.description
    desc = [typ(d,"RKM-C024")]
    alternatives = (("CASE","RK2-007","RKM-X01"),("PATTERN","RK2-008","RKM-C001"),
                    ("SCENARIO","R-37","RKM-C003"))
    multi = list(desc)
    for label,rel,cls in alternatives:
        triples=[(d,RISK[rel],EX[label]),typ(EX[label],cls)]
        add("S-C09-"+label,"C-09",desc+triples,profile="published",published=[d])
        if label!="CASE":
            add("S-C09-WRONG-"+label+"-TYPE","C-09",desc+[(d,RISK[rel],EX[label]),typ(EX[label],"RKM-C014")],
                "VIOLATES",["C09"+label.title()],profile="published",published=[d])
        multi+=triples
    multi += [(EX.CASE,OWL.differentFrom,EX.PATTERN)]
    add("S-C09-MULTIPLE-TARGETS","C-09",multi,profile="published",published=[d])
    add("S-C09-PUBLISHED-NO-TARGET","C-09",desc,"VIOLATES",["C09Aboutness"],
        profile="published",published=[d])
    add("S-C09-ORDINARY-NO-TARGET","C-09",desc,profile="published",
        note="No publication target declared: C09 has an empty focus population, not a publication pass.")
    add("S-C09-UNTYPED-PUBLISHED","C-09",[(d,RISK["RK2-007"],EX.CASE),typ(EX.CASE,"RKM-X01")],
        "VIOLATES",["C09PublishedDescription"],profile="published",published=[d])
    add("S-C09-WRONG-TARGET-TYPE","C-09",desc+[(d,RISK["RK2-007"],EX.CASE),typ(EX.CASE,"RKM-C001")],
        "VIOLATES",["C09Case"],profile="published",published=[d])
    add("S-C09-DELETED-MINIMUM","C-09",desc,profile="published",published=[d],mutation="remove-c09-min",
        note="Control: removing aboutness minimum admits the previously invalid published graph.")

    integration = list(c06)+threshold+scale+multi
    for label,rel,source,artifact,direct in VERSION_RULES:
        subject,version,art=EX[label+"Assessment"],EX[label+"Version"],EX[label+"Artifact"]
        base=[typ(subject,source),typ(version,"RKM-C015"),typ(art,artifact),
              (subject,RISK[rel],version),(version,RISK["RX-006"],art)]
        integration+=base
        add("S-C25-"+label+"-VALID","C-25",base)
        add("S-C25-"+label+"-UNTYPED-VERSION","C-25",[x for x in base if x!=typ(version,"RKM-C015")],
            "VIOLATES",["C25"+label+"Link"])
        add("S-C25-"+label+"-UNTYPED-SOURCE","C-25",[x for x in base if x!=typ(subject,source)],
            "VIOLATES",["C25"+label])
        add("S-C25-"+label+"-MISSING-TARGET","C-25",
            [x for x in base if x[1]!=RISK["RX-006"]],"VIOLATES",["C25"+label+"Link"])
        add("S-C25-"+label+"-WRONG-KIND","C-25",
            [x for x in base if x!=typ(art,artifact)]+[typ(art,"RKM-C014")],
            "VIOLATES",["C25"+label+"Link"])
        add("S-C25-"+label+"-TWO-TARGETS","C-25",base+[typ(EX.extraArtifact,artifact),
            (version,RISK["RX-006"],EX.extraArtifact)],"VIOLATES",["C25"+label+"Link"])
        add("S-C25-"+label+"-ALIASED-TARGET","C-25",base+[(version,RISK["RX-006"],EX.aliasArtifact),
            (art,OWL.sameAs,EX.aliasArtifact)])
        if direct:
            add("S-C25-"+label+"-DIRECT-MATCH","C-25",base+[(subject,RISK[direct],art)])
            add("S-C25-"+label+"-DIRECT-MISMATCH","C-25",base+[(subject,RISK[direct],EX.other)],
                "VIOLATES",["C25"+label+"Agreement"])
            add("S-C25-"+label+"-DIRECT-ALIAS","C-25",base+[(subject,RISK[direct],EX.aliasArtifact),
                (art,OWL.sameAs,EX.aliasArtifact)])
    add("S-INTEGRATION-ALL-FOUR","INTEGRATION",integration,profile="published",published=[d],
        note="All four rule modules run together on a single positive graph.")
    add("S-INTEGRATION-C09-DEFECT","INTEGRATION",
        [x for x in integration if not (x[0]==d and x[1] in [RISK[a[1]] for a in alternatives])],
        "VIOLATES",["C09Aboutness"],profile="published",published=[d])
    return cases


def execute(spec, taxonomy):
    raw = spec["raw"]
    row={k:v for k,v in spec.items() if k not in ("raw","publication_targets")}
    row["publication_targets"]=[str(x) for x in spec["publication_targets"]]
    row["raw_turtle"]=raw.serialize(format="turtle")
    row["raw_sha256"]=digest(row["raw_turtle"])
    row["engine_executed"]=False
    started=time.monotonic()
    try:
        normalized, mapping=(copy_graph(raw), {}) if spec["profile"]=="raw" else normalize_identity(raw)
    except ValueError as e:
        row.update(observed="IDENTITY_CONFLICT",reason=str(e),violations=[])
    else:
        row["identity_map"]=mapping
        # Explicit taxonomy is support data for SHACL class/subclass checks.
        data=copy_graph(normalized)
        for t in taxonomy: data.add(t)
        shapes=Graph().parse(PROFILE_DIR/(spec["profile"]+".ttl"),format="turtle")
        for target in spec["publication_targets"]:
            normalized_target=URIRef(mapping.get(str(target),str(target)))
            shapes.add((S.C09PublishedDescription,SH.targetNode,normalized_target))
        if spec["mutation"]=="remove-c08-or":
            shapes.remove((S.C08Anchor,SH["or"],None))
        elif spec["mutation"]=="remove-c09-min":
            shapes.remove((S.C09Aboutness,SH.minCount,None))
        row["data_turtle"]=data.serialize(format="turtle")
        row["shapes_turtle"]=shapes.serialize(format="turtle")
        row["data_sha256"]=digest(row["data_turtle"])
        row["shapes_sha256"]=digest(row["shapes_turtle"])
        dual=any(list(normalized.objects(x,RISK["RX-025"])) and list(normalized.objects(x,RISK["RK2-020"]))
                 for x in normalized.subjects(RDF.type,RISK["RKM-C070"]))
        if spec["profile"]=="task-ready" and dual:
            row.update(observed="BLOCKED",reason="C-08 unit/scale compatibility schema not approved",violations=[])
        else:
            conforms, results, text=validate(data_graph=data,shacl_graph=shapes,inference="none",
                advanced=False,meta_shacl=True,abort_on_first=False,allow_infos=False,allow_warnings=False,
                do_owl_imports=False,inplace=False)
            report=next(results.subjects(RDF.type,SH.ValidationReport))
            violations=[]
            for result in results.objects(report,SH.result):
                violations.append({"shape":str(results.value(result,SH.sourceShape)),
                    "component":str(results.value(result,SH.sourceConstraintComponent)),
                    "focus":str(results.value(result,SH.focusNode)),
                    "path":str(results.value(result,SH.resultPath) or "")})
            row.update(observed="CONFORMS" if conforms else "VIOLATES",engine_executed=True,
                       violations=violations,validation_text=text,result_turtle=results.serialize(format="turtle"))
    actual_shapes=sorted({v["shape"].removeprefix(str(S)) for v in row["violations"]})
    actual_components={(v["shape"].removeprefix(str(S)), v["component"].removeprefix(str(SH)))
                       for v in row["violations"]}
    matches=(row["observed"]==spec["expected"] and actual_shapes==spec["expected_shapes"] and
             actual_components==set(spec["expected_components"].items()))
    row["status"]=("BLOCKED" if row["observed"]=="BLOCKED" else "PASS") if matches else "FAIL"
    row["elapsed_ms"]=round((time.monotonic()-started)*1000)
    return row


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    model=json.loads((ROOT/"ontology/riskium-model.json").read_text())
    profile_receipt=json.loads((PROFILE_DIR/"receipt.json").read_text())
    if profile_receipt["source_sha256"]!=digest((ROOT/"ontology/riskium-model.json").read_bytes()):
        raise SystemExit("SHACL source digest mismatch")
    for profile, expected in profile_receipt["profiles_sha256"].items():
        if digest((PROFILE_DIR/(profile+".ttl")).read_bytes())!=expected:
            raise SystemExit("SHACL profile digest mismatch: "+profile)
    taxonomy=Graph()
    for g in model["generalizations"]:taxonomy.add((RISK[g["specific"]],RDFS.subClassOf,RISK[g["general"]]))
    specs=fixture_specs(); rows=[execute(s,taxonomy) for s in specs]
    baseline=[r for r in json.loads((ROOT/"evaluation/coverage-review.json").read_text())["obligation_reviews"]
              if r["engine"]=="SHACL"]
    obligations=[]
    for b in baseline:
        cid=b["source_element"]; relevant=[r for r in rows if r["constraint"]==cid]
        outcome="NOT_RUN"
        if relevant:
            outcome="FAIL" if any(x["status"]=="FAIL" for x in relevant) else ("PARTIAL" if cid=="C-08" else "PASS")
        obligations.append(dict(id=b["obligation_id"],family=b["family"],source_element=cid,
             outcome=outcome,case_ids=[r["id"] for r in relevant],
             scope="Selected explicit-data profile only" if relevant else "Not implemented in this batch"))
    counts={x:sum(o["outcome"]==x for o in obligations) for x in ("PASS","PARTIAL","FAIL","NOT_RUN")}
    report=dict(title="Riskium scoped SHACL execution 0.1.0",source_commit=subprocess.check_output(
        ["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
        generated_at_utc=datetime.now(timezone.utc).isoformat(),runtime_python=sys.version.split()[0],
        engine={p:importlib.metadata.version(p) for p in ("pyshacl","rdflib","owlrl")},
        inputs={p:digest((ROOT/p).read_bytes()) for p in ["ontology/riskium-model.json","evaluation/coverage-review.json",
            "tools/build_shacl.py","tools/run_shacl.py","tools/requirements-shacl.txt",
            "ontology/shacl/0.1.0/receipt.json"]},
        profile_sha256={p.stem:digest(p.read_bytes()) for p in sorted(PROFILE_DIR.glob("*.ttl"))},
        inference_policy="No OWL/RDFS materialization; source subclass taxonomy appended explicitly; asserted sameAs normalization and symmetric differentFrom only; no imports",
        coverage=dict(baseline=359,outcomes=counts,fully_exercised_percent=round(counts["PASS"]/359*100,2),
                      exercised_including_partial_percent=round((counts["PASS"]+counts["PARTIAL"])/359*100,2)),
        cases=rows,obligations=obligations,
        limitations=["C-08 unit/scale compatibility is BLOCKED for dual-anchor task-ready data.",
            "Endpoint-cardinality and catalog-admission baseline families are not executed in this batch.",
            "A declared publication target list is a profile input, not an inferred domain publication fact.",
            "Explicit difference evidence is an admission policy, not proof of real-world actor identity.",
            "These fixtures are synthetic conformance examples, not independent domain validation."])
    (OUT/"report.json").write_text(json.dumps(report,indent=2)+"\n")
    md=f"""# Riskium SHACL execution report — profile 0.1.0

Source commit: `{report['source_commit']}`. This is a **scoped explicit-data validation** run, separate from the [HermiT receipt](../hermit/report.md). The [JSON receipt](report.json) retains each raw graph, normalized data graph, exact shapes graph, publication target list, hashes, validation output and expected source-shape oracle.

## Method and policy

The runner uses pySHACL {report['engine']['pyshacl']}, RDFLib {report['engine']['rdflib']} and OWL-RL package {report['engine']['owlrl']}. OWL-RL is not enabled: inference is `none`, no imports are followed, and only the 66 source subclass triples are explicitly appended as class-check support. Each validation checks the shapes with meta-SHACL. The exact top-level source-shape and constraint-component pairs must match the expected set, so an unrelated violation cannot substitute for the intended negative result. The [profile review](profile-review.md) records policy decisions and source paths.

The source conceptual model is unchanged. Four versioned shape graphs separate raw (no managed-content admission), managed (the selected C-06/C-08/C-25 rules), published (plus C-09 for an externally declared publication target list), and task-ready (same scoped rules, with an explicit compatibility gate). This is not a complete raw/managed/task-ready schema. Publication is deliberately not asserted as a new domain class or inferred from a description's mere existence.

For managed/published/task-ready data, identity normalization uses only asserted `owl:sameAs` equivalence, chooses a stable canonical IRI, preserves combined types and links, and symmetrizes explicit `owl:differentFrom`. A conflict is rejected before SHACL. Raw staging keeps the original identity assertions, including conflicts. Different names alone do not supply actor-distinctness evidence. Both raw and normalized graphs are retained. External identity verification and grounding remain independent obligations.

## Results and coverage

- {sum(r['engine_executed'] for r in rows)} actual SHACL validation runs.
- {sum(r['status']=='PASS' for r in rows)} matching case outcomes, including identity-policy rejection controls.
- {sum(r['status']=='BLOCKED' for r in rows)} BLOCKED case(s), excluded from successful engine executions.
- {sum(r['status']=='FAIL' for r in rows)} unexpected outcomes.

Of **359 predeclared SHACL obligations**, **{counts['PASS']} PASS, {counts['PARTIAL']} PARTIAL, {counts['NOT_RUN']} NOT_RUN**. Scoped PASS coverage is **{report['coverage']['fully_exercised_percent']}%**; exercised coverage including partial work is **{report['coverage']['exercised_including_partial_percent']}%**. The unimplemented 254 endpoint rules, 80 catalog-admission rules and other constraint routes remain in the denominator. More cases for four constraints do not increase this obligation count. Neither percentage measures the semantic correctness of the ontology.

| Constraint | Outcome | What was tested | Remaining boundary |
| --- | --- | --- | --- |
| C-06 | PASS, scoped profile | Named mediation participants, local counts/types, normalized identity and explicit difference evidence | Actual identity, mandate grounding and every other endpoint are separate claims. |
| C-08 | PARTIAL | Indicator-only, scale-only, structural dual anchor, no anchor, wrong types, excess count and deleted-rule mutation | No approved unit/scale compatibility schema; dual-anchor task-ready admission remains BLOCKED. |
| C-09 | PASS, scoped profile | Declared published focus, each alternative, multiple targets, absent/wrong target and deleted-minimum mutation | Publication membership is provided by the caller; meaning of multiple targets still needs domain review. |
| C-25 | PASS, scoped profile | All four version kinds, missing/wrong/multiple targets, alias normalization, direct-reference equality for Context/Method/Scale | The catalog has no direct criteria-reference property to compare; no such property was invented. |

## Full case register

| Case | Profile | Expected | Observed | Verdict | Reported source shapes |
| --- | --- | --- | --- | --- | --- |
"""
    for r in rows:
        md+=f"| `{r['id']}` | {r['profile']} | {r['expected']} | {r['observed']} | {r['status']} | {', '.join(sorted({v['shape'].removeprefix(str(S)) for v in r['violations']})) or '—'} |\n"
    md+="\n## Full baseline register\n\n| Obligation | Source | Outcome |\n| --- | --- | --- |\n"
    for o in obligations:md+=f"| `{o['id']}` | `{o['source_element']}` | {o['outcome']} |\n"
    md+="""
## Reproduce and next work

```sh
python3 -m venv .venv-shacl
.venv-shacl/bin/pip install -r tools/requirements-shacl.txt
.venv-shacl/bin/python tools/build_shacl.py
.venv-shacl/bin/python tools/run_shacl.py
```

The JSON contains exact snapshots for this run, including effective targetNode additions and shape mutations. Base profiles are in `ontology/shacl/0.1.0/`. Next implement the 254 ordered endpoint obligations with deliberate inverse-path controls, then catalog admission and remaining constraint routes. Resolve C-08 compatibility through an approved scalar/unit/scale schema before turning its partial outcome into a pass. Requirements, competency questions, independent semantic review, application history and case adequacy retain separate evidence registers.
"""
    (OUT/"report.md").write_text(md)
    print(json.dumps(dict(cases=len(rows),engine_runs=sum(r["engine_executed"] for r in rows),
        failed=[r["id"] for r in rows if r["status"]=="FAIL"],coverage=report["coverage"])))
    if any(r["status"]=="FAIL" for r in rows):raise SystemExit(1)


if __name__=="__main__":main()
