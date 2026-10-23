# Ontology requirements specification

Documentation revision 0.4.2; conceptual design 0.3.1; English public export, 21 October 2026.

Riskium organizes risk knowledge for interpretation, continuity, provenance and analysis. Intended readers include risk analysts, domain experts, ontology researchers and technical integrators. The scope concerns knowledge and recorded statements, rather than prescribing a complete management process.

This revision preserves the twelve current requirement families and eight current scope obligations while removing obsolete application/status references. Historical acquisition material is outside this public export. No historical test result is inherited as a current formal pass.

## Current requirements

### Content scope

Reference: RKRS-01; priority: MUST.

Represent risk content, context and evidence without prescribing a management process.

Acceptance: Map information without inferring process compliance.

Reject: Inferring a complete process or certification from stored content.

### Case continuity

Reference: RKRS-02; priority: MUST.

Keep a case distinct from register entries, scenarios, scores and occurrences.

Acceptance: Two entries and two scenarios can concern one case without identity collapse.

Reject: Merging cases solely because labels or scores match.

### Document identity and history

Reference: RKRS-03; priority: MUST.

Separate artifact, issued version and expressed content; preserve issued payloads.

Acceptance: Retrieve a superseded issued version without overwriting it.

Reject: Historical retrieval silently reads current mutable values.

### Assessment context

Reference: RKRS-04; priority: MUST.

Retain method, scale, dimension, basis, context and time with results.

Acceptance: Equal scores on incompatible versions remain distinguishable.

Reject: Treating missing context as zero or equal values as comparability.

### Reported and computed scores

Reference: RKRS-05; priority: MUST.

Distinguish supplied scores from calculations with justified pinned inputs.

Acceptance: Retain an unverified reported score; reject a claimed computation with missing required inputs.

Reject: Presenting supplied arithmetic as a verified calculation.

### Source-qualified assertions

Reference: RKRS-06; priority: MUST.

Preserve source content, locator, interpretation origin, corrections and conflicting assertions.

Acceptance: A proposed mapping preserves its source assertion and does not create an occurrence.

Reject: Overwriting evidence or treating a correction as independent corroboration.

### Evidence-qualified responsibility

Reference: RKRS-07; priority: MUST.

Keep assignment information separate from an asserted mandate; ground actual relators with distinct participants.

Acceptance: Retain an assignment record without fabricating an actor or actual mandate.

Reject: Inferring Risk Owner or a second actor from documentation alone.

### Time and workflow

Reference: RKRS-08; priority: MUST.

Separate recorded, reference and validity time and scheme-qualified workflow interpretation.

Acceptance: A closed entry does not establish cessation; an absent rule stays unknown.

Reject: Inferring treatment effectiveness or cessation from a state label.

### External boundaries and modes

Reference: RKRS-09; priority: MUST.

Keep heterogeneous referents optional; vulnerability requires one justified object bearer.

Acceptance: The typed projection excludes untyped boundary notions and preserves bearer dependence.

Reject: Treating a description as an actual vulnerability or an untyped boundary as a typed core class.

### Policies and thresholds

Reference: RKRS-10; priority: MUST.

Preserve source-qualified appetite/tolerance meanings and a compatible indicator or scale anchor.

Acceptance: A scale-only threshold can be represented without inventing an indicator.

Reject: Collapsing different source meanings or inventing required evidence.

### Projection and admission

Reference: RKRS-11; priority: MUST.

Account for model elements and distinguish raw, managed and task-ready data.

Acceptance: An incomplete record remains available without a false readiness declaration.

Reject: Confusing data completeness, mapping allocation and semantic adequacy.

### Quality evidence and reuse

Reference: RKRS-12; priority: SHOULD.

Bind claims to the exact model, evidence population, method and limits.

Acceptance: Every published result identifies its input version and scope.

Reject: Inheriting a result from a different version or treating counts as semantic validity.

## Competency questions

- **Which entries document the same case?** Expected: Two distinct entries can refer to one case. Reject: Entries become the case or are grouped by equal labels.
- **Which scenarios concern a case?** Expected: Distinct scenario specifications link to the case. Reject: Scenario identity is collapsed into case identity.
- **Can equal scores use different scale versions?** Expected: Both values and their different pinned scales remain retrievable. Reject: Numeric equality alone authorizes comparison.
- **Can assignment information exist without an actual mandate?** Expected: The assignment is retained without an asserted real mandate. Reject: A relator or second actor is invented.
- **Does entry closure establish risk cessation?** Expected: Closure and cessation evidence are independent. Reject: Closure automatically establishes cessation.
- **Can an assertion be traced to its source?** Expected: Its source identity, locator and interpretation origin are recoverable. Reject: Missing or misjoined provenance is presented as source support.
- **Does correction lineage remain distinguishable?** Expected: A correction is linked to its corrected statement. Reject: The correction is counted as independent corroboration.
- **Can unsupported case identity remain unasserted?** Expected: A candidate scenario can remain incomplete without a fabricated case. Reject: An identity is invented to satisfy a managed-record constraint.

## Traceability and evidence status

The post-prerelease [traceability ledger](../evaluation/traceability/README.md) now reconciles all 12 requirement families, eight scope obligations and eight CQ identities against exact model elements and source-bound evidence. The [CQ contracts](cq/README.md) record 40 executed synthetic queries: 32 answer cases and eight detected query mutants. Five original synthetic-task contracts have bounded execution; CQ06–CQ08 still need their declared independent evidence population in #13. Numeric, locator and general correction metadata use an explicit supplementary record policy. Neither trace completeness nor matching synthetic answers establishes full requirement or independent semantic acceptance.

Machine-readable [requirements](requirements.json), [scope obligations](scope-requirements.json), [competency questions](competency-questions.json) and [test obligations](test-obligations.csv) retain distinct identities and statuses. Requirement-to-constraint links are current design links, not proof of fulfillment.

The [engineering policy](engineering-policy.md) defines the method. The [formal-validation plan](../evaluation/formal-validation-plan.md) defines the coverage contract. The native OntoUML exchange now has schema, SDK and source-fidelity checks with explicit generalization-set decisions. The bounded OWL mapping and scoped HermiT/SHACL modules have executed; their reports preserve the remaining unexecuted routes. Complete semantic verification, requirement/CQ acceptance and independent semantic adequacy review remain open. See the [OWL review](../evaluation/owl-mapping-review.md), [HermiT report](../evaluation/hermit/report.md) and [SHACL ledger](../evaluation/shacl/coverage-status.md).
