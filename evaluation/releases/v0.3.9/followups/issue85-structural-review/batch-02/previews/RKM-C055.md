# Responsible Person — N3b-2 documentary preview

**Planning preview; not deployed or independently validated.**

## Authored definition, unchanged

A person bearing a responsible-agent role in a specified assignment context.

[Source model 0.3.2](https://github.com/ArazSaieArasi3/riskium/blob/706a9f04bf391fa6e098fff615510a28e863c3a9/ontology/0.3.2/riskium-model.json); subdomain D07; stereotype role; identity supplier RKM-C048.

Identity basis: Inherits bearer identity; role membership depends on an explicit responsibility or evidential context.

Authored verification status, preserved verbatim: Bounded review and finite tests; native OntoUML and independent semantic validation pending

Later bounded qualification/publication evidence is in the [v0.3.9 receipt](https://github.com/ArazSaieArasi3/riskium/blob/706a9f04bf391fa6e098fff615510a28e863c3a9/evaluation/releases/v0.3.9/R2b-outcome.md). Source labels and documentary comparisons are not independent semantic ratings.

## Documentary comparison

**ANALOGY → ANALOGY**.

Retain the person/function analogy while preserving the assigned responsible-person role as a contextual participation of the same human bearer.

| Selected term | Source kind and locator |
|---|---|
| [prov:Person](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Person) | External comparison: PROVENANCE_CLASS; §4.2, Person |
| [prov:Role](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Role) | External comparison: PROVENANCE_CLASS; §4.3, Role |
| [OntoUML specification: Role](https://ontouml.readthedocs.io/en/latest/classes/sortals/role/index.html#definition) | Modeling foundation: MODELING_FOUNDATION; Definition and constraints C1-C2 |

## Current structural context

G-24 provides the sole inherited identity supplier Person; G-25 supplies the ResponsibleAgentRole path and inherited R-56 mediation. The same human can bear different roles across contexts without being duplicated or merged with an organization.

Source continuity: concept record unchanged=True; direct edges unchanged=True; inherited edges unchanged=True. Ancestor and neighbor changes are reported separately.

| Observation | Source-bound result |
|---|---|
| Inheritance path | G-20: RKM-C048 → RKM-C047; G-22: RKM-C053 → RKM-C047; G-24: RKM-C055 → RKM-C048; G-25: RKM-C055 → RKM-C053 |
| Ancestor identity providers | RKM-C048 |
| Inherited mandatory mediation | R-56: relators per bearer 1..* |
| Changed inheritance endpoint | RKM-C048: typing_rationale |
| Changed ancestor | RKM-C048: typing_rationale |
| Changed relation neighbor | None in this selected context |
| Excluded blanket sets | GS-RKM-C047 |
| Retained GS-RKM-C048 | isDisjoint=False; isComplete=False; CARRIED_FORWARD_NOT_REASSESSED_IN_THIS_PACKET |
| Retained GS-RKM-C053 | isDisjoint=True; isComplete=False; CARRIED_FORWARD_NOT_REASSESSED_IN_THIS_PACKET |
| Retained GS-AgentKinds | isDisjoint=True; isComplete=False; EXPLICITLY_RETAINED_BEARER_KIND_CRITERION |

Bearer-kind exclusivity is separate from contextual participation. Shared parenthood does not create a blanket role set; different contextual roles do not create a new bearer identity. A responsibility statement or provenance function alone does not establish actual authorization, and local operational admission does not determine analytical RiskCase existence.

Complete source observations are in [contexts.json](../contexts.json). Context SHA-256: `6d10589e255e97c19c492fdf5157bee18b12489e172f2fe7f12646149a0d4694`.

Authored definition SHA-256: `61f43224df609951279875db88159a78bf4c1aa7aeb09f04f1eef8dae2a649af`.

No formal alignment axiom, new ontology-engine execution or independent expert rating is supplied. Remaining documentary batches, full component qualification and actual publication/readback retain their separate gates. #23 and #78 remain separate.
