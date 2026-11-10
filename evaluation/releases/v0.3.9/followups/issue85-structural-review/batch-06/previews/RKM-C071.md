# Signal — N3b-6 documentary preview

**Planning preview; not deployed or independently validated.**

## Authored definition, unchanged

An information item indicating a potentially relevant change or condition and potentially prompting review; it does not by itself establish a risk event.

[Source model 0.3.2](https://github.com/ArazSaieArasi3/riskium/blob/36ff7a55becfe206b821fe969fecd5efbcd22149/ontology/0.3.2/riskium-model.json); subdomain D10; stereotype subkind; identity supplier RKM-C014.

Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.

Authored verification status, preserved verbatim: Bounded review and finite tests; native OntoUML and independent semantic validation pending

Later bounded qualification/publication evidence is in the [v0.3.9 receipt](https://github.com/ArazSaieArasi3/riskium/blob/36ff7a55becfe206b821fe969fecd5efbcd22149/evaluation/releases/v0.3.9/R2b-outcome.md). Source labels and documentary comparisons are not independent semantic ratings.

## Documentary comparison

**RELATED → RELATED**.

Retain the relationship to observation results without equating every signal with a SOSA Result or an actual risk event. A signal is information selected as potentially relevant to review; its significance requires context.

| Selected term | Source kind and locator |
|---|---|
| [sosa:Result](https://www.w3.org/TR/2017/REC-vocab-ssn-20171019/#SOSAResult) | SOSA_RESULT_CLASS; §4.7.2.1 |

## Current structural context

RX-026 requires supporting observation results in the managed signal profile; RX-027 can identify thresholds and RX-028 can prompt case review. Revised RiskCase meaning was reviewed. Source incomplete material is retained without fabricating observations; neither an alert nor a crossed threshold automatically proves a risk occurrence or cause.

Source continuity: concept record unchanged=True; local association/generalization records unchanged=True; inherited edges unchanged=True. Ancestor and neighbor changes are reported separately.

| Observation | Source-bound result |
|---|---|
| Inheritance path | GX-057: RKM-C071 → RKM-C014 |
| Source constraint route | C-01, C-02, C-08, C-16, C-18 — [selected source statements](../evidence-monitoring-checks.json) |
| Changed ancestor | RKM-C014: typing_rationale |
| Changed relation neighbor | RKM-X01: definition, identity_basis, typing_rationale |
| Excluded blanket sets | GS-RKM-C014 |

Reference, role participation and evidence-use relationship remain distinct; a citation or provenance link is not proof of claim truth. Observation information and indicator specifications do not create actual risk events. Thresholds use supported indicator/scale semantics, and signals preserve context and uncertainty without inventing missing values.

Complete source observations are in [contexts.json](../contexts.json). Context SHA-256: `90f9b3b9a228b1911b13682772b58ed97fe4a36eb8a0cf0945c537d583bbefa3`.

Authored definition SHA-256: `f244b1ed62c670baf57ccb90cbe233adc43a3005f32eb22fab5758392bce7969`.

No formal alignment axiom, new ontology-engine execution or independent expert rating is supplied. Documentary batch accounting is complete; full component qualification and actual publication/readback retain their separate gates. #23 and #78 remain separate.
