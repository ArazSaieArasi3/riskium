# How Riskium's formal checks fit together

A well-formed ontology, a conforming record and a trustworthy risk assessment answer different questions. Riskium therefore keeps its conceptual commitments, OWL reasoning, explicit-data validation and application history separate. This page explains their connection and gives every interpretation constraint a route to its evidence and remaining work.

## Choose the question first

| Question | Language and input | What the check can establish |
| --- | --- | --- |
| What does the model mean? | Structured conceptual JSON and native OntoUML exchange | Source definitions, relation directions, multiplicities and interpretation constraints; exchange checks establish representation fidelity. |
| What follows from the bounded ontology? | OWL 2 axioms in Turtle, loaded as RDF/XML by HermiT | Consistency, class satisfiability and the declared entailment/countermodel probes for this mapping. |
| Is the required information explicitly present? | RDF data plus a named SHACL profile | Conformance of the selected graph and focus population under the stated identity and inference policy. |
| Can a selected assessment be compared or preserved? | Supplementary task metadata, SHACL profiles and SQLite schema/transactions | Declared compatibility/selection decisions and tested storage/history behavior within a named profile. |
| Does a source support the claim? | SPARQL answer contracts, source locators and human interpretation | Reproducible retrieval and provenance joins; truth, normative meaning and adequacy still require judgment. |

The conceptual catalog contains 80 concepts, 134 associations/bridges, 66 generalizations and 25 interpretation constraints. The bounded OWL export contains 77 typed local classes plus one local foundational proxy, 127 object properties and the 66 subclass links. Three optional boundary concepts and seven bridges are excluded. Stereotypes and abstractness annotations do not automatically acquire executable OWL semantics. The [reviewed mapping](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/owl-mapping-review.md) records the exact axiom choices, restrictions and exclusions.

## Read OWL results under its assumptions

OWL uses an open-world interpretation: a missing asserted link need not be false. If a Threshold must have an indicator or a scale, the ontology may satisfy that existential with an unnamed witness. That does not supply the named anchor an application needs. C-08 therefore has distinct OWL and explicit-data routes.

OWL also has no unique-name assumption. Two names need not denote two different individuals; a maximum-one restriction can sometimes be satisfied by identifying their referents. Explicit distinction or an independently justified identity policy is needed before treating two names as two witnesses. Domain and range infer types from a relation assertion; they are not database-style rejection rules for untyped input.

This export has no external `owl:imports`. Its closure is its own graph, and its foundational Object is an annotated local proxy. A non-entailment probe concerns the declared premise and conclusion: absence of an assertion alone is not proof of negation. The original HermiT receipt records 693 passing finite cases covering 281 of 295 baseline obligations; 14 remain NOT_RUN. This does not certify all possible interpretations or data.

## Validate explicit data under a named task

SHACL receipts identify the raw/effective data, shapes, focus selectors, engine, identity policy and expected result components. They use inference `none`; documented source taxonomy and normalization are supplied explicitly. OWL existential witnesses are not silently materialized. Source-end bounds count sources per target through an inverse path; target-end bounds count targets per source through a direct path.

Raw staging, CatalogInspection and selected task-ready profiles have different admission rules. Catalog metadata acceptance does not establish complete risk-assessment readiness. A negative fixture passes its test when the intended rule rejects it, rather than when an unrelated defect happens to fail validation. Preflight policy rejection and an actual SHACL execution are counted separately.

The historical 359-obligation ledger remains 341 scoped PASS, one PARTIAL and 17 NOT_RUN. Later compatibility profile 0.6.0 and comparison profile 0.7.0 add scoped alternatives without relabeling that ledger. For example, compatible declared metadata does not prove correct unit conversion, numerical evaluation or general dimensional adequacy. C-08 remains globally PARTIAL.

## Test changes over time in the application

A static graph cannot demonstrate that an issued payload survived an attempted update. The SQLite history profile 0.1.0 tests sealing, mutation rejection, revision lineage and populated migration. Assessment profile 0.2.0 adds selected pinned assessment/result snapshots, queries, migration and bounded backup/concurrency checks. Its 306-element mapping register is source accounting, not 306 successful semantic tests.

The assessment supplement covers selected subclauses of eleven constraints. It does not implement their complete original meanings. In particular, preserving a reported/computed distinction is not an arithmetic engine; storing a time token is not an interval or timezone policy. PostgreSQL, private migration and real workloads remain separate acceptance work.

The later [assessment-correction overlay 0.3.0](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/implementation/relational/0.3.0/README.md) adds migration 4 and an immutable application declaration between issued versions of one assessment identity. Its 36 fixed scenarios retain original values, source qualifiers and conflicting branches; three native graph comparisons show that no correction predicate was added to OWL. This does not implement general assertion/scenario correction or identify independent corroboration. Reproduce with `python tools/run_relational_correction.py --check` and `python tools/build_correction_inventory.py --check`. The original accepted-scope rows below remain unchanged.

## Reproduce without replacing historical evidence

Use a clean checkout of the desired source and record its commit first. Commands below run from the repository root. Create the appropriate environment from `tools/requirements-hermit.txt`, `tools/requirements-shacl.txt` or `tools/requirements-owl.txt`; documentation dependencies are in `tools/publication/requirements.txt`. The [reproduction guide](Reproduce) gives installation and the full module sequence.

| Route | Command | Expected and recorded evidence |
| --- | --- | --- |
| Conceptual/native allocation | `python tools/validate_model.py` and `python tools/review_coverage.py` | Source and planned-obligation consistency; not an engine result. |
| OWL representation | `python tools/build_owl.py --check` | Export matches reviewed sources; not a reasoner run. |
| HermiT | `.venv-hermit/bin/python tools/run_hermit.py` | Re-executes the bounded probes and writes a new receipt; original observed population is 693 cases, 281/295 obligations. |
| Original SHACL modules | Run builders/runners in the reproduction guide, then `python tools/summarize_shacl.py` | Re-executes declared graphs; original observed ledger is 341 PASS / 1 PARTIAL / 17 NOT_RUN. |
| C-08 compatibility | `.venv-shacl/bin/python tools/run_compatibility_shacl.py --check` | Fresh replay against stored oracles: 41 scenarios, including 37 engine executions and four preflight rejections. |
| C-13/C-18 comparison | `.venv-shacl/bin/python tools/run_comparison_shacl.py --check` | Fresh replay: 55 scenarios, including 50 engine executions and five preflight rejections. |
| SQL history | `python tools/run_relational_history.py --check` | Fresh finite history/migration replay checked against its saved receipt. |
| SQL assessment | `.venv-shacl/bin/python tools/run_relational_assessment.py --check` | 48 fixed cases, 100 frozen generated inputs, two SHACL comparisons and four generated workload patterns; runtime timing need not be identical. |
| Query and requirement traces | `.venv-shacl/bin/python tools/run_cq.py --check` and `.venv-shacl/bin/python tools/build_traceability.py --check` | Fixed answer/mutation and trace checks; independent-population and adequacy boundaries remain separate. |
| This reading register | `.venv-shacl/bin/python tools/build_formal_reference.py --check` | Verifies source bindings, all 25 rows and generated explanation parity; zero new scientific executions. |

Run receipt-writing commands in a disposable checkout or preserve the original files first. A new execution has its own source/runtime/serialization identity. Compare logical results, exact oracles and source hashes as specified by each runner; do not replace a dated receipt merely to make a current page look complete.

## Read the constraint register

Each row below retains the source statement, OWL encoding boundary, historical engine obligation IDs/outcomes, owner-accepted bounded claim and exclusions. Evidence links point to the actual source receipts; saved case IDs allow inspection of the original oracles. The later SQL assessment overlay is labeled separately. All 25 bounded dispositions were accepted by the author/owner for the first final release; this is not independent review or full original MUST fulfillment. The dated accepted-scope file's pending-freeze status was subsequently resolved by published v0.3.1; its original bytes are retained.

Use the [term search](https://arazsaiearasi3.github.io/riskium/current/reference/search.html) or [conceptual constraints](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#constraints) to locate the source vocabulary. [Evaluation](Evaluation) and the [work plan](Work-Plan) explain the wider evidence and remaining tasks. No complete first-order/TPTP verification package is claimed: adding one requires a separately reviewed translation, assumptions, source mappings, oracles and validation issue before implementation or acceptance claims.

| Constraint | Historical HermiT | Historical SHACL | Bounded disposition |
| --- | --- | --- | --- |
| [C-01 Risk Case is not ISO Risk](#C-01) | PASS | NOT_RUN | scoped evidence |
| [C-02 No realization from description](#C-02) | PASS | NOT_RUN | scoped evidence |
| [C-03 Issued version immutability](#C-03) | NOT_RUN | NOT_RUN | scoped alternative |
| [C-04 Assessment interpretation](#C-04) | NOT_RUN | NOT_RUN | scoped alternative |
| [C-05 Temporal and administrative distinction](#C-05) | NOT_RUN | NOT_RUN | design and finite controls |
| [C-06 Relator participant distinctness](#C-06) | PASS | PASS | scoped evidence |
| [C-07 Role-qualified ownership](#C-07) | PASS | NOT_RUN | design and finite controls |
| [C-08 Threshold anchor](#C-08) | PASS | PARTIAL | scoped alternative |
| [C-09 Description aboutness](#C-09) | NOT_RUN | PASS | scoped alternative |
| [C-10 Framework-qualified tolerance](#C-10) | NOT_RUN | NOT_RUN | design and finite controls |
| [C-11 Vocabulary resource identity](#C-11) | NOT_RUN | PASS | scoped alternative |
| [C-12 Evidence does not endorse](#C-12) | NOT_RUN | PASS | scoped alternative |
| [C-13 Scale and dimension compatibility](#C-13) | NOT_RUN | NOT_RUN | scoped alternative |
| [C-14 Heterogeneous boundaries](#C-14) | NOT_RUN | NOT_RUN | structural alternative |
| [C-15 Intrinsic vulnerability bearer](#C-15) | PASS | NOT_RUN | design and finite controls |
| [C-16 Admission profiles](#C-16) | NOT_RUN | NOT_RUN | scoped alternative |
| [C-17 Multiple assertions](#C-17) | NOT_RUN | NOT_RUN | scoped alternative |
| [C-18 Comparable assessments](#C-18) | NOT_RUN | NOT_RUN | scoped alternative |
| [C-19 Workflow semantics](#C-19) | NOT_RUN | NOT_RUN | executable claim deferred |
| [C-20 Risk Item vocabulary](#C-20) | PASS | NOT_RUN | design and finite controls |
| [C-21 Reported and computed scores](#C-21) | NOT_RUN | NOT_RUN | executable claim deferred |
| [C-22 Responsibility identity](#C-22) | PASS | NOT_RUN | design and finite controls |
| [C-23 Context relation coherence](#C-23) | PASS | PASS | scoped evidence |
| [C-24 Revision coherence](#C-24) | PASS | PASS | scoped evidence |
| [C-25 Version target coherence](#C-25) | PASS | PASS | scoped evidence |

<h2 id="C-01">C-01 — Risk Case is not ISO Risk</h2>

Case identity is preserved across descriptions, scores, owners and administrative states. Equal labels do not establish case identity.

**OWL encoding:** Separate Case, Entry, Scenario and Result classes; no label key

**OWL boundary:** Verify intended identity examples and non-entailment without assuming unique names.

**Historical outcomes:** HermiT `HERMIT-0605` **PASS**; SHACL `SHACL-0606` **NOT_RUN**.

**Accepted bounded claim:** Separate case, entry and revision keys; labels do not merge identities.

**Remaining/excluded:** Actual organizational case grounding and real reassessment continuity require attributable evidence; no automatic identity adjudication.

**Later SQL assessment overlay (0.2.0):** selected subclauses only; consult the [assessment method](Database-Assurance), [exact mapping](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/implementation/relational/0.2.0/mapping.json) and [executed receipt](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/relational/assessment/report.json.gz). This does not expand the earlier owner acceptance or change either historical engine outcome.

**Evidence:** [evaluation/cq/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/cq/report.json) · [evaluation/hermit/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/hermit/report.json) · [evaluation/relational/history/report.json.gz](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/relational/history/report.json.gz) · [ontology/riskium-model.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/riskium-model.json).

<details markdown="1"><summary>Original fixture identifiers and source route</summary>

**HermiT cases:** H-C-01-IDENTITY-COUNTERMODEL

**SHACL cases:** No executed case for this obligation.

[Conceptual clause](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#C-01) · [Native exchange](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/native/riskium.ontouml.json) · [OWL export](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/derived/riskium.owl.ttl)

</details>

<h2 id="C-02">C-02 — No realization from description</h2>

A scenario, consequence statement, signal, plan or report alone must not create actual occurrences, outcomes, controls or effectiveness assertions.

**OWL encoding:** No description-to-occurrence realization property chain

**OWL boundary:** Verify prohibited inferences; source statements alone cannot certify absence in an open world.

**Historical outcomes:** HermiT `HERMIT-0607` **PASS**; SHACL `SHACL-0608` **NOT_RUN**.

**Accepted bounded claim:** Documentary scenarios/source statements do not automatically assert actual occurrence or effect.

**Remaining/excluded:** No claim that every external inference/application obeys the boundary or that a missing graph assertion proves nonoccurrence.

**Evidence:** [evaluation/cq/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/cq/report.json) · [evaluation/hermit/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/hermit/report.json) · [evaluation/sources/cq0708/report.json.gz](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/sources/cq0708/report.json.gz) · [ontology/riskium-model.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/riskium-model.json).

<details markdown="1"><summary>Original fixture identifiers and source route</summary>

**HermiT cases:** H-C02-NO-REALIZATION

**SHACL cases:** No executed case for this obligation.

[Conceptual clause](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#C-02) · [Native exchange](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/native/riskium.ontouml.json) · [OWL export](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/derived/riskium.owl.ttl)

</details>

<h2 id="C-03">C-03 — Issued version immutability</h2>

Issued semantic content and effective dependency versions are immutable. Correction and supersession create lineage-preserving new versions.

**OWL encoding:** Version classes/links only; no immutable issued payload semantics

**OWL boundary:** Enforce immutable payloads and lineage in data governance/database.

**Historical outcomes:** HermiT `HERMIT-0609` **NOT_RUN**; SHACL `SHACL-0610` **NOT_RUN**.

**Accepted bounded claim:** Executed SQLite profile 0.1.0 preserves sealed payload, provenance and version-owned dependency snapshots, creates new revisions and rejects specified mutations.

**Remaining/excluded:** No general native InformationContent/RX-007 admission, PostgreSQL/full private-schema migration or protection against administrative DDL/PRAGMA bypass.

**Later SQL assessment overlay (0.2.0):** selected subclauses only; consult the [assessment method](Database-Assurance), [exact mapping](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/implementation/relational/0.2.0/mapping.json) and [executed receipt](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/relational/assessment/report.json.gz). This does not expand the earlier owner acceptance or change either historical engine outcome.

**Evidence:** [evaluation/relational/history/report.json.gz](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/relational/history/report.json.gz) · [evaluation/sources/cq0708/report.json.gz](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/sources/cq0708/report.json.gz) · [ontology/riskium-model.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/riskium-model.json).

<details markdown="1"><summary>Original fixture identifiers and source route</summary>

**HermiT cases:** No executed case for this obligation.

**SHACL cases:** No executed case for this obligation.

[Conceptual clause](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#C-03) · [Native exchange](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/native/riskium.ontouml.json) · [OWL export](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/derived/riskium.owl.ttl)

</details>

<h2 id="C-04">C-04 — Assessment interpretation</h2>

Results retain method/scale version, dimension, basis, relevant context and time semantics. A score is not the risk, and estimated likelihood need not be numeric.

**OWL encoding:** Assessment classes, typed links and applicable end bounds

**OWL boundary:** Verify method, scale, dimension, basis, context and time joins in data rules.

**Historical outcomes:** HermiT `HERMIT-0611` **NOT_RUN**; SHACL `SHACL-0612` **NOT_RUN**.

**Accepted bounded claim:** Selected comparison records require pinned interpretation metadata and matching declared context; equal score labels/numbers cannot authorize that named task.

**Remaining/excluded:** Not universal assessment readiness, full temporal semantics, all qualitative likelihood interpretations or reproduced version-specific method payload permissions.

**Later SQL assessment overlay (0.2.0):** selected subclauses only; consult the [assessment method](Database-Assurance), [exact mapping](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/implementation/relational/0.2.0/mapping.json) and [executed receipt](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/relational/assessment/report.json.gz). This does not expand the earlier owner acceptance or change either historical engine outcome.

**Evidence:** [evaluation/cq/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/cq/report.json) · [evaluation/shacl/comparison/report.json.gz](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/shacl/comparison/report.json.gz) · [ontology/riskium-model.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/riskium-model.json).

<details markdown="1"><summary>Original fixture identifiers and source route</summary>

**HermiT cases:** No executed case for this obligation.

**SHACL cases:** No executed case for this obligation.

[Conceptual clause](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#C-04) · [Native exchange](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/native/riskium.ontouml.json) · [OWL export](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/derived/riskium.owl.ttl)

</details>

<h2 id="C-05">C-05 — Temporal and administrative distinction</h2>

Recorded time, reference time and validity intervals are distinct. Workflow closure does not prove risk cessation or successful treatment.

**OWL encoding:** Distinct class/link vocabulary only

**OWL boundary:** Temporal interval and administrative-state rules require explicit data validation.

**Historical outcomes:** HermiT `HERMIT-0613` **NOT_RUN**; SHACL `SHACL-0614` **NOT_RUN**.

**Accepted bounded claim:** Recorded/reference/validity time and administrative versus real-world status remain distinct design commitments; synthetic retrieval illustrates closure versus cessation.

**Remaining/excluded:** Interval ordering, timezone/unknown-endpoint policy, actual cessation and treatment-effectiveness adjudication or workflow execution are not implemented/accepted claims.

**Later SQL assessment overlay (0.2.0):** selected subclauses only; consult the [assessment method](Database-Assurance), [exact mapping](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/implementation/relational/0.2.0/mapping.json) and [executed receipt](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/relational/assessment/report.json.gz). This does not expand the earlier owner acceptance or change either historical engine outcome.

**Evidence:** [evaluation/cq/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/cq/report.json) · [ontology/riskium-model.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/riskium-model.json).

<details markdown="1"><summary>Original fixture identifiers and source route</summary>

**HermiT cases:** No executed case for this obligation.

**SHACL cases:** No executed case for this obligation.

[Conceptual clause](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#C-05) · [Native exchange](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/native/riskium.ontouml.json) · [OWL export](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/derived/riskium.owl.ttl)

</details>

<h2 id="C-06">C-06 — Relator participant distinctness</h2>

An asserted ResponsibilityRelator requires at least two distinct mediated individuals. If bearer and authority resolve to one actor and no further grounding exists, retain ResponsibilityAssignmentInformation without asserting the relator.

**OWL encoding:** Local end bounds and same-pair property disjointness for the two mediation roles

**OWL boundary:** Explicit distinct participants, identity resolution and assignment grounding still need an admission/profile check.

**Historical outcomes:** HermiT `HERMIT-0615` **PASS**; SHACL `SHACL-0616` **PASS**.

**Accepted bounded claim:** Bounded OWL and explicit-data tests enforce declared participant distinctness and retain assignment information when no relator can be grounded.

**Remaining/excluded:** Explicit identity evidence is required; different names alone do not prove different individuals or actual mandate truth.

**Evidence:** [evaluation/hermit/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/hermit/report.json) · [evaluation/shacl/coverage-status.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/shacl/coverage-status.json) · [evaluation/shacl/endpoints/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/shacl/endpoints/report.json) · [evaluation/shacl/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/shacl/report.json) · [ontology/riskium-model.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/riskium-model.json).

<details markdown="1"><summary>Original fixture identifiers and source route</summary>

**HermiT cases:** H-C06-DISTINCT-PARTICIPANTS, H-C06-SAME-PARTICIPANT

**SHACL cases:** S-C06-DISTINCT, S-C06-SUBTYPE-BEARER, S-C06-WRONG-BEARER-TYPE, S-C06-WRONG-AUTHORITY-TYPE, S-C06-REVERSE-DIFFERENCE, S-C06-UNRESOLVED-NAMES, S-C06-SAME-ACTOR, S-C06-ALIASED-SAME-ACTOR, S-C06-ALIAS-CHAIN, S-C06-IDENTITY-CONFLICT, S-C06-RAW-IDENTITY-CONFLICT, S-C06-MISSING-BEARER, S-C06-MISSING-AUTHORITY, S-C06-EXCESS-BEARER, S-C06-EXCESS-AUTHORITY, S-C06-INFORMATION-ONLY, S-C06-RAW-INCOMPLETE, S-C06-MANAGED-INCOMPLETE

[Conceptual clause](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#C-06) · [Native exchange](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/native/riskium.ontouml.json) · [OWL export](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/derived/riskium.owl.ttl)

</details>

<h2 id="C-07">C-07 — Role-qualified ownership</h2>

ResponsibleAgentRole does not automatically mean Risk Owner. Ownership mapping requires recorded responsibility type, accountability, authority and applicable context.

**OWL encoding:** Responsible/authorizing roles stay separate; no automatic owner equivalence

**OWL boundary:** Ownership interpretation depends on mandate, scope and evidence review.

**Historical outcomes:** HermiT `HERMIT-0617` **PASS**; SHACL `SHACL-0618` **NOT_RUN**.

**Accepted bounded claim:** A responsibility role/assignment record is not automatically an actual mandate or Risk Owner.

**Remaining/excluded:** Automatic source-to-owner mapping with validated accountability/authority/scope is deferred; no automatic Risk Owner population.

**Evidence:** [evaluation/cq/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/cq/report.json) · [ontology/riskium-model.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/riskium-model.json).

<details markdown="1"><summary>Original fixture identifiers and source route</summary>

**HermiT cases:** H-C07-NO-AUTHORITY

**SHACL cases:** No executed case for this obligation.

[Conceptual clause](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#C-07) · [Native exchange](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/native/riskium.ontouml.json) · [OWL export](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/derived/riskium.owl.ttl)

</details>

<h2 id="C-08">C-08 — Threshold anchor</h2>

At least one of thresholdForIndicator or thresholdOnScale is present. If both are present, their scale/unit interpretation is compatible. Qualitative boundaries use scale semantics rather than invented numeric units.

**OWL encoding:** Threshold anchor union plus individual end bounds

**OWL boundary:** A named anchor and cross-field unit/scale compatibility require explicit-data validation.

**Historical outcomes:** HermiT `HERMIT-0619` **PASS**; SHACL `SHACL-0620` **PARTIAL**.

**Accepted bounded claim:** Profile 0.6.0 checks declared numeric/qualitative metadata compatibility for its caller-selected dual-anchor threshold task.

**Remaining/excluded:** Global C-08 remains PARTIAL; no unit conversion, broad dimensional adequacy, numeric evaluation or full risk-record admission.

**Evidence:** [evaluation/shacl/compatibility/report.json.gz](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/shacl/compatibility/report.json.gz) · [evaluation/shacl/coverage-status.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/shacl/coverage-status.json) · [evaluation/shacl/endpoints/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/shacl/endpoints/report.json) · [evaluation/shacl/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/shacl/report.json) · [ontology/riskium-model.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/riskium-model.json).

<details markdown="1"><summary>Original fixture identifiers and source route</summary>

**HermiT cases:** H-C08-ANCHOR-UNION, H-C08-REMOVED-UNION, H-C08-SCALE-ONLY, H-C08-ANONYMOUS-ANCHOR, H-C08-DUAL-ANCHOR, H-C08-NO-FABRICATED-INDICATOR

**SHACL cases:** S-C08-INDICATOR-ONLY, S-C08-SCALE-ONLY, S-C08-DUAL-STRUCTURAL, S-C08-NO-ANCHOR, S-C08-RAW-NO-ANCHOR, S-C08-WRONG-INDICATOR-TYPE, S-C08-WRONG-SCALE-TYPE, S-C08-TWO-INDICATORS, S-C08-TWO-SCALES, S-C08-TASK-DUAL-UNKNOWN, S-C08-DELETED-ANCHOR-RULE

[Conceptual clause](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#C-08) · [Native exchange](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/native/riskium.ontouml.json) · [OWL export](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/derived/riskium.owl.ttl)

</details>

<h2 id="C-09">C-09 — Description aboutness</h2>

Every published RiskDescription has at least one case, pattern or scenario target. Multiple valid targets are permitted and require explicit interpretation.

**OWL encoding:** Aboutness links and individual end bounds; no global description existential

**OWL boundary:** A published-description profile needs an explicit publication focus and a validated aboutness alternative. Ordinary descriptions are not thereby rejected.

**Historical outcomes:** HermiT `HERMIT-0621` **NOT_RUN**; SHACL `SHACL-0622` **PASS**.

**Accepted bounded claim:** Published-description SHACL checks explicit case/pattern/scenario aboutness and permits multiple declared targets.

**Remaining/excluded:** Not HermiT discharge, target truth, occurrence evidence or a single universal target interpretation.

**Evidence:** [evaluation/shacl/coverage-status.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/shacl/coverage-status.json) · [evaluation/shacl/endpoints/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/shacl/endpoints/report.json) · [evaluation/shacl/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/shacl/report.json) · [ontology/riskium-model.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/riskium-model.json).

<details markdown="1"><summary>Original fixture identifiers and source route</summary>

**HermiT cases:** No executed case for this obligation.

**SHACL cases:** S-C09-CASE, S-C09-PATTERN, S-C09-WRONG-PATTERN-TYPE, S-C09-SCENARIO, S-C09-WRONG-SCENARIO-TYPE, S-C09-MULTIPLE-TARGETS, S-C09-PUBLISHED-NO-TARGET, S-C09-ORDINARY-NO-TARGET, S-C09-UNTYPED-PUBLISHED, S-C09-WRONG-TARGET-TYPE, S-C09-DELETED-MINIMUM

[Conceptual clause](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#C-09) · [Native exchange](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/native/riskium.ontouml.json) · [OWL export](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/derived/riskium.owl.ttl)

</details>

<h2 id="C-10">C-10 — Framework-qualified tolerance</h2>

Tolerance statements retain source framework/version, original meaning and context. Permissible deviation is not automatically equivalent to readiness to bear remaining risk.

**OWL encoding:** Source-qualified tolerance vocabulary retained

**OWL boundary:** Framework/version meaning and applicability are not a universal OWL equivalence.

**Historical outcomes:** HermiT `HERMIT-0623` **NOT_RUN**; SHACL `SHACL-0624` **NOT_RUN**.

**Accepted bounded claim:** Distinct source-qualified tolerance meanings are represented without global equivalence.

**Remaining/excluded:** Complete normative appetite/tolerance definitions and ISO/COBIT/Risk IT equivalence/crosswalk/compliance are unassessed and unclaimed.

**Evidence:** [evaluation/references/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/references/report.json) · [ontology/riskium-model.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/riskium-model.json) · [references/corpus.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/references/corpus.json).

<details markdown="1"><summary>Original fixture identifiers and source route</summary>

**HermiT cases:** No executed case for this obligation.

**SHACL cases:** No executed case for this obligation.

[Conceptual clause](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#C-10) · [Native exchange](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/native/riskium.ontouml.json) · [OWL export](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/derived/riskium.owl.ttl)

</details>

<h2 id="C-11">C-11 — Vocabulary resource identity</h2>

Vocabulary resources retain scheme-qualified identity. Labels are representations and are not OWL classes by default.

**OWL encoding:** Vocabulary resources are classes of resources, labels annotations

**OWL boundary:** Scheme-qualified identity and label governance require data checks.

**Historical outcomes:** HermiT `HERMIT-0625` **NOT_RUN**; SHACL `SHACL-0626` **PASS**.

**Accepted bounded claim:** Vocabulary metadata is keyed by scheme/edition/code; label equality does not create classes or cross-scheme identity.

**Remaining/excluded:** Metadata key validation is not universal ontological identity adjudication or a HermiT PASS for this clause.

**Evidence:** [evaluation/shacl/qualification/report.json.gz](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/shacl/qualification/report.json.gz) · [ontology/riskium-model.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/riskium-model.json).

<details markdown="1"><summary>Original fixture identifiers and source route</summary>

**HermiT cases:** No executed case for this obligation.

**SHACL cases:** VOC-RKM-C006, VOC-RKM-C017, VOC-RKM-C019, VOC-RKM-C027, VOC-RKM-C028, VOC-RKM-C029, VOC-RKM-C038, VOC-RKM-C039, VOC-RKM-C040, VOC-RKM-C042, VOC-RKM-C046, VOC-RKM-C059, VOC-RKM-C060, VOC-RKM-C061, VOC-RAW-INCOMPLETE, VOC-MISSING-SCHEME, VOC-MISSING-EDITION, VOC-MISSING-CODE, VOC-MISSING-LABEL, VOC-BLANK-CODE, VOC-SCHEME-MISMATCH, VOC-DELETED-AGREEMENT, VOC-DUPLICATE-KEY, VOC-DELETED-UNIQUENESS, VOC-OTHER-SCHEME, VOC-OTHER-EDITION, VOC-ASSERTED-ALIAS, VOC-WRONG-CANDIDATE, VOC-INTEGRATED

[Conceptual clause](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#C-11) · [Native exchange](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/native/riskium.ontouml.json) · [OWL export](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/derived/riskium.owl.ttl)

</details>

<h2 id="C-12">C-12 — Evidence does not endorse</h2>

EvidenceReference states an evidential role such as support, challenge or context. Linking a source does not automatically prove the target claim.

**OWL encoding:** Evidence links carry types, no endorsement implication

**OWL boundary:** Evidential role and truth/endorsement require interpretation.

**Historical outcomes:** HermiT `HERMIT-0627` **NOT_RUN**; SHACL `SHACL-0628` **PASS**.

**Accepted bounded claim:** Selected evidence records carry source/item/target and Support/Challenge/Context role; source-query provenance can be inspected.

**Remaining/excluded:** Conformance and source links do not establish truth, endorsement, evidential adequacy or independent corroboration.

**Evidence:** [evaluation/shacl/qualification/report.json.gz](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/shacl/qualification/report.json.gz) · [evaluation/sources/cq06/report.json.gz](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/sources/cq06/report.json.gz) · [evaluation/sources/cq0708/report.json.gz](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/sources/cq0708/report.json.gz) · [ontology/riskium-model.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/riskium-model.json).

<details markdown="1"><summary>Original fixture identifiers and source route</summary>

**HermiT cases:** No executed case for this obligation.

**SHACL cases:** EVIDENCE-SUPPORT, EVIDENCE-CHALLENGE, EVIDENCE-CONTEXT, EVIDENCE-RAW, EVIDENCE-MISSING-ROLE, EVIDENCE-MISSING-SOURCE, EVIDENCE-MISSING-ITEM, EVIDENCE-MISSING-TARGET, EVIDENCE-UNKNOWN-ROLE, EVIDENCE-LITERAL-SOURCE, EVIDENCE-MISSING-ITEM-PAIR, EVIDENCE-DELETED-ITEM-RULE, EVIDENCE-SUPPORT-WITHOUT-PAIR, EVIDENCE-DELETED-ROLE-RULE, EVIDENCE-CHALLENGE-WITH-SUPPORT-PAIR, EVIDENCE-OTHER-ITEM, EVIDENCE-OTHER-TARGET, EVIDENCE-INTEGRATED

[Conceptual clause](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#C-12) · [Native exchange](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/native/riskium.ontouml.json) · [OWL export](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/derived/riskium.owl.ttl)

</details>

<h2 id="C-13">C-13 — Scale and dimension compatibility</h2>

A selected level belongs to the selected scale version and dimension. Results on incompatible methods/scales are not ranked merely by equal labels or numeric codes.

**OWL encoding:** Scale/dimension classes and links

**OWL boundary:** Pinning, compatibility and numerical ordering require explicit data rules.

**Historical outcomes:** HermiT `HERMIT-0629` **NOT_RUN**; SHACL `SHACL-0630` **NOT_RUN**.

**Accepted bounded claim:** Profile 0.7.0 checks selected level/scale-version/dimension joins for the declared comparison task.

**Remaining/excluded:** No general level ordering, numeric-code ranking, unit transformation or proof of scale meaning.

**Later SQL assessment overlay (0.2.0):** selected subclauses only; consult the [assessment method](Database-Assurance), [exact mapping](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/implementation/relational/0.2.0/mapping.json) and [executed receipt](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/relational/assessment/report.json.gz). This does not expand the earlier owner acceptance or change either historical engine outcome.

**Evidence:** [evaluation/shacl/comparison/report.json.gz](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/shacl/comparison/report.json.gz) · [ontology/riskium-model.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/riskium-model.json).

<details markdown="1"><summary>Original fixture identifiers and source route</summary>

**HermiT cases:** No executed case for this obligation.

**SHACL cases:** No executed case for this obligation.

[Conceptual clause](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#C-13) · [Native exchange](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/native/riskium.ontouml.json) · [OWL export](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/derived/riskium.owl.ttl)

</details>

<h2 id="C-14">C-14 — Heterogeneous boundaries</h2>

RiskSource, Consequence and RiskControl remain catalog notions and optional external boundaries, excluded from native formal-core class assertions. Source, outcome and control content is represented by RiskSourceReference, ConsequenceStatement and ControlReference.

**OWL encoding:** Three optional boundaries and seven bridges excluded from class/property export

**OWL boundary:** External alignment requires a separately reviewed import or bridge.

**Historical outcomes:** HermiT `HERMIT-0631` **NOT_RUN**; SHACL `SHACL-0632` **NOT_RUN**.

**Accepted bounded claim:** Three optional heterogeneous boundaries and seven bridges are excluded from the typed core; documentary reference classes remain.

**Remaining/excluded:** Structural/boundary checks are not new HermiT runs or proof of external referent existence; external ontology import/mapping extension stays future work.

**Evidence:** [evaluation/c14-boundary-review.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/c14-boundary-review.json) · [evaluation/shacl/admission/report.json.gz](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/shacl/admission/report.json.gz) · [ontology/riskium-model.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/riskium-model.json).

<details markdown="1"><summary>Original fixture identifiers and source route</summary>

**HermiT cases:** No executed case for this obligation.

**SHACL cases:** No executed case for this obligation.

[Conceptual clause](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#C-14) · [Native exchange](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/native/riskium.ontouml.json) · [OWL export](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/derived/riskium.owl.ttl)

</details>

<h2 id="C-15">C-15 — Intrinsic vulnerability bearer</h2>

Every asserted intrinsic Vulnerability has exactly one substantial-endurant bearer. A reported hypothesis alone is information, not an actual mode.

**OWL encoding:** Characterization bearer relation has its reviewed exactly-one source-end restriction

**OWL boundary:** OWL can satisfy existence anonymously or merge named bearers; actual substantial bearer/admission needs separate evidence.

**Historical outcomes:** HermiT `HERMIT-0633` **PASS**; SHACL `SHACL-0634` **NOT_RUN**.

**Accepted bounded claim:** Bounded OWL bearer dependence/cardinality supports the intrinsic-vulnerability design; reports remain documentary information.

**Remaining/excluded:** Full explicit-data bearer admission and real-world substantial-bearer/vulnerability grounding remain unexecuted/unaccepted; no automatic mode from a hypothesis.

**Evidence:** [evaluation/hermit/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/hermit/report.json) · [ontology/riskium-model.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/riskium-model.json).

<details markdown="1"><summary>Original fixture identifiers and source route</summary>

**HermiT cases:** H-C15-TWO-DISTINCT-BEARERS

**SHACL cases:** No executed case for this obligation.

[Conceptual clause](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#C-15) · [Native exchange](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/native/riskium.ontouml.json) · [OWL export](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/derived/riskium.owl.ttl)

</details>

<h2 id="C-16">C-16 — Admission profiles</h2>

Raw source content is retained in staging. Managed records require identity, subject, title and provenance. Analytical readiness additionally requires the pinned context, method, scale, basis, dimension and time required for the selected task.

**OWL encoding:** Typed managed profile is documented

**OWL boundary:** Raw, managed and task-ready admission are SHACL/application profiles, not inferred from absent triples.

**Historical outcomes:** HermiT `HERMIT-0635` **NOT_RUN**; SHACL `SHACL-0636` **NOT_RUN**.

**Accepted bounded claim:** CatalogInspection metadata admission and separately named compatibility/comparison/source/history tasks have explicit staging and task boundaries.

**Remaining/excluded:** No general complete RiskAssessment readiness or arbitrary multi-relation/conditional integration; only named executed profiles may be called supported.

**Later SQL assessment overlay (0.2.0):** selected subclauses only; consult the [assessment method](Database-Assurance), [exact mapping](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/implementation/relational/0.2.0/mapping.json) and [executed receipt](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/relational/assessment/report.json.gz). This does not expand the earlier owner acceptance or change either historical engine outcome.

**Evidence:** [evaluation/relational/history/report.json.gz](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/relational/history/report.json.gz) · [evaluation/shacl/admission/report.json.gz](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/shacl/admission/report.json.gz) · [evaluation/shacl/comparison/report.json.gz](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/shacl/comparison/report.json.gz) · [evaluation/shacl/compatibility/report.json.gz](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/shacl/compatibility/report.json.gz) · [evaluation/sources/cq06/report.json.gz](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/sources/cq06/report.json.gz) · [evaluation/sources/cq0708/report.json.gz](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/sources/cq0708/report.json.gz) · [ontology/riskium-model.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/riskium-model.json).

<details markdown="1"><summary>Original fixture identifiers and source route</summary>

**HermiT cases:** No executed case for this obligation.

**SHACL cases:** No executed case for this obligation.

[Conceptual clause](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#C-16) · [Native exchange](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/native/riskium.ontouml.json) · [OWL export](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/derived/riskium.owl.ttl)

</details>

<h2 id="C-17">C-17 — Multiple assertions</h2>

Multiple classifications, descriptions, actors and evidence assertions are retained with role, context, provenance and time. Scalar export requires an explicit selection rule when several values apply.

**OWL encoding:** No scalar collapse or forced functional property beyond stated end bounds

**OWL boundary:** Assertion-level provenance, context and export selection remain data obligations.

**Historical outcomes:** HermiT `HERMIT-0637` **NOT_RUN**; SHACL `SHACL-0638` **NOT_RUN**.

**Accepted bounded claim:** Selected source-query/SQL fixtures retain conflicting assertions, original/reissued values and provenance without silently selecting or overwriting.

**Remaining/excluded:** A universal scalar-export selection policy across all contexts/times and complete multi-assertion admission is deferred.

**Later SQL assessment overlay (0.2.0):** selected subclauses only; consult the [assessment method](Database-Assurance), [exact mapping](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/implementation/relational/0.2.0/mapping.json) and [executed receipt](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/relational/assessment/report.json.gz). This does not expand the earlier owner acceptance or change either historical engine outcome.

**Evidence:** [evaluation/relational/history/report.json.gz](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/relational/history/report.json.gz) · [evaluation/sources/cq06/report.json.gz](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/sources/cq06/report.json.gz) · [evaluation/sources/cq0708/report.json.gz](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/sources/cq0708/report.json.gz) · [ontology/riskium-model.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/riskium-model.json).

<details markdown="1"><summary>Original fixture identifiers and source route</summary>

**HermiT cases:** No executed case for this obligation.

**SHACL cases:** No executed case for this obligation.

[Conceptual clause](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#C-17) · [Native exchange](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/native/riskium.ontouml.json) · [OWL export](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/derived/riskium.owl.ttl)

</details>

<h2 id="C-18">C-18 — Comparable assessments</h2>

Direct comparison requires matching pinned method, scale, dimension, basis and temporal context; a governed explicit transformation may enable a different comparison. Missing data is not zero. Reported scores do not imply a reproducible computation.

**OWL encoding:** Distinct pinned interpretation vocabulary

**OWL boundary:** Comparison and approved transformations need governed calculation rules.

**Historical outcomes:** HermiT `HERMIT-0639` **NOT_RUN**; SHACL `SHACL-0640` **NOT_RUN**.

**Accepted bounded claim:** Profile 0.7.0 checks strict eligibility for direct comparison of two selected pairs under declared pinned interpretation; missing data is not zero.

**Remaining/excluded:** Governed transformations, ranking/calculation, general temporal interpretation and universal assessment comparability are not claimed.

**Later SQL assessment overlay (0.2.0):** selected subclauses only; consult the [assessment method](Database-Assurance), [exact mapping](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/implementation/relational/0.2.0/mapping.json) and [executed receipt](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/relational/assessment/report.json.gz). This does not expand the earlier owner acceptance or change either historical engine outcome.

**Evidence:** [evaluation/cq/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/cq/report.json) · [evaluation/shacl/comparison/report.json.gz](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/shacl/comparison/report.json.gz) · [ontology/riskium-model.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/riskium-model.json).

<details markdown="1"><summary>Original fixture identifiers and source route</summary>

**HermiT cases:** No executed case for this obligation.

**SHACL cases:** No executed case for this obligation.

[Conceptual clause](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#C-18) · [Native exchange](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/native/riskium.ontouml.json) · [OWL export](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/derived/riskium.owl.ttl)

</details>

<h2 id="C-19">C-19 — Workflow semantics</h2>

State labels are scheme/version qualified. Transition rules and authority are source-backed content. Missing rule means UNKNOWN; Closed does not imply ceased risk and Treated does not imply effectiveness.

**OWL encoding:** Workflow labels and state classes remain source-qualified

**OWL boundary:** Transitions, authorization and UNKNOWN handling need data/application rules.

**Historical outcomes:** HermiT `HERMIT-0641` **NOT_RUN**; SHACL `SHACL-0642` **NOT_RUN**.

**Accepted bounded claim:** Workflow labels/rules/authority remain source-qualified design content; Closed/Treated alone cannot establish cessation/effectiveness.

**Remaining/excluded:** No executable transition authority engine, universal workflow scheme mapping or treatment-effectiveness acceptance is claimed.

**Evidence:** [evaluation/cq/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/cq/report.json) · [ontology/riskium-model.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/riskium-model.json).

<details markdown="1"><summary>Original fixture identifiers and source route</summary>

**HermiT cases:** No executed case for this obligation.

**SHACL cases:** No executed case for this obligation.

[Conceptual clause](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#C-19) · [Native exchange](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/native/riskium.ontouml.json) · [OWL export](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/derived/riskium.owl.ttl)

</details>

<h2 id="C-20">C-20 — Risk Item vocabulary</h2>

In the terminology adopted by this profile, Risk Item denotes the managed risk subject modeled as RiskCase. This context-qualified mapping does not equate RiskCase with RiskRegisterEntry, RiskScenarioSpecification, ISO risk or any global Risk Item class.

**OWL encoding:** Risk Item contextual synonym retained in requirements, no OWL equivalence

**OWL boundary:** Context-sensitive terminology needs human review.

**Historical outcomes:** HermiT `HERMIT-0643` **PASS**; SHACL `SHACL-0644` **NOT_RUN**.

**Accepted bounded claim:** Risk Item is a local terminology convention for the managed RiskCase subject, distinct from entry/scenario/ISO risk.

**Remaining/excluded:** No global Risk Item equivalence, automatic label-based import/class alignment or universal terminology standard.

**Evidence:** [evaluation/hermit/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/hermit/report.json) · [evaluation/relational/history/report.json.gz](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/relational/history/report.json.gz) · [ontology/riskium-model.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/riskium-model.json).

<details markdown="1"><summary>Original fixture identifiers and source route</summary>

**HermiT cases:** H-C20-NO-CASE-ENTRY-EQUIVALENCE

**SHACL cases:** No executed case for this obligation.

[Conceptual clause](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#C-20) · [Native exchange](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/native/riskium.ontouml.json) · [OWL export](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/derived/riskium.owl.ttl)

</details>

<h2 id="C-21">C-21 — Reported and computed scores</h2>

A reported RiskScoreResult may have no derivedFrom links. A computed RiskScoreResult requires at least one linked DimensionAssessmentResult, a pinned method and adequate inputs. The score kind must be recorded.

**OWL encoding:** Score/result properties retain local bounds, no universal derivedFrom minimum

**OWL boundary:** Conditional reported-versus-computed dependency and arithmetic need data rules.

**Historical outcomes:** HermiT `HERMIT-0645` **NOT_RUN**; SHACL `SHACL-0646` **NOT_RUN**.

**Accepted bounded claim:** Reported and computed score meanings/links are distinguished in the conceptual design.

**Remaining/excluded:** Complete current conditional computed-score admission, formula/input scalar schema and reproducible arithmetic engine are not executed public capabilities. Historical private calculation checks remain historical.

**Later SQL assessment overlay (0.2.0):** selected subclauses only; consult the [assessment method](Database-Assurance), [exact mapping](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/implementation/relational/0.2.0/mapping.json) and [executed receipt](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/relational/assessment/report.json.gz). This does not expand the earlier owner acceptance or change either historical engine outcome.

**Evidence:** [evaluation/cq/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/cq/report.json) · [evaluation/manuscript-review/ledger.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/manuscript-review/ledger.json) · [ontology/riskium-model.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/riskium-model.json).

<details markdown="1"><summary>Original fixture identifiers and source route</summary>

**HermiT cases:** No executed case for this obligation.

**SHACL cases:** No executed case for this obligation.

[Conceptual clause](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#C-21) · [Native exchange](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/native/riskium.ontouml.json) · [OWL export](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/derived/riskium.owl.ttl)

</details>

<h2 id="C-22">C-22 — Responsibility identity</h2>

Repeated mandates between the same participants are permitted when grounding assignment, responsibility scope or validity differs. Duplicate representations of the same grounded mandate must resolve to one relator identity; participant equality alone is not an identity key.

**OWL encoding:** No keys based solely on mediated participant pairs

**OWL boundary:** Mandate identity and duplicate adjudication depend on assignment, scope and validity.

**Historical outcomes:** HermiT `HERMIT-0647` **PASS**; SHACL `SHACL-0648` **NOT_RUN**.

**Accepted bounded claim:** Bounded OWL countermodels avoid using participant pair alone as a mandate identity key.

**Remaining/excluded:** Actual assignment/scope/validity grounding and application deduplication of mandates are deferred; no new actual responsibility identities from names.

**Evidence:** [evaluation/cq/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/cq/report.json) · [evaluation/hermit/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/hermit/report.json) · [ontology/riskium-model.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/riskium-model.json).

<details markdown="1"><summary>Original fixture identifiers and source route</summary>

**HermiT cases:** H-C22-NO-PARTICIPANT-PAIR-KEY

**SHACL cases:** No executed case for this obligation.

[Conceptual clause](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#C-22) · [Native exchange](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/native/riskium.ontouml.json) · [OWL export](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/derived/riskium.owl.ttl)

</details>

<h2 id="C-23">C-23 — Context relation coherence</h2>

Every analyzedInContext link is also a hasContext link for the same RiskCase and RiskContextSpecification. The broader hasContext relation may include non-analysis context.

**OWL encoding:** The source-backed `analyzedInContext` to `hasContext` subproperty axiom is encoded

**OWL boundary:** Reverse implication is absent; same-pair implication needs a reasoner test.

**Historical outcomes:** HermiT `HERMIT-0649` **PASS**; SHACL `SHACL-0650` **PASS**.

**Accepted bounded claim:** Current explicit graph coherence checks analyzedInContext as a subrelation of hasContext with the same pair; no reverse repair.

**Remaining/excluded:** Finite asserted-graph constraint checks, not all data or full task/semantic acceptance.

**Evidence:** [evaluation/hermit/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/hermit/report.json) · [evaluation/shacl/coherence/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/shacl/coherence/report.json) · [ontology/riskium-model.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/riskium-model.json).

<details markdown="1"><summary>Original fixture identifiers and source route</summary>

**HermiT cases:** H-C23-NO-REVERSE-CONTEXT, H-C23-ANALYZED-IMPLIES-CONTEXT

**SHACL cases:** C23-MATCH, C23-GENERAL-ONLY, C23-UNSPECIFIED, C23-MISSING-GENERAL, C23-DIFFERENT-GENERAL, C23-MULTIPLE, C23-MISSING-ONE, C23-UNTYPED-SUBJECT, C23-WRONG-CONTEXT-TYPE, C23-CONTEXT-ALIASES, C23-LABELS-NOT-IDENTITY, C23-RAW-INCOMPLETE, C23-DELETED-RULE, C23-REVERSED-RULE, C23-INTEGRATED-VALID, C23-INTEGRATED-MISSING

[Conceptual clause](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#C-23) · [Native exchange](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/native/riskium.ontouml.json) · [OWL export](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/derived/riskium.owl.ttl)

</details>

<h2 id="C-24">C-24 — Revision coherence</h2>

For each EntryRevision, revisionOf and inherited versionOf identify the same RiskRegisterEntry. previousRevision is irreflexive and acyclic and, when present, relates revisions of the same entry.

**OWL encoding:** The source-backed `revisionOf` to `versionOf` subproperty axiom is encoded

**OWL boundary:** Target coherence follows only for this relationship; irreflexivity, acyclicity and ordering still need reviewed data rules.

**Historical outcomes:** HermiT `HERMIT-0651` **PASS**; SHACL `SHACL-0652` **PASS**.

**Accepted bounded claim:** Current graph coherence and SQLite history enforce selected same-entry revision/version targets and predecessor-cycle rules, including branches and tested long chains.

**Remaining/excluded:** Static graph evidence alone is not history; SQLite history is limited to declared profile and configured connection, not universal storage certification.

**Later SQL assessment overlay (0.2.0):** selected subclauses only; consult the [assessment method](Database-Assurance), [exact mapping](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/implementation/relational/0.2.0/mapping.json) and [executed receipt](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/relational/assessment/report.json.gz). This does not expand the earlier owner acceptance or change either historical engine outcome.

**Evidence:** [evaluation/hermit/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/hermit/report.json) · [evaluation/relational/history/report.json.gz](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/relational/history/report.json.gz) · [evaluation/shacl/coherence/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/shacl/coherence/report.json) · [ontology/riskium-model.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/riskium-model.json).

<details markdown="1"><summary>Original fixture identifiers and source route</summary>

**HermiT cases:** H-C-24-IDENTITY-COUNTERMODEL, H-C24-REVISION-IMPLIES-VERSION

**SHACL cases:** C24-CHAIN-1, C24-CHAIN-2, C24-CHAIN-3, C24-CHAIN-6, C24-CHAIN-12, C24-BRANCH, C24-SKIPPED-PREDECESSOR, C24-BLANK-NODES, C24-MISSING-REVISION-OF, C24-MISSING-VERSION-OF, C24-DIFFERENT-ENTRY-TARGETS, C24-DELETED-EQUALITY, C24-WRONG-ENTRY-TYPE, C24-UNTYPED-REVISION, C24-MULTIPLE-ENTRY-TARGETS, C24-CYCLE-1, C24-CYCLE-2, C24-CYCLE-3, C24-CYCLE-8, C24-CYCLE-17, C24-DELETED-CYCLE, C24-WEAKENED-CYCLE, C24-CROSS-ENTRY, C24-DELETED-LINEAGE, C24-TWO-PREDECESSORS, C24-RELAXED-PREDECESSORS, C24-ENTRY-ALIASES, C24-ALIASED-SELF-LOOP, C24-LABELS-NOT-IDENTITY, C24-RAW-CONFLICT, C24-INTEGRATED-VALID, C24-INTEGRATED-CROSS-ENTRY

[Conceptual clause](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#C-24) · [Native exchange](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/native/riskium.ontouml.json) · [OWL export](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/derived/riskium.owl.ttl)

</details>

<h2 id="C-25">C-25 — Version target coherence</h2>

usesContextVersion targets a version of RiskContextSpecification; usesMethodVersion a version of AssessmentMethodSpecification; usesScaleVersion a version of AssessmentScale; usesCriteriaVersion a version of RiskCriteria. Artifact-level references, when present, agree with versionOf.

**OWL encoding:** Four selected-version target-kind existential restrictions on their source classes

**OWL boundary:** Named `versionOf` and artifact-level reference agreement remain explicit-data joins; no wrong-kind contradiction follows without reviewed artifact-kind disjointness.

**Historical outcomes:** HermiT `HERMIT-0653` **PASS**; SHACL `SHACL-0654` **PASS**.

**Accepted bounded claim:** Bounded native version-target checks and selected explicit-data direct/version reference coherence have executed fixtures. SQL supplements version-owned target coherence only.

**Remaining/excluded:** SQL bindings do not replace native assessment subject/required-role admission; no full conditional multi-relation risk-record acceptance.

**Later SQL assessment overlay (0.2.0):** selected subclauses only; consult the [assessment method](Database-Assurance), [exact mapping](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/implementation/relational/0.2.0/mapping.json) and [executed receipt](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/relational/assessment/report.json.gz). This does not expand the earlier owner acceptance or change either historical engine outcome.

**Evidence:** [evaluation/hermit/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/hermit/report.json) · [evaluation/relational/history/report.json.gz](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/relational/history/report.json.gz) · [evaluation/shacl/coverage-status.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/shacl/coverage-status.json) · [evaluation/shacl/endpoints/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/shacl/endpoints/report.json) · [evaluation/shacl/report.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/shacl/report.json) · [ontology/riskium-model.json](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/riskium-model.json).

<details markdown="1"><summary>Original fixture identifiers and source route</summary>

**HermiT cases:** H-C25-VERSION-TARGET-RX-014, H-C25-VERSION-TARGET-RX-015, H-C25-VERSION-TARGET-RX-016, H-C25-VERSION-TARGET-RX-013

**SHACL cases:** S-C25-Context-VALID, S-C25-Context-UNTYPED-VERSION, S-C25-Context-UNTYPED-SOURCE, S-C25-Context-MISSING-TARGET, S-C25-Context-WRONG-KIND, S-C25-Context-TWO-TARGETS, S-C25-Context-ALIASED-TARGET, S-C25-Context-DIRECT-MATCH, S-C25-Context-DIRECT-MISMATCH, S-C25-Context-DIRECT-ALIAS, S-C25-Method-VALID, S-C25-Method-UNTYPED-VERSION, S-C25-Method-UNTYPED-SOURCE, S-C25-Method-MISSING-TARGET, S-C25-Method-WRONG-KIND, S-C25-Method-TWO-TARGETS, S-C25-Method-ALIASED-TARGET, S-C25-Method-DIRECT-MATCH, S-C25-Method-DIRECT-MISMATCH, S-C25-Method-DIRECT-ALIAS, S-C25-Scale-VALID, S-C25-Scale-UNTYPED-VERSION, S-C25-Scale-UNTYPED-SOURCE, S-C25-Scale-MISSING-TARGET, S-C25-Scale-WRONG-KIND, S-C25-Scale-TWO-TARGETS, S-C25-Scale-ALIASED-TARGET, S-C25-Scale-DIRECT-MATCH, S-C25-Scale-DIRECT-MISMATCH, S-C25-Scale-DIRECT-ALIAS, S-C25-Criteria-VALID, S-C25-Criteria-UNTYPED-VERSION, S-C25-Criteria-UNTYPED-SOURCE, S-C25-Criteria-MISSING-TARGET, S-C25-Criteria-WRONG-KIND, S-C25-Criteria-TWO-TARGETS, S-C25-Criteria-ALIASED-TARGET

[Conceptual clause](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#C-25) · [Native exchange](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/native/riskium.ontouml.json) · [OWL export](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/ontology/derived/riskium.owl.ttl)

</details>

## Source and review record

Generated by `tools/build_formal_reference.py` from the conceptual source, reviewed OWL mapping, unchanged engine ledgers, [owner-accepted scope](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/owner-review/accepted-scope.json) and later SQL mapping. [Machine-readable routes and digests](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/formal-reference/register.json) preserve the original rows. The register is a reading aid, not a new execution receipt. The full cross-document consistency gate is [#39](https://github.com/ArazSaieArasi3/riskium/issues/39), scheduled before the next stable freeze.


## Current engineering checkpoint

The 25 detailed clauses above retain their original scientific populations and accepted bounded interpretations. Source distribution v0.3.4 is published. SQL 0.7.0 adds a supplementary C065 lifecycle with 43 fixed controls under #53; consistency 0.3.0 accounts for 450 routes under #54. Those later engineering controls do not change the historical HermiT/SHACL denominators or complete every native clause. [Current traceability](Traceability) and [work plan](Work-Plan) bind their limits and next steps.


---

Documentation **0.4.0** · Model **0.3.1** · [Published source v0.3.4](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.4) · [Target v0.3.5](https://github.com/ArazSaieArasi3/riskium/issues/51) · [Equivalent Pages guide](https://arazsaiearasi3.github.io/riskium/current/guide/Formalization.html).

Reviewed explanatory source: [documentation/0.4.0/guides/Formalization.md](https://github.com/ArazSaieArasi3/riskium/blob/2c4b0c46f22c90a3a5782e7c918e79f791aa4816/documentation/0.4.0/guides/Formalization.md). Source SHA-256: `e052a2482208270299c663a32240ffed94351d888af2923d3777a0586df77e69`. Actual channel/source closure: [#55](https://github.com/ArazSaieArasi3/riskium/issues/55).
