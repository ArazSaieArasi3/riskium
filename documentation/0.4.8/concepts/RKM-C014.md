# Information Artifact

**Source ID:** `RKM-C014` · **Subdomain:** [D02 · Risk Information](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A managed documentary object with an instituted identity that persists across its descriptions and issued versions. Artifact identity is distinct from a file path, a storage row and semantic content.

## Identity and modeling

- OntoUML stereotype: `kind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Provides an explicitly governed individuation principle within the declared profile; surrogate keys are identifiers of that policy, not independent ontological proof.
- Typing rationale: Proposed identity-supplying sortal; external Person/Organization and instituted case identities require their owning-domain commitments.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-68` | incoming `supportsRecordedArtifact` | [Evidence Reference](RKM-C065.md) | 0..* → 1..* |
| `RX-006` | incoming `versionOf` | [Artifact Version](RKM-C015.md) | 0..* → 1 |

Generalizes: none recorded.  
Specialized by: [Risk Register Entry](RKM-C022.md), [Risk Description](RKM-C024.md), [Classification Assertion](RKM-C020.md), [Identification Information](RKM-C026.md), [Actor Reference](RKM-C050.md), [Responsibility Assignment Information](RKM-C051.md), [Risk Nature Assertion](RKM-C005.md), [Assessment Information](RKM-C032.md), [Assessment Basis](RKM-C033.md), [Dimension Assessment Result](RKM-C034.md), [Assessment Method Specification](RKM-C035.md), [Assessment Scale](RKM-C036.md), [Risk Score Result](RKM-C037.md), [Treatment Decision Information](RKM-C041.md), [Plan Specification](RKM-C043.md), [Consequence Statement](RKM-C025.md), [Record State Assertion](RKM-C062.md), [Evidence Reference](RKM-C065.md), [Risk Pattern Specification](RKM-C001.md), [Risk Context Specification](RKM-C002.md), [Risk Scenario Specification](RKM-C003.md), [Classification Scheme](RKM-C018.md), [Risk Register](RKM-C030.md), [Evidence Item](RKM-C066.md), [Observation Result](RKM-C068.md), [Indicator](RKM-C069.md), [Threshold](RKM-C070.md), [Signal](RKM-C071.md), [Risk Criteria](RKM-C072.md), [Risk Appetite Statement](RKM-C073.md), [Risk Tolerance Statement](RKM-C074.md), [Objective Reference](RKM-X02.md), [Uncertainty Statement](RKM-X03.md), [Risk Evaluation Outcome](RKM-X04.md), [Control Reference](RKM-X05.md), [Vocabulary Concept](RKM-C017.md), [Tag](RKM-C021.md), [Risk Source Reference](RKM-X06.md).

## External definition and alignment status

**Documentary disposition:** `RELATED` · reviewed 2026-11-05.

**Authored comparison:** A managed documentary identity persisting across versions has additional institution and content conditions not supplied by PROV Entity.

### prov:Entity

**External source definition (paraphrase):** A thing considered through fixed aspects, including conceptual or imaginary things.

**Source:** PROV-O: The PROV Ontology. W3C Recommendation, 30 April 2013. [§4.1, Entity](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Entity). Accessed 2026-11-05.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
