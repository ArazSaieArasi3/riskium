# Owner-led review for the first final Riskium release

## Decision, authority and evidence boundary

On 23 October 2026, the project owner stated that **he will perform the current release's review with assistant support**. This supersedes the independent-review scheduling requirement for this first final release. It does not establish independence, supply ratings, change technical acceptance rules or accept unresolved critical defects. The reviewer is Araz Saie Arasi, a project author/owner. The assistant prepares evidence, counterexamples, explanations and proposed dispositions; only explicit owner responses become owner ratings.

Current status: **OWNER_SCOPE_REVIEW_COMPLETE_FINAL_FREEZE_PENDING**. On 24 October 2026 the owner explicitly stated that he had read and agreed with the concrete Persian table and rationale. The [versioned register](register.json) now records all 11 decisions: nine scoped acceptances, one approved necessary revision (implemented in manuscript 7.0.8), and one accepted publication condition awaiting the exact final freeze. The [accepted scope](accepted-scope.json) applies to all 25 clauses and 28 traces; full original MUST fulfillment is not claimed. #7 completes the owner scope-review phase; [#28](https://github.com/ArazSaieArasi3/riskium/issues/28) owns the remaining technical publication condition. #23 preserves independent review as future nonblocking work. The historical independent-review register, source quality synthesis and their zero-independent-rating status remain unchanged.

The rc.5–rc.7 paragraphs and preliminary recommendation table below document the earlier preparation state. Their statements about pending ratings are historical; the current live status is the explicit decision recorded above. No unconditional final-candidate PASS is inferred.

## Review protocol

Review the critical cohort below against the final candidate's exact sources and evidence. For each row, record the owner's explicit Accept / Revise / Defer judgment, scope, rationale and cited evidence or counterexample. Preserve the original response and subsequent resolution. The assistant's recommendation is visibly separate. A row requiring technical evidence cannot be accepted solely because the proposed wording sounds reasonable. A critical in-scope identity, prohibited inference or data-loss defect must be corrected and retested before final publication. A deferral removes the associated claim only when it does not conceal a defect in the retained scope.

No owner-acceptance percentage is reported until actual ratings exist. No inter-rater agreement, independent-expert validation or whole-ontology semantic-correctness percentage is inferred. A named finite review cohort can be completed while unreviewed ontology groups remain explicitly outside that review claim.

| ID | Owner judgment to make | Evidence and counterexample focus | Assistant's preliminary recommendation |
| --- | --- | --- | --- |
| OR-01 | RiskCase identity is distinct from register entry and revision | Native definitions; one case in several registers/scenarios; labels alone cannot merge cases | Accept the distinction subject to actual mapping/history evidence. |
| OR-02 | Scenario specifications/descriptions do not prove an occurrence | Native/OWL boundary; documentary content without independent occurrence evidence | Retain the explicit specification/occurrence boundary. |
| OR-03 | Responsibility information and grounded relators remain distinct | C-06/C-22; participant aliases and explicit distinction; no unique-name assumption | Accept only the declared scoped identity policy; grounding remains a judgment. |
| OR-04 | Issued versions and lineage preserve intended knowledge | C-03/C-24/C-25; static graph checks versus actual history tests in #12 | Require the retained relational/history claims to have executable evidence. |
| OR-05 | C-08 supplementary compatibility policy is adequate for its named task | Profile 0.6.0; unknown units/versions, qualitative terms and conversion exclusions | Accept metadata comparison only; retain global PARTIAL. |
| OR-06 | C-13 selected level/version/dimension interpretation is adequate | Profile 0.7.0; wrong/unknown membership, version targets and missing data | Accept scoped joins if examples and remaining limits fit intended use. |
| OR-07 | C-18 direct comparison eligibility is adequate | Profile 0.7.0; cross-method/scale/time, equal numbers and unsupported transformation | Accept eligibility only; no ranking/calculation or universal comparability claim. |
| OR-08 | Source/standards statements match inspected material | Bounded corpus; unassessed detailed appetite/tolerance definitions | Keep qualified alignment claims; no unsupported normative equivalence. |
| OR-09 | Sourced cases/CQ populations represent intended tasks without invented facts | #13 population receipts, ambiguous/withheld 11 case admissions, expected answers | Judge actual source-backed populations; leave unsupported admissions out. |
| OR-10 | The final claim matrix and manuscript match actual evidence | All MUST requirements, alternative routes, scientific and engineering counts | Accept only after each retained claim has its evidence and scope. |
| OR-11 | Final package is reproducible and critical findings are resolved | Clean freeze, files/tags/checksums/rights/diagrams/Pages and document bindings | Accept after final candidate verification; current prerelease checks alone are insufficient. |

The recommendations are preparation for discussion, **not the owner's judgments**. Source-sensitive recommendations remain conditional. The final release may describe this as owner/author review with assistant support, and must leave independent validation unestablished until #23 supplies actual independent evidence.

## Rc.5 evidence available for the owner

[The published SQL profile and clause dispositions](../relational/history/README.md) and [verified release](../releases/v0.3.1-rc.5-publication.json) now supply scoped executable evidence for OR-01 and OR-04: exact case/entry/revision separation, populated migration, immutable issued payload/dependencies and history. This supports discussion; both owner judgments and all other register ratings remain pending. No automatic acceptance is recorded.

## Rc.6 evidence available for the owner

[Published source-backed CQ06 evidence](../sources/cq06/README.md) and [verified rc.6 publication](../releases/v0.3.1-rc.6-publication.json) now support OR-09 discussion: 13 inspected source statements, exact DOI/page/row/origin joins, deliberate misjoin controls, and 11 still-withheld organizational case admissions. CQ07/08 and semantic adequacy remain explicit limits. No owner rating or independent judgment has been added.

## Rc.7 evidence available for the owner

[Published CQ07/CQ08 evidence](../sources/cq0708/README.md) and [verified rc.7 publication](../releases/v0.3.1-rc.7-publication.json) now support OR-09 and final OR-10 discussion: five inspected original/reissued assertion pairs, one underlying study lineage, exact retained values/context and dedicated unresolved-identity queries over all 11 already-WITHHELD candidates. Raw conflicts/false case promotion and source forgery have separate controls. This is scoped technical evidence; no owner rating or independent judgment has been added. [Preparation issue #27](https://github.com/ArazSaieArasi3/riskium/issues/27) owns the next concrete final claim/route matrix and decision table.

## Concrete final-review package

Preparation #27 supplies the [11-row decision table](../final-review/owner-decisions.md), [all-clause and historical-route matrix](../final-review/README.md) and [seven exact manuscript proposals](../final-review/manuscript.md). These are assistant recommendations, not owner ratings. The preparation package preserves its historical zero-rating snapshot. The live register now contains the owner's explicit decisions; remaining technical critical-finding checks and final freeze are tracked in #28.
