# Plan Specification — N3b-5 documentary preview

**Planning preview; not deployed or independently validated.**

## Authored definition, unchanged

A versioned specification of intended actions, resources, responsibilities, timing and conditions for a stated purpose.

[Source model 0.3.2](https://github.com/ArazSaieArasi3/riskium/blob/64ebfa6c9bec92184f5671cb6d5aef6397b0a9e1/ontology/0.3.2/riskium-model.json); subdomain D06; stereotype subkind; identity supplier RKM-C014.

Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.

Authored verification status, preserved verbatim: Bounded review and finite tests; native OntoUML and independent semantic validation pending

Later bounded qualification/publication evidence is in the [v0.3.9 receipt](https://github.com/ArazSaieArasi3/riskium/blob/64ebfa6c9bec92184f5671cb6d5aef6397b0a9e1/evaluation/releases/v0.3.9/R2b-outcome.md). Source labels and documentary comparisons are not independent semantic ratings.

## Documentary comparison

**RELATED → RELATED**.

Retain PROV Plan as related intended-action content. Riskium records its own resources, responsibility, timing, purpose and versions without adopting a full PROV representation or treating the plan as its execution.

| Selected term | Source kind and locator |
|---|---|
| [prov:Plan](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Plan) | PROVENANCE_CLASS; §4.3, Plan |

## Current structural context

R-21 concerns one or more analytical risk cases; R-62 gives the plan role. R-64 relates an actual TreatmentActivity separately, and R-63 can connect decisions. A plan can be recorded before any execution is established; issued-content changes follow new-version lineage.

Source continuity: concept record unchanged=True; direct edges unchanged=True; inherited edges unchanged=True. Ancestor and neighbor changes are reported separately.

| Observation | Source-bound result |
|---|---|
| Inheritance path | G-15: RKM-C043 → RKM-C014 |
| Source constraint route | C-01, C-02, C-03, C-05 — [selected source statements](../treatment-policy-checks.json) |
| Changed ancestor | RKM-C014: typing_rationale |
| Changed relation neighbor | RKM-X01: definition, identity_basis, typing_rationale |
| Excluded blanket sets | GS-RKM-C014 |

Recorded choices, plans and references remain information; actual activity, realized controls and effectiveness need their own support. Vocabulary labels do not establish resource identity, authority or cross-framework equivalence. Source-qualified appetite/tolerance statements and their contexts are preserved without importing unseen normative terms.

Complete source observations are in [contexts.json](../contexts.json). Context SHA-256: `bf0c8fe45f5456b9e4789fcd56cda8a2b6d6a395c54eef67249b4f5a409e9ccc`.

Authored definition SHA-256: `0ceb042882790789768aa62e9b44e782b0f67834b31d2e29baafb728d8b5bbd8`.

No formal alignment axiom, new ontology-engine execution or independent expert rating is supplied. Remaining documentary batches, full component qualification and actual publication/readback retain their separate gates. #23 and #78 remain separate.
