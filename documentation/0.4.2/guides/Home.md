# Riskium: enterprise risk knowledge

Riskium is a conceptual ontology for organizing enterprise risk information. It separates a continuing risk case from register entries, possible scenarios, assessments and supporting evidence. These distinctions help readers track what a record says without treating a description as proof that an event occurred.

**[Source release v0.3.5](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.5) is published.** This documentation explains model **0.3.1** and the bounded engineering included in that release. The [version guide](Artifact-Versions.md) distinguishes the model, source package, documentation and manuscript.

The next source release, **v0.3.6**, is being prepared. Its assessment selection feature is available only on the [development branch](https://github.com/ArazSaieArasi3/riskium/tree/plan/v0.3.6-assessment-selection). It has not been merged into the published package. [Assessment selection](Database-Assurance.md#assessment-selection-in-development) explains the proposed behavior and what its checks establish.

## Choose a reading path

- **Researcher or reviewer:** [problem and scope](Overview.md) → [modeling rationale](Decisions.md) → [formal method](Formalization.md) → [evidence](Evaluation.md) → [limitations](Limitations.md) → [reproduction](Reproduce.md).
- **Domain specialist:** [scope](Scope.md) → [using the model](Using-the-Model.md) → [competency questions](Competency-Questions.md) → [sources](References.md) → [limitations](Limitations.md).
- **Developer or integrator:** [model views](Visualization.md) → [database behavior and API boundaries](Database-Assurance.md) → [traceability](Traceability.md) → [reproduction](Reproduce.md) → [release and citation](Publication.md).

## Inspect an artifact

Use the [conceptual reference](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html) for definitions and constraints, the [selected diagram](https://arazsaiearasi3.github.io/riskium/current/reference/diagrams/index.html) for orientation, and the [OWL reference](https://arazsaiearasi3.github.io/riskium/current/widoco/index-en.html) for the bounded formal export. [Find a term](https://arazsaiearasi3.github.io/riskium/current/reference/search.html) or follow the [text explorer](https://arazsaiearasi3.github.io/riskium/current/explore/index.html) to inspect named connections. The [visualization guide](Visualization.md) explains each view's limits.

## What the evidence supports

The release supports source preservation, selected formal checks and finite software/database contracts. It does not establish whole-model semantic correctness, production readiness or organizational benefit. All eleven organizational case admissions remain withheld, and independent semantic ratings remain zero. [Evaluation](Evaluation.md) explains the results; [the work plan](Work-Plan.md) identifies the remaining research decisions.
