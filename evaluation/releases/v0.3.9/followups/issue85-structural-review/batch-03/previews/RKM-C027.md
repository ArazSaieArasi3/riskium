# Intake Channel Term — N3b-3 documentary preview

**Planning preview; not deployed or independently validated.**

## Authored definition, unchanged

A controlled value naming how risk information entered the registration process; it is not a risk source. This is a managed vocabulary resource with scheme-qualified identity, not a bare string.

[Source model 0.3.2](https://github.com/ArazSaieArasi3/riskium/blob/446f412e737a9f456addb2b12c63e867a33b70d3/ontology/0.3.2/riskium-model.json); subdomain D04; stereotype subkind; identity supplier RKM-C014.

Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.

Authored verification status, preserved verbatim: Bounded review and finite tests; native OntoUML and independent semantic validation pending

Later bounded qualification/publication evidence is in the [v0.3.9 receipt](https://github.com/ArazSaieArasi3/riskium/blob/446f412e737a9f456addb2b12c63e867a33b70d3/evaluation/releases/v0.3.9/R2b-outcome.md). Source labels and documentary comparisons are not independent semantic ratings.

## Documentary comparison

**RELATED → RELATED**.

Retain vocabulary-concept context for an intake-channel value. The channel describes how information arrived; it is not a real-world contributor to risk or a universal channel taxonomy.

| Selected term | Source kind and locator |
|---|---|
| [skos:Concept](https://www.w3.org/TR/2009/REC-skos-reference-20090818/#concepts) | VOCABULARY_CLASS; §3, especially §§3.1 and 3.5.1 |

## Current structural context

The path through ClassificationTerm and VocabularyConcept preserves InformationArtifact identity. R-27 records a source-qualified channel; common text neither identifies the vocabulary resource nor resolves a risk source.

Source continuity: concept record unchanged=True; direct edges unchanged=True; inherited edges unchanged=True. Ancestor and neighbor changes are reported separately.

| Observation | Source-bound result |
|---|---|
| Inheritance path | G2-052: RKM-C017 → RKM-C014; G2-053: RKM-C019 → RKM-C017; G2-055: RKM-C027 → RKM-C019 |
| Source constraint route | C-11, C-17 — [selected source statements](../registration-checks.json) |
| Changed ancestor | RKM-C014: typing_rationale |
| Changed relation neighbor | None in this selected context |
| Excluded blanket sets | GS-RKM-C014 |
| Retained GS-RKM-C019 | isDisjoint=False; isComplete=False; CARRIED_FORWARD_NOT_REASSESSED_IN_THIS_PACKET |
| Retained GS-RKM-C017 | isDisjoint=False; isComplete=False; CARRIED_FORWARD_NOT_REASSESSED_IN_THIS_PACKET |

Documentary identity is separate from analytical RiskCase identity and local operational admission. Shared parenthood creates no blanket exclusivity or covering axiom. Vocabulary values, qualified statements and their referents remain distinct; closure and missing authorization do not supply new risk/effectiveness/permission facts.

Complete source observations are in [contexts.json](../contexts.json). Context SHA-256: `92748d0c75959ed2a049d5c02d3afc148f72b2ad61ebf52fc77a0f3192c7a7f0`.

Authored definition SHA-256: `4ff876d9af18db53648db45c5d06ad27c75dae3790719e5f07c56f00e78e9879`.

No formal alignment axiom, new ontology-engine execution or independent expert rating is supplied. Remaining documentary batches, full component qualification and actual publication/readback retain their separate gates. #23 and #78 remain separate.
