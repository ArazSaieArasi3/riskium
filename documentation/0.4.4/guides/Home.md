# Riskium: organizational risk knowledge

Riskium is a conceptual ontology for organizing organizational risk knowledge. It connects a continuing risk case with its register entries, scenarios, objectives, assessments and evidence while preserving their identities, versions and sources.

## Follow a report through change

A source reports an **unfavorable** effect on a delivery objective. It later declares two alternative corrections: one **favorable**, one **mixed**. A second source retains its own unfavorable report. Riskium keeps each report, source and recorded context separately. It does not choose which report is true.

[See the version-by-version example](Using-the-Model.md#risk-nature-history) → [inspect the query contract](Database-Assurance.md#risk-nature-retrieval) → [run it](Reproduce.md#risk-nature-example).

**[Published source v0.3.6](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.6)** includes assessment selection using SQL 0.8.0/schema 9. **Risk-nature retrieval is executed development for proposed v0.3.7**, using SQL 0.9.0/schema 10. The model and OWL remain **0.3.1**. Documentation **0.4.4** explains both source roles; [artifact versions](Artifact-Versions.md) and [the work plan](Work-Plan.md) show the release boundary.

## Choose a reading path

- **Researcher or reviewer:** [scope and rationale](Overview.md) → [native commitments](Decisions.md) → [source-to-result trace](Traceability.md) → [evaluation](Evaluation.md) → [limitations](Limitations.md).
- **Domain specialist:** [scope](Scope.md) → [report and correction example](Using-the-Model.md#risk-nature-history) → [questions the model answers](Competency-Questions.md) → [sources](References.md) → [limits](Limitations.md).
- **Developer or integrator:** [query behavior](Database-Assurance.md#risk-nature-retrieval) → [executable example](Reproduce.md#risk-nature-example) → [trace and receipt](Traceability.md) → [distribution status](Publication.md).

## Inspect the model

[Conceptual reference](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html) · [selected and complete diagrams](https://arazsaiearasi3.github.io/riskium/current/reference/diagrams/index.html) · [WebVOWL](https://arazsaiearasi3.github.io/riskium/current/webvowl/index.html) · [bounded OWL reference](https://arazsaiearasi3.github.io/riskium/current/widoco/index-en.html) · [find a term](https://arazsaiearasi3.github.io/riskium/current/reference/search.html).

## What the evidence supports

The nature task has **60 completed engineering controls and 51 malformed-request variants**. These differ from historical HermiT/SHACL populations and semantic review. All eleven organizational admissions remain **WITHHELD**; independent semantic ratings remain **zero**. [Evaluation](Evaluation.md) explains the populations and [the work plan](Work-Plan.md) identifies the remaining release and research work.
