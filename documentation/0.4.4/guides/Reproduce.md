# Reproduce a specific result

## Risk-nature example

Use **Python 3.12** with SQLite supporting `STRICT` tables. The recorded R2 runs used SQLite **3.45.1** on the host and **3.53.1** locally; they are finite engine-specific results. Start from an empty working folder with Git and network access for this public checkout and the pinned Python packages. The commands below use a separate virtual environment. No private file or credential is needed for the synthetic example.

```sh
git clone https://github.com/ArazSaieArasi3/riskium.git riskium
cd riskium
```

The remaining commands run inside that folder:

```sh
git checkout --detach 674886381b5520e0771b3a958919e735327572c2
python -m venv ../riskium-env
../riskium-env/bin/python -m pip install -r tools/requirements-shacl.txt -r tools/publication/requirements.txt
../riskium-env/bin/python - <<'PYEXAMPLE'
import sys
sys.path.insert(0, 'tools')
import run_relational_risk_nature as fixture
import relational_risk_nature as api
u = fixture.U
db = fixture.fresh()
fixture.later(db)
for version in ('A-v1', 'A-v2', 'A-v3', 'B-v1', 'A-v4', 'U-v1', 'Z-v1'):
    row = api.get(db, u(version))['row']
    print(version, row['term_version_id'].split(':')[-1],
          (row['context_version_id'] or 'NONE').split(':')[-1],
          [v.split(':')[-1] for v in row['objective_version_ids']], row['readiness'])
print('family', [r[0].split(':')[-1] for r in api.family(db, u('A-v1'))['lineage']])
print('case-2', [r['version_id'].split(':')[-1] for r in api.by_case(db, u('case-2'))['rows']])
db.close()
PYEXAMPLE
```

On Windows, activate the environment or use `..\riskium-env\Scripts\python.exe` in place of `../riskium-env/bin/python`; run the Python example in a Python file if the shell does not support a heredoc.

Expected complete printed values:

```text
A-v1 negative-v1 context-v1 ['objective-v1'] READY_FOR_DECLARED_RETRIEVAL
A-v2 positive-v1 context-v2 ['objective-v2'] READY_FOR_DECLARED_RETRIEVAL
A-v3 mixed-v1 context-v1 ['objective-v1'] READY_FOR_DECLARED_RETRIEVAL
B-v1 other-negative-v1 context-v1 ['objective-v1'] READY_FOR_DECLARED_RETRIEVAL
A-v4 positive-v2 context-v2 ['objective-v2'] READY_FOR_DECLARED_RETRIEVAL
U-v1 negative-v1 NONE [] NOT_READY_CONTEXT_UNRECORDED
Z-v1 negative-v1 context-empty-v1 [] NOT_READY_OBJECTIVES_UNRECORDED
family ['A-v1', 'A-v2', 'A-v3']
case-2 ['C-v1']
```

This uses synthetic source records and an in-memory populated database. `fresh()` constructs the prior schema-9 population, upgrades additively and issues the declared records. `later()` adds the unlinked A-v4 bundle. No latest-version argument is implicit.

For complete literal rows, sources, dependencies and RDF triples, inspect [the committed actual receipt](https://github.com/ArazSaieArasi3/riskium/blob/674886381b5520e0771b3a958919e735327572c2/evaluation/integration/v0.3.7/inputs/r2-completion.json) and [the R1 literal oracles](https://github.com/ArazSaieArasi3/riskium/blob/674886381b5520e0771b3a958919e735327572c2/implementation/relational/0.9.0/query-oracles.json). Run `python tools/audit_risk_nature_alignment.py --check` at the pinned source to reconcile them. `python tools/run_relational_risk_nature.py --output build/nature-runtime.json` replays 59 controls and honestly leaves the external hosted-download control pending; the separately completed receipt in [#65](https://github.com/ArazSaieArasi3/riskium/issues/65) records its actual independent readback.

The immutable published **v0.3.6 offline package** is a separate reproduction path below. The v0.3.7 development example is not an offline release archive.

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
python -m venv ../riskium-env-shacl
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

Documentation 0.4.4 lives after the source-release checkpoint. Use a full checkout of the documentation commit named in the page's source record, install `tools/publication/requirements.txt`, then run:

```bash
python tools/publication/released_documentation.py --check
python tools/publication/released_documentation.py --output build/released-site
```

Expected result: local guide, link, source-binding and frozen-snapshot checks pass, and a static site appears under `build/released-site`. This builds a local package. Live publication agreement requires separate actual Wiki/HTTP readback.

## Private files and troubleshooting

The approved manuscript 7.0.8 was checked against the actual Word/PDF files. Public CI checks its hash-bound receipt; it does not retrieve private author files. `tools/read_current_manuscript.py --directory /path/to/approved/files --check` requires those approved binaries. Historical private database/pharmaceutical evidence remains archived evidence.

If Git-history checks fail, verify that the checkout includes the pinned history and that dependencies were installed in the active environment. If checksums fail, obtain the exact release assets again and investigate before using the files. [Limitations](Limitations.md) distinguish reproducible engineering results from scientific acceptance.
