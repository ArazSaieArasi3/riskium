# First release profile and gates

The first **development prerelease, [v0.3.1-rc.1](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.1-rc.1)**, was published on 22 October 2026. It freezes conceptual design 0.3.1 at `cfb85905ab37549c7090f00a41ca62cdd3364ab5`. It is not a stable scientific validation or production-readiness claim. The four release assets preserve the source archive, exact tracked-file inventory, fresh final-freeze evidence and checksums. Post-release documentation on main does not move the tag.

## Completed development-prerelease gates

| Gate | Completion evidence |
| --- | --- |
| Rights and citation | Project owner approved CC BY 4.0 for original scientific artifacts and MIT for original software. LICENSE, RIGHTS.md and NOTICE.md define distinct scopes and exclusions. AUTHORS.md matches manuscript 7.0.6's three ordered authors and affiliations. CITATION.cff is CFF 1.2.0 schema-valid. No DOI, ORCID or article publication is invented. |
| Evidence and claims | Final run at the tagged commit passed 693 HermiT cases and reproduced all five SHACL modules. Results, obligation outcomes and coverage matched historical receipts. HermiT retains 14 NOT_RUN; SHACL retains 341 scoped PASS, 1 PARTIAL and 17 NOT_RUN of 359. C-08 and all open routes remain explicit in the release notes and claim inventory. |
| Public reference and Wiki | Pages run 39829909477 succeeded for the release source. Live readback found 11 navigation links, working filtering and the license/author notices. Wiki head 709bcf003a43b692eb543d21fa0c61546e5e0d15 rendered the new notices and all seven curated files matched docs/wiki byte for byte. These public routes remain mutable; the tagged source is the immutable reference. |
| Freeze and reproduction | A clean detached checkout and newly installed pinned environment completed all 21 commands and 79 regressions successfully. Fresh reports, graphs, command logs and comparison/readback receipts are in the 93-file freeze-evidence asset. Historical source receipts retain their actual provenance. |
| Inventory and publication | All 149 tracked files (18,504,728 bytes) in the source archive matched source-manifest.json. The tag resolves to the exact release commit. GitHub reports draft=false and prerelease=true; all four uploaded asset sizes and SHA-256 digests match local verified files. Issue #15 records final completion. |

## Explicit limits and next milestone

The first package can report executed formal modules and a bounded typed-core mapping without closing every parent research issue. Open #4/#5 routes, requirement/CQ acceptance (#6), independent semantic review (#7), standards interpretation (#8), full quality synthesis (#11), relational implementation (#12), literature case acceptance (#13), manuscript (#14) and future extensions (#16) stay openly tracked. They are not accepted claims. #9 is complete; #10 remains open for a justified explorer and broader interface checks.

Next, reconcile requirement/CQ acceptance in #6 and align the manuscript with the exact released evidence in #14; continue formal/semantic work under its own issues. A stable scientific release requires a separate review and stronger evidence. Corrections use a new version; published tags and evidence are not moved to hide changes. See the [prerelease specification](prerelease-v0.3.1-rc.1.md) and [release checklist](release-checklist.md).
