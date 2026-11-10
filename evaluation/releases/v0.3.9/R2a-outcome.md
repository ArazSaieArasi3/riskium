# R2a complete: six prepared and independently verified package assets

**R2a is complete. Public release and maintained-channel publication remain R2b.**
The qualified source for package **v0.3.9** is commit
`ce0baefa3495d1bc3b42f56ad578154d5bc4f178` (tree
`34d29be464b36e33a33ed8e966662cb40dfb4ac0`). Its five scientific 0.3.2 bodies are
byte-identical to R1. One packaging component is added to the selection: **six
active components**, **32 historical components**, **1,213 selected file bindings**.
The original R1 selection and CI receipts retain their original source hashes.

[Actual CI 42776380967](https://github.com/ArazSaieArasi3/riskium/actions/runs/42776380967),
attempt 1, succeeded in both jobs. The package job runs only after exact-source
qualification succeeds and consumes that job's downloaded artifact. Fresh
selected-source qualification matched all 20 RiskCase expectations, with 13
SHACL and eight HermiT invocations plus native schema/SDK and OWL 2 DL checks.
The package job passed all 17 guard tests. Their synthetic adapter fixtures are
packaging controls, separately counted from scientific-engine evidence.

The prepared [CI package artifact](https://github.com/ArazSaieArasi3/riskium/actions/runs/42776380967/artifacts/13744371351)
contains exactly six assets:

| Asset | Purpose |
|---|---|
| riskium-v0.3.9-source.tar.gz | Preserves all 2,091 committed source files, their modes and versioned provenance. |
| source-manifest.json | Binds every source body and the complete Git commit/tree. |
| artifact-versions.json | Keeps active and historical components, versions and dependencies distinct. |
| freeze-receipt.json | Binds the actual same-source qualification and prepared asset hashes without claiming publication. |
| release-notes.md | Describes the selected contribution, supported checks and publication boundary. |
| SHA256SUMS.txt | Covers the other five assets; it does not contain a circular hash of itself. |

Both actual CI artifacts were downloaded and their API-reported SHA-256 digests
verified. The separate verifier checked the six assets in an isolated Python
process, without repository imports or ontology dependencies. It reconstructed
the entire Git tree and pinned commit from the archive and checked component,
source-contract, reader and qualification bindings. A separate local rebuild,
using the downloaded real CI qualification report, reproduced **all six assets
byte for byte**. The source archive SHA-256 is
`4d91158d02a1b058b6c8f371909d9030cfe7dbb9388beda881a791663488eca9`.

This is CI-artifact download verification, not a public-release download. The
[receipt](R2a-ci-receipt.json) and [offline verifier result](R2a-verification.json)
record the exact evidence. No release/tag, live Wiki/Pages update or issue closure
is inferred. Main and manuscript **7.2.21** are unchanged; article binaries,
independent semantic acceptance, a full database/PostgreSQL migration and
production performance are outside this preparation result.

## Next endpoint: R2b coordinated publication

Publish these exact six verified assets with the qualified source commit, then
download them through public release URLs. Reconcile and read back the affected
maintained README/Wiki/Pages entry points, source links and version roles,
including the frozen manuscript's own source role. Receipt-only descendants are
delivery metadata, not replacement archive sources. If selected inputs change,
rebuild and requalify before publication. Retain prior releases and a concrete
rollback path for maintained pointers. Close #92/#93 only after their own last
publication criteria pass; broader curation and research work remain separate.

[Packaging recipes and promotion checklist](../../../tools/releases/v039/package/README.md)
