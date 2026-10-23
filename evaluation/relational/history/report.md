# Executed SQLite identity and issued-history slice 0.1.0

**Scoped application/history evidence, not full relational or ontology acceptance.** Model/OWL unchanged; no PostgreSQL run or owner/independent judgment is claimed.

Execution checkout `11ffed4f4e74a61909c92395201b9abe29798f44`; [full compressed receipt](report.json.gz), [mapping](../../../implementation/relational/0.1.0/mapping.json) and [scope/dictionary](README.md). Exact input hashes bind all executed files.

Engine: SQLite 3.53.1; foreign_keys=ON and recursive_triggers=ON. Schema 1 is populated from public synthetic fixtures, then upgraded transactionally to schema 2 without rebuilding its rows. The private historical companion is not copied or migrated by this suite.

Summary: {"scenarios": 67, "statuses": {"PASS": 67}, "by_kind": {"migration": 9, "preflight": 2, "operation": 48, "mutation-control": 4, "roundtrip": 4}, "native_relations_exported": 5, "concepts_and_support_kinds": 10}. SQL traces, exact errors, before/after logical/schema/ledger snapshots, migration rollback and selected round trips are retained. A PASS means the expected acceptance, rejection or control outcome matched; mutants are not admitted domain cases.

| Case | Kind | Expected SQL error | Verdict |
| --- | --- | --- | --- |
| `MIGRATE-POPULATED-V1` | migration | — | PASS |
| `MIGRATE-IDEMPOTENT` | migration | — | PASS |
| `MIGRATE-INVALID-CYCLE-ATOMIC` | migration | R-MIGRATION-CYCLE | PASS |
| `MIGRATE-INVALID-DEPENDENCY-ATOMIC` | migration | R-MIGRATION-DEPENDENCY | PASS |
| `MIGRATE-INVALID-CONTENT-ATOMIC` | migration | R-MIGRATION-ISSUED-CONTENT | PASS |
| `MIGRATE-INVALID-REVISION-ATOMIC` | migration | R-MIGRATION-REVISION-TARGET | PASS |
| `MIGRATE-FOREIGN-KEY-ATOMIC` | migration | R-MIGRATION-FOREIGN-KEY | PASS |
| `MIGRATE-SOURCE-HASH-DRIFT` | migration | R-MIGRATION-SOURCE-HASH | PASS |
| `MIGRATE-SCHEMA-DRIFT` | migration | R-MIGRATION-SCHEMA-DRIFT | PASS |
| `CONFIGURATION-REQUIRED` | preflight | R-CONNECTION-POLICY: foreign_keys and recursive_triggers must be ON | PASS |
| `RECURSIVE-CONFIGURATION-REQUIRED` | preflight | R-CONNECTION-POLICY: foreign_keys and recursive_triggers must be ON | PASS |
| `RAW-UNKNOWN-IS-PRESERVED` | operation | — | PASS |
| `DUPLICATE-LABELS-DISTINCT-CASES` | operation | — | PASS |
| `ONE-CASE-MULTIPLE-ENTRIES` | operation | — | PASS |
| `HISTORY-EXACT` | operation | — | PASS |
| `DEPENDENCY-SNAPSHOTS-EXACT` | operation | — | PASS |
| `NATIVE-EDGES-EXACT` | operation | — | PASS |
| `ISSUED-NO-UPDATE-PAYLOAD_JSON` | operation | R-ISSUED-IMMUTABLE | PASS |
| `ISSUED-NO-UPDATE-SOURCE_RECORD_ID` | operation | R-ISSUED-IMMUTABLE | PASS |
| `ISSUED-NO-UPDATE-ARTIFACT_ID` | operation | R-ISSUED-IMMUTABLE | PASS |
| `ISSUED-NO-UPDATE-ISSUED_AT` | operation | R-ISSUED-IMMUTABLE | PASS |
| `ISSUED-NO-UPDATE-IS_ISSUED` | operation | R-ISSUED-IMMUTABLE | PASS |
| `ISSUED-NO-DELETE` | operation | R-ISSUED-IMMUTABLE | PASS |
| `ISSUED-NO-REPLACE` | operation | R-VERSION-DUPLICATE | PASS |
| `ISSUED-NO-UPDATE-OR-REPLACE` | operation | R-ISSUED-IMMUTABLE | PASS |
| `MANAGED-ENTRY-MISSING-CASE` | operation | FOREIGN KEY constraint failed | PASS |
| `MANAGED-ENTRY-WRONG-REGISTER-KIND` | operation | FOREIGN KEY constraint failed | PASS |
| `MANAGED-ENTRY-UNKNOWN-CASE-NOT-ADMITTED` | operation | NOT NULL constraint failed: register_entry.case_id | PASS |
| `IDENTITY-CROSS-FAMILY-REFERENCE` | operation | FOREIGN KEY constraint failed | PASS |
| `CATALOG-NO-UPDATE-SOURCE_RECORD` | operation | R-CATALOG-IMMUTABLE | PASS |
| `CATALOG-NO-UPDATE-RISK_CASE` | operation | R-CATALOG-IMMUTABLE | PASS |
| `CATALOG-NO-UPDATE-INFORMATION_ARTIFACT` | operation | R-CATALOG-IMMUTABLE | PASS |
| `SOURCE-NO-REPLACE` | operation | R-CATALOG-DUPLICATE | PASS |
| `IDENTITY-NO-CROSS-FAMILY-REPLACE` | operation | R-CATALOG-DUPLICATE | PASS |
| `CATALOG-NO-DELETE-CASCADE` | operation | R-CATALOG-IMMUTABLE | PASS |
| `DEPENDENCY-NO-LATE-APPEND` | operation | R-DEPENDENCY-FROZEN | PASS |
| `DEPENDENCY-NO-UPDATE` | operation | R-DEPENDENCY-FROZEN | PASS |
| `DEPENDENCY-NO-DELETE` | operation | R-DEPENDENCY-FROZEN | PASS |
| `DEPENDENCY-NO-REPLACE` | operation | R-DEPENDENCY-DUPLICATE | PASS |
| `WORKING-DRAFT-EDITABLE` | operation | — | PASS |
| `ISSUE-NEW-REVISION-PRESERVES-OLD-PINS` | operation | — | PASS |
| `ISSUE-NEW-REVISION-SNAPSHOT-EXACT` | operation | — | PASS |
| `ISSUE-GENERIC-ARTIFACT-VERSION` | operation | — | PASS |
| `ISSUE-ROLLBACK-EMPTY-CONTENT` | operation | R-ISSUE-CONTENT-REQUIRED | PASS |
| `ISSUE-ROLLBACK-MISSING-TIME` | operation | R-ISSUE-TIME-REQUIRED | PASS |
| `ISSUE-ROLLBACK-WRONG-DEPENDENCY-KIND` | operation | R-DEPENDENCY-TARGET-KIND | PASS |
| `ISSUE-ROLLBACK-WRONG-DIRECT-ARTIFACT` | operation | R-DEPENDENCY-DIRECT-TARGET | PASS |
| `ISSUE-ROLLBACK-UNISSUED-DEPENDENCY` | operation | R-DEPENDENCY-TARGET-NOT-ISSUED | PASS |
| `ISSUE-ROLLBACK-ENTRY-WITHOUT-REVISION-TARGET` | operation | R-REVISION-TARGET-KIND | PASS |
| `REVISION-OF-EQUALS-VERSION-OF` | operation | CHECK constraint failed: revision_target | PASS |
| `PREDECESSOR-CROSS-ENTRY` | operation | R-PREDECESSOR-SAME-ISSUED-ENTRY | PASS |
| `PREDECESSOR-MISSING` | operation | R-PREDECESSOR-SAME-ISSUED-ENTRY | PASS |
| `PREDECESSOR-SELF-CYCLE` | operation | R-PREDECESSOR-CYCLE | PASS |
| `PREDECESSOR-BRANCH-ALLOWED` | operation | — | PASS |
| `PREDECESSOR-SKIP-ALLOWED` | operation | — | PASS |
| `PREDECESSOR-17-CHAIN` | operation | — | PASS |
| `CYCLE-DETECTED-WITHOUT-IMMUTABILITY` | mutation-control | R-PREDECESSOR-CYCLE | PASS |
| `DELETED-IMMUTABILITY-EXPOSES-CHANGE` | mutation-control | — | PASS |
| `DELETED-DEPENDENCY-GUARD-EXPOSES-APPEND` | mutation-control | — | PASS |
| `DELETED-CYCLE-GUARD-EXPOSES-CYCLE` | mutation-control | — | PASS |
| `TRANSACTION-FAILURE-ROLLS-BACK-PRIOR-WRITES` | operation | R-ISSUED-IMMUTABLE | PASS |
| `FILE-CLOSE-REOPEN-MIGRATION` | roundtrip | — | PASS |
| `SQL-DUMP-RESTORE-EXACT` | roundtrip | — | PASS |
| `SQL-BACKUP-EXACT` | roundtrip | — | PASS |
| `RDF-SELECTED-FACTS-ROUNDTRIP` | roundtrip | — | PASS |
| `FOREIGN-KEY-CHECK` | operation | — | PASS |
| `INTEGRITY-CHECK` | operation | — | PASS |

Replay with `python tools/run_relational_history.py --check`. Runtime versions are recorded per execution; the semantic/schema/state comparisons must match across supported SQLite >=3.38 environments. Byte-identical database files across SQLite versions are not claimed.
