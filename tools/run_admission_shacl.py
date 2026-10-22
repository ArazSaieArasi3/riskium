"""Execute all catalog metadata admission rows with independently fixed oracles."""
import importlib.metadata
import json
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timezone

from pyshacl import validate
from rdflib import BNode, Graph, Literal, Namespace, OWL, RDF, RDFS, URIRef, XSD

from build_admission_shapes import A, AP, DC, OUT as PROFILE_DIR, compile_request, digest
from build_shacl import ROOT, RISK, SH
from build_endpoint_shapes import E
from run_endpoint_shacl import copy, extract, sha

EX = Namespace("urn:riskium:admission-fixture:")
OUT = ROOT / "evaluation/shacl/admission"


def graph_snapshot(graph, registry):
    # Preserve shared blank-node identifiers across data, shapes and results.
    # Independent per-graph canonicalization would break blank targetNode joins.
    text = "\n".join(sorted(graph.serialize(format="nt").splitlines())) + "\n"
    key = sha(text); registry.setdefault(key, dict(format="nt", text=text))
    return key


def reconstruct_pair(report, row):
    context = {}
    data = Graph().parse(data=report["graphs"][row["data_graph"]]["text"], format="nt", bnode_context=context)
    shapes = Graph().parse(data=report["graphs"][row["shapes_graph"]]["text"], format="nt", bnode_context=context)
    return data, shapes


def fixture_record(cid, suffix="", task=False, record=None, candidate=None):
    record = record if record is not None else EX[cid + suffix + "-record"]
    candidate = candidate if candidate is not None else EX[cid + suffix + "-candidate"]
    g = Graph()
    for triple in ((record, AP.candidate, candidate), (record, AP.declaredClass, RISK[cid]),
                   (record, DC.title, Literal("Catalog record", lang="en")),
                   (record, DC.subject, EX.subject), (record, DC.source, EX.source),
                   (candidate, RDF.type, RISK[cid])):
        g.add(triple)
    if task: g.add((record, AP.requestedTask, AP.CatalogInspection))
    return g, record, candidate


def fixture_specs(model, core, excluded):
    specs = []

    def add(cid, elements, family, raw, requests, expected=(), profile="managed-catalog",
            mutation=None, endpoint=None):
        specs.append(dict(id=cid, source_elements=elements, family=family, raw=raw,
                          requests=requests, expected_findings=[tuple(map(str, x)) for x in expected],
                          profile=profile, mutation=mutation, endpoint=endpoint))

    for cid in core:
        base, record, candidate = fixture_record(cid)
        request = [(record, cid)]
        add(cid + "-MANAGED", [cid], "Managed complete", base, request)
        task, _, _ = fixture_record(cid, task=True)
        add(cid + "-TASK", [cid], "Catalog task complete", task, request, profile="task-catalog-inspection")
        incomplete = Graph(); incomplete.add((record, AP.declaredClass, RISK[cid]))
        add(cid + "-RAW", [cid], "Incomplete raw staging", incomplete, request, profile="raw")
        for name, path, shape in (("CANDIDATE", AP.candidate, A.Candidate),
                                  ("TITLE", DC.title, A.Title),
                                  ("SUBJECT", DC.subject, A.Subject), ("SOURCE", DC.source, A.Source)):
            data = copy(base); data.remove((record, path, None))
            add(cid + "-MISSING-" + name, [cid], "Required metadata", data, request,
                [(shape, SH.MinCountConstraintComponent, record)])
        data = copy(base); data.remove((candidate, RDF.type, None))
        add(cid + "-UNTYPED", [cid], "Explicit candidate type", data, request,
            [(A["CandidateType-" + cid], SH.ClassConstraintComponent, record)])
        add(cid + "-UNTYPED-MUTANT", [cid], "Omitted-rule mutation", data, request,
            mutation="remove-candidate-class")
        data = copy(base); data.set((record, DC.title, Literal("   ")))
        add(cid + "-BLANK-TITLE", [cid], "Text boundary", data, request,
            [(A.Title, SH.PatternConstraintComponent, record)])
        data = copy(base); data.set((record, DC.title, Literal(7)))
        add(cid + "-NON-TEXT-TITLE", [cid], "Text datatype", data, request,
            [(A.Title, SH.OrConstraintComponent, record)])
        data = copy(base); data.set((record, DC.source, Literal("source-label")))
        add(cid + "-LITERAL-SOURCE", [cid], "Source locator type", data, request,
            [(A.Source, SH.NodeKindConstraintComponent, record)])
        data = copy(base); data.remove((record, DC.source, None))
        add(cid + "-SOURCE-MUTANT", [cid], "Omitted-rule mutation", data, request,
            mutation="remove-source-minimum")
        data = copy(base); data.add((record, AP.requestedTask, AP.RiskAssessment))
        add(cid + "-UNSUPPORTED-TASK", [cid], "Unsupported readiness", data, request,
            [(A.RequestedTask, SH.InConstraintComponent, record)])
        add(cid + "-MISSING-TASK", [cid], "Task input missing", base, request,
            [(A.RequiredTask, SH.MinCountConstraintComponent, record)], profile="task-catalog-inspection")
        wrong = next(x for x in core if x != cid)
        data = copy(base); data.set((record, AP.declaredClass, RISK[wrong]))
        add(cid + "-WRONG-DECLARATION", [cid], "External class request", data, request,
            [(A["ExpectedClass-" + cid], SH.HasValueConstraintComponent, record),
             (A.DeclaredClass, SH.InConstraintComponent, record)])
        blank = BNode(cid + "-blank-record")
        data, _, _ = fixture_record(cid, record=blank)
        add(cid + "-BLANK-RECORD", [cid], "Managed record identity", data, [(blank, cid)],
            [(A.Record, SH.NodeKindConstraintComponent, blank)])
        data, _, _ = fixture_record(cid, candidate=BNode(cid + "-blank-candidate"))
        add(cid + "-BLANK-CANDIDATE", [cid], "Managed candidate identity", data, request,
            [(A.Candidate, SH.NodeKindConstraintComponent, record)])
        data = copy(base); alias = EX[cid + "-alias"]
        data.add((candidate, OWL.sameAs, alias)); data.add((record, AP.candidate, alias))
        add(cid + "-ALIAS", [cid], "Asserted alias normalization", data, request)
        other, other_record, _ = fixture_record(cid, suffix="-other")
        data = copy(base)
        for t in other: data.add(t)
        add(cid + "-SAME-LABEL", [cid], "Equal labels retain distinct records", data,
            request + [(other_record, cid)])
        data = copy(base); alias = EX[cid + "-0-record-alias"]
        data.add((record, OWL.sameAs, alias))
        add(cid + "-FOCUS-ALIAS", [cid], "Normalized external focus", data, request)

    for cid in excluded:
        base, record, _ = fixture_record(cid)
        add(cid + "-RAW-BOUNDARY", [cid], "Optional boundary staging", base, [(record, cid)], profile="raw")
        add(cid + "-CORE-EXCLUSION", [cid], "Optional boundary rejection", base, [(record, cid)],
            [(A.DeclaredClass, SH.InConstraintComponent, record)])
        data, _, _ = fixture_record(core[0]); data.set((record, AP.declaredClass, RISK[cid]))
        # Explicit managed request fixes a core declaration; switching it to a boundary cannot evade validation.
        core_record = EX[core[0] + "-record"]
        data.set((core_record, AP.declaredClass, RISK[cid]))
        data.remove((record, None, None))
        add(cid + "-PROMOTION-ATTEMPT", [cid], "Boundary promotion attempt", data, [(core_record, core[0])],
            [(A.DeclaredClass, SH.InConstraintComponent, core_record),
             (A["ExpectedClass-" + core[0]], SH.HasValueConstraintComponent, core_record)])

    for gen in model["generalizations"]:
        general, specific = gen["general"], gen["specific"]
        if general not in core or specific not in core: continue
        base, record, candidate = fixture_record(general, suffix="-" + gen["id"])
        base.set((candidate, RDF.type, RISK[specific]))
        add(gen["id"] + "-SUBTYPE", [general, specific], "Source subtype admission", base, [(record, general)])
        data, record, candidate = fixture_record(specific, suffix="-" + gen["id"])
        data.set((candidate, RDF.type, RISK[general]))
        add(gen["id"] + "-REVERSE", [general, specific], "No reverse inheritance", data, [(record, specific)],
            [(A["CandidateType-" + specific], SH.ClassConstraintComponent, record)])

    for rel in (r for r in model["associations"] if r["scope_layer"] == "FORMAL_CORE"):
        rid = rel["id"]
        def participant(cid, suffix):
            if cid in core: return fixture_record(cid, suffix=suffix)
            candidate = EX[cid + suffix + "-anchor"]; g = Graph()
            g.add((candidate, RDF.type, RISK[cid])); return g, None, candidate
        source, sr, sc = participant(rel["source"], "-" + rid + "-source")
        target, tr, tc = participant(rel["target"], "-" + rid + "-target")
        for t in target: source.add(t)
        source.add((sc, RISK[rid], tc))
        request = [(node, cid) for node, cid in ((sr, rel["source"]), (tr, rel["target"])) if node is not None]
        elements = [rel["source"], rel["target"]]
        checks = [(str(node), cid) for node, record, cid in ((sc, sr, rel["source"]),
                  (tc, tr, rel["target"])) if record is None]
        add(rid + "-PAIR-ADMISSION", elements, "Endpoint plus admission integration", source, request, endpoint=rid)
        specs[-1]["anchor_checks"] = checks
        missing = copy(source); missing.remove((tc, RDF.type, None))
        add(rid + "-UNTYPED-FILLER", elements, "Endpoint filler type", missing, request,
            [(A["CandidateType-" + rel["target"]], SH.ClassConstraintComponent, tr)] if tr is not None
            else [(A.AnchorCheck, SH.ClassConstraintComponent, tc)], endpoint=rid)
        specs[-1]["anchor_checks"] = checks
    return specs


def execute(spec, module, taxonomy, catalog, registry, endpoints):
    row = {k: v for k, v in spec.items() if k not in ("raw", "requests")}
    row["requests"] = [(str(node), cid) for node, cid in spec["requests"]]
    row["raw_graph"] = graph_snapshot(spec["raw"], registry)
    started = time.monotonic()
    try:
        shapes, normalized, mapping = compile_request(module, spec["raw"], spec["requests"], spec["profile"], catalog)
        row["identity_map"] = mapping
        if spec["mutation"] == "remove-source-minimum": shapes.remove((A.Source, SH.minCount, None))
        if spec["mutation"] == "remove-candidate-class":
            for _, cid in spec["requests"]: shapes.remove((A["CandidateType-" + cid], SH["class"], None))
        if spec["endpoint"]:
            for t in extract(endpoints, [E[spec["endpoint"] + "-source"], E[spec["endpoint"] + "-target"]]): shapes.add(t)
        for node, cid in spec.get("anchor_checks", []):
            shapes.add((A.AnchorCheck, RDF.type, SH.NodeShape))
            shapes.add((A.AnchorCheck, SH.targetNode, URIRef(node)))
            shapes.add((A.AnchorCheck, SH["class"], RISK[cid]))
        data = copy(normalized)
        if spec["profile"] != "raw":
            for t in taxonomy: data.add(t)
        row["data_graph"] = graph_snapshot(data, registry)
        row["shapes_graph"] = graph_snapshot(shapes, registry)
        conforms, results, text = validate(data_graph=data, shacl_graph=shapes, inference="none",
            meta_shacl=True, advanced=False, do_owl_imports=False, abort_on_first=False, inplace=False)
        report = next(results.subjects(RDF.type, SH.ValidationReport))
        findings = [(str(results.value(n, SH.sourceShape)), str(results.value(n, SH.sourceConstraintComponent)),
                     str(results.value(n, SH.focusNode))) for n in results.objects(report, SH.result)]
        expected = {tuple(mapping.get(value, value) if i == 2 else value for i, value in enumerate(finding))
                    for finding in spec["expected_findings"]}
        matches = set(findings) == expected and bool(conforms) == (not expected)
        row.update(status="PASS" if matches else "FAIL", observed="CONFORMS" if conforms else "VIOLATES",
                   violations=findings, expected_findings=sorted(expected), result_graph=graph_snapshot(results, registry),
                   validation_text=text, engine_executed=True)
    except Exception as exc:
        row.update(status="ERROR", observed="ERROR", error=type(exc).__name__ + ": " + str(exc), engine_executed=False)
    row["elapsed_ms"] = round((time.monotonic() - started) * 1000)
    return row


def main():
    module_path = PROFILE_DIR / "admission.ttl"
    receipt = json.loads((PROFILE_DIR / "receipt.json").read_text())
    model_path = ROOT / "ontology/riskium-model.json"
    contract_path = ROOT / "evaluation/coverage-review.json"
    if (receipt["shapes_sha256"], receipt["source_sha256"], receipt["contract_sha256"], receipt["policy_sha256"]) != (
            digest(module_path), digest(model_path), digest(contract_path), digest(OUT / "profile-policy.json")):
        raise SystemExit("Admission shapes/source/contract/policy digest mismatch")
    model = json.loads(model_path.read_text())
    core, excluded = receipt["core_classes"], receipt["excluded_boundaries"]
    catalog = set(core + excluded)
    reviewed = [r for r in json.loads(contract_path.read_text())["obligation_reviews"]
                if r["engine"] == "SHACL" and r["family"] == "Admission and class profile"]
    if len(reviewed) != 80 or {r["source_element"] for r in reviewed} != catalog:
        raise SystemExit("Admission denominator changed")
    module = Graph().parse(module_path, format="turtle")
    endpoints = Graph().parse(ROOT / "ontology/shacl/0.2.0/endpoints.ttl", format="turtle")
    taxonomy = Graph()
    for g in model["generalizations"]: taxonomy.add((RISK[g["specific"]], RDFS.subClassOf, RISK[g["general"]]))
    specs = fixture_specs(model, core, excluded); registry = {}; rows = []
    for i, spec in enumerate(specs, 1):
        row = execute(spec, module, taxonomy, catalog, registry, endpoints); rows.append(row)
        if row["status"] != "PASS": print(json.dumps({k: row.get(k) for k in ("id", "status", "error", "violations", "expected_findings")}), flush=True)
        if i % 100 == 0: print(json.dumps(dict(progress=i, total=len(specs))), flush=True)
    obligations = []
    for r in reviewed:
        relevant = [c for c in rows if r["source_element"] in c["source_elements"]]
        obligations.append(dict(id=r["obligation_id"], source_element=r["source_element"],
            source_element_sha256=r["source_element_sha256"],
            disposition="MANAGED_CATALOG_METADATA" if r["source_element"] in core else "OPTIONAL_CORE_EXCLUSION",
            outcome="PASS" if relevant and all(c["status"] == "PASS" for c in relevant) else "FAIL",
            case_ids=[c["id"] for c in relevant]))
    counts = Counter(c["status"] for c in rows); passed = sum(o["outcome"] == "PASS" for o in obligations)
    inputs = ["ontology/riskium-model.json", "ontology/derived/riskium.owl.ttl", "evaluation/coverage-review.json",
              "evaluation/native-review-decisions.json", "ontology/shacl/0.3.0/admission.ttl", "ontology/shacl/0.3.0/receipt.json",
              "ontology/shacl/0.2.0/endpoints.ttl", "evaluation/shacl/admission/profile-policy.json",
              "tools/build_admission_shapes.py", "tools/run_admission_shacl.py", "tools/run_endpoint_shacl.py",
              "tools/build_endpoint_shapes.py", "tools/build_shacl.py", "tools/run_shacl.py", "tools/requirements-shacl.txt"]
    report = dict(title="Riskium catalog admission 0.3.0", source_commit=subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(), generated_at_utc=datetime.now(timezone.utc).isoformat(),
        runtime_python=sys.version.split()[0], engine={p: importlib.metadata.version(p) for p in ("pyshacl", "rdflib", "owlrl")},
        inputs={p: digest(ROOT / p) for p in inputs},
        inference_policy="none; append source taxonomy only outside raw staging; normalize only asserted named sameAs",
        focus_policy="Explicit nonempty external record/expected-class request, preserved per case; raw is not admission",
        coverage=dict(passed=passed, total=80, core_profiles=77, boundary_exclusions=3, case_statuses=dict(counts),
            actual_engine_runs=sum(c["engine_executed"] for c in rows),
            families={f: dict(total=sum(c["family"] == f for c in rows),
                passed=sum(c["family"] == f and c["status"] == "PASS" for c in rows)) for f in sorted({c["family"] for c in rows})}),
        snapshot_reconstruction="Parse data and shapes N-Triples with one shared bnode_context; use reconstruct_pair(). Blank-node labels are preserved within the receipt, not canonical graph identities.",
        graphs=registry, cases=rows, obligations=obligations,
        limits=["PASS applies to managed catalog metadata and the sole CatalogInspection task, not full risk-record admission.",
                "Three PASS rows establish exclusion of optional notions, not admission or semantic truth of referents.",
                "127 relation pairs combine endpoints and record/candidate typing only; full conditional/multi-relation integration remains open.",
                "C-08 compatibility, remaining constraint routes, independent semantic review and CQ acceptance remain open."])
    (OUT / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    md = f"""# Catalog metadata admission SHACL report — module 0.3.0

Source commit `{report['source_commit']}`. **{passed}/80** catalog-admission obligations passed within the declared [policy](profile-review.md): 77 managed catalog class profiles and three explicit boundary exclusions. **{report['coverage']['actual_engine_runs']} actual SHACL validations**, {counts.get('FAIL', 0)} unexpected results, {counts.get('ERROR', 0)} errors. These are application metadata/task-inspection results, not complete risk-record or semantic validation.

The [JSON receipt](report.json) retains complete raw, effective data, shapes and result graph snapshots, external focus/class requests, identity maps, exact input/code hashes, runtime versions, expected/observed shape-component-focus sets and individual case outcomes. Use `reconstruct_pair()` to parse the `data_graph` and `shapes_graph` snapshots with a shared blank-node context, preserving cross-graph target identities. Snapshot hashes identify serialized content within this receipt, not canonical RDF graph identities. No source model or OWL axiom is changed. Policy is an author implementation decision, not an independent domain review.

Each of 77 core concepts is exercised with complete managed metadata, the sole supported catalog-inspection task, incomplete raw staging, missing metadata, wrong text/source types, missing candidate type, unsupported/missing task, wrong class declaration, blank identities, aliases and equal-label distinct records. Omitted source/type rule mutations must change rejection to conformance. Source generalizations have subtype and forbidden reverse controls. All 127 relations combine both endpoint shapes with admission envelopes for both participants, including an untyped filler. No result here discharges the remaining 21 constraints or C-08 compatibility.

## Fixture families

| Family | Matched / total |
| --- | ---: |
"""
    for f, v in report["coverage"]["families"].items(): md += f"| {f} | {v['passed']}/{v['total']} |\n"
    md += "\n## All 80 source-bound obligations\n\n| Obligation | Concept | Disposition | Outcome | Cases |\n| --- | --- | --- | --- | ---: |\n"
    for o in obligations: md += f"| `{o['id']}` | `{o['source_element']}` | {o['disposition']} | {o['outcome']} | {len(o['case_ids'])} |\n"
    md += "\n## Reproduce\n\n```sh\n.venv-shacl/bin/python tools/build_admission_shapes.py\n.venv-shacl/bin/python tools/run_admission_shacl.py\n.venv-shacl/bin/python tools/summarize_shacl.py\n```\n\nContinue parent #5 with constraint routes, C-08 compatibility and full-profile integration. Close child #17 only after regression checks and published readback.\n"
    (OUT / "report.md").write_text(md)
    print(json.dumps(report["coverage"]), flush=True)
    if passed != 80 or counts.get("FAIL", 0) or counts.get("ERROR", 0): raise SystemExit(1)


if __name__ == "__main__":
    main()
