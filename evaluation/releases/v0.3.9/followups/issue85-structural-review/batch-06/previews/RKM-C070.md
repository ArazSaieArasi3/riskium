# Threshold — N3b-6 documentary preview

**Planning preview; not deployed or independently validated.**

## Authored definition, unchanged

A versioned information specification of a context-qualified decision boundary for an indicator or assessment scale, with a comparator, permissible value interpretation and applicability context.

[Source model 0.3.2](https://github.com/ArazSaieArasi3/riskium/blob/36ff7a55becfe206b821fe969fecd5efbcd22149/ontology/0.3.2/riskium-model.json); subdomain D10; stereotype subkind; identity supplier RKM-C014.

Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.

Authored verification status, preserved verbatim: Bounded review and finite tests; native OntoUML and independent semantic validation pending

Later bounded qualification/publication evidence is in the [v0.3.9 receipt](https://github.com/ArazSaieArasi3/riskium/blob/36ff7a55becfe206b821fe969fecd5efbcd22149/evaluation/releases/v0.3.9/R2b-outcome.md). Source labels and documentary comparisons are not independent semantic ratings.

## Documentary comparison

**NO_DIRECT_EQUIVALENT_REVIEWED → CONTRAST**.

Clarify the former scoped-absence label as a contrast in intended role: a DQV measuring standard does not itself specify a comparator-qualified decision boundary. No global absence, class disjointness or exact threshold equivalence is asserted.

| Selected term | Source kind and locator |
|---|---|
| [dqv:Metric](https://www.w3.org/TR/2016/NOTE-vocab-dqv-20161215/#dqv:Metric) | DATASET_QUALITY_PATTERN_CLASS; §4.2 |

## Current structural context

RX-025 and RK2-020 each permit an indicator or scale anchor. C-08 requires at least one supported anchor, with compatible interpretation if both exist; it does not require both. Qualitative boundaries retain scale semantics rather than invented numerical units. RX-027 records selected signal comparison.

Source continuity: concept record unchanged=True; local association/generalization records unchanged=True; inherited edges unchanged=True. Ancestor and neighbor changes are reported separately.

| Observation | Source-bound result |
|---|---|
| Inheritance path | GX-056: RKM-C070 → RKM-C014 |
| Source constraint route | C-03, C-04, C-08, C-13, C-18 — [selected source statements](../evidence-monitoring-checks.json) |
| Changed ancestor | RKM-C014: typing_rationale |
| Changed relation neighbor | None in this selected context |
| Excluded blanket sets | GS-RKM-C014 |

Reference, role participation and evidence-use relationship remain distinct; a citation or provenance link is not proof of claim truth. Observation information and indicator specifications do not create actual risk events. Thresholds use supported indicator/scale semantics, and signals preserve context and uncertainty without inventing missing values.

Complete source observations are in [contexts.json](../contexts.json). Context SHA-256: `bb4d410eddaa8063092a523b6f6617193d0aad6966d2d2928fafaf154720ac5b`.

Authored definition SHA-256: `3abf29196482b00645aeb2af24d8964e25927ddfefa0eecb9266be77e8e7bbf2`.

No formal alignment axiom, new ontology-engine execution or independent expert rating is supplied. Documentary batch accounting is complete; full component qualification and actual publication/readback retain their separate gates. #23 and #78 remain separate.
