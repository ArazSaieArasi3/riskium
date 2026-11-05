# Entry Revision

**Source ID:** `RKM-C023` · **Subdomain:** [D04 · Risk Registration](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

An identifiable version of a register entry, preserving the content and qualified links effective at its issue.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Artifact Version](RKM-C015.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-02` | outgoing `hasDescription` | [Risk Description](RKM-C024.md) | 1 → 0..* |
| `R-23` | outgoing `hasStateAssertion` | [Record State Assertion](RKM-C062.md) | 1 → 0..* |
| `R-24` | outgoing `hasTag` | [Tag](RKM-C021.md) | 0..* → 0..* |
| `R-28` | outgoing `documentsAssessment` | [Assessment Information](RKM-C032.md) | 1..* → 0..* |
| `R-29` | outgoing `documentsClassification` | [Classification Assertion](RKM-C020.md) | 1..* → 0..* |
| `R-30` | outgoing `documentsAssignment` | [Responsibility Assignment Information](RKM-C051.md) | 1..* → 0..* |
| `R-33` | outgoing `revisionOf` | [Risk Register Entry](RKM-C022.md) | 0..* → 1 |
| `R-34` | outgoing `previousRevision` | [Entry Revision](RKM-C023.md) | 0..* → 0..1 |
| `R-34` | incoming `previousRevision` | [Entry Revision](RKM-C023.md) | 0..* → 0..1 |
| `R-38` | outgoing `recordsConsequence` | [Consequence Statement](RKM-C025.md) | 1 → 0..* |
| `R-44` | outgoing `recordsNature` | [Risk Nature Assertion](RKM-C005.md) | 1..* → 0..* |
| `R-52` | outgoing `recordsIdentification` | [Identification Information](RKM-C026.md) | 1..* → 0..* |
| `R-60` | outgoing `recordsDecision` | [Treatment Decision Information](RKM-C041.md) | 1..* → 0..* |
| `R-61` | outgoing `recordsPlan` | [Plan Specification](RKM-C043.md) | 1..* → 0..* |
| `RK2-016` | outgoing `recordsControlReference` | [Control Reference](RKM-X05.md) | 0..* → 0..* |
| `RK2-017` | outgoing `recordsObservation` | [Observation Result](RKM-C068.md) | 0..* → 0..* |
| `RX-031` | incoming `assignmentForRevision` | [Workflow Assignment](RKM-C064.md) | 0..* → 1 |

Generalizes: [Artifact Version](RKM-C015.md).  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `CONTRAST` · reviewed 2026-11-05.

**Authored comparison:** An Entry Revision is a version entity with qualified effective links; prov:Revision is the provenance relationship producing a revision.

### prov:Entity

**External source definition (paraphrase):** A thing considered through fixed aspects, including conceptual or imaginary things.

**Source:** PROV-O: The PROV Ontology. W3C Recommendation, 30 April 2013. [§4.1, Entity](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Entity). Accessed 2026-11-05.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

### prov:Revision

**External source definition (paraphrase):** A qualified derivation whose result revises an original while retaining substantial content.

**Source:** PROV-O: The PROV Ontology. W3C Recommendation, 30 April 2013. [§4.3, Revision](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Revision). Accessed 2026-11-05.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
