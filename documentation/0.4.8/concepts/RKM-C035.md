# Assessment Method Specification

**Source ID:** `RKM-C035` · **Subdomain:** [D05 · Risk Assessment](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A versioned specification of procedures and rules used to produce and interpret assessment results.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-46` | incoming `usesMethod` | [Assessment Information](RKM-C032.md) | 0..* → 0..1 |
| `R-49` | outgoing `permitsScale` | [Assessment Scale](RKM-C036.md) | 0..* → 0..* |
| `R-50` | incoming `scoreMethod` | [Risk Score Result](RKM-C037.md) | 0..* → 1 |
| `RK2-018` | outgoing `specifiesDimension` | [Assessment Dimension](RKM-C039.md) | 0..* → 0..* |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `ANALOGY` · reviewed 2026-11-05.

**Authored comparison:** Reusable procedures distinguish a method from an execution; the SOSA domain and Riskium’s risk-assessment interpretation rules differ.

### sosa:Procedure

**External source definition (paraphrase):** A reusable method describing how observations, samplings or actuations are performed.

**Source:** Semantic Sensor Network Ontology. W3C Recommendation, 19 October 2017; SOSA/SSN. [§4.8.2.1](https://www.w3.org/TR/2017/REC-vocab-ssn-20171019/#SOSAProcedure). Accessed 2026-11-05.

**Inspected scope:** Selected core classes only; observed properties and their specifications remain distinct.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
