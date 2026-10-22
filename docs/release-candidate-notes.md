# Riskium 0.3.1 development prerelease: candidate notes

This is a review draft for a possible `v0.3.1-rc.1`, **not a release or tag**. The release commit, rights decision, citation metadata, final clean rerun and checksum manifest are still pending. The [release profile](first-release-profile.md) controls the gates.

## Proposed package and claims

The GitHub source archive will contain the exact tracked tree of the release commit. Primary entry points are the [structured conceptual model](../ontology/riskium-model.json), [native exchange](../ontology/native/riskium.ontouml.json), [bounded OWL mapping](../ontology/derived/riskium.owl.ttl), [selected](../diagrams/selected-view.svg) and [complete](../diagrams/complete-view.svg) conceptual views, [requirements](../requirements/ontology-requirements.md), [candidate claim inventory](../evaluation/release-claims.md), [evaluation receipts](../evaluation/README.md), [generated reference](site/index.html) and [reproduction guide](reproducibility.md). The native [Wiki](https://github.com/ArazSaieArasi3/riskium/wiki) is a separate Git repository; its last source-matched publication was `55d80eb` and must be checked again at release freeze. Pages is deployed from `main` `/docs`, so its URL is mutable and must be read back at the release commit.

Permitted wording at the present source: conceptual design 0.3.1; 80 catalog concepts, of which 77 are in the typed core and three are optional phenomenon boundaries. The bounded OWL mapping and native exchange have documented engineering checks. The HermiT suite passed 693 executed cases covering 281 of 295 baseline reasoner obligations, with 14 engine-specific constraint routes NOT_RUN. The SHACL ledger records 341 scoped PASS, one PARTIAL and 17 NOT_RUN of 359 obligations. These denominators and the full open-route list are in the [generated claim inventory](../evaluation/release-claims.md).

Do not claim complete semantic validity, independent expert acceptance, full managed-record or risk-assessment readiness, a working database, a complete OWL representation, or an ontology explorer. C-08 compatibility, other open constraint routes and full multi-relation integration remain explicit. An independently reviewed scientific release is a later decision.

## Rights and citation decision

| Item | Observed state | Decision needed from the rights holder |
| --- | --- | --- |
| Conceptual model and requirements | The public repository has no repository-wide license or verified author list. | Confirm ownership and the license and scope for model and requirements. |
| Documentation, generated reference and SVG diagrams | These are derived from the model; the two SVGs have no embedded image elements or external image references. This inspection does not establish ownership of every imported idea or asset. | Confirm permission and the license for text, diagrams and generated views; identify any third-party attribution or exclusion. |
| Validation code and recorded outputs | Python tools, tests and optional pinned Python/npm dependencies are present; dependency packages are not committed as vendored source. | Confirm the code/output license scope and any notices needed for included material. Dependency licenses remain separate. |
| Citation | The Wiki uses “Riskium: An Ontology for Risk Knowledge” as its heading; version 0.3.1 is the conceptual design version. No DOI is assigned. | Verify final title, ordered authors and affiliations, publication year/date and preferred citation text. Include ORCIDs only if supplied and verified. Do not invent a DOI. |

No license or `CITATION.cff` is added by this draft. Public readability is not a reuse license; see [RIGHTS.md](../RIGHTS.md).

## Preflight and release freeze

At commit `12bcb05`, `validate_model.py`, `review_coverage.py`, `build_owl.py --check` and 79 regression tests passed on 22 October 2026. The Pages deployment for that commit also succeeded. This is a preflight; it did not rerun the HermiT engine or all SHACL module fixtures in a fresh environment and is **not** the final release-commit receipt.

After rights and citation are resolved, commit their exact files and finalize these notes. Freeze one commit; run the documented checks and selected engines in fresh pinned environments; compare generated artifacts and receipts; then generate a SHA-256 inventory with `python3 tools/build_release_manifest.py --ref <full-release-commit> --output <manifest-outside-repo>.json` and verify it with `--verify`. The manifest covers all tracked files at the pinned commit, excluding the separate Wiki Git history and untracked files. Review public Pages/Wiki content and the exact source archive before creating the tag and release. Record any remaining limitations in the published release notes; use no placeholder DOI.
