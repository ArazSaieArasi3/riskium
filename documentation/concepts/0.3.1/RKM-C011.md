# Vulnerability

**Source ID:** `RKM-C011` · **Subdomain:** [D01 · Risk Phenomena](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

An intrinsic susceptibility of a bearer to specified risk-relevant conditions or effects. The proposed mode interpretation requires a supported bearer; security-specific exploitation meanings remain source-qualified.

## Identity and modeling

- OntoUML stereotype: `mode`; abstract: `false`.
- Identity supplier: `None`.
- Identity basis: Intrinsic susceptibility with exactly one substantial-endurant bearer. Bearer identity is supplied externally. Mere reported susceptibility is recorded as information, not automatically asserted as an actual intrinsic mode.
- Typing rationale: The approved intrinsic interpretation is proposed as «mode» and is connected to an imported Object category through characterization. Broader relational vulnerability meanings are not silently equated with this interpretation.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RK2-002` | incoming `refersToVulnerability` | [Risk Context Specification](RKM-C002.md) | 0..* → 0..* |
| `RK3-004` | incoming `bearsVulnerability` | EXT-OBJECT (external anchor; [source catalog](../../../ontology/riskium-model.json)) | 1 → 0..* |

Generalizes: none recorded.  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
