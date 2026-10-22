# First release profile and gates

Target a **reviewed development prerelease of conceptual design 0.3.1**, provisionally `v0.3.1-rc.1`. This is a proposed package designation, not an existing tag or a claim of stable scientific validation. The first published release must point to an immutable source commit and declare the exact package inventory, digests, checks and limitations. Keep the first release small: conceptual source, native exchange, bounded OWL export, readable reference, requirements, evaluation receipts and reproducibility instructions.

## Decisions and blocking gates

| Gate | Current evidence | Action before the first release |
| --- | --- | --- |
| Rights and citation | Project owner approved CC BY 4.0 for original scientific artifacts and MIT for software; [RIGHTS.md](../RIGHTS.md), [NOTICE.md](../NOTICE.md), [AUTHORS.md](../AUTHORS.md) and [CITATION.cff](../CITATION.cff) record scopes, exclusions and manuscript-matched authors/affiliations. | Decision implemented on 22 October 2026. Preserve the artifact scopes and exclusions in the frozen package and public pages. No DOI or unpublished article metadata is invented. **Decision gate met.** |
| Evidence and claims | The [candidate claim inventory](../evaluation/release-claims.md) lists HermiT's 281/295, SHACL's 341 scoped PASS, one PARTIAL and 17 NOT_RUN of 359, and every open formal route. [C-14 review](../evaluation/c14-boundary-review.md) reuses prior evidence without adding engine coverage. | Review the final wording and limits at the exact release commit; preserve C-08 and all unrun routes. Do not label module coverage overall semantic validity. **Blocking until freeze review.** |
| Generated reference and links | The [public reference](https://arazsaiearasi3.github.io/riskium/site/) was first deployed from commit `6ca90cc` via `main` `/docs`; the Pages run succeeded and the entry redirected to the rendered reference with nine repository links and scoped coverage notices. The [native Wiki](https://github.com/ArazSaieArasi3/riskium/wiki) contains six pages and `_Sidebar.md`; its head `55d80eb` was cloned and all seven files matched the curated source from `0021111` byte for byte on 22 October 2026. | Public reference and Wiki publication/readback gate met for the development prerelease. A separately justified ontology explorer and broader mobile/download review remain in #10; they are not claimed as delivered in this package. |
| Freeze and reproduction | Model and 359-row SHACL contract are pinned; individual module receipts exist. A full clean rehearsal at `313c967` reproduced 79 regressions, 693 HermiT cases and all five SHACL modules in fresh pinned environments; results matched the historical receipts. `tools/build_release_manifest.py` inventories an exact Git commit. | On the proposed release commit, run required clean checks, verify receipts and public file inventory, produce SHA-256 manifest and release notes, then read back public files and tag. The preflight is not the final clean rerun. **Blocking.** |

## Explicit prerelease limits

The first package can report executed formal modules and a bounded typed-core mapping without closing every parent research issue. Open #4/#5 routes, requirement/CQ acceptance (#6), independent semantic review (#7), standards interpretation (#8), full quality synthesis (#11), relational implementation (#12), manuscript (#14) and future extensions (#16) stay openly tracked. They are not counted as accepted claims. A stable scientific release requires a separate decision and stronger evidence. The Wiki publication work in #9 is complete; #10 remains open for explorer and broader interface checks despite the deployed reference.

## Convergent sequence

1. Preserve the approved rights/citation decision and claim-based evidence summary, with exact unresolved obligations.
2. Preserve the verified Wiki and Pages routes in the package inventory; review public links at the frozen release commit.
3. Freeze a source commit, rerun required checks in a clean environment, record inventory/checksums and issue release notes.
4. Publish the prerelease tag only after the blocking gates pass, then read it back. Update #15 with the exact evidence and limitations.

Any change to the model, mapping, source contract or generated pages after freeze requires a new build and check run. This profile makes no DOI, certification, completeness or independent-review claim.
