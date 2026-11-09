# Candidate generalization-set policy

Candidate **0.3.2-case.1**; not the published current dictionary. Source SHA-256: `e98a63b286441c80fc10a9644804d64fc2b611e906b2d27cf3d72f3ebd72cfa8`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

Emit only explicitly listed retained sets; common parenthood is not a set-creation rule.

## Explicitly retained sets

### GS-RKM-C015

Parent: [Artifact Version](RKM-C015.md); disjoint: `false`; complete: `false`.

Existing reviewed set policy retained; its broader semantic review remains separate.

No blanket exclusivity or covering constraint is imposed on this sibling group.

Members: `G-19`, `GX-051`.

Criterion status: `CARRIED_FORWARD_NOT_REASSESSED_IN_THIS_PACKET`.

### GS-RKM-C048

Parent: [Person](RKM-C048.md); disjoint: `false`; complete: `false`.

Existing reviewed set policy retained; its broader semantic review remains separate.

No blanket exclusivity or covering constraint is imposed on this sibling group.

Members: `G-24`, `G-28`.

Criterion status: `CARRIED_FORWARD_NOT_REASSESSED_IN_THIS_PACKET`.

### GS-RKM-C053

Parent: [Responsible Agent Role](RKM-C053.md); disjoint: `true`; complete: `false`.

Existing reviewed set policy retained; its broader semantic review remains separate.

The current person and organization role specializations inherit distinct human/social-entity identity; other bearer kinds are not ruled out.

Members: `G-25`, `G-27`.

Criterion status: `CARRIED_FORWARD_NOT_REASSESSED_IN_THIS_PACKET`.

### GS-RKM-C049

Parent: [Organization](RKM-C049.md); disjoint: `false`; complete: `false`.

Existing reviewed set policy retained; its broader semantic review remains separate.

No blanket exclusivity or covering constraint is imposed on this sibling group.

Members: `G-26`, `G-30`.

Criterion status: `CARRIED_FORWARD_NOT_REASSESSED_IN_THIS_PACKET`.

### GS-RKM-C054

Parent: [Authorizing Agent Role](RKM-C054.md); disjoint: `true`; complete: `false`.

Existing reviewed set policy retained; its broader semantic review remains separate.

The current person and organization role specializations inherit distinct human/social-entity identity; other bearer kinds are not ruled out.

Members: `G-29`, `G-31`.

Criterion status: `CARRIED_FORWARD_NOT_REASSESSED_IN_THIS_PACKET`.

### GS-RKM-C019

Parent: [Classification Term](RKM-C019.md); disjoint: `false`; complete: `false`.

Existing reviewed set policy retained; its broader semantic review remains separate.

No blanket exclusivity or covering constraint is imposed on this sibling group.

Members: `G2-050`, `G2-055`, `G2-056`, `G2-057`, `G2-060`, `G2-061`, `G2-062`, `G2-063`, `G2-064`, `G2-065`.

Criterion status: `CARRIED_FORWARD_NOT_REASSESSED_IN_THIS_PACKET`.

### GS-RKM-C017

Parent: [Vocabulary Concept](RKM-C017.md); disjoint: `false`; complete: `false`.

Existing reviewed set policy retained; its broader semantic review remains separate.

No blanket exclusivity or covering constraint is imposed on this sibling group.

Members: `G2-053`, `G2-058`, `G2-059`.

Criterion status: `CARRIED_FORWARD_NOT_REASSESSED_IN_THIS_PACKET`.

### GS-AgentKinds

Parent: [Agent](RKM-C047.md); disjoint: `true`; complete: `false`.

Bearer kind: human individual or organized social entity.

Person is defined as a human individual; Organization is an organized social entity. The current model does not close Agent to these two kinds.

Members: `G-20`, `G-21`.

Criterion status: `EXPLICITLY_RETAINED_BEARER_KIND_CRITERION`.

## Excluded blanket sets

### GS-RKM-C014

Shared documentary identity does not supply one specialization criterion for documentary subkinds and an evidential role. Retain every subtype edge; do not invent a replacement set for all subkinds.

### GS-RKM-C047

Retain the separate, disjoint and incomplete AgentKinds set; responsible and authorizing participation must not compete with Person/Organization classification.
