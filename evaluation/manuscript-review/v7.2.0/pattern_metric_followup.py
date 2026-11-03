"""Bounded follow-up to the manuscript's OntoUML and design observations.

The catalogue triggers are review prompts, never automatic defect verdicts. The
Ensan--Du semantic metrics are deliberately not computed from catalog edges.
"""
from collections import Counter, defaultdict
from itertools import combinations, permutations
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
MODEL = REPO / "ontology/riskium-model.json"
NATIVE = REPO / "evaluation/native-review-decisions.json"
BASE = HERE.parent / "v7.1.0/supplement/pattern-report.json"
STRUCTURE = HERE.parent / "v7.1.0/supplement/structural-report.json"
CATALOGUE = "https://ontouml.readthedocs.io/en/latest/anti-patterns/"
THESIS = "https://www.collectionscanada.gc.ca/obj/thesescanada/vol2/002/NR89158.PDF"
M = json.loads(MODEL.read_text())
N = json.loads(NATIVE.read_text())
P = json.loads(BASE.read_text())
S = json.loads(STRUCTURE.read_text())
classes = {x["id"]: x for x in M["concepts"] + M["imported_types"] if x.get("scope_layer") == "FORMAL_CORE" or x["id"].startswith("EXT-")}
assocs = [a for a in M["associations"] if a["source"] in classes and a["target"] in classes]
gens = M["generalizations"]
st = lambda x: (classes[x].get("ontouml_stereotype") or "").lower()
byid = {a["id"]: a for a in assocs}
parents = defaultdict(set)
for g in gens:
    parents[g["specific"]].add(g["general"])


def ancestors(x):
    found = set()
    pending = list(parents[x])
    while pending:
        p = pending.pop()
        if p not in found:
            found.add(p)
            pending.extend(parents[p])
    return found


anc = {c: ancestors(c) for c in classes}
sub = lambda a, b: a == b or b in anc[a]


def upper(card):
    n = card.split("..")[-1]
    return float("inf") if n == "*" else int(n)


def lower(card):
    return int(card.split("..")[0])


def candidate(family, ids, interpretation):
    return dict(family=family, ids=ids, rule_url=CATALOGUE + family + "/index.html",
                trigger_interpretation=interpretation,
                disposition="SEMANTIC_ADJUDICATION_PENDING",
                reviewer="Automated structural screen; no independent semantic reviewer",
                provenance="pinned model and generated report; no assertion of a defect or model edit")


def selected():
    out = []
    reasons = {
        "GSRig": "A generalization set contains both rigid and anti-rigid children under the selected trigger.",
        "RepRel": "A relator has two mediation paths with repeatable relator-end cardinality under the selected trigger.",
        "ImpAbs": "The selected association/cardinality and subtype structure may conceal an implicit abstraction.",
        "BinOver": "The selected conservative overlap test found potentially overlapping endpoint types.",
        "RelSpec": "Endpoint specialization makes an association pair a potential relation-specialization review prompt."
    }
    for family, entry in P["anti_patterns"].items():
        for item in entry["candidates"]:
            ids = item if isinstance(item, list) else [item]
            out.append(candidate(family, ids, reasons[family]))
    return out


def additional():
    results = {}
    # DecInt: actual multiple concrete parents; a simple multi-parent count is not enough.
    results["DecInt"] = [candidate("DecInt", [x] + sorted(parents[x]),
        "Multiple direct concrete parents; covering and extension conditions still need semantic review.")
        for x in sorted(classes) if sum(not classes[p].get("is_abstract", False) for p in parents[x]) >= 2]
    mediation = defaultdict(list)
    for a in assocs:
        if a.get("stereotype") == "mediation":
            if st(a["source"]) == "relator":
                mediation[a["target"]].append((a["source"], a["id"], a["target_end_cardinality"]))
            if st(a["target"]) == "relator":
                mediation[a["source"]].append((a["target"], a["id"], a["source_end_cardinality"]))
    # FreeRole: a directly mediated role with a role subtype lacking its own mediation.
    results["FreeRole"] = [candidate("FreeRole", [parent, child],
        "Directly mediated parent role and unmediated child role; alternative inherited paths need review.")
        for parent, child in sorted((g["general"], g["specific"]) for g in gens)
        if st(parent) == st(child) == "role" and mediation[parent] and not mediation[child]]
    # MultDep: distinct non-specializing relators connected directly to the same bearer.
    results["MultDep"] = [candidate("MultDep", [bearer, a[0], b[0], a[1], b[1]],
        "A bearer is directly mediated by two unrelated relators; whether both are essential is unreviewed.")
        for bearer, mm in sorted(mediation.items()) for a, b in combinations(sorted(mm), 2)
        if not sub(a[0], b[0]) and not sub(b[0], a[0])]
    # RelOver: the two mediated bearer types must overlap and the summed bound exceed two.
    relators = defaultdict(list)
    for bearer, mm in mediation.items():
        for relator, relation, bound in mm:
            relators[relator].append((bearer, relation, bound))
    results["RelOver"] = [candidate("RelOver", [r, a[0], b[0], a[1], b[1]],
        "Mediated types have a known common subtype/ancestry and cardinality sum above two; actual overlap is unverified.")
        for r, mm in sorted(relators.items()) for a, b in combinations(sorted(mm), 2)
        if (sub(a[0], b[0]) or sub(b[0], a[0]) or any(sub(z,a[0]) and sub(z,b[0]) for z in classes))
        and upper(a[2]) + upper(b[2]) > 2]
    # Relation composition is a topology and cardinality prompt, not an entailment proof.
    results["RelComp"] = [candidate("RelComp", [a["id"], b["id"]],
        "The second association has both endpoints below one end of the first; a positive and plural bound holds at that end.")
        for a, b in permutations(assocs, 2)
        if any(lower(a[end]) > 0 and upper(a[end]) > 1 and sub(b["source"], a[side]) and sub(b["target"], a[side])
               for side, end in [("target", "target_end_cardinality"), ("source", "source_end_cardinality")])]
    return results


def main():
    assert hashlib.sha256(MODEL.read_bytes()).hexdigest() == P["model_sha256"] == N["source_model_sha256"]
    assert len(P["controls"]) == 6 and all(c["status"] == "PASS" for c in P["controls"])
    assert len(M["domains"]) == 11 and len(S["rows"]) == 11
    found = selected()
    assert len(found) == sum(x["count"] for x in P["anti_patterns"].values()) == 97
    newer = additional()
    no_feature = {
        "HetColl": "No memberOf meronymic relation in the pinned typed-core associations.",
        "HomoFunc": "No componentOf meronymic relation in the pinned typed-core associations.",
        "PartOver": "No meronymic relation in the pinned typed-core associations.",
        "WholeOver": "No meronymic relation in the pinned typed-core associations.",
        "MixIden": "No mixin-stereotyped class in the pinned typed core; roleMixins do not satisfy this rule's mixin precondition.",
        "UndefFormal": "No formal-stereotyped association in the pinned typed core; property/quality completeness is also unestablished.",
        "UndefPhase": "No phase-stereotyped class in the pinned typed core."
    }
    assert len(newer) == 5 and len(no_feature) == 7
    all_names = sorted(set(P["anti_patterns"]) | set(newer) | set(no_feature))
    assert len(all_names) == 20
    coverage = []
    for name in all_names:
        if name in P["anti_patterns"]:
            coverage.append(dict(name=name, status="REPLAYED_SELECTED_TRIGGER", count=P["anti_patterns"][name]["count"], source=CATALOGUE+name+"/index.html"))
        elif name in newer:
            coverage.append(dict(name=name, status="ADDITIONAL_BOUNDED_TRIGGER", count=len(newer[name]), source=CATALOGUE+name+"/index.html",
                                 caveat="Catalog-specific semantic conditions or complete native export may need further review."))
        else:
            coverage.append(dict(name=name, status="EXCLUDED_NO_REQUIRED_VOCABULARY", count=None, reason=no_feature[name], source=CATALOGUE+name+"/index.html"))
    allocation = []
    for d in M["domains"]:
        symbols = [x for x in d["concept_ids"] if x in classes]
        allocation.append(dict(subdomain=d["id"], title=d["title"], allocated_class_symbols=symbols,
                               allocated_property_symbols=None, allocated_axioms=None,
                               strong_local_dependencies=None, moderate_local_dependencies=None,
                               strong_external_dependencies=None, moderate_external_dependencies=None,
                               NSLD=None, NMLD=None, NSED=None, NMED=None, COH=None, COP=None,
                               reason="Subdomain catalog membership is not a separately scoped ontology module with allocated axioms, properties and interfaces."))
    report = dict(
      schema="riskium-pattern-metric-followup-v1", model_sha256=P["model_sha256"],
      model_version=M["version"], source_model_git_commit=P["repository_commit"],
      native_decisions_sha256=hashlib.sha256(NATIVE.read_bytes()).hexdigest(),
      selected_report_sha256=hashlib.sha256(BASE.read_bytes()).hexdigest(),
      structural_report_sha256=hashlib.sha256(STRUCTURE.read_bytes()).hexdigest(),
      catalogue=coverage, selected_candidates=found,
      additional_candidates={k:v for k,v in newer.items()},
      selected_controls=P["controls"],
      semantic_metric_method=dict(source=THESIS+" (chapter 7, definitions 7.3--7.10); Ensan and Du, Information Systems 38(5), 2013, doi:10.1016/j.is.2012.11.012",
        required="Axiom and concept/role-symbol allocation to explicit modules, local/external signatures, interfaces and semantic strong/moderate dependency sets under the source definitions.",
        available="Only catalog concept ownership and a derived single-ontology OWL graph; relations and axioms have not been allocated to executable modules with declared interfaces.",
        decision="NOT_COMPUTED_INVALID_DENOMINATOR_AND_SEMANTIC_INPUT",
        rationale="Even n(n-1) would count only local class names, omitting roles; association/generalization edges do not determine entailment-based strong/moderate dependencies. Inventing COH/COP would misattribute graph observations to Ensan--Du.",
        structural_columns="n/e/k/i/x/b are distinct observations in the pinned structural report, not semantic scores.",
        weights=None, uncertainty="Module partition and semantic dependence are undecided. No threshold or rank is justified.",
        by_subdomain=allocation),
      decision=dict(model_changed=False, actual_defects_confirmed=0,
          actual_defects_status="UNKNOWN_NO_INDEPENDENT_SEMANTIC_ADJUDICATION",
          selected_trigger_occurrences=len(found),
          additional_trigger_occurrences=sum(map(len,newer.values())),
          independent_reviewer="NOT_OBTAINED", next_owner="Issue #23 for independent interpretations; formal modularization is separate model/OWL compatibility work."))
    target = Path(sys.argv[1]) if len(sys.argv)>1 else HERE/"pattern-metric-followup.json"
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n")
    print(json.dumps(dict(path=str(target), selected=len(found), additional={k:len(v) for k,v in newer.items()}, coverage=len(coverage), controls=len(P["controls"]))))


if __name__ == "__main__":
    main()
