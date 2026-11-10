# Reproduction

Download the six files attached to [v0.3.9](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.9), preserving their names. The source archive is fixed to commit `ce0baefa3495d1bc3b42f56ad578154d5bc4f178`. Keep it distinct from GitHub's automatically generated source archives and from the later reader-delivery commit.

After extracting the source archive, use its standalone verifier against the directory containing all six downloaded assets:

```sh
python -I tools/releases/v039/package/verify_package.py --assets /path/to/assets --expected-source-commit ce0baefa3495d1bc3b42f56ad578154d5bc4f178 --expected-run-id 42776380967 --report verification.json
```

The offline verifier reconstructs the pinned commit/tree, checks the 2,091-file source archive, 1,213 selected bindings and scientific/reader/component agreement. Its historical `PASS_PACKAGE_NOT_PUBLISHED` label describes its offline scope; actual public availability is reported separately in the [publication receipt](https://github.com/ArazSaieArasi3/riskium/blob/ce0baefa3495d1bc3b42f56ad578154d5bc4f178/evaluation/releases/v0.3.9/R2a-outcome.md) and [live publication record](https://github.com/ArazSaieArasi3/riskium/blob/main/evaluation/releases/v0.3.9/publication.json).

For the full scientific engine replay, follow the [qualified workflow](https://github.com/ArazSaieArasi3/riskium/blob/ce0baefa3495d1bc3b42f56ad578154d5bc4f178/.github/workflows/issue93-candidate.yml) and its pinned dependencies. The [actual CI](https://github.com/ArazSaieArasi3/riskium/actions/runs/42776380967) retains separate qualification and packaging job outputs. Historical tests execute against their bound sources; do not run old source-specific assertions against an unrelated successor and call that a historical replay.
