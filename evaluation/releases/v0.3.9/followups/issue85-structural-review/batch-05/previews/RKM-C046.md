# Plan Role Term — N3b-5 documentary preview

**Planning preview; not deployed or independently validated.**

## Authored definition, unchanged

A controlled value describing the role of a plan, such as primary response or contingency. This is a managed vocabulary resource with scheme-qualified identity, not a bare string.

[Source model 0.3.2](https://github.com/ArazSaieArasi3/riskium/blob/64ebfa6c9bec92184f5671cb6d5aef6397b0a9e1/ontology/0.3.2/riskium-model.json); subdomain D06; stereotype subkind; identity supplier RKM-C014.

Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.

Authored verification status, preserved verbatim: Bounded review and finite tests; native OntoUML and independent semantic validation pending

Later bounded qualification/publication evidence is in the [v0.3.9 receipt](https://github.com/ArazSaieArasi3/riskium/blob/64ebfa6c9bec92184f5671cb6d5aef6397b0a9e1/evaluation/releases/v0.3.9/R2b-outcome.md). Source labels and documentary comparisons are not independent semantic ratings.

## Documentary comparison

**RELATED → RELATED**.

Retain vocabulary-resource context for primary-response, contingency or other plan functions. SKOS does not define those local functions, and a PlanRoleTerm is not an OntoUML agent role or performance of a response.

| Selected term | Source kind and locator |
|---|---|
| [skos:Concept](https://www.w3.org/TR/2009/REC-skos-reference-20090818/#concepts) | VOCABULARY_CLASS; §3, especially §§3.1 and 3.5.1 |

## Current structural context

R-62 assigns the chosen function to a plan specification. Scheme-qualified identity is inherited through ClassificationTerm/VocabularyConcept; the retained incomplete/non-disjoint groups are carried policy, not a new semantic-partition approval.

Source continuity: concept record unchanged=True; direct edges unchanged=True; inherited edges unchanged=True. Ancestor and neighbor changes are reported separately.

| Observation | Source-bound result |
|---|---|
| Inheritance path | G2-052: RKM-C017 → RKM-C014; G2-053: RKM-C019 → RKM-C017; G2-062: RKM-C046 → RKM-C019 |
| Source constraint route | C-02, C-11, C-17 — [selected source statements](../treatment-policy-checks.json) |
| Changed ancestor | RKM-C014: typing_rationale |
| Changed relation neighbor | None in this selected context |
| Excluded blanket sets | GS-RKM-C014 |
| Retained GS-RKM-C019 | isDisjoint=False; isComplete=False; CARRIED_FORWARD_NOT_REASSESSED_IN_THIS_PACKET |
| Retained GS-RKM-C017 | isDisjoint=False; isComplete=False; CARRIED_FORWARD_NOT_REASSESSED_IN_THIS_PACKET |

Recorded choices, plans and references remain information; actual activity, realized controls and effectiveness need their own support. Vocabulary labels do not establish resource identity, authority or cross-framework equivalence. Source-qualified appetite/tolerance statements and their contexts are preserved without importing unseen normative terms.

Complete source observations are in [contexts.json](../contexts.json). Context SHA-256: `3680570c21c4894e07231aa88b8096074a429c282cd4873311ba121ba31f6e3c`.

Authored definition SHA-256: `00f108d06e107135b1818225321282130e4b4135427ed2e1b627fe748dc21304`.

No formal alignment axiom, new ontology-engine execution or independent expert rating is supplied. Remaining documentary batches, full component qualification and actual publication/readback retain their separate gates. #23 and #78 remain separate.
