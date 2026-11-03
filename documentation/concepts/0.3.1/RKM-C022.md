# Risk Register Entry

**Source ID:** `RKM-C022` · **Subdomain:** [D04 · Risk Registration](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A managed register record about exactly one RiskCase in this profile. Distinct entries, source systems or registers can record the same case. A software record is an implementation record, not an additional risk subject.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-01` | outgoing `recordsAbout` | [Risk Case](RKM-X01.md) | 0..* → 1 |
| `R-33` | incoming `revisionOf` | [Entry Revision](RKM-C023.md) | 0..* → 1 |
| `RX-008` | outgoing `memberOfRegister` | [Risk Register](RKM-C030.md) | 0..* → 1 |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
