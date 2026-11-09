# Explicit evidential-use SQLite and RDF slice

Date: 2026-11-09. Scope: **B0-5 / P2** for [issue #93](https://github.com/ArazSaieArasi3/riskium/issues/93). The bounded synthetic SQLite/RDF slice is complete. **This is a candidate sidecar, not a production migration, PostgreSQL implementation or completed ontology release.**

## Selected design

The existing SQLite v7 reader checks an exact schema and its issued historical snapshots. Adding new tables directly would violate that reader's contract. This packet leaves v7 untouched and copies its issued documentary snapshots into a separate, explicitly version-bound sidecar. [contract.json](contract.json) pins the source fixture, candidate export contract, combined SHACL profile, SQL/RDF queries and implementation/test inputs.

Import preserves four reference snapshots, their exact item/context version pins, documentary identities and proposed purposes. Import creates **no EvidenceUseRelator, EvidenceReferenceRole or EvidenceItem assertion**. The new information-only RDF route types the cited artifact as InformationArtifact, preserving the reference pointer and contexts. The original v7 graph, which asserted the evidence role under its historical contract, is neither rewritten nor retroactively declared invalid. Its four mismatches with the candidate profile remain reproducible compatibility observations.

An explicit use requires an existing reference version, the same item version recorded by that reference, an explicitly recorded context version, a named grounding-record version, an actual-use purpose, a recorded timestamp and a nonempty justification. The reference participates as EvidenceReferenceRole and the cited artifact as EvidenceItem only in that use projection. Roles preserve existing artifact identity. A reference's proposed purpose can differ from an explicitly justified actual-use purpose; the two fields are not silently overwritten or equated.

The three use decisions in [fixtures.json](fixtures.json) are deliberately authored **synthetic test decisions**, covering support, challenge and context. They are not inferred from legacy references, pharmaceutical records, expert judgments or organizational activity. Grounding existence and structural coherence are checked; truth or factual adequacy of the grounding is not established by a nonempty record.

## Relational and RDF contract

| Stored surface | Meaning and output |
|---|---|
| `artifact`, `artifact_version` | Copy documentary identity and exact issued-version payload digests from the source snapshot. No new enterprise RiskCase is created. |
| `reference_snapshot`, `reference_context` | Preserve the reference's item-version pointer, proposed purpose, locator and allowed context-version links. These remain information before a use decision. |
| `grounding_record` | Store a separately supplied documentary grounding version, text and locator. The RDF output identifies its artifact and version; the text/locator remain candidate application metadata. |
| `evidence_use` | Store the explicit episode and its version pins. RE-001 mediates the EvidenceItem, RE-002 mediates the participating reference, RE-003 points to the grounding record, and candidate context/purpose fields qualify the use. |
| `explicit_alias` | Record supplied alias links among imported documentary identities. Direct or transitive aliasing of the mediated participants prevents accepting a use; adding a conflicting alias after use is also rejected. This does not resolve undeclared real-world identity. |
| `metadata` | Bind the imported snapshot, schema and candidate export contract. Exact-schema checks, foreign keys and immutable-record guards protect this bounded artifact. |

[schema.sql](schema.sql) supplies strict tables, foreign keys, exact-version coherence, declared-alias checks and exact-tuple uniqueness. The Python adapter adds append-only update/delete guards, canonical UTC validation, transaction rollback and source-snapshot integrity checks. The unique tuple uses the exact reference/item/context/grounding versions and purpose; adjudicating equivalent episodes described under different grounding identities remains a separate identity problem. Corrections and operational temporal reconciliation are outside this slice.

Standalone `use-N.ttl` files are version-qualified projections. The generated TriG file preserves one named graph per use. Application version pins, grounding text/locator and decision metadata use candidate `eu:` properties; they are not new native OntoUML relations. The selected SQL/SPARQL comparison runs over the union of these use graphs and retains explicit version pins in its answer columns.

## Executed evidence

[verification-report.json](verification-report.json) records the actual checks and output hashes.

| Check | Actual result and supported interpretation |
|---|---|
| Sidecar unit tests | **21/21 pass.** These exercise import without inferred use, version pins, information-only references, SQL/SPARQL answers, incomplete/invalid inputs, duplicate episodes, direct/transitive/late aliases, direct SQL rejection, append-only behavior, schema drift, connection policy, backup/reopen, controlled dump recovery and tampered-dump rollback. |
| Frozen baseline regression | **21/21 pass:** 16 qualified-evidence tests and five source-transition tests. The embedded original fixture replay keeps its own denominator and is not added to this test count. |
| SHACL outcomes | **17/17 match expectations:** four historical incompatibilities are reconfirmed, four new information projections conform, three explicit-use projections conform, and six corrupted exports reject. The candidate OWL is supplied as the ontology graph; inference and imports are disabled. |
| Selected query parity | The ten-column SQL and SPARQL answers agree for all three explicit use records. Removing one use from the RDF export changes the answers and is detected. This establishes parity of this query on this fixture, not general SQL/SPARQL equivalence. |
| Source and database integrity | The original v7 schema/data state hash is unchanged before/after the sidecar run. Sidecar SQLite integrity is `ok` and foreign-key violations are zero. Backup/reopen and audited dump recovery retain the checked state. |

The first integration run exposed a purpose-literal representation mismatch against the pinned shape's enumeration. The exporter was corrected to emit the same RDF string term representation, and a dedicated profile-enumeration regression was added. All results above belong to the final corrected run; the shape was not weakened to obtain acceptance.

## Replay

Use the Python dependencies from the [B0-1 replay instructions](../issue93-evidence-use/README.md#replay). A fresh checkout first rebuilds the deterministic candidate input and B0-4 output. Then:

```sh
python evaluation/manuscript-review/v7.2.3/issue93-generalization-sets/build_candidate.py
python evaluation/manuscript-review/v7.2.3/issue93-export-contract/export_candidate.py
python evaluation/manuscript-review/v7.2.3/issue93-relational-use/verify_use.py
```

The final command recreates only its own ignored synthetic `generated/` outputs: a SQLite file, controlled dump, four information graphs, three use graphs, a TriG dataset and selected query answers. Older receipt files are not rewritten. Public code and the report are source-bound; generated bytes are separately retained as execution artifacts.

## Remaining boundary

**P3 is next:** generate the full candidate dictionary and structural bindings, reconcile readers/diagrams, and execute a candidate CI route before assessing promotion. Issue #93 remains open. No pharmaceutical backfill, production deployment, PostgreSQL result, independent semantic validation, new GitHub Actions success or public release is claimed. Manuscript 7.2.21 and main remain unchanged. Dataset #71, deployment #36, broader mapping #12/#35 and RiskCase #92 retain their separate scope.
