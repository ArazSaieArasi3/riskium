"""Execute C-11/C-12 records with external focus and exact SHACL oracles."""
import importlib.metadata
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone

from pyshacl import validate
from rdflib import Graph, Literal, Namespace, OWL, RDF, RDFS, URIRef, XSD

from build_qualification_shapes import Q, S, DC, OUT as PROFILE, digest, render
from build_shacl import ROOT, RISK, SH
from build_admission_shapes import A, AP, compile_request
from build_endpoint_shapes import E
from run_admission_shacl import fixture_record, graph_snapshot, reconstruct_pair
from run_endpoint_shacl import copy, extract
from run_shacl import normalize_identity

EX = Namespace("urn:riskium:qualification:")
OUT = ROOT / "evaluation/shacl/qualification"


def vocab(cid="RKM-C019", suffix="", scheme=None, edition=None, code="A", label="Same label"):
    g = Graph(); record = EX["v-record-" + cid + suffix]; term = EX["v-term-" + cid + suffix]
    scheme = scheme or EX.scheme; edition = edition or EX.edition
    for triple in ((record, Q.candidate, term), (record, Q.scheme, scheme), (record, Q.edition, edition),
                   (record, Q.localCode, Literal(code)), (record, DC.title, Literal(label)),
                   (term, RDF.type, RISK[cid])): g.add(triple)
    model = json.loads((ROOT / "ontology/riskium-model.json").read_text())
    _, classified = __import__("build_qualification_shapes").vocabulary_ids(model)
    if cid in classified:
        g.add((term, RISK["R-05"], scheme)); g.add((scheme, RDF.type, RISK["RKM-C018"]))
    return g, record, term


def evidence(role=Q.Support, suffix=""):
    g = Graph(); record = EX["e-record" + suffix]; ref = EX["e-ref" + suffix]
    item = EX["item" + suffix]; target = EX["target" + suffix]
    for triple in ((record, Q.candidate, ref), (record, Q.item, item), (record, Q.target, target),
                   (record, Q.role, role), (record, DC.source, EX["source" + suffix]),
                   (ref, RDF.type, RISK["RKM-C065"]), (item, RDF.type, RISK["RKM-C066"]),
                   (target, RDF.type, RISK["RKM-C014"]), (ref, RISK["RX-021"], item)):
        g.add(triple)
    if role == Q.Support: g.add((ref, RISK["R-68"], target))
    return g, record, ref


def findings(shape, component, *records):
    return [(str(S[shape]), str(SH[component]), str(r)) for r in records]


def specs(vocab_ids, classified):
    cases = []
    def add(name, constraint, graph, requests, expected=(), profile="managed", mutation=None, integration=False):
        cases.append(dict(id=name, constraint=constraint, raw=graph, requests=requests,
                          expected_findings=list(expected), profile=profile, mutation=mutation,
                          integration=integration))
    for cid in vocab_ids:
        g, r, _ = vocab(cid); add("VOC-" + cid, "C-11", g, [(r, cid)])
    g, r, t = vocab(); add("VOC-RAW-INCOMPLETE", "C-11", Graph(), [(r, "RKM-C019")], profile="raw")
    for name, predicate, shape in (("SCHEME", Q.scheme, "VocabScheme"), ("EDITION", Q.edition, "VocabEdition"),
                                   ("CODE", Q.localCode, "VocabCode"), ("LABEL", DC.title, "VocabLabel")):
        bad = copy(g); bad.remove((r, predicate, None))
        add("VOC-MISSING-" + name, "C-11", bad, [(r, "RKM-C019")], findings(shape, "MinCountConstraintComponent", r))
    bad = copy(g); bad.set((r, Q.localCode, Literal("   ")))
    add("VOC-BLANK-CODE", "C-11", bad, [(r, "RKM-C019")], findings("VocabCode", "PatternConstraintComponent", r))
    bad = copy(g); bad.remove((t, RISK["R-05"], None))
    add("VOC-SCHEME-MISMATCH", "C-11", bad, [(r, "RKM-C019")], findings("ClassifiedTerm", "SPARQLConstraintComponent", r))
    add("VOC-DELETED-AGREEMENT", "C-11", bad, [(r, "RKM-C019")], mutation="delete-scheme-agreement")
    g2, r2, _ = vocab(suffix="-other"); pair = copy(g)
    for triple in g2: pair.add(triple)
    add("VOC-DUPLICATE-KEY", "C-11", pair, [(r, "RKM-C019"), (r2, "RKM-C019")],
        findings("VocabularyRecord", "SPARQLConstraintComponent", r, r2))
    add("VOC-DELETED-UNIQUENESS", "C-11", pair, [(r, "RKM-C019"), (r2, "RKM-C019")], mutation="delete-uniqueness")
    for label, scheme, edition in (("OTHER-SCHEME", EX.otherScheme, EX.edition),
                                    ("OTHER-EDITION", EX.scheme, EX.otherEdition)):
        another, ar, _ = vocab(suffix="-other", scheme=scheme, edition=edition)
        both = copy(g)
        for triple in another: both.add(triple)
        add("VOC-" + label, "C-11", both, [(r, "RKM-C019"), (ar, "RKM-C019")])
    bad = copy(g); bad.add((t, OWL.sameAs, EX.termAlias)); bad.add((r, Q.candidate, EX.termAlias))
    add("VOC-ASSERTED-ALIAS", "C-11", bad, [(r, "RKM-C019")])
    bad = copy(g); bad.set((r, Q.candidate, EX.noType))
    add("VOC-WRONG-CANDIDATE", "C-11", bad, [(r, "RKM-C019")],
        findings("VocabCandidate", "ClassConstraintComponent", r) + findings("ClassifiedTerm", "SPARQLConstraintComponent", r))
    for role, name in ((Q.Support,"SUPPORT"),(Q.Challenge,"CHALLENGE"),(Q.Context,"CONTEXT")):
        eg, er, _ = evidence(role); add("EVIDENCE-" + name, "C-12", eg, [(er, "RKM-C065")])
    eg, er, ref = evidence()
    add("EVIDENCE-RAW", "C-12", Graph(), [(er, "RKM-C065")], profile="raw")
    for label, predicate, shape in (("ROLE",Q.role,"EvidenceRole"),("SOURCE",DC.source,"EvidenceSource"),
                                     ("ITEM",Q.item,"EvidenceItem"),("TARGET",Q.target,"EvidenceTarget")):
        bad = copy(eg); bad.remove((er, predicate, None))
        add("EVIDENCE-MISSING-" + label,"C-12",bad,[(er,"RKM-C065")],findings(shape,"MinCountConstraintComponent",er))
    bad=copy(eg);bad.set((er,Q.role,Q.Unknown))
    add("EVIDENCE-UNKNOWN-ROLE","C-12",bad,[(er,"RKM-C065")],findings("EvidenceRole","InConstraintComponent",er))
    bad=copy(eg);bad.set((er,DC.source,Literal("source text")))
    add("EVIDENCE-LITERAL-SOURCE","C-12",bad,[(er,"RKM-C065")],findings("EvidenceSource","NodeKindConstraintComponent",er))
    bad=copy(eg);bad.remove((ref,RISK["RX-021"],None))
    add("EVIDENCE-MISSING-ITEM-PAIR","C-12",bad,[(er,"RKM-C065")],findings("EvidenceRecord","SPARQLConstraintComponent",er))
    add("EVIDENCE-DELETED-ITEM-RULE","C-12",bad,[(er,"RKM-C065")],mutation="delete-item-agreement")
    bad=copy(eg);bad.remove((ref,RISK["R-68"],None))
    add("EVIDENCE-SUPPORT-WITHOUT-PAIR","C-12",bad,[(er,"RKM-C065")],findings("EvidenceRecord","SPARQLConstraintComponent",er))
    add("EVIDENCE-DELETED-ROLE-RULE","C-12",bad,[(er,"RKM-C065")],mutation="delete-role-agreement")
    bad=copy(eg);bad.set((er,Q.role,Q.Challenge))
    add("EVIDENCE-CHALLENGE-WITH-SUPPORT-PAIR","C-12",bad,[(er,"RKM-C065")],findings("EvidenceRecord","SPARQLConstraintComponent",er))
    bad=copy(eg);bad.set((er,Q.item,EX.otherItem));bad.add((EX.otherItem,RDF.type,RISK["RKM-C066"]))
    add("EVIDENCE-OTHER-ITEM","C-12",bad,[(er,"RKM-C065")],findings("EvidenceRecord","SPARQLConstraintComponent",er))
    bad=copy(eg);bad.set((er,Q.target,EX.otherTarget));bad.add((EX.otherTarget,RDF.type,RISK["RKM-C014"]))
    add("EVIDENCE-OTHER-TARGET","C-12",bad,[(er,"RKM-C065")],findings("EvidenceRecord","SPARQLConstraintComponent",er))
    add("VOC-INTEGRATED", "C-11", g, [(r,"RKM-C019")], integration=True)
    add("EVIDENCE-INTEGRATED", "C-12", eg, [(er,"RKM-C065")], integration=True)
    return cases


def execute(spec, module, taxonomy, classified, registry):
    row = {k:v for k,v in spec.items() if k not in ("raw","requests")}
    row["requests"]=[(str(record),cid) for record,cid in spec["requests"]]
    row["raw_graph"]=graph_snapshot(spec["raw"],registry)
    try:
        if not spec["requests"]: raise ValueError("Nonempty external focus is required")
        if spec["profile"] == "raw": data=copy(spec["raw"]); shapes=Graph(); mapping={}
        elif spec["profile"] == "managed":
            for p in (RDFS.subClassOf,RDFS.subPropertyOf,OWL.imports,OWL.equivalentClass,OWL.equivalentProperty):
                if any(spec["raw"].triples((None,p,None))): raise ValueError("Instance schema/import assertion")
            reserved=tuple(map(str,(RISK,Q,S,AP,A,RDF,RDFS,OWL,SH,XSD)))
            for p in (OWL.sameAs,OWL.differentFrom):
                for left,right in spec["raw"].subject_objects(p):
                    if str(left).startswith(reserved) or str(right).startswith(reserved):
                        raise ValueError("Reserved vocabulary alias")
            data,mapping=normalize_identity(spec["raw"])
            for triple in taxonomy:data.add(triple)
            shapes=copy(module)
            # No data declaration chooses a weaker shape: requests are independent of the graph.
            for record,cid in spec["requests"]:
                record=URIRef(mapping.get(str(record),str(record)))
                if cid in classified:
                    for owner in (S.VocabularyRecord,S.ClassifiedTerm):shapes.add((owner,SH.targetNode,record))
                elif cid=="RKM-C065":shapes.add((S.EvidenceRecord,SH.targetNode,record))
                else:shapes.add((S.VocabularyRecord,SH.targetNode,record))
            for mut,owner,query in (("delete-uniqueness",S.VocabularyRecord,S.DuplicateKey),
                ("delete-scheme-agreement",S.ClassifiedTerm,S.SchemeAgreement),
                ("delete-item-agreement",S.EvidenceRecord,S.ItemAgreement),
                ("delete-role-agreement",S.EvidenceRecord,S.RoleAgreement)):
                if spec["mutation"]==mut:shapes.remove((owner,SH.sparql,query))
            if spec["integration"]:
                endpoint=Graph().parse(ROOT/"ontology/shacl/0.2.0/endpoints.ttl")
                ids=("R-05",) if spec["constraint"]=="C-11" else ("R-68","RX-021")
                for triple in extract(endpoint,[E[r+"-"+end] for r in ids for end in ("source","target")]):shapes.add(triple)
                admission=Graph().parse(ROOT/"ontology/shacl/0.3.0/admission.ttl")
                participants=[(x,str(cls).split("#")[-1]) for x,cls in spec["raw"].subject_objects(RDF.type)
                    if cls in {RISK[c] for c in ("RKM-C019","RKM-C018","RKM-C065","RKM-C066","RKM-C014")}]
                requests=[]
                for i,(candidate,cid) in enumerate(participants):
                    envelope,record,_=fixture_record(cid,suffix="-qualification-"+str(i),candidate=candidate)
                    for triple in envelope:data.add(triple)
                    requests.append((record,cid))
                adm,_,_=compile_request(admission,spec["raw"],requests,"managed-catalog",{x[1] for x in participants})
                for triple in adm:shapes.add(triple)
                row["integration_relations"]=ids
        else:raise ValueError("Unsupported profile")
        row["identity_map"]=mapping
        row["data_graph"]=graph_snapshot(data,registry);row["shapes_graph"]=graph_snapshot(shapes,registry)
        conforms,result,validation_text=validate(data_graph=data,shacl_graph=shapes,inference="none",meta_shacl=True,
            do_owl_imports=False,advanced=False,abort_on_first=False,inplace=False)
        root=next(result.subjects(RDF.type,SH.ValidationReport))
        observed={(str(result.value(n,SH.sourceShape)),str(result.value(n,SH.sourceConstraintComponent)),
                    str(result.value(n,SH.focusNode))) for n in result.objects(root,SH.result)}
        expected={(a,b,mapping.get(c,c)) for a,b,c in spec["expected_findings"]}
        row.update(status="PASS" if observed==expected and bool(conforms)==(not expected) else "FAIL",
            observed="CONFORMS" if conforms else "VIOLATES",violations=sorted(observed),expected_findings=sorted(expected),
            result_graph=graph_snapshot(result,registry),validation_text=validation_text,engine_executed=True)
    except Exception as exc:row.update(status="ERROR",error=type(exc).__name__+": "+str(exc),engine_executed=False)
    return row


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    source=PROFILE/"qualification.ttl"; receipt=json.loads((PROFILE/"receipt.json").read_text())
    if (receipt["source_sha256"],receipt["contract_sha256"],receipt["shapes_sha256"]) != (
        digest(ROOT/"ontology/riskium-model.json"),digest(ROOT/"evaluation/coverage-review.json"),digest(source)):
        raise SystemExit("Source or shape digest mismatch")
    model=json.loads((ROOT/"ontology/riskium-model.json").read_text()); taxonomy=Graph()
    for g in model["generalizations"]:taxonomy.add((RISK[g["specific"]],RDFS.subClassOf,RISK[g["general"]]))
    module=Graph().parse(source);registry={};rows=[]
    for case in specs(receipt["vocabulary_classes"],set(receipt["classified_term_classes"])):
        row=execute(case,module,taxonomy,set(receipt["classified_term_classes"]),registry);rows.append(row)
        if row["status"]!="PASS":print(json.dumps({k:row.get(k) for k in ("id","status","error","violations","expected_findings")}),flush=True)
    obligations=[]
    for item in receipt["obligations"]:
        cases=[r for r in rows if r["constraint"]==item["source_element"]]
        obligations.append(dict(**item,outcome="PASS" if cases and all(r["status"]=="PASS" for r in cases) else "FAIL",
            case_ids=[r["id"] for r in cases]))
    inputs=["ontology/riskium-model.json","ontology/derived/riskium.owl.ttl","evaluation/coverage-review.json",
        "ontology/shacl/0.5.0/qualification.ttl","ontology/shacl/0.5.0/receipt.json",
        "tools/build_qualification_shapes.py","tools/run_qualification_shacl.py","tools/requirements-shacl.txt"]
    counts=Counter(r["status"] for r in rows)
    report=dict(title="Vocabulary and evidence qualification 0.5.0",source_commit=subprocess.check_output(
        ["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),generated_at_utc=datetime.now(timezone.utc).isoformat(),
        runtime_python=sys.version.split()[0],engine={p:importlib.metadata.version(p) for p in ("pyshacl","rdflib","owlrl")},
        inputs={p:digest(ROOT/p) for p in inputs},profiles={"raw":"staging only", "managed":"external nonempty focus; asserted aliases; source taxonomy; inference none"},
        coverage=dict(total=2,passed=sum(o["outcome"]=="PASS" for o in obligations),cases=len(rows),statuses=dict(counts)),
        graphs=registry,cases=rows,obligations=obligations,
        limitations=["Application identity key does not prove domain identity or scheme governance.",
            "Role-qualified provenance does not establish truth, adequacy, endorsement or real-world interpretation.",
            "Selected endpoint/catalog integration does not establish complete managed-profile admission."])
    (OUT/"report.json").write_text(json.dumps(report,indent=2)+"\n")
    md=f"""# Scheme-qualified vocabulary and role-qualified evidence — module 0.5.0

Source commit `{report['source_commit']}`. **{report['coverage']['passed']}/2 scoped obligations PASS**. **{len(rows)} actual SHACL validations**, {counts.get('FAIL',0)} unexpected outcomes and {counts.get('ERROR',0)} errors. [Policy](profile-review.md) and [full receipt](report.json) define the exact limits.

Every selected VocabularyConcept subtype receives a managed record with explicit scheme, edition, local code and descriptive label. Only ClassificationTerm descendants require the matching `belongsToScheme` pair. An EvidenceReference record identifies source, item, target and Support/Challenge/Context role; the explicit `pointsToEvidence` and role-appropriate support pair are checked. These are application metadata and graph checks. A source link and even a Support role never prove the target's truth.

Each case preserves raw/effective data, shapes and result graph snapshots, identity map, input digests and exact shape/component/focus oracle. Raw means staging only. Inference is none; no imports or truth repair. Selected endpoint and catalog cases are included, while full managed integration remains #5 and independent interpretation remains #7.

| Case | Constraint | Expected | Observed | Result |
| --- | --- | --- | --- | --- |
"""
    for row in rows:md+=f"| `{row['id']}` | {row['constraint']} | {'VIOLATES' if row['expected_findings'] else 'CONFORMS'} | {row.get('observed','ERROR')} | {row['status']} |\n"
    md+="\nReproduce with `tools/build_qualification_shapes.py`, `tools/run_qualification_shacl.py` and `tools/summarize_shacl.py` in the pinned SHACL environment.\n"
    (OUT/"report.md").write_text(md)
    print(json.dumps(report["coverage"]),flush=True)
    if any(r["status"]!="PASS" for r in rows):raise SystemExit(1)


if __name__=="__main__":main()
