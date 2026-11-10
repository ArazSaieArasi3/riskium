# Assessment Dimension — N3b-4 documentary preview

**Planning preview; not deployed or independently validated.**

## Authored definition, unchanged

A managed vocabulary resource specifying an assessment aspect, such as likelihood or consequence severity. The vocabulary item, the aspect denoted and its measured or judged value remain distinct.

[Source model 0.3.2](https://github.com/ArazSaieArasi3/riskium/blob/8a115ef9c3fb6b0501c6ed9c9fd6b258d358028e/ontology/0.3.2/riskium-model.json); subdomain D05; stereotype subkind; identity supplier RKM-C014.

Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.

Authored verification status, preserved verbatim: Bounded review and finite tests; native OntoUML and independent semantic validation pending

Later bounded qualification/publication evidence is in the [v0.3.9 receipt](https://github.com/ArazSaieArasi3/riskium/blob/8a115ef9c3fb6b0501c6ed9c9fd6b258d358028e/evaluation/releases/v0.3.9/R2b-outcome.md). Source labels and documentary comparisons are not independent semantic ratings.

## Documentary comparison

**ANALOGY → ANALOGY**.

Retain the DQV dimension/metric separation as a pattern analogy within its dataset-quality scope. Riskium uses a managed term for a risk-assessment aspect, distinct from the aspect denoted and the judged result.

| Selected term | Source kind and locator |
|---|---|
| [dqv:Dimension](https://www.w3.org/TR/2016/NOTE-vocab-dqv-20161215/#dqv:Dimension) | DATASET_QUALITY_PATTERN_CLASS; §4.3 |

## Current structural context

The path through ClassificationTerm/VocabularyConcept preserves scheme-qualified identity. R-48, RK2-018 and RK2-019 connect result, method and scale to the dimension. DQV metric requirements are not automatically added to the Riskium profile.

Source continuity: concept record unchanged=True; direct edges unchanged=True; inherited edges unchanged=True. Ancestor and neighbor changes are reported separately.

| Observation | Source-bound result |
|---|---|
| Inheritance path | G2-052: RKM-C017 → RKM-C014; G2-059: RKM-C039 → RKM-C017 |
| Source constraint route | C-04, C-11, C-13 — [selected source statements](../assessment-checks.json) |
| Changed ancestor | RKM-C014: typing_rationale |
| Changed relation neighbor | None in this selected context |
| Excluded blanket sets | GS-RKM-C014 |
| Retained GS-RKM-C017 | isDisjoint=False; isComplete=False; CARRIED_FORWARD_NOT_REASSESSED_IN_THIS_PACKET |

Documentary identity is separate from activity, risk identity and real-world values. Comparable interpretation requires the selected method/scale/dimension/basis/context/time or a justified transformation; missing input is not zero. A recorded score does not by itself establish acceptability, and a qualitative uncertainty statement need not contain probability.

Complete source observations are in [contexts.json](../contexts.json). Context SHA-256: `0eca95999a0a4d59ee6a0ed470c6cb3c4bafa0512944beb2e51bce31895228fc`.

Authored definition SHA-256: `07982a61e14b975e44154a54191780ec0ac6a8eb211430ddfa2ff6136dd163ea`.

No formal alignment axiom, new ontology-engine execution or independent expert rating is supplied. Remaining documentary batches, full component qualification and actual publication/readback retain their separate gates. #23 and #78 remain separate.
