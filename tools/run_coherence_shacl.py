"""Run bounded context/revision coherence with exact negative and mutation oracles."""
import importlib.metadata
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone

from pyshacl import validate
from rdflib import BNode, Graph, Literal, Namespace, OWL, RDF, RDFS

from build_coherence_shapes import C, OUT as PROFILE_DIR, CONSTRAINTS, digest, prepare
from build_shacl import ROOT, RISK, SH
from build_endpoint_shapes import E
from build_admission_shapes import compile_request
from run_admission_shacl import fixture_record, graph_snapshot, reconstruct_pair
from run_endpoint_shacl import copy, extract

EX = Namespace("urn:riskium:coherence:")
OUT = ROOT / "evaluation/shacl/coherence"


def context(analyzed=("a",), general=("a",)):
    g = Graph(); case = EX.case
    g.add((case, RDF.type, RISK["RKM-X01"]))
    for label in set(analyzed) | set(general): g.add((EX[label], RDF.type, RISK["RKM-C002"]))
    for label in analyzed: g.add((case, RISK["R-35"], EX[label]))
    for label in general: g.add((case, RISK["RX-001"], EX[label]))
    return g


def chain(n, blank=False):
    g = Graph(); nodes = [(BNode("revision-" + str(i)) if blank else EX["revision-" + str(i)]) for i in range(n)]
    g.add((EX.entry, RDF.type, RISK["RKM-C022"]))
    for i, node in enumerate(nodes):
        for t in ((node, RDF.type, RISK["RKM-C023"]), (node, RISK["R-33"], EX.entry),
                  (node, RISK["RX-006"], EX.entry)):
            g.add(t)
        if i: g.add((node, RISK["R-34"], nodes[i - 1]))
    return g, nodes


def findings(shape, component, *foci):
    return [(str(C[shape]), str(SH[component]), str(f)) for f in foci]


def fixture_specs():
    specs = []
    def add(cid, constraint, raw, expected=(), profile="managed", mutation=None, integration=False):
        specs.append(dict(id=cid, constraint=constraint, raw=raw, expected_findings=list(expected),
                          profile=profile, mutation=mutation, integration=integration))
    missing = findings("C23Case", "SPARQLConstraintComponent", EX.case)
    add("C23-MATCH", "C-23", context())
    add("C23-GENERAL-ONLY", "C-23", context((), ("a",)))
    add("C23-UNSPECIFIED", "C-23", context((), ()))
    add("C23-MISSING-GENERAL", "C-23", context(("a",), ()), missing)
    add("C23-DIFFERENT-GENERAL", "C-23", context(("a",), ("b",)), missing)
    add("C23-MULTIPLE", "C-23", context(("a", "b"), ("a", "b", "c")))
    add("C23-MISSING-ONE", "C-23", context(("a", "b"), ("a",)), missing)
    g = context(); g.remove((EX.case, RDF.type, None))
    add("C23-UNTYPED-SUBJECT", "C-23", g, findings("C23Case", "ClassConstraintComponent", EX.case))
    g = context(); g.set((EX.a, RDF.type, RISK["RKM-C022"]))
    add("C23-WRONG-CONTEXT-TYPE", "C-23", g,
        findings("C23AnalyzedType", "ClassConstraintComponent", EX.case) + findings("C23ContextType", "ClassConstraintComponent", EX.case))
    g = context(("a",), ("b",)); g.add((EX.a, OWL.sameAs, EX.b))
    add("C23-CONTEXT-ALIASES", "C-23", g)
    g = context(("a",), ("b",))
    for node in (EX.a, EX.b): g.add((node, RDFS.label, Literal("same label")))
    add("C23-LABELS-NOT-IDENTITY", "C-23", g, missing)
    add("C23-RAW-INCOMPLETE", "C-23", context(("a",), ()), profile="raw")
    add("C23-DELETED-RULE", "C-23", context(("a",), ()), mutation="delete-context-inclusion")
    add("C23-REVERSED-RULE", "C-23", context((), ("a",)), missing, mutation="reverse-context-inclusion")

    for n in (1, 2, 3, 6, 12):
        g, _ = chain(n); add("C24-CHAIN-" + str(n), "C-24", g)
    g, nodes = chain(3); g.remove((nodes[2], RISK["R-34"], None)); g.add((nodes[2], RISK["R-34"], nodes[0]))
    add("C24-BRANCH", "C-24", g)
    g, nodes = chain(4); g.set((nodes[3], RISK["R-34"], nodes[1]))
    add("C24-SKIPPED-PREDECESSOR", "C-24", g)
    g, nodes = chain(2, blank=True); add("C24-BLANK-NODES", "C-24", g)
    g, nodes = chain(1)
    g.remove((nodes[0], RISK["R-33"], None))
    add("C24-MISSING-REVISION-OF", "C-24", g,
        findings("C24Entry", "MinCountConstraintComponent", nodes[0]) + findings("C24Entry", "EqualsConstraintComponent", nodes[0]))
    g, nodes = chain(1); g.remove((nodes[0], RISK["RX-006"], None))
    add("C24-MISSING-VERSION-OF", "C-24", g,
        findings("C24VersionEntry", "MinCountConstraintComponent", nodes[0]) + findings("C24Entry", "EqualsConstraintComponent", nodes[0]))
    g, nodes = chain(1); g.add((EX.otherEntry, RDF.type, RISK["RKM-C022"]))
    g.set((nodes[0], RISK["RX-006"], EX.otherEntry))
    mismatch = copy(g)
    add("C24-DIFFERENT-ENTRY-TARGETS", "C-24", g, findings("C24Entry", "EqualsConstraintComponent", nodes[0]))
    add("C24-DELETED-EQUALITY", "C-24", mismatch, mutation="delete-entry-equality")
    g, nodes = chain(1); g.set((EX.entry, RDF.type, RISK["RKM-C002"]))
    add("C24-WRONG-ENTRY-TYPE", "C-24", g,
        findings("C24Entry", "ClassConstraintComponent", nodes[0]) + findings("C24VersionEntry", "ClassConstraintComponent", nodes[0]))
    g, nodes = chain(1); g.remove((nodes[0], RDF.type, None))
    add("C24-UNTYPED-REVISION", "C-24", g, findings("C24Revision", "ClassConstraintComponent", nodes[0]))
    g, nodes = chain(1); g.add((EX.otherEntry, RDF.type, RISK["RKM-C022"]))
    for prop in ("R-33", "RX-006"): g.add((nodes[0], RISK[prop], EX.otherEntry))
    add("C24-MULTIPLE-ENTRY-TARGETS", "C-24", g,
        findings("C24Entry", "MaxCountConstraintComponent", nodes[0]) + findings("C24VersionEntry", "MaxCountConstraintComponent", nodes[0]))
    for n in (1, 2, 3, 8, 17):
        g, nodes = chain(n); g.add((nodes[0], RISK["R-34"], nodes[-1]))
        add("C24-CYCLE-" + str(n), "C-24", g, findings("C24Acyclic", "SPARQLConstraintComponent", *nodes))
    g, nodes = chain(2); g.add((nodes[0], RISK["R-34"], nodes[-1]))
    add("C24-DELETED-CYCLE", "C-24", g, mutation="delete-cycle")
    g, nodes = chain(3); g.add((nodes[0], RISK["R-34"], nodes[-1]))
    add("C24-WEAKENED-CYCLE", "C-24", g, mutation="self-loop-only")
    g, nodes = chain(2); g.add((EX.otherEntry, RDF.type, RISK["RKM-C022"]))
    for prop in ("R-33", "RX-006"): g.set((nodes[1], RISK[prop], EX.otherEntry))
    cross_entry = copy(g)
    add("C24-CROSS-ENTRY", "C-24", g, findings("C24Lineage", "SPARQLConstraintComponent", nodes[1]))
    add("C24-DELETED-LINEAGE", "C-24", cross_entry, mutation="delete-same-entry")
    g, nodes = chain(3); g.add((nodes[2], RISK["R-34"], nodes[0]))
    add("C24-TWO-PREDECESSORS", "C-24", g, findings("C24Previous", "MaxCountConstraintComponent", nodes[2]))
    add("C24-RELAXED-PREDECESSORS", "C-24", g, mutation="relax-predecessor-count")
    g, nodes = chain(1); g.set((nodes[0], RISK["RX-006"], EX.entryAlias)); g.add((EX.entry, OWL.sameAs, EX.entryAlias))
    add("C24-ENTRY-ALIASES", "C-24", g)
    g, nodes = chain(2); g.add((nodes[0], OWL.sameAs, nodes[1]))
    add("C24-ALIASED-SELF-LOOP", "C-24", g, findings("C24Acyclic", "SPARQLConstraintComponent", nodes[0]))
    g = copy(mismatch)
    for node in (EX.entry, EX.otherEntry): g.add((node, RDFS.label, Literal("same entry label")))
    add("C24-LABELS-NOT-IDENTITY", "C-24", g, findings("C24Entry", "EqualsConstraintComponent", EX["revision-0"]))
    add("C24-RAW-CONFLICT", "C-24", mismatch, profile="raw")
    for prefix, cid, graph, expected in (("C23-INTEGRATED-VALID", "C-23", context(), ()),
        ("C23-INTEGRATED-MISSING", "C-23", context(("a",), ("b",)), missing),
        ("C24-INTEGRATED-VALID", "C-24", chain(3)[0], ()),
        ("C24-INTEGRATED-CROSS-ENTRY", "C-24", cross_entry,
         findings("C24Lineage", "SPARQLConstraintComponent", EX["revision-1"]))):
        add(prefix, cid, graph, expected, integration=True)
    return specs


def execute(spec, module, taxonomy, registry):
    row = {k: v for k, v in spec.items() if k != "raw"}
    row["raw_graph"] = graph_snapshot(spec["raw"], registry)
    try:
        data, aliases = prepare(spec["raw"], spec["profile"])
        shapes = copy(module) if spec["profile"] == "managed" else Graph()
        if spec["profile"] == "managed":
            for t in taxonomy: data.add(t)
        mut = spec["mutation"]
        for mutation, owner, query in (("delete-context-inclusion", C.C23Case, C.C23Inclusion),
                                      ("delete-cycle", C.C24Acyclic, C.C24Cycle),
                                      ("delete-same-entry", C.C24Lineage, C.C24SameEntry)):
            if mut == mutation: shapes.remove((owner, SH.sparql, query))
        if mut == "reverse-context-inclusion":
            query = str(shapes.value(C.C23Inclusion, SH.select)).replace("risk:R-35", "risk:TMP").replace("risk:RX-001", "risk:R-35").replace("risk:TMP", "risk:RX-001")
            shapes.set((C.C23Inclusion, SH.select, Literal(query)))
        if mut == "self-loop-only":
            shapes.set((C.C24Cycle, SH.select, Literal(str(shapes.value(C.C24Cycle, SH.select)).replace("risk:R-34+", "risk:R-34"))))
        if mut == "delete-entry-equality": shapes.remove((C.C24Entry, SH.equals, None))
        if mut == "relax-predecessor-count": shapes.set((C.C24Previous, SH.maxCount, Literal(2)))
        if spec["integration"]:
            endpoints = Graph().parse(ROOT / "ontology/shacl/0.2.0/endpoints.ttl")
            rels = ("R-35", "RX-001") if spec["constraint"] == "C-23" else ("R-33", "R-34", "RX-006")
            for t in extract(endpoints, [E[r + "-" + end] for r in rels for end in ("source", "target")]): shapes.add(t)
            admission = Graph().parse(ROOT / "ontology/shacl/0.3.0/admission.ttl")
            # Caller supplies expected entity classes independently of envelope declarations.
            participants = sorted([(n, str(cls).split("#")[-1]) for n, cls in spec["raw"].subject_objects(RDF.type)
                                   if cls in (RISK["RKM-X01"], RISK["RKM-C002"], RISK["RKM-C023"], RISK["RKM-C022"])], key=lambda x: str(x[0]))
            requests = []
            for i, (candidate, cid) in enumerate(participants):
                envelope, record, _ = fixture_record(cid, suffix="-coherence-" + str(i), candidate=candidate)
                for t in envelope: data.add(t)
                requests.append((record, cid))
            adm, _, _ = compile_request(admission, spec["raw"], requests, "managed-catalog", {x[1] for x in participants})
            for t in adm: shapes.add(t)
            row["admission_requests"] = [(str(n), cid) for n, cid in requests]
            row["endpoint_relations"] = list(rels)
        row["identity_map"] = aliases
        row["data_graph"] = graph_snapshot(data, registry); row["shapes_graph"] = graph_snapshot(shapes, registry)
        conforms, report, text = validate(data_graph=data, shacl_graph=shapes, inference="none", meta_shacl=True,
            do_owl_imports=False, advanced=False, abort_on_first=False, inplace=False)
        root = next(report.subjects(RDF.type, SH.ValidationReport))
        observed = [(str(report.value(n, SH.sourceShape)), str(report.value(n, SH.sourceConstraintComponent)),
                     str(report.value(n, SH.focusNode))) for n in report.objects(root, SH.result)]
        expected = {(a, b, aliases.get(c, c)) for a, b, c in spec["expected_findings"]}
        row.update(status="PASS" if set(observed) == expected and bool(conforms) == (not expected) else "FAIL",
            observed="CONFORMS" if conforms else "VIOLATES", violations=observed, expected_findings=sorted(expected),
            result_graph=graph_snapshot(report, registry), validation_text=text, engine_executed=True)
    except Exception as exc:
        row.update(status="ERROR", error=type(exc).__name__ + ": " + str(exc), engine_executed=False)
    return row


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    receipt = json.loads((PROFILE_DIR / "receipt.json").read_text()); module_path = PROFILE_DIR / "coherence.ttl"
    if (receipt["source_sha256"], receipt["contract_sha256"], receipt["shapes_sha256"]) != (
        digest(ROOT / "ontology/riskium-model.json"), digest(ROOT / "evaluation/coverage-review.json"), digest(module_path)):
        raise SystemExit("Source/contract/shapes digest mismatch")
    model = json.loads((ROOT / "ontology/riskium-model.json").read_text()); taxonomy = Graph()
    for g in model["generalizations"]: taxonomy.add((RISK[g["specific"]], RDFS.subClassOf, RISK[g["general"]]))
    module = Graph().parse(module_path); registry = {}; rows = []
    for spec in fixture_specs():
        result = execute(spec, module, taxonomy, registry); rows.append(result)
        if result["status"] != "PASS": print(json.dumps({k: result.get(k) for k in ("id", "status", "error", "violations", "expected_findings")}), flush=True)
    obligations = []
    for item in receipt["obligations"]:
        cases = [r for r in rows if r["constraint"] == item["source_element"]]
        obligations.append(dict(**item, outcome="PASS" if cases and all(r["status"] == "PASS" for r in cases) else "FAIL", case_ids=[r["id"] for r in cases]))
    inputs = ["ontology/riskium-model.json", "ontology/derived/riskium.owl.ttl", "evaluation/coverage-review.json",
        "ontology/shacl/0.4.0/coherence.ttl", "ontology/shacl/0.4.0/receipt.json", "tools/build_coherence_shapes.py",
        "tools/run_coherence_shacl.py", "tools/build_shacl.py", "tools/run_shacl.py", "tools/build_admission_shapes.py",
        "tools/run_admission_shacl.py", "tools/run_endpoint_shacl.py", "tools/build_endpoint_shapes.py",
        "ontology/shacl/0.2.0/endpoints.ttl", "ontology/shacl/0.3.0/admission.ttl", "tools/requirements-shacl.txt"]
    counts = Counter(r["status"] for r in rows)
    report = dict(title="Explicit context and revision coherence 0.4.0", source_commit=subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(), generated_at_utc=datetime.now(timezone.utc).isoformat(),
        runtime_python=sys.version.split()[0], engine={p: importlib.metadata.version(p) for p in ("pyshacl", "rdflib", "owlrl")},
        inputs={p: digest(ROOT / p) for p in inputs}, profiles={"raw": "staging only; no normalization or conformance claim", "managed": "explicit graph; asserted instance aliases; source taxonomy only; inference none; no imports or repairs"},
        coverage=dict(total=2, passed=sum(o["outcome"] == "PASS" for o in obligations), cases=len(rows), statuses=dict(counts)),
        graphs=registry, cases=rows, obligations=obligations,
        limitations=["Static C-24 graph conformance does not establish issued-content immutability or historical transaction behavior (#12/C-03).",
            "Only selected relation and admission integration is exercised; full conditional/multi-relation acceptance remains #5.",
            "No independent domain validation, source truth or overall semantic-correctness percentage follows."])
    (OUT / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    md = f"""# Explicit context and revision coherence — module 0.4.0

Source commit `{report['source_commit']}`. **{report['coverage']['passed']}/2 obligations PASS**, **{len(rows)} actual SHACL validations**, {counts.get('FAIL',0)} unexpected outcomes and {counts.get('ERROR',0)} errors. [Full JSON receipt](report.json) and [profile decisions](profile-review.md) preserve the scope and evidence.

C-23 requires the same explicit hasContext pair for every analyzedInContext pair, without inferring the reverse or repairing missing values. C-24 checks matching singleton entry targets, optional single predecessors, arbitrary recorded transitive cycles and same-entry lineage. Branches remain allowed. Cycles of 1, 2, 3, 8 and 17 nodes, alias collapse, raw conflicts, type/target errors and removed/reversed/weakened rules have separate outcomes. Four cases integrate selected endpoint shapes and application metadata admission for all participants. No whole-profile admission is claimed.

The JSON retains exact raw/data/shapes/result snapshots, normalized identity maps, expectations and code/input digests. Reconstruct data and shapes with `run_admission_shacl.reconstruct_pair()` and its shared blank-node context. Engine inference is none, imports disabled, only pinned source taxonomy appended. Instance schema/import assertions and reserved-vocabulary aliases reject before SHACL; raw retains them. The conceptual model, OWL and coverage contract are unchanged. Static graph checks do not prove historical immutability or independent semantic correctness.

| Case | Constraint | Profile | Mutation | Expected | Observed | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
"""
    for r in rows:
        md += f"| `{r['id']}` | {r['constraint']} | {r['profile']} | {r['mutation'] or '—'} | {'VIOLATES' if r['expected_findings'] else 'CONFORMS'} | {r.get('observed','ERROR')} | {r['status']} |\n"
    md += "\nReproduce with `tools/build_coherence_shapes.py`, `tools/run_coherence_shacl.py` and `tools/summarize_shacl.py` in the pinned SHACL environment. Parent #5 retains C-08 compatibility, other constraint routes and complete integration.\n"
    (OUT / "report.md").write_text(md)
    print(json.dumps(report["coverage"]), flush=True)
    if any(r["status"] != "PASS" for r in rows): raise SystemExit(1)


if __name__ == "__main__": main()
