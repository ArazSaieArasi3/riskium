# Executed SQLite assessment profile 0.2.0

Bounded engineering evidence under #29/#12. Original v0.3.1, ORSD 0.4.3, paper 7.0.8 and SQL profile 0.1.0 remain unchanged. No new actual case study, PostgreSQL run, independent review or production certification.

The [database requirements](../../../requirements/relational-requirements.json), [policy](../../../implementation/relational/0.2.0/policy.json) and [48 fixed / 100 seeded inputs](../../../implementation/relational/0.2.0/fixtures.json) were committed before execution at `3ed56e501bff3ece7d58a7e49167f6a928fd3739`. The full RDF projection regression also uses separately hand-authored expected facts, not query output.

Summary: {"fixed_cases": 48, "statuses": {"PASS": 48}, "by_kind": {"operation": 39, "roundtrip": 3, "differential": 3, "concurrency": 1, "mutation-control": 2}, "generated_inputs": 100, "generated_matches": 100, "schema_audit": {"tables": 16, "columns": 86, "foreign_key_columns": 57, "named_indexes": 40, "one_column_tables": 0, "findings": 0}, "measured_workloads": 4, "shacl_engine_executions": 2}.

[Full receipt with exact SQL errors, before/after state hashes, traces, generated answers, schema audit, query plans and measurements](report.json.gz). [Actual schema dictionary and FD review](../../../implementation/relational/0.2.0/schema-dictionary.md).

The two weakened-rule controls deliberately remove enforcement; their bad inputs becoming possible is sensitivity evidence, not valid domain data. Raw/unknown, managed rows and strict task eligibility remain distinct. Reported lexical zero is retained without arithmetic. Historical native interpretation facts are exported in separate named assessment-version graphs.

Timing samples describe 1,000 generated assessments/results in memory and four declared workloads; there is no approved production SLO or human usability result. Query-plan text is retained but not required byte-equal across SQLite versions. No normal-form or universal mapping correctness score is inferred from structural counts.

| Case | Expected | Observed | Result |
| --- | --- | --- | --- |
| MIGRATE-POPULATED-PRESERVES-BASE | True | True | PASS |
| MIGRATION-IDEMPOTENT | True | True | PASS |
| MIGRATION-LEDGER-DRIFT | R-MIGRATION-SOURCE-HASH | R-MIGRATION-SOURCE-HASH | PASS |
| MIGRATION-SCHEMA-DRIFT | R-MIGRATION-SCHEMA-DRIFT | R-MIGRATION-SCHEMA-DRIFT | PASS |
| CONNECTION-FK-OFF | R-CONNECTION-POLICY: foreign_keys and recursive_triggers must be ON | R-CONNECTION-POLICY: foreign_keys and recursive_triggers must be ON | PASS |
| CONNECTION-TRIGGERS-OFF | R-CONNECTION-POLICY: foreign_keys and recursive_triggers must be ON | R-CONNECTION-POLICY: foreign_keys and recursive_triggers must be ON | PASS |
| EXACT-VERSION-PINNED-LOOKUP | [['urn:riskium:assessment:r1', '0', 'urn:riskium:sql:context-v1', 'urn:riskium:assessment:method-v3', 'urn:riskium:assessment:basis-v1', 'urn:riskium:assessment:scale-v3', 'urn:riskium:assessment:dimension']] | [['urn:riskium:assessment:r1', '0', 'urn:riskium:sql:context-v1', 'urn:riskium:assessment:method-v3', 'urn:riskium:assessment:basis-v1', 'urn:riskium:assessment:scale-v3', 'urn:riskium:assessment:dimension']] | PASS |
| UNKNOWN-IS-NULL-NOT-ZERO | [['UNKNOWN', None]] | [['UNKNOWN', None]] | PASS |
| DUPLICATE-LABELS-NOT-IDENTITY | 2 | 2 | PASS |
| REPORTED-ZERO-LEXEME | 0 | 0 | PASS |
| RAW-INPUT-EXACT | {"score":null,"case":null,"synthetic":true} | {"score":null,"case":null,"synthetic":true} | PASS |
| DIRECT-COMPARISON-SAME-PINS | SCOPED_DIRECT_COMPARISON_ADMISSIBLE | SCOPED_DIRECT_COMPARISON_ADMISSIBLE | PASS |
| DIRECT-COMPARISON-MISSING-TIME | NOT_READY | NOT_READY | PASS |
| DIRECT-COMPARISON-DIFFERENT-VERSION | NOT_ADMISSIBLE_BY_EXACT_PIN_POLICY | NOT_ADMISSIBLE_BY_EXACT_PIN_POLICY | PASS |
| ISSUED-RESULT-NO-UPDATE | R-ISSUED-METADATA | R-ISSUED-METADATA | PASS |
| ISSUED-ASSESSMENT-NO-DELETE | R-ISSUED-METADATA | R-ISSUED-METADATA | PASS |
| ISSUED-SCALE-NO-LEVEL-APPEND | R-ISSUED-METADATA | R-ISSUED-METADATA | PASS |
| ISSUED-ASSESSMENT-NO-RESULT-APPEND | R-ASSESSMENT-FROZEN | R-ASSESSMENT-FROZEN | PASS |
| TYPING-CANNOT-REINTERPRET-ISSUED-ARTIFACT | R-TYPE-ALREADY-ISSUED | R-TYPE-ALREADY-ISSUED | PASS |
| TYPING-BASE-KIND-MISMATCH | R-TYPE-BASE-KIND | R-TYPE-BASE-KIND | PASS |
| WRONG-CONTEXT-VERSION-KIND | R-ROLE-KIND | R-ROLE-KIND | PASS |
| DIRECT-CONTEXT-TARGET-MISMATCH | R-ROLE-TARGET | R-ROLE-TARGET | PASS |
| UNISSUED-METHOD-PIN | R-ROLE-ISSUED | R-ROLE-ISSUED | PASS |
| INVALID-RECORDED-CALENDAR | R-TIME-LEXICAL | R-TIME-LEXICAL | PASS |
| INVALID-VALIDITY-ORDER | R-TIME-ORDER | R-TIME-ORDER | PASS |
| COMPUTED-WITHOUT-FORMULA | R-COMPUTATION-UNSUPPORTED | R-COMPUTATION-UNSUPPORTED | PASS |
| REPORTED-NULL-IS-NOT-VALUE | R-REPORTED-VALUE | R-REPORTED-VALUE | PASS |
| UNKNOWN-WITH-INVENTED-ZERO | R-UNKNOWN-VALUE | R-UNKNOWN-VALUE | PASS |
| LEVEL-OF-DIFFERENT-SCALE-VERSION | R-LEVEL-VERSION | R-LEVEL-VERSION | PASS |
| MISSING-DIMENSION | NOT NULL constraint failed: result_snapshot.dimension_id | NOT NULL constraint failed: result_snapshot.dimension_id | PASS |
| MISSING-LOCATOR | R-SOURCE-QUALIFIER | R-SOURCE-QUALIFIER | PASS |
| UNKNOWN-SOURCE-KEY | FOREIGN KEY constraint failed | FOREIGN KEY constraint failed | PASS |
| FAILED-BUNDLE-ROLLS-BACK-ALL-ROWS | True | True | PASS |
| HISTORICAL-ANSWER-UNCHANGED-AFTER-NEW-VERSION | True | True | PASS |
| TWO-QUALIFIED-RESULTS-SAME-DIMENSION | 2 | 2 | PASS |
| READ-ONLY-BACKUP-RESTORE | True | True | PASS |
| SQL-DUMP-RESTORE | True | True | PASS |
| FILE-CLOSE-REOPEN | True | True | PASS |
| SQL-RDF-FIXED-FACTS | True | True | PASS |
| RDF-NAMED-HISTORY-NOT-UNIONED | True | True | PASS |
| SHACL-DIRECT-COMPARISON-ELIGIBILITY | True | True | PASS |
| BOUND-PARAMETER-SQL-INJECTION-LEXEME | '; DROP TABLE result_snapshot; -- | '; DROP TABLE result_snapshot; -- | PASS |
| SCHEMA-DICTIONARY-DESIGN-AUDIT | True | True | PASS |
| UNEXPLAINED-ONE-COLUMN-TABLE-FLAGGED | True | True | PASS |
| TWO-CONNECTION-WRITER-CONFLICT-RETRY | True | True | PASS |
| DELETED-IMMUTABILITY-GUARD-EXPOSES-CHANGE | changed | changed | PASS |
| DELETED-VERSION-TARGET-GUARD-EXPOSES-MISJOIN | True | True | PASS |
| SCHEMA-TAMPERING-DETECTED | R-ASSESSMENT-SCHEMA-DRIFT | R-ASSESSMENT-SCHEMA-DRIFT | PASS |

Replay: `python tools/run_relational_assessment.py --check`. Every input must match its saved SHA-256; source cases, runtime observations and generated test populations have separate meanings.
