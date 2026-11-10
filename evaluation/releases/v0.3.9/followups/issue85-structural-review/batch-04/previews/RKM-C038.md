# Assessment Scale Level — N3b-4 documentary preview

**Planning preview; not deployed or independently validated.**

## Authored definition, unchanged

A managed vocabulary resource specifying a permissible value or category on an identified assessment scale version. It denotes a level; it is not a measured value occurrence or a bare lexical label.

[Source model 0.3.2](https://github.com/ArazSaieArasi3/riskium/blob/8a115ef9c3fb6b0501c6ed9c9fd6b258d358028e/ontology/0.3.2/riskium-model.json); subdomain D05; stereotype subkind; identity supplier RKM-C014.

Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.

Authored verification status, preserved verbatim: Bounded review and finite tests; native OntoUML and independent semantic validation pending

Later bounded qualification/publication evidence is in the [v0.3.9 receipt](https://github.com/ArazSaieArasi3/riskium/blob/8a115ef9c3fb6b0501c6ed9c9fd6b258d358028e/evaluation/releases/v0.3.9/R2b-outcome.md). Source labels and documentary comparisons are not independent semantic ratings.

## Documentary comparison

**RELATED → RELATED**.

Retain the SKOS distinction between an identified vocabulary resource and its lexical label. A level resource is not a value occurrence; this does not prohibit SKOS dual typing in general or adopt an OWL alignment.

| Selected term | Source kind and locator |
|---|---|
| [skos:Concept](https://www.w3.org/TR/2009/REC-skos-reference-20090818/#concepts) | VOCABULARY_CLASS; §3, especially §§3.1 and 3.5.1 |
| [Lexical labels](https://www.w3.org/TR/2009/REC-skos-reference-20090818/#labels) | LEXICAL_LABEL_PROPERTY_FAMILY; §5.1 |

## Current structural context

The VocabularyConcept ancestry preserves documentary identity; R-16 assigns one scale and R-15 selects a level for a result. C-13 also requires the selected level to match the scale version and dimension; a matching label alone is insufficient.

Source continuity: concept record unchanged=True; direct edges unchanged=True; inherited edges unchanged=True. Ancestor and neighbor changes are reported separately.

| Observation | Source-bound result |
|---|---|
| Inheritance path | G2-052: RKM-C017 → RKM-C014; G2-058: RKM-C038 → RKM-C017 |
| Source constraint route | C-11, C-13, C-18 — [selected source statements](../assessment-checks.json) |
| Changed ancestor | RKM-C014: typing_rationale |
| Changed relation neighbor | None in this selected context |
| Excluded blanket sets | GS-RKM-C014 |
| Retained GS-RKM-C017 | isDisjoint=False; isComplete=False; CARRIED_FORWARD_NOT_REASSESSED_IN_THIS_PACKET |

Documentary identity is separate from activity, risk identity and real-world values. Comparable interpretation requires the selected method/scale/dimension/basis/context/time or a justified transformation; missing input is not zero. A recorded score does not by itself establish acceptability, and a qualitative uncertainty statement need not contain probability.

Complete source observations are in [contexts.json](../contexts.json). Context SHA-256: `cf7c566b17c40487856bae842edba37531c9563bb7225de72f2d284b6b6fac93`.

Authored definition SHA-256: `f7b3438be17f79ad27670ad6247f69c97dfff22698bbdc74e66087e2b57230d9`.

No formal alignment axiom, new ontology-engine execution or independent expert rating is supplied. Remaining documentary batches, full component qualification and actual publication/readback retain their separate gates. #23 and #78 remain separate.
