# Responsibility Relator

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C052`; **source title:** `ResponsibilityRelator`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D07 · Risk Responsibility](Subdomains.md#d07)

## Authored source definition

A temporally qualified responsibility relationship connecting its participants, responsibility scope and grounding assignment.

## Identity and source typing

- OntoUML stereotype: `relator`; abstract: `false`.
- Identity supplier: [Responsibility Relator](RKM-C052.md)
- Identity basis: A grounded responsibility relationship with at least two distinct mediated individuals.
- Typing rationale: Relator proposal. Same actor at both named role ends is insufficient to establish two distinct participants; retain only assignment information until grounding is resolved.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-55 | incoming `documentsActualMandate` | [Responsibility Assignment Information](RKM-C051.md) | 0..* | 0..1 | FORMAL_CORE |
| R-56 | outgoing `mediatesBearer` | [Responsible Agent Role](RKM-C053.md) | 1..* | 1 | FORMAL_CORE |
| R-57 | outgoing `mediatesAuthority` | [Authorizing Agent Role](RKM-C054.md) | 1..* | 1 | FORMAL_CORE |
| R-58 | outgoing `mandateAbout` | [Risk Case](RKM-X01.md) | 0..* | 1..* | FORMAL_CORE |
| R-59 | outgoing `mandateRole` | [Responsibility Role Term](RKM-C059.md) | 0..* | 1 | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: None recorded.<br>
Direct subtypes: None recorded.

## Current documentary comparisons

**Disposition:** `RELATED` · reviewed 2026-11-10.

Retain Relator as a modeling foundation rather than an external responsibility definition. Riskium adds grounding, temporal scope and responsibility semantics; its distinct-participant identity rule is additional to the C2 minimum-cardinality sum.

An owner name alone does not establish a grounded mandate or distinct mediated participants; independent judgment remains #23.

### Modeling foundations, separate from the domain comparison

These terms inform the selected modeling pattern; they do not supply a risk-domain definition or an asserted alignment axiom.

### «Relator»

**Selected source meaning (paraphrase):** A dependent truth-maker connecting multiple participants through material relations.

**Source and locator:** [OntoUML specification: Relator](https://ontouml.readthedocs.io/en/latest/classes/sortals/relator/index.html), Unversioned latest documentation; response digest and current access date retained; [Definition; Constraints C1-C2](https://ontouml.readthedocs.io/en/latest/classes/sortals/relator/index.html#definition). Inspected 2026-11-10.

**Inspected scope:** Definition and constraints C1-C2 only; this modeling construct is not the definition of a responsibility mandate.

**Review role:** Assistant-supported reinspection of selected primary passages and unchanged authored/local structural context; not an independent expert judgment.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-reuse-review/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
