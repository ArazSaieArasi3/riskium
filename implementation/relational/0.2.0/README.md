# Public SQLite assessment/result profile 0.2.0

This additive engineering profile extends the unchanged public identity/history schema 0.1.0 with six tables, migration 3, an explicit type strategy and version-owned interpretation facts. It is compatible with conceptual model 0.3.1 and separately specified by DRSD 0.1.0. It changes no native ontology, original ORSD priority, manuscript claim, stable v0.3.1 tag or historical engine outcome.

[Policy and decisions](policy.json), [native mapping and scope](mapping.json), [R2RML export declaration](mapping.ttl), [schema tables](003_assessment_tables.sql), [generated guards/views/indexes](003_assessment_guards.sql), [actual dictionary and dependency review](schema-dictionary.md), [frozen synthetic fixtures](fixtures.json), [executed receipt](../../../evaluation/relational/assessment/README.md), [assurance checklist and methods](../../../docs/relational-assurance.md).

The [selected relational ownership diagram](schema-ownership.md) explains how the new tables retain base identity and version ownership; the dictionary/DDL owns exact physical details.

| Table | Purpose | Version/identity boundary |
| --- | --- | --- |
| artifact_typing | Explicit membership for assessment, basis, result, level and dimension | Existing generic InformationArtifact identity; typing must precede any issue; vocabulary uses scheme/edition/code keys |
| scale_snapshot | Declared scale/version/dimension | Metadata staged before issuing its scale version and frozen afterward |
| scale_level | Level membership in a selected scale version | Managed level identity is not a bare label or value |
| method_scope | Method-version permission for scale/dimension | Composite-key many-to-many association; no current/latest permission substitution |
| assessment_snapshot | Context/method/basis pins and distinct time qualifiers | Owned by one assessment version; optional direct assertions are preserved rather than inferred |
| result_snapshot | Qualified dimension result, selection, source and lexical value | Owned by one result version and one assessment version; multiple qualified values stay distinct |

The selected native export has 14 additional predicates; combined with the original five, the current slices expose 19 distinct predicates. Five new artifact subtypes add to the original ten explicit representations. These counts describe selected mapping support, not complete class/constraint acceptance. The exhaustive current inventory marks every other source element explicitly. SQL/RDF projection is version-qualified and synthetic tests do not establish independent semantic adequacy.

Issued bundle payload JSON contains the exact declared assessment/result metadata. Seal guards check payload/relational agreement. Role references must name issued correctly typed versions; explicit artifact targets must agree. Sealed metadata cannot change/delete/replace or gain late children. A result identity cannot silently move to a different assessment identity. The supported issue API wraps parent and result sealing in one transaction.

`v_assessment_frame` supports exact version-based queries. `v_assessment_quads` emits selected native and declared comparison-profile facts in a separate named graph for each issued assessment version. Combining specifically selected compatible graphs for a comparison is explicit; silently unioning all historical interpretations is unsupported. The original base `v_native_facts` is unchanged. No numeric score predicate is invented: lexical reported values and their source qualifiers stay SQL/application fields, and COMPUTED claims are rejected.

Recorded, reference and validity times are separate. Canonical UTC calendar strings and simple supplied endpoint order are checked; general interval/workflow reasoning is absent. Assessment version grouping preserves old payloads and answers, but no generic assessment correction/supersession relation is implemented. Source presence is not proof of truth or corroboration.

Migration 3 verifies the exact configured v2 base schema/ledger before extension and preserves all base rows. New v3 files require the new reader/API; the old v2-only migration reader rejects them rather than pretending compatibility. Earlier scale/method versions lacking newly scoped metadata are not backfilled or made task-ready. Backup/dump restoration checks actual data semantics as well as FKs, hashes and schema.

The [five query examples](queries/) use bound parameters. Every table/column and declared FD is documented. Guarded redundant direct/version references are explicit; no universal one-table-per-class, minimum-column-count rule, normal-form proof or production-performance guarantee is asserted.

```sh
python tools/build_relational_assessment.py --check
python tools/run_relational_assessment.py --check
python tools/check_database_assurance.py --check
```

Replays execute the frozen 48 fixed controls, 100 seeded inputs, two SQL-projection SHACL checks and four measured workload patterns. Two deliberately deleted-rule controls demonstrate sensitivity, not valid domain data. PostgreSQL, the private full-schema migration, justified formula/workflow engines and actual user/production acceptance remain separately unexecuted.
