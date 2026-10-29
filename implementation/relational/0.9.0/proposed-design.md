# Proposed storage, query and evidence boundaries

This is the implementation contract for #65, declared under #64 before runtime code. A final schema dictionary must explain the implemented SQL, every field/key/index and its actual consumers. The structure below bounds the task while allowing reviewed physical details to be chosen during implementation. Changes to acceptance meanings or literal outcomes require a separate reviewed amendment; never edit a failed expectation to match runtime output.

## Native derivation and scope choice

| Route | Existing model 0.3.1 meaning | Version ownership in this task |
| --- | --- | --- |
| G-07, C005 → C014 | Documentary assertion identity | One governed assertion artifact; distinct issued C015 versions through RX-006 |
| R-41, C005 → X01, exactly 1 | natureOf one RiskCase | Required case ID owned by assertion version; same case within the scoped artifact's version/correction family |
| R-42, C005 → C006, exactly 1 | declaresNature one NatureTerm | Exact issued term version plus its scheme-version dependency |
| G2-050/G2-053/G2-052 | NatureTerm → ClassificationTerm → VocabularyConcept → InformationArtifact | Explicit inherited typing; no labels as identities or classes |
| R-05, C019 → C018, exactly 1 | belongsToScheme | Term version owns an exact issued scheme version; stable scheme ID/code are the local governed term key |
| R-43, C005 → C002, 0..1 | natureInContext | Nullable exact issued context version; absence preserved explicitly |
| RK2-011, C002 → X02, 0..* | referencesObjective | Objective version list belongs to the pinned context version; no direct assertion/objective predicate |
| R-44, C023 → C005; inverse minimum 1 | recordsNature | One or more new recording entry revisions own exact assertion-version bindings before they issue |
| GX-049/GX-061/GX-047/G-19 | Scheme/objective/context artifact identity and entry-version identity | Supporting typed identities retain their exact native generalization paths |

All these routes currently have deferred or previously bounded mappings. Their declaration does not promote historical accounting rows. Support for a scheme/term/objective/context in this task is a selected documentary projection; taxonomy hierarchy, cross-scheme equivalence, objective governance and whole-model mapping remain outside its acceptance.

The current model supports this packet without a native revision. Full assertion management and automatic truth selection would require additional task and policy decisions, so they are excluded. RKRS-02/03/06/08/11/12 supply the derived task routes. Original RQ-CQ06 and RQ-CQ07 retain their original provenance/correction meanings. The no-fabrication principle of RQ-CQ08 is reused for raw nature content; this does not execute its original scenario population.

## Proposed relations and functional dependencies

Use additive typed membership over existing `information_artifact(kind=C014)` for C005, C006, C018 and X02; preserve `kind=C002` for context and the existing entry/register/version machinery. Prevent incompatible reuse of old profile members or late subtype additions to issued identities. No old kind discriminator, table, migration or issued row may be reinterpreted.

| Proposed storage role | Fields and functional dependency | Required behavior |
| --- | --- | --- |
| Nature membership | artifact ID → essential selected native class; term key additionally binds stable scheme artifact and code | Identity belongs to the governed caller namespace, with the existing case/artifact/version family registry. No label-based keys; term code is stable within its scheme. |
| Support snapshot | version ID → artifact ID, narrative, original source ID, locator, interpretation origin, recorded UTC; term snapshots also retain code and exact scheme version | Supports the finite scheme/term/objective subset. Payload and typed rows agree exactly; existing versions cannot receive these memberships retroactively. |
| Context-objective snapshot | context version ID and objective version ID form a unique binding; context version owns the full sorted list and documentary qualifiers | Targets issued X02 versions; no duplicate or wrong-type pins, and at most one version per objective artifact in a given context version. Empty is allowed as an incomplete task input. This supports new context versions only; no backfilling onto issued contexts. |
| Nature snapshot | version ID → artifact ID, case ID, exact term version, nullable context version, narrative, original source ID, locator, interpretation origin, recorded UTC | One case and one term; 0..1 context. All referenced direct identities, when supplied, must agree with versionOf. No latest joins. |
| Entry/nature binding | recording entry version ID plus assertion version ID is unique; entry payload owns its sorted exact target list | Recording entry belongs to the same case, with issued predecessor of the same entry when present. Collect all recorders at assertion issuance; no late insert/update/delete/replace on either sealed side. |
| Nature correction | corrected version ID → one prior version, actor, reason, source ID, locator, interpretation origin, recorded UTC | Exact issued C005 versions of the same artifact and case; branches allowed, no self/cycle. Endpoint sources remain separate from declaration provenance. |

The physical schema may split support rows or use a discriminated snapshot relation where a key/dependency review justifies it. The final dictionary must explain nullability, alternate keys, foreign keys, checks, views, guards, indexes and generated fields. Raw table counts or surrogate keys do not establish normalization or ontological adequacy.

Every issued semantic payload equals its normalized typed facts. Exclude only the initial display label from semantic snapshots; labels are presentation metadata with governed identity held separately. Source JSON is retained verbatim in the existing source record relation. The version source ID must agree with its owned semantic snapshot. No provenance, identity or timestamp may be filled from a fixture by runtime code.

## Issuance and immutability

1. Validate exact configured schema 9/10, trusted source hashes and old/new data before access. Canonical recorded UTC uses a real calendar, seconds and `Z`; dependency/predecessor instants cannot exceed the owning issue time.
2. Issue support versions in dependency order. A term pins its exact issued scheme version. A new context version captures its exact objective list before sealing. Identity and payload/source checks reject duplicate or incompatible memberships.
3. In one caller-safe transaction/savepoint, stage the new assertion version, all new recording entry revisions and their complete immutable bindings. Each recording revision's payload names the exact assertion version. Entry case and optional same-entry predecessor are checked.
4. Seal recording revisions after validating their staged targets, then seal the assertion after verifying its required issued recorders. During transaction-internal staging the target may still be unissued; no public reader returns a partial bundle. Final semantic audit rejects any committed incomplete managed bundle. SQL sealing guards and configured-reader health must agree on these boundaries.
5. If supplied, append the explicit correction declaration after both assertion endpoints are issued. Validate source/locator/origin/actor/reason, canonical time, same artifact/case and acyclic single-parent lineage. A later version without a declaration has no inferred correction edge.
6. Run complete integrity/semantic health before commit. On failure, roll back new identities, all version rows, recorders, typed bindings and the correction together. Inside a caller transaction retain the caller's prior changes and ability to roll back.

The fixture's two original recorders show that R-44 has a minimum of one rather than an arbitrary exactly-one constraint. Entry `previousRevision` preserves entry history through the original base machinery and does not establish assertion correction. A recording revision's own previousRevision is not recursively copied into the nature task graph. Its base native facts retain that lineage. Later attachment of another recording revision to an already-issued nature version is outside this finite immutable projection and must not alter its graph.

All new managed relations reject update/delete and duplicate IGNORE/REPLACE where those operations could hide or rewrite facts. Existing append-only source/catalog rules remain intact. Direct SQL within the supported connection is checked by guards; configured readers also re-audit schema, allocator, old semantic views and new payload/link coherence. Administrative DDL, disabling checks and possession of a modified file remain outside logical guard guarantees; their drift must be detected at health/restore boundaries.

## Query and RDF outcomes

The normative complete scalar row is in `query-oracles.json`. `get` additionally returns the exact source records keyed by role/ID, including each dependency source and any correction declaration. `by_case` returns every matching complete row. `family` follows only explicit correction edges from an explicit root and includes its complete rows and declarations. Known-empty cases differ from unknown IDs. Parameterized inputs and explicit version/root arguments are required. Ordering supports repeatable presentation and carries no priority or truth semantics.

Use named graph ID = exact assertion version ID. Native subjects for R-41/42/43 are assertion artifacts, and R-44 subjects are EntryRevision versions. Exact term/scheme/context/objective versions appear through RX-006 and their C015 type. Serialized JSON, recorded timestamps, source locators, readiness and correction declarations remain supplementary; no native predicate is invented for them.

The literal TriG file has eight graphs and 306 total quads, a separate population from the 306 native source elements. Each is a selected graph for its own issued interpretation. It does not assert complete admission or global functionality across a historical union. The declared SPARQL query must be executed with one explicit graph. Literal query outputs contain nine rows because A-v1 has two recording revisions. SQL/RDF normalization must compare full declared IDs/pins, including null context/objective fields. Compare actual native triples exactly, not just a count or isomorphism over a subset.

## Assurance and completion gates

| Evidence | Required actual outcome under #65/#66 |
| --- | --- |
| Populated migration | Start from the exact schema-9 loader/timeline in prior-population.json. Preserve every old table row, immutable payload, migration hash, allocator and old schema object; compare old native views before new writes. Repeat upgrade is idempotent; failed upgrade is atomic. |
| Later writes | Old assessment/evidence/knowledge named graphs remain identical. Existing base native facts remain a subset when genuinely new base identities/entry versions add facts. Preserve all seven earlier nature graphs after A-v4. |
| Invalid writes | Execute each declared negative variant through API and relevant raw SQL, including null/blank provenance, wrong types/owners/pins, late bindings and duplicate conflict algorithms. Compare complete pre/post logical state. |
| Recovery and transactions | Actual file backup, close/reopen, nested caller rollback, valid logical restore with separately retained trusted digest, edited-dump rejection and bounded two-connection visibility/conflict/retry. Capture engine/configuration and actual exceptions separately. |
| Workload | Fixed template-derived workloads, seeds 17/29 with 200/400 distinct reports round-robin across four cases. Record the generator and construction digest, answer counts, 5 warmups, 31 measured repetitions, median/p95 and plans/index rationale. Repeated reports are workload copies, not independent cases or semantic evidence. |
| Trace and sensitivity | Ten derived requirements and all 60 fixed controls join concrete input, query/oracle, actual observation and exact source. Missing/not-run/failure remain distinct. Demonstrate latest-pin, dropped-filter, inferred-lineage, union and guard mutants. Preserve original source-component inventories. |
| Current evidence | Independently download a hosted exact-source receipt and compare its digest/content. Record all runtime controls in separate evaluated files; leave this declaration's null observations unchanged. |
| Reader | Review six qualitative criteria and researcher/reviewer, domain and integrator paths. Explain the finite example, unknowns and correction/source boundaries in plain English. Source generation and actual Wiki/Pages delivery require separate evidence. |
| Publication | Reconcile all 306 native dispositions and manuscript boundaries using real outcomes. Select exact versioned components, freeze a full source archive plus five companion assets, then verify each public download, tag/Latest and every previous published inventory. |

All DBR-01..24 dispositions are explicit in the contract: 22 are affected and DBR-04/08 inherit unchanged assessment/score behavior. DBR-25..28 remain deferred. Declaration checks do not execute the 60 runtime controls or recertify inherited evidence. The manuscript remains 7.0.8 with no new element-specific claim until #66 reconciles the supported wording. The proposed distribution number alone conveys no release, organizational or conference acceptance.
