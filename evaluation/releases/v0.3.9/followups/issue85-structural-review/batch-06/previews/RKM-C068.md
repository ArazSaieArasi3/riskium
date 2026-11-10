# Observation Result — N3b-6 documentary preview

**Planning preview; not deployed or independently validated.**

## Authored definition, unchanged

An information result produced by an observation activity, qualified by subject, time, method and available units.

[Source model 0.3.2](https://github.com/ArazSaieArasi3/riskium/blob/36ff7a55becfe206b821fe969fecd5efbcd22149/ontology/0.3.2/riskium-model.json); subdomain D10; stereotype subkind; identity supplier RKM-C014.

Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.

Authored verification status, preserved verbatim: Bounded review and finite tests; native OntoUML and independent semantic validation pending

Later bounded qualification/publication evidence is in the [v0.3.9 receipt](https://github.com/ArazSaieArasi3/riskium/blob/36ff7a55becfe206b821fe969fecd5efbcd22149/evaluation/releases/v0.3.9/R2b-outcome.md). Source labels and documentary comparisons are not independent semantic ratings.

## Documentary comparison

**RELATED → RELATED**.

Retain SOSA Result as related output context. SOSA also covers actuation and sampling results, while this Riskium concept selects observation information qualified by subject, method, time and available units; no class equivalence or imported restriction is asserted.

| Selected term | Source kind and locator |
|---|---|
| [sosa:Result](https://www.w3.org/TR/2017/REC-vocab-ssn-20171019/#SOSAResult) | SOSA_RESULT_CLASS; §4.7.2.1 |

## Current structural context

RX-022 relates an ObservationActivity to its informational result; RX-023 identifies the indicator and RX-024 the continuing RiskCase. RK2-026 can retain context and RK2-017 connects revisions. The result is neither its activity nor a risk occurrence; a numeric value alone is insufficient for cross-context comparison.

Source continuity: concept record unchanged=True; local association/generalization records unchanged=True; inherited edges unchanged=True. Ancestor and neighbor changes are reported separately.

| Observation | Source-bound result |
|---|---|
| Inheritance path | GX-054: RKM-C068 → RKM-C014 |
| Source constraint route | C-01, C-04, C-05, C-18 — [selected source statements](../evidence-monitoring-checks.json) |
| Changed ancestor | RKM-C014: typing_rationale |
| Changed relation neighbor | RKM-X01: definition, identity_basis, typing_rationale |
| Excluded blanket sets | GS-RKM-C014 |

Reference, role participation and evidence-use relationship remain distinct; a citation or provenance link is not proof of claim truth. Observation information and indicator specifications do not create actual risk events. Thresholds use supported indicator/scale semantics, and signals preserve context and uncertainty without inventing missing values.

Complete source observations are in [contexts.json](../contexts.json). Context SHA-256: `aa4cb25fc2edc45284ba6f503364a9bc4d9901bce8372c4be405f14f217fa76c`.

Authored definition SHA-256: `7b660221341d48f1359461ec7e15b81fcc009585650f24a3f619694437faebdc`.

No formal alignment axiom, new ontology-engine execution or independent expert rating is supplied. Documentary batch accounting is complete; full component qualification and actual publication/readback retain their separate gates. #23 and #78 remain separate.
