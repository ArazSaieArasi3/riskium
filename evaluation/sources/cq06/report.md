# Executed source-backed CQ06 trace packet

**Scoped source-trace query evidence; no native managed-case admission, independent semantic acceptance or owner judgment.**

Execution checkout `4b1d9f221a118494d19906893141de10efd18eac`; prior source/oracle freeze `2542c5b0762c4390c2d5af132fe52a01249fe2fc`. [Cohort and inspected-source/rights policy](README.md); [complete receipt](report.json.gz). Exact code/input/graph/query hashes and answer/finding oracles are retained.

Engine: {"name": "RDFLib SPARQL SELECT", "version": "7.6.0", "python": "3.12.14", "inference": "none", "remote_service": false}. Automated replay uses the frozen selected source data; primary PDF inspection is separately recorded in inspection.json, not falsely repeated by CI.

Summary: {"source_documents": 2, "sourced_records": 13, "withheld_case_admissions": 11, "managed_cases_admitted": 0, "scenarios": 35, "actual_query_executions": 35, "source_query_cases": 14, "synthetic_negative_cases": 16, "query_mutants_detected": 3, "guard_mutation_controls": 1, "identity_controls": 1, "statuses": {"PASS": 35}}. Source-backed records and deliberately synthetic failures/mutants are separate populations. A raw query can retrieve coherent forged metadata; frozen-cohort inspection checks reject it. Queries alone do not prove source truth.

| Case | Population/control | Raw answers | Task accepted | Verdict |
| --- | --- | --- | --- | --- |
| SOURCED-COHORT-13 | source-query | 13 | True | PASS |
| SOURCED-UPX-MAT-004-001 | source-query | 1 | True | PASS |
| SOURCED-UPX-MAT-004-002 | source-query | 1 | True | PASS |
| SOURCED-UPX-MAT-004-003 | source-query | 1 | True | PASS |
| SOURCED-UPX-MAT-004-004 | source-query | 1 | True | PASS |
| SOURCED-UPX-MAT-004-005 | source-query | 1 | True | PASS |
| SOURCED-UPX-MAT-004-006 | source-query | 1 | True | PASS |
| SOURCED-UPX-MAT-004-007 | source-query | 1 | True | PASS |
| SOURCED-UPX-MAT-004-008 | source-query | 1 | True | PASS |
| SOURCED-UPX-MAT-004-009 | source-query | 1 | True | PASS |
| SOURCED-UPX-MAT-004-010 | source-query | 1 | True | PASS |
| SOURCED-UPX-MAT-004-011 | source-query | 1 | True | PASS |
| SOURCED-EX-SRC-PH-001-001 | source-query | 1 | True | PASS |
| SOURCED-EX-SRC-PH-001-003 | source-query | 1 | True | PASS |
| MISSING-SOURCE | synthetic-negative | 0 | False | PASS |
| MISSING-LOCATOR | synthetic-negative | 0 | False | PASS |
| MISSING-ORIGIN | synthetic-negative | 0 | False | PASS |
| CROSS-SOURCE-RECORD | synthetic-negative | 0 | False | PASS |
| CROSS-RECORD-EVIDENCE | synthetic-negative | 0 | False | PASS |
| CROSS-RECORD-STATEMENT | synthetic-negative | 0 | False | PASS |
| MISSING-NATIVE-SUPPORT | synthetic-negative | 0 | False | PASS |
| MISSING-NATIVE-EVIDENCE | synthetic-negative | 0 | False | PASS |
| WRONG-LOCATOR | synthetic-negative | 0 | False | PASS |
| MULTIPLE-SOURCES-REMAIN-VISIBLE | synthetic-negative | 1 | False | PASS |
| COHERENT-FORGED-SOURCE-IS-REJECTED | synthetic-negative | 1 | False | PASS |
| COHERENT-FORGED-LOCATOR-IS-REJECTED | synthetic-negative | 1 | False | PASS |
| CONFLICTING-ORIGINS-REMAIN-VISIBLE | synthetic-negative | 2 | False | PASS |
| GUARD-DELETION-EXPOSES-FORGED-SOURCE | guard-mutation | 1 | False | PASS |
| QUERY-MUTANT-CROSS-RECORD | query-mutation | 169 | False | PASS |
| QUERY-MUTANT-REVERSED-NATIVE | query-mutation | 0 | False | PASS |
| QUERY-MUTANT-MISSING-ORIGIN | query-mutation | 13 | False | PASS |
| EQUAL-DESCRIPTIONS-KEEP-DISTINCT-IDS | identity-control | 2 | True | PASS |
| UNTRACKED-RECORD-NOT-ADMITTED | synthetic-negative | 1 | False | PASS |
| NO-CASE-PROMOTION | synthetic-negative | 1 | False | PASS |
| NO-SCENARIO-PROMOTION | synthetic-negative | 1 | False | PASS |

The 13 sourced records include 11 still-WITHHELD scenario descriptions and two review labels. No source score, probability, primary corroboration, event occurrence, full data accuracy or whole-ontology acceptance is claimed. CQ07/08 and owner review remain separate; old 40 synthetic CQ and scientific receipts retain their actual denominators.

Replay: `python tools/run_source_cq06.py --check`. Optional exact supplied PDF recheck: `python tools/run_source_cq06.py --verify-pdfs /path/to/private-pdfs` (requires pypdf; no PDF is published).
