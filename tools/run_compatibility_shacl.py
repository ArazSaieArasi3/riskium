"""Execute/replay the bounded C-08 application policy with fixed exact oracles."""
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

from build_compatibility_shapes import C, CP, OUT as PROFILE_DIR, POLICY, digest, prepare, render
from build_shacl import ROOT, RISK, SH
from build_endpoint_shapes import E
from build_admission_shapes import A, compile_request
from run_admission_shacl import fixture_record, graph_snapshot, reconstruct_pair
from run_endpoint_shacl import copy, extract

EX = Namespace("urn:riskium:compatibility-fixture:")
OUT = ROOT / "evaluation/shacl/compatibility"
MISSING = {str(C[n]) for n in ("MissingNumericUnit", "MissingScheme", "MissingTermSet", "UnresolvedVersionMatch", "UnresolvedDimensionMatch", "UnresolvedVersionBinding", "UnresolvedUnitMatch", "UnresolvedSchemeMatch", "UnresolvedTermSetMatch")}
INCOMPATIBLE = {str(C[n]) for n in ("VersionMatch", "DimensionMatch", "KindMatch", "UnitMatch", "SchemeMatch", "TermSetMatch", "VersionBinding")}
INPUTS = ["ontology/riskium-model.json", "ontology/derived/riskium.owl.ttl", "evaluation/coverage-review.json",
    "evaluation/shacl/coverage-status.json", "evaluation/shacl/compatibility/profile-policy.json",
    "ontology/shacl/0.6.0/compatibility.ttl", "ontology/shacl/0.6.0/receipt.json",
    "ontology/shacl/0.2.0/endpoints.ttl", "ontology/shacl/0.3.0/admission.ttl",
    "tools/build_compatibility_shapes.py", "tools/run_compatibility_shacl.py",
    "tools/build_coherence_shapes.py", "tools/build_shacl.py", "tools/run_shacl.py",
    "tools/build_admission_shapes.py", "tools/run_admission_shacl.py", "tools/run_endpoint_shacl.py",
    "tools/build_endpoint_shapes.py", "tools/requirements-shacl.txt"]


def base(qualitative=False):
    g = Graph()
    for node, cls in ((EX.threshold, "RKM-C070"), (EX.indicator, "RKM-C069"), (EX.scale, "RKM-C036"),
                      (EX.dimension, "RKM-C039"), (EX.version, "RKM-C015")):
        g.add((node, RDF.type, RISK[cls]))
    for triple in ((EX.threshold, RISK["RX-025"], EX.indicator), (EX.threshold, RISK["RK2-020"], EX.scale),
                   (EX.scale, RISK["RK2-019"], EX.dimension), (EX.indicator, CP.dimension, EX.dimension),
                   (EX.version, RISK["RX-006"], EX.scale)):
        g.add(triple)
    for node in (EX.indicator, EX.scale):
        g.add((node, CP.scaleVersion, EX.version)); g.add((node, CP.source, EX.syntheticSource))
        g.add((node, CP.kind, CP.Qualitative if qualitative else CP.Numeric))
        for predicate, value in ((CP.scheme, EX.scheme), (CP.termSet, EX.termSet)) if qualitative else ((CP.unit, EX.unit),):
            g.add((node, predicate, value))
    return g


def findings(shape, component="SPARQLConstraintComponent", focus=EX.threshold):
    return [(str(C[shape]), str(SH[component]), str(focus))]


def fixture_specs():
    specs = []
    def add(cid, graph, expected=(), decision="COMPATIBLE_FOR_DECLARED_TASK", mutation=None, integration=False, profile="dual-anchor-metadata", targets=(EX.threshold,)):
        specs.append(dict(id=cid, raw=graph, expected_findings=list(expected), expected_decision=decision,
                          mutation=mutation, integration=integration, profile=profile, targets=list(targets)))
    add("C08-NUMERIC-MATCH", base())
    add("C08-QUALITATIVE-MATCH", base(True))
    for label, node, field, shape in (("INDICATOR-VERSION", EX.indicator, CP.scaleVersion, "IndicatorVersion"),
         ("SCALE-VERSION", EX.scale, CP.scaleVersion, "ScaleVersion"),
         ("INDICATOR-DIMENSION", EX.indicator, CP.dimension, "IndicatorDimension"),
         ("SCALE-DIMENSION", EX.scale, RISK["RK2-019"], "ScaleDimension"),
         ("INDICATOR-KIND", EX.indicator, CP.kind, "IndicatorKind"),
         ("INDICATOR-SOURCE", EX.indicator, CP.source, "IndicatorSource")):
        g = base(); g.remove((node, field, None))
        expected = findings(shape, "MinCountConstraintComponent")
        if field == CP.scaleVersion: expected += findings(shape + "Target", "MinCountConstraintComponent")
        add("C08-MISSING-" + label, g, expected, "NOT_READY")
    for label, node in (("INDICATOR", EX.indicator), ("SCALE", EX.scale)):
        g = base(); g.remove((node, CP.unit, None))
        add("C08-MISSING-" + label + "-UNIT", g, findings("MissingNumericUnit"), "NOT_READY")
    for field, label in ((CP.scheme, "Scheme"), (CP.termSet, "TermSet")):
        g = base(True); g.remove((EX.indicator, field, None))
        add("C08-MISSING-QUALITATIVE-" + label.upper(), g, findings("Missing" + label), "NOT_READY")
        g = base(True); g.set((EX.indicator, field, EX.otherInterpretation)); g.add((EX.otherInterpretation, OWL.differentFrom, EX.scheme if field == CP.scheme else EX.termSet))
        add("C08-DIFFERENT-QUALITATIVE-" + label.upper(), g, findings(label + "Match"), "INCOMPATIBLE")
    for label, field, value, shape in (("UNIT", CP.unit, EX.otherUnit, "UnitMatch"),
         ("DIMENSION", CP.dimension, EX.otherDimension, "DimensionMatch"),
         ("VERSION", CP.scaleVersion, EX.otherVersion, "VersionMatch")):
        g = base(); original = g.value(EX.indicator, field); g.set((EX.indicator, field, value))
        g.add((value, OWL.differentFrom, original))
        if field == CP.dimension: g.add((value, RDF.type, RISK["RKM-C039"]))
        if field == CP.scaleVersion:
            g.add((value, RDF.type, RISK["RKM-C015"])); g.add((value, RISK["RX-006"], EX.scale))
        add("C08-DIFFERENT-" + label, g, findings(shape), "INCOMPATIBLE")
        if field == CP.unit:
            add("C08-DELETED-UNIT-RULE", copy(g), mutation="UnitMatch")
            alias = copy(g); alias.remove((value, OWL.differentFrom, EX.unit)); alias.add((value, OWL.sameAs, EX.unit)); add("C08-UNIT-EXPLICIT-ALIAS", alias)
            unknown = copy(g); unknown.remove((value, OWL.differentFrom, EX.unit)); add("C08-UNKNOWN-UNIT-MAPPING", unknown, findings("UnresolvedUnitMatch"), "NOT_READY")
            labels = copy(g)
            for unit in (value, EX.unit): labels.add((unit, RDFS.label, Literal("same unit")))
            add("C08-LABELS-NOT-IDENTITY", labels, findings(shape), "INCOMPATIBLE")
        if field == CP.scaleVersion:
            alias = copy(g); alias.remove((value, OWL.differentFrom, EX.version)); alias.add((value, OWL.sameAs, EX.version)); add("C08-VERSION-EXPLICIT-ALIAS", alias)
    g = base(); g.set((EX.indicator, CP.kind, CP.Qualitative))
    g.remove((EX.indicator, CP.unit, None)); add("C08-DIFFERENT-KIND", g, findings("KindMatch"), "INCOMPATIBLE")
    g = base(); g.add((EX.otherScale, RDF.type, RISK["RKM-C036"])); g.add((EX.otherScale, OWL.differentFrom, EX.scale)); g.set((EX.version, RISK["RX-006"], EX.otherScale))
    add("C08-WRONG-VERSION-TARGET", g, findings("VersionBinding"), "INCOMPATIBLE")
    g = base(); g.remove((EX.version, RISK["RX-006"], None))
    add("C08-MISSING-VERSION-TARGET", g, findings("IndicatorVersionTarget", "MinCountConstraintComponent") + findings("ScaleVersionTarget", "MinCountConstraintComponent"), "NOT_READY")
    g = base(); g.add((EX.indicator, CP.unit, EX.otherUnit)); g.add((EX.otherUnit, OWL.differentFrom, EX.unit))
    add("C08-CONFLICTING-UNITS", g, findings("IndicatorUnit", "MaxCountConstraintComponent") + findings("UnitMatch"), "INVALID")
    g = base(); g.set((EX.indicator, CP.unit, Literal("metre")))
    add("C08-LITERAL-UNIT", g, findings("IndicatorUnit", "NodeKindConstraintComponent") + findings("UnresolvedUnitMatch"), "INVALID")
    g = base(True); g.add((EX.indicator, CP.unit, EX.unit))
    add("C08-QUALITATIVE-INVENTED-UNIT", g, findings("QualitativeNoUnit"), "INVALID")
    g = base(); g.remove((EX.threshold, RDF.type, None))
    add("C08-UNTYPED-SELECTED-THRESHOLD", g, findings("Threshold", "ClassConstraintComponent"), "INVALID")
    g = base(); g.set((EX.indicator, CP.kind, EX.unsupportedKind))
    add("C08-UNKNOWN-KIND", g, findings("IndicatorKind", "InConstraintComponent") + findings("KindMatch"), "INVALID")
    g = base(); g.remove((EX.indicator, CP.unit, None))
    add("C08-DELETED-COMPLETENESS-RULE", g, mutation="MissingNumericUnit")
    add("C08-RAW-INCOMPLETE", copy(g), decision="STAGING_ONLY", profile="raw")
    for label, triple in (("IDENTITY-CONFLICT", (EX.unit, OWL.sameAs, EX.otherUnit)),
        ("RESERVED-ALIAS", (CP.Numeric, OWL.sameAs, CP.Qualitative)),
        ("SCHEMA-INJECTION", (EX.fake, RDFS.subClassOf, RISK["RKM-C070"]))):
        g = base(); g.add(triple)
        if label == "IDENTITY-CONFLICT": g.add((EX.unit, OWL.differentFrom, EX.otherUnit))
        add("C08-" + label, g, decision="PROFILE_REJECTED")
    add("C08-EMPTY-FOCUS", base(), decision="PROFILE_REJECTED", targets=())
    for label, graph, expected, decision in (
        ("NUMERIC", base(), (), "COMPATIBLE_FOR_DECLARED_TASK"),
        ("QUALITATIVE", base(True), (), "COMPATIBLE_FOR_DECLARED_TASK")):
        add("C08-INTEGRATED-" + label, graph, expected, decision, integration=True)
    g = base(); g.set((EX.indicator, CP.unit, EX.otherUnit)); g.add((EX.otherUnit, OWL.differentFrom, EX.unit))
    add("C08-INTEGRATED-INCOMPATIBLE", g, findings("UnitMatch"), "INCOMPATIBLE", integration=True)
    g = base(); g.remove((EX.scale, RISK["RK2-019"], None))
    expected = findings("ScaleDimension", "MinCountConstraintComponent") + [(str(E["RK2-019-target-count"]), str(SH.MinCountConstraintComponent), str(EX.scale))]
    add("C08-INTEGRATED-MISSING-DIMENSION", g, expected, "NOT_READY", integration=True)
    g = base(); g.remove((EX.threshold, RDF.type, None))
    record = fixture_record("RKM-C070", suffix="-compatibility-0", candidate=EX.threshold)[1]
    expected = findings("Threshold", "ClassConstraintComponent") + [(str(A["CandidateType-RKM-C070"]), str(SH.ClassConstraintComponent), str(record))]
    add("C08-INTEGRATED-UNTYPED-THRESHOLD", g, expected, "INVALID", integration=True)
    return specs


def decide(violations, profile):
    if profile == "raw": return "STAGING_ONLY"
    if not violations: return "COMPATIBLE_FOR_DECLARED_TASK"
    if any(component != str(SH.MinCountConstraintComponent) and shape not in MISSING | INCOMPATIBLE
           for shape, component, focus in violations): return "INVALID"
    # Known incompatibility wins over additional missing fields; neither is accepted.
    if any(shape in INCOMPATIBLE for shape, component, focus in violations): return "INCOMPATIBLE"
    return "NOT_READY"


def execute(spec, module, taxonomy, registry):
    row = {k: v for k, v in spec.items() if k not in ("raw", "targets")}
    row["targets"] = [str(t) for t in spec["targets"]]; row["raw_graph"] = graph_snapshot(spec["raw"], registry)
    try: data, aliases = prepare(spec["raw"], spec["profile"], spec["targets"])
    except ValueError as exc:
        row.update(observed="PROFILE_REJECTED", error=str(exc), violations=[], engine_executed=False)
    else:
        try:
            shapes = copy(module) if spec["profile"] != "raw" else Graph()
            if spec["profile"] != "raw":
                for t in taxonomy: data.add(t)
                for owner in module.subjects(RDF.type, SH.NodeShape):
                    if owner == C.Threshold or any(module.objects(owner, SH.sparql)):
                        for target in spec["targets"]: shapes.add((owner, SH.targetNode, URIRef(aliases.get(str(target), str(target)))))
            if spec["mutation"]:
                owner = C[spec["mutation"]]; shapes.remove((owner, SH.sparql, C[spec["mutation"] + "Query"]))
            if spec["integration"]:
                endpoints = Graph().parse(ROOT / "ontology/shacl/0.2.0/endpoints.ttl")
                rels = ("RX-025", "RK2-020", "RK2-019")
                for t in extract(endpoints, [E[r + "-" + end] for r in rels for end in ("source", "target")]): shapes.add(t)
                admission = Graph().parse(ROOT / "ontology/shacl/0.3.0/admission.ttl")
                requests = []
                participants = ((EX.threshold, "RKM-C070"), (EX.indicator, "RKM-C069"),
                                (EX.scale, "RKM-C036"), (EX.dimension, "RKM-C039"), (EX.version, "RKM-C015"))
                for i, (candidate, cid) in enumerate(participants):
                    envelope, record, _ = fixture_record(cid, suffix="-compatibility-" + str(i), candidate=candidate)
                    # Envelope metadata must not repair missing domain type evidence.
                    for t in envelope:
                        if t != (candidate, RDF.type, RISK[cid]): data.add(t)
                    requests.append((record, cid))
                adm, _, _ = compile_request(admission, spec["raw"], requests, "managed-catalog", {cid for _, cid in participants})
                for t in adm: shapes.add(t)
                row["admission_requests"] = [(str(n), cid) for n, cid in requests]; row["endpoint_relations"] = list(rels)
            row["identity_map"] = aliases
            row["data_graph"] = graph_snapshot(data, registry); row["shapes_graph"] = graph_snapshot(shapes, registry)
            conforms, result, text = validate(data_graph=data, shacl_graph=shapes, inference="none", meta_shacl=True,
                do_owl_imports=False, advanced=False, abort_on_first=False, inplace=False)
            root = next(result.subjects(RDF.type, SH.ValidationReport))
            violations = sorted({(str(result.value(n, SH.sourceShape)), str(result.value(n, SH.sourceConstraintComponent)),
                str(result.value(n, SH.focusNode))) for n in result.objects(root, SH.result)})
            row.update(observed=decide(violations, spec["profile"]), violations=violations, engine_executed=True,
                result_graph=graph_snapshot(result, registry), validation_text=text, conforms=bool(conforms))
        except Exception as exc:
            row.update(observed="ENGINE_ERROR", error=type(exc).__name__ + ": " + str(exc), violations=[], engine_executed=False)
    aliases = row.get("identity_map", {})
    expected = sorted({(a, b, aliases.get(c, c)) for a, b, c in spec["expected_findings"]})
    row["expected_findings"] = expected
    row["status"] = "PASS" if row["observed"] == spec["expected_decision"] and row["violations"] == expected and row["observed"] != "ENGINE_ERROR" else "FAIL"
    return row


def run():
    module, compiled = render(); receipt = json.loads((PROFILE_DIR / "receipt.json").read_text())
    if not isomorphic(module, Graph().parse(PROFILE_DIR / "compatibility.ttl")) or json.dumps(receipt, sort_keys=True) != json.dumps(dict(compiled, shapes_sha256=digest(PROFILE_DIR / "compatibility.ttl")), sort_keys=True):
        raise ValueError("Committed shapes or receipt differs from reviewed builder/policy")
    taxonomy = Graph(); model = json.loads((ROOT / "ontology/riskium-model.json").read_text())
    for g in model["generalizations"]: taxonomy.add((RISK[g["specific"]], RDFS.subClassOf, RISK[g["general"]]))
    registry = {}; rows = [execute(s, module, taxonomy, registry) for s in fixture_specs()]
    failures = [r for r in rows if r["status"] != "PASS"]
    for r in failures: print(json.dumps({k:r.get(k) for k in ("id", "observed", "expected_decision", "violations", "expected_findings", "error")}), flush=True)
    baseline = json.loads((ROOT / "evaluation/shacl/coverage-status.json").read_text())
    report = dict(schema="riskium-c08-application-evidence-v1", generated_at_utc=datetime.now(timezone.utc).isoformat(),
        source_commit=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        source_commit_role="Execution checkout; exact executed bytes are bound by inputs. Receipt may be committed in a later evidence commit.",
        inputs={p: digest(ROOT / p) for p in INPUTS}, runtime_python=sys.version.split()[0],
        engine={p:importlib.metadata.version(p) for p in ("pyshacl", "rdflib", "owlrl")}, inference="none", imports=False,
        summary=dict(scenarios=len(rows), engine_executions=sum(r["engine_executed"] for r in rows),
            preflight_rejections=sum(r["observed"] == "PROFILE_REJECTED" for r in rows),
            selected_integration_cases=sum(r["integration"] for r in rows), mutation_controls=sum(bool(r["mutation"]) for r in rows),
            statuses=dict(Counter(r["status"] for r in rows)), decisions=dict(Counter(r["observed"] for r in rows))),
        baseline=dict(obligations=baseline["baseline"], outcomes=baseline["outcomes"],
            c08=next(r for r in baseline["obligations"] if r["source_element"] == "C-08")),
        supplemental_outcome="SCOPED_APPLICATION_POLICY_EXECUTED" if not failures else "FAILED",
        global_c08_outcome="PARTIAL", native_semantics_changed=False, independent_semantic_acceptance=False,
        graphs=registry, cases=rows)
    if failures: raise ValueError("Compatibility fixture/oracle failure")
    return report


def verify_saved(stored, fresh):
    if stored["inputs"] != fresh["inputs"] or stored["summary"] != fresh["summary"] or stored["baseline"] != fresh["baseline"]:
        raise ValueError("Receipt source binding or accounting differs")
    if stored["global_c08_outcome"] != "PARTIAL" or stored["native_semantics_changed"] or stored["independent_semantic_acceptance"]:
        raise ValueError("Receipt overstates scientific acceptance")
    if stored["supplemental_outcome"] != "SCOPED_APPLICATION_POLICY_EXECUTED": raise ValueError("Receipt not accepted")
    for key, graph in stored["graphs"].items():
        if hashlib.sha256(graph["text"].encode()).hexdigest() != key: raise ValueError("Snapshot hash mismatch")
    if len(stored["cases"]) != len(fresh["cases"]): raise ValueError("Case population differs")
    for old, new in zip(stored["cases"], fresh["cases"]):
        keys = ("id", "profile", "targets", "mutation", "integration", "expected_decision", "expected_findings", "violations", "observed", "status", "engine_executed")
        if any(json.dumps(old[k], sort_keys=True) != json.dumps(new[k], sort_keys=True) for k in keys):
            raise ValueError("Saved oracle differs from independent fixture expectation: " + new["id"])
        for field in ("raw_graph", "data_graph", "shapes_graph"):
            if field in new and not isomorphic(Graph().parse(data=stored["graphs"][old[field]]["text"], format="nt"),
                                               Graph().parse(data=fresh["graphs"][new[field]]["text"], format="nt")):
                raise ValueError("Saved effective graph differs: " + new["id"])
        if old["engine_executed"]:
            result = Graph().parse(data=stored["graphs"][old["result_graph"]]["text"], format="nt")
            root = next(result.subjects(RDF.type, SH.ValidationReport))
            actual = sorted({(str(result.value(n, SH.sourceShape)), str(result.value(n, SH.sourceConstraintComponent)), str(result.value(n, SH.focusNode))) for n in result.objects(root, SH.result)})
            if json.dumps(actual) != json.dumps(old["violations"]) or bool(result.value(root, SH.conforms).toPython()) != old["conforms"]:
                raise ValueError("Saved result graph contradicts the case: " + new["id"])


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--check", action="store_true"); args = parser.parse_args()
    report = run(); path = OUT / "report.json.gz"
    if args.check:
        verify_saved(json.loads(gzip.decompress(path.read_bytes())), report)
    else:
        OUT.mkdir(parents=True, exist_ok=True)
        path.write_bytes(gzip.compress((json.dumps(report, indent=2) + "\n").encode(), mtime=0))
        lines = ["# C-08 declared interpretation compatibility — application profile 0.6.0", "",
            "**Scoped application policy executed; global C-08 remains PARTIAL.** No native ontology/OWL change, unit conversion, value/comparator evaluation or independent semantic acceptance is claimed.", "",
            "Execution checkout: `" + report["source_commit"] + "`; exact input hashes and raw/effective/shapes/result graphs are in [the full receipt](report.json.gz). [Policy](profile-policy.json) and [review](profile-review.md) define the task.", "",
            "Summary: " + json.dumps(report["summary"]) + ".", "",
            "The original 359-row ledger and old blocked task fixture are retained byte for byte. The new evidence covers explicit supplementary metadata, not approval of every possible interpretation of C-08. The unchanged ledger remains 341 scoped PASS, 1 PARTIAL and 17 NOT_RUN. HermiT is not rerun by this module.", "",
            "| Case | Expected decision | Observed | Engine executed | Verdict |", "| --- | --- | --- | --- | --- |"]
        for r in report["cases"]: lines.append(f"| `{r['id']}` | {r['expected_decision']} | {r['observed']} | {r['engine_executed']} | {r['status']} |")
        lines += ["", "Replay: `python tools/run_compatibility_shacl.py --check`. This executes fresh validations, verifies the fixed oracles, snapshot hashes and source bindings, and compares saved raw/effective/shapes graphs. Preflight rejections and software tests are not added to the engine count."]
        (OUT / "report.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(report["summary"]), flush=True)


if __name__ == "__main__": main()
