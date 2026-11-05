# Vulnerability

**Source ID:** `RKM-C011` · **Subdomain:** [D01 · Risk Phenomena](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

An intrinsic susceptibility of a bearer to specified risk-relevant conditions or effects. The proposed mode interpretation requires a supported bearer; security-specific exploitation meanings remain source-qualified.

## Identity and modeling

- OntoUML stereotype: `mode`; abstract: `false`.
- Identity supplier: `None`.
- Identity basis: Intrinsic susceptibility with exactly one substantial-endurant bearer. Bearer identity is supplied externally. Mere reported susceptibility is recorded as information, not automatically asserted as an actual intrinsic mode.
- Typing rationale: The approved intrinsic interpretation is proposed as «mode» and is connected to an imported Object category through characterization. Broader relational vulnerability meanings are not silently equated with this interpretation.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RK2-002` | incoming `refersToVulnerability` | [Risk Context Specification](RKM-C002.md) | 0..* → 0..* |
| `RK3-004` | incoming `bearsVulnerability` | EXT-OBJECT (external anchor; [source catalog](../../../ontology/riskium-model.json)) | 1 → 0..* |

Generalizes: none recorded.  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `RELATED` · reviewed 2026-11-05.

**Authored comparison:** The security weakness account informs one use; the intrinsic-mode interpretation separately requires a bearer. Neither source equates all vulnerabilities with one domain class.

### Vulnerability

**External source definition (paraphrase):** A weakness susceptible to exploitation by a threat source.

**Source:** Guide for Conducting Risk Assessments, NIST SP 800-30 Revision 1. September 2012; DOI 10.6028/NIST.SP.800-30r1. [Appendix B, printed B-13, PDF page 63; attributed there to CNSSI 4009](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf#page=63). Accessed 2026-11-05.

**Inspected scope:** Security-specific terms, selected glossary entries and tables only; not a universal enterprise-risk vocabulary. Glossary entries retain their original attributions.

### «Mode»

**External source definition (paraphrase):** An individual intrinsic property dependent on one bearer.

**Source:** OntoUML specification: Mode. Unversioned latest documentation, inspected 5 November 2026. [Definition; Constraints C1-C2](https://ontouml.readthedocs.io/en/latest/classes/aspects/mode/index.html#definition). Accessed 2026-11-05.

**Inspected scope:** Definition and constraints C1-C2 inspected through public indexed full text; direct response returned HTTP 403, so no response-body hash is claimed.

**Separate follow-up:** [#23](https://github.com/ArazSaieArasi3/riskium/issues/23).

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
