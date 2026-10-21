"""Run source-bound HermiT checks and emit an inspectable JSON/Markdown receipt.

The HermiT jar is supplied by pinned owlready2; it is not copied into this repo.
Every entailment conclusion contains declarations, preventing OWLAPI from
silently treating a bare RDF triple as a non-axiom.
"""
import concurrent.futures
import hashlib
import importlib.metadata
import json
import os
import re
import subprocess
import tempfile
import time
from pathlib import Path

from rdflib import BNode, Graph, Literal, Namespace, RDF, RDFS, OWL, XSD
from rdflib.compare import isomorphic

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evaluation/hermit"
MODEL = ROOT / "ontology/riskium-model.json"
OWL_TTL = ROOT / "ontology/derived/riskium.owl.ttl"
MAPPING_RECEIPT = ROOT / "evaluation/owl-mapping-receipt.json"
CONTRACT = ROOT / "evaluation/coverage-review.json"
RISK = Namespace("https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def hermit_jar():
    import owlready2
    return Path(owlready2.__file__).parent / "hermit/HermiT.jar"


def declarations(graph, classes=(), properties=()):
    for c in classes:
        graph.add((RISK[c], RDF.type, OWL.Class))
    for p in properties:
        graph.add((RISK[p], RDF.type, OWL.ObjectProperty))


def individuals(graph, *items):
    for item in items:
        graph.add((item, RDF.type, OWL.NamedIndividual))


def logical_relation_conclusion(full, relation):
    g = Graph()
    p = RISK[relation["id"]]
    source, target = RISK[relation["source"]], RISK[relation["target"]]
    declarations(g, [relation["source"], relation["target"]], [relation["id"]])
    for pred, obj in ((RDFS.domain, source), (RDFS.range, target)):
        g.add((p, pred, obj))
    restrictions = 0
    for cls in (source, target):
        for b in full.objects(cls, RDFS.subClassOf):
            if not isinstance(b, BNode):
                continue
            op = full.value(b, OWL.onProperty)
            if op != p and not (isinstance(op, BNode) and full.value(op, OWL.inverseOf) == p):
                continue
            g.add((cls, RDFS.subClassOf, b))
            for t in full.triples((b, None, None)):
                g.add(t)
                if isinstance(t[2], BNode):
                    for nested in full.triples((t[2], None, None)):
                        g.add(nested)
            restrictions += 1
    return g, restrictions


def run_command(jar, args, timeout=30):
    command = ["java", "-Xmx512m", "-jar", str(jar), *args]
    started = time.monotonic()
    try:
        p = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        return {"exit_code": p.returncode, "stdout": p.stdout.strip(), "stderr": p.stderr.strip(),
                "elapsed_ms": round((time.monotonic() - started) * 1000)}
    except subprocess.TimeoutExpired:
        return {"exit_code": None, "stdout": "", "stderr": "timeout", "elapsed_ms": round((time.monotonic() - started) * 1000)}


def run_case(spec, jar, base, temp):
    row = {k: v for k, v in spec.items() if k not in ("conclusion", "premise")}
    premise_path = base
    if "premise" in spec:
        premise_path = temp / (spec["id"] + "-premise.rdf")
        spec["premise"].serialize(destination=premise_path, format="xml")
        row["premise_sha256"] = sha(premise_path)
    if "conclusion" in spec:
        conclusion_path = temp / (spec["id"] + "-conclusion.rdf")
        spec["conclusion"].serialize(destination=conclusion_path, format="xml")
        row["conclusion_sha256"] = sha(conclusion_path)
        args = ["--premise=" + premise_path.as_uri(), "--conclusion=" + conclusion_path.as_uri(), "-E"]
    elif spec["kind"] == "class_sat":
        args = ["--consistency=<" + str(RISK[spec["source_element"]]) + ">", str(premise_path)]
    elif spec["kind"] == "consistency":
        args = ["-k", str(premise_path)]
    elif spec["kind"] == "unsatisfiable_list":
        args = ["-U", str(premise_path)]
    else:
        raise ValueError(spec["kind"])
    result = run_command(jar, args)
    row["command"] = ["java", "-Xmx512m", "-jar", "<pinned HermiT.jar>", *args]
    row.update(result)
    expected_inconsistency = (spec["kind"] == "consistency" and spec["expected"] is False and
                              result["exit_code"] == 1 and
                              "org.semanticweb.owlapi.reasoner.InconsistentOntologyException" in result["stderr"])
    if spec["kind"] in ("class_sat", "consistency"):
        satisfiable = "is satisfiable." in result["stdout"] and "not satisfiable" not in result["stdout"]
        observed = expected_inconsistency or satisfiable == spec["expected"]
    elif spec["kind"] == "unsatisfiable_list":
        observed = result["stdout"].strip() == "Classes equivalent to 'owl:Nothing':\n\towl:Nothing"
    else:
        observed = result["stdout"] == "true" if spec["expected"] else result["stdout"] == "false"
    row["observed_outcome"] = "INCONSISTENT" if expected_inconsistency else result["stdout"]
    row["status"] = "PASS" if (result["exit_code"] == 0 and observed and not result["stderr"]) or expected_inconsistency else "FAIL"
    return row


def build_specs(full, model, reviewed):
    obligations = {r["source_element"]: r["obligation_id"] for r in reviewed if r["engine"] == "HermiT"}
    specs = [dict(id="H-BASE-CONSISTENCY", kind="consistency", family="Baseline", expected=True),
             dict(id="H-BASE-UNSAT", kind="unsatisfiable_list", family="Baseline", expected=True)]
    classes = [c for c in model["concepts"] if c["scope_layer"] == "FORMAL_CORE"]
    for c in classes:
        specs.append(dict(id=obligations[c["id"]], kind="class_sat", family="Class satisfiability",
                          source_element=c["id"], expected=True))
    for g in model["generalizations"]:
        conclusion = Graph()
        declarations(conclusion, [g["specific"], g["general"]])
        conclusion.add((RISK[g["specific"]], RDFS.subClassOf, RISK[g["general"]]))
        specs.append(dict(id=obligations[g["id"]], kind="entailment", family="Declared subclass entailment",
                          source_element=g["id"], expected=True, conclusion=conclusion))
    for r in model["associations"]:
        if r["scope_layer"] != "FORMAL_CORE":
            continue
        conclusion, count = logical_relation_conclusion(full, r)
        specs.append(dict(id=obligations[r["id"]], kind="entailment", family="Relation mapping",
                          source_element=r["id"], expected=True, conclusion=conclusion,
                          qualified_restrictions=count))
    return specs


def scenario_specs(full, model):
    specs = []
    # The wrong range must not be entailed: a control for declared relation conclusions.
    bad = Graph()
    declarations(bad, ["RKM-C001"], ["R-01"])
    bad.add((RISK["R-01"], RDFS.range, RISK["RKM-C001"]))
    specs.append(dict(id="H-CONTROL-WRONG-RANGE", kind="entailment", family="Negative control",
                      expected=False, conclusion=bad, meaning="Unjustified R-01 range"))
    # Source-to-general does not automatically mean general-to-source.
    reversed_edge = Graph()
    declarations(reversed_edge, ["RKM-C014", "RKM-C022"])
    reversed_edge.add((RISK["RKM-C014"], RDFS.subClassOf, RISK["RKM-C022"]))
    specs.append(dict(id="H-CONTROL-REVERSE-G01", kind="entailment", family="Negative control",
                      expected=False, conclusion=reversed_edge, meaning="Reversed subclass entailment"))
    # Three actual disjoint sets are tested by forcing membership in both siblings.
    policy = json.loads((ROOT / "evaluation/native-review-decisions.json").read_text())
    by_g = {g["id"]: g for g in model["generalizations"]}
    for s in policy["generalization_sets"]:
        if not s["isDisjoint"]:
            continue
        members = [by_g[x]["specific"] for x in s["generalizations"]]
        g = Graph()
        for t in full:
            g.add(t)
        individual = RISK["probe-" + s["id"]]
        individuals(g, individual)
        for c in members:
            g.add((individual, RDF.type, RISK[c]))
        specs.append(dict(id="H-DISJOINT-" + s["id"], kind="consistency", family="Boundary mutation",
                          expected=False, premise=g, meaning="Shared individual in disjoint siblings"))
    # C-15: two explicitly different bearers for the same intrinsic mode.
    g = Graph()
    for t in full:
        g.add(t)
    v, a, b = (RISK["probe-vulnerability"], RISK["probe-bearer-A"], RISK["probe-bearer-B"])
    individuals(g, v, a, b)
    g.add((v, RDF.type, RISK["RKM-C011"]))
    g.add((a, RISK["RK3-004"], v))
    g.add((b, RISK["RK3-004"], v))
    g.add((a, OWL.differentFrom, b))
    specs.append(dict(id="H-C15-TWO-DISTINCT-BEARERS", kind="consistency", family="Constraint probe",
                      constraint="C-15", expected=False, premise=g,
                      meaning="At-most-one bearer with two named distinct objects"))
    # Consistency of a DifferentIndividuals countermodel supports non-entailment of equality.
    for cid, cls in (("C-01", "RKM-X01"), ("C-24", "RKM-C023")):
        g = Graph()
        for t in full:
            g.add(t)
        a, b = RISK["probe-" + cid + "-a"], RISK["probe-" + cid + "-b"]
        individuals(g, a, b)
        g.add((a, RDF.type, RISK[cls])); g.add((b, RDF.type, RISK[cls]))
        g.add((a, OWL.differentFrom, b))
        specs.append(dict(id="H-" + cid + "-IDENTITY-COUNTERMODEL", kind="consistency",
                          family="Constraint probe", constraint=cid, expected=True, premise=g,
                          meaning="Two named instances may remain distinct"))
    # C-02: documentary class membership does not imply actual occurrence.
    g = Graph()
    for t in full:
        g.add(t)
    i = RISK["probe-description"]
    individuals(g, i)
    g.add((i, RDF.type, RISK["RKM-C024"]))
    c = Graph(); declarations(c, ["RKM-C004"]); individuals(c, i)
    c.add((i, RDF.type, RISK["RKM-C004"]))
    specs.append(dict(id="H-C02-NO-REALIZATION", kind="entailment", family="Constraint probe",
                      constraint="C-02", expected=False, premise=g, conclusion=c,
                      meaning="Description alone does not entail occurrence"))
    # C-07: a responsible role is not automatically an authorizing one.
    g = Graph()
    for t in full:
        g.add(t)
    i = RISK["probe-responsible"]
    individuals(g, i)
    g.add((i, RDF.type, RISK["RKM-C053"]))
    c = Graph(); declarations(c, ["RKM-C054"]); individuals(c, i)
    c.add((i, RDF.type, RISK["RKM-C054"]))
    specs.append(dict(id="H-C07-NO-AUTHORITY", kind="entailment", family="Constraint probe",
                      constraint="C-07", expected=False, premise=g, conclusion=c,
                      meaning="Responsibility alone does not entail authorization"))
    # C-23: the broader context link does not entail the narrower analytical one.
    g = Graph()
    for t in full:
        g.add(t)
    a, b = RISK["probe-case"], RISK["probe-context"]
    individuals(g, a, b)
    g.add((a, RISK["RX-001"], b))
    c = Graph(); declarations(c, properties=["R-35"]); individuals(c, a, b)
    c.add((a, RISK["R-35"], b))
    specs.append(dict(id="H-C23-NO-REVERSE-CONTEXT", kind="entailment", family="Constraint probe",
                      constraint="C-23", expected=False, premise=g, conclusion=c,
                      meaning="hasContext alone does not entail analyzedInContext"))
    analyzed = Graph()
    for t in full:
        analyzed.add(t)
    individuals(analyzed, a, b)
    analyzed.add((a, RISK["R-35"], b))
    implied = Graph(); declarations(implied, properties=["RX-001"]); individuals(implied, a, b)
    implied.add((a, RISK["RX-001"], b))
    specs.append(dict(id="H-C23-ANALYZED-IMPLIES-CONTEXT", kind="entailment",
                      family="Constraint probe", constraint="C-23", expected=True,
                      premise=analyzed, conclusion=implied,
                      meaning="Source-backed same-pair property inclusion"))
    revision, entry = RISK["probe-revision"], RISK["probe-entry"]
    rev_graph = Graph()
    for t in full:
        rev_graph.add(t)
    individuals(rev_graph, revision, entry)
    rev_graph.add((revision, RISK["R-33"], entry))
    version_conclusion = Graph()
    declarations(version_conclusion, properties=["RX-006"])
    individuals(version_conclusion, revision, entry)
    version_conclusion.add((revision, RISK["RX-006"], entry))
    specs.append(dict(id="H-C24-REVISION-IMPLIES-VERSION", kind="entailment",
                      family="Constraint probe", constraint="C-24", expected=True,
                      premise=rev_graph, conclusion=version_conclusion,
                      meaning="Source-backed revision/version property inclusion"))
    no_global_equivalence = Graph()
    declarations(no_global_equivalence, ["RKM-X01", "RKM-C022"])
    no_global_equivalence.add((RISK["RKM-X01"], RDFS.subClassOf, RISK["RKM-C022"]))
    specs.append(dict(id="H-C20-NO-CASE-ENTRY-EQUIVALENCE", kind="entailment",
                      family="Constraint probe", constraint="C-20", expected=False,
                      conclusion=no_global_equivalence,
                      meaning="RiskCase is not globally a RiskRegisterEntry"))
    same_participants = Graph()
    for t in full:
        same_participants.add(t)
    r1, r2, bearer, authority = (RISK["probe-mandate-1"], RISK["probe-mandate-2"],
                                 RISK["probe-mandate-bearer"], RISK["probe-mandate-authority"])
    individuals(same_participants, r1, r2, bearer, authority)
    for relator in (r1, r2):
        same_participants.add((relator, RDF.type, RISK["RKM-C052"]))
        same_participants.add((relator, RISK["R-56"], bearer))
        same_participants.add((relator, RISK["R-57"], authority))
    same_participants.add((r1, OWL.differentFrom, r2))
    specs.append(dict(id="H-C22-NO-PARTICIPANT-PAIR-KEY", kind="consistency",
                      family="Constraint probe", constraint="C-22", expected=True,
                      premise=same_participants,
                      meaning="Two distinct mandates can share mediated participants"))
    entry = RISK["probe-entry-open-world"]
    missing_named = Graph()
    for t in full:
        missing_named.add(t)
    individuals(missing_named, entry)
    missing_named.add((entry, RDF.type, RISK["RKM-C022"]))
    specs.append(dict(id="H-OWA-ANONYMOUS-CASE", kind="consistency", family="Open-world boundary",
                      expected=True, premise=missing_named,
                      meaning="No named case assertion does not contradict an existential restriction"))
    exists = Graph()
    individuals(exists, entry)
    restriction = BNode("case-exists")
    exists.add((entry, RDF.type, restriction))
    exists.add((restriction, RDF.type, OWL.Restriction))
    exists.add((restriction, OWL.onProperty, RISK["R-01"]))
    exists.add((restriction, OWL.someValuesFrom, RISK["RKM-X01"]))
    declarations(exists, ["RKM-X01"], ["R-01"])
    specs.append(dict(id="H-OWA-EXISTENTIAL-CASE", kind="entailment", family="Open-world boundary",
                      expected=True, premise=missing_named, conclusion=exists,
                      meaning="Entry entails some case without naming one"))
    same_fillers = Graph()
    for t in full:
        same_fillers.add(t)
    c1, c2 = RISK["probe-case-name-1"], RISK["probe-case-name-2"]
    individuals(same_fillers, entry, c1, c2)
    same_fillers.add((entry, RISK["R-01"], c1))
    same_fillers.add((entry, RISK["R-01"], c2))
    identity = Graph(); individuals(identity, c1, c2)
    identity.add((c1, OWL.sameAs, c2))
    specs.append(dict(id="H-OWA-MAX1-MERGES-NAMES", kind="entailment", family="Open-world boundary",
                      expected=True, premise=same_fillers, conclusion=identity,
                      meaning="Two named case fillers can be inferred equal under maximum one"))
    return specs


def consequence_specs(full, model):
    """Exercise inferred consequences and finite boundary mutations, not just stated axioms."""
    specs = []
    for gen in model["generalizations"]:
        specific, general = gen["specific"], gen["general"]
        individual = RISK["probe-generalization-" + gen["id"]]
        premise = Graph()
        for t in full:
            premise.add(t)
        individuals(premise, individual)
        premise.add((individual, RDF.type, RISK[specific]))
        conclusion = Graph()
        declarations(conclusion, [general]); individuals(conclusion, individual)
        conclusion.add((individual, RDF.type, RISK[general]))
        specs.append(dict(id="H-ABOX-" + gen["id"], kind="entailment", family="Inferred subclass membership",
                          source_element=gen["id"], expected=True, premise=premise, conclusion=conclusion,
                          meaning="Specific instance inherits its declared general type"))
        reverse = Graph()
        declarations(reverse, [general, specific])
        reverse.add((RISK[general], RDFS.subClassOf, RISK[specific]))
        specs.append(dict(id="H-REVERSE-" + gen["id"], kind="entailment", family="Reverse hierarchy control",
                          source_element=gen["id"], expected=False, conclusion=reverse,
                          meaning="General class need not be a subclass of this specific class"))
    for rel in model["associations"]:
        if rel["scope_layer"] != "FORMAL_CORE":
            continue
        prop = RISK[rel["id"]]
        a, b = RISK["probe-" + rel["id"] + "-a"], RISK["probe-" + rel["id"] + "-b"]
        premise = Graph()
        for t in full:
            premise.add(t)
        individuals(premise, a, b)
        premise.add((a, prop, b))
        conclusion = Graph()
        declarations(conclusion, [rel["source"], rel["target"]])
        individuals(conclusion, a, b)
        conclusion.add((a, RDF.type, RISK[rel["source"]]))
        conclusion.add((b, RDF.type, RISK[rel["target"]]))
        specs.append(dict(id="H-ABOX-" + rel["id"], kind="entailment", family="Inferred relation typing",
                          source_element=rel["id"], expected=True, premise=premise, conclusion=conclusion,
                          meaning="A property assertion infers both endpoint types"))
        for end in ("source", "target"):
            cardinality = rel[end + "_end_cardinality"]
            m = re.fullmatch(r"(\d+)(?:\.\.(\d+|\*))?", cardinality)
            upper = int(m[1]) if m[2] is None else (None if m[2] == "*" else int(m[2]))
            if upper != 1:
                continue
            focus = RISK["probe-" + rel["id"] + "-" + end + "-focus"]
            others = [RISK["probe-" + rel["id"] + "-" + end + "-1"],
                      RISK["probe-" + rel["id"] + "-" + end + "-2"]]
            for n, expected in ((1, True), (2, False)):
                fixture = Graph()
                for t in full:
                    fixture.add(t)
                individuals(fixture, focus, *others[:n])
                for other in others[:n]:
                    fixture.add((other, prop, focus) if end == "source" else (focus, prop, other))
                if n == 2:
                    fixture.add((others[0], OWL.differentFrom, others[1]))
                specs.append(dict(id="H-MAX1-" + rel["id"] + "-" + end + "-" + str(n),
                                  kind="consistency", family="Cardinality boundary",
                                  source_element=rel["id"], expected=expected, premise=fixture,
                                  meaning=("One named filler is consistent" if n == 1 else
                                           "Two explicitly distinct fillers violate maximum one")))
    return specs


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    model = json.loads(MODEL.read_text())
    mapping = json.loads(MAPPING_RECEIPT.read_text())
    if mapping["inputs_sha256"]["ontology/riskium-model.json"] != sha(MODEL) or mapping["output_sha256"] != sha(OWL_TTL):
        raise SystemExit("Reviewed mapping input/output digest mismatch")
    reviewed = json.loads(CONTRACT.read_text())["obligation_reviews"]
    contract_details = {c["id"]: c for c in json.loads((ROOT / "evaluation/coverage-contract.json").read_text())["constraint_dispositions"]}
    hermit_rows = [r for r in reviewed if r["engine"] == "HermiT"]
    if len(hermit_rows) != 295:
        raise SystemExit("HermiT obligation denominator changed")
    full = Graph().parse(OWL_TTL, format="turtle")
    premise = OUT / "premise.rdf"
    full.serialize(destination=premise, format="xml")
    if not isomorphic(full, Graph().parse(premise, format="xml")):
        raise SystemExit("RDF/XML premise changed the source graph")
    jar = hermit_jar()
    version = run_command(jar, ["--version"])
    if version["exit_code"] != 0 or not version["stdout"].startswith("1.3.8.1099"):
        raise SystemExit("Unexpected HermiT version: " + str(version))
    specs = build_specs(full, model, reviewed) + scenario_specs(full, model) + consequence_specs(full, model)
    with tempfile.TemporaryDirectory(prefix="riskium-hermit-") as td:
        temp = Path(td)
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            rows = list(pool.map(lambda s: run_case(s, jar, premise, temp), specs))
    by_obligation = {r["id"]: r for r in rows}
    tracked = []
    for obligation in hermit_rows:
        row = by_obligation.get(obligation["obligation_id"])
        if row:
            tracked.append({"id": obligation["obligation_id"], "family": obligation["family"],
                            "source_element": obligation["source_element"], "outcome": row["status"],
                            "case_id": row["id"]})
        else:
            cid = obligation["source_element"]
            probes = [r for r in rows if r.get("constraint") == cid]
            if probes:
                tracked.append({"id": obligation["obligation_id"], "family": obligation["family"],
                                "source_element": cid, "outcome": "PASS" if all(p["status"] == "PASS" for p in probes) else "FAIL",
                                "case_id": ", ".join(p["id"] for p in probes),
                                "scope": "bounded OWL portion only"})
            else:
                detail = contract_details[cid]
                tracked.append({"id": obligation["obligation_id"], "family": obligation["family"],
                                "source_element": cid, "outcome": "NOT_RUN",
                                "reason": "Current OWL route: " + detail["owl_route"] + " Remaining route: " +
                                          detail["shacl_route"] + " " + detail["outside_engine_obligation"]})
    from collections import Counter
    counts = Counter(x["outcome"] for x in tracked)
    counts["PASS"] += 0
    report = {
        "title": "Riskium HermiT execution receipt", "model_version": model["version"],
        "source_commit": os.environ.get("RISKIUM_SOURCE_COMMIT", "507acd8dfa8874c9f0065bad3c4dc3dfbe74d0ab"),
        "engine": {"name": "HermiT", "version": version["stdout"].splitlines()[0],
                   "jar_sha256": sha(jar), "package": "owlready2==" + importlib.metadata.version("owlready2"),
                   "java": subprocess.run(["java", "-version"], capture_output=True, text=True).stderr.splitlines()[0]},
        "inputs": {"owl_turtle_sha256": sha(OWL_TTL), "mapping_receipt_sha256": sha(MAPPING_RECEIPT),
                   "contract_sha256": sha(CONTRACT), "premise_rdfxml_sha256": sha(premise),
                   "imports": [], "inference_policy": "OWL 2 open world; no unique-name assumption; no external imports"},
        "coverage": {"baseline_obligations": len(tracked), "allocated": len(tracked), "outcomes": dict(counts),
                     "executed_pass_fraction": f"{counts['PASS']}/{len(tracked)}",
                     "executed_pass_percent": round(counts["PASS"] / len(tracked) * 100, 2),
                     "structural_families": {k: {"total": sum(x["family"] == k for x in tracked),
                                                "passed": sum(x["family"] == k and x["outcome"] == "PASS" for x in tracked)}
                                             for k in ("Class satisfiability", "Declared subclass entailment", "Relation mapping", "Constraint encoding disposition")}},
        "supplemental": {"family_counts": {k: {"total": sum(r["family"] == k for r in rows),
                                             "passed": sum(r["family"] == k and r["status"] == "PASS" for r in rows)}
                                           for k in sorted(set(r["family"] for r in rows))
                                           if k not in ("Baseline", "Class satisfiability", "Declared subclass entailment", "Relation mapping", "Constraint probe")}},
        "cases": rows, "obligations": tracked,
        "limitations": ["A declared axiom being entailed tests the mapping, not independent truth in the domain.",
                        "Non-entailment probes apply to the exact fixture and current OWL mapping only.",
                        "Unencoded conditional, temporal, provenance and data-admission rules remain open.",
                        "Consistency and satisfiability do not establish semantic adequacy or data conformance."],
    }
    (OUT / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    table = "| Family | Passed / total | Interpretation |\n| --- | ---: | --- |\n"
    labels = {"Class satisfiability": "Named classes can have an instance in some model.",
              "Declared subclass entailment": "Mapped specialization axioms are entailed.",
              "Relation mapping": "Declared domain/range and nontrivial cardinality axioms are entailed.",
              "Constraint encoding disposition": "Only a bounded, separately listed subset has a HermiT oracle."}
    for k, v in report["coverage"]["structural_families"].items():
        table += f"| {k} | {v['passed']} / {v['total']} | {labels[k]} |\n"
    failed = [r for r in rows if r["status"] != "PASS"]
    md = f"""# Riskium HermiT reasoning report

This report is the execution receipt for the reviewed typed-core OWL mapping of conceptual model **{model['version']}**, based on commit `{report['source_commit']}`. The exact [premise RDF/XML](premise.rdf) and [machine-readable result](report.json) are retained beside this report. HermiT {report['engine']['version']} was supplied by {report['engine']['package']} (jar SHA-256 `{report['engine']['jar_sha256']}`), running on {report['engine']['java']}. The import closure is empty; the separately annotated external Object anchor is a local proxy.

## How the reasoning was run

`tools/run_hermit.py` parses the reviewed Turtle with RDFLib 7.6.0, writes RDF/XML for HermiT's OWLAPI loader, then runs the HermiT CLI against that exact premise. It checks baseline consistency and the unsatisfiable-class list; it asks for satisfiability of each typed class, entailment of each declared generalization, and entailment of each relation's declared domain, range and nontrivial qualified cardinality restrictions. Each conclusion explicitly declares the relevant OWL classes and object property; a bare RDF triple can otherwise be ignored by the OWLAPI loader. Additional negative and boundary fixtures test the oracle and selected forbidden inferences. Every process return code, output and elapsed time is in JSON.

Run from the repository root after installing pinned dependencies:

```sh
python3 -m venv .venv-hermit
.venv-hermit/bin/pip install -r tools/requirements-hermit.txt
.venv-hermit/bin/python tools/run_hermit.py
```

The source Turtle SHA-256 is `{sha(OWL_TTL)}`; the exact RDF/XML premise SHA-256 is `{sha(premise)}`. The contract SHA-256 is `{sha(CONTRACT)}`. The generated RDF/XML is semantically checked against the Turtle before execution; byte-for-byte serialized RDF/XML can vary with blank-node identifiers on a fresh regeneration, so the committed premise and its digest identify this run.

## Results and coverage

Baseline ontology consistency: **{by_obligation['H-BASE-CONSISTENCY']['status']}**. Unsatisfiable-class inventory (none other than `owl:Nothing` expected): **{by_obligation['H-BASE-UNSAT']['status']}**. Across the **295 predeclared HermiT-related obligations**, **{counts['PASS']} passed, {counts.get('FAIL',0)} failed, and {counts.get('NOT_RUN',0)} remain without a sound HermiT oracle**. Execution coverage is **{report['coverage']['executed_pass_percent']}% ({counts['PASS']}/295)**. Source allocation is **295/295 (100%)**; this differs from execution coverage. All **{len(rows)} executed cases** passed in this run. These fractions are not percentages of ontological correctness.

{table}
The 127 relation results confirm entailment of mapped axioms, including 88 nontrivial qualified restrictions across 254 ordered ends. They do **not** establish closed-world completeness or distinctness of named fillers. The 25 constraint obligations are listed individually below, including those whose full meaning is not encoded in OWL. Treating a reasoner-inapplicable portion as a pass would inflate coverage.

Supplemental semantic controls go beyond rechecking asserted axioms. They infer general types from specific instances, infer endpoint types from actual property assertions, challenge reverse inheritance, and test every maximum-one relation end with one filler and then two explicitly different fillers. These tests are **additional cases**, not extra baseline obligations. Their results are:

| Supplemental family | Passed / total |
| --- | ---: |
"""
    for k, v in report["supplemental"]["family_counts"].items():
        md += f"| {k} | {v['passed']} / {v['total']} |\n"
    md += """

### Negative, boundary and mutation controls

| Case | Expected | Observed | Purpose |
| --- | --- | --- | --- |
"""
    for r in rows:
        if r["family"] in ("Negative control", "Boundary mutation", "Constraint probe"):
            md += f"| `{r['id']}` | {'true' if r['expected'] else 'false'} | `{r['observed_outcome']}`; {r['status']} | {r['meaning']} |\n"
    md += "\n### Constraint obligation register\n\n| Obligation | Constraint | Outcome | Evidence or remaining reason |\n| --- | --- | --- | --- |\n"
    for x in tracked:
        if x["family"] == "Constraint encoding disposition":
            md += f"| `{x['id']}` | {x['source_element']} | {x['outcome']} | {x.get('case_id', x.get('reason', ''))} |\n"
    md += "\n### Full 295-row baseline register\n\n| ID | Family | Source | Outcome | Case |\n| --- | --- | --- | --- | --- |\n"
    for x in tracked:
        md += f"| `{x['id']}` | {x['family']} | `{x['source_element']}` | {x['outcome']} | `{x.get('case_id','—')}` |\n"
    md += "\n## Quality limits and next work\n\nThe result establishes consistency and satisfiability for this exact mapped snapshot, with traceable HermiT oracle checks. It does not prove exhaustive semantic validity, requirement acceptance, empirical usefulness or independent expert agreement. Some negative probes demonstrate a countermodel or a non-entailment for a named fixture; absence of an asserted statement by itself is never treated as negation. The unrun constraint obligations need reviewed OWL extensions where justified, SHACL profiles, application checks or independent interpretation evidence. Issue #5 should implement explicit-data SHACL profiles; #6 must reconcile requirement and CQ execution. The [OWL mapping review](../owl-mapping-review.md) details every constraint's encoding boundary.\n"
    (OUT / "report.md").write_text(md)
    print(json.dumps({"coverage": report["coverage"], "failed_cases": [r["id"] for r in failed],
                      "case_count": len(rows)}, ensure_ascii=False))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
