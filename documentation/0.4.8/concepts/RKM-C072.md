# Risk Criteria

**Source ID:** `RKM-C072` · **Subdomain:** [D11 · Risk Policy](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A versioned information specification of reference conditions used to judge the significance or acceptability of risk in an identified context.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RX-017` | outgoing `criteriaForContext` | [Risk Context Specification](RKM-C002.md) | 0..* → 1..* |
| `RX-018` | outgoing `considersAppetiteStatement` | [Risk Appetite Statement](RKM-C073.md) | 0..* → 0..* |
| `RX-019` | outgoing `considersToleranceStatement` | [Risk Tolerance Statement](RKM-C074.md) | 0..* → 0..* |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `NEEDS_LICENSED_SOURCE` · reviewed 2026-11-05.

**Authored comparison:** The ISO catalogue confirms edition identity only. Exact normative risk-criteria wording and clause mapping remain unassessed until legitimate text is inspected.

**Source identity only:** [ISO 31073:2022, Risk management — Vocabulary](https://www.iso.org/standard/79637.html), Edition 1, February 2022. Accessed 2026-11-05.

No normative term definition or clause locator is claimed from catalogue metadata.

**Separate follow-up:** [#78](https://github.com/ArazSaieArasi3/riskium/issues/78).

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
