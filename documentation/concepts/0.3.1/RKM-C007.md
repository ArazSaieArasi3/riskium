# Risk Source

**Source ID:** `RKM-C007` · **Subdomain:** [D01 · Risk Phenomena](Subdomains.md) · **Layer:** `OPTIONAL_PHENOMENON_BOUNDARY`

## Current authored definition

A contextual source role that an entity may play in giving rise to risk, alone or with other contributors. The catalog boundary spans possible bearer categories and is not assigned a single OntoUML stereotype here.

## Identity and modeling

- OntoUML stereotype: `None`; abstract: `false`.
- Identity supplier: `None`.
- Identity basis: Bearer-specific; no uniform identity principle over objects, events, situations and aspects.
- Typing rationale: Broad domain notion retained in the catalog and optional external bridge; no uniform native OntoUML class asserted.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RK3-002` | incoming `resolvesToSource` | [Risk Source Reference](RKM-X06.md) | 0..* → 0..1 |
| `RX-005` | incoming `hasSource` | [Risk Case](RKM-X01.md) | 0..* → 0..* |

Generalizes: none recorded.  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
