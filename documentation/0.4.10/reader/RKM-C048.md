# Person

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C048`; **source title:** `Person`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D07 · Risk Responsibility](Subdomains.md#d07)

## Authored source definition

A human individual who may participate in risk management activities or assignments.

## Identity and source typing

- OntoUML stereotype: `kind`; abstract: `false`.
- Identity supplier: [Person](RKM-C048.md)
- Identity basis: Provides an explicitly governed individuation principle within the declared profile; surrogate keys are identifiers of that policy, not independent ontological proof.
- Typing rationale: Proposed identity-supplying person kind; person identity belongs to the owning external domain and does not institute RiskCase approval requirements.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| — | No direct catalog association recorded. | — | — | — | — |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Agent](RKM-C047.md)<br>
Direct subtypes: [Responsible Person](RKM-C055.md), [Authorizing Person](RKM-C057.md)

## Current documentary comparisons

**Disposition:** `RELATED` · reviewed 2026-11-10.

Retain a human-agent comparison without adopting external identity or typing axioms. Riskium preserves the person identity owned by the external domain; participation and a responsibility mandate need separate evidence.

### prov:Person

**Selected source meaning (paraphrase):** A person considered as a provenance agent.

**Source and locator:** [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/), W3C Recommendation, 30 April 2013; [§4.2, Person](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Person). Inspected 2026-11-10.

**Inspected scope:** Selected Entity, Person, Organization, Revision, Role, Usage and qualifiedUsage passages only; no import or PROV conformance asserted.

**Authored illustration, not an executed test:** The same externally identified person participates in two analyses without being duplicated.

**Interpretation counterexample:** An owner name in an imported document alone does not establish authority or a grounded assignment.

**Review role:** Assistant-supported inspection of selected primary-source passages and the current authored model; no independent human rating.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-changed-review/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
