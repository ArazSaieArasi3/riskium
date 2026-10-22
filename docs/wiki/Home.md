# Riskium: An Ontology for Risk Knowledge

Riskium makes the subject of risk analysis distinct from the entries, scenarios, assessments and evidence describing it. This documentation explains the current conceptual model, its requirements and the limits of its evaluation.

The conceptual design is version 0.3.1. A native OntoUML exchange has documented schema, source-fidelity and SDK interoperability checks. A bounded typed-core OWL mapping and [scoped HermiT run](https://github.com/ArazSaieArasi3/riskium/blob/main/evaluation/hermit/report.md) are recorded: 693 executed cases passed, covering 281 of 295 reasoner obligations; 14 engine-specific constraint rows remain NOT_RUN. The [SHACL ledger](https://github.com/ArazSaieArasi3/riskium/blob/main/evaluation/shacl/coverage-status.md) records 341 scoped PASS, one PARTIAL and 17 NOT_RUN of 359 obligations. These are engineering results; independent semantic review remains open.

## Reading routes

- Research: [purpose and scope](Scope), [requirements and competency questions](Requirements), then [evaluation and limitations](Evaluation).
- Domain interpretation: [modeling decisions](Modeling-Decisions) and [how to inspect the model](Using-the-Model).
- Technical: [model source](https://github.com/ArazSaieArasi3/riskium/blob/main/ontology/riskium-model.json), [reproducibility](https://github.com/ArazSaieArasi3/riskium/blob/main/docs/reproducibility.md) and [candidate prerelease claims](https://github.com/ArazSaieArasi3/riskium/blob/main/evaluation/release-claims.md).

The [repository](https://github.com/ArazSaieArasi3/riskium) owns the version-controlled model. Wiki explanations and generated references use those definitions; they do not independently redefine them.

## Authors, reuse and citation

The authors are Araz Saie Arasi, Hassan Haghighi and Hossein Azgomi, in manuscript order. See their exact [affiliations](https://github.com/ArazSaieArasi3/riskium/blob/main/AUTHORS.md) and [citation metadata](https://github.com/ArazSaieArasi3/riskium/blob/main/CITATION.cff). Original scientific artifacts and Wiki content use CC BY 4.0; original project software uses MIT under the distinct [license scopes](https://github.com/ArazSaieArasi3/riskium/blob/main/RIGHTS.md). Third-party material retains its own terms. No DOI is asserted.
