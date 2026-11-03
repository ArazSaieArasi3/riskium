# Workflow Assignment

**Source ID:** `RKM-C064` · **Subdomain:** [D08 · Risk Workflow](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A temporally bounded situation in which a managed record revision has an assigned workflow state under an identified scheme version; the statement documenting this situation is separate.

## Identity and modeling

- OntoUML stereotype: `situation`; abstract: `false`.
- Identity supplier: `None`.
- Identity basis: A time-qualified configuration whose participants and context must be evidenced.
- Typing rationale: Situation interpretation; neither a workflow label nor an assessment score is the situation itself.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RX-029` | outgoing `assignsState` | [Workflow State Term](RKM-C061.md) | 0..* → 1 |
| `RX-030` | outgoing `underSchemeVersion` | [Workflow Scheme Version](RKM-C063.md) | 0..* → 1 |
| `RX-031` | outgoing `assignmentForRevision` | [Entry Revision](RKM-C023.md) | 0..* → 1 |
| `RX-032` | incoming `documentsWorkflowAssignment` | [Record State Assertion](RKM-C062.md) | 0..* → 0..1 |

Generalizes: none recorded.  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
