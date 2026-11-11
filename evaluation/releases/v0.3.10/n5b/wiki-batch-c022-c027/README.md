# W3: native Wiki C022–C027

Date: 11 November 2026. This six-page documentary batch is complete within the remaining coordinated-publication gate for the already published v0.3.10 (#85). The broader channel gate remains open.

## Observed checks

| Check | Actual result |
|---|---|
| Verified reference | Reused the retained deployed reader artifact 13802387546 from run 42899912762. Its previously recorded ZIP SHA-256 is `22fcee8b647917d0235ca0af44ac35f565fca60a31ef4c533ede71db0b8b88dd`. All 114 reference-body SHA-256 hashes were freshly compared with the published expected inventory. The artifact was not downloaded again. |
| Source boundary | Release ID 440894153 binds scientific source `4ae0cdc72a1008e8107be320694d90324890b696` and documentary adapter `fb751343d19007c9fa8c43376181d8d1c5c2cb4f`. Scientific model 0.3.2, review 0.2.0 and reader 0.4.10 retain their declared roles. |
| Published scope | Saved C022 Risk Register Entry, C023 Entry Revision, C024 Risk Description, C025 Consequence Statement, C026 Identification Information and C027 Intake Channel Term through the native Wiki editor. Each editor value was checked before submission. |
| Browser recovery | C022 saved successfully despite a navigation-wait timeout; the updated page and revision appeared in fresh state. Slow edit navigation for C023/C024 was inspected rather than interpreted as a failed save. For later navigation, the actual observed link destinations were opened directly through the browser. Exactly six Wiki commits confirm that no repeated save created an extra batch revision. |
| Independent stored-content verification | Wiki commit `856d2cbeac2fe57877363030b57faa80d4eebda8` differs from `eb706c21c7fd77f9fc798b91d4e5d263b43e7f1f` in exactly the six declared paths. All six stored bodies match the expected hashes byte for byte; all twenty-two previously matching files remain equal, and no unexpected path was added. |
| Full inventory | [Readback](readback.json) covers all 114 expected files: 28 match, including twenty-seven updated concepts and one preserved historical reference; 86 remain. The batch is 6/6 complete. Cumulative synchronization is 24.6%, not an ontology-correctness percentage. |
| Previous CI completion | [CI receipt](previous-checkpoint-ci.json) records fifteen completed observed workflows at repository checkpoint `8b3c221ec044d3a8dbcf9cbceae9734d2c72ccd8`: eleven succeeded and four retired publishers were skipped. All three previously pending runs succeeded, including both full historical suites. No observed prior run remains pending or failed; these are workflow counts, not counts of individual tests or independent semantic judgments. |
| Preserved scope | No manuscript, scientific definition, frozen selected input, release tag or public release asset changed. Earlier release-download and HTTP Pages evidence retain their dates; neither full download nor HTTP acceptance was rerun by this Wiki-only batch. |

## Next bounded execution

Publish **C028–C033**, with at most two or three saves per browser call, then independently read back actual Git bytes and preserve the previously equal population. Inspect actual stored content before retrying any interrupted save. Continue with 49 remaining C-series concepts, six X-series concepts, nine aggregate/structural pages, twenty guides and two navigation files. Current Home/sidebar/footer are last. Close #85 only after all 114 expected bodies and final cross-channel current-pointer/navigation checks pass.

[W2 evidence](../wiki-batch-c016-c021/README.md), [W1 evidence](../wiki-batch-c010-c015/README.md) and [initial N5b readback](../wiki-readback.json) remain dated history. [Current progress](../progress.json) points to W3. Separate #78/#23 scopes remain open; H1–H3 remain paused.
