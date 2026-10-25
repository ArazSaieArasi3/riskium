# Local visualization dependencies

`webvowl/1.1.7/` contains the official WebVOWL core built from the exact upstream commit in `provenance.json`, with the Riskium read-only patch. It does not contain the upstream application, data sets or conversion server. D3 3.5.17 is a separate local runtime; lodash/core 4.18.1 is bundled in WebVOWL. Their original copyright/license texts are included. Build-only dependency versions and registry integrity values are in `tools/publication/webvowl/package-lock.json`; no build server or PhantomJS lifecycle script was run.

The original Riskium shell and projection generator are MIT; scientific source content remains under its existing CC BY 4.0 scope. Third-party licenses are not replaced by those licenses. `provenance.json` binds exact runtime/license hashes; local generated copies must match them byte for byte.
