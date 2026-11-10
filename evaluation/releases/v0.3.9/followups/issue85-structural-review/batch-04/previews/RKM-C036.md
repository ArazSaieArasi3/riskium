# Assessment Scale — N3b-4 documentary preview

**Planning preview; not deployed or independently validated.**

## Authored definition, unchanged

A governed scale specification defining permissible values or ordered levels for a specified assessment dimension.

[Source model 0.3.2](https://github.com/ArazSaieArasi3/riskium/blob/8a115ef9c3fb6b0501c6ed9c9fd6b258d358028e/ontology/0.3.2/riskium-model.json); subdomain D05; stereotype subkind; identity supplier RKM-C014.

Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.

Authored verification status, preserved verbatim: Bounded review and finite tests; native OntoUML and independent semantic validation pending

Later bounded qualification/publication evidence is in the [v0.3.9 receipt](https://github.com/ArazSaieArasi3/riskium/blob/8a115ef9c3fb6b0501c6ed9c9fd6b258d358028e/evaluation/releases/v0.3.9/R2b-outcome.md). Source labels and documentary comparisons are not independent semantic ratings.

## Documentary comparison

**ANALOGY → ANALOGY**.

Retain NIST Table F-2 as an example of an interpreted severity scale. Its security-specific levels and numerical codes are not universal Riskium scales or probabilities and are not adopted as a mandatory scheme.

| Selected term | Source kind and locator |
|---|---|
| [Assessment scale: vulnerability severity](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf#page=78) | SECURITY_SCALE_EXAMPLE; Appendix F, Table F-2, printed F-2, PDF page 78 |

## Current structural context

RK2-019 declares one dimension, R-16 relates level resources to their scale, and version references qualify interpretation. Equal codes or labels across scales do not license ranking or arithmetic; qualitative values remain possible.

Source continuity: concept record unchanged=True; direct edges unchanged=True; inherited edges unchanged=True. Ancestor and neighbor changes are reported separately.

| Observation | Source-bound result |
|---|---|
| Inheritance path | G-12: RKM-C036 → RKM-C014 |
| Source constraint route | C-04, C-11, C-13, C-18 — [selected source statements](../assessment-checks.json) |
| Changed ancestor | RKM-C014: typing_rationale |
| Changed relation neighbor | None in this selected context |
| Excluded blanket sets | GS-RKM-C014 |

Documentary identity is separate from activity, risk identity and real-world values. Comparable interpretation requires the selected method/scale/dimension/basis/context/time or a justified transformation; missing input is not zero. A recorded score does not by itself establish acceptability, and a qualitative uncertainty statement need not contain probability.

Complete source observations are in [contexts.json](../contexts.json). Context SHA-256: `4b42634fcf76f9d5be95cd728599bbcc38f637f32f31b1b3f67643b372313d00`.

Authored definition SHA-256: `a705563c110bd1b41e33f653c4443a681ae162ebb3fdbd24c9cf403d708c66db`.

No formal alignment axiom, new ontology-engine execution or independent expert rating is supplied. Remaining documentary batches, full component qualification and actual publication/readback retain their separate gates. #23 and #78 remain separate.
