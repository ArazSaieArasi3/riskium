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

The conceptual catalog contains 80 concepts, 134 associations/bridges, 66 generalizations and 25 interpretation constraints. The bounded OWL export contains 77 typed local classes plus one local foundational proxy, 127 object properties and the 66 subclass links. Three optional boundary concepts and seven bridges are excluded. Stereotypes and abstractness annotations do not automatically acquire executable OWL semantics. The [reviewed mapping](../evaluation/owl-mapping-review.md) records the exact axiom choices, restrictions and exclusions.

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

The later [assessment-correction overlay 0.3.0](../implementation/relational/0.3.0/README.md) adds migration 4 and an immutable application declaration between issued versions of one assessment identity. Its 36 fixed scenarios retain original values, source qualifiers and conflicting branches; three native graph comparisons show that no correction predicate was added to OWL. This does not implement general assertion/scenario correction or identify independent corroboration. Reproduce with `python tools/run_relational_correction.py --check` and `python tools/build_correction_inventory.py --check`. The original accepted-scope rows below remain unchanged.

## Reproduce without replacing historical evidence

Use a clean checkout of the desired source and record its commit first. Commands below run from the repository root. Create the appropriate environment from `tools/requirements-hermit.txt`, `tools/requirements-shacl.txt` or `tools/requirements-owl.txt`; documentation dependencies are in `tools/publication/requirements.txt`. The [reproduction guide](reproducibility.md) gives installation and the full module sequence.

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

Use the [term search](https://arazsaiearasi3.github.io/riskium/current/reference/search.html) or [conceptual constraints](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#constraints) to locate the source vocabulary. [Evaluation](guides/Evaluation.md) and the [work plan](work-plan.md) explain the wider evidence and remaining tasks. No complete first-order/TPTP verification package is claimed: adding one requires a separately reviewed translation, assumptions, source mappings, oracles and validation issue before implementation or acceptance claims.
