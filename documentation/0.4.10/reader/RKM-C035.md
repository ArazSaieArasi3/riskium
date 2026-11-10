# Assessment Method Specification

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C035`; **source title:** `AssessmentMethodSpecification`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D05 · Risk Assessment](Subdomains.md#d05)

## Authored source definition

A versioned specification of procedures and rules used to produce and interpret assessment results.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-46 | incoming `usesMethod` | [Assessment Information](RKM-C032.md) | 0..* | 0..1 | FORMAL_CORE |
| R-49 | outgoing `permitsScale` | [Assessment Scale](RKM-C036.md) | 0..* | 0..* | FORMAL_CORE |
| R-50 | incoming `scoreMethod` | [Risk Score Result](RKM-C037.md) | 0..* | 1 | FORMAL_CORE |
| RK2-018 | outgoing `specifiesDimension` | [Assessment Dimension](RKM-C039.md) | 0..* | 0..* | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Information Artifact](RKM-C014.md)<br>
Direct subtypes: None recorded.

## Current documentary comparisons

**Disposition:** `ANALOGY` · reviewed 2026-11-10.

Retain the reusable procedure/execution distinction from SOSA. A risk assessment method specification adds risk-specific interpretation rules; no SOSA restriction or full method equivalence is adopted.

R-46/R-50 relate information and scores to a method; R-49 and RK2-018 describe permitted scales/dimensions. The specification retains documentary identity; a separately pinned ArtifactVersion identifies which issued content was used. A procedure description alone is not execution evidence.

### sosa:Procedure

**Selected source meaning (paraphrase):** A reusable method describing how observations, samplings or actuations are performed.

**Source and locator:** [Semantic Sensor Network Ontology](https://www.w3.org/TR/2017/REC-vocab-ssn-20171019/), W3C Recommendation, 19 October 2017; SOSA/SSN; [§4.8.2.1](https://www.w3.org/TR/2017/REC-vocab-ssn-20171019/#SOSAProcedure). Inspected 2026-11-10.

**Inspected scope:** Selected core classes only; observed properties and their specifications remain distinct.

**Review role:** Assistant-supported primary-passage comparison, current ancestry/neighbor/set-policy and selected assessment source-contract checks; not an instance or independent expert evaluation.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-04/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
