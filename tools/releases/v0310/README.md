# Prepare current curation for v0.3.10

This additive toolchain prepares documentary review **0.2.0** and reader **0.4.10** for scientific model **0.3.2**. It does not deploy Pages/Wiki, create a release, run an ontology engine or assert independent semantic acceptance.

```sh
python -m pip install -r tools/releases/v0310/requirements.txt
python -B tools/releases/v0310/curation.py --check
python -B tools/releases/v0310/reader.py --check
python -B tools/releases/v0310/qualify.py --mode LOCAL --commit planning/v0.3.10-curation --output /tmp/riskium-n4-new
```

Use a new empty output destination. Rebuild the checked-in curation and reader by omitting their `--check` flags when their declared inputs or recipes change. `qualify.py` creates two independent staged builds, compares their bytes, checks all HTML/Wiki body pairs and local routes, runs preservation/mutation contracts, and records environment/source bindings. LOCAL reports explicitly disclose a dirty working tree; CI requires a clean checkout and its exact commit SHA.

`guard.py` preserves every baseline tracked file at `8e63a88717f3e9efe804004a678adb61e6500510`, except two named planning documents. Additions are limited to this toolchain, the new review/reader versions, their v0.3.10 receipts and the dedicated qualification workflow. It does not modify the frozen v0.3.9 selector or replay tools.

The prepared projection is an affected-reader slice: 91 HTML bodies and 94 Wiki files including navigation. It is **not** the entire public site or a replacement for unrelated Wiki guides. N5 must compose it with preserved channels, freeze package selection, qualify historical replay routing, publish and perform actual readbacks before #85 can close. Existing v0.3.9 publication counts are not reused as v0.3.10 evidence. Normative adoption remains #78 and independent interpretation remains #23.
