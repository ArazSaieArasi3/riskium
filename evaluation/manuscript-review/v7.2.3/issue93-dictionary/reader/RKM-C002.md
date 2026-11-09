# Risk Context Specification

Candidate **0.3.2-structural.2**; not the published current dictionary. Source SHA-256: `c1556811a468919b75521d1a93b8ef8f91c24bf2799deae274b1d211d5e4d5b7`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C002`; **source title:** `RiskContextSpecification`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D01 · Risk Phenomena](Subdomains.md#d01)

## Authored source definition

A versioned information specification of analysis boundaries, circumstances, time horizon and objective references under which risk statements and results are interpreted.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-35 | incoming `analyzedInContext` | [Risk Case](RKM-X01.md) | 0..* | 0..* | FORMAL_CORE |
| R-43 | incoming `natureInContext` | [Risk Nature Assertion](RKM-C005.md) | 0..* | 0..1 | FORMAL_CORE |
| R-45 | incoming `assessmentContext` | [Assessment Information](RKM-C032.md) | 0..* | 0..1 | FORMAL_CORE |
| RK2-001 | outgoing `refersToCondition` | [Predisposing Condition](RKM-C008.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-002 | outgoing `refersToVulnerability` | [Vulnerability](RKM-C011.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-003 | outgoing `refersToExposure` | [Exposure](RKM-C012.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-009 | incoming `descriptionContext` | [Risk Description](RKM-C024.md) | 0..* | 0..1 | FORMAL_CORE |
| RK2-010 | incoming `scenarioContext` | [Risk Scenario Specification](RKM-C003.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-011 | outgoing `referencesObjective` | [Objective Reference](RKM-X02.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-012 | incoming `uncertaintyContext` | [Uncertainty Statement](RKM-X03.md) | 0..* | 0..1 | FORMAL_CORE |
| RK2-023 | incoming `appetiteContext` | [Risk Appetite Statement](RKM-C073.md) | 0..* | 1..* | FORMAL_CORE |
| RK2-024 | incoming `toleranceContext` | [Risk Tolerance Statement](RKM-C074.md) | 0..* | 1..* | FORMAL_CORE |
| RK2-026 | incoming `observationContext` | [Observation Result](RKM-C068.md) | 0..* | 0..1 | FORMAL_CORE |
| RK3-003 | incoming `sourceReferenceContext` | [Risk Source Reference](RKM-X06.md) | 0..* | 0..1 | FORMAL_CORE |
| RX-001 | incoming `hasContext` | [Risk Case](RKM-X01.md) | 0..* | 1..* | FORMAL_CORE |
| RX-017 | incoming `criteriaForContext` | [Risk Criteria](RKM-C072.md) | 0..* | 1..* | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Information Artifact](RKM-C014.md)  
Direct subtypes: None recorded.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [candidate execution receipts](../README.md) separately report the current bounded structural and engine checks. Neither the source label nor this generated page supplies independent semantic acceptance, a sourced external definition or standards equivalence. Term-level external alignment is not inferred here.

[Rebuildable source recipe](../../issue93-generalization-sets/build_candidate.py) · [Export contract](../../issue93-export-contract/input-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)
