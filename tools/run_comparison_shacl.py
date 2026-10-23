"""Source-bound C-13/C-18 fixed-oracle executions and immutable receipt replay."""
import argparse
import gzip
import hashlib
import importlib.metadata
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pyshacl import validate
from rdflib import Graph, Literal, Namespace, OWL, RDF, RDFS, URIRef
from rdflib.compare import isomorphic
from build_comparison_shapes import C, SP, OUT as PROFILE_DIR, SELECTORS, digest, prepare, render
from build_shacl import ROOT, RISK, SH
from build_endpoint_shapes import E
from build_admission_shapes import A, compile_request
from run_admission_shacl import fixture_record, graph_snapshot, reconstruct_pair
from run_endpoint_shacl import copy, extract

EX=Namespace("urn:riskium:comparison-fixture:")
OUT=ROOT/"evaluation/shacl/comparison"
REQUEST=(EX.request,EX.leftAssessment,EX.leftResult,EX.rightAssessment,EX.rightResult)
TYPES=((EX.leftAssessment,"RKM-C032"),(EX.rightAssessment,"RKM-C032"),
    (EX.leftResult,"RKM-C034"),(EX.rightResult,"RKM-C034"),(EX.level,"RKM-C038"),
    (EX.scale,"RKM-C036"),(EX.dimension,"RKM-C039"),(EX.scaleVersion,"RKM-C015"),
    (EX.method,"RKM-C035"),(EX.methodVersion,"RKM-C015"),(EX.basis,"RKM-C033"),
    (EX.basisVersion,"RKM-C015"),(EX.context,"RKM-C002"),(EX.contextVersion,"RKM-C015"))
INPUTS=["ontology/riskium-model.json","ontology/derived/riskium.owl.ttl","evaluation/coverage-review.json",
    "evaluation/shacl/coverage-status.json","evaluation/shacl/comparison/profile-policy.json",
    "ontology/shacl/0.7.0/comparison.ttl","ontology/shacl/0.7.0/receipt.json",
    "ontology/shacl/0.2.0/endpoints.ttl","ontology/shacl/0.3.0/admission.ttl",
    "tools/build_comparison_shapes.py","tools/run_comparison_shacl.py","tools/build_coherence_shapes.py",
    "tools/build_shacl.py","tools/run_shacl.py","tools/build_admission_shapes.py","tools/run_admission_shacl.py",
    "tools/run_endpoint_shacl.py","tools/build_endpoint_shapes.py","tools/requirements-shacl.txt"]


def base():
    g=Graph()
    for n,cid in TYPES:g.add((n,RDF.type,RISK[cid]))
    for assessment,result in ((EX.leftAssessment,EX.leftResult),(EX.rightAssessment,EX.rightResult)):
        for p,value in ((RISK["R-13"],result),(RISK["R-46"],EX.method),(RISK["RX-015"],EX.methodVersion),
            (RISK["R-12"],EX.basis),(SP.basisVersion,EX.basisVersion),(RISK["R-45"],EX.context),
            (RISK["RX-014"],EX.contextVersion),(SP.temporalContext,EX.temporal),(SP.source,EX.syntheticSource)):
            g.add((assessment,p,value))
        for p,value in ((RISK["R-14"],EX.scale),(RISK["R-15"],EX.level),(RISK["R-48"],EX.dimension),(RISK["RX-016"],EX.scaleVersion)):
            g.add((result,p,value))
    for triple in ((EX.level,RISK["R-16"],EX.scale),(EX.level,SP.levelScaleVersion,EX.scaleVersion),
        (EX.scale,RISK["RK2-019"],EX.dimension),(EX.method,RISK["R-49"],EX.scale),
        (EX.method,RISK["RK2-018"],EX.dimension),(EX.scaleVersion,RISK["RX-006"],EX.scale),
        (EX.methodVersion,RISK["RX-006"],EX.method),(EX.basisVersion,RISK["RX-006"],EX.basis),
        (EX.contextVersion,RISK["RX-006"],EX.context)):
        g.add(triple)
    return g


def findings(shape,component="SPARQLConstraintComponent",foci=(EX.request,)):
    return [(str(C[shape]),str(SH[component]),str(f)) for f in foci]


def fork_method(g):
    for n,cid in ((EX.otherMethod,"RKM-C035"),(EX.otherMethodVersion,"RKM-C015")):g.add((n,RDF.type,RISK[cid]))
    g.set((EX.rightAssessment,RISK["R-46"],EX.otherMethod));g.set((EX.rightAssessment,RISK["RX-015"],EX.otherMethodVersion))
    for t in ((EX.otherMethodVersion,RISK["RX-006"],EX.otherMethod),(EX.otherMethod,RISK["R-49"],EX.scale),
        (EX.otherMethod,RISK["RK2-018"],EX.dimension),(EX.otherMethod,OWL.differentFrom,EX.method),
        (EX.otherMethodVersion,OWL.differentFrom,EX.methodVersion)):g.add(t)
    return g


def fork_scale(g):
    for n,cid in ((EX.otherScale,"RKM-C036"),(EX.otherScaleVersion,"RKM-C015"),(EX.otherLevel,"RKM-C038")):g.add((n,RDF.type,RISK[cid]))
    for p,n in (("R-14",EX.otherScale),("RX-016",EX.otherScaleVersion),("R-15",EX.otherLevel)):
        g.set((EX.rightResult,RISK[p],n))
    for t in ((EX.otherLevel,RISK["R-16"],EX.otherScale),(EX.otherLevel,SP.levelScaleVersion,EX.otherScaleVersion),
        (EX.otherScaleVersion,RISK["RX-006"],EX.otherScale),(EX.otherScale,RISK["RK2-019"],EX.dimension),
        (EX.method,RISK["R-49"],EX.otherScale),(EX.otherScale,OWL.differentFrom,EX.scale),
        (EX.otherScaleVersion,OWL.differentFrom,EX.scaleVersion)):g.add(t)
    return g


def fixture_specs():
    specs=[]
    def add(cid,g,expected=(),decision="DIRECT_COMPARISON_ADMISSIBLE",mutation=None,integration=False,
            profile="direct-comparison",request=REQUEST,participants=TYPES):
        specs.append(dict(id=cid,raw=copy(g),expected_findings=list(expected),expected_decision=decision,
            mutation=mutation,integration=integration,profile=profile,request=list(request),participants=list(participants)))
    add("COMPARE-MATCH",base())
    for label,node,p,shape,foci,extra in (
        ("SCALE",EX.leftResult,RISK["R-14"],"SelectionScale",(EX.leftResult,),["SelectionScaleDimension"]),
        ("LEVEL",EX.leftResult,RISK["R-15"],"SelectionLevel",(EX.leftResult,),["SelectionLevelScale","SelectionLevelVersion","SelectionLevelVersionTarget"]),
        ("DIMENSION",EX.leftResult,RISK["R-48"],"SelectionDimension",(EX.leftResult,),[]),
        ("SCALE-VERSION",EX.leftResult,RISK["RX-016"],"SelectionScaleVersion",(EX.leftResult,),["SelectionScaleVersionTarget"]),
        ("LEVEL-VERSION",EX.level,SP.levelScaleVersion,"SelectionLevelVersion",(EX.leftResult,EX.rightResult),["SelectionLevelVersionTarget"]),
        ("METHOD",EX.leftAssessment,RISK["R-46"],"LeftMethod",(EX.request,),[]),
        ("METHOD-VERSION",EX.leftAssessment,RISK["RX-015"],"LeftMethodVersion",(EX.request,),["LeftMethodVersionTarget"]),
        ("BASIS",EX.leftAssessment,RISK["R-12"],"LeftBasis",(EX.request,),[]),
        ("BASIS-VERSION",EX.leftAssessment,SP.basisVersion,"LeftBasisVersion",(EX.request,),["LeftBasisVersionTarget"]),
        ("CONTEXT",EX.leftAssessment,RISK["R-45"],"LeftContext",(EX.request,),[]),
        ("CONTEXT-VERSION",EX.leftAssessment,RISK["RX-014"],"LeftContextVersion",(EX.request,),["LeftContextVersionTarget"]),
        ("TIME",EX.leftAssessment,SP.temporalContext,"LeftTemporal",(EX.request,),[]),
        ("SOURCE",EX.leftAssessment,SP.source,"LeftSource",(EX.request,),[])):
        g=base();g.remove((node,p,None));expected=findings(shape,"MinCountConstraintComponent",foci)
        for name in extra:expected+=findings(name,"MinCountConstraintComponent",foci)
        add("MISSING-"+label,g,expected,"NOT_READY")
    for label,p,shape in (("MEMBERSHIP",RISK["R-13"],"LeftMissingMembership"),
        ("SCALE-PERMISSION",RISK["R-49"],"LeftMissingScalePermission"),
        ("DIMENSION-PERMISSION",RISK["RK2-018"],"LeftMissingDimensionPermission")):
        g=base();node=EX.leftAssessment if label=="MEMBERSHIP" else EX.method;g.remove((node,p,None))
        expected=findings(shape)
        if label!="MEMBERSHIP":expected+=findings(shape.replace("Left","Right"))
        add("MISSING-"+label,g,expected,"NOT_READY")
        if label=="MEMBERSHIP":add("DELETED-MEMBERSHIP-RULE",copy(g),mutation=shape)
    g=base();g.add((EX.otherScale,RDF.type,RISK["RKM-C036"]));g.add((EX.otherScale,OWL.differentFrom,EX.scale));g.set((EX.level,RISK["R-16"],EX.otherScale))
    bad_level=copy(g);expected=findings("LevelScaleMismatch",foci=(EX.leftResult,EX.rightResult))
    add("LEVEL-ON-DISTINCT-SCALE",g,expected,"INVALID_SELECTION")
    add("DELETED-LEVEL-SCALE-RULE",copy(g),mutation="LevelScaleMismatch")
    g=copy(bad_level);g.remove((EX.otherScale,OWL.differentFrom,EX.scale))
    add("LEVEL-SCALE-IDENTITY-UNKNOWN",g,findings("LevelScaleUnknown",foci=(EX.leftResult,EX.rightResult)),"NOT_READY")
    g=copy(g);g.add((EX.otherScale,OWL.sameAs,EX.scale));add("LEVEL-SCALE-EXPLICIT-ALIAS",g)
    g=base();g.add((EX.otherVersion,RDF.type,RISK["RKM-C015"]));g.add((EX.otherVersion,RISK["RX-006"],EX.scale));g.add((EX.otherVersion,OWL.differentFrom,EX.scaleVersion));g.set((EX.level,SP.levelScaleVersion,EX.otherVersion))
    add("LEVEL-ON-DISTINCT-VERSION",g,findings("LevelVersionMismatch",foci=(EX.leftResult,EX.rightResult)),"INVALID_SELECTION")
    cross_method=fork_method(base());expected=findings("PairMethodMismatch")+findings("PairMethodVersionMismatch")
    add("CROSS-METHOD",cross_method,expected,"NOT_COMPARABLE")
    g=copy(cross_method);g.remove((EX.otherMethod,OWL.differentFrom,EX.method));g.remove((EX.otherMethodVersion,OWL.differentFrom,EX.methodVersion))
    add("METHOD-IDENTITY-UNKNOWN",g,findings("PairMethodUnknown")+findings("PairMethodVersionUnknown"),"NOT_READY")
    g=copy(g);g.add((EX.otherMethod,OWL.sameAs,EX.method));g.add((EX.otherMethodVersion,OWL.sameAs,EX.methodVersion))
    add("METHOD-EXPLICIT-ALIASES",g)
    g=copy(cross_method);g.add((EX.request,SP.transformation,EX.unexecutedRule))
    add("TRANSFORMATION-HINT-DOES-NOT-ENABLE-DIRECT-COMPARISON",g,expected,"NOT_COMPARABLE")
    g=copy(cross_method)
    for n in (EX.method,EX.otherMethod):g.add((n,RDFS.label,Literal("same method label")))
    for n in (EX.leftResult,EX.rightResult):g.add((n,SP.reportedCode,Literal(5)))
    add("EQUAL-LABELS-AND-NUMBERS-NOT-COMPARABLE",g,expected,"NOT_COMPARABLE")
    cross_scale=fork_scale(base());expected=findings("PairScaleMismatch")+findings("PairScaleVersionMismatch")
    add("CROSS-SCALE",cross_scale,expected,"NOT_COMPARABLE")
    g=copy(cross_scale);g.add((EX.otherDimension,RDF.type,RISK["RKM-C039"]));g.add((EX.otherDimension,OWL.differentFrom,EX.dimension))
    g.set((EX.otherScale,RISK["RK2-019"],EX.otherDimension));g.set((EX.rightResult,RISK["R-48"],EX.otherDimension));g.add((EX.method,RISK["RK2-018"],EX.otherDimension))
    add("CROSS-DIMENSION",g,expected+findings("PairDimensionMismatch"),"NOT_COMPARABLE")
    g=base()
    for n,cid in ((EX.otherVersion,"RKM-C015"),(EX.otherLevel,"RKM-C038")):g.add((n,RDF.type,RISK[cid]))
    for t in ((EX.otherVersion,RISK["RX-006"],EX.scale),(EX.otherVersion,OWL.differentFrom,EX.scaleVersion),
        (EX.otherLevel,RISK["R-16"],EX.scale),(EX.otherLevel,SP.levelScaleVersion,EX.otherVersion)):g.add(t)
    g.set((EX.rightResult,RISK["R-15"],EX.otherLevel));g.set((EX.rightResult,RISK["RX-016"],EX.otherVersion))
    add("SAME-SCALE-DISTINCT-VERSION",g,findings("PairScaleVersionMismatch"),"NOT_COMPARABLE")
    g=base();g.add((EX.otherBasis,RDF.type,RISK["RKM-C033"]));g.add((EX.otherBasisVersion,RDF.type,RISK["RKM-C015"]))
    g.add((EX.otherBasisVersion,RISK["RX-006"],EX.otherBasis));g.add((EX.otherBasis,OWL.differentFrom,EX.basis));g.add((EX.otherBasisVersion,OWL.differentFrom,EX.basisVersion))
    g.set((EX.rightAssessment,RISK["R-12"],EX.otherBasis));g.set((EX.rightAssessment,SP.basisVersion,EX.otherBasisVersion))
    add("CROSS-BASIS",g,findings("PairBasisMismatch")+findings("PairBasisVersionMismatch"),"NOT_COMPARABLE")
    g=base();g.add((EX.otherContext,RDF.type,RISK["RKM-C002"]));g.add((EX.otherContextVersion,RDF.type,RISK["RKM-C015"]))
    for t in ((EX.otherContextVersion,RISK["RX-006"],EX.otherContext),(EX.otherContext,OWL.differentFrom,EX.context),
        (EX.otherContextVersion,OWL.differentFrom,EX.contextVersion)):g.add(t)
    g.set((EX.rightAssessment,RISK["R-45"],EX.otherContext));g.set((EX.rightAssessment,RISK["RX-014"],EX.otherContextVersion))
    add("CROSS-CONTEXT",g,findings("PairContextMismatch")+findings("PairContextVersionMismatch"),"NOT_COMPARABLE")
    g=base();g.set((EX.rightAssessment,SP.temporalContext,EX.otherTemporal));g.add((EX.otherTemporal,OWL.differentFrom,EX.temporal))
    add("CROSS-TEMPORAL-CONTEXT",g,findings("PairTemporalMismatch"),"NOT_COMPARABLE")
    add("DELETED-TEMPORAL-RULE",copy(g),mutation="PairTemporalMismatch")
    g.remove((EX.otherTemporal,OWL.differentFrom,EX.temporal));add("UNRESOLVED-TEMPORAL-CONTEXT",g,findings("PairTemporalUnknown"),"NOT_READY")
    g=copy(g);g.add((EX.otherTemporal,OWL.sameAs,EX.temporal));add("TEMPORAL-EXPLICIT-ALIAS",g)
    g=base();g.add((EX.otherMethod,RDF.type,RISK["RKM-C035"]));g.add((EX.otherMethod,OWL.differentFrom,EX.method));g.set((EX.methodVersion,RISK["RX-006"],EX.otherMethod))
    add("METHOD-VERSION-TARGET-MISMATCH",g,findings("LeftMethodBindingMismatch")+findings("RightMethodBindingMismatch"),"INVALID_SELECTION")
    for label,version,target,cls in (("BASIS",EX.basisVersion,EX.basis,"RKM-C033"),("CONTEXT",EX.contextVersion,EX.context,"RKM-C002")):
        g=base();g.add((EX.otherArtifact,RDF.type,RISK[cls]));g.add((EX.otherArtifact,OWL.differentFrom,target));g.set((version,RISK["RX-006"],EX.otherArtifact))
        title=label.title();add(label+"-VERSION-TARGET-MISMATCH",g,findings("Left"+title+"BindingMismatch")+findings("Right"+title+"BindingMismatch"),"INVALID_SELECTION")
    g=base();g.add((EX.otherScale,RDF.type,RISK["RKM-C036"]));g.add((EX.otherScale,OWL.differentFrom,EX.scale));g.set((EX.scaleVersion,RISK["RX-006"],EX.otherScale))
    expected=findings("ScaleVersionBindingMismatch",foci=(EX.leftResult,EX.rightResult))+findings("LevelVersionBindingMismatch",foci=(EX.leftResult,EX.rightResult))
    add("SCALE-VERSION-TARGET-MISMATCH",g,expected,"INVALID_SELECTION")
    g=base();g.remove((EX.scaleVersion,RISK["RX-006"],None))
    expected=findings("SelectionScaleVersionTarget","MinCountConstraintComponent",(EX.leftResult,EX.rightResult))+findings("SelectionLevelVersionTarget","MinCountConstraintComponent",(EX.leftResult,EX.rightResult))
    add("MISSING-SCALE-VERSION-TARGET",g,expected,"NOT_READY")
    g=base();g.set((EX.leftAssessment,SP.temporalContext,Literal(0)))
    add("ZERO-IS-NOT-MISSING-TIME",g,findings("LeftTemporal","NodeKindConstraintComponent")+findings("PairTemporalUnknown"),"INVALID")
    g=base();g.add((EX.leftAssessment,SP.temporalContext,EX.extraTemporal))
    add("CONFLICTING-TEMPORAL-CONTEXT",g,findings("LeftTemporal","MaxCountConstraintComponent")+findings("PairTemporalUnknown"),"INVALID")
    g=base();g.remove((EX.leftResult,RDF.type,None));add("UNTYPED-SELECTED-RESULT",g,findings("Selection","ClassConstraintComponent",(EX.leftResult,)),"INVALID")
    for label,triple in (("IDENTITY-CONFLICT",(EX.temporal,OWL.sameAs,EX.otherTemporal)),
        ("RESERVED-ALIAS",(SP.temporalContext,OWL.sameAs,SP.source)),
        ("SCHEMA-INJECTION",(EX.fake,RDFS.subClassOf,RISK["RKM-C034"])),
        ("FOCUS-INJECTION",(EX.request,SP.leftAssessment,EX.leftAssessment))):
        g=base();g.add(triple)
        if label=="IDENTITY-CONFLICT":g.add((EX.temporal,OWL.differentFrom,EX.otherTemporal))
        add(label,g,decision="PROFILE_REJECTED")
    add("EMPTY-FOCUS",base(),decision="PROFILE_REJECTED",request=())
    g=base();g.remove((EX.leftAssessment,SP.temporalContext,None));add("RAW-INCOMPLETE",g,decision="STAGING_ONLY",profile="raw")
    add("INTEGRATED-MATCH",base(),integration=True)
    add("INTEGRATED-CROSS-METHOD",copy(cross_method),findings("PairMethodMismatch")+findings("PairMethodVersionMismatch"),"NOT_COMPARABLE",integration=True,
        participants=TYPES+((EX.otherMethod,"RKM-C035"),(EX.otherMethodVersion,"RKM-C015")))
    g=base();g.remove((EX.leftResult,RISK["R-48"],None))
    expected=findings("SelectionDimension","MinCountConstraintComponent",(EX.leftResult,))+[(str(E["R-48-target-count"]),str(SH.MinCountConstraintComponent),str(EX.leftResult))]
    add("INTEGRATED-MISSING-DIMENSION",g,expected,"NOT_READY",integration=True)
    g=base();g.remove((EX.leftResult,RDF.type,None));record=fixture_record("RKM-C034",suffix="-comparison-2",candidate=EX.leftResult)[1]
    expected=findings("Selection","ClassConstraintComponent",(EX.leftResult,))+[(str(A["CandidateType-RKM-C034"]),str(SH.ClassConstraintComponent),str(record))]
    add("INTEGRATED-UNTYPED-RESULT",g,expected,"INVALID",integration=True)
    return specs


def decide(violations,profile):
    if profile=="raw":return "STAGING_ONLY"
    if not violations:return "DIRECT_COMPARISON_ADMISSIBLE"
    def local(s):return s.removeprefix(str(C))
    if any(component!=str(SH.MinCountConstraintComponent) and not local(shape).endswith(("Mismatch","Unknown")) and "Missing" not in local(shape)
        for shape,component,focus in violations):return "INVALID"
    if any(local(s).endswith("Mismatch") and not local(s).startswith("Pair") for s,c,f in violations):return "INVALID_SELECTION"
    if any(local(s).startswith("Pair") and local(s).endswith("Mismatch") for s,c,f in violations):return "NOT_COMPARABLE"
    return "NOT_READY"


def execute(spec,module,receipt,taxonomy,registry):
    row={k:v for k,v in spec.items() if k not in ("raw","request","participants")}
    row["request"]=[str(n) for n in spec["request"]];row["participants"]=[(str(n),cid) for n,cid in spec["participants"]]
    row["raw_graph"]=graph_snapshot(spec["raw"],registry)
    try:data,aliases=prepare(spec["raw"],spec["profile"],spec["request"])
    except ValueError as exc:row.update(observed="PROFILE_REJECTED",error=str(exc),violations=[],engine_executed=False)
    else:
        try:
            shapes=copy(module) if spec["profile"]!="raw" else Graph()
            request=[URIRef(aliases.get(str(n),str(n))) for n in spec["request"]]
            if spec["profile"]!="raw":
                for t in taxonomy:data.add(t)
                for p,n in zip(SELECTORS,request[1:]):data.add((request[0],p,n))
                for group,targets in (("selection",(request[2],request[4])),("comparison",(request[0],))):
                    for owner in receipt["target_owners"][group]:
                        for target in targets:shapes.add((URIRef(owner),SH.targetNode,target))
            if spec["mutation"]:
                name=spec["mutation"];shapes.remove((C[name],SH.sparql,C[name+"Query"]))
            if spec["integration"]:
                rels=("R-14","R-15","R-16","R-48","RX-016","RK2-019")
                endpoints=Graph().parse(ROOT/"ontology/shacl/0.2.0/endpoints.ttl")
                for t in extract(endpoints,[E[r+"-"+end] for r in rels for end in ("source","target")]):shapes.add(t)
                admission=Graph().parse(ROOT/"ontology/shacl/0.3.0/admission.ttl");requests=[]
                for i,(candidate,cid) in enumerate(spec["participants"]):
                    envelope,record,_=fixture_record(cid,suffix="-comparison-"+str(i),candidate=candidate)
                    for t in envelope:
                        if t!=(candidate,RDF.type,RISK[cid]):data.add(t)
                    requests.append((record,cid))
                adm,_,_=compile_request(admission,spec["raw"],requests,"managed-catalog",{cid for n,cid in spec["participants"]})
                for t in adm:shapes.add(t)
                row["endpoint_relations"]=list(rels);row["admission_requests"]=[(str(n),cid) for n,cid in requests]
            row["identity_map"]=aliases;row["data_graph"]=graph_snapshot(data,registry);row["shapes_graph"]=graph_snapshot(shapes,registry)
            conforms,result,text=validate(data_graph=data,shacl_graph=shapes,inference="none",meta_shacl=True,
                do_owl_imports=False,advanced=False,abort_on_first=False,inplace=False)
            root=next(result.subjects(RDF.type,SH.ValidationReport))
            violations=sorted({(str(result.value(n,SH.sourceShape)),str(result.value(n,SH.sourceConstraintComponent)),str(result.value(n,SH.focusNode))) for n in result.objects(root,SH.result)})
            row.update(observed=decide(violations,spec["profile"]),violations=violations,engine_executed=True,
                result_graph=graph_snapshot(result,registry),validation_text=text,conforms=bool(conforms))
        except Exception as exc:row.update(observed="ENGINE_ERROR",error=type(exc).__name__+": "+str(exc),violations=[],engine_executed=False)
    expected=sorted({(s,c,row.get("identity_map",{}).get(f,f)) for s,c,f in spec["expected_findings"]});row["expected_findings"]=expected
    row["status"]="PASS" if row["observed"]==spec["expected_decision"] and row["violations"]==expected and row["observed"]!="ENGINE_ERROR" else "FAIL"
    return row


def run():
    module,compiled=render();receipt=json.loads((PROFILE_DIR/"receipt.json").read_text())
    if not isomorphic(module,Graph().parse(PROFILE_DIR/"comparison.ttl")) or json.dumps(receipt,sort_keys=True)!=json.dumps(dict(compiled,shapes_sha256=digest(PROFILE_DIR/"comparison.ttl")),sort_keys=True):raise ValueError("Shapes/receipt differ from policy builder")
    taxonomy=Graph()
    for gen in json.loads((ROOT/"ontology/riskium-model.json").read_text())["generalizations"]:taxonomy.add((RISK[gen["specific"]],RDFS.subClassOf,RISK[gen["general"]]))
    registry={};rows=[execute(s,module,receipt,taxonomy,registry) for s in fixture_specs()]
    failed=[r for r in rows if r["status"]!="PASS"]
    for r in failed:print(json.dumps({k:r.get(k) for k in ("id","observed","expected_decision","violations","expected_findings","error")}),flush=True)
    if failed:raise ValueError("Comparison fixture/oracle failure")
    baseline=json.loads((ROOT/"evaluation/shacl/coverage-status.json").read_text())
    return dict(schema="riskium-comparison-application-evidence-v1",generated_at_utc=datetime.now(timezone.utc).isoformat(),
        source_commit=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
        source_commit_role="Execution checkout; executed inputs bound by exact hashes; evidence may be committed subsequently.",
        inputs={p:digest(ROOT/p) for p in INPUTS},runtime_python=sys.version.split()[0],
        engine={p:importlib.metadata.version(p) for p in ("pyshacl","rdflib","owlrl")},inference="none",imports=False,
        summary=dict(scenarios=len(rows),engine_executions=sum(r["engine_executed"] for r in rows),
            preflight_rejections=sum(r["observed"]=="PROFILE_REJECTED" for r in rows),
            selected_integration_cases=sum(r["integration"] for r in rows),mutation_controls=sum(bool(r["mutation"]) for r in rows),
            statuses=dict(Counter(r["status"] for r in rows)),decisions=dict(Counter(r["observed"] for r in rows))),
        baseline=dict(obligations=baseline["baseline"],outcomes=baseline["outcomes"],
            selected_rows=[r for r in baseline["obligations"] if r["source_element"] in ("C-13","C-18")]),
        obligations=receipt["obligations"],supplemental_outcome="SCOPED_ALTERNATIVE_SHACL_ROUTE_EXECUTED",
        global_constraint_acceptance="PARTIAL",native_semantics_changed=False,independent_semantic_acceptance=False,
        owner_review_completed=False,graphs=registry,cases=rows)


def verify_saved(stored,fresh):
    for key in ("inputs","summary","baseline","obligations","supplemental_outcome","global_constraint_acceptance","native_semantics_changed","independent_semantic_acceptance","owner_review_completed"):
        if stored[key]!=fresh[key]:raise ValueError("Receipt binding/accounting differs: "+key)
    for key,g in stored["graphs"].items():
        if hashlib.sha256(g["text"].encode()).hexdigest()!=key:raise ValueError("Graph hash mismatch")
    if len(stored["cases"])!=len(fresh["cases"]):raise ValueError("Case population differs")
    keys=("id","profile","request","participants","mutation","integration","expected_decision","expected_findings","violations","observed","status","engine_executed")
    for old,new in zip(stored["cases"],fresh["cases"]):
        if any(json.dumps(old[k],sort_keys=True)!=json.dumps(new[k],sort_keys=True) for k in keys):raise ValueError("Oracle differs: "+new["id"])
        for field in ("raw_graph","data_graph","shapes_graph"):
            if field in new and not isomorphic(Graph().parse(data=stored["graphs"][old[field]]["text"],format="nt"),Graph().parse(data=fresh["graphs"][new[field]]["text"],format="nt")):raise ValueError("Saved input graph differs: "+new["id"])
        if old["engine_executed"]:
            result=Graph().parse(data=stored["graphs"][old["result_graph"]]["text"],format="nt");root=next(result.subjects(RDF.type,SH.ValidationReport))
            actual=sorted({(str(result.value(n,SH.sourceShape)),str(result.value(n,SH.sourceConstraintComponent)),str(result.value(n,SH.focusNode))) for n in result.objects(root,SH.result)})
            if json.dumps(actual)!=json.dumps(old["violations"]) or bool(result.value(root,SH.conforms).toPython())!=old["conforms"]:raise ValueError("Result graph contradicts receipt")


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--check",action="store_true");args=parser.parse_args();report=run();path=OUT/"report.json.gz"
    if args.check:verify_saved(json.loads(gzip.decompress(path.read_bytes())),report)
    else:
        OUT.mkdir(parents=True,exist_ok=True);path.write_bytes(gzip.compress((json.dumps(report,indent=2)+"\n").encode(),mtime=0))
        lines=["# C-13/C-18 selection and comparison — application profile 0.7.0","",
            "**Scoped alternative SHACL route executed; global constraint acceptance remains partial.** Original engine NOT_RUN rows and historical receipts are unchanged. No native/OWL change, ranking, calculation, transformation execution or independent review is established.","",
            "Execution checkout: `"+report["source_commit"]+"`. [Full receipt](report.json.gz), [policy](profile-policy.json), [review and clause dispositions](profile-review.md). Exact executed bytes are bound by all input hashes.","",
            "Summary: "+json.dumps(report["summary"])+".","",
            "The frozen 359-row ledger remains 341 scoped PASS, one PARTIAL and 17 NOT_RUN; this receipt supplements C-13/C-18 routes rather than rewriting that historical checkpoint. Owner-led review is a pending separate release activity, not independent validation.","",
            "| Case | Expected | Observed | Engine executed | Verdict |","| --- | --- | --- | --- | --- |"]
        for r in report["cases"]:lines.append(f"| `{r['id']}` | {r['expected_decision']} | {r['observed']} | {r['engine_executed']} | {r['status']} |")
        lines += ["","Replay: `python tools/run_comparison_shacl.py --check`. This executes fixed fixtures anew and verifies hashes, exact oracles, effective graphs and saved result graphs. Engineering regression calls and preflight rejections are separate from this module's engine count."]
        (OUT/"report.md").write_text("\n".join(lines)+"\n")
    print(json.dumps(report["summary"]),flush=True)


if __name__=="__main__":main()
