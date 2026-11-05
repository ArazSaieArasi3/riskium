# Risk Case

**Source ID:** `RKM-X01` · **Subdomain:** [D01 · Risk Phenomena](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

An instituted, identifiable subject of enterprise-risk analysis and tracking. It persists across its descriptions, reassessments, responsibilities and administrative record states under a governed identity policy. It is neither its register entry nor a scenario specification nor an actual occurrence.

## Identity and modeling

- OntoUML stereotype: `kind`; abstract: `false`.
- Identity supplier: [Risk Case](RKM-X01.md).
- Identity basis: Stable case identifier in a governed namespace. Text similarity never automatically merges cases. Change of objective or context triggers a documented identity review; split/merge decisions preserve original identifiers and evidence.
- Typing rationale: Proposed identity-supplying sortal; external Person/Organization and instituted case identities require their owning-domain commitments.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-01` | incoming `recordsAbout` | [Risk Register Entry](RKM-C022.md) | 0..* → 1 |
| `R-03` | incoming `classifies` | [Classification Assertion](RKM-C020.md) | 0..* → 1 |
| `R-07` | incoming `identifiedRisk` | [Identification Information](RKM-C026.md) | 0..* → 1 |
| `R-09` | incoming `assignmentAbout` | [Responsibility Assignment Information](RKM-C051.md) | 0..* → 1 |
| `R-11` | incoming `assesses` | [Assessment Information](RKM-C032.md) | 0..* → 1 |
| `R-19` | incoming `decisionAbout` | [Treatment Decision Information](RKM-C041.md) | 0..* → 1 |
| `R-21` | incoming `planAbout` | [Plan Specification](RKM-C043.md) | 0..* → 1..* |
| `R-22` | incoming `statementAbout` | [Consequence Statement](RKM-C025.md) | 0..* → 1 |
| `R-35` | outgoing `analyzedInContext` | [Risk Context Specification](RKM-C002.md) | 0..* → 0..* |
| `R-36` | incoming `scenarioAbout` | [Risk Scenario Specification](RKM-C003.md) | 0..* → 1..* |
| `R-41` | incoming `natureOf` | [Risk Nature Assertion](RKM-C005.md) | 0..* → 1 |
| `R-58` | incoming `mandateAbout` | [Responsibility Relator](RKM-C052.md) | 0..* → 1..* |
| `R-67` | incoming `controlAddressing` | [Risk Control](RKM-C045.md) | 0..* → 0..* |
| `RK2-004` | outgoing `hasEstablishedState` | [Risk State](RKM-C013.md) | 0..* → 0..* |
| `RK2-007` | incoming `describesCase` | [Risk Description](RKM-C024.md) | 0..* → 0..* |
| `RK3-001` | outgoing `hasSourceReference` | [Risk Source Reference](RKM-X06.md) | 0..* → 0..* |
| `RX-001` | outgoing `hasContext` | [Risk Context Specification](RKM-C002.md) | 0..* → 1..* |
| `RX-002` | outgoing `appliesPattern` | [Risk Pattern Specification](RKM-C001.md) | 0..* → 0..* |
| `RX-003` | outgoing `concernsObjective` | [Objective Reference](RKM-X02.md) | 0..* → 1..* |
| `RX-004` | incoming `uncertaintyAbout` | [Uncertainty Statement](RKM-X03.md) | 0..* → 1 |
| `RX-005` | outgoing `hasSource` | [Risk Source](RKM-C007.md) | 0..* → 0..* |
| `RX-011` | incoming `evaluatesCase` | [Risk Evaluation Outcome](RKM-X04.md) | 0..* → 1 |
| `RX-024` | incoming `observesCase` | [Observation Result](RKM-C068.md) | 0..* → 1 |
| `RX-028` | incoming `promptsReviewOf` | [Signal](RKM-C071.md) | 0..* → 0..* |

Generalizes: none recorded.  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `NO_DIRECT_EQUIVALENT_REVIEWED` · reviewed 2026-11-05.

**Authored comparison:** PROV Entity does not specify continuing organizational risk-case identity. This scoped source comparison neither proves novelty nor replaces the existing COVER/IRISPortal comparison or independent review.

### prov:Entity

**External source definition (paraphrase):** A thing considered through fixed aspects, including conceptual or imaginary things.

**Source:** PROV-O: The PROV Ontology. W3C Recommendation, 30 April 2013. [§4.1, Entity](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Entity). Accessed 2026-11-05.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

**Separate follow-up:** [#23](https://github.com/ArazSaieArasi3/riskium/issues/23).

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
