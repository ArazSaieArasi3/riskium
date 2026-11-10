# Control Reference

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-X05`; **source title:** `ControlReference`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D06 · Risk Treatment](Subdomains.md#d06)

## Authored source definition

A managed identifier or description of a claimed control whose real-world bearer may remain unresolved.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| RK2-016 | incoming `recordsControlReference` | [Entry Revision](RKM-C023.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-022 | incoming `referencesControlBaseline` | [Assessment Basis](RKM-C033.md) | 0..* | 0..* | FORMAL_CORE |
| RX-020 | outgoing `resolvesToControl` | [Risk Control](RKM-C045.md) | 0..* | 0..1 | OPTIONAL_EXTERNAL_BRIDGE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Information Artifact](RKM-C014.md)<br>
Direct subtypes: None recorded.

## Current documentary comparisons

**Disposition:** `CONTRAST` · reviewed 2026-11-10.

Retain the contrast between a managed control identifier/description and a safeguard. NIST security-controls text retains its FIPS 199/CNSSI 4009 attribution; neither it nor PROV Entity proves a resolved bearer, implementation or effectiveness.

RX-020 keeps resolution to the heterogeneous control boundary optional. RK2-016/RK2-022 retain register and assessment-baseline references. C-14 excludes a uniform formal-core RiskControl class, so unresolved references remain information rather than fabricated realized controls.

### prov:Entity

**Selected source meaning (paraphrase):** A thing considered through fixed aspects, including conceptual or imaginary things.

**Source and locator:** [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/), W3C Recommendation, 30 April 2013; [§4.1, Entity](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Entity). Inspected 2026-11-10.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

### Security Controls

**Selected source meaning (paraphrase):** Safeguards protecting information and systems against security risks.

**Source and locator:** [Guide for Conducting Risk Assessments, NIST SP 800-30 Revision 1](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf), September 2012; DOI 10.6028/NIST.SP.800-30r1; [Appendix B, printed B-11, PDF page 61; attributed there to FIPS 199/CNSSI 4009](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf#page=61). Inspected 2026-11-10.

**Inspected scope:** Security-specific terms, selected glossary entries and tables only; not a universal enterprise-risk vocabulary. Glossary entries retain their original attributions.

**Review role:** Assistant-supported source comparison, current ancestry/neighbor/set-policy and selected treatment/policy contracts; normative deferrals explicit; not independent expert or operational evaluation.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-05/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
