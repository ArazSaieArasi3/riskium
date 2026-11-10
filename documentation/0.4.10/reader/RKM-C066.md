# Evidence Item

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C066`; **source title:** `EvidenceItem`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D09 · Risk Evidence](Subdomains.md#d09)

## Authored source definition

An information artifact playing an evidential role for a specified claim or analytical activity. The same artifact may be used as evidence in one context and not another.

## Identity and source typing

- OntoUML stereotype: `role`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits bearer identity; role membership depends on an explicit responsibility or evidential context.
- Typing rationale: Anti-rigid documentary role founded through mandatory mediation by EvidenceUseRelator. The artifact retains InformationArtifact identity when not used as evidence.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| RE-001 | incoming `mediatesEvidenceItem` | [Evidence Use Relator](RKM-C075.md) | 1..* | 1 | FORMAL_CORE |
| RX-021 | incoming `pointsToEvidence` | [Evidence Reference](RKM-C065.md) | 1..* | 1 | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Information Artifact](RKM-C014.md)<br>
Direct subtypes: None recorded.

## Current documentary comparisons

**Disposition:** `RELATED` · reviewed 2026-11-10.

Retain the external comparison and separately document the role foundation. EvidenceItem inherits artifact identity; RE-001 makes participation depend on grounded use. It does not classify every artifact as evidence everywhere.

### prov:Entity

**Selected source meaning (paraphrase):** A thing considered through fixed aspects, including conceptual or imaginary things.

**Source and locator:** [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/), W3C Recommendation, 30 April 2013; [§4.1, Entity](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Entity). Inspected 2026-11-10.

**Inspected scope:** Selected Entity, Person, Organization, Revision, Role, Usage and qualifiedUsage passages only; no import or PROV conformance asserted.

### prov:Role

**Selected source meaning (paraphrase):** A function in an activity-qualified provenance context.

**Source and locator:** [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/), W3C Recommendation, 30 April 2013; [§4.3, Role](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Role). Inspected 2026-11-10.

**Inspected scope:** Selected Entity, Person, Organization, Revision, Role, Usage and qualifiedUsage passages only; no import or PROV conformance asserted.

### Modeling foundations, separate from the domain comparison

These terms inform the selected modeling pattern; they do not supply a risk-domain definition or an asserted alignment axiom.

### OntoUML Role

**Selected source meaning (paraphrase):** A contingent, relationally dependent sortal that inherits identity.

**Source and locator:** [OntoUML specification: Role](https://ontouml.readthedocs.io/en/latest/classes/sortals/role/index.html), Unversioned latest documentation; response body hash and access date retained; [Definition; constraints C1-C2](https://ontouml.readthedocs.io/en/latest/classes/sortals/role/index.html). Inspected 2026-11-10.

**Inspected scope:** Definition and constraints C1-C2 only; modeling foundation, not a domain definition.

**Authored illustration, not an executed test:** A retained report plays an evidential role in one grounded analysis and remains the same artifact afterwards.

**Interpretation counterexample:** A bibliography mention alone does not establish actual evidential participation or claim truth.

**Review role:** Assistant-supported inspection of selected primary-source passages and the current authored model; no independent human rating.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-changed-review/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Selected integration interpretation](../../../evaluation/manuscript-review/v7.2.3/issue93-integration/definitions/RKM-C066.md) preserves the separate candidate design decision.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
