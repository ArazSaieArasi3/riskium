# Workflow Assignment

**Source ID:** `RKM-C064` · **Subdomain:** [D08 · Risk Workflow](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A temporally bounded situation in which a managed record revision has an assigned workflow state under an identified scheme version; the statement documenting this situation is separate.

## Identity and modeling

- OntoUML stereotype: `situation`; abstract: `false`.
- Identity supplier: `None`.
- Identity basis: A time-qualified configuration whose participants and context must be evidenced.
- Typing rationale: Situation interpretation; neither a workflow label nor an assessment score is the situation itself.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RX-029` | outgoing `assignsState` | [Workflow State Term](RKM-C061.md) | 0..* → 1 |
| `RX-030` | outgoing `underSchemeVersion` | [Workflow Scheme Version](RKM-C063.md) | 0..* → 1 |
| `RX-031` | outgoing `assignmentForRevision` | [Entry Revision](RKM-C023.md) | 0..* → 1 |
| `RX-032` | incoming `documentsWorkflowAssignment` | [Record State Assertion](RKM-C062.md) | 0..* → 0..1 |

Generalizes: none recorded.  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `NO_DIRECT_EQUIVALENT_REVIEWED` · reviewed 2026-11-05.

**Authored comparison:** PROV Role is an activity-qualified function, not the timed record-state situation specified here. No direct external equivalent is adopted from that comparison.

### prov:Role

**External source definition (paraphrase):** A function in an activity-qualified provenance context.

**Source:** PROV-O: The PROV Ontology. W3C Recommendation, 30 April 2013. [§4.3, Role](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Role). Accessed 2026-11-05.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
