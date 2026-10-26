# Current traceability and document consistency

This guide joins the existing source-bound ledgers for the audited public Riskium baseline. It contains **423 trace rows**: 28 original requirement/scope/CQ rows, 306 native elements, 65 historical manuscript claims, seven approved manuscript amendments, twelve retained release claims and five correction requirements. A row is an accounting route, not a successful scientific test.

[Full JSON table](../evaluation/consistency/traceability.json) · [CSV table](../evaluation/consistency/traceability.csv) · [Input inventory](../evaluation/consistency/inventory.json) · [Findings and resolutions](../evaluation/consistency/findings.json) · [Actual manuscript readback](../evaluation/consistency/manuscript-readback.json).

## Versions and evidence boundaries

The ontology remains 0.3.1, ORSD 0.4.3 and approved article 7.0.8. The latest published source distribution is v0.3.2. Later SQL correction 0.3.0/migration 4 and current Pages explanations are separately identified development artifacts; they have not replaced immutable source assets. Next publication #41 must select and freeze its exact component set.

Original HermiT outcomes remain 281 PASS / 14 NOT_RUN of 295 obligations. Historical SHACL outcomes remain 341 scoped PASS / one PARTIAL / 17 NOT_RUN of 359. Original CQ populations, three withdrawn article claims and zero independent ratings remain visible. Owner acceptance is bounded and does not complete original MUST requirements. Later correction, comparison and source receipts supplement rather than relabel those populations.

## How to follow a row

Start with a requirement or stable native identifier. The table records the source, linked model elements/constraints, selected implementation or explicit omission, original obligation/query/fixture IDs, actual receipts and outcomes, retained claim and limit, article location, reading routes, owner scope and current follow-up issues. The same row can have a passing structural check and an unimplemented application meaning. Article-wide inventory claims do not imply that every term has its own article paragraph.

The original [28-row ledger](../evaluation/traceability/README.md), [formal-method guide](formal-method.md), [SQL correction receipt](../evaluation/relational/correction/README.md) and [approved article receipt](../evaluation/manuscript-review/v7.0.8/README.md) retain their full source detail. The current table adds a common reading route without rewriting those checkpoints.

## Requirement and question routes

| ID | Purpose | Model elements | Constraints | Current bounded scope |
| --- | --- | ---: | --- | --- |
| RKRS-01 | Content scope | 10 | C-01, C-02 | scoped design and evidence |
| RKRS-02 | Case continuity | 10 | C-01, C-20 | scoped identity evidence |
| RKRS-03 | Document identity and history | 9 | C-03, C-24, C-25 | scoped sqlite history |
| RKRS-04 | Assessment context | 18 | C-04, C-13, C-18 | scoped comparison task |
| RKRS-05 | Reported and computed scores | 5 | C-21 | design only operational claim deferred |
| RKRS-06 | Source-qualified assertions | 9 | C-02, C-12, C-17 | scoped source backed supplements |
| RKRS-07 | Evidence-qualified responsibility | 12 | C-06, C-07, C-22 | scoped distinction only |
| RKRS-08 | Time and workflow | 13 | C-05, C-19 | design only operational claim deferred |
| RKRS-09 | External boundaries and modes | 9 | C-14, C-15 | scoped mapping and bearer design |
| RKRS-10 | Policies and thresholds | 9 | C-08, C-10, C-11 | scoped declaration policy |
| RKRS-11 | Projection and admission | 8 | C-16, C-23, C-24, C-25 | scoped named tasks only |
| RKRS-12 | Quality evidence and reuse | 0 |  | scoped provenance synthesis |
| RKM-SCOPE-01 | Risk knowledge scope | 10 | C-01, C-02 | scoped design and evidence |
| RKM-SCOPE-02 | Case continuity | 27 | C-01, C-04, C-13, C-18, C-20 | scoped identity evidence |
| RKM-SCOPE-03 | Source-qualified policy statements | 9 | C-08, C-10, C-11 | source meaning limited |
| RKM-SCOPE-04 | Boundary-aware standards review | 0 |  | scoped inspected corpus |
| RKM-SCOPE-05 | Complete inventory disposition | 8 | C-16, C-23, C-24, C-25 | public id continuity only |
| RKM-SCOPE-06 | Temporal statement interpretation | 20 | C-03, C-05, C-19, C-24, C-25 | scoped history and temporal boundary |
| RKM-SCOPE-07 | Threshold interpretation | 9 | C-08, C-10, C-11 | scoped declaration policy |
| RKM-SCOPE-08 | Evidence-qualified responsibility | 12 | C-06, C-07, C-22 | scoped distinction only |
| RQ-CQ01 | Which entries document the same case? | 3 |  | scoped synthetic query |
| RQ-CQ02 | Which scenarios concern a case? | 3 |  | scoped synthetic query |
| RQ-CQ03 | Can equal scores use different scale versions? | 10 |  | scoped synthetic query |
| RQ-CQ04 | Can assignment information exist without an actual mandate? | 5 |  | scoped synthetic query |
| RQ-CQ05 | Does entry closure establish risk cessation? | 10 |  | scoped synthetic query |
| RQ-CQ06 | Can an assertion be traced to its source? | 5 |  | scoped source backed supplement |
| RQ-CQ07 | Does correction lineage remain distinguishable? | 3 |  | scoped source backed supplement |
| RQ-CQ08 | Can unsupported case identity remain unasserted? | 3 |  | scoped source backed supplement |

## Native and application coverage

All 306 source elements retain their exact identities and source hashes. The SQL register still records 250 incomplete core mappings and 11 external elements. Correction 0.3.0 adds application history for selected C-03/C-17 subclauses and no new native classes/predicates. All 25 constraint sections in the Formalization guide retain original engine outcomes, bounded claims and exclusions.

| Correction requirement | Original requirements | Constraints | Executed case links |
| --- | --- | --- | ---: |
| COR-01 | RKRS-03, RKRS-11 | C-03 | 5 |
| COR-02 | RKRS-03, RKRS-06 | C-03, C-17 | 10 |
| COR-03 | RKRS-04, RKRS-11 | C-04, C-17 | 7 |
| COR-04 | RKRS-06, RKRS-11 | C-02, C-12, C-17 | 7 |
| COR-05 | RKRS-11, RKRS-12 | C-03 | 7 |

## Manuscript reconciliation

The 65-row 7.0.7 claim baseline is retained with the seven approved 7.0.8 paragraph amendments and twelve bounded release claims. Fresh readback of both author-facing files matched their approved SHA-256 values; all seven amended DOCX paragraphs matched exactly. The unchanged PDF retains its earlier nine-page rendering QA; this audit does not claim a new render, article revision or independent review. New SQL/Pages capabilities are not silently added article claims.

## Publication and next release

The audit report records source/generated parity separately from actual Wiki/Pages publication. Historical readbacks stay dated. The completion record binds the final corrected source, deployed file bodies and fresh Wiki commit. After any further change, #41 must rerun affected checks before its final stable freeze and independently verify its new assets after publication. Broader source/scenario mapping, formal/application policies, source adequacy, independent review and deployment remain open in the [work plan](work-plan.md).

Run `python tools/audit_consistency.py --check` and the documentation builders to reject missing rows, stale hashes or changed historical denominators. This check executes no new HermiT/SHACL test and produces no ontology correctness percentage.
