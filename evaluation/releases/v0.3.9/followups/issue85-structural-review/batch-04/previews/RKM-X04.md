# Risk Evaluation Outcome — N3b-4 documentary preview

**Planning preview; not deployed or independently validated.**

## Authored definition, unchanged

A recorded judgment of risk significance or acceptability based on identified assessment information and criteria versions. It is distinct from a numeric score and from the evaluation activity.

[Source model 0.3.2](https://github.com/ArazSaieArasi3/riskium/blob/8a115ef9c3fb6b0501c6ed9c9fd6b258d358028e/ontology/0.3.2/riskium-model.json); subdomain D05; stereotype subkind; identity supplier RKM-C014.

Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.

Authored verification status, preserved verbatim: Bounded review and finite tests; native OntoUML and independent semantic validation pending

Later bounded qualification/publication evidence is in the [v0.3.9 receipt](https://github.com/ArazSaieArasi3/riskium/blob/8a115ef9c3fb6b0501c6ed9c9fd6b258d358028e/evaluation/releases/v0.3.9/R2b-outcome.md). Source labels and documentary comparisons are not independent semantic ratings.

## Documentary comparison

**CONTRAST → CONTRAST**.

Retain the distinction between a criteria-based significance/acceptability judgment and a DQV metric result. This is a difference of intended role, not a global disjointness claim between external and local classes.

| Selected term | Source kind and locator |
|---|---|
| [dqv:QualityMeasurement](https://www.w3.org/TR/2016/NOTE-vocab-dqv-20161215/#dqv:QualityMeasurement) | DATASET_QUALITY_PATTERN_CLASS; §4.1 |

## Current structural context

RX-011 identifies the case, RX-012 requires assessment information and RX-013 pins a criteria ArtifactVersion. C-25 governs the versioned target. A numeric score alone does not establish acceptability or a treatment decision; revised case and version neighbors were reviewed.

Source continuity: concept record unchanged=True; direct edges unchanged=True; inherited edges unchanged=True. Ancestor and neighbor changes are reported separately.

| Observation | Source-bound result |
|---|---|
| Inheritance path | GX-063: RKM-X04 → RKM-C014 |
| Source constraint route | C-01, C-04, C-18, C-25 — [selected source statements](../assessment-checks.json) |
| Changed ancestor | RKM-C014: typing_rationale |
| Changed relation neighbor | RKM-C015: typing_rationale; RKM-X01: definition, identity_basis, typing_rationale |
| Excluded blanket sets | GS-RKM-C014 |

Documentary identity is separate from activity, risk identity and real-world values. Comparable interpretation requires the selected method/scale/dimension/basis/context/time or a justified transformation; missing input is not zero. A recorded score does not by itself establish acceptability, and a qualitative uncertainty statement need not contain probability.

Complete source observations are in [contexts.json](../contexts.json). Context SHA-256: `19a02aea5aad30b76949da44d9c767ab18fbe6bde952996fb4b1add053ca28dd`.

Authored definition SHA-256: `0f69cfccc44bc1be7f1e88e8d0334ed8c1d0e0c304187d86e1d638ca4d8d40e6`.

No formal alignment axiom, new ontology-engine execution or independent expert rating is supplied. Remaining documentary batches, full component qualification and actual publication/readback retain their separate gates. #23 and #78 remain separate.
