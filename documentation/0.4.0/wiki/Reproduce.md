# Reproduce the relevant source

Choose the exact artifact and source before running a check. Published stable distribution **v0.3.4** is tagged at **cc02e45749995b8710802822ae709d49e0a83993** and has six independently verified assets. Its source-bound 373 software tests and 28 core plus ten release-specific freeze checks describe that frozen source. They are not the current development-test count.

## Current engineering checkpoints

Lifecycle #53 binds actual 0.7.0 controls and earlier source/full/hosted closure. Current alignment #54 at ccc89a184a618ccc2c107ccbf27a15232060557e passed 409 full software tests, 28 candidate gates and ten hosted workflows; its downloaded 1020 source files matched the manifest and Git blobs. Reproduce that checkpoint at its exact commit. Later changes require affected checks again.

With the repository's pinned Python dependencies installed, the current source routes include:

```bash
python tools/run_relational_source_scenario.py --check
python tools/run_relational_source_scenario_lineage.py --check
python tools/run_relational_evidence.py --check
python tools/run_relational_evidence_lifecycle.py --check
python tools/audit_current_alignment.py --check
python -m unittest discover -s tests -v
```

The four SQL populations remain 54/54/62/43. Local recorded SQLite was 3.53.1 and hosted replay used 3.45.1; each actual receipt keeps its own runtime. New documentation source/integrity and actual publication checks are recorded under #55.

## Private and historical artifacts

Actual approved manuscript 7.0.8 Word/PDF bytes and locations were freshly checked under #54. Public CI validates the hash-bound receipt; it does not fetch private author binaries. `tools/read_current_manuscript.py --directory /path/to/approved/files --check` requires those approved files. Archived private relational/pharmaceutical executions retain their original archive/member/hash and are not claimed as fresh public reruns.

[Historical detailed reproduction guide](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/docs/reproducibility.md) retains its original commands and populations. Final v0.3.5 selection/freeze, independent asset downloads and final submission reproduction remain separate gates. [Work plan](Work-Plan).


---

Documentation **0.4.0** · Model **0.3.1** · [Published source v0.3.4](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.4) · [Target v0.3.5](https://github.com/ArazSaieArasi3/riskium/issues/51) · [Equivalent Pages guide](https://arazsaiearasi3.github.io/riskium/current/guide/Reproduce.html).

Reviewed explanatory source: [documentation/0.4.0/guides/Reproduce.md](https://github.com/ArazSaieArasi3/riskium/blob/2c4b0c46f22c90a3a5782e7c918e79f791aa4816/documentation/0.4.0/guides/Reproduce.md). Source SHA-256: `0d4162dda98cbb9a66cb701a07090e9c809f02e8488c3d921403b130433d87f6`. Actual channel/source closure: [#55](https://github.com/ArazSaieArasi3/riskium/issues/55).
