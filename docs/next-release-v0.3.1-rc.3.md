# Next packet C-08 compatibility for v0.3.1-rc.3

Status: **implemented with scoped evidence; publication tracked in [#21](https://github.com/ArazSaieArasi3/riskium/issues/21)**. [Application profile 0.6.0](../evaluation/shacl/compatibility/profile-review.md) and [execution report](../evaluation/shacl/compatibility/report.md) deliver this bounded batch under [#5](https://github.com/ArazSaieArasi3/riskium/issues/5), after published v0.3.1-rc.2. All 41 scenario expectations matched: 37 actual SHACL validations and four expected preflight rejections, with five selected integration cases and two deleted-rule controls. Global C-08 remains PARTIAL; the historical ledger/blocked fixture are unchanged. The entire SHACL parent issue, all 17 NOT_RUN routes and the relational/case/independent-review projects are not included in this one packet. This record describes the original scope below; the linked receipt is the implementation evidence.

## Exact current gap

The conditional module accepts a structural threshold with an indicator anchor, a scale anchor or both. The source has RX-025 thresholdForIndicator, RK2-020 thresholdOnScale and RK2-019 scaleForDimension. It has no native Indicator-to-scale/unit/version relation or approved numeric unit schema. Consequently the dual-anchor task-ready case S-C08-TASK-DUAL-UNKNOWN is BLOCKED; current C-08 remains PARTIAL. A new property or equivalence must not be silently invented to obtain a passing test.

## Small deliverable

1. Define and review a versioned **application-record compatibility policy**, separating any supplementary indicator/scale-version/dimension/unit metadata from the unchanged native core. Declare caller focus, source/edition, aliases, missingness and the exact supported task. If a conceptual change is required, stop treating it as a documentation-only 0.3.1 package and version the reviewed model explicitly.
2. Begin with conservative exact matching: same declared scale version, dimension and canonical unit where numeric units apply. Unknown mappings and missing evidence remain NOT_READY or BLOCKED according to the declared profile; unequal labels are not proof of incompatibility or identity. Qualitative scales require their justified scheme/version/term interpretation without invented numeric units. Automatic conversions and wider equivalences are deferred unless separately justified and tested.
3. Predeclare positive, invalid, incomplete, conflicting/alias and deleted-rule mutation fixtures, with exact expected shape/component/focus outcomes. Include at least a compatible pair, a genuinely incompatible declared pair, missing compatibility evidence, qualitative-scale behavior and a mutation that would hide a mismatch. Use independently fixed expected outcomes for the declared rule; do not describe author-created fixtures as independent expert validation.
4. Execute the selected SHACL profile and one explicit interaction with existing endpoint/catalog rules. Preserve raw/effective data, shapes, source hashes, engine/inference/focus policy and expected/observed results. Reconcile the C-08 ledger and quality/manuscript claim implications without rewriting old receipts.

## Acceptance and release boundary

- The missing policy is explicit, versioned and distinguished from native ontology semantics.
- Valid, invalid and incomplete inputs produce the intended outcomes; a missing field does not become a fabricated value or a pass.
- Mutation/error controls and the selected integration batch pass with exact oracles.
- Unsupported conversions, remaining NOT_RUN routes and all independent-meaning limits remain visible. Do not promote PARTIAL to full PASS merely because a new set of fixtures passes.
- The scoped evidence, notes, source archive and assets support a new development prerelease. Closing this packet does not automatically close parent #5, change HermiT outcomes or establish full risk-assessment readiness.

The intended result is one independently inspectable compatibility improvement and its evidence. It is not a target percentage for global correctness, a whole-ontology semantic certification or a production application.
