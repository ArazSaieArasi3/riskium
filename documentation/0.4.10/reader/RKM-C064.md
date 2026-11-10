# Workflow Assignment

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C064`; **source title:** `WorkflowAssignment`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D08 · Risk Workflow](Subdomains.md#d08)

## Authored source definition

A temporally bounded situation in which a managed record revision has an assigned workflow state under an identified scheme version; the statement documenting this situation is separate.

## Identity and source typing

- OntoUML stereotype: `situation`; abstract: `false`.
- Identity supplier: No identity supplier is assigned in this source record.
- Identity basis: A time-qualified configuration whose participants and context must be evidenced.
- Typing rationale: Situation interpretation; neither a workflow label nor an assessment score is the situation itself.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| RX-029 | outgoing `assignsState` | [Workflow State Term](RKM-C061.md) | 0..* | 1 | FORMAL_CORE |
| RX-030 | outgoing `underSchemeVersion` | [Workflow Scheme Version](RKM-C063.md) | 0..* | 1 | FORMAL_CORE |
| RX-031 | outgoing `assignmentForRevision` | [Entry Revision](RKM-C023.md) | 0..* | 1 | FORMAL_CORE |
| RX-032 | incoming `documentsWorkflowAssignment` | [Record State Assertion](RKM-C062.md) | 0..* | 0..1 | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: None recorded.<br>
Direct subtypes: None recorded.

## Current documentary comparisons

**Disposition:** `CONTRAST` · reviewed 2026-11-10.

Replace the scoped absence label with a contrast. Riskium WorkflowAssignment is a timed record-state situation under a scheme version, rather than an activity-function description.

The statement documenting an assignment is distinct from the assignment situation.

### prov:Role

**Selected source meaning (paraphrase):** A function in an activity-qualified provenance context.

**Source and locator:** [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/), W3C Recommendation, 30 April 2013; [§4.3, Role](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Role). Inspected 2026-11-10.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

**Review role:** Assistant-supported reinspection of selected primary passages and unchanged authored/local structural context; not an independent expert judgment.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-reuse-review/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
