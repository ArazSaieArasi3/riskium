# Semantic core and application profiles

Decision date: 2026-11-07.

This adopted design decision clarifies the intended meaning of RiskCase and the separation between shared semantics and application admission. It accompanies the author-held manuscript revision 7.2.13. The pinned conceptual model 0.3.1, OWL projection, published reader snapshots and historical database receipts retain their original definitions and execution scopes. Reconciliation of those generated artifacts requires a separately reviewed source revision; this document does not claim that migration has run.

## RiskCase and analytical identity

A RiskCase is an identifiable risk item for analysis and tracking in relation to objectives and context. It may represent a threat or opportunity from a specified perspective. Its identity persists across descriptions, assessments and record states; several entries may document it. Formal register acceptance is application-specific, not a general condition for a RiskCase.

Identification as an analytical subject does not require organizational committee approval. A record, scenario specification, actual occurrence and assessment have different roles. Similar labels or equal scores do not establish shared case identity. A shared identifier needs a declared scope and justified identity reconciliation; an identifier alone does not establish that two descriptions concern the same subject.

Threat or opportunity interpretation is qualified by objectives, perspective and context. Partners can evaluate the same subject differently. The existing RiskNatureAssertion concept is relevant to recording those interpretations; this decision adds no disjoint threat/opportunity class partition or automatic identity-merging rule.

## Shared semantics and local requirements

| Layer | Responsibility | Example |
| --- | --- | --- |
| Shared semantic core | Preserve concept meanings, identity distinctions and coherent relations. | A possible scenario is distinct from an asserted occurrence. |
| Application profile | State the requirements for a declared use or readiness level. | Entry into an approved operational register may require an owner, approval and a completed assessment. |
| Implementation | Enforce the selected representation and data contract. | Database keys and separately specified SHACL conditions implement the applicable checks. |

Applications may extend terminology, classifications, evidence, responsibility and workflow requirements while preserving reused core meanings. Local requirements must be identified as local. They must not turn a missing optional field into a universal denial of RiskCase existence or redefine closure as risk cessation.

Context and objectives remain central to interpretation. The completeness of their explicit representation can depend on the selected task profile. Missing information must remain distinguishable from a negative assertion. Exchanged data should declare the applicable profile and retain source identifiers and context. An extension is compatible when it preserves the meaning of reused core terms and their applicable constraints; contradictory local reinterpretations require explicit mappings or revised local terms.

## Literature application and historical evidence

Source extraction, analytical case construction and acceptance into a particular operational register are separate activities. A literature-derived case may use the study's justified context without inventing a deployment at a named enterprise. Conversely, a generic category, ambiguous phrase or bundled set of materially different outcomes is not automatically one identifiable analytical case.

Historical WITHHELD decisions remain part of their original application contract. Reconsideration under this design decision needs new, traceable judgments that distinguish missing operational eligibility from unresolved analytical identity. No source scenario becomes an actual occurrence merely because its analytical interpretation is accepted. This documentation creates no database instances and changes no historical outcome.

## Source-informed interpretation

ISACA, The Risk IT Framework, second edition, 2020, page 37 discusses risk items, scenario components and register-based tracking. Pages 9 and 20 address beneficial and adverse aspects of risk. The inspected portions support a contextual management interpretation; they do not supply a formal identity-equivalence axiom for RiskCase.

PeopleCert International Limited, PRINCE2 Project Management Foundation: Quick Reference Guide, version 7.2, April 2025, section 4.5, pages 24-25 describes uncertainty relative to objectives, threats and opportunities, and register-based records. In this edition the section is a risk practice. It informs the interpretation of a risk item; Riskium's continuing analytical identity is an explicit design commitment.

[PeopleCert-authored guide](https://mypd.co.uk/wp-content/uploads/2025/09/PRINCE2_ProjectManagement_FND_QRG_EN_v.7.2.pdf).

These are scoped conceptual correspondences. Neither a complete framework implementation nor formal class equivalence or compliance certification is asserted. Restricted source texts and private dataset records are not redistributed.

## Interpretation of quality evidence

Structural observations show how the projected design is connected, how subdomains reach one another and where shared infrastructure concentrates dependencies. HermiT results address the tested logical consequences; pySHACL results address the declared explicit-data conditions. Ontological review and pattern screening examine distinct conceptual questions, while preliminary expert feedback supplies qualitative conceptual acceptance. None of these different evidence units is pooled into an overall semantic-correctness percentage.

The current structural observations are not semantic COH/COP. A subsequent semantic dependency evaluation requires declared local/external symbols, axiom allocation, source-faithful entailment tests and documented weights. Logical module views may be investigated without assuming that each catalog subdomain must first be deployed as a separate production file. Optimal modularity and general independent semantic acceptance remain separate, unestablished claims.

## Follow-up and related artifacts

1. Review the RiskCase definition, identity rationale and affected requirements in the next source revision.
2. Reconcile native, OWL, SHACL, relational and generated reader artifacts against that reviewed source.
3. Reassess selected literature candidates under an explicit analytical-case profile while preserving historical decisions.
4. Keep semantic dependency calculations separate from descriptive graph observations.

[Modeling decisions](../modeling-decisions.md) · [Current scope guide](../guides/Scope.md) · [Pinned model](../../ontology/riskium-model.json) · [OWL mapping](../../evaluation/owl-mapping-review.md) · [Quality evidence](../../evaluation/quality/README.md) · [Case study work](https://github.com/ArazSaieArasi3/riskium/issues/13) · [Semantic module work](https://github.com/ArazSaieArasi3/riskium/issues/77)
