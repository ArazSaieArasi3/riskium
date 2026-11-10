# Evidence Reference Role

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C076`; **source title:** `EvidenceReferenceRole`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D09 · Risk Evidence](Subdomains.md#d09)

## Authored source definition

A qualified EvidenceReference participating in an actual grounded evidential-use relationship. The reference retains documentary identity when it is only a record of a proposed use.

## Identity and source typing

- OntoUML stereotype: `role`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits InformationArtifact identity through EvidenceReference; role membership depends on grounded evidential use.
- Typing rationale: Anti-rigid participation of a documentary reference, distinct from merely recording a proposed use.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| RE-002 | incoming `mediatesEvidenceReference` | [Evidence Use Relator](RKM-C075.md) | 1..* | 1 | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Evidence Reference](RKM-C065.md)<br>
Direct subtypes: None recorded.

## Current documentary comparisons

**Disposition:** `CONTRAST` · reviewed 2026-11-10.

Distinguish a function description from the documentary reference that participates in grounded use. GE-001 preserves reference identity through EvidenceReference and InformationArtifact; RE-002 supplies the role dependency. The reference can exist as a record of proposed use without this role membership.

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

**Authored illustration, not an executed test:** An existing qualified reference participates in an actual grounded use while keeping its documentary identity.

**Interpretation counterexample:** Assigning a PROV function label or recording a proposed use alone does not instantiate this participation role.

**Review role:** Assistant-supported inspection of selected primary-source passages and the current authored model; no independent human rating.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-changed-review/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** ISOLATED_CANDIDATE; scoped tests recorded separately

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Selected integration interpretation](../../../evaluation/manuscript-review/v7.2.3/issue93-integration/definitions/RKM-C076.md) preserves the separate candidate design decision.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
