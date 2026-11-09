# Risk Case

Selected scientific source **0.3.2** for package **v0.3.9**; publication has not yet occurred. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-X01`; **source title:** `RiskCase`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D01 · Risk Phenomena](Subdomains.md#d01)

## Authored source definition

An identifiable risk item for analysis and tracking in relation to objectives and context, which may represent a threat or opportunity from a specified perspective. Its identity persists across descriptions, assessments and administrative record states. It is distinct from a register entry, scenario specification and actual occurrence. Formal organizational register acceptance is application-specific, not a general condition for its existence.

## Identity and source typing

- OntoUML stereotype: `kind`; abstract: `false`.
- Identity supplier: [Risk Case](RKM-X01.md)
- Identity basis: Scoped case identity with traceable source references and continuity criteria. A local identifier represents that identity; equal labels or scores do not establish it. Several descriptions or register entries may concern the same case. Changes in objectives or context require an explicit identity judgment when continuity is uncertain; documented split/merge decisions retain source identifiers and lineage.
- Typing rationale: Proposed identity-supplying kind for the adopted analytical risk item. Analytical identification does not require formal register approval; local governance requirements belong to the declared application profile.
- Source aliases: {'label': 'Risk Item', 'language': 'en', 'scope': 'Context-qualified terminology in this design profile; not a global synonym.', 'relation': 'local synonym for managed risk subject', 'mapping_status': 'INTERPRETATION_OF_USER_DESCRIPTION; not global terminology equivalence'}

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-01 | incoming `recordsAbout` | [Risk Register Entry](RKM-C022.md) | 0..* | 1 | FORMAL_CORE |
| R-03 | incoming `classifies` | [Classification Assertion](RKM-C020.md) | 0..* | 1 | FORMAL_CORE |
| R-07 | incoming `identifiedRisk` | [Identification Information](RKM-C026.md) | 0..* | 1 | FORMAL_CORE |
| R-09 | incoming `assignmentAbout` | [Responsibility Assignment Information](RKM-C051.md) | 0..* | 1 | FORMAL_CORE |
| R-11 | incoming `assesses` | [Assessment Information](RKM-C032.md) | 0..* | 1 | FORMAL_CORE |
| R-19 | incoming `decisionAbout` | [Treatment Decision Information](RKM-C041.md) | 0..* | 1 | FORMAL_CORE |
| R-21 | incoming `planAbout` | [Plan Specification](RKM-C043.md) | 0..* | 1..* | FORMAL_CORE |
| R-22 | incoming `statementAbout` | [Consequence Statement](RKM-C025.md) | 0..* | 1 | FORMAL_CORE |
| R-35 | outgoing `analyzedInContext` | [Risk Context Specification](RKM-C002.md) | 0..* | 0..* | FORMAL_CORE |
| R-36 | incoming `scenarioAbout` | [Risk Scenario Specification](RKM-C003.md) | 0..* | 1..* | FORMAL_CORE |
| R-41 | incoming `natureOf` | [Risk Nature Assertion](RKM-C005.md) | 0..* | 1 | FORMAL_CORE |
| R-58 | incoming `mandateAbout` | [Responsibility Relator](RKM-C052.md) | 0..* | 1..* | FORMAL_CORE |
| R-67 | incoming `controlAddressing` | [Risk Control](RKM-C045.md) | 0..* | 0..* | OPTIONAL_EXTERNAL_BRIDGE |
| RK2-004 | outgoing `hasEstablishedState` | [Risk State](RKM-C013.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-007 | incoming `describesCase` | [Risk Description](RKM-C024.md) | 0..* | 0..* | FORMAL_CORE |
| RK3-001 | outgoing `hasSourceReference` | [Risk Source Reference](RKM-X06.md) | 0..* | 0..* | FORMAL_CORE |
| RX-001 | outgoing `hasContext` | [Risk Context Specification](RKM-C002.md) | 0..* | 1..* | FORMAL_CORE |
| RX-002 | outgoing `appliesPattern` | [Risk Pattern Specification](RKM-C001.md) | 0..* | 0..* | FORMAL_CORE |
| RX-003 | outgoing `concernsObjective` | [Objective Reference](RKM-X02.md) | 0..* | 1..* | FORMAL_CORE |
| RX-004 | incoming `uncertaintyAbout` | [Uncertainty Statement](RKM-X03.md) | 0..* | 1 | FORMAL_CORE |
| RX-005 | outgoing `hasSource` | [Risk Source](RKM-C007.md) | 0..* | 0..* | OPTIONAL_EXTERNAL_BRIDGE |
| RX-011 | incoming `evaluatesCase` | [Risk Evaluation Outcome](RKM-X04.md) | 0..* | 1 | FORMAL_CORE |
| RX-024 | incoming `observesCase` | [Observation Result](RKM-C068.md) | 0..* | 1 | FORMAL_CORE |
| RX-028 | incoming `promptsReviewOf` | [Signal](RKM-C071.md) | 0..* | 0..* | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: None recorded.<br>
Direct subtypes: None recorded.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. Neither the source label nor this generated page supplies independent semantic acceptance, a sourced external definition or standards equivalence. Term-level external alignment is not inferred here.

The adopted analytical-item definition is implemented in scientific source 0.3.2. [issue #92](https://github.com/ArazSaieArasi3/riskium/issues/92) tracks maintained-channel publication. Analytical task readiness and local operational-register eligibility remain distinct; the [selected task profiles](../../../evaluation/manuscript-review/v7.2.3/issue92-riskcase/case_profiles.py) supply the explicit-data checks.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)
