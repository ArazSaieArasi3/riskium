# Authorizing Person — N3b-2 documentary preview

**Planning preview; not deployed or independently validated.**

## Authored definition, unchanged

A person bearing an authorizing-agent role in a specified context.

[Source model 0.3.2](https://github.com/ArazSaieArasi3/riskium/blob/706a9f04bf391fa6e098fff615510a28e863c3a9/ontology/0.3.2/riskium-model.json); subdomain D07; stereotype role; identity supplier RKM-C048.

Identity basis: Inherits bearer identity; role membership depends on an explicit responsibility or evidential context.

Authored verification status, preserved verbatim: Bounded review and finite tests; native OntoUML and independent semantic validation pending

Later bounded qualification/publication evidence is in the [v0.3.9 receipt](https://github.com/ArazSaieArasi3/riskium/blob/706a9f04bf391fa6e098fff615510a28e863c3a9/evaluation/releases/v0.3.9/R2b-outcome.md). Source labels and documentary comparisons are not independent semantic ratings.

## Documentary comparison

**ANALOGY → ANALOGY**.

Retain the analogy while separating human identity from supported approval authority. A provenance role label supplies neither a mandate nor a decision-specific authorization policy.

| Selected term | Source kind and locator |
|---|---|
| [prov:Person](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Person) | External comparison: PROVENANCE_CLASS; §4.2, Person |
| [prov:Role](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Role) | External comparison: PROVENANCE_CLASS; §4.3, Role |
| [OntoUML specification: Role](https://ontouml.readthedocs.io/en/latest/classes/sortals/role/index.html#definition) | Modeling foundation: MODELING_FOUNDATION; Definition and constraints C1-C2 |

## Current structural context

G-28 preserves Person identity, G-29 supplies the authorizing-role path and R-57 is inherited. The non-disjoint Person sibling policy permits different contextual roles without asserting that one person fills both distinct participants of one mandate.

Source continuity: concept record unchanged=True; direct edges unchanged=True; inherited edges unchanged=True. Ancestor and neighbor changes are reported separately.

| Observation | Source-bound result |
|---|---|
| Inheritance path | G-20: RKM-C048 → RKM-C047; G-23: RKM-C054 → RKM-C047; G-28: RKM-C057 → RKM-C048; G-29: RKM-C057 → RKM-C054 |
| Ancestor identity providers | RKM-C048 |
| Inherited mandatory mediation | R-57: relators per bearer 1..* |
| Changed inheritance endpoint | RKM-C048: typing_rationale |
| Changed ancestor | RKM-C048: typing_rationale |
| Changed relation neighbor | None in this selected context |
| Excluded blanket sets | GS-RKM-C047 |
| Retained GS-RKM-C048 | isDisjoint=False; isComplete=False; CARRIED_FORWARD_NOT_REASSESSED_IN_THIS_PACKET |
| Retained GS-RKM-C054 | isDisjoint=True; isComplete=False; CARRIED_FORWARD_NOT_REASSESSED_IN_THIS_PACKET |
| Retained GS-AgentKinds | isDisjoint=True; isComplete=False; EXPLICITLY_RETAINED_BEARER_KIND_CRITERION |

Bearer-kind exclusivity is separate from contextual participation. Shared parenthood does not create a blanket role set; different contextual roles do not create a new bearer identity. A responsibility statement or provenance function alone does not establish actual authorization, and local operational admission does not determine analytical RiskCase existence.

Complete source observations are in [contexts.json](../contexts.json). Context SHA-256: `6b165ff08db3861612be94444c6d61eddfc70b708608b6be3c5543adb1a4bf49`.

Authored definition SHA-256: `72f3421abcdca41a7a7e70288a17e310fd1c6b1e852f09ed1c7f9e12f916d007`.

No formal alignment axiom, new ontology-engine execution or independent expert rating is supplied. Remaining documentary batches, full component qualification and actual publication/readback retain their separate gates. #23 and #78 remain separate.
