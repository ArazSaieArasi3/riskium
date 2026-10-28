# Evidence-reference lifecycle 0.7.0: schema and query review

Migration 8 adds one STRICT application table, its four explicit indexes, ledger/invalid-data views and four guards. SQLite also owns its AUTOINCREMENT allocator table. Earlier schema objects, rows, migration bytes and named native projections remain unchanged.

## Ownership and dependencies

`event_id` and `ordinal` are candidate keys. Each determines the entire event row. A C065 artifact owns many immutable issued versions and many supplementary lifecycle events; context-qualified decisions concern that artifact, and CORRECT links two of its issued versions. Context and actor attribution are application metadata, not new native identities or verified mandates.

| Column | Ownership and constraint |
| --- | --- |
| ordinal | SQLite-assigned positive AUTOINCREMENT primary key; contiguous committed order is checked. Ledger sequence is ordinal × 10, bounded within SQLite integer range. |
| event_id | Nonempty unique external event/request identity. Duplicate insertion and replacement abort. |
| kind | CORRECT, SELECT, WITHDRAW or CLEAR, with distinct nullable-field rules. |
| artifact_id | Existing InformationArtifact FK; guards require its already represented C065 membership and matching endpoint ownership. |
| context_id | Required nonempty supplementary policy context for SELECT/WITHDRAW/CLEAR; null for CORRECT. |
| version_id | Exact issued C065 version FK; null only for CLEAR. |
| prior_version_id | Exact issued C065 version FK for CORRECT; null for other kinds. One immutable parent per corrected child, acyclic and same artifact. |
| actor_id | Nonempty documentary attribution; no native actor identity or access-control conclusion follows. |
| reason | Required nonempty documentary rationale. |
| recorded_at | Supplied canonical real-calendar UTC metadata. This is not an authenticated clock or world-validity interval; sequence is ingestion order. |
| source_record_id | Existing source FK, distinct from artifact origin and either endpoint's source. |
| source_locator | Required nonempty locator within the attributed source. |
| interpretation_origin | Required nonempty interpretation provenance. |

All fields are immutable after append. Endpoint payloads/item/target pins remain owned by the original v7 tables. New normalized joins preserve original source JSON; the event row does not duplicate that JSON. Every read/write audits all eight migration hashes, exact schema, connection configuration, FKs/integrity, earlier semantic checks, current event semantics and allocator state.

## Index rationale

| Index | Reason |
| --- | --- |
| Implicit unique event_id index | Enforces request identity and serves exact event lookup; a second event-id index would be redundant. |
| evidence_lifecycle_one_parent | Partial unique corrected-version key for CORRECT; enforces one parent and serves child/declaration joins. |
| evidence_lifecycle_parent | Partial predecessor/child index for recursive all-branch traversal. |
| evidence_lifecycle_context | Partial context/artifact/ordinal index for the last SELECT/CLEAR at an explicit ledger bound. |
| evidence_lifecycle_withdrawal | Partial context/artifact/version/ordinal index for withdrawal existence within that bound. |

These choices follow the actual bound queries and key constraints. Real production volume/concurrency and performance SLOs are outside this packet. Event counts and indexes are not a database-quality score.

Local SQLite 3.53.1 EXPLAIN QUERY PLAN used the context and covering withdrawal indexes for selection, and the predecessor and unique-child indexes for family traversal. Ordering by the computed public sequence also used a temporary sort. This observation is recorded as local query review, not a production latency guarantee.

## Transaction, query and recovery behavior

`append` and `issue_corrected` use BEGIN IMMEDIATE or a caller-preserving savepoint. Failed atomic issue removes the new version identity, declaration and allocator advance while retaining earlier outer writes. SQLite guards also enforce direct-SQL boundaries. Old exact-schema readers reject v8; the new reader accepts only populated validated v7 upgrades or already validated v8 databases.

The selection query requires artifact, context and an explicit nonnegative integer as-of sequence. It reads the last SELECT/CLEAR and notices known by that bound. A withdrawn selected version returns WITHDRAWN and a null selected pointer, retaining the old version ID in the result/history. There is no newest-version fallback. CLEAR preserves earlier events and does not undo withdrawal; reinstatement is deferred.

Family traversal preserves all declared correction branches and exposes each endpoint source separately from declaration source. Native export uses the exact unchanged per-version v7 graph; it does not project decisions or union history.

Backup/reopen and SQL dump recovery compare actual state. Dump restoration recreates tables, rows and schema, then preserves SQLite allocator statements in their original order before auditing inside the transaction. Inconsistent restored pins, prior payloads, withdrawals or allocator clocks cause full rollback. This is engineering integrity, not cryptographic authenticity against an administrator who coherently rewrites an entire database.
