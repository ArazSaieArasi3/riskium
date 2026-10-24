# Ontology requirements specification

Documentation revision **0.4.3**; conceptual design **0.3.1**; owner-approved release scope, **24 October 2026**. Previous documentation revision 0.4.2 remains in Git history at commit `193dc7209bc762f11e5e12e19e5aae42cee22cb3`.

Riskium organizes risk knowledge for interpretation, continuity, provenance and analysis. Intended readers include risk analysts, domain experts, ontology researchers and technical integrators. The scope concerns knowledge and recorded statements, rather than prescribing a complete management process.

This revision preserves the twelve current requirement families and eight current scope obligations while removing obsolete application/status references. Historical acquisition material is outside this public export. No historical test result is inherited as a current formal pass.

## Accepted scope for the first final release

The owner explicitly read and accepted the concrete 11-axis review on 24 October 2026. This revision synchronizes that decision with the source-bound evidence and manuscript 7.0.8. The [machine-readable release-scope overlay](https://github.com/ArazSaieArasi3/riskium/blob/8afe169968b5c1396c02834dbc499af691b894b4/requirements/release-scope-v0.3.1.json) preserves every original requirement, criterion, negative criterion and priority alongside the current accepted scope. The original source definitions and historical engine/trace ledgers remain unchanged. Full original requirement fulfillment is not claimed.

Riskium v0.3.1 is a bounded, reproducible risk-knowledge research artifact. Accepted tasks include declared metadata compatibility, selected level/scale joins and direct-comparison eligibility, scoped SQLite identity/history preservation, source trace and correction/withheld-identity queries. Source/standards statements remain portion-qualified; author review is disclosed and is not independent validation.

**The owner explicitly accepts these release boundaries:** RKRS-05 retains its MUST priority and conceptual distinction, while complete computed-score admission/arithmetic is not a current executed capability; RKRS-08 retains its MUST priority and recorded-time/workflow distinctions, while complete interval/transition/cessation execution is not claimed; RKRS-11 retains its MUST priority, while admission/readiness is supported only for the individually named executed profiles. A critical defect inside a retained task cannot be waived by this scope decision.

The [accepted all-clause/claim overlay](https://github.com/ArazSaieArasi3/riskium/blob/8afe169968b5c1396c02834dbc499af691b894b4/evaluation/owner-review/accepted-scope.json) covers all 25 clauses and all 28 requirement/scope/CQ traces, including proposed alternatives for the historical 14 HermiT and 17 SHACL NOT_RUN rows. Alternatives are not new engine PASS outcomes. The [artifact compatibility table](Artifact-Versions) binds independent document/model/database versions. Final publication still needs its exact technical freeze.

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

The post-prerelease [traceability ledger](Traceability) now reconciles all 12 requirement families, eight scope obligations and eight CQ identities against exact model elements and source-bound evidence. The [CQ contracts](Competency-Questions) record 40 executed synthetic queries: 32 answer cases and eight detected query mutants. At the original checkpoint, five synthetic-task contracts have bounded execution and CQ06–CQ08 lack their declared independent evidence population. Later separately bound CQ06 evidence covers 13 inspected source statements; CQ07/CQ08 evidence covers five original/reissued pairs and 11 still-withheld identity candidates. The owner accepts these finite source-backed tasks for this release; full original/independent population acceptance remains outside the current claim under #13. Numeric, locator and general correction metadata use an explicit supplementary record policy. Neither trace completeness nor matching synthetic answers establishes full requirement or independent semantic acceptance.

Machine-readable [requirements](https://github.com/ArazSaieArasi3/riskium/blob/8afe169968b5c1396c02834dbc499af691b894b4/requirements/requirements.json), [scope obligations](https://github.com/ArazSaieArasi3/riskium/blob/8afe169968b5c1396c02834dbc499af691b894b4/requirements/scope-requirements.json), [competency questions](https://github.com/ArazSaieArasi3/riskium/blob/8afe169968b5c1396c02834dbc499af691b894b4/requirements/competency-questions.json) and [test obligations](https://github.com/ArazSaieArasi3/riskium/blob/8afe169968b5c1396c02834dbc499af691b894b4/requirements/test-obligations.csv) retain distinct identities and statuses. Requirement-to-constraint links are current design links, not proof of fulfillment.

The [engineering policy](https://github.com/ArazSaieArasi3/riskium/blob/8afe169968b5c1396c02834dbc499af691b894b4/requirements/engineering-policy.md) defines the method. The [formal-validation plan](https://github.com/ArazSaieArasi3/riskium/blob/8afe169968b5c1396c02834dbc499af691b894b4/evaluation/formal-validation-plan.md) defines the coverage contract. The native OntoUML exchange now has schema, SDK and source-fidelity checks with explicit generalization-set decisions. The bounded OWL mapping and scoped HermiT/SHACL modules have executed; their reports preserve the remaining unexecuted routes. Complete semantic verification and full original/independent requirement/CQ acceptance remain open. The current bounded release scope has attributable owner acceptance; the exact final technical freeze remains pending. See the [OWL review](Formalization), [HermiT report](https://github.com/ArazSaieArasi3/riskium/blob/8afe169968b5c1396c02834dbc499af691b894b4/evaluation/hermit/report.md) and [SHACL ledger](https://github.com/ArazSaieArasi3/riskium/blob/8afe169968b5c1396c02834dbc499af691b894b4/evaluation/shacl/coverage-status.md).

---

[Equivalent Pages guide](https://arazsaiearasi3.github.io/riskium/current/guide/Requirements.html) · [WIDOCO](https://arazsaiearasi3.github.io/riskium/current/widoco/index-en.html) · [OWL explorer](https://arazsaiearasi3.github.io/riskium/current/explore/index.html) · [Published v0.3.1](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.1).

Explanatory source: [requirements/ontology-requirements.md](https://github.com/ArazSaieArasi3/riskium/blob/main/requirements/ontology-requirements.md). Source SHA-256: `68e09fd8cce2805da2d2fa0f29f76b0601282c598855d99a41631dccfaf9ff33`. This current explanation and later development evidence are separate from the immutable v0.3.1 source assets.
