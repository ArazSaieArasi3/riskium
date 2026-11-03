# Authorizing Agent Role

**Source ID:** `RKM-C054` · **Subdomain:** [D07 · Risk Responsibility](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A context-dependent role borne by an agent authorized to approve or issue a specified decision or assignment.

## Identity and modeling

- OntoUML stereotype: `roleMixin`; abstract: `true`.
- Identity supplier: `None`.
- Identity basis: Inherits bearer identity; role membership depends on an explicit responsibility or evidential context.
- Typing rationale: Anti-rigid contextual classification. Role mixins aggregate person and organization bearers without supplying identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-57` | incoming `mediatesAuthority` | [Responsibility Relator](RKM-C052.md) | 1..* → 1 |

Generalizes: [Agent](RKM-C047.md).  
Specialized by: [Authorizing Person](RKM-C057.md), [Authorizing Organization](RKM-C058.md).

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
