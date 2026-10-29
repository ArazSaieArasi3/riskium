# Schema 9: assessment decision ledger

Migration 9 adds one STRICT table, two indexes, one audit view and four guards. Earlier tables, views, guards, migration hashes and native projections are preserved. `assessment_snapshot` remains the owner of a whole result bundle; the new table records supplementary documentary decisions.

| Field | Ownership and constraint |
| --- | --- |
| ordinal | INTEGER primary key, assigned by SQLite AUTOINCREMENT; durable sequence must be consecutive and positive. API input excludes it and SQL guards reject supplied ordinals. |
| event_id | Unique nonblank documentary event identifier; duplicate IGNORE/REPLACE operations are rejected. |
| kind | SELECT, WITHDRAW or CLEAR; unsupported operations are rejected. |
| assessment_id | Foreign key to the existing artifact; requires existing RKM-C032 membership. |
| decision_context_id | Nonblank application context key; not an assertion of a native context/version. |
| target_version | Foreign key to a version; SELECT/WITHDRAW require an issued assessment snapshot of the same artifact. CLEAR requires null. |
| actor | Nonblank documentary attribution, with no inferred authorization or mandate. |
| reason | Nonblank explanation of the explicit decision. |
| source_record_id | Existing source record for the decision, separate from assessment and result sources. |
| source_locator | Nonblank locator within the decision source. |
| interpretation_origin | Nonblank statement of interpretation origin. |
| recorded_at | Canonical UTC calendar timestamp; cannot precede the target's issuance. This is not a general validity/interval engine. |

The primary key determines the event row; the unique event ID is an alternate key. Both target and assessment are retained to support CLEAR and a stable context history. The cross-target guard enforces their coherence. No universal domain normalization claim follows from this implementation choice.

`assessment_selection_context(assessment_id, decision_context_id, ordinal)` supports explicit as-of retrieval. The partial withdrawal index adds the target version for sticky context-local withdrawal checks. These are query-based design choices, not measured production performance guarantees.

`v_assessment_selection_invalid` detects missing provenance, invalid time/event/assessment/target, reselecting a withdrawn version and invalid sequence. Insert guards validate actual rows; update/delete guards preserve event immutability. The API additionally validates exact input fields and runs original semantic audits, foreign-key/integrity checks, exact schema and migration hashes. Both assessment and earlier evidence allocators are audited separately.

Migrations and writes use BEGIN IMMEDIATE or a nested savepoint. A failed inner operation preserves the caller's earlier changes and leaves the caller able to roll back. Issue failure removes partial identities, sealed versions, result rows and correction edges together. Historical queries order by assigned sequence, including when timestamps and display names disagree.

Recovery checks SQLite backup and real close/reopen. Logical dump restoration requires an independently retained expected logical-state digest; merely receiving a digest alongside an edited dump does not authenticate it. Schema/data/allocator audits and the final digest check run before commit. External database statements are rejected. Guard weakening is tested only in a disposable database copy.

The existing native assessment graphs remain version-scoped. Selection does not union historical interpretations, choose a scalar from multiple results, compute a score, promote incomplete data or infer independent corroboration.
