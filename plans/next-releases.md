# Riskium release roadmap after v0.3.9

Date: 10 November 2026. Planning source: main 3ce6f557. This is a scoped proposal, not a created tag, published release or evidence of implementation. The next selected planning target is v0.3.10; subsequent numbers are provisional until their source/component selection is qualified. Package, ontology, database and documentation versions remain independent.

## Goal of the next release

**v0.3.10 will deliver a source-qualified external-definition curation component for the current 0.3.2 ontology, preserving authored meanings and historical source evidence, and making the corresponding concept comparisons consistently available through repository, Wiki and Pages.**

Do not make a full database, complete pharmaceutical reconstruction, all semantic metrics or a commercial product prerequisites for this bounded release.

## Current execution checkpoint

N1 impact inventory and N2 changed/new documentary review are complete on the planning branch. [The N2 packet](../evaluation/releases/v0.3.9/followups/issue85-changed-review/README.md) records eight current-source dispositions with primary-source locators and separate modeling-foundation comparisons. It preserves scientific definitions, historical reviews and deployed reader bodies. Eight local negative integrity controls are rejected; these are not ontology-engine executions or independent expert ratings.

The next finite execution is N3a: confirm the 17 reuse candidates. Then recheck the 57 structural-context records in bounded subdomain batches, qualify the full 82-concept successor curation, and publish/read back the selected documentation package. #85 remains open until that last gate. v0.3.10 is a planning target; v0.3.9 remains the published package.

| Order / package target | Work and concrete endpoint | Issues and boundaries |
|---|---|---|
| v0.3.10 — current concept curation | N1 inventory and N2 review of six changed and two new records are complete. Confirm the 17 reuse candidates, recheck 57 structural-context records in bounded batches, qualify the complete curation component, publish and independently read back affected dossiers/navigation. Preserve historical source/receipts. | #85; #78 for exact normative dependencies. A source may be explicitly unassessed/deferred rather than forcing equivalence. Close #85 only after its own gate. |
| v0.4.0 — current-model database pilot | Predeclare one small analytical-case profile covering identity, context/objectives, optional register membership and selected evidence use. Implement the bounded SQLite mapping, profile ERD/data dictionary and positive/negative/incomplete task controls. Add a separately documented small ChatGPT-assisted synthetic sample, with fixed expected answers established before runtime output; distinguish generated from source-derived data. | A bounded child scope of #12/#35/#5. Existing engineering fixtures are not retrospectively called this generative pilot. Full ontology mapping and all parent issues need not close. |
| v0.5.0 — pharmaceutical source-to-database pilot | Select a small declared source-derived cohort (proposed starting size: five examples, not an observed count). Retain source locators, original statements, extracted context, rewritten records, identity decisions and target mappings. Load into the qualified current profile and test selected retrieval/SQL–SPARQL tasks. Document which ecosystem/enterprise perspective each example represents. | #71/#13/#72 and mapping #12/#35. Development data are distinct from an independently prepared evaluation population. Do not automatically reclassify the historical withheld cohort or demand full corpus completion. |
| v0.6.0 — evidence and evaluation consolidation | Review a declared portion of the repaired current ontology with actual specialists and independent task cases. Resolve selected remaining logical/data obligations. Decide whether executable semantic modules are appropriate; calculate semantic COH/COP only if modules, dependency rules and oracles are declared. | #23/#4/#5/#77; #78 exact crosswalks where justified. Review findings and residual limits are outcomes, not failure to achieve a fabricated correctness percentage. Optional modularity is not a gate if no modularity claim is made. |
| v1.0.0 — bounded stable research implementation | Freeze the supported ontology/profile/task scope, reproducible installation, documented ERDs and source-to-data provenance. Qualify SQLite and a real PostgreSQL implementation for that declared scope, including migrations, backup/restore and selected query parity. Publish coherent artifacts, current guides and repeatable acceptance evidence. | #36 plus remaining accepted #12/#35 scope; #74 maintains article/venue and artifact-role consistency. Production workloads, private migration and organization-wide effectiveness require their own target/evidence and are not implied by a stable research release. |
| Later service/product track — version unallocated | Define the product brief and one service boundary/API/interoperability prototype, then task/user evaluation. A possible journal paper may report the resulting evidence and architecture. Allocate a package version after acceptance scope is agreed. | #73/#72/#23; separate from commercial readiness. An entire application and a second paper are not prerequisites for v1.0.0. |

## Finite execution order

1. N1 completed: 82-row source/curation impact inventory and three rejected source-integrity mutants.
2. N2: review six changed and two new records; keep exact source/edition/locator and the distinction among related terms, analogy, candidate alignment and equivalence.
3. N3: confirm the 74 remaining reuse/context dispositions and qualify the current curation component. Split this into small subdomain batches if needed.
4. N4: publish/read back the curation component and freeze/package v0.3.10 under its own source/component checks.
5. D1: declare the v0.4.0 relational pilot and its expected answers; then implement/test the declared scope and the distinct generative sample.

No future release is claimed done by this roadmap. A late optional source or larger dataset should become a declared deferral, not an unbounded release blocker. Parent issues close only against their complete criteria; release slices may finish while parents stay open.

## Database and pharmaceutical status at this checkpoint

SQLite is implemented for the historical research companion, including SQL component 0.9.0/schema 10. Separate source-bound synthetic identity/history and evidence-use slices have actually been exercised: the latter reports 21/21 sidecar tests, 17/17 SHACL expectations and three selected SQL/SPARQL query rows, with SQLite integrity ok and no foreign-key violations. These are retained execution receipts, not new tests run by this planning packet. No real PostgreSQL execution is established here.

The pharmaceutical risk corpus checkpoint records 30 journal articles plus one correction, 883 consolidated items, 1,011 source records and 1,695 reported values. These are archived source-population counts, not counts of operational risk cases or a freshly audited private database. Staging and selected source/scenario/evidence mappings exist; full reconstruction/backfill into the current 0.3.2 relational profile remains #71. The public repository does not redistribute the private corpus database or full-text PDFs. Without direct access to a newer private corpus, this checkpoint cannot independently certify its freshness/completeness. CM-PharmE ontology releases and its separate application demonstrations are not proof that this Riskium corpus migration is complete.

Relevant evidence: `evaluation/manuscript-review/v7.2.3/issue92-riskcase/README.md`, `evaluation/manuscript-review/v7.2.3/issue93-relational-use/verification-report.json`, `implementation/relational/0.9.0/README.runtime.md`, and `evaluation/releases/v0.3.9/channels.json`.
