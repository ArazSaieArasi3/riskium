# Executed relational identity/history profile 0.1.0

Current conceptual baseline: **0.3.1**, unchanged. This is a new bounded public SQLite profile, not the complete historical companion. [Mapping and exact source signatures](../../../implementation/relational/0.1.0/mapping.json), [SQL tables](../../../implementation/relational/0.1.0/001_tables.sql), [generated guards/views](../../../implementation/relational/0.1.0/002_guards.sql), [synthetic fixture and independent expected history/edges](../../../implementation/relational/0.1.0/fixtures.json), [readable execution receipt](report.md), [full receipt](report.json.gz). Completion is tracked by #24 under open parent #12.

## Provenance and actual execution

The private `Riskium_SQLite_v0.3.0-rc.1_integrated_review.zip` was inspected read-only for schema names (128 tables). Archive SHA256 `0a7abf11cd143f1b02027eb77f4f5bfcee613021d9eebb63bb7c46fa81f8d220`; embedded ontology SHA256 `503e6753496be60fb9aaa5592633506823f769070cd8bc9dbba853929473b230`. That source differs from the current model SHA256 `4a052bb0b7321e5209417c69e96644089aa7dba1734cce4a70e5223f2ebbaf59`. Its historical 859 checks were **not rerun** and are not current evidence. No private rows, schema implementation or binary are included here.

Execution used SQLite **3.53.1** locally; each hosted replay records its own actual version in stdout/environment. Supported runtime is SQLite >=3.38 with foreign_keys=ON and recursive_triggers=ON. PostgreSQL was not executed. Schema 1 is created and populated with the new public fixture; schema 2 transactionally audits those existing rows and installs guards, indexes and views. Failed audits leave data/schema/ledger unchanged. This is an executed populated upgrade of this profile, **not migration of the private 128-table database**.

The 67 scenarios have fixed expected outcomes: 9 migration, 2 configuration preflight, 48 operations, 4 deliberately weakened guard controls, and 4 round trips. Each case records actual SQL trace, exact errors, independent expected/observed results and before/after row/schema/ledger hashes. Rejection must match the intended SQL error; an unrelated error fails. Mutant success demonstrates test sensitivity, not an acceptable domain record. Round trips cover file close/reopen, SQL dump/restore, SQLite backup API, and serialization/reparse of the selected native RDF facts. No full database-to-ontology equivalence or disaster recovery certification is claimed.

## Dictionary: all stored fields

| Table | Fields and meaning | Native versus supplementary |
| --- | --- | --- |
| source_record | record_id: source key; original_json: exact raw JSON, including null and unresolved input | Supplementary append-only provenance/staging; preservation does not admit an incomplete domain record |
| identity_registry | resource_id: exact governed IRI-like identifier; family: case/artifact/version | Supplementary global key discipline; labels never identify/merge entities; external identity truth is not proved |
| risk_case | case_id: RKM-X01 key; family: enforced case; label: non-unique display; source_record_id: provenance | Selected native case; family/label/provenance are storage metadata |
| information_artifact | artifact_id: RKM-C014 or supported subtype key; family: artifact; kind: declared native class; label; source_record_id | Native artifact typing; display/provenance/family supplementary; append-only metadata is a local policy |
| register_entry | entry_id: RKM-C022 artifact; entry_kind: fixed type; case_id: R-01 recordsAbout; register_id: RX-008 memberOfRegister; register_kind: fixed RKM-C030 | Native edges and typed foreign keys; type columns are storage enforcement |
| working_draft | draft_id; artifact_id; entry_id; previous_version_id; payload_json; source_record_id | Entire row is application staging, editable and excluded from native issued-version export |
| draft_dependency | draft_id; slot: Context/Method/Scale/Criteria; target_version_id; optional direct_artifact_id | Supplementary pending version bindings; draft deletion cascades only these staging rows |
| version_snapshot | version_id: sealed RKM-C015; family: version; artifact_id: RX-006 versionOf; entry_id: sealed RKM-C023/R-33 revisionOf; previous_version_id: R-34; payload_json: serialized snapshot; source_record_id; issued_at; is_issued: 0 staging / 1 sealed | Only sealed rows export native Version/Revision facts. Payload/state/time/provenance supplementary. No fabricated InformationContent instance or full RX-007 encoding |
| version_dependency | owner_version_id; slot; target_version_id: already issued typed version; optional direct_artifact_id: must equal target's versionOf | Supplementary version-owned immutable snapshot bindings, **not** native assessment usesVersion assertions |
| schema_migration | version: applied migration number; sha256: exact executed SQL bytes | Supplementary migration ledger; PRAGMA user_version must agree |

`v_issued_history` retrieves sealed payloads/provenance and stable entry/case/register joins. `v_native_facts` emits selected typing and exactly five source relations: R-01, RX-008, R-33, R-34, RX-006. It does not invent native predicates for storage fields. Four indexes have no measured workload-performance claim.

## Clause dispositions

| Clause | Executed current route | Remaining boundary |
| --- | --- | --- |
| C-01 | Typed mandatory case/register references; equal labels retain distinct case keys; multiple entries may record the same case | Full case identity/source truth and all task admission remain separate |
| C-03 | Issued payload, provenance, identity/target, time and owned dependencies cannot change/delete/replace; new issue is atomic and preserves prior pins/history | Supplementary serialized payload, not full InformationContent/RX-007 admission or universal security guarantee |
| C-24 | revisionOf equals versionOf; predecessor must be an issued revision of the same entry; self/cross-entry/missing/cyclic links rejected; branches, skipped predecessors and 17-node chain exercised | No full temporal chronology or complete relational/ontology acceptance |
| C-25 | C-25-style Context/Method/Scale/Criteria target-kind and optional direct-versus-version target coherence, pinned at issue | Version-owned application bindings do not replace native assessment subject admission, required-role coverage or complete C-25 validation |

All historical HermiT/SHACL rows and denominators remain unchanged; no HermiT PASS is inferred from SQL. Owner/independent judgment is not supplied. Full #12 mapping/migration/formulas/workloads, real cases, time intervals, concurrent production operation and scoring are not claimed. DDL/PRAGMA disabling can bypass storage guards; the configured connection plus schema-health checks define the supported contract. Cyclic dependency cohorts are unsupported because dependencies must already be issued.

## Reproduce

```sh
python tools/build_relational_history.py --check
python tools/run_relational_history.py --check
python -m unittest discover -s tests -p test_relational_history.py -v
python tools/run_relational_history.py --database /tmp/riskium-history-demo.sqlite
```

The database output path must not exist. The last command creates public synthetic data only. Use `relational_history.connect/migrate/issue_draft` for the supported lifecycle. Dump restore creates all tables before rows (deferred foreign keys still require referenced tables to exist), checks all FKs transactionally, then restores/checks the ledger version. The receipt binds exact executed source hashes and checkout; regenerating it is explicit. Replays compare logical schema/state/outcomes across supported runtimes, not binary database bytes. Owner review and final acceptance remain governed by [the fixed final gates](../../../docs/stable-release-gates.md).
