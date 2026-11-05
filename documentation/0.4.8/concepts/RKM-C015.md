# Artifact Version

**Source ID:** `RKM-C015` · **Subdomain:** [D02 · Risk Information](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

An identifiable issued documentary version of a managed information artifact. Its issued semantic content and effective dependency versions are immutable; revisions receive distinct version identities.

## Identity and modeling

- OntoUML stereotype: `kind`; abstract: `false`.
- Identity supplier: [Artifact Version](RKM-C015.md).
- Identity basis: Provides an explicitly governed individuation principle within the declared profile; surrogate keys are identifiers of that policy, not independent ontological proof.
- Typing rationale: Proposed identity-supplying sortal; external Person/Organization and instituted case identities require their owning-domain commitments.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RX-006` | outgoing `versionOf` | [Information Artifact](RKM-C014.md) | 0..* → 1 |
| `RX-007` | outgoing `expressesContent` | [Information Content](RKM-C016.md) | 0..* → 1..* |
| `RX-013` | incoming `usesCriteriaVersion` | [Risk Evaluation Outcome](RKM-X04.md) | 0..* → 1 |
| `RX-014` | incoming `usesContextVersion` | [Assessment Information](RKM-C032.md) | 0..* → 1 |
| `RX-015` | incoming `usesMethodVersion` | [Assessment Information](RKM-C032.md) | 0..* → 0..1 |
| `RX-016` | incoming `usesScaleVersion` | [Dimension Assessment Result](RKM-C034.md) | 0..* → 0..1 |

Generalizes: none recorded.  
Specialized by: [Entry Revision](RKM-C023.md), [Workflow Scheme Version](RKM-C063.md).

## External definition and alignment status

**Documentary disposition:** `CONTRAST` · reviewed 2026-11-05.

**Authored comparison:** An issued Artifact Version is an entity; prov:Revision describes a derivation, not the resulting version. First issue also need not be a revision.

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
