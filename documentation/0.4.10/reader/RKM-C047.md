# Agent

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C047`; **source title:** `Agent`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D07 · Risk Responsibility](Subdomains.md#d07)

## Authored source definition

An entity capable of performing or being accountable for relevant actions, including persons and organizations within the declared profile.

## Identity and source typing

- OntoUML stereotype: `category`; abstract: `true`.
- Identity supplier: No identity supplier is assigned in this source record.
- Identity basis: No new identity principle; Person and Organization supply different identities.
- Typing rationale: Rigid abstract non-sortal over the external actor kinds.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-51 | incoming `assessmentPerformer` | [Assessment Activity](RKM-C031.md) | 0..* | 0..* | FORMAL_CORE |
| R-53 | incoming `resolvesToAgent` | [Actor Reference](RKM-C050.md) | 0..* | 0..1 | FORMAL_CORE |
| R-65 | incoming `treatmentPerformer` | [Treatment Activity](RKM-C044.md) | 0..* | 0..* | FORMAL_CORE |
| R-70 | incoming `refersToAgent` | [Evidence Reference](RKM-C065.md) | 0..* | 0..* | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: None recorded.<br>
Direct subtypes: [Person](RKM-C048.md), [Organization](RKM-C049.md), [Responsible Agent Role](RKM-C053.md), [Authorizing Agent Role](RKM-C054.md)

## Current documentary comparisons

**Disposition:** `RELATED` · reviewed 2026-11-10.

Retain the provenance-agent comparison without equating capabilities, accountability or identity policies. The Riskium Agent category aggregates bearers rather than supplying a new identity principle.

The explicit AgentKinds set distinguishes human Person from Organization and remains incomplete. Excluding GS-RKM-C047 prevents bearer-kind classification from competing with responsible/authorizing participation. Changed Person/Organization typing rationales are checked at the generalization endpoints.

### prov:Agent

**Selected source meaning (paraphrase):** Something bearing responsibility for an activity, entity or another agent’s activity.

**Source and locator:** [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/), W3C Recommendation, 30 April 2013; [§4.1, Agent](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Agent). Inspected 2026-11-10.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

### Modeling foundations, separate from the domain comparison

These terms inform the selected modeling pattern; they do not supply a risk-domain definition or an asserted alignment axiom.

### OntoUML specification: Category

**Selected source meaning (paraphrase):** An abstract rigid non-sortal aggregating different bearer identities.

**Source and locator:** [OntoUML specification: Category](https://ontouml.readthedocs.io/en/latest/classes/nonsortals/category/index.html), Unversioned latest documentation; access date and response digest retained; [Definition and constraints C1-C2](https://ontouml.readthedocs.io/en/latest/classes/nonsortals/category/index.html#definition). Inspected 2026-11-10.

**Inspected scope:** Definition and selected identity/dependency/abstractness constraints only; not an external domain definition or conformance certificate.

**Review role:** Assistant-supported selected-source comparison, ancestry/neighbor/set-policy review and bounded static identity/dependency checks; no instance-level or independent expert evaluation.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-02/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Selected integration interpretation](../../../evaluation/manuscript-review/v7.2.3/issue93-integration/definitions/RKM-C047.md) preserves the separate candidate design decision.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
