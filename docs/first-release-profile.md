# First release profile and gates

Target a **reviewed development prerelease of conceptual design 0.3.1**, provisionally `v0.3.1-rc.1`. This is a proposed package designation, not an existing tag or a claim of stable scientific validation. The first published release must point to an immutable source commit and declare the exact package inventory, digests, checks and limitations. Keep the first release small: conceptual source, native exchange, bounded OWL export, readable reference, requirements, evaluation receipts and reproducibility instructions.

## Decisions and blocking gates

| Gate | Current evidence | Action before the first release |
| --- | --- | --- |
| Rights and citation | [RIGHTS.md](../RIGHTS.md) explicitly says no repository-wide license, DOI or final citation metadata. | Rights holder selects the actual license scope, resolves third-party items and verifies author/title/version/date in citation metadata. Publish no assumed license or placeholder DOI. **Blocking.** |
| Evidence and claims | The [candidate claim inventory](../evaluation/release-claims.md) lists HermiT's 281/295, SHACL's 341 scoped PASS, one PARTIAL and 17 NOT_RUN of 359, and every open formal route. [C-14 review](../evaluation/c14-boundary-review.md) reuses prior evidence without adding engine coverage. | Review the final wording and limits at the exact release commit; preserve C-08 and all unrun routes. Do not label module coverage overall semantic validity. **Blocking until freeze review.** |
| Generated reference and links | [Local reference](site/index.html) takes its HermiT/SHACL figures from matching receipts; its nine relative links resolve locally. As observed on 22 October 2026, the native Wiki exists but contains only an initial one-line Home page; the curated source pages are ready for synchronization. Repository metadata reports `has_pages=false`. | Synchronize Wiki, verify its rendered pages and links, enable/deploy Pages and read back the public URL when access allows. Until then, make no live-publication claim. **Blocking for a public-reference claim.** |
| Freeze and reproduction | Model and 359-row SHACL contract are pinned; individual module receipts exist. This C-14 reconciliation is source-bound. | On the proposed release commit, run required clean checks, verify receipts and public file inventory, produce SHA-256 manifest and release notes, then read back public files and tag. **Blocking.** |

## Explicit prerelease limits

The first package can report executed formal modules and a bounded typed-core mapping without closing every parent research issue. Open #4/#5 routes, requirement/CQ acceptance (#6), independent semantic review (#7), standards interpretation (#8), full quality synthesis (#11), relational implementation (#12), manuscript (#14) and future extensions (#16) stay openly tracked. They are not counted as accepted claims. A stable scientific release requires a separate decision and stronger evidence. The Wiki (#9) and Pages (#10) must be reported according to actual publication/readback rather than the existence of local source files.

## Convergent sequence

1. Complete the rights/citation decision and claim-based evidence summary, with exact unresolved obligations.
2. Refresh the public reference and Wiki/Pages routes; verify rendered content and URLs where publishable.
3. Freeze a source commit, rerun required checks in a clean environment, record inventory/checksums and issue release notes.
4. Publish the prerelease tag only after the blocking gates pass, then read it back. Update #15 with the exact evidence and limitations.

Any change to the model, mapping, source contract or generated pages after freeze requires a new build and check run. This profile makes no DOI, certification, completeness or independent-review claim.
