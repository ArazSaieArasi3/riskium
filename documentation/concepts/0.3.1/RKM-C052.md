# Responsibility Relator

**Source ID:** `RKM-C052` · **Subdomain:** [D07 · Risk Responsibility](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A temporally qualified responsibility relationship connecting its participants, responsibility scope and grounding assignment.

## Identity and modeling

- OntoUML stereotype: `relator`; abstract: `false`.
- Identity supplier: [Responsibility Relator](RKM-C052.md).
- Identity basis: A grounded responsibility relationship with at least two distinct mediated individuals.
- Typing rationale: Relator proposal. Same actor at both named role ends is insufficient to establish two distinct participants; retain only assignment information until grounding is resolved.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-55` | incoming `documentsActualMandate` | [Responsibility Assignment Information](RKM-C051.md) | 0..* → 0..1 |
| `R-56` | outgoing `mediatesBearer` | [Responsible Agent Role](RKM-C053.md) | 1..* → 1 |
| `R-57` | outgoing `mediatesAuthority` | [Authorizing Agent Role](RKM-C054.md) | 1..* → 1 |
| `R-58` | outgoing `mandateAbout` | [Risk Case](RKM-X01.md) | 0..* → 1..* |
| `R-59` | outgoing `mandateRole` | [Responsibility Role Term](RKM-C059.md) | 0..* → 1 |

Generalizes: none recorded.  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
