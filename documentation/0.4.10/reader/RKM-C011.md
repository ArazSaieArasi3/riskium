# Vulnerability

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C011`; **source title:** `Vulnerability`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D01 · Risk Phenomena](Subdomains.md#d01)

## Authored source definition

An intrinsic susceptibility of a bearer to specified risk-relevant conditions or effects. The proposed mode interpretation requires a supported bearer; security-specific exploitation meanings remain source-qualified.

## Identity and source typing

- OntoUML stereotype: `mode`; abstract: `false`.
- Identity supplier: No identity supplier is assigned in this source record.
- Identity basis: Intrinsic susceptibility with exactly one substantial-endurant bearer. Bearer identity is supplied externally. Mere reported susceptibility is recorded as information, not automatically asserted as an actual intrinsic mode.
- Typing rationale: The approved intrinsic interpretation is proposed as «mode» and is connected to an imported Object category through characterization. Broader relational vulnerability meanings are not silently equated with this interpretation.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| RK2-002 | incoming `refersToVulnerability` | [Risk Context Specification](RKM-C002.md) | 0..* | 0..* | FORMAL_CORE |
| RK3-004 | incoming `bearsVulnerability` | [External Object](EXT-OBJECT.md) | 1 | 0..* | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: None recorded.<br>
Direct subtypes: None recorded.

## Current documentary comparisons

**Disposition:** `RELATED` · reviewed 2026-11-10.

Retain the security comparison and identify Mode separately as a modeling foundation. The current intrinsic-susceptibility interpretation requires a supported bearer; exactly-one characterization is distinct from a documentary weakness report.

Neither shared terminology nor the type annotation supplies actual bearer evidence or independent semantic acceptance.

### Vulnerability

**Selected source meaning (paraphrase):** A weakness open to threat-source exploitation.

**Source and locator:** [Guide for Conducting Risk Assessments, NIST SP 800-30 Revision 1](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf), September 2012; DOI 10.6028/NIST.SP.800-30r1; [Appendix B, printed B-13, PDF page 63; attributed there to CNSSI 4009](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf#page=63). Inspected 2026-11-10.

**Inspected scope:** Security-specific terms, selected glossary entries and tables only; not a universal enterprise-risk vocabulary. Glossary entries retain their original attributions.

### Modeling foundations, separate from the domain comparison

These terms inform the selected modeling pattern; they do not supply a risk-domain definition or an asserted alignment axiom.

### «Mode»

**Selected source meaning (paraphrase):** An individual intrinsic property dependent on one bearer.

**Source and locator:** [OntoUML specification: Mode](https://ontouml.readthedocs.io/en/latest/classes/aspects/mode/index.html), Unversioned latest documentation; response digest and current access date retained; [Definition; Constraints C1-C2](https://ontouml.readthedocs.io/en/latest/classes/aspects/mode/index.html#definition). Inspected 2026-11-10.

**Inspected scope:** Definition and constraints C1-C2 only; direct HTTP succeeds in this execution. The older null hash/HTTP-403 record is retained in historical review 0.1.0.

**Review role:** Assistant-supported reinspection of selected primary passages and unchanged authored/local structural context; not an independent expert judgment.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-reuse-review/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
