# Responsible Person

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C055`; **source title:** `ResponsiblePerson`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D07 · Risk Responsibility](Subdomains.md#d07)

## Authored source definition

A person bearing a responsible-agent role in a specified assignment context.

## Identity and source typing

- OntoUML stereotype: `role`; abstract: `false`.
- Identity supplier: [Person](RKM-C048.md)
- Identity basis: Inherits bearer identity; role membership depends on an explicit responsibility or evidential context.
- Typing rationale: Anti-rigid contextual classification. Role mixins aggregate person and organization bearers without supplying identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| — | No direct catalog association recorded. | — | — | — | — |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Person](RKM-C048.md), [Responsible Agent Role](RKM-C053.md)<br>
Direct subtypes: None recorded.

## Current documentary comparisons

**Disposition:** `ANALOGY` · reviewed 2026-11-10.

Retain the person/function analogy while preserving the assigned responsible-person role as a contextual participation of the same human bearer.

G-24 provides the sole inherited identity supplier Person; G-25 supplies the ResponsibleAgentRole path and inherited R-56 mediation. The same human can bear different roles across contexts without being duplicated or merged with an organization.

### prov:Person

**Selected source meaning (paraphrase):** A person considered as a provenance agent.

**Source and locator:** [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/), W3C Recommendation, 30 April 2013; [§4.2, Person](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Person). Inspected 2026-11-10.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

### prov:Role

**Selected source meaning (paraphrase):** A function in an activity-qualified provenance context.

**Source and locator:** [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/), W3C Recommendation, 30 April 2013; [§4.3, Role](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Role). Inspected 2026-11-10.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

### Modeling foundations, separate from the domain comparison

These terms inform the selected modeling pattern; they do not supply a risk-domain definition or an asserted alignment axiom.

### OntoUML specification: Role

**Selected source meaning (paraphrase):** A contextual sortal inheriting one identity principle.

**Source and locator:** [OntoUML specification: Role](https://ontouml.readthedocs.io/en/latest/classes/sortals/role/index.html), Unversioned latest documentation; access date and response digest retained; [Definition and constraints C1-C2](https://ontouml.readthedocs.io/en/latest/classes/sortals/role/index.html#definition). Inspected 2026-11-10.

**Inspected scope:** Definition and selected identity/dependency/abstractness constraints only; not an external domain definition or conformance certificate.

**Review role:** Assistant-supported selected-source comparison, ancestry/neighbor/set-policy review and bounded static identity/dependency checks; no instance-level or independent expert evaluation.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-02/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
