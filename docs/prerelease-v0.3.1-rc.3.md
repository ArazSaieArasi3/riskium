# Riskium v0.3.1-rc.3 development prerelease

## Goal and delivered behavior

Deliver one bounded C-08 improvement: compare explicit indicator/scale interpretation declarations for caller-selected dual-anchor thresholds. Application profile **0.6.0** distinguishes compatible declarations, known mismatches, incomplete/unresolved evidence and malformed input. Numeric metadata use exact canonical-unit identity with no conversion; qualitative metadata require matching declared scheme/term-set/version identities without invented numeric units. Different resource names alone are not evidence of distinct meanings. No native conceptual relation, class, definition or OWL axiom changes.

The [policy and review](https://github.com/ArazSaieArasi3/riskium/blob/v0.3.1-rc.3/evaluation/shacl/compatibility/profile-review.md), [machine-readable policy](https://github.com/ArazSaieArasi3/riskium/blob/v0.3.1-rc.3/evaluation/shacl/compatibility/profile-policy.json), [readable report](https://github.com/ArazSaieArasi3/riskium/blob/v0.3.1-rc.3/evaluation/shacl/compatibility/report.md) and compressed full receipt retain exact expectations, source hashes, caller focus, raw/effective/shapes/result graphs, runtime and selected integration evidence. Five cases combine the new module with selected endpoint and catalog metadata rules; missing domain types are not repaired by the record envelopes.

## Executed evidence

- **41 fixed author-written scenarios matched their exact expected outcome**: **37 actual SHACL validations**, **4 expected preflight rejections**, **5 selected integration cases**, **2 deleted-rule controls**. The mutation and raw-staging cases are controls, not newly compatible real risk cases.
- **108 software regressions** passed locally before the release request. The candidate workflow independently runs all software regressions and the full compatibility receipt replay, plus existing synthetic CQ and source/documentation checks. Actual hosted command outputs determine its gate results.
- The compressed receipt was regenerated from the committed implementation source. Its source/input hashes bind the exact executed code, policy, ontology, shapes and unchanged historical coverage ledger. The release source includes that receipt as new evidence.
- The historical HermiT and five earlier SHACL module receipts are retained. There is **no new HermiT run**. New compatibility SHACL execution/replay is explicitly distinguished from those historical modules and from software regression engine calls.

## Preserved limits and manuscript impact

Global C-08 remains **PARTIAL**. The original historical blocked task is not rewritten. The original fixed ledger remains **341 scoped PASS, 1 PARTIAL and 17 NOT_RUN / 359**; new application evidence is a supplement, not an artificial extra ledger PASS. The frozen quality synthesis retains its actual checkpoint and scope. Manuscript 7.0.7's bounded C-08/full-acceptance limits remain accurate; no article binary is edited or published in this packet.

This profile does not evaluate numeric boundary values/comparators, qualitative term order, physical conversions, external source truth, contextual adequacy or full risk-assessment readiness. Independent semantic acceptance remains unestablished; author fixtures do not substitute for expert judgments. Parent #5 remains open for its remaining routes and complete required integration. #4/#7/#12/#13 and future #16 remain separately tracked.

## Final-release exit and next packet

[Final-release MUST gates](https://github.com/ArazSaieArasi3/riskium/blob/v0.3.1-rc.3/docs/stable-release-gates.md) now specify the exit from development prereleases. Target **v0.3.1** is conditional on the unchanged model baseline, explicit acceptance/disposition of all retained in-scope claims/routes, required formal/data/application/CQ evidence, actual independent review, no unresolved critical findings and one clean final stabilization/freeze. The earliest planned decision point is after the rc.7 review packet, provided the earlier packets' release-critical residual work is also resolved. Rc numbers alone do not satisfy those gates; future extensions #16 are nonblocking.

Next bounded packet: **rc.4 under #4**, targeting [C-13/C-18 scale selection and exact comparison routes](https://github.com/ArazSaieArasi3/riskium/blob/v0.3.1-rc.3/docs/next-release-v0.3.1-rc.4.md). Predeclare the task/schema and execute selected valid/invalid/incomplete/mutation cases through the appropriate method. Preserve HermiT NOT_RUN unless a real HermiT execution discharges that exact obligation; alternative evidence retains its own method and limitations.

## Package and publication

Five assets: exact tracked source archive, source-manifest.json, candidate-receipt.json, release-notes.md and SHA256SUMS.txt. The source archive contains the new compatibility receipt; private manuscript/database companions remain outside this public package. Earlier rc.1/rc.2 tags and assets are not moved or replaced. The source commit records a publication request; the actual GitHub Release, successful workflow and independent asset/tag readback establish publication. This is a development prerelease, not stable or production certification.
