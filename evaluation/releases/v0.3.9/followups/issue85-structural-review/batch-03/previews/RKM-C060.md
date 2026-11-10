# Analysis State Term — N3b-3 documentary preview

**Planning preview; not deployed or independently validated.**

## Authored definition, unchanged

A controlled value describing progress of analysis under a specified analysis-state scheme. This is a managed vocabulary resource with scheme-qualified identity, not a bare string.

[Source model 0.3.2](https://github.com/ArazSaieArasi3/riskium/blob/446f412e737a9f456addb2b12c63e867a33b70d3/ontology/0.3.2/riskium-model.json); subdomain D08; stereotype subkind; identity supplier RKM-C014.

Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.

Authored verification status, preserved verbatim: Bounded review and finite tests; native OntoUML and independent semantic validation pending

Later bounded qualification/publication evidence is in the [v0.3.9 receipt](https://github.com/ArazSaieArasi3/riskium/blob/446f412e737a9f456addb2b12c63e867a33b70d3/evaluation/releases/v0.3.9/R2b-outcome.md). Source labels and documentary comparisons are not independent semantic ratings.

## Documentary comparison

**RELATED → RELATED**.

Retain vocabulary-concept context for analysis progress. A value under a declared analysis scheme is not the state of a real-world risk situation or evidence of assessment quality.

| Selected term | Source kind and locator |
|---|---|
| [skos:Concept](https://www.w3.org/TR/2009/REC-skos-reference-20090818/#concepts) | VOCABULARY_CLASS; §3, especially §§3.1 and 3.5.1 |

## Current structural context

R-31 optionally records analysis state in a RecordStateAssertion. Scheme/version and temporal qualification matter; incomplete or absent state information is not silently replaced by a workflow value or an invented completion result.

Source continuity: concept record unchanged=True; direct edges unchanged=True; inherited edges unchanged=True. Ancestor and neighbor changes are reported separately.

| Observation | Source-bound result |
|---|---|
| Inheritance path | G2-052: RKM-C017 → RKM-C014; G2-053: RKM-C019 → RKM-C017; G2-064: RKM-C060 → RKM-C019 |
| Source constraint route | C-05, C-11, C-19 — [selected source statements](../registration-checks.json) |
| Changed ancestor | RKM-C014: typing_rationale |
| Changed relation neighbor | None in this selected context |
| Excluded blanket sets | GS-RKM-C014 |
| Retained GS-RKM-C019 | isDisjoint=False; isComplete=False; CARRIED_FORWARD_NOT_REASSESSED_IN_THIS_PACKET |
| Retained GS-RKM-C017 | isDisjoint=False; isComplete=False; CARRIED_FORWARD_NOT_REASSESSED_IN_THIS_PACKET |

Documentary identity is separate from analytical RiskCase identity and local operational admission. Shared parenthood creates no blanket exclusivity or covering axiom. Vocabulary values, qualified statements and their referents remain distinct; closure and missing authorization do not supply new risk/effectiveness/permission facts.

Complete source observations are in [contexts.json](../contexts.json). Context SHA-256: `e1566f897f9c069b42fe4d83524a565fad609cd1da655f3fa9aa16fb688f93b5`.

Authored definition SHA-256: `91d804902c99c34c924afe49626845c8ca89207838484b4427f2601e31a64e3c`.

No formal alignment axiom, new ontology-engine execution or independent expert rating is supplied. Remaining documentary batches, full component qualification and actual publication/readback retain their separate gates. #23 and #78 remain separate.
