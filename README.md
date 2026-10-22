# Riskium

Riskium is a conceptual ontology for organizing risk knowledge. It distinguishes a managed risk case from its register entries, scenario specifications, assessment results and supporting evidence.

The model supports the interpretation and traceability of risk information. It does not prescribe a complete risk-management process or establish regulatory compliance.

## Start here

| Goal | Read |
| --- | --- |
| Understand the scope and main distinctions | [Overview](docs/overview.md) |
| Inspect the conceptual model | [Complete model](ontology/riskium-model.json) and [typed projection](ontology/derived/typed-core.json) |
| Inspect the bounded OWL mapping | [OWL Turtle](ontology/derived/riskium.owl.ttl) and [mapping review](evaluation/owl-mapping-review.md) |
| View the model | [Selected view](diagrams/selected-view.svg) and [complete view](diagrams/complete-view.svg) |
| Review the requirements | [Ontology requirements](requirements/ontology-requirements.md) |
| Assess the evidence and remaining work | [Evaluation](evaluation/README.md) and [roadmap](docs/roadmap.md) |
| Inspect the HermiT reasoning evidence | [Human-readable report](evaluation/hermit/report.md), [JSON receipt](evaluation/hermit/report.json) and [exact premise](evaluation/hermit/premise.rdf) |
| Inspect explicit-data validation | [Current SHACL coverage](evaluation/shacl/coverage-status.md), [endpoint report](evaluation/shacl/endpoints/report.md), [conditional-profile report](evaluation/shacl/report.md) and [profile decisions](evaluation/shacl/profile-review.md) |
| Understand semantic assurance | [Measures and limits](evaluation/semantic-assurance-plan.md) and [independent-review inventory](evaluation/semantic-review-register.json) |
| Reproduce the local checks | [Reproducibility](docs/reproducibility.md) |
| Browse the prepared Wiki content | [Wiki source](docs/wiki/Home.md) |

## Current state

The imported conceptual design is version **0.3.1**. Its complete catalog contains 80 concepts, including 77 typed core concepts and three optional phenomenon boundaries. One imported foundational anchor is recorded separately. The model records 134 associations or bridges, 66 generalizations and 25 interpretation constraints.

The source JSON is a structured conceptual design. A [native OntoUML exchange representation](ontology/native/riskium.ontouml.json) preserves that source and records explicit generalization-set decisions. Its [review](evaluation/native-model-review.md) reports official schema conformance, SDK interoperability, source fidelity and the remaining semantic limits. A [bounded OWL 2 mapping](ontology/derived/riskium.owl.ttl) covers the typed core; its [review](evaluation/owl-mapping-review.md) explains the local anchor proxy, open-world restrictions and deferred constraints. A [HermiT suite](evaluation/hermit/report.md), [conditional SHACL batch](evaluation/shacl/report.md) and all 254 [ordered endpoint checks](evaluation/shacl/endpoints/report.md) have executed; the [current SHACL ledger](evaluation/shacl/coverage-status.md) preserves their separate scopes. These engineering checks do not establish independent semantic validity or an overall semantic-correctness percentage.

The [generated reference](docs/site/index.html) is prepared for local browsing; a public Pages deployment and native Wiki publication have not yet been verified. No stable scholarly release or DOI is claimed.

## Reuse and contribution

Read the [reading guide](READING-GUIDE.md), [contribution rules](CONTRIBUTING.md) and [rights status](RIGHTS.md). Public documentation is maintained in English. Definitions have one owner in the model; explanations and generated views refer to that source.
