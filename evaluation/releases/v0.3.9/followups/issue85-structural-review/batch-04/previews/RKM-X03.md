# Uncertainty Statement — N3b-4 documentary preview

**Planning preview; not deployed or independently validated.**

## Authored definition, unchanged

A managed statement of what is uncertain about a risk case, including assumptions and evidential limitations; it does not imply a numerical probability.

[Source model 0.3.2](https://github.com/ArazSaieArasi3/riskium/blob/8a115ef9c3fb6b0501c6ed9c9fd6b258d358028e/ontology/0.3.2/riskium-model.json); subdomain D05; stereotype subkind; identity supplier RKM-C014.

Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.

Authored verification status, preserved verbatim: Bounded review and finite tests; native OntoUML and independent semantic validation pending

Later bounded qualification/publication evidence is in the [v0.3.9 receipt](https://github.com/ArazSaieArasi3/riskium/blob/8a115ef9c3fb6b0501c6ed9c9fd6b258d358028e/evaluation/releases/v0.3.9/R2b-outcome.md). Source labels and documentary comparisons are not independent semantic ratings.

## Documentary comparison

**RELATED → RELATED**.

Retain the annotation body/target pattern for an uncertainty statement, without importing its serialization contract or treating the statement as a probability distribution.

| Selected term | Source kind and locator |
|---|---|
| [oa:Annotation](https://www.w3.org/TR/2017/REC-annotation-model-20170223/#annotations) | ANNOTATION_RESOURCE_CLASS; §3.1 |

## Current structural context

RX-004 concerns a continuing RiskCase; RK2-012/RK2-013 retain context and its use in assessment information. Revised RiskCase meaning was reviewed. Assumptions and evidential limitations may be qualitative; absence of a probability is not zero uncertainty.

Source continuity: concept record unchanged=True; direct edges unchanged=True; inherited edges unchanged=True. Ancestor and neighbor changes are reported separately.

| Observation | Source-bound result |
|---|---|
| Inheritance path | GX-062: RKM-X03 → RKM-C014 |
| Source constraint route | C-02, C-04, C-16, C-18 — [selected source statements](../assessment-checks.json) |
| Changed ancestor | RKM-C014: typing_rationale |
| Changed relation neighbor | RKM-X01: definition, identity_basis, typing_rationale |
| Excluded blanket sets | GS-RKM-C014 |

Documentary identity is separate from activity, risk identity and real-world values. Comparable interpretation requires the selected method/scale/dimension/basis/context/time or a justified transformation; missing input is not zero. A recorded score does not by itself establish acceptability, and a qualitative uncertainty statement need not contain probability.

Complete source observations are in [contexts.json](../contexts.json). Context SHA-256: `4970ca0e4ac061e95b22e7b1a23dd5f8ccec6566388c748c30f6015aa0359ca6`.

Authored definition SHA-256: `035695e5556206de3d19a53ff0cafb6ed7c5e175633de0a7fd0cffc69a4ccd8a`.

No formal alignment axiom, new ontology-engine execution or independent expert rating is supplied. Remaining documentary batches, full component qualification and actual publication/readback retain their separate gates. #23 and #78 remain separate.
