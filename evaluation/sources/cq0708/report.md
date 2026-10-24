# Executed source-backed CQ07/CQ08 packet

**Scoped correction/identity inspection, not complete native admission, clinical estimate validation, independent review or owner acceptance.**

Execution checkout `920524ee05d4f7f7468ce7a9aa75a70cc7c08503`; source/oracle freeze `920524ee05d4f7f7468ce7a9aa75a70cc7c08503`. [Scope, dictionary, rights and sources](README.md); [complete receipt](report.json.gz). Exact inputs/query/graph/binding/finding oracles are retained.

Engine: {"name": "RDFLib SPARQL SELECT", "version": "7.6.0", "python": "3.12.14", "inference": "none", "remote_service": false}. CI replays frozen public selected source data; the actual primary PDF review is separately recorded in inspection.json.

Summary: {"correction_source_documents": 2, "independent_study_lineages": 1, "selected_assertion_pairs": 5, "retained_assertion_versions": 10, "changed_selected_values": 4, "unchanged_reissued_values": 1, "withheld_identity_candidates": 11, "managed_cases_admitted": 0, "scenarios": 59, "actual_query_executions": 59, "by_route": {"cq07": 30, "cq08": 29}, "by_kind": {"source-query": 18, "synthetic-negative": 31, "identity-control": 2, "guard-mutation": 2, "query-mutation": 4, "roundtrip": 2}, "query_mutants_detected": 4, "statuses": {"PASS": 59}}. Source queries, synthetic negatives, identity/guard/mutant controls and round trips are disjoint scenario kinds. An unbound case is an absent graph assertion, not a real-world nonexistence result.

| Case | CQ | Kind | Raw answers | Validator admits | Verdict |
| --- | --- | --- | --- | --- | --- |
| SOURCE-CQ07-ALL-FIVE | cq07 | source-query | 5 | True | PASS |
| SOURCE-CQ08-ALL-ELEVEN | cq08 | source-query | 11 | True | PASS |
| SOURCE-CQ07-T1-ALL-P2P3 | cq07 | source-query | 1 | True | PASS |
| SOURCE-CQ07-T2-ALL-P2P3 | cq07 | source-query | 1 | True | PASS |
| SOURCE-CQ07-T2-NONONC-P2P3 | cq07 | source-query | 1 | True | PASS |
| SOURCE-CQ07-T2-LEAD-P2P3 | cq07 | source-query | 1 | True | PASS |
| SOURCE-CQ07-T2-ONC-P2P3 | cq07 | source-query | 1 | True | PASS |
| SOURCE-CQ08-UPX-MAT-004-001 | cq08 | source-query | 1 | True | PASS |
| SOURCE-CQ08-UPX-MAT-004-002 | cq08 | source-query | 1 | True | PASS |
| SOURCE-CQ08-UPX-MAT-004-003 | cq08 | source-query | 1 | True | PASS |
| SOURCE-CQ08-UPX-MAT-004-004 | cq08 | source-query | 1 | True | PASS |
| SOURCE-CQ08-UPX-MAT-004-005 | cq08 | source-query | 1 | True | PASS |
| SOURCE-CQ08-UPX-MAT-004-006 | cq08 | source-query | 1 | True | PASS |
| SOURCE-CQ08-UPX-MAT-004-007 | cq08 | source-query | 1 | True | PASS |
| SOURCE-CQ08-UPX-MAT-004-008 | cq08 | source-query | 1 | True | PASS |
| SOURCE-CQ08-UPX-MAT-004-009 | cq08 | source-query | 1 | True | PASS |
| SOURCE-CQ08-UPX-MAT-004-010 | cq08 | source-query | 1 | True | PASS |
| SOURCE-CQ08-UPX-MAT-004-011 | cq08 | source-query | 1 | True | PASS |
| CQ07-MISSING-LINEAGE | cq07 | synthetic-negative | 0 | False | PASS |
| CQ07-WRONG-PARENT | cq07 | synthetic-negative | 0 | False | PASS |
| CQ07-CROSS-ARTIFACT | cq07 | synthetic-negative | 0 | False | PASS |
| CQ07-MISSING-ORIGINAL-TYPE | cq07 | synthetic-negative | 0 | False | PASS |
| CQ07-MISSING-ORIGINAL-SOURCE | cq07 | synthetic-negative | 0 | False | PASS |
| CQ07-MISSING-CORRECTION-NOTICE | cq07 | synthetic-negative | 0 | False | PASS |
| CQ07-UNRELATED-CORRECTION | cq07 | synthetic-negative | 0 | False | PASS |
| CQ07-WRONG-LOCATOR | cq07 | synthetic-negative | 1 | False | PASS |
| CQ07-MISSING-LOCATOR | cq07 | synthetic-negative | 1 | False | PASS |
| CQ07-WRONG-UNIT | cq07 | synthetic-negative | 1 | False | PASS |
| CQ07-WRONG-CONTEXT | cq07 | synthetic-negative | 0 | False | PASS |
| CQ07-COHERENT-WRONG-CONTEXT | cq07 | synthetic-negative | 1 | False | PASS |
| CQ07-COHERENT-FORGED-SOURCE | cq07 | synthetic-negative | 1 | False | PASS |
| CQ07-FORGED-REPORTED-VALUE | cq07 | synthetic-negative | 1 | False | PASS |
| CQ07-CONFLICTING-VALUES-PRESERVED | cq07 | synthetic-negative | 2 | False | PASS |
| CQ07-ORIGINAL-OVERWRITE-DETECTED | cq07 | synthetic-negative | 1 | False | PASS |
| CQ07-CORRECTION-NOT-CORROBORATION | cq07 | synthetic-negative | 1 | False | PASS |
| CQ07-WRONG-DISPOSITION | cq07 | synthetic-negative | 1 | False | PASS |
| CQ07-UNKNOWN-DENOMINATOR-NOT-ZERO | cq07 | synthetic-negative | 1 | False | PASS |
| CQ07-EQUAL-TITLES-DISTINCT-ASSERTIONS | cq07 | identity-control | 2 | True | PASS |
| CQ07-DELETED-SOURCE-GUARD-EXPOSES-FORGERY | cq07 | guard-mutation | 1 | True | PASS |
| CQ08-MISSING-CANDIDATE | cq08 | synthetic-negative | 0 | False | PASS |
| CQ08-MISSING-SOURCE | cq08 | synthetic-negative | 1 | False | PASS |
| CQ08-WRONG-SOURCE | cq08 | synthetic-negative | 1 | False | PASS |
| CQ08-WRONG-LOCATOR | cq08 | synthetic-negative | 1 | False | PASS |
| CQ08-WRONG-PRIOR-RECORD | cq08 | synthetic-negative | 1 | False | PASS |
| CQ08-UNAUTHORIZED-ADMISSION | cq08 | synthetic-negative | 1 | False | PASS |
| CQ08-UNAUTHORIZED-OCCURRENCE | cq08 | synthetic-negative | 1 | False | PASS |
| CQ08-FALSE-CASE-LINK | cq08 | synthetic-negative | 1 | False | PASS |
| CQ08-NATIVE-CASE-PROMOTION | cq08 | synthetic-negative | 1 | False | PASS |
| CQ08-NATIVE-SCENARIO-PROMOTION | cq08 | synthetic-negative | 1 | False | PASS |
| CQ08-CONFLICTING-CASE-LINKS-PRESERVED | cq08 | synthetic-negative | 2 | False | PASS |
| CQ08-ALIAS-DOES-NOT-ALLOCATE-CASE | cq08 | synthetic-negative | 1 | False | PASS |
| CQ08-EQUAL-TITLES-DISTINCT-CANDIDATES | cq08 | identity-control | 2 | True | PASS |
| CQ08-DELETED-IDENTITY-GUARD-EXPOSES-PROMOTION | cq08 | guard-mutation | 1 | True | PASS |
| QUERY-MUTANT-CQ07-REVERSED | cq07 | query-mutation | 0 | True | PASS |
| QUERY-MUTANT-CQ07-OVERWRITE-OLD | cq07 | query-mutation | 5 | True | PASS |
| QUERY-MUTANT-CQ08-BOUND-ONLY | cq08 | query-mutation | 0 | True | PASS |
| QUERY-MUTANT-CQ08-INVENT-CASE | cq08 | query-mutation | 11 | True | PASS |
| SERIALIZE-REPARSE-CQ07 | cq07 | roundtrip | 5 | True | PASS |
| SERIALIZE-REPARSE-CQ08 | cq08 | roundtrip | 11 | True | PASS |

A deliberately deleted guard may admit a synthetic forgery; its PASS means sensitivity matched its fixed oracle, not that the forged record is acceptable. Parser/engine failures are ERROR. No old assertion is overwritten, no correction adds independent corroboration, no withheld candidate is admitted and no historical engine denominator is rewritten.

Replay: `python tools/run_source_cq0708.py --check`. Optional privately held exact PDF recheck: `python tools/run_source_cq0708.py --verify-pdfs /path/to/private-pdfs` (pypdf required; no PDF is packaged).
