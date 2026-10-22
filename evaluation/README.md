# Evaluation status

This snapshot has migration-integrity, structural, coverage-design, native-exchange, bounded OWL-mapping and scoped HermiT checks. They verify the exported inventory, references, endpoint cardinality syntax and direction, inheritance structure, publication boundary, official exchange-schema conformance, SDK interoperability, OWL Turtle syntax and source mapping, and the executed reasoning cases. They do not establish domain adequacy, complete OntoUML semantic conformance or SHACL execution.

The [native model review](native-model-review.md) records the source-preserving exchange representation, ten design dispositions, explicit generalization-set policy and legacy verifier limitations.

The [OWL mapping review](owl-mapping-review.md) records the three pinned inputs, axiom choices, import and identity decisions, and disposition of all 25 interpretation constraints. The [receipt](owl-mapping-receipt.json) records input and output digests and coverage counts. RDF parsing and regression checks are mapping checks, not logical reasoning.

The [HermiT report](hermit/report.md) records actual reasoning outcomes, the [JSON receipt](hermit/report.json) records every case, and the [RDF/XML premise](hermit/premise.rdf) pins the exact input graph. The [remaining-route review](hermit/remaining-routes.md) assigns the 14 unexecuted constraint rows and the explicit-data remainder of three bounded OWL passes. Its baseline fraction separates executed obligations from the constraints still lacking a sound HermiT oracle. Supplemental inference and mutation cases have their own denominator. This evidence does not substitute for SHACL, independent semantic review or empirical adequacy.

The [migration receipt](migration-integrity.json) states what was preserved and edited. The earlier [coverage plan](coverage-plan.json) and [test obligations](../requirements/test-obligations.csv) identify planned formal work; their planning statuses predate the HermiT execution. Use the HermiT report for current reasoner outcomes.

The [coverage contract](coverage-contract.md) records expected behavior, engine limits and planned routes for all 25 constraints. Its [row review](coverage-review.json) accounts for all 674 baseline obligations against exact source elements. Ten supplementary families retain imports, optional boundaries, scope requirements and integration work outside that baseline. The HermiT report records the subsequent scoped execution; the other formal and review routes remain distinct.

HermiT tests OWL consistency, class satisfiability and supported entailment/non-entailment on the reviewed mapping. SHACL is intended for declared explicit-data profiles. Constraints outside either formalism need an explicit policy, application check or review disposition; they must not disappear from the denominator.

Independent semantic review, case-based adequacy, standards interpretation, query answerability and reproducibility are separate evidence categories. A single aggregate pass percentage cannot replace these judgments.

Read the [formal-validation plan](formal-validation-plan.md) and [roadmap](../docs/roadmap.md) for remaining work.
