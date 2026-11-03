# Evidence Item

**Source ID:** `RKM-C066` · **Subdomain:** [D09 · Risk Evidence](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

An information artifact playing an evidential role for a specified claim or analytical activity. The same artifact may be used as evidence in one context and not another.

## Identity and modeling

- OntoUML stereotype: `role`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits bearer identity; role membership depends on an explicit responsibility or evidential context.
- Typing rationale: Anti-rigid contextual classification. Role mixins aggregate person and organization bearers without supplying identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RX-021` | incoming `pointsToEvidence` | [Evidence Reference](RKM-C065.md) | 1..* → 1 |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
