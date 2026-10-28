# Riskium v0.3.5 — prospective source distribution

**RELEASE_SUPPORT_NOT_FROZEN.** The published Latest stable distribution is v0.3.4. This document describes the target v0.3.5 package; no v0.3.5 tag, source freeze, public assets or publication is established by this support packet.

## Purpose and selected changes

v0.3.5 consolidates the bounded EvidenceReference lifecycle implementation with current source/paper accounting and documentation. It keeps the accepted conceptual/scientific baseline and earlier published source distributions intact.

| Component | Selected version | Supported change |
| --- | --- | --- |
| Evidence-reference lifecycle | 0.7.0 / schema migration 8 | Same-artifact correction branches, context-scoped SELECT/WITHDRAW/CLEAR and explicit as-of history for already represented issued C065 versions |
| Current consistency | 0.3.0 | 450 accounting routes, including the unchanged 423-row historical trace; 39 declared current claim routes |
| Current documentation | 0.4.0 | Current source guides, 23 Wiki projections and separate generated Pages bindings; four earlier snapshots preserved |

The [exact selection](../releases/selection-v0.3.5.json) records 29 current components, 687 unique selected source files and 68 current dependency edges. Twenty-six prior component rows remain byte-identical; two current rows are replaced and one is added. Original documentation 0.3 / consistency 0.2 snapshot-generation rows and edges remain separate historical provenance. All 380 v0.3.4 selected file bindings and 237 files across four frozen snapshots are preserved.

## Offline verification of the unpacked source

Use Python 3.12 or later. The verification commands use only the Python standard library and do not invoke Git or the network.

```sh
python -B tools/prepare_release_v035.py --check-profile
python -B tools/prepare_release_v035.py --check-unpacked /path/to/unpacked-source --manifest /path/to/source-manifest.json
```

The first command verifies the prospective profile, anchored selection, selected payloads and required support tooling. The second also verifies the complete supplied manifest against the actual unpacked file set, sizes and SHA-256 values. Keep source-manifest.json outside the unpacked source directory. The unpacked source must contain no Git metadata, symbolic links or extra generated files. A profile-only check does not establish a complete archive inventory.

The validator rejects missing or changed selected sources, omitted release tooling, wrong selection/receipt versions, unsafe or duplicate manifest paths and a recomputed manifest that omits required payloads. The profile is deliberately outside the publication registries. Integrity checks do not authenticate an arbitrary modified validator: after publication, obtain the release's source identity and asset digests from the independently verified publication record.

## Final gates before publication

This support packet declares the following subsequent work; it does not record those gates as executed:

1. Select the final clean source and replay affected component, migration, accounting and full software checks.
2. Independently read back actual native Wiki and all relevant served Pages bytes against that source, with timestamps, exact source identity and preserved snapshots. Retained #55 receipts remain bound to their original source.
3. Execute the exact-source dry freeze and independently inspect six staged assets: source archive, source manifest, artifact versions, freeze receipt, release notes and checksum list.
4. Activate only the reviewed new v0.3.5 publication, then independently download and verify all six public assets, tag/Latest and all eleven prior release inventories.

## Scientific and application scope

Native model 0.3.1, ORSD 0.4.3, original DRSD 0.1.0 and approved manuscript 7.0.8 are unchanged. All 306 native IDs retain their dispositions; 236 elements remain deferred. The 450 trace rows are accounting routes, not 450 successful scientific tests. Later engineering is NOT_CLAIMED_IN_PAPER.

Historical HermiT outcomes remain 281 PASS / 14 NOT_RUN of 295; historical SHACL outcomes remain 341 scoped PASS / one PARTIAL / 17 NOT_RUN of 359. This packet does not relabel those receipts as fresh complete engine runs. All eleven organizational admissions remain WITHHELD and actual independent semantic ratings remain zero. The owner-approved bounded scope is retained without new owner responses.

General native assertion semantics, reinstatement, R-69..R-72, broader rules/workflow/formulas, PostgreSQL/private migration and deployment retain their separate issue criteria. Conference submission still requires supported contribution/case claims, actual independent semantic scrutiny, final manuscript/reproduction, venue/track/deadline/policies and coauthor approval.

Scientific content retains CC BY 4.0 and original software MIT under the existing scopes, third-party exclusions and authors' respective contributions. See [RIGHTS](../RIGHTS.md), [NOTICE](../NOTICE.md), [AUTHORS](../AUTHORS.md) and [citation metadata](../CITATION.cff). Native model citation 0.3.1 is unchanged.
