# Assessment Basis — N3b-4 documentary preview

**Planning preview; not deployed or independently validated.**

## Authored definition, unchanged

A specification of assumptions and control conditions under which an assessment result is interpreted.

[Source model 0.3.2](https://github.com/ArazSaieArasi3/riskium/blob/8a115ef9c3fb6b0501c6ed9c9fd6b258d358028e/ontology/0.3.2/riskium-model.json); subdomain D05; stereotype subkind; identity supplier RKM-C014.

Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.

Authored verification status, preserved verbatim: Bounded review and finite tests; native OntoUML and independent semantic validation pending

Later bounded qualification/publication evidence is in the [v0.3.9 receipt](https://github.com/ArazSaieArasi3/riskium/blob/8a115ef9c3fb6b0501c6ed9c9fd6b258d358028e/evaluation/releases/v0.3.9/R2b-outcome.md). Source labels and documentary comparisons are not independent semantic ratings.

## Documentary comparison

**NO_DIRECT_EQUIVALENT_REVIEWED → CONTRAST**.

Clarify the former scoped-absence label as a contrast in definitional scope: generic prov:Entity can describe provenance, but does not define risk-specific assumptions or control conditions. No disjointness, global absence or exact external equivalent is asserted.

| Selected term | Source kind and locator |
|---|---|
| [prov:Entity](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Entity) | PROVENANCE_CLASS; §4.1, Entity |

## Current structural context

R-12 makes the basis explicit for the assessment information; RK2-022 may identify the control baseline assumed. The documentary specification does not establish that the controls exist or are effective, and different bases cannot be silently pooled.

Source continuity: concept record unchanged=True; direct edges unchanged=True; inherited edges unchanged=True. Ancestor and neighbor changes are reported separately.

| Observation | Source-bound result |
|---|---|
| Inheritance path | G-09: RKM-C033 → RKM-C014 |
| Source constraint route | C-02, C-04, C-18 — [selected source statements](../assessment-checks.json) |
| Changed ancestor | RKM-C014: typing_rationale |
| Changed relation neighbor | None in this selected context |
| Excluded blanket sets | GS-RKM-C014 |

Documentary identity is separate from activity, risk identity and real-world values. Comparable interpretation requires the selected method/scale/dimension/basis/context/time or a justified transformation; missing input is not zero. A recorded score does not by itself establish acceptability, and a qualitative uncertainty statement need not contain probability.

Complete source observations are in [contexts.json](../contexts.json). Context SHA-256: `caa62869adb8c3a8dbfcd44962f395051376b7a5f0c51acc8f95a02f011e7959`.

Authored definition SHA-256: `738a7a329e6623c14f2d79d69179a4095a3428b63bf0339702c7f63b8171c77f`.

No formal alignment axiom, new ontology-engine execution or independent expert rating is supplied. Remaining documentary batches, full component qualification and actual publication/readback retain their separate gates. #23 and #78 remain separate.
