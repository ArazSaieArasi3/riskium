# HermiT constraint disposition after the conditional OWL review

The [execution report](report.md) is the authoritative outcome register. Its denominator retains all 25 interpretation constraints. This review assigns the **14 NOT_RUN HermiT rows** to evidence that can actually decide them; it does not relabel them PASS or remove them from the 295-row baseline. The 11 PASS rows establish a bounded OWL portion only. The [coverage contract](../coverage-contract.md) retains the source wording and planned positive/prohibited behavior.

| Constraint | Next evidence and issue | Decision needed before a result can count |
| --- | --- | --- |
| C-03 | Application history and transaction tests; #12 for persistence mapping | An issued payload cannot be overwritten; a revision creates a distinct version with lineage. Static graph shape checks alone cannot test a past update. |
| C-04 | Task-ready SHACL joins in #5; interpretation review in #7 | Approve method, scale, dimension, basis and time properties before requiring them or judging qualitative likelihood. |
| C-05 | Temporal field/interval shapes in #5; application and semantic review in #7/#12 | Pin recorded, reference and validity time semantics; workflow closure cannot imply cessation or effectiveness. |
| C-09 | Published-description SHACL profile in #5 | Define the publication focus population; require at least one explicit case, pattern or scenario link and preserve legitimate multiple targets. No unconditional OWL restriction on every description. |
| C-10 | Source-qualified provenance shape in #5 and standards interpretation in #8 | Approve framework/version, context and original-meaning references; avoid a universal tolerance equivalence. |
| C-11 | Scheme-qualified vocabulary admission in #5 | Approve scheme identifiers, resource identity and labels; a shared label is not an identity key. |
| C-12 | Evidence qualification shape in #5; adequacy review in #7 | Require support/challenge/context and source locator once schema is pinned; evidence presence cannot prove truth or endorsement. |
| C-13 | Scale/version/dimension joins in #5; interpretation review in #7 | Pin unit, scale version and selected dimension, including missing and conversion policy. |
| C-14 | Core-boundary admission in #5; external-bridge decision in #8 | Reject the three optional catalog notions as managed core classes; any import/bridge needs a separate ownership decision. |
| C-16 | Raw, managed and task-ready SHACL profiles in #5 | Approve required identity, title, provenance and task inputs; an incomplete raw record is not automatically an invalid managed record. |
| C-17 | Assertion qualifier shape in #5; scalar export rule in #12 | Preserve multiple values with context/time/provenance and specify any one-value selection policy. |
| C-18 | Task comparison shape in #5; governed calculation and interpretation in #7/#12 | Matching numbers or labels cannot alone establish comparability across methods, scales or times. |
| C-19 | Workflow scheme/version shape in #5; transition behavior in #12 | Check recorded authorization and transition rules; undefined transitions remain UNKNOWN. |
| C-21 | Computed/reported score shape in #5; formula test in #12 | Approve score kind, required inputs, method pinning and formula before asserting computed correctness. |

The newly exercised C-06, C-08 and C-25 still need **explicit-data** counterparts in #5: resolve actor identity and named mediation participants; check named threshold anchors plus dual-anchor compatibility; check named `versionOf` targets and agreement with any direct artifact references. Their HermiT PASS rows do not discharge those separate tasks.

**Subsequent evidence:** the first [SHACL report](../shacl/report.md) now exercises explicit-data C-06/C-09/C-25 within a declared profile and the structural portion of C-08. C-08 compatibility remains PARTIAL/BLOCKED. C-09 therefore has alternative explicit-data evidence, while its HermiT row stays NOT_RUN. The [profile review](../shacl/profile-review.md) defines publication focus and identity policy; independent grounding and interpretation are still pending.

## Next executable batch

Continue #5 with the 254 ordered endpoint obligations, then catalog admission and the remaining rows above. For each fixture, record the data graph, shapes graph, focus population, inference policy and the exact violated shape. Keep positive, negative and boundary results separate from this HermiT receipt and reconcile requirement/CQ evidence in #6. Independent semantic adequacy remains #7.
