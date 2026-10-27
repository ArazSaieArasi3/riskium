# Riskium v0.3.3

Bounded stable source distribution of unchanged ontology **0.3.1**, ORSD **0.4.3** and accepted manuscript **7.0.8**. This package consolidates completed engineering and documentation work after v0.3.2. It does not change the original scientific scope or owner decisions.

## Selected components

The [24-component matrix](../releases/distribution-v0.3.3.json) retains the ten accepted components and eight earlier engineering supplements, then explicitly selects:

| Component | Version and scope |
| --- | --- |
| SQLite assessment correction | 0.3.0, additive migration 4; immutable same-identity correction lineage and 36 fixed scenarios. Source/scenario mapping and general assertion correction remain open. |
| WebVOWL | 0.1.0; the asserted OWL graph, with explicit omitted-axiom inventory and recorded runtime/browser provenance. |
| Formal reference | 0.1.0; reading and evidence routes for all 25 interpretation constraints. No new scientific engine run. |
| Cross-document traceability | 0.1.0; completed audit #39, 423 source-bound rows and six resolved findings. Final-source inventory/checks are rerun rather than relabeling the dated audit receipt. |
| Documentation | 0.2.0; new frozen route `releases/v0.3.3`, derived from exact audited explanatory source `e574f19dea81f58a7112ded67fe02452ece2e8bd`, for model 0.3.1. All earlier documentation snapshots remain unchanged. |
| Rights and model citation | Existing model-0.3.1 metadata; separate distribution identity. |

Documentation 0.2.0 preserves the audited pre-publication checkpoint, including its then-current v0.3.2 status and planned #41. Its explicit source/version banner makes that chronology visible. Current guides can later record publication completion without rewriting this snapshot. Author-facing Word/PDF and historical private database binaries remain outside the public source archive.

## Release gates and verification

The exact clean final source must pass all 28 aggregate checks, the separately executed software regressions and component/hash compatibility validation. Fresh native Wiki Git plus actual HTTPS bytes must match the 23 selected Wiki files, all 68 current files and every registered frozen snapshot. Six release assets bind the tracked source archive, complete per-file inventory, freeze receipt, component matrix, notes and SHA256SUMS.

A new Draft is downloaded and validated before final/latest designation. A separate job downloads the final assets again and verifies checksums, archive contents, exact tag/source and Latest state. Preservation covers **all nine** previous releases, including stable v0.3.2, and their tag commits/assets. An ordinary subsequent push cannot repeat publication. Failed or queued gates never count as success.

## Retained evidence limits

Historical HermiT remains 281 PASS / 14 NOT_RUN; historical SHACL remains 341 scoped PASS / one PARTIAL / 17 NOT_RUN. Later finite replays retain their own populations. The 250 incomplete SQL core mappings, eleven external elements and eleven WITHHELD organizational case admissions remain explicit. Independent reviewer ratings remain zero. No full FOL package, complete native rule coverage, generic workflow/formula engine, PostgreSQL/private migration, production or human acceptance is claimed.

Next: #35/#12 source/scenario and general correction mapping; #4/#5 remaining formal/application policies; #37/#13 source/case adequacy; #23 independent judgment; #36 deployment acceptance. These wider objectives do not block this bounded distribution.

## Reproduce

Install `tools/requirements-shacl.txt` and `tools/publication/requirements.txt` in a clean exact checkout. Run `python tools/prepare_stable_release.py --tag v0.3.3 --output /absolute/empty/path/out` with output outside the checkout. This performs actual live documentation checks and all aggregate gates before packaging. The profile and matrix must match; existing tags, assets and snapshots cannot be replaced.
