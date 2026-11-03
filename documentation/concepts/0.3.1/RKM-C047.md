# Agent

**Source ID:** `RKM-C047` · **Subdomain:** [D07 · Risk Responsibility](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

An entity capable of performing or being accountable for relevant actions, including persons and organizations within the declared profile.

## Identity and modeling

- OntoUML stereotype: `category`; abstract: `true`.
- Identity supplier: `None`.
- Identity basis: No new identity principle; Person and Organization supply different identities.
- Typing rationale: Rigid abstract non-sortal over the external actor kinds.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-51` | incoming `assessmentPerformer` | [Assessment Activity](RKM-C031.md) | 0..* → 0..* |
| `R-53` | incoming `resolvesToAgent` | [Actor Reference](RKM-C050.md) | 0..* → 0..1 |
| `R-65` | incoming `treatmentPerformer` | [Treatment Activity](RKM-C044.md) | 0..* → 0..* |
| `R-70` | incoming `refersToAgent` | [Evidence Reference](RKM-C065.md) | 0..* → 0..* |

Generalizes: none recorded.  
Specialized by: [Person](RKM-C048.md), [Organization](RKM-C049.md), [Responsible Agent Role](RKM-C053.md), [Authorizing Agent Role](RKM-C054.md).

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
