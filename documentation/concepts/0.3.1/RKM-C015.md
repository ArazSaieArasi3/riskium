# Artifact Version

**Source ID:** `RKM-C015` · **Subdomain:** [D02 · Risk Information](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

An identifiable issued documentary version of a managed information artifact. Its issued semantic content and effective dependency versions are immutable; revisions receive distinct version identities.

## Identity and modeling

- OntoUML stereotype: `kind`; abstract: `false`.
- Identity supplier: [Artifact Version](RKM-C015.md).
- Identity basis: Provides an explicitly governed individuation principle within the declared profile; surrogate keys are identifiers of that policy, not independent ontological proof.
- Typing rationale: Proposed identity-supplying sortal; external Person/Organization and instituted case identities require their owning-domain commitments.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RX-006` | outgoing `versionOf` | [Information Artifact](RKM-C014.md) | 0..* → 1 |
| `RX-007` | outgoing `expressesContent` | [Information Content](RKM-C016.md) | 0..* → 1..* |
| `RX-013` | incoming `usesCriteriaVersion` | [Risk Evaluation Outcome](RKM-X04.md) | 0..* → 1 |
| `RX-014` | incoming `usesContextVersion` | [Assessment Information](RKM-C032.md) | 0..* → 1 |
| `RX-015` | incoming `usesMethodVersion` | [Assessment Information](RKM-C032.md) | 0..* → 0..1 |
| `RX-016` | incoming `usesScaleVersion` | [Dimension Assessment Result](RKM-C034.md) | 0..* → 0..1 |

Generalizes: none recorded.  
Specialized by: [Entry Revision](RKM-C023.md), [Workflow Scheme Version](RKM-C063.md).

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
