# Evidence Use Relator

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C075`; **source title:** `EvidenceUseRelator`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D09 · Risk Evidence](Subdomains.md#d09)

## Authored source definition

A context-qualified evidential-use relationship connecting a qualified reference and a distinct information artifact used as support, challenge or context in an analysis. Its grounding concerns that use, not the truth of the referenced claim.

## Identity and source typing

- OntoUML stereotype: `relator`; abstract: `false`.
- Identity supplier: [Evidence Use Relator](RKM-C075.md)
- Identity basis: One grounded use episode qualified by its reference, evidence artifact, analysis context and evidential purpose; different descriptions of that same use do not supply new identities.
- Typing rationale: Relator candidate: a grounded evidential-use relationship, with two distinct mediated documentary participants. The information describing a proposed use is not automatically an instance of this relator.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| RE-001 | outgoing `mediatesEvidenceItem` | [Evidence Item](RKM-C066.md) | 1..* | 1 | FORMAL_CORE |
| RE-002 | outgoing `mediatesEvidenceReference` | [Evidence Reference Role](RKM-C076.md) | 1..* | 1 | FORMAL_CORE |
| RE-003 | outgoing `groundedInUseRecord` | [Information Artifact](RKM-C014.md) | 0..* | 1 | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: None recorded.<br>
Direct subtypes: None recorded.

## Current documentary comparisons

**Disposition:** `ANALOGY` · reviewed 2026-11-10.

Use an analogy to provenance usage while preserving the different participant structure. Riskium objectifies a grounded use linking a qualified reference and an evidence artifact, with context and purpose. RE-001 and RE-002 mediate the participants; RE-003 records grounding. OntoUML C2 supplies a minimum-count rule; distinct participants are an additional Riskium C-26 commitment, not a conclusion from that sum.

### prov:Usage

**Selected source meaning (paraphrase):** Qualified use of an entity by an activity.

**Source and locator:** [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/), W3C Recommendation, 30 April 2013; [§4.3, Usage](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Usage). Inspected 2026-11-10.

**Inspected scope:** Selected Entity, Person, Organization, Revision, Role, Usage and qualifiedUsage passages only; no import or PROV conformance asserted.

### prov:qualifiedUsage

**Selected source meaning (paraphrase):** Connects an activity to its usage qualification.

**Source and locator:** [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/), W3C Recommendation, 30 April 2013; [§4.3, qualifiedUsage: domain Activity, range Usage](https://www.w3.org/TR/2013/REC-prov-o-20130430/#qualifiedUsage). Inspected 2026-11-10.

**Inspected scope:** Selected Entity, Person, Organization, Revision, Role, Usage and qualifiedUsage passages only; no import or PROV conformance asserted.

### Modeling foundations, separate from the domain comparison

These terms inform the selected modeling pattern; they do not supply a risk-domain definition or an asserted alignment axiom.

### OntoUML Relator

**Selected source meaning (paraphrase):** An identity-bearing objectification of a relationship; mediation minima total at least two.

**Source and locator:** [OntoUML specification: Relator](https://ontouml.readthedocs.io/en/latest/classes/sortals/relator/index.html), Unversioned latest documentation; response body hash and access date retained; [Definition; constraints C1-C2](https://ontouml.readthedocs.io/en/latest/classes/sortals/relator/index.html). Inspected 2026-11-10.

**Inspected scope:** Definition and constraints C1-C2 only; modeling foundation rather than an external definition of evidential use.

**Authored illustration, not an executed test:** A documented analysis uses a particular report as support through a distinct qualified reference and a grounding record.

**Interpretation counterexample:** A proposed citation without grounded use is information; reusing one individual at both mediated ends violates Riskium C-26.

**Review role:** Assistant-supported inspection of selected primary-source passages and the current authored model; no independent human rating.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-changed-review/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** ISOLATED_CANDIDATE; scoped source, OWL and explicit-data tests recorded separately

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Selected integration interpretation](../../../evaluation/manuscript-review/v7.2.3/issue93-integration/definitions/RKM-C075.md) preserves the separate candidate design decision.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
