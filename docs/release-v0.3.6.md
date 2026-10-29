# Riskium v0.3.6: context-qualified assessment selection

This source distribution adds an explicit choice of an issued assessment version
for one application decision context, while preserving its complete result bundle
and documentary history. Corrections do not silently select a replacement. A
withdrawal reports WITHDRAWN without falling back to another version; independent
contexts and explicit historical ledger queries retain their own answers.

| Artifact | Selected version and scope |
| --- | --- |
| Source distribution | v0.3.6, exact source in the manifests |
| Assessment-selection profile | 0.8.0, SQLite schema 9; internal Python API |
| Current traceability | 0.4.0, 460 accounted routes |
| Reader checkpoint | 0.4.2, reviewed Wiki and Pages at R4 |
| Native model and bounded exports | 0.3.1 |
| Original ORSD / DRSD | 0.4.3 / 0.1.0 |
| Approved manuscript | 7.0.8; new selection routes are NOT_CLAIMED_IN_PAPER |

The selected matrix contains 30 components: 27 retained, two replaced and one
added. All 687 selected v0.3.5 source-file hashes are preserved. Original
declarations, prospective NOT_RUN/NOT_REVIEWED fields and dated R2/R3 receipts
remain checkpoints; the later R4 observations and final freeze evidence are
separate records.

## Verify the distribution

Download all six assets together. Run `sha256sum -c SHA256SUMS.txt`, then extract
`riskium-v0.3.6-source.tar.gz`. The archive has a `v0.3.6/` directory. The manifest
records every committed source file, its size, mode and SHA-256. From the extracted
directory, run:

```sh
python tools/release_v036.py verify --folder /path/to/the/six/assets
```

The verifier uses the Python standard library and needs no Git history or Git
executable. Checksums establish internal agreement; compare the downloaded assets
with the trusted external publication or authenticated artifact digest as well.
`freeze-receipt.json` retains its prepublication phase, even after publication.
The later public-download verification belongs to the release completion record
in [#61](https://github.com/ArazSaieArasi3/riskium/issues/61).

## Evidence and interpretation

The 44 assessment controls use concrete synthetic data and fixed expectations
declared before implementation. Twelve additional API/recovery regressions and
the unchanged historical software suites have separate populations. The final
source-qualified suite and actual Wiki/Pages readback are authenticated by their
GitHub run and artifact identities in the freeze receipt.

Documentation 0.4.2 is the R4 prepublication reading checkpoint. Its references to
v0.3.5 as published and v0.3.6 as a candidate retain that dated meaning. For this
distribution's selected versions, use these release notes and `artifact-versions.json`.
Reader-channel maintenance after publication is a separate status update.

Engineering and reader evidence does not establish full semantic correctness,
production readiness, authenticated organizational authority or scientific
acceptance. All eleven organizational admissions remain WITHHELD; independent
semantic ratings remain zero. The model, scientific claims and manuscript retain
their previous bounds. Research content is CC BY 4.0 and original software is MIT,
subject to the retained rights and third-party notices.
