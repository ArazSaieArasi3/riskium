# Shared-graph validation profile 0.1.0

Executed engineering supplement after stable v0.3.1. Seven module families run together; 29 selected relation pairs. This does not rewrite historical engine outcomes or grant full native/task acceptance.

The [fixed graph](fixtures.ttl), [exact expected findings](cases.json) and [policy](../../implementation/validation/0.1.0/policy.json) were committed before the validator. The two joint rules prevent separately admissible threshold/comparison declarations from silently using different scales or versions.

Summary: {"scenarios": 31, "engine_executions": 21, "preflight_rejections": 9, "staging_cases": 1, "mutation_controls": 4, "module_families": 7, "selected_relations": 29, "statuses": {"PASS": 31}, "decisions": {"SCOPED_TASK_ADMISSIBLE": 6, "CATALOG_ACCEPTED": 2, "STAGING_ONLY": 1, "NOT_ADMISSIBLE_FOR_SCOPED_TASK": 13, "PROFILE_REJECTED": 9}}.

Mutation controls deliberately remove one rule; admitting their bad inputs demonstrates sensitivity, not acceptable domain data. Raw staging and catalog metadata acceptance never become task acceptance.

[Full graph/input/result receipt](report.json.gz). Replay: `python tools/run_integrated_validation.py --check`.

| Case | Expected | Observed | Engine | Control | Result |
| --- | --- | --- | --- | --- | --- |
| JOINT-VALID | SCOPED_TASK_ADMISSIBLE | SCOPED_TASK_ADMISSIBLE | True | fixed | PASS |
| CATALOG-ONLY-NO-TASK-ACCEPTANCE | CATALOG_ACCEPTED | CATALOG_ACCEPTED | True | fixed | PASS |
| RAW-INCOMPLETE-PRESERVED | STAGING_ONLY | STAGING_ONLY | False | fixed | PASS |
| MISSING-UNIT | NOT_ADMISSIBLE_FOR_SCOPED_TASK | NOT_ADMISSIBLE_FOR_SCOPED_TASK | True | fixed | PASS |
| MISSING-TIME | NOT_ADMISSIBLE_FOR_SCOPED_TASK | NOT_ADMISSIBLE_FOR_SCOPED_TASK | True | fixed | PASS |
| BLANK-VOCABULARY-CODE | NOT_ADMISSIBLE_FOR_SCOPED_TASK | NOT_ADMISSIBLE_FOR_SCOPED_TASK | True | fixed | PASS |
| CHALLENGE-CANNOT-ASSERT-SUPPORT | NOT_ADMISSIBLE_FOR_SCOPED_TASK | NOT_ADMISSIBLE_FOR_SCOPED_TASK | True | fixed | PASS |
| CONTEXT-SUBSET-MISMATCH | NOT_ADMISSIBLE_FOR_SCOPED_TASK | NOT_ADMISSIBLE_FOR_SCOPED_TASK | True | fixed | PASS |
| REVISION-SELF-CYCLE | NOT_ADMISSIBLE_FOR_SCOPED_TASK | NOT_ADMISSIBLE_FOR_SCOPED_TASK | True | fixed | PASS |
| PUBLISHED-WITHOUT-ABOUTNESS | NOT_ADMISSIBLE_FOR_SCOPED_TASK | NOT_ADMISSIBLE_FOR_SCOPED_TASK | True | fixed | PASS |
| UNRESOLVED-ACTOR-DISTINCTION | NOT_ADMISSIBLE_FOR_SCOPED_TASK | NOT_ADMISSIBLE_FOR_SCOPED_TASK | True | fixed | PASS |
| MISSING-CATALOG-TITLE | NOT_ADMISSIBLE_FOR_SCOPED_TASK | NOT_ADMISSIBLE_FOR_SCOPED_TASK | True | fixed | PASS |
| MISSING-NATIVE-INDICATOR-TYPE | NOT_ADMISSIBLE_FOR_SCOPED_TASK | NOT_ADMISSIBLE_FOR_SCOPED_TASK | True | fixed | PASS |
| COMPOUND-UNIT-TIME-TITLE | NOT_ADMISSIBLE_FOR_SCOPED_TASK | NOT_ADMISSIBLE_FOR_SCOPED_TASK | True | fixed | PASS |
| VERSION-ALIAS-NORMALIZES-ALL-MODULES | SCOPED_TASK_ADMISSIBLE | SCOPED_TASK_ADMISSIBLE | True | fixed | PASS |
| IDENTITY-CONFLICT | PROFILE_REJECTED | PROFILE_REJECTED | False | fixed | PASS |
| CROSS-MODULE-RESERVED-ALIAS | PROFILE_REJECTED | PROFILE_REJECTED | False | fixed | PASS |
| SCHEMA-INJECTION | PROFILE_REJECTED | PROFILE_REJECTED | False | fixed | PASS |
| IN-BAND-COMPARISON-SELECTOR | PROFILE_REJECTED | PROFILE_REJECTED | False | fixed | PASS |
| IN-BAND-SHAPE-SWITCH | PROFILE_REJECTED | PROFILE_REJECTED | False | fixed | PASS |
| IN-BAND-INTEGRATION-SELECTOR | PROFILE_REJECTED | PROFILE_REJECTED | False | fixed | PASS |
| EMPTY-COMPARISON-REQUEST | PROFILE_REJECTED | PROFILE_REJECTED | False | fixed | PASS |
| EMPTY-CATALOG-REQUEST | PROFILE_REJECTED | PROFILE_REJECTED | False | fixed | PASS |
| UNTARGETED-NATIVE-PARTICIPANT | PROFILE_REJECTED | PROFILE_REJECTED | False | fixed | PASS |
| MUTANT-DELETE-UNIT-CHECK | SCOPED_TASK_ADMISSIBLE | SCOPED_TASK_ADMISSIBLE | True | mutation | PASS |
| MUTANT-DELETE-ACTOR-DISTINCTION | SCOPED_TASK_ADMISSIBLE | SCOPED_TASK_ADMISSIBLE | True | mutation | PASS |
| MUTANT-DELETE-CYCLE-CHECK | SCOPED_TASK_ADMISSIBLE | SCOPED_TASK_ADMISSIBLE | True | mutation | PASS |
| MODULES-SEPARATELY-VALID-BUT-DIFFERENT-SCALE | NOT_ADMISSIBLE_FOR_SCOPED_TASK | NOT_ADMISSIBLE_FOR_SCOPED_TASK | True | fixed | PASS |
| MODULES-SEPARATELY-VALID-BUT-DIFFERENT-VERSION | NOT_ADMISSIBLE_FOR_SCOPED_TASK | NOT_ADMISSIBLE_FOR_SCOPED_TASK | True | fixed | PASS |
| MUTANT-DELETE-JOINT-VERSION-CHECK | SCOPED_TASK_ADMISSIBLE | SCOPED_TASK_ADMISSIBLE | True | mutation | PASS |
| CATALOG-ACCEPTS-MISSING-TASK-UNIT | CATALOG_ACCEPTED | CATALOG_ACCEPTED | True | fixed | PASS |
