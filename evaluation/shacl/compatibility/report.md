# C-08 declared interpretation compatibility — application profile 0.6.0

**Scoped application policy executed; global C-08 remains PARTIAL.** No native ontology/OWL change, unit conversion, value/comparator evaluation or independent semantic acceptance is claimed.

Execution checkout: `177f3bdcd0a2d12f80348771bbbd70cd8e2e1adb`; exact input hashes and raw/effective/shapes/result graphs are in [the full receipt](report.json.gz). [Policy](profile-policy.json) and [review](profile-review.md) define the task.

Summary: {"scenarios": 41, "engine_executions": 37, "preflight_rejections": 4, "selected_integration_cases": 5, "mutation_controls": 2, "statuses": {"PASS": 41}, "decisions": {"COMPATIBLE_FOR_DECLARED_TASK": 8, "NOT_READY": 13, "INCOMPATIBLE": 9, "INVALID": 6, "STAGING_ONLY": 1, "PROFILE_REJECTED": 4}}.

The original 359-row ledger and old blocked task fixture are retained byte for byte. The new evidence covers explicit supplementary metadata, not approval of every possible interpretation of C-08. The unchanged ledger remains 341 scoped PASS, 1 PARTIAL and 17 NOT_RUN. HermiT is not rerun by this module.

| Case | Expected decision | Observed | Engine executed | Verdict |
| --- | --- | --- | --- | --- |
| `C08-NUMERIC-MATCH` | COMPATIBLE_FOR_DECLARED_TASK | COMPATIBLE_FOR_DECLARED_TASK | True | PASS |
| `C08-QUALITATIVE-MATCH` | COMPATIBLE_FOR_DECLARED_TASK | COMPATIBLE_FOR_DECLARED_TASK | True | PASS |
| `C08-MISSING-INDICATOR-VERSION` | NOT_READY | NOT_READY | True | PASS |
| `C08-MISSING-SCALE-VERSION` | NOT_READY | NOT_READY | True | PASS |
| `C08-MISSING-INDICATOR-DIMENSION` | NOT_READY | NOT_READY | True | PASS |
| `C08-MISSING-SCALE-DIMENSION` | NOT_READY | NOT_READY | True | PASS |
| `C08-MISSING-INDICATOR-KIND` | NOT_READY | NOT_READY | True | PASS |
| `C08-MISSING-INDICATOR-SOURCE` | NOT_READY | NOT_READY | True | PASS |
| `C08-MISSING-INDICATOR-UNIT` | NOT_READY | NOT_READY | True | PASS |
| `C08-MISSING-SCALE-UNIT` | NOT_READY | NOT_READY | True | PASS |
| `C08-MISSING-QUALITATIVE-SCHEME` | NOT_READY | NOT_READY | True | PASS |
| `C08-DIFFERENT-QUALITATIVE-SCHEME` | INCOMPATIBLE | INCOMPATIBLE | True | PASS |
| `C08-MISSING-QUALITATIVE-TERMSET` | NOT_READY | NOT_READY | True | PASS |
| `C08-DIFFERENT-QUALITATIVE-TERMSET` | INCOMPATIBLE | INCOMPATIBLE | True | PASS |
| `C08-DIFFERENT-UNIT` | INCOMPATIBLE | INCOMPATIBLE | True | PASS |
| `C08-DELETED-UNIT-RULE` | COMPATIBLE_FOR_DECLARED_TASK | COMPATIBLE_FOR_DECLARED_TASK | True | PASS |
| `C08-UNIT-EXPLICIT-ALIAS` | COMPATIBLE_FOR_DECLARED_TASK | COMPATIBLE_FOR_DECLARED_TASK | True | PASS |
| `C08-UNKNOWN-UNIT-MAPPING` | NOT_READY | NOT_READY | True | PASS |
| `C08-LABELS-NOT-IDENTITY` | INCOMPATIBLE | INCOMPATIBLE | True | PASS |
| `C08-DIFFERENT-DIMENSION` | INCOMPATIBLE | INCOMPATIBLE | True | PASS |
| `C08-DIFFERENT-VERSION` | INCOMPATIBLE | INCOMPATIBLE | True | PASS |
| `C08-VERSION-EXPLICIT-ALIAS` | COMPATIBLE_FOR_DECLARED_TASK | COMPATIBLE_FOR_DECLARED_TASK | True | PASS |
| `C08-DIFFERENT-KIND` | INCOMPATIBLE | INCOMPATIBLE | True | PASS |
| `C08-WRONG-VERSION-TARGET` | INCOMPATIBLE | INCOMPATIBLE | True | PASS |
| `C08-MISSING-VERSION-TARGET` | NOT_READY | NOT_READY | True | PASS |
| `C08-CONFLICTING-UNITS` | INVALID | INVALID | True | PASS |
| `C08-LITERAL-UNIT` | INVALID | INVALID | True | PASS |
| `C08-QUALITATIVE-INVENTED-UNIT` | INVALID | INVALID | True | PASS |
| `C08-UNTYPED-SELECTED-THRESHOLD` | INVALID | INVALID | True | PASS |
| `C08-UNKNOWN-KIND` | INVALID | INVALID | True | PASS |
| `C08-DELETED-COMPLETENESS-RULE` | COMPATIBLE_FOR_DECLARED_TASK | COMPATIBLE_FOR_DECLARED_TASK | True | PASS |
| `C08-RAW-INCOMPLETE` | STAGING_ONLY | STAGING_ONLY | True | PASS |
| `C08-IDENTITY-CONFLICT` | PROFILE_REJECTED | PROFILE_REJECTED | False | PASS |
| `C08-RESERVED-ALIAS` | PROFILE_REJECTED | PROFILE_REJECTED | False | PASS |
| `C08-SCHEMA-INJECTION` | PROFILE_REJECTED | PROFILE_REJECTED | False | PASS |
| `C08-EMPTY-FOCUS` | PROFILE_REJECTED | PROFILE_REJECTED | False | PASS |
| `C08-INTEGRATED-NUMERIC` | COMPATIBLE_FOR_DECLARED_TASK | COMPATIBLE_FOR_DECLARED_TASK | True | PASS |
| `C08-INTEGRATED-QUALITATIVE` | COMPATIBLE_FOR_DECLARED_TASK | COMPATIBLE_FOR_DECLARED_TASK | True | PASS |
| `C08-INTEGRATED-INCOMPATIBLE` | INCOMPATIBLE | INCOMPATIBLE | True | PASS |
| `C08-INTEGRATED-MISSING-DIMENSION` | NOT_READY | NOT_READY | True | PASS |
| `C08-INTEGRATED-UNTYPED-THRESHOLD` | INVALID | INVALID | True | PASS |

Replay: `python tools/run_compatibility_shacl.py --check`. This executes fresh validations, verifies the fixed oracles, snapshot hashes and source bindings, and compares saved raw/effective/shapes graphs. Preflight rejections and software tests are not added to the engine count.
