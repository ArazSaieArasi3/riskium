# Problem, approach and contribution

> Reader 0.4.7 accompanies the v0.3.8 source package. Model/OWL remain 0.3.1 and SQL remains 0.9.0/schema 10. The current author-held manuscript is 7.2.3; its public receipt records ten pages and 36 references. Release status is established by the separate publication record.

## Retained technical checkpoint

The following technical material retains its original 0.4.5 wording, source links and dated populations. Its references to manuscript 7.0.8 or earlier releases describe those checkpoints, not the current article or an extra validation claim. [Current artifact roles](Artifact-Versions.md), [publication](Publication.md) and [work plan](Work-Plan.md) distinguish them.

Risk records can mix the subject being monitored with descriptions, possible scenarios, scores and source documents. Riskium makes their different identity and interpretation roles explicit. A continuing RiskCase can have several entries and scenarios; a scenario specification is different from an actual occurrence.

## What the model contributes

The conceptual model separates cases, records, information artifacts and issued versions. Assessment information carries the method, scale, dimension, basis, context and time needed to interpret a result. Responsibility information does not by itself establish a real mandate, and administrative closure does not establish that a risk ceased.

These distinctions support traceable interpretation of incomplete or conflicting information. They do not establish predictive accuracy, risk reduction, regulatory compliance or production readiness. [Scope](Scope.md) states the boundaries, and [modeling decisions](Decisions.md) explains the rationale.

## How the artifacts fit together

The [conceptual source](https://github.com/ArazSaieArasi3/riskium/blob/58ff468ec4e8f3500ace6869601a25ea263c3d9f/ontology/riskium-model.json) defines the design. A native OntoUML exchange preserves the source and records explicit generalization-set decisions. The bounded OWL export represents selected formal commitments; SHACL profiles and database checks address separate explicit-data and history tasks.

Use the [formal-method guide](Formalization.md) to understand those assumptions, then [evaluation](Evaluation.md) to inspect actual results and their populations. [Traceability](Traceability.md) connects requirements and claims to source and evidence. The [source register](References.md) records inspected comparisons and remaining related-work limits; it does not establish universal novelty or superiority.

## Where to continue

For a concrete inspection task, read [using the model](Using-the-Model.md). For a review, continue through [evaluation](Evaluation.md), [limitations](Limitations.md), [reproduction](Reproduce.md) and the [exact published release](Publication.md).
