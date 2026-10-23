# Riskium v0.3.1-rc.5 development prerelease

## Goal and delivered behavior

Deliver the first current public **relational identity and issued-history slice**, profile **0.1.0**, mapped to unchanged conceptual model **0.3.1**. Distinct cases retain their keys despite equal labels; entries keep typed case/register references; issuing a revision atomically snapshots content, provenance and version dependencies. Issued snapshots and owned dependencies resist update, delete and replacement. New revisions retain the earlier history and pinned versions; predecessors must be issued revisions of the same entry, without cycles.

[Scope, dictionary and clause dispositions](https://github.com/ArazSaieArasi3/riskium/blob/v0.3.1-rc.5/evaluation/relational/history/README.md), [exact mapping](https://github.com/ArazSaieArasi3/riskium/blob/v0.3.1-rc.5/implementation/relational/0.1.0/mapping.json) and [executed report](https://github.com/ArazSaieArasi3/riskium/blob/v0.3.1-rc.5/evaluation/relational/history/report.md) distinguish native concepts/relations from supplementary storage metadata. SQL tables, generated guards/views, public synthetic fixtures, migration/issue/restore helpers and complete compressed evidence are included. #24 owns this packet; broader #12 remains open.

## Executed evidence

- **67 scenario expectations matched**: 9 populated migration/audit cases, 2 required-configuration preflights, 48 actual operations, 4 guard-deletion controls and 4 round trips. These categories are disjoint. Controls demonstrate sensitivity and are not accepted risk cases.
- Actual **SQLite 3.53.1** local execution, foreign_keys=ON and recursive_triggers=ON. Hosted replay records its actual supported runtime. Schema 1 is populated before transactional schema-2 migration; existing rows and IDs survive. Invalid legacy cycles/references/content and drift are rejected with exact errors and unchanged row/schema/ledger state.
- File close/reopen, SQL dump/restore, SQLite backup and selected RDF fact serialization/reparse match fixed expected history/identity/edge vectors. Failed issue rolls back the entire operation, including allocated IDs, while retaining the draft. `REPLACE`, late dependency mutation, cross-entry lineage and 17-node ancestry are covered.
- **122 software regressions** passed locally. The candidate workflow runs **14 gates**, including the full fresh SQL replay, earlier C-08 and C-13/C-18 SHACL replays, synthetic CQ/source/trace/documentation checks and regressions. Actual hosted receipt establishes their publication-time outcomes.
- The SQL receipt was regenerated from committed implementation `11ffed4f4e74a61909c92395201b9abe29798f44`; all 10 exact input hashes were checked against that commit. Receipt publication is a subsequent commit. Logical/schema/oracle comparisons across supported engines do not claim byte-identical SQLite files.

## Claim boundaries

C-03 issued-history and C-24 lineage receive current scoped SQL evidence. C-01 supplies selected typed identity joins. C-25 receives **application target-coherence only**: these are version-owned supplementary bindings, not native assessment usesVersion assertions or complete C-25 subject/required-role admission. Serialized payload is supplementary, not a fabricated InformationContent instance or full RX-007 encoding. Only sealed rows export native ArtifactVersion/EntryRevision facts. DDL/PRAGMA disabling lies outside the supported configured-connection contract.

The historical private 128-table companion was inspected read-only and has a different embedded source hash. It is neither copied, migrated nor relabeled by this new profile. Its old 859 checks were not rerun. No private data/binary enters these public synthetic assets. No PostgreSQL, full-schema migration, scoring formula, temporal-interval, workload/concurrency, production readiness or full ontology equivalence is claimed.

Native source, OWL axioms, manuscript 7.0.7, historical HermiT/SHACL receipts and denominators remain unchanged. No HermiT NOT_RUN is turned into HermiT PASS. Earlier scoped profiles remain bounded; no universal scientific-acceptance claim is added.

## Review, next packet and publication

Owner-led review with assistant support remains #7: the prepared 11-row register still contains **zero owner ratings**. Independent review remains future nonblocking #23. The [final-release gates](https://github.com/ArazSaieArasi3/riskium/blob/v0.3.1-rc.5/docs/stable-release-gates.md) still require actual owner judgments, explicit disposition of retained technical/source claims, resolution of critical in-scope defects and a final clean freeze.

Next is [rc.6 source-backed CQ06 provenance](https://github.com/ArazSaieArasi3/riskium/blob/v0.3.1-rc.5/docs/next-release-v0.3.1-rc.6.md) under #13. Independently specified expected answers do not imply an independent reviewer. CQ07/08, the withheld 11 admissions, formal/integration residuals and final claim matrix require their own explicit dispositions. Parent #12 may remain open for unclaimed later work.

Five immutable assets: exact tracked source archive, source-manifest.json, candidate-receipt.json, release-notes.md and SHA256SUMS.txt. A release request is not publication evidence; successful hosted jobs, live Release/tag and independent downloaded-asset readback establish publication. This is a development prerelease, not the final v0.3.1. Prior rc tags/assets are preserved.
