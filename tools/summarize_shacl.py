"""Reconcile source-bound SHACL module receipts against the fixed 359-row baseline."""
import hashlib
import gzip
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"evaluation/shacl"


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    paths=[OUT/"report.json",OUT/"endpoints/report.json",OUT/"admission/report.json.gz"]
    baseline_path=ROOT/"evaluation/coverage-review.json"
    model_path=ROOT/"ontology/riskium-model.json"
    baseline=[r for r in json.loads(baseline_path.read_text())["obligation_reviews"] if r["engine"]=="SHACL"]
    if len(baseline)!=359:raise SystemExit("SHACL denominator changed")
    reports=[json.loads(gzip.decompress(p.read_bytes()).decode()) if p.suffix==".gz"
             else json.loads(p.read_text()) for p in paths]
    evidence=[];merged={}
    for path,report in zip(paths,reports):
        if report["inputs"]["ontology/riskium-model.json"]!=digest(model_path) or report["inputs"]["evaluation/coverage-review.json"]!=digest(baseline_path):
            raise SystemExit("Cannot merge receipts from different source/contract snapshots")
        relative=path.relative_to(ROOT).as_posix()
        evidence.append(dict(path=relative,sha256=digest(path),source_commit=report["source_commit"]))
        for o in report["obligations"]:
            if o["outcome"]=="NOT_RUN":continue
            identifier=o["id"]
            if identifier in merged:raise SystemExit("Overlapping adjudicated obligation: "+identifier)
            merged[identifier]=dict(outcome=o["outcome"],source_element=o["source_element"],
                evidence=relative,case_ids=o["case_ids"])
    rows=[]
    for b in baseline:
        item=merged.get(b["obligation_id"],dict(outcome="NOT_RUN",evidence=None,case_ids=[]))
        if item.get("source_element",b["source_element"])!=b["source_element"]:
            raise SystemExit("Obligation source identity mismatch")
        rows.append(dict(id=b["obligation_id"],source_element=b["source_element"],family=b["family"],
                         **{k:v for k,v in item.items() if k!="source_element"}))
    counts=Counter(r["outcome"] for r in rows)
    result=dict(status="MODULE_EXECUTION_COVERAGE_NOT_FULL_PROFILE_OR_SEMANTIC_VALIDITY",baseline=359,
        source_sha256=digest(model_path),contract_sha256=digest(baseline_path),evidence=evidence,
        outcomes=dict(counts),pass_percent=round(counts["PASS"]/359*100,2),
        exercised_including_partial_percent=round((counts["PASS"]+counts["PARTIAL"])/359*100,2),
        families={k:dict(Counter(r["outcome"] for r in rows if r["family"]==k)) for k in sorted({r["family"] for r in rows})},
        limitations=["Conditional profiles and cardinality module are executed separately; 127 relation pairs have endpoint integration tests.",
            "Catalog metadata admission is scoped to CatalogInspection, not risk assessment; full conditional/multi-relation integration remains pending.",
            "C-08 unit/scale compatibility remains PARTIAL/BLOCKED.",
            "Coverage percentages do not measure overall semantic correctness."],obligations=rows)
    (OUT/"coverage-status.json").write_text(json.dumps(result,indent=2)+"\n")
    md=f"""# SHACL module execution coverage

This is the current source-bound execution ledger for conceptual model 0.3.1. It combines the [conditional profile batch](report.md) [ordered endpoint batch](endpoints/report.md) and [catalog metadata admission batch](admission/report.md). The [JSON ledger](coverage-status.json) pins their exact digests and each obligation's case references. All receipts use the same conceptual source and 359-row coverage contract; no historical pass from another model is imported.

| Measure | Result |
| --- | ---: |
| Baseline obligations | 359 |
| PASS within declared module scope | {counts['PASS']} |
| PARTIAL | {counts['PARTIAL']} |
| NOT_RUN | {counts['NOT_RUN']} |
| PASS coverage | {result['pass_percent']}% |
| Exercised including partial | {result['exercised_including_partial_percent']}% |

| Family | PASS | PARTIAL | NOT_RUN |
| --- | ---: | ---: | ---: |
"""
    for name,values in result["families"].items():md+=f"| {name} | {values.get('PASS',0)} | {values.get('PARTIAL',0)} | {values.get('NOT_RUN',0)} |\n"
    md+="""
The endpoint batch executes all 254 ordered ends with isolated cardinality controls and paired-end integration for all 127 typed relations. The earlier conditional profiles retain three scoped passes and C-08's partial result. Their fixture populations differ; this ledger reports obligation coverage, not full-profile acceptance of arbitrary records. All 80 catalog-admission rows now have scoped metadata or boundary-exclusion evidence. The 21 other constraint rows remain NOT_RUN. Global integration across relations and conditional profiles still needs separate fixtures.

The next batch implements remaining constraint routes and full managed-profile integration. Catalog admission supports metadata inspection only, not risk-assessment readiness. Unit/scale compatibility needs an approved schema. Requirement/CQ outcomes, independent semantic judgments and real-world case adequacy are governed by the [semantic assurance plan](../semantic-assurance-plan.md).

Reproduce after running the respective suites:

```sh
python3 tools/summarize_shacl.py
```

## Complete 359-row ledger

| Obligation | Source | Outcome | Evidence |
| --- | --- | --- | --- |
"""
    for r in rows:
        link="[admission receipt](admission/report.md)" if r["evidence"] and "/admission/" in r["evidence"] else "[endpoint receipt](endpoints/report.md)" if r["evidence"] and "/endpoints/" in r["evidence"] else "[conditional receipt](report.md)" if r["evidence"] else "—"
        md+=f"| `{r['id']}` | `{r['source_element']}` | {r['outcome']} | {link} |\n"
    (OUT/"coverage-status.md").write_text(md)
    print(json.dumps({k:result[k] for k in ("outcomes","pass_percent","exercised_including_partial_percent")}))


if __name__=="__main__":main()
