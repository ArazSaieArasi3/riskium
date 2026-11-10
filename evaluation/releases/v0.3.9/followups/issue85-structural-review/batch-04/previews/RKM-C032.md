# Assessment Information — N3b-4 documentary preview

**Planning preview; not deployed or independently validated.**

## Authored definition, unchanged

A managed information artifact documenting an assessment and its scope, basis, methods, time context, participants and results. It is distinct from performing that assessment.

[Source model 0.3.2](https://github.com/ArazSaieArasi3/riskium/blob/8a115ef9c3fb6b0501c6ed9c9fd6b258d358028e/ontology/0.3.2/riskium-model.json); subdomain D05; stereotype subkind; identity supplier RKM-C014.

Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.

Authored verification status, preserved verbatim: Bounded review and finite tests; native OntoUML and independent semantic validation pending

Later bounded qualification/publication evidence is in the [v0.3.9 receipt](https://github.com/ArazSaieArasi3/riskium/blob/8a115ef9c3fb6b0501c6ed9c9fd6b258d358028e/evaluation/releases/v0.3.9/R2b-outcome.md). Source labels and documentary comparisons are not independent semantic ratings.

## Documentary comparison

**ANALOGY → ANALOGY**.

Retain the NIST security-report comparison as a documentary precedent. It describes an output of assessment, not the assessment activity or a universal enterprise/ecosystem report template.

| Selected term | Source kind and locator |
|---|---|
| [Risk Assessment Report](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf#page=59) | SECURITY_DOCUMENTARY_REPORT; Appendix B, printed B-9, PDF page 59 |

## Current structural context

R-11 targets the continuing RiskCase; R-12 records basis and R-13/R-17 allow dimensional and score outputs. RX-014 pins context version, while optional method links are completed under the selected analytical task. Revised RiskCase and ArtifactVersion neighbors were reviewed.

Source continuity: concept record unchanged=True; direct edges unchanged=True; inherited edges unchanged=True. Ancestor and neighbor changes are reported separately.

| Observation | Source-bound result |
|---|---|
| Inheritance path | G-08: RKM-C032 → RKM-C014 |
| Source constraint route | C-01, C-04, C-16, C-18, C-25 — [selected source statements](../assessment-checks.json) |
| Changed ancestor | RKM-C014: typing_rationale |
| Changed relation neighbor | RKM-C015: typing_rationale; RKM-X01: definition, identity_basis, typing_rationale |
| Excluded blanket sets | GS-RKM-C014 |

Documentary identity is separate from activity, risk identity and real-world values. Comparable interpretation requires the selected method/scale/dimension/basis/context/time or a justified transformation; missing input is not zero. A recorded score does not by itself establish acceptability, and a qualitative uncertainty statement need not contain probability.

Complete source observations are in [contexts.json](../contexts.json). Context SHA-256: `48a9f52516fb833f6ddc8d3583c9aa14d537ef8493f2c0b1caf66acfba4ae1dc`.

Authored definition SHA-256: `d60b3c178be4eebfb834479130fa22afa7e2e354e23b983bf2ab71f95de7df4c`.

No formal alignment axiom, new ontology-engine execution or independent expert rating is supplied. Remaining documentary batches, full component qualification and actual publication/readback retain their separate gates. #23 and #78 remain separate.
