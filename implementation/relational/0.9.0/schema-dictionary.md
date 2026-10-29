# Schema 10: risk-nature assertions

Migration `010_risk_nature.sql` adds eight STRICT tables, four query indexes, immutable-row/duplicate/frozen-link guards and two semantic audit views. It changes no prior schema object. [The generator](../../../tools/build_risk_nature_schema.py) is deterministic; the runtime executes only the reviewed SQL file. [The runtime API](../../../tools/relational_risk_nature.py) validates exact migration hashes, schema, configured foreign keys/recursive triggers, integrity and prior/new semantic data.

## Tables and dependencies

| Table | Fields, keys and purpose |
| --- | --- |
| nature_membership | artifact_id PK/FK to existing generic C014 identity; native_class constrained to C005/C006/C018/X02; optional scheme_id FK and code required only for C006. UNIQUE(scheme_id,code) is the scheme-qualified alternate term key. Essential membership cannot be attached to an issued artifact or reused by earlier profile memberships. |
| nature_support | version_id PK/FK; artifact_id FK; native_class; narrative, source_record_id FK, source_locator, interpretation_origin, recorded_at; code and scheme_version_id FK only for C006. One version determines its complete immutable semantic row. Scheme targets must be issued C018; version source/owner/time/payload must agree with the base snapshot. |
| nature_context | version_id PK/FK; artifact_id FK to a C002 identity; the five narrative/provenance/time fields above. Its complete sorted objective-version list belongs to its payload. Only unissued new context versions can acquire these rows/links. |
| nature_objective | context_version_id FK plus objective_version_id FK form the PK; objective_id FK is checked against the target version owner. UNIQUE(context_version_id,objective_id) prevents conflicting version pins for one objective in a context. Targets must be issued X02 versions. |
| nature_snapshot | version_id PK/FK; artifact_id FK to C005 membership; case_id required FK; term_version_id required FK; context_version_id nullable FK; narrative/provenance/time fields. A version determines all interpretation pins. An assertion artifact retains one case across this bounded version family. |
| nature_entry | version_id PK/FK; entry_id FK; nullable previous_version_id FK; narrative/provenance/time fields. Its sorted exact nature-version list belongs to its immutable payload. Base entry/version guards preserve same-entry issued predecessor and acyclic entry history. |
| nature_entry_link | (entry_version_id,nature_version_id) PK and FKs. Both sides must be unissued when a new binding stages. At least one recording revision is required when an assertion seals; entry and assertion cases must match. Final health rejects a sealed entry pointing to an unissued nature version. |
| nature_correction | corrected_version_id PK/FK; prior_version_id FK; actor, reason, source_record_id FK, source_locator, interpretation_origin, recorded_at. The child determines one predecessor and complete declaration qualifiers. Both endpoints must be issued versions of the same artifact/case, with no self/cycle. The inverse is many, preserving branches. |

The five repeated narrative/provenance fields deliberately belong to each issued record. Their source roles may differ. Original source JSON lives verbatim in the existing append-only `source_record`; labels remain immutable catalog presentation values and are excluded from semantic snapshots. Term code is stable under its scheme identity, while term/scheme wording can have distinct issued versions. No label or file path is a key for semantic identity.

## Payloads and SQL constraints

`v_nature_expected_payload` reconstructs each supported semantic record with sorted field names and sorted list bindings. Issued JSON must equal this canonical representation; unknown/extra/missing fields and wrong null/list/scalar types cannot silently change the issued meaning. `v_nature_invalid` checks provenance, valid UTC calendar timestamps, owner/source/time coherence, native kinds, exact issued dependency versions, objective ownership, case continuity, recording links and corrections. Sealing checks these views after all child links stage, and checks the required issued recorders. Internal staging may contain unsealed targets while the atomic bundle is being assembled.

Every new table rejects UPDATE/DELETE and duplicate INSERT conflict algorithms. Inserts cannot attach semantic facts or links to an already-issued version. Nulls are retained only where declared, such as optional context and absent entry predecessor. Provenance strings require nonblank text. The generator materializes Python's complete Unicode whitespace set into SQL guards, aligning raw SQL and API rejection, including nonbreaking spaces. Full original-source truth or Unicode normalization is not inferred from storage validity.

SQL guards provide configured-connection protection. Health rechecks their exact definitions as well as semantic views, foreign keys, existing allocators and integrity. A changed logical dump with structurally valid altered history may still satisfy constraints; restoration therefore also requires a separately trusted complete logical-state digest. Administrator file/DDL privileges and an attacker controlling both a file and its claimed digest remain outside logical authentication guarantees.

## Queries and indexes

| Index or key | Consumer and rationale |
| --- | --- |
| nature_by_case(case_id,version_id) | Bound all-issued case query and deterministic ID ordering; workload plans verify indexed lookup. |
| nature_by_artifact(artifact_id,version_id) | Case-continuity checks across versions of one assertion artifact. |
| nature_children(prior_version_id,corrected_version_id) | Recursive explicit-root correction-family traversal. |
| nature_recorders(nature_version_id,entry_version_id) | Exact-version recording list and required-recorder checks. |
| Snapshot PKs | Direct exact-version retrieval and exact dependency joins. |
| Objective PK and unique key | Ordered objective-version lists and one pin per objective artifact/context. |

The three bound queries are in `queries/`. No SQL identifier is assembled from caller input. RDF output is generated from actual pinned SQL rows through the public exact-version projection, with the original model identifiers and inherited types. Each named graph is compared in full with the preimplementation literal graph. Historical union, source records as RiskSource, direct nature/objective predicates, native correction and version-as-C005 typing are excluded.

## Transactions and measured limits

Public writes use BEGIN IMMEDIATE or a nested savepoint. Failure preserves the caller's earlier state and ability to roll back. Upgrade preserves every old row, schema object, migration hash and old native view. File backup/reopen, logical restore, edited-dump rejection and real two-connection read visibility/writer conflict/retry are replayed. The fixture uses ordinary SQLite journal behavior and busy_timeout=0 for a bounded explicit conflict test; no general concurrent deployment guarantee is claimed.

Workloads contain 200/400 distinct synthetic reports (seeds 17/29), distributed across four cases with 50/100 rows each. Each measured query has five warmups and 31 repetitions, recorded median/p95, construction digest and actual EXPLAIN plan. These are direct SQL query timings; full public-API health and source checks add cost. They are not production latency/SLO or semantic accuracy estimates. The independently downloaded exact-source receipt, engine versions and final outcome are recorded under #65.
