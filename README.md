# Riskium

Riskium is a conceptual ontology for organizing risk knowledge. It distinguishes a managed risk case from its register entries, scenario specifications, assessment results and supporting evidence.

The model supports the interpretation and traceability of risk information. It does not prescribe a complete risk-management process or establish regulatory compliance.

## Start here

| Goal | Read |
| --- | --- |
| Understand the scope and main distinctions | [Overview](docs/overview.md) |
| Inspect the conceptual model | [Complete model](ontology/riskium-model.json) and [typed projection](ontology/derived/typed-core.json) |
| View the model | [Selected view](diagrams/selected-view.svg) and [complete view](diagrams/complete-view.svg) |
| Review the requirements | [Ontology requirements](requirements/ontology-requirements.md) |
| Assess the evidence and remaining work | [Evaluation](evaluation/README.md) and [roadmap](docs/roadmap.md) |
| Reproduce the local checks | [Reproducibility](docs/reproducibility.md) |
| Browse the prepared Wiki content | [Wiki source](docs/wiki/Home.md) |

## Current state

The imported conceptual design is version **0.3.1**. Its complete catalog contains 80 concepts, including 77 typed core concepts and three optional phenomenon boundaries. One imported foundational anchor is recorded separately. The model records 134 associations or bridges, 66 generalizations and 25 interpretation constraints.

The source JSON is a structured conceptual design. A [native OntoUML exchange representation](ontology/native/riskium.ontouml.json) now preserves that source and records explicit generalization-set decisions. Its [review](evaluation/native-model-review.md) reports official schema conformance, SDK interoperability, source fidelity and the remaining semantic limits. A complete OWL formalization is not yet provided. The HermiT and SHACL suites are planned, not executed. These engineering checks do not establish independent semantic validity.

The [generated reference](docs/site/index.html) is prepared for local browsing; a public Pages deployment and native Wiki publication have not yet been verified. No stable scholarly release or DOI is claimed.

## Reuse and contribution

Read the [reading guide](READING-GUIDE.md), [contribution rules](CONTRIBUTING.md) and [rights status](RIGHTS.md). Public documentation is maintained in English. Definitions have one owner in the model; explanations and generated views refer to that source.
