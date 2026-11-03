# Risk Control

**Source ID:** `RKM-C045` · **Subdomain:** [D06 · Risk Treatment](Subdomains.md) · **Layer:** `OPTIONAL_PHENOMENON_BOUNDARY`

## Current authored definition

A contextual measure intended to maintain or modify risk. A policy, device, practice or activity may serve as its bearer. Implementation and observed effectiveness are separate claims; one cross-category stereotype is not asserted.

## Identity and modeling

- OntoUML stereotype: `None`; abstract: `false`.
- Identity supplier: `None`.
- Identity basis: Bearer-specific; no uniform identity principle over objects, events, situations and aspects.
- Typing rationale: Broad domain notion retained in the catalog and optional external bridge; no uniform native OntoUML class asserted.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-66` | incoming `implementsControl` | [Treatment Activity](RKM-C044.md) | 0..* → 0..* |
| `R-67` | outgoing `controlAddressing` | [Risk Case](RKM-X01.md) | 0..* → 0..* |
| `RX-020` | incoming `resolvesToControl` | [Control Reference](RKM-X05.md) | 0..* → 0..1 |

Generalizes: none recorded.  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
