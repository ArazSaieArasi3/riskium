# Information Content

**Source ID:** `RKM-C016` · **Subdomain:** [D02 · Risk Information](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

The abstract informational meaning expressed by artifacts or versions. Content identity requires an explicit equivalence policy and is not inferred from equal strings or file hashes.

## Identity and modeling

- OntoUML stereotype: `abstract`; abstract: `false`.
- Identity supplier: `None`.
- Identity basis: Abstract content identity requires a separately declared equivalence policy.
- Typing rationale: OntoUML 2 abstract-domain commitment, not a concrete managed-document kind. Native profile conformance is not established by this catalog.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RX-007` | incoming `expressesContent` | [Artifact Version](RKM-C015.md) | 0..* → 1..* |

Generalizes: none recorded.  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
