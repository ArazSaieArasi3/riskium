# Authorizing Agent Role — N3b-2 documentary preview

**Planning preview; not deployed or independently validated.**

## Authored definition, unchanged

A context-dependent role borne by an agent authorized to approve or issue a specified decision or assignment.

[Source model 0.3.2](https://github.com/ArazSaieArasi3/riskium/blob/706a9f04bf391fa6e098fff615510a28e863c3a9/ontology/0.3.2/riskium-model.json); subdomain D07; stereotype roleMixin; identity supplier None.

Identity basis: Inherits bearer identity; role membership depends on an explicit responsibility or evidential context.

Authored verification status, preserved verbatim: Bounded review and finite tests; native OntoUML and independent semantic validation pending

Later bounded qualification/publication evidence is in the [v0.3.9 receipt](https://github.com/ArazSaieArasi3/riskium/blob/706a9f04bf391fa6e098fff615510a28e863c3a9/evaluation/releases/v0.3.9/R2b-outcome.md). Source labels and documentary comparisons are not independent semantic ratings.

## Documentary comparison

**ANALOGY → ANALOGY**.

Retain the bounded analogy. An authorizing role requires a supported authority context; a provenance function or activity participation alone does not establish approval authority.

| Selected term | Source kind and locator |
|---|---|
| [prov:Role](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Role) | External comparison: PROVENANCE_CLASS; §4.3, Role |
| [prov:Association](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Association) | External comparison: PROVENANCE_CLASS; §4.3, Association |
| [OntoUML specification: RoleMixin](https://ontouml.readthedocs.io/en/latest/classes/nonsortals/rolemixin/index.html#definition) | Modeling foundation: MODELING_FOUNDATION; Definition and constraints C1-C2 |

## Current structural context

The abstract roleMixin aggregates person and organization bearers without supplying identity. R-57 supplies the selected mandatory dependency. Responsible and authorizing participation are not globally exclusive merely because they share Agent as a parent.

Source continuity: concept record unchanged=True; direct edges unchanged=True; inherited edges unchanged=True. Ancestor and neighbor changes are reported separately.

| Observation | Source-bound result |
|---|---|
| Inheritance path | G-23: RKM-C054 → RKM-C047 |
| Ancestor identity providers | None; identity is not supplied by this non-sortal. |
| Inherited mandatory mediation | R-57: relators per bearer 1..* |
| Changed inheritance endpoint | None in this selected direct context. |
| Changed ancestor | None in this selected context |
| Changed relation neighbor | None in this selected context |
| Excluded blanket sets | GS-RKM-C047 |
| Retained GS-RKM-C054 | isDisjoint=True; isComplete=False; CARRIED_FORWARD_NOT_REASSESSED_IN_THIS_PACKET |
| Retained GS-AgentKinds | isDisjoint=True; isComplete=False; EXPLICITLY_RETAINED_BEARER_KIND_CRITERION |

Bearer-kind exclusivity is separate from contextual participation. Shared parenthood does not create a blanket role set; different contextual roles do not create a new bearer identity. A responsibility statement or provenance function alone does not establish actual authorization, and local operational admission does not determine analytical RiskCase existence.

Complete source observations are in [contexts.json](../contexts.json). Context SHA-256: `6457ead085475a9ee8a46f050f3bd9cbf600fc39814c24bfc899ed20407d3ae5`.

Authored definition SHA-256: `ef746bc0466bcdfa7ca04721df87dbd383dd1ab5282b0a1a743a55d54e169c26`.

No formal alignment axiom, new ontology-engine execution or independent expert rating is supplied. Remaining documentary batches, full component qualification and actual publication/readback retain their separate gates. #23 and #78 remain separate.
