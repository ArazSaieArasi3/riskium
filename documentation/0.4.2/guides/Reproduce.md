# Reproduce a specific result

Begin with the exact artifact and source you want to inspect. The published **[v0.3.5 source](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.5)** contains the code, fixed expectations and saved receipts for that release. A new run has its own source and runtime; it does not replace the historical evidence automatically.

## Get and verify the release

Download all six assets from the exact release page into one directory. From that directory:

```bash
sha256sum -c SHA256SUMS.txt
tar -xzf riskium-v0.3.5-source.tar.gz
```

Expected result: the five listed payloads report `OK`. Inspect `source-manifest.json` for the archived paths and exact source identity. The [publication record](https://github.com/ArazSaieArasi3/riskium/issues/59) reports independent byte checks for all 1,107 archived source files. `freeze-receipt.json` records the earlier freeze phase; the publication record supplies the later public-download evidence.

## Run the public software checks

For Git-aware source and documentation checks, use a full Git checkout, then select the release:

```bash
git checkout v0.3.5
git rev-parse HEAD
python -m venv .venv-shacl
. .venv-shacl/bin/activate
python -m pip install -r tools/requirements-shacl.txt -r tools/publication/requirements.txt
python tools/run_relational_source_scenario.py --check
python tools/run_relational_source_scenario_lineage.py --check
python tools/run_relational_evidence.py --check
python tools/run_relational_evidence_lifecycle.py --check
python tools/audit_current_alignment.py --check
python -m unittest discover -s tests -v
```

`HEAD` should be `8a9a95bba17327d04c5560879819b2e61b48ff19`. At publication, the full software suite passed **495 tests**; the four SQL populations contained **54, 54, 62 and 43 fixed controls**, respectively. Runners compare their observed results with the declared expectations and fail on differences. Runtime-specific values follow each receipt's rules. The 28 core checks and 13 release checks are separate gates, not an additional count of independent scientific experiments.

An extracted source archive supports its documented offline checks; commands that inspect Git history need a full checkout. [The formal-method guide](Formalization.md) identifies reasoner/SHACL prerequisites and commands separately. Running this software sequence does not repeat every historical engine experiment.

## Rebuild the maintained documentation

To inspect the unreleased assessment selection work, check out the [exact development commit](https://github.com/ArazSaieArasi3/riskium/commit/12fb2011801fe47f3245f3f7367952bc0e749448) in a separate full clone. With the Python dependencies installed, run `python tools/run_assessment_selection.py --output build/asl-report.json`, `python tools/audit_assessment_alignment.py --check`, and `python -m unittest discover -s tests -p test_assessment_alignment.py -v`. The first command should report **44 PASS, zero FAIL and zero ERROR**; the alignment check should report **460 routes**. These are development results on synthetic fixtures. They do not alter the exact v0.3.5 release checks below.

Documentation 0.4.1 lives after the source-release checkpoint. Use a full checkout of the documentation commit named in the page's source record, install `tools/publication/requirements.txt`, then run:

```bash
python tools/publication/published_documentation.py --check
python tools/publication/published_documentation.py --output build/published-site
```

Expected result: local guide, link, source-binding and frozen-snapshot checks pass, and a static site appears under `build/published-site`. This builds a local package. Live publication agreement requires separate actual Wiki/HTTP readback.

## Private files and troubleshooting

The approved manuscript 7.0.8 was checked against the actual Word/PDF files. Public CI checks its hash-bound receipt; it does not retrieve private author files. `tools/read_current_manuscript.py --directory /path/to/approved/files --check` requires those approved binaries. Historical private database/pharmaceutical evidence remains archived evidence.

If Git-history checks fail, verify that the checkout includes the pinned history and that dependencies were installed in the active environment. If checksums fail, obtain the exact release assets again and investigate before using the files. [Limitations](Limitations.md) distinguish reproducible engineering results from scientific acceptance.
