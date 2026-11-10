# Objective Reference — N3b-5 documentary preview

**Planning preview; not deployed or independently validated.**

## Authored definition, unchanged

A managed information item identifying an objective in its source context, without asserting that the information item is the objective.

[Source model 0.3.2](https://github.com/ArazSaieArasi3/riskium/blob/64ebfa6c9bec92184f5671cb6d5aef6397b0a9e1/ontology/0.3.2/riskium-model.json); subdomain D11; stereotype subkind; identity supplier RKM-C014.

Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.

Authored verification status, preserved verbatim: Bounded review and finite tests; native OntoUML and independent semantic validation pending

Later bounded qualification/publication evidence is in the [v0.3.9 receipt](https://github.com/ArazSaieArasi3/riskium/blob/64ebfa6c9bec92184f5671cb6d5aef6397b0a9e1/evaluation/releases/v0.3.9/R2b-outcome.md). Source labels and documentary comparisons are not independent semantic ratings.

## Documentary comparison

**CONTRAST → CONTRAST**.

Retain the distinction between an informational reference and the objective it identifies. Generic PROV Entity has broad provenance scope and does not alone determine referent identity or objective achievement.

| Selected term | Source kind and locator |
|---|---|
| [prov:Entity](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Entity) | PROVENANCE_CLASS; §4.1, Entity |

## Current structural context

RX-003 connects analytical RiskCase to objective references; RK2-011 allows context-specific references. Revised RiskCase meaning was reviewed. The reference can identify source-context objectives without importing an entire organization ontology or asserting that the objective has been achieved.

Source continuity: concept record unchanged=True; direct edges unchanged=True; inherited edges unchanged=True. Ancestor and neighbor changes are reported separately.

| Observation | Source-bound result |
|---|---|
| Inheritance path | GX-061: RKM-X02 → RKM-C014 |
| Source constraint route | C-01, C-02, C-16, C-17 — [selected source statements](../treatment-policy-checks.json) |
| Changed ancestor | RKM-C014: typing_rationale |
| Changed relation neighbor | RKM-X01: definition, identity_basis, typing_rationale |
| Excluded blanket sets | GS-RKM-C014 |

Recorded choices, plans and references remain information; actual activity, realized controls and effectiveness need their own support. Vocabulary labels do not establish resource identity, authority or cross-framework equivalence. Source-qualified appetite/tolerance statements and their contexts are preserved without importing unseen normative terms.

Complete source observations are in [contexts.json](../contexts.json). Context SHA-256: `98898062c789999f89cf5b6ffb4908a57a0565a3a3f26ba24ea5498334181f10`.

Authored definition SHA-256: `9f5fc6f5737c13985ea824e8f9ea10cb0cd5daeee41ff53bf27037b88bbad27f`.

No formal alignment axiom, new ontology-engine execution or independent expert rating is supplied. Remaining documentary batches, full component qualification and actual publication/readback retain their separate gates. #23 and #78 remain separate.
