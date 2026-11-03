# Subdomains and their relationships

Riskium has **one general domain** and eleven catalog **subdomains**. The table below is generated from model 0.3.1. Concept pages retain stable source identifiers and explicit membership.

[View the print-ready SVG](../../../diagrams/subdomain-relationships.svg) · [Concept index](README.md)

| ID and subdomain | Purpose | Concepts | Direct neighbor subdomains |
| --- | --- | --- | --- |
| D01 · Risk Phenomena | Preserve the distinction between what risk knowledge is about and the information expressing it. | [Risk Pattern Specification](RKM-C001.md), [Risk Context Specification](RKM-C002.md), [Risk Scenario Specification](RKM-C003.md), [Risk Occurrence](RKM-C004.md), [Risk Nature Assertion](RKM-C005.md), [Nature Term](RKM-C006.md), [Risk Source](RKM-C007.md), [Predisposing Condition](RKM-C008.md), [Trigger](RKM-C009.md), [Consequence](RKM-C010.md), [Vulnerability](RKM-C011.md), [Exposure](RKM-C012.md), [Risk State](RKM-C013.md), [Risk Case](RKM-X01.md), [Risk Source Reference](RKM-X06.md) | [D03](#d03--risk-classification) (1), [D04](#d04--risk-registration) (10), [D05](#d05--risk-assessment) (5), [D06](#d06--risk-treatment) (3), [D07](#d07--risk-responsibility) (2), [D09](#d09--risk-evidence) (1), [D10](#d10--risk-monitoring) (3), [D11](#d11--risk-policy) (5) |
| D02 · Risk Information | Preserve documentary identity, interpretation and version lineage. | [Information Artifact](RKM-C014.md), [Artifact Version](RKM-C015.md), [Information Content](RKM-C016.md) | [D05](#d05--risk-assessment) (4), [D09](#d09--risk-evidence) (1) |
| D03 · Risk Classification | Organize risk content without confusing a term, its label and its referent. | [Vocabulary Concept](RKM-C017.md), [Classification Scheme](RKM-C018.md), [Classification Term](RKM-C019.md), [Classification Assertion](RKM-C020.md), [Tag](RKM-C021.md) | [D01](#d01--risk-phenomena) (1), [D04](#d04--risk-registration) (2) |
| D04 · Risk Registration | Provide an advanced register representation with recoverable historical content. | [Risk Register Entry](RKM-C022.md), [Entry Revision](RKM-C023.md), [Risk Description](RKM-C024.md), [Consequence Statement](RKM-C025.md), [Identification Information](RKM-C026.md), [Intake Channel Term](RKM-C027.md), [Description Role Term](RKM-C028.md), [Consequence Slot Term](RKM-C029.md), [Risk Register](RKM-C030.md) | [D01](#d01--risk-phenomena) (10), [D03](#d03--risk-classification) (2), [D05](#d05--risk-assessment) (1), [D06](#d06--risk-treatment) (3), [D07](#d07--risk-responsibility) (2), [D08](#d08--risk-workflow) (2), [D10](#d10--risk-monitoring) (1) |
| D05 · Risk Assessment | Support interpretation and comparison of results without prescribing an assessment process. | [Assessment Activity](RKM-C031.md), [Assessment Information](RKM-C032.md), [Assessment Basis](RKM-C033.md), [Dimension Assessment Result](RKM-C034.md), [Assessment Method Specification](RKM-C035.md), [Assessment Scale](RKM-C036.md), [Risk Score Result](RKM-C037.md), [Assessment Scale Level](RKM-C038.md), [Assessment Dimension](RKM-C039.md), [Epistemic Status Term](RKM-C040.md), [Uncertainty Statement](RKM-X03.md), [Risk Evaluation Outcome](RKM-X04.md) | [D01](#d01--risk-phenomena) (5), [D02](#d02--risk-information) (4), [D04](#d04--risk-registration) (1), [D06](#d06--risk-treatment) (3), [D07](#d07--risk-responsibility) (1), [D09](#d09--risk-evidence) (1), [D10](#d10--risk-monitoring) (1) |
| D06 · Risk Treatment | Connect decisions and reported actions to their evidential basis and risk subject. | [Treatment Decision Information](RKM-C041.md), [Treatment Strategy Term](RKM-C042.md), [Plan Specification](RKM-C043.md), [Treatment Activity](RKM-C044.md), [Risk Control](RKM-C045.md), [Plan Role Term](RKM-C046.md), [Control Reference](RKM-X05.md) | [D01](#d01--risk-phenomena) (3), [D04](#d04--risk-registration) (3), [D05](#d05--risk-assessment) (3), [D07](#d07--risk-responsibility) (1), [D09](#d09--risk-evidence) (1) |
| D07 · Risk Responsibility | Answer who was recorded as responsible, for what, and under which temporal and authority context. | [Agent](RKM-C047.md), [Person](RKM-C048.md), [Organization](RKM-C049.md), [Actor Reference](RKM-C050.md), [Responsibility Assignment Information](RKM-C051.md), [Responsibility Relator](RKM-C052.md), [Responsible Agent Role](RKM-C053.md), [Authorizing Agent Role](RKM-C054.md), [Responsible Person](RKM-C055.md), [Responsible Organization](RKM-C056.md), [Authorizing Person](RKM-C057.md), [Authorizing Organization](RKM-C058.md), [Responsibility Role Term](RKM-C059.md) | [D01](#d01--risk-phenomena) (2), [D04](#d04--risk-registration) (2), [D05](#d05--risk-assessment) (1), [D06](#d06--risk-treatment) (1), [D09](#d09--risk-evidence) (1) |
| D08 · Risk Workflow | Preserve administrative history while keeping it distinct from real-world risk conditions. | [Analysis State Term](RKM-C060.md), [Workflow State Term](RKM-C061.md), [Record State Assertion](RKM-C062.md), [Workflow Scheme Version](RKM-C063.md), [Workflow Assignment](RKM-C064.md) | [D04](#d04--risk-registration) (2) |
| D09 · Risk Evidence | Preserve provenance and prevent an evidence link from automatically endorsing a claim. | [Evidence Reference](RKM-C065.md), [Evidence Item](RKM-C066.md) | [D01](#d01--risk-phenomena) (1), [D02](#d02--risk-information) (1), [D05](#d05--risk-assessment) (1), [D06](#d06--risk-treatment) (1), [D07](#d07--risk-responsibility) (1) |
| D10 · Risk Monitoring | Represent monitoring content and interpretation without designing an organizational monitoring process. | [Observation Activity](RKM-C067.md), [Observation Result](RKM-C068.md), [Indicator](RKM-C069.md), [Threshold](RKM-C070.md), [Signal](RKM-C071.md) | [D01](#d01--risk-phenomena) (3), [D04](#d04--risk-registration) (1), [D05](#d05--risk-assessment) (1) |
| D11 · Risk Policy | Preserve decision context and source-specific meanings without modeling a complete governance framework. | [Risk Criteria](RKM-C072.md), [Risk Appetite Statement](RKM-C073.md), [Risk Tolerance Statement](RKM-C074.md), [Objective Reference](RKM-X02.md) | [D01](#d01--risk-phenomena) (5) |

## How to read the matrix

The upper triangle contains **23 unordered subdomain pairs** representing **55 distinct concept-level associations**. A number in a cell counts direct associations between concepts in that pair; the diagonal marks self-comparison. It does not count generalizations, rank importance, prescribe process order, or assign navigability. Optional catalog boundary bridges are included. Blank upper cells have no direct association in this catalog version; they do not prove that the topics are unrelated. The short reading path in the figure is explanatory, not a formal edge direction.

## Relationship evidence

| Pair | Distinct associations |
| --- | ---: |
| D01 · Risk Phenomena ↔ D03 · Risk Classification | 1 |
| D01 · Risk Phenomena ↔ D04 · Risk Registration | 10 |
| D01 · Risk Phenomena ↔ D05 · Risk Assessment | 5 |
| D01 · Risk Phenomena ↔ D06 · Risk Treatment | 3 |
| D01 · Risk Phenomena ↔ D07 · Risk Responsibility | 2 |
| D01 · Risk Phenomena ↔ D09 · Risk Evidence | 1 |
| D01 · Risk Phenomena ↔ D10 · Risk Monitoring | 3 |
| D01 · Risk Phenomena ↔ D11 · Risk Policy | 5 |
| D02 · Risk Information ↔ D05 · Risk Assessment | 4 |
| D02 · Risk Information ↔ D09 · Risk Evidence | 1 |
| D03 · Risk Classification ↔ D04 · Risk Registration | 2 |
| D04 · Risk Registration ↔ D05 · Risk Assessment | 1 |
| D04 · Risk Registration ↔ D06 · Risk Treatment | 3 |
| D04 · Risk Registration ↔ D07 · Risk Responsibility | 2 |
| D04 · Risk Registration ↔ D08 · Risk Workflow | 2 |
| D04 · Risk Registration ↔ D10 · Risk Monitoring | 1 |
| D05 · Risk Assessment ↔ D06 · Risk Treatment | 3 |
| D05 · Risk Assessment ↔ D07 · Risk Responsibility | 1 |
| D05 · Risk Assessment ↔ D09 · Risk Evidence | 1 |
| D05 · Risk Assessment ↔ D10 · Risk Monitoring | 1 |
| D06 · Risk Treatment ↔ D07 · Risk Responsibility | 1 |
| D06 · Risk Treatment ↔ D09 · Risk Evidence | 1 |
| D07 · Risk Responsibility ↔ D09 · Risk Evidence | 1 |

[Structural receipt](../../../evaluation/manuscript-review/v7.1.0/supplement/structural-report.json) · [Model source](../../../ontology/riskium-model.json) · [Diagram generator](../../../tools/build_subdomain_relationships.py).

