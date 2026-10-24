# Shared-graph validation 0.1.0

This independently versioned application supplement composes the unchanged Riskium 0.3.1 profiles on one graph. Its [policy](policy.json) pins every scientific input and all seven module families. It is post-release engineering work; it does not change the v0.3.1 tag, the owner-approved scope, ORSD 0.4.3, manuscript 7.0.8 or SQLite schema 0.1.0.

`raw` preserves received triples without admission. `managed-catalog` checks declared catalog metadata only. `scoped-comparison` validates the caller-selected publication, vocabulary, evidence, threshold and comparison tasks together, including 29 selected relation pairs, C-06/C-08/C-09/C-25 and C-23/C-24 graph rules. Only the last profile can return `SCOPED_TASK_ADMISSIBLE`; it grants eligibility for this finite task policy, not complete risk-record readiness.

The task adds two explicit engineering joins: the threshold and both results must select the same normalized scale and scale version. This prevents separately valid metadata modules from being combined under inconsistent pins. Unequal unresolved identifiers fail the exact-join task; that is not proof that the physical scales cannot be converted. No calculations, workflow transitions, transformations or time-interval algorithms are supplied.

Callers supply focus independently of the data. Every explicitly typed native participant needs a caller-selected catalog envelope. Catalog metadata never inserts missing native types. Named `sameAs` assertions normalize across all modules and requests; conflicting distinctions and aliases of participating vocabulary are rejected. The wrapper blocks in-band schema, imports, shapes and reserved selectors. Engine exceptions remain failures. The public validator has no option to disable a rule.

The [31 frozen scenarios](../../../evaluation/integration/cases.json) predate the validator at commit `6243411579029120459cdd914a17b6006c7cdbbf`. [Execution and replay evidence](../../../evaluation/integration/README.md) stores effective data, shapes, actual results, exact findings and all input hashes. Four deliberately weakened-rule controls demonstrate fixture sensitivity and are not admissible domain data. The 359 historical SHACL obligations and 295 HermiT obligations keep their original outcomes.

```sh
python tools/run_integrated_validation.py --check
python -m unittest discover -s tests -p test_integrated_validation.py -v
```

For arbitrary local Turtle input, write a separate caller-owned JSON request with the six keys shown in `evaluation/integration/cases.json` under `requests`, then run:

```sh
python tools/validate_integrated.py graph.ttl request.json --profile scoped-comparison
```

The CLI returns 1 for profile/admission rejection and nonzero on engine errors. A zero exit for raw/catalog profiles still grants no task acceptance. Exact provenance existence and graph conformance do not establish source truth or independent scientific validation.
