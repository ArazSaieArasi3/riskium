# Evidence Reference

**Source ID:** `RKM-C065` · **Subdomain:** [D09 · Risk Evidence](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A qualified reference linking a claim or activity to an evidence item, with its intended evidential role and provenance.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-68` | outgoing `supportsRecordedArtifact` | [Information Artifact](RKM-C014.md) | 0..* → 1..* |
| `R-69` | outgoing `refersToOccurrence` | [Risk Occurrence](RKM-C004.md) | 0..* → 0..* |
| `R-70` | outgoing `refersToAgent` | [Agent](RKM-C047.md) | 0..* → 0..* |
| `R-71` | outgoing `refersToAssessmentActivity` | [Assessment Activity](RKM-C031.md) | 0..* → 0..* |
| `R-72` | outgoing `refersToTreatmentActivity` | [Treatment Activity](RKM-C044.md) | 0..* → 0..* |
| `RX-021` | outgoing `pointsToEvidence` | [Evidence Item](RKM-C066.md) | 1..* → 1 |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
