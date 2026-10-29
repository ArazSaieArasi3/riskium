# Reproduce a specific result

Begin with the exact artifact and source you want to inspect. The published **[v0.3.6 source](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.6)** contains the code, fixed expectations and saved receipts for that release. A new run has its own source and runtime; it does not replace the historical evidence automatically.

## Get and verify the release

Download all six assets from the exact release page into one directory. From that directory:

```bash
sha256sum -c SHA256SUMS.txt
tar -xzf riskium-v0.3.6-source.tar.gz
python v0.3.6/tools/release_v036.py verify --folder . --source 58ff468ec4e8f3500ace6869601a25ea263c3d9f
```

Expected result: the five listed payloads report `OK`, and the extracted standard-library-only verifier reports `V036_SIX_ASSET_OFFLINE_PASS` without requiring Git. Inspect `source-manifest.json` for the archived paths and exact source identity. The [publication record](https://github.com/ArazSaieArasi3/riskium/issues/61#issuecomment-6507087968) reports independent byte checks for all 1,234 archived source files. `freeze-receipt.json` records the earlier freeze phase; the publication record supplies the later public-download evidence.

## Run the public software checks

For Git-aware source and documentation checks, use a full Git checkout, then select the release:

```bash
git checkout v0.3.6
git rev-parse HEAD
python -m venv .venv-shacl
. .venv-shacl/bin/activate
python -m pip install -r tools/requirements-shacl.txt -r tools/publication/requirements.txt
python tools/run_relational_source_scenario.py --check
python tools/run_relational_source_scenario_lineage.py --check
python tools/run_relational_evidence.py --check
python tools/run_relational_evidence_lifecycle.py --check
python tools/audit_current_alignment.py --check
python tools/run_v036_versioned_suite.py
```

`HEAD` should be `58ff468ec4e8f3500ace6869601a25ea263c3d9f`. At publication, the source-qualified suite passed **533 current tests and ten pinned historical reader tests**; the four SQL populations contained **54, 54, 62 and 43 fixed controls**, respectively. Runners compare their observed results with the declared expectations and fail on differences. Runtime-specific values follow each receipt's rules. The retained v0.3.5 28-core/13-release gate populations describe their historical checkpoint. The later v0.3.6 freeze binds its actual suite, reader and affected-check receipts separately; these are not additional independent scientific experiments.

An extracted source archive supports its documented offline checks; commands that inspect Git history need a full checkout. [The formal-method guide](Formalization.md) identifies reasoner/SHACL prerequisites and commands separately. Running this software sequence does not repeat every historical engine experiment.

## Synthetic two-context example

At published source `58ff468ec4e8f3500ace6869601a25ea263c3d9f`, with the dependencies above installed, run this from the repository root. The helper creates disposable synthetic data; use the managed-ID API in [Database assurance](Database-Assurance.md) for application integration.

```bash
python - <<'PYEXAMPLE'
import sys
sys.path.insert(0, "tools")
import run_assessment_selection as demo
import relational_assessment_selection as api

db = demo.fresh()
demo.timeline(db, through=4)
for context, boundary in (("X", 1), ("X", 2), ("X", 4), ("Y", 4)):
    answer = api.selection(db, demo.U("A"), context, boundary)
    version = answer["assessment_version"]
    short = version.removeprefix(demo.U("")) if version else None
    print(context, boundary, answer["state"], short)
db.close()
PYEXAMPLE
```

Expected output:

```text
X 1 SELECTED A-v1
X 2 SELECTED A-v2
X 4 WITHDRAWN None
Y 4 SELECTED A-v3
```

X's withdrawal preserves both earlier answers. Y keeps its separate selected bundle. A correction alone does not select a replacement. These are explicit ledger boundaries, not wall-clock inference.

## Rebuild the maintained documentation

At the exact v0.3.6 source above, run `python tools/run_assessment_selection.py --output build/asl-report.json`, `python tools/audit_assessment_alignment.py --check` and `python -m unittest discover -s tests -p test_assessment_alignment.py -v`. Expect **44 PASS, zero FAIL and zero ERROR**, and **460 accounted routes**. Those are bounded synthetic engineering outcomes, separate from the historical 54/54/62/43 populations. The published-source suite runner executes the ten frozen older reader tests at their own reviewed source; a direct unqualified discovery command does not resolve their historical publisher contract.

Documentation 0.4.3 lives after the source-release checkpoint. Use a full checkout of the documentation commit named in the page's source record, install `tools/publication/requirements.txt`, then run:

```bash
python tools/publication/released_documentation.py --check
python tools/publication/released_documentation.py --output build/released-site
```

Expected result: local guide, link, source-binding and frozen-snapshot checks pass, and a static site appears under `build/released-site`. This builds a local package. Live publication agreement requires separate actual Wiki/HTTP readback.

## Private files and troubleshooting

The approved manuscript 7.0.8 was checked against the actual Word/PDF files. Public CI checks its hash-bound receipt; it does not retrieve private author files. `tools/read_current_manuscript.py --directory /path/to/approved/files --check` requires those approved binaries. Historical private database/pharmaceutical evidence remains archived evidence.

If Git-history checks fail, verify that the checkout includes the pinned history and that dependencies were installed in the active environment. If checksums fail, obtain the exact release assets again and investigate before using the files. [Limitations](Limitations.md) distinguish reproducible engineering results from scientific acceptance.
