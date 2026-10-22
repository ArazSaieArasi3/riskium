"""Run the complete ordered-endpoint contract, local controls and paired integration."""
import hashlib
import importlib.metadata
import json
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timezone

from pyshacl import validate
from rdflib import BNode, Graph, Literal, Namespace, RDF, RDFS, URIRef
from rdflib.compare import to_canonical_graph

from build_shacl import ROOT, RISK, SH
from build_endpoint_shapes import E, OUT as PROFILE_DIR
from run_shacl import normalize_identity

EX=Namespace("urn:riskium:endpoint-fixture:")
OUT=ROOT/"evaluation/shacl/endpoints"


def sha(data):
    return hashlib.sha256(data.encode() if isinstance(data,str) else data).hexdigest()


def copy(g):
    result=Graph()
    for t in g:result.add(t)
    return result


def extract(module, shape_ids):
    g=Graph();pending=list(shape_ids);seen=set()
    while pending:
        subject=pending.pop()
        if subject in seen:continue
        seen.add(subject)
        for triple in module.triples((subject,None,None)):
            g.add(triple);obj=triple[2]
            if isinstance(obj,BNode) or (obj,RDF.type,SH.PropertyShape) in module:
                pending.append(obj)
    return g


def graph_snapshot(g, registry):
    text="\n".join(sorted(to_canonical_graph(g).serialize(format="nt").splitlines()))+"\n"
    key=sha(text)
    registry.setdefault(key,dict(format="nt",text=text))
    return key


def fixture_specs(module, reviewed):
    specs=[];by_element={r["source_element"]:r for r in reviewed}
    def add(cid, elements, family, raw, shapes, expected=(), focus=None, mutation=None, note="", focus_by_shape=None):
        expected_foci={str(k):str(v) for k,v in (focus_by_shape or {}).items()}
        if focus is not None:expected_foci.update({str(a):str(focus) for a,_ in expected})
        if any(str(a) not in expected_foci for a,_ in expected):raise ValueError("Missing negative focus oracle")
        specs.append(dict(id=cid,source_elements=elements,family=family,raw=raw,shapes=shapes,
            expected=[(str(a),str(b)) for a,b in expected],expected_focus=str(focus) if focus is not None else None,
            expected_findings=[(str(a),str(b),expected_foci[str(a)]) for a,b in expected],
            mutation=mutation,note=note))
    for row in reviewed:
        element=row["source_element"];rid,end=element.split(":");contract=row["cases"]
        focus=EX[element+"-focus"];p=RISK[rid];node=E[rid+"-"+end];ps=E[rid+"-"+end+"-count"]
        shape=extract(module,[node]);shape.remove((node,SH.targetClass,None));shape.add((node,SH.targetNode,focus))
        lo,hi=contract["minimum"],contract["maximum"]
        def data(n, reverse=False, blank=False):
            g=Graph();g.add((focus,RDF.type,RISK[contract["focus_class"]]))
            for i in range(n):
                other=BNode("value-"+str(i)) if blank else EX[element+"-value-"+str(i)]
                g.add((other,RDF.type,RISK[contract["counted_class"]]))
                direct=(contract["property_path"]=="direct") != reverse
                g.add((focus,p,other) if direct else (other,p,focus))
            return g
        valid=list(contract["valid_counts"])
        if hi is None and 5 not in valid:valid.append(5)
        for n in valid:
            add("EP-"+element+"-VALID-"+str(n),[element],"Valid cardinality",data(n),copy(shape),focus=focus)
        for side,n,component,pred,relaxed in (("MIN",lo-1,SH.MinCountConstraintComponent,SH.minCount,0),
                                             ("MAX",(hi+1 if hi is not None else -1),SH.MaxCountConstraintComponent,SH.maxCount,
                                              hi+1 if hi is not None else None)):
            if (side=="MIN" and lo==0) or (side=="MAX" and hi is None):continue
            add("EP-"+element+"-BELOW-"+side if side=="MIN" else "EP-"+element+"-ABOVE-"+side,
                [element],"Invalid cardinality",data(n),copy(shape),[(ps,component)],focus)
            mutant=copy(shape);mutant.set((ps,pred,Literal(relaxed)))
            add("EP-"+element+"-RELAXED-"+side,[element],"Bound mutation",data(n),mutant,focus=focus,
                mutation="relax-"+side.lower(),note="The violating graph becomes conforming after the relevant bound is relaxed.")
        # A hasValue sentinel makes both directions observable even for 0..*.
        witness=data(1);decoy=EX[element+"-reverse-decoy"]
        witness.add((focus,p,decoy) if contract["property_path"]=="inverse" else (decoy,p,focus))
        control=copy(shape);control.add((ps,SH.hasValue,EX[element+"-value-0"]))
        add("EP-"+element+"-PATH-WITNESS",[element],"Path witness",witness,control,focus=focus,
            note="Supplementary hasValue sentinel; not a domain cardinality axiom.")
        reversed_shape=copy(control);old_path=reversed_shape.value(ps,SH.path)
        if contract["property_path"]=="inverse":
            reversed_shape.set((ps,SH.path,p));reversed_shape.remove((old_path,None,None))
        else:
            inverse=BNode("mutated-inverse");reversed_shape.set((ps,SH.path,inverse))
            reversed_shape.add((inverse,SH.inversePath,p))
        add("EP-"+element+"-REVERSED-PATH",[element],"Path mutation",witness,reversed_shape,
            [(ps,SH.HasValueConstraintComponent)],focus,mutation="reverse-path",
            note="Both directions have one value; only the required witness distinguishes them.")
        if hi is not None:
            aliases=data(2);aliases.add((EX[element+"-value-0"],URIRef("http://www.w3.org/2002/07/owl#sameAs"),
                                        EX[element+"-value-1"]))
            add("EP-"+element+"-ALIASED-VALUES",[element],"Identity boundary",aliases,copy(shape),focus=focus)
            add("EP-"+element+"-ONE-BLANK",[element],"Blank-node boundary",data(1,blank=True),copy(shape),focus=focus)
            add("EP-"+element+"-TWO-BLANKS",[element],"Blank-node boundary",data(2,blank=True),copy(shape),
                [(ps,SH.MaxCountConstraintComponent)],focus)
    # Exercise original targetClass populations and both ends together for every relation.
    for rid in sorted({e.split(":")[0] for e in by_element}):
        rows=[by_element[rid+":"+end] for end in ("source","target")]
        shapes=extract(module,[E[rid+"-source"],E[rid+"-target"]])
        source,target=EX[rid+"-pair-source"],EX[rid+"-pair-target"];p=RISK[rid]
        base=Graph();base.add((source,RDF.type,RISK[rows[1]["cases"]["focus_class"]]))
        base.add((target,RDF.type,RISK[rows[0]["cases"]["focus_class"]]));base.add((source,p,target))
        elements=[r["source_element"] for r in rows]
        add("PAIR-"+rid+"-VALID",elements,"Paired-end integration",base,shapes)
        minimums=[(E[rid+"-"+end+"-count"],SH.MinCountConstraintComponent)
                  for end,row in zip(("source","target"),rows) if row["cases"]["minimum"]>0]
        if minimums:
            missing=copy(base);missing.remove((source,p,target))
            add("PAIR-"+rid+"-MISSING",elements,"Paired-end integration",missing,copy(shapes),minimums,
                focus_by_shape={E[rid+"-source-count"]:target,E[rid+"-target-count"]:source})
        for end,row in zip(("source","target"),rows):
            if row["cases"]["maximum"] is None:continue
            excess=copy(base);extra=EX[rid+"-extra-"+end]
            if end=="source":
                excess.add((extra,RDF.type,RISK[rows[1]["cases"]["focus_class"]]));excess.add((extra,p,target))
            else:
                excess.add((extra,RDF.type,RISK[rows[0]["cases"]["focus_class"]]));excess.add((source,p,extra))
            add("PAIR-"+rid+"-EXCESS-"+end,elements,"Paired-end integration",excess,copy(shapes),
                [(E[rid+"-"+end+"-count"],SH.MaxCountConstraintComponent)],
                focus_by_shape={E[rid+"-"+end+"-count"]:target if end=="source" else source})
    return specs


def execute(spec,taxonomy,registry):
    row={k:v for k,v in spec.items() if k not in ("raw","shapes")}
    row["raw_graph"]=graph_snapshot(spec["raw"],registry)
    normalized,mapping=normalize_identity(spec["raw"]);data=copy(normalized)
    for t in taxonomy:data.add(t)
    row["identity_map"]=mapping;row["normalized_graph"]=graph_snapshot(normalized,registry)
    row["shapes_graph"]=graph_snapshot(spec["shapes"],registry)
    start=time.monotonic()
    try:
        conforms,results,text=validate(data_graph=data,shacl_graph=spec["shapes"],inference="none",
            meta_shacl=True,advanced=False,do_owl_imports=False,abort_on_first=False,inplace=False)
        report=next(results.subjects(RDF.type,SH.ValidationReport))
        findings=[]
        for item in results.objects(report,SH.result):
            findings.append(dict(shape=str(results.value(item,SH.sourceShape)),
                component=str(results.value(item,SH.sourceConstraintComponent)),
                focus=str(results.value(item,SH.focusNode))))
        actual={(x["shape"],x["component"]) for x in findings}
        expected={tuple(x) for x in spec["expected"]}
        finding_matches={(x["shape"],x["component"],x["focus"]) for x in findings}=={tuple(x) for x in spec["expected_findings"]}
        focus_matches=not spec["expected_focus"] or all(x["focus"]==spec["expected_focus"] for x in findings)
        matched=actual==expected and bool(conforms)==(not expected) and focus_matches and finding_matches
        row.update(status="PASS" if matched else "FAIL",observed="CONFORMS" if conforms else "VIOLATES",
            violations=findings,result_graph=graph_snapshot(results,registry),validation_text=text)
    except Exception as exc:
        row.update(status="ERROR",observed="ERROR",error=type(exc).__name__+": "+str(exc))
    row["elapsed_ms"]=round((time.monotonic()-start)*1000)
    return row


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    receipt=json.loads((PROFILE_DIR/"receipt.json").read_text())
    module_path=PROFILE_DIR/"endpoints.ttl";model_path=ROOT/"ontology/riskium-model.json"
    if receipt["shapes_sha256"]!=sha(module_path.read_bytes()) or receipt["source_sha256"]!=sha(model_path.read_bytes()):
        raise SystemExit("Endpoint source or shapes digest mismatch")
    module=Graph().parse(module_path,format="turtle")
    review=json.loads((ROOT/"evaluation/coverage-review.json").read_text())
    reviewed=[r for r in review["obligation_reviews"] if r["engine"]=="SHACL" and
              r["family"]=="Managed-profile endpoint cardinality"]
    if len(reviewed)!=254:raise SystemExit("Endpoint denominator changed")
    metadata={x["source_element"]:x for x in receipt["endpoints"]}
    for r in reviewed:
        a,b=metadata[r["source_element"]],r["cases"]
        if (a["minimum"],a["maximum"],a["focus_class"],a["path"])!=(
            b["minimum"],b["maximum"],b["focus_class"],b["property_path"]):
            raise SystemExit("Endpoint contract mismatch: "+r["source_element"])
    model=json.loads(model_path.read_text());taxonomy=Graph()
    for g in model["generalizations"]:taxonomy.add((RISK[g["specific"]],RDFS.subClassOf,RISK[g["general"]]))
    registry={};taxonomy_key=graph_snapshot(taxonomy,registry)
    specs=fixture_specs(module,reviewed);rows=[]
    for i,spec in enumerate(specs,1):
        rows.append(execute(spec,taxonomy,registry))
        if i%200==0:print(json.dumps(dict(progress=i,total=len(specs))),flush=True)
    obligations=[]
    for r in reviewed:
        relevant=[x for x in rows if r["source_element"] in x["source_elements"]]
        obligations.append(dict(id=r["obligation_id"],source_element=r["source_element"],
            outcome="PASS" if relevant and all(x["status"]=="PASS" for x in relevant) else "FAIL",
            case_ids=[x["id"] for x in relevant],bounds={k:r["cases"][k] for k in ("minimum","maximum")},
            not_applicable={k:r["cases"][k] for k in ("below_minimum","above_maximum")
                            if r["cases"][k].get("expected")=="NOT_APPLICABLE"}))
    counts=Counter(x["status"] for x in rows);passed=sum(x["outcome"]=="PASS" for x in obligations)
    report=dict(title="Riskium endpoint SHACL execution 0.2.0",source_commit=subprocess.check_output(
        ["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),generated_at_utc=datetime.now(timezone.utc).isoformat(),
        runtime_python=sys.version.split()[0],engine={p:importlib.metadata.version(p) for p in ("pyshacl","rdflib","owlrl")},
        inputs={p:sha((ROOT/p).read_bytes()) for p in ("ontology/riskium-model.json","evaluation/coverage-review.json",
            "ontology/shacl/0.2.0/endpoints.ttl","ontology/shacl/0.2.0/receipt.json","tools/build_endpoint_shapes.py",
            "tools/run_endpoint_shacl.py","tools/run_shacl.py","tools/requirements-shacl.txt")},
        inference_policy="none; append shared source taxonomy; asserted sameAs normalization only; no imports",
        data_reconstruction="Parse normalized_graph snapshot and union shared taxonomy_graph before validation",
        taxonomy_graph=taxonomy_key,graphs=registry,cases=rows,obligations=obligations,
        coverage=dict(passed=passed,total=254,percent=round(passed/254*100,2),case_statuses=dict(counts),
            families={family:dict(total=sum(x["family"]==family for x in rows),
                passed=sum(x["family"]==family and x["status"]=="PASS" for x in rows)) for family in sorted({x["family"] for x in rows})}),
        limits=["Local targetNode controls and paired targetClass integration test this cardinality module only.",
            "The 0.1.0 conditional profiles retain their own receipt; a fully integrated managed-record admission suite is pending.",
            "Unbounded ends have no above-maximum negative; zero minima have no below-minimum negative.",
            "Value-node counts use normalized RDF identity, not proof of real-world distinctness.",
            "No catalog admission, unit/scale compatibility or independent semantic validity is established."])
    (OUT/"report.json").write_text(json.dumps(report,indent=2)+"\n")
    md=f"""# Ordered endpoint SHACL report — module 0.2.0

Source commit `{report['source_commit']}`. All **{passed}/254 ({report['coverage']['percent']}%)** declared endpoint obligations passed. There were **{len(rows)} actual SHACL runs**, **{counts.get('FAIL',0)} unexpected results** and **{counts.get('ERROR',0)} errors. These are cardinality-coverage results, not an ontology semantic-correctness score.

## Inputs, method and interpretation

The [JSON receipt](report.json) retains every raw/normalized graph, effective shapes graph, result graph, identity map, expected/observed source-shape and component, input hashes, engine/runtime versions and elapsed time. Graph snapshots are content-addressed canonical N-Triples. To reconstruct a validation data graph, union the case's normalized snapshot with the shared taxonomy snapshot. Base shapes are `ontology/shacl/0.2.0/endpoints.ttl`.

The generator reads the reviewed model; an independent predeclared 254-row contract supplies fixture bounds, focus classes and expected path direction. The two representations are checked for agreement before execution. A **source-end** label counts sources per target through an inverse path; a **target-end** label counts targets per source through a direct path. Counts include all distinct RDF value nodes on that path after asserted sameAs normalization. Filler type admission is a separate obligation and cannot hide an excessive count.

Local controls activate exactly one endpoint for an explicit focus node, then test valid counts and every applicable below/above-bound case. Every applicable bound is relaxed in a mutation: the previously rejected graph must become conforming. Every one of 254 paths has a supplementary hasValue witness and a reversed-path mutation. Both directions have one node, so cardinality alone cannot mask the reversal; the reversed path must fail specifically for the missing witness. These hasValue constraints are controls in fixture snapshots, not added domain rules. Unbounded or zero-minimum exclusions are retained below and never counted as negative-test passes.

Each of 127 relations also runs with both original targetClass populations and both endpoint shapes together, including valid, missing-link and applicable excessive-count cases. This establishes paired integration within the endpoint module. It does not yet establish full-profile admission across all relations plus the conditional 0.1.0 shapes. The original [conditional-profile receipt](../report.md) remains separately inspectable.

SHACL inference is `none`, no imports are followed, only the 66 source subclass triples are explicitly supplied, and each case runs meta-SHACL. The result must match the exact source-shape/component/focus-node set, including each focus in paired integration. All finite upper bounds also receive alias-normalization and one/two blank-node boundary probes.

## Fixture families

| Family | Passed / total |
| --- | ---: |
"""
    for k,v in report["coverage"]["families"].items():md+=f"| {k} | {v['passed']}/{v['total']} |\n"
    md+="\n## All 254 endpoint obligations\n\n| Obligation | Source | Outcome | Cases | Bounds | Excluded negative cases and reasons |\n| --- | --- | --- | ---: | --- | --- |\n"
    for o in obligations:
        reasons="; ".join(k+": "+v["reason"] for k,v in o["not_applicable"].items()) or "—"
        md+=f"| `{o['id']}` | `{o['source_element']}` | {o['outcome']} | {len(o['case_ids'])} | {o['bounds']['minimum']}..{o['bounds']['maximum'] if o['bounds']['maximum'] is not None else '*'} | {reasons} |\n"
    md+="\n## All executed cases\n\n| Case | Family | Expected | Observed | Verdict |\n| --- | --- | --- | --- | --- |\n"
    for r in rows:
        md+=f"| `{r['id']}` | {r['family']} | {'VIOLATES' if r['expected'] else 'CONFORMS'} | {r['observed']} | {r['status']} |\n"
    md+="""
## Reproduce and next step

```sh
.venv-shacl/bin/python tools/build_endpoint_shapes.py
.venv-shacl/bin/python tools/run_endpoint_shacl.py
```

Pinned environment setup is in `docs/reproducibility.md`. Next implement the 80 catalog-admission obligations, then remaining constraint routes and full managed-profile integration. C-08 compatibility remains partial; requirement/CQ execution and independent semantic review retain separate evidence.
"""
    (OUT/"report.md").write_text(md)
    print(json.dumps(dict(cases=len(rows),statuses=dict(counts),endpoints_passed=passed,total=254)),flush=True)
    if counts.get("FAIL",0) or counts.get("ERROR",0):raise SystemExit(1)


if __name__=="__main__":main()
