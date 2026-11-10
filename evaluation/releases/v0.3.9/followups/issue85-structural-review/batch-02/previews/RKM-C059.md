# Responsibility Role Term — N3b-2 documentary preview

**Planning preview; not deployed or independently validated.**

## Authored definition, unchanged

A controlled value identifying the kind of responsibility or authority assigned. This is a managed vocabulary resource with scheme-qualified identity, not a bare string.

[Source model 0.3.2](https://github.com/ArazSaieArasi3/riskium/blob/706a9f04bf391fa6e098fff615510a28e863c3a9/ontology/0.3.2/riskium-model.json); subdomain D07; stereotype subkind; identity supplier RKM-C014.

Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.

Authored verification status, preserved verbatim: Bounded review and finite tests; native OntoUML and independent semantic validation pending

Later bounded qualification/publication evidence is in the [v0.3.9 receipt](https://github.com/ArazSaieArasi3/riskium/blob/706a9f04bf391fa6e098fff615510a28e863c3a9/evaluation/releases/v0.3.9/R2b-outcome.md). Source labels and documentary comparisons are not independent semantic ratings.

## Documentary comparison

**RELATED → RELATED**.

Retain vocabulary-concept/function context. The controlled term denotes a responsibility or authority kind; selecting the term does not instantiate the actual role or the mandate grounding it.

| Selected term | Source kind and locator |
|---|---|
| [skos:Concept](https://www.w3.org/TR/2009/REC-skos-reference-20090818/#concepts) | External comparison: VOCABULARY_CLASS; §3, especially §§3.1 and 3.5.1 |
| [prov:Role](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Role) | External comparison: PROVENANCE_CLASS; §4.3, Role |

## Current structural context

The path through ClassificationTerm and VocabularyConcept preserves InformationArtifact identity. R-54 records an assignment's selected term and R-59 a mandate's term; lexical equality alone establishes neither mandate identity nor actual authorization.

Source continuity: concept record unchanged=True; direct edges unchanged=True; inherited edges unchanged=True. Ancestor and neighbor changes are reported separately.

| Observation | Source-bound result |
|---|---|
| Inheritance path | G2-052: RKM-C017 → RKM-C014; G2-053: RKM-C019 → RKM-C017; G2-063: RKM-C059 → RKM-C019 |
| Ancestor identity providers | RKM-C014 |
| Inherited mandatory mediation | Not asserted for this documentary/category type. |
| Changed inheritance endpoint | None in this selected direct context. |
| Changed ancestor | RKM-C014: typing_rationale |
| Changed relation neighbor | None in this selected context |
| Excluded blanket sets | GS-RKM-C014 |
| Retained GS-RKM-C019 | isDisjoint=False; isComplete=False; CARRIED_FORWARD_NOT_REASSESSED_IN_THIS_PACKET |
| Retained GS-RKM-C017 | isDisjoint=False; isComplete=False; CARRIED_FORWARD_NOT_REASSESSED_IN_THIS_PACKET |

Bearer-kind exclusivity is separate from contextual participation. Shared parenthood does not create a blanket role set; different contextual roles do not create a new bearer identity. A responsibility statement or provenance function alone does not establish actual authorization, and local operational admission does not determine analytical RiskCase existence.

Complete source observations are in [contexts.json](../contexts.json). Context SHA-256: `097ba7479f1af93e964abfa1a6cdf662b95bb62f819164918e4ba7a8c23f88de`.

Authored definition SHA-256: `5d60cf57ae684b2ba39d85432b90ffd56bba53a2e282b477b229b85d7b454094`.

No formal alignment axiom, new ontology-engine execution or independent expert rating is supplied. Remaining documentary batches, full component qualification and actual publication/readback retain their separate gates. #23 and #78 remain separate.
