# Database requirements, mapping and executed evidence

This trace separates static source accounting, authored design review, fixed executions, generated properties and workload observations. Current scope is public SQLite 0.2.0/DRSD 0.1.0, not full original ORSD or deployment acceptance. Four future MUST requirements remain NOT_RUN rather than being removed or silently downgraded.

[Machine trace/readiness](assurance.json), [all 306 source dispositions](mapping-coverage.json), [actual SQL receipt](report.json.gz), [method and checklist](../../../docs/relational-assurance.md).

| DB requirement | Source ORSD | Implementation objects | Evidence | Status |
| --- | --- | --- | --- | --- |
| DBR-01 Scope and source inventory | RKRS-01, RKRS-11, RKRS-12 | full source inventory, mapping.json | mapping-coverage.json | PASS_WITH_DECLARED_PROFILE_LIMITS |
| DBR-02 Governed identity and subtype strategy | RKRS-02, RKRS-03 | identity_registry, information_artifact, artifact_typing | DUPLICATE-LABELS-NOT-IDENTITY, TYPING-CANNOT-REINTERPRET-ISSUED-ARTIFACT, TYPING-BASE-KIND-MISMATCH | PASS_WITH_DECLARED_PROFILE_LIMITS |
| DBR-03 Native relations and loss register | RKRS-04, RKRS-11 | mapping.json, v_assessment_quads | EXACT-VERSION-PINNED-LOOKUP, MISSING-DIMENSION, SQL-RDF-FIXED-FACTS | PASS_WITH_DECLARED_PROFILE_LIMITS |
| DBR-04 Assessment interpretation pins | RKRS-04 | assessment_snapshot, result_snapshot, scale_snapshot, scale_level, method_scope | EXACT-VERSION-PINNED-LOOKUP, DIRECT-COMPARISON-SAME-PINS, DIRECT-COMPARISON-MISSING-TIME, DIRECT-COMPARISON-DIFFERENT-VERSION, WRONG-CONTEXT-VERSION-KIND, DIRECT-CONTEXT-TARGET-MISMATCH, UNISSUED-METHOD-PIN, LEVEL-OF-DIFFERENT-SCALE-VERSION, HISTORICAL-ANSWER-UNCHANGED-AFTER-NEW-VERSION, RDF-NAMED-HISTORY-NOT-UNIONED | PASS_WITH_DECLARED_PROFILE_LIMITS |
| DBR-05 Immutable issued history | RKRS-03 | version_snapshot, version-owned guards, atomic issue_bundle | MIGRATE-POPULATED-PRESERVES-BASE, ISSUED-RESULT-NO-UPDATE, ISSUED-ASSESSMENT-NO-DELETE, ISSUED-SCALE-NO-LEVEL-APPEND, ISSUED-ASSESSMENT-NO-RESULT-APPEND, TYPING-CANNOT-REINTERPRET-ISSUED-ARTIFACT, FAILED-BUNDLE-ROLLS-BACK-ALL-ROWS, HISTORICAL-ANSWER-UNCHANGED-AFTER-NEW-VERSION | PASS_WITH_DECLARED_PROFILE_LIMITS |
| DBR-06 Multiple values and missingness | RKRS-04, RKRS-06 | result_snapshot, source_record | UNKNOWN-IS-NULL-NOT-ZERO, DUPLICATE-LABELS-NOT-IDENTITY, REPORTED-ZERO-LEXEME, REPORTED-NULL-IS-NOT-VALUE, UNKNOWN-WITH-INVENTED-ZERO, TWO-QUALIFIED-RESULTS-SAME-DIMENSION, BOUND-PARAMETER-SQL-INJECTION-LEXEME | PASS_WITH_DECLARED_PROFILE_LIMITS |
| DBR-07 Source and interpretation provenance | RKRS-06 | source_record, result source_locator/interpretation_origin, owner-specific RDF source | RAW-INPUT-EXACT, MISSING-LOCATOR, UNKNOWN-SOURCE-KEY, TWO-QUALIFIED-RESULTS-SAME-DIMENSION | PASS_WITH_DECLARED_PROFILE_LIMITS |
| DBR-08 Reported versus computed values | RKRS-05 | result_snapshot.score_kind/reported_value | UNKNOWN-IS-NULL-NOT-ZERO, REPORTED-ZERO-LEXEME, COMPUTED-WITHOUT-FORMULA, REPORTED-NULL-IS-NOT-VALUE, UNKNOWN-WITH-INVENTED-ZERO | PASS_WITH_DECLARED_PROFILE_LIMITS |
| DBR-09 Relational integrity and types |  | all table keys/FKs/STRICT/checks, configured connection | CONNECTION-FK-OFF, CONNECTION-TRIGGERS-OFF, MISSING-DIMENSION, UNKNOWN-SOURCE-KEY | PASS_WITH_DECLARED_PROFILE_LIMITS |
| DBR-10 Atomic writes and migrations | RKRS-03 | schema_migration, migration 3, atomic issue_bundle | MIGRATE-POPULATED-PRESERVES-BASE, MIGRATION-IDEMPOTENT, MIGRATION-LEDGER-DRIFT, MIGRATION-SCHEMA-DRIFT, FAILED-BUNDLE-ROLLS-BACK-ALL-ROWS | PASS_WITH_DECLARED_PROFILE_LIMITS |
| DBR-11 Backup and recovery |  | backup API, restore_dump data audit, reopen | READ-ONLY-BACKUP-RESTORE, SQL-DUMP-RESTORE, FILE-CLOSE-REOPEN | PASS_WITH_DECLARED_PROFILE_LIMITS |
| DBR-12 Explicit time fields | RKRS-08 | assessment_snapshot recorded/reference/validity fields | DIRECT-COMPARISON-MISSING-TIME, INVALID-RECORDED-CALENDAR, INVALID-VALIDITY-ORDER | PASS_WITH_DECLARED_PROFILE_LIMITS |
| DBR-13 Purpose and dependency review |  | actual table purposes, authored FD/denormalization review, one-column controls | SCHEMA-DICTIONARY-DESIGN-AUDIT, UNEXPLAINED-ONE-COLUMN-TABLE-FLAGGED, schema_audit | PASS_WITH_DECLARED_PROFILE_LIMITS |
| DBR-14 Complete schema dictionary |  | schema-dictionary.md | SCHEMA-DICTIONARY-DESIGN-AUDIT, schema_audit | PASS_WITH_DECLARED_PROFILE_LIMITS |
| DBR-15 Reproducible synthetic exploration |  | fixtures.json generated_inputs, seeded metamorphic checks | generative:100 | PASS_WITH_DECLARED_PROFILE_LIMITS |
| DBR-16 Sensitivity and exact failure oracles |  | a_result_snapshot_update, a_assessment_snapshot_insert, exact error oracles | DELETED-IMMUTABILITY-GUARD-EXPOSES-CHANGE, DELETED-VERSION-TARGET-GUARD-EXPOSES-MISJOIN | PASS_WITH_DECLARED_PROFILE_LIMITS |
| DBR-17 SQL/RDF differential checks | RKRS-04, RKRS-11 | v_assessment_quads, mapping.ttl, expected_graph, SHACL selection task | SQL-RDF-FIXED-FACTS, RDF-NAMED-HISTORY-NOT-UNIONED, SHACL-DIRECT-COMPARISON-ELIGIBILITY | PASS_WITH_DECLARED_PROFILE_LIMITS |
| DBR-18 Query usability and historical retrieval | RKRS-03, RKRS-04 | queries/*.sql, historical version lookups | EXACT-VERSION-PINNED-LOOKUP, DIRECT-COMPARISON-SAME-PINS, DIRECT-COMPARISON-MISSING-TIME, DIRECT-COMPARISON-DIFFERENT-VERSION, HISTORICAL-ANSWER-UNCHANGED-AFTER-NEW-VERSION | PASS_WITH_DECLARED_PROFILE_LIMITS |
| DBR-19 Measured workload and index evidence |  | four workload SQL files, answer oracles, EXPLAIN QUERY PLAN, timing samples | pinned_result, source_trace, assessment_results, historical_versions | PASS_WITH_DECLARED_PROFILE_LIMITS |
| DBR-20 Bounded concurrent transactions |  | two-connection WAL/snapshot/writer conflict | TWO-CONNECTION-WRITER-CONFLICT-RETRY | PASS_WITH_DECLARED_PROFILE_LIMITS |
| DBR-21 Configured trust boundaries |  | parameter binding, field whitelist, connection policy, schema/data health | MIGRATION-LEDGER-DRIFT, MIGRATION-SCHEMA-DRIFT, CONNECTION-FK-OFF, CONNECTION-TRIGGERS-OFF, BOUND-PARAMETER-SQL-INJECTION-LEXEME, SCHEMA-TAMPERING-DETECTED | PASS_WITH_DECLARED_PROFILE_LIMITS |
| DBR-22 Engine/runtime evidence |  | declared and actual runtime/configuration | engine | PASS_WITH_DECLARED_PROFILE_LIMITS |
| DBR-23 Artifact versions and trace integrity | RKRS-12 | versioned manifest, artifact/requirement/case crosswalk, source hashes | component/requirement/case references | PASS_WITH_DECLARED_PROFILE_LIMITS |
| DBR-24 Scoped release readiness | RKRS-11, RKRS-12 | all retained scoped gates | all current DBR-01..DBR-23 evidence | PASS_WITH_DECLARED_PROFILE_LIMITS |
| DBR-25 PostgreSQL implementation |  | future PostgreSQL work |  | NOT_RUN_FUTURE |
| DBR-26 Private full-schema migration |  | future authorized private full-schema migration |  | NOT_RUN_FUTURE |
| DBR-27 General formulas, intervals and workflow | RKRS-05, RKRS-08 | future formula/interval/workflow semantics |  | NOT_RUN_FUTURE |
| DBR-28 Deployment and user acceptance |  | future real user/deployment acceptance |  | NOT_RUN_FUTURE |

## Original ORSD crosswalk

| Original requirement | DBR derivations | Current boundary |
| --- | --- | --- |
| RKRS-01 | DBR-01 | DERIVED_SUBCLAUSES_ONLY_NOT_FULL_ORSD_ACCEPTANCE: Current DBR scope supplies only the named subclauses; original semantic/application acceptance is not inherited. |
| RKRS-02 | DBR-02 | DERIVED_SUBCLAUSES_ONLY_NOT_FULL_ORSD_ACCEPTANCE: Current DBR scope supplies only the named subclauses; original semantic/application acceptance is not inherited. |
| RKRS-03 | DBR-02, DBR-05, DBR-10, DBR-18 | DERIVED_SUBCLAUSES_ONLY_NOT_FULL_ORSD_ACCEPTANCE: Current DBR scope supplies only the named subclauses; original semantic/application acceptance is not inherited. |
| RKRS-04 | DBR-03, DBR-04, DBR-06, DBR-17, DBR-18 | DERIVED_SUBCLAUSES_ONLY_NOT_FULL_ORSD_ACCEPTANCE: Current DBR scope supplies only the named subclauses; original semantic/application acceptance is not inherited. |
| RKRS-05 | DBR-08, DBR-27 | DERIVED_SUBCLAUSES_ONLY_NOT_FULL_ORSD_ACCEPTANCE: Current DBR scope supplies only the named subclauses; original semantic/application acceptance is not inherited. |
| RKRS-06 | DBR-06, DBR-07 | DERIVED_SUBCLAUSES_ONLY_NOT_FULL_ORSD_ACCEPTANCE: Current DBR scope supplies only the named subclauses; original semantic/application acceptance is not inherited. |
| RKRS-07 |  | NO_CURRENT_DB_IMPLEMENTATION: Responsibility and actual mandates are outside this assessment/result slice. |
| RKRS-08 | DBR-12, DBR-27 | DERIVED_SUBCLAUSES_ONLY_NOT_FULL_ORSD_ACCEPTANCE: Current DBR scope supplies only the named subclauses; original semantic/application acceptance is not inherited. |
| RKRS-09 |  | NO_CURRENT_DB_IMPLEMENTATION: External/mode bearer boundary remains in the model; no new full relational bearer mapping. |
| RKRS-10 |  | NO_CURRENT_DB_IMPLEMENTATION: Appetite, tolerance and threshold task tables are not implemented here. |
| RKRS-11 | DBR-01, DBR-03, DBR-17, DBR-24 | DERIVED_SUBCLAUSES_ONLY_NOT_FULL_ORSD_ACCEPTANCE: Current DBR scope supplies only the named subclauses; original semantic/application acceptance is not inherited. |
| RKRS-12 | DBR-01, DBR-23, DBR-24 | DERIVED_SUBCLAUSES_ONLY_NOT_FULL_ORSD_ACCEPTANCE: Current DBR scope supplies only the named subclauses; original semantic/application acceptance is not inherited. |

## Original CQ crosswalk

| CQ | Current database evidence | Remaining boundary |
| --- | --- | --- |
| RQ-CQ01 | BASE_PROFILE_EVIDENCE_ONLY | Selected case/entry joins remain the original public profile, not independently adjudicated cases. |
| RQ-CQ02 | NOT_IMPLEMENTED | No scenario-to-case relational population is added. |
| RQ-CQ03 | SCOPED_SQL_TASK_SUPPLEMENT | Equal lexical scores retain distinct pins; no arithmetic/ranking is supplied. |
| RQ-CQ04 | NOT_IMPLEMENTED | Assignment/actual mandate mapping remains separate. |
| RQ-CQ05 | NOT_IMPLEMENTED | No full workflow/cessation engine or acceptance is supplied. |
| RQ-CQ06 | SCOPED_SYNTHETIC_SQL_TRACE_ONLY | Source FK/locator/origin engineering; not the independent literature/source accuracy population. |
| RQ-CQ07 | NOT_IMPLEMENTED_GENERAL_CORRECTION | Artifact version grouping and original entry lineage do not implement general corrected-assertion semantics. |
| RQ-CQ08 | BOUNDARY_PRESERVED_NOT_FULL_TASK | No new governed organizational case is admitted; no original independent population is relabeled. |
