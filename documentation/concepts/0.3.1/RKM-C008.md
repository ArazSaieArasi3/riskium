# Predisposing Condition

**Source ID:** `RKM-C008` · **Subdomain:** [D01 · Risk Phenomena](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A risk-relevant situation that increases susceptibility to specified occurrences or effects. Reference to it requires explicit source support and does not establish a causal mechanism.

## Identity and modeling

- OntoUML stereotype: `situation`; abstract: `false`.
- Identity supplier: `None`.
- Identity basis: A time-qualified configuration whose participants and context must be evidenced.
- Typing rationale: Situation interpretation; neither a workflow label nor an assessment score is the situation itself.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RK2-001` | incoming `refersToCondition` | [Risk Context Specification](RKM-C002.md) | 0..* → 0..* |

Generalizes: none recorded.  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
