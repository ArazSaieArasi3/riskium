# Executable brief: ontology-to-database assurance

Owner request: 24 October 2026. Execution: #29 under #12. This brief organizes the questions, decisions, artifacts, checks and residual uncertainties before publication of any broader database claim.

## Improved implementation prompt

Treat the accepted ontology, original ORSD and competency questions as semantic authorities. Build an independently versioned database requirements specification and a bounded relational implementation. Reuse the ontology requirements by explicit derivation; add database-specific integrity, lifecycle, migration, recovery, performance, concurrency, security, usability and deployment requirements. Preserve original requirement priorities and historical evaluation outcomes.

Before running the implementation, freeze the task scope, engine/configuration, exact source versions, identity/inheritance/missingness/time/calculation policies, fixed valid/invalid/incomplete/mutation fixtures, independent expected answer vectors and deterministic generated inputs. Explain every semantic-to-physical mapping: classes, identity, subtypes, properties, directions, cardinalities, constraints, vocabulary, versions, source qualifiers and unimplemented semantics. Do not require one table per class or treat an opaque JSON column as complete mapping.

Execute an additive populated migration to a new assessment/result profile without editing the accepted base schema. Make interpretation metadata version-owned and immutable at issue. Distinguish raw preservation, managed records and task readiness; keep missing distinct from lexical zero, supplied values distinct from justified computations, and statements distinct from actual cases/occurrences. Keep named historical RDF interpretation graphs separate.

Run actual SQL tests with exact failure causes, atomic rollback, key/type/reference controls, duplicate-label identities, multi-value qualifiers, historical retrieval, source trace, serialization, backup/restore and bounded concurrent connections. Compare selected SQL answers and RDF facts with explicit expected facts and SHACL task eligibility. Use seeded synthetic and metamorphic tests independently of a real case study. Never use generated data or an LLM's expected answers as independent domain truth.

Audit every actual table and column, key, FK, check, trigger, index, purpose and authored functional-dependency decision. Flag unexplained key-only/one-column tables, but allow a justified subtype or membership relation. Document deliberate constrained redundancy and do not infer a proved normal form or usefulness from counts. Provide executable task queries, measure representative synthetic workloads and plans, and disclose that actual user/deployment SLOs and acceptance remain separately pending.

Maintain machine-checkable bidirectional links between ORSD/CQs, database requirements, mapping decisions, schema/dictionary/queries, fixture/oracle, actual results and component manifests. Reject stale hashes, missing evidence, orphan requirements, missing negative cases and undeclared exclusions. Report exact supported counts and unimplemented source elements, all retained/future requirement statuses, method/runtime/population and limits. Update repository documentation, the OntoSPK-style documentation surface, roadmap, issue evidence and CI. Close only the bounded completed task; retain broader original mapping, private migration, PostgreSQL, scientific and deployment obligations. Do not change the published v0.3.1 or manufacture owner/independent judgments.

## Organized questions and current defaults

| Question | Decision for this execution | Evidence or remaining input |
| --- | --- | --- |
| When is mapping checked? | Before DDL, after actual SQL implementation, during populated migration, on every relevant change and before release | Source mapping, exact fixtures, migration receipts and CI |
| Which requirements are reused? | Preserve all original semantic IDs/priorities; derive named DB requirements and disclose unmapped tasks | DRSD and original ORSD/CQ crosswalk |
| What new requirements are needed? | Integrity, transaction/recovery, physical design, queries/workload, concurrency, configuration, artifact lifecycle and deployment requirements | 28 DBR rows; 24 retained engineering checks, four explicit future obligations |
| What is the mapping unit? | An element or subclause with source hash, storage/derivation/external/unimplemented disposition | Full 306-element inventory, not a table-count proxy |
| How is inheritance mapped? | Existing artifact identity plus explicit concrete membership and version-owned facts | Reviewed type strategy, PK/FK/guard and RDF expectations |
| What about one-column tables? | Review purpose, identity, FD, FK, consumer and cost; a justified subtype membership can be valid | Actual design audit and an executable explained/unexplained-table control |
| What is unknown? | Preserve source JSON and SQL NULL; no zero/default or fabricated identity | Fixed missing-data and generated lexical-value controls |
| Can generated data test design? | Yes for declared engineering properties, edge cases, metamorphic invariants and workloads | Frozen seeded inputs and exact oracles; no real-case/clinical/domain accuracy claim |
| How are corrections/history handled? | Preserve issued versions and artifact-version grouping; retain base entry-revision lineage | Generic assessment correction/supersession links remain unimplemented; do not claim full CQ07 |
| How is source provenance checked? | Exact source FK, locator, origin and owner-specific joins, with source-isolation controls | Existence/consistency is not independent source truth |
| How is usefulness tested? | Runnable version/history/trace/comparison tasks with exact expected answers | Real user task success and deployment acceptance remain DBR-28 |
| What engine is being accepted? | SQLite >=3.38 as an offline/public research profile; report actual versions | PostgreSQL is DBR-25, not inferred from SQLite passes |
| What load is representative? | Engineering probe: 1,000 generated assessment/result pairs, four query patterns, five warmups and 31 timings | Actual concurrency, data size, deployment hardware and latency SLOs are not yet approved |
| How are failures treated? | Exact error and rollback required; engine errors never become domain rejection or mutant detection | Fixed case vectors and explicit before/after logical state digests |
| What additional questions need future answers? | Deployment engine, real user roles/permissions, private-data scope, workload/latency targets, backup RPO/RTO and user acceptance tasks | Defaults above allow current offline engineering work; they do not appoint users or approve production use |

## Acceptance and reporting rules

The bounded profile can be engineering-complete while full scientific/application adequacy remains open. Count schema objects as inventory; mapping support as source-element disposition; fixed tests by scenario kind; generated inputs by seed and property; performance by workload/runtime; and user/independent reviews only from actual people. Do not average an unresolved critical retained-scope defect into a green score. No overall correctness or readiness percentage is assigned.

The version chain is model 0.3.1 / original ORSD 0.4.3 -> database requirements 0.1.0 -> relational profile 0.2.0 / migration 3 -> bound fixtures, dictionary, query examples, trace and executed receipt. The original public SQL profile 0.1.0 and private historical database remain separate. Original manuscript 7.0.8 makes no new claim merely because this development task completes.
