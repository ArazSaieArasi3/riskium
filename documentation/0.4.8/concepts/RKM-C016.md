# Information Content

**Source ID:** `RKM-C016` · **Subdomain:** [D02 · Risk Information](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

The abstract informational meaning expressed by artifacts or versions. Content identity requires an explicit equivalence policy and is not inferred from equal strings or file hashes.

## Identity and modeling

- OntoUML stereotype: `abstract`; abstract: `false`.
- Identity supplier: `None`.
- Identity basis: Abstract content identity requires a separately declared equivalence policy.
- Typing rationale: OntoUML 2 abstract-domain commitment, not a concrete managed-document kind. Native profile conformance is not established by this catalog.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RX-007` | incoming `expressesContent` | [Artifact Version](RKM-C015.md) | 0..* → 1..* |

Generalizes: none recorded.  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `RELATED` · reviewed 2026-11-05.

**Authored comparison:** PROV permits conceptual entities but gives no policy for identity of abstract meanings; Riskium content equivalence remains application-governed.

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
