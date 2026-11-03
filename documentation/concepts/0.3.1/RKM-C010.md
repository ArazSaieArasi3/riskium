# Consequence

**Source ID:** `RKM-C010` · **Subdomain:** [D01 · Risk Phenomena](Subdomains.md) · **Layer:** `OPTIONAL_PHENOMENON_BOUNDARY`

## Current authored definition

An outcome relevant to objectives, considered as a referent distinct from a statement about it. Outcomes can have different ontological categories; no universal event or object stereotype is asserted.

## Identity and modeling

- OntoUML stereotype: `None`; abstract: `false`.
- Identity supplier: `None`.
- Identity basis: Bearer-specific; no uniform identity principle over objects, events, situations and aspects.
- Typing rationale: Broad domain notion retained in the catalog and optional external bridge; no uniform native OntoUML class asserted.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RK2-006` | incoming `hasEstablishedConsequence` | [Risk Occurrence](RKM-C004.md) | 0..* → 0..* |
| `RX-010` | incoming `refersToActualOutcome` | [Consequence Statement](RKM-C025.md) | 0..* → 0..1 |

Generalizes: none recorded.  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
