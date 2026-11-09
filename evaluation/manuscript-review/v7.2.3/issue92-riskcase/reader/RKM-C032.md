# Assessment Information

Candidate **0.3.2-case.1**; not the published current dictionary. Source SHA-256: `e98a63b286441c80fc10a9644804d64fc2b611e906b2d27cf3d72f3ebd72cfa8`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C032`; **source title:** `AssessmentInformation`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D05 · Risk Assessment](Subdomains.md#d05)

## Authored source definition

A managed information artifact documenting an assessment and its scope, basis, methods, time context, participants and results. It is distinct from performing that assessment.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-11 | outgoing `assesses` | [Risk Case](RKM-X01.md) | 0..* | 1 | FORMAL_CORE |
| R-12 | outgoing `hasBasis` | [Assessment Basis](RKM-C033.md) | 0..* | 1 | FORMAL_CORE |
| R-13 | outgoing `hasDimensionResult` | [Dimension Assessment Result](RKM-C034.md) | 1 | 0..* | FORMAL_CORE |
| R-17 | outgoing `hasScoreResult` | [Risk Score Result](RKM-C037.md) | 1 | 0..* | FORMAL_CORE |
| R-26 | incoming `producesAssessmentInformation` | [Assessment Activity](RKM-C031.md) | 0..* | 0..* | FORMAL_CORE |
| R-28 | incoming `documentsAssessment` | [Entry Revision](RKM-C023.md) | 1..* | 0..* | FORMAL_CORE |
| R-45 | outgoing `assessmentContext` | [Risk Context Specification](RKM-C002.md) | 0..* | 0..1 | FORMAL_CORE |
| R-46 | outgoing `usesMethod` | [Assessment Method Specification](RKM-C035.md) | 0..* | 0..1 | FORMAL_CORE |
| R-47 | outgoing `epistemicStatus` | [Epistemic Status Term](RKM-C040.md) | 0..* | 0..1 | FORMAL_CORE |
| RK2-013 | outgoing `recordsUncertainty` | [Uncertainty Statement](RKM-X03.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-015 | incoming `recordsRemainingRiskAssessment` | [Treatment Decision Information](RKM-C041.md) | 0..* | 0..* | FORMAL_CORE |
| RX-012 | incoming `usesAssessment` | [Risk Evaluation Outcome](RKM-X04.md) | 0..* | 1..* | FORMAL_CORE |
| RX-014 | outgoing `usesContextVersion` | [Artifact Version](RKM-C015.md) | 0..* | 1 | FORMAL_CORE |
| RX-015 | outgoing `usesMethodVersion` | [Artifact Version](RKM-C015.md) | 0..* | 0..1 | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Information Artifact](RKM-C014.md)  
Direct subtypes: None recorded.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [candidate execution receipts](../README.md) separately report the current bounded structural and engine checks. Neither the source label nor this generated page supplies independent semantic acceptance, a sourced external definition or standards equivalence. Term-level external alignment is not inferred here.

[Rebuildable source recipe](../build_candidate.py) · [Export contract](../input-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)
