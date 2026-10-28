# Current documentation 0.4.0

The 21 shared guide sources in this namespace reconcile published v0.3.4, target v0.3.5, executed lifecycle 0.7.0 and current consistency 0.3.0 with the unchanged scientific baseline. Their reviewed source is selected by exact commit in [selection.json](selection.json); [policy.json](policy.json) binds every guide hash. Pages and native Wiki derive from those same Markdown bodies.

Run `python tools/publication/current_documentation.py --check` to validate the reviewed guides, 23 generated Wiki files, 31 maintained HTML headers, local links/manifests and all four frozen snapshots. The separately bound [component](../../evaluation/documentation/current-0.4.0/component.json) records current file and Wiki hashes. Existing documentation 0.3.0 source files and all 380 v0.3.4 selected file bindings remain unchanged.

The new deployment runs after the preserved predecessor Pages/status pipelines, verifies the exact current main and actual published v0.3.4 identity, rechecks the source, then deploys the 0.4.0 maintained bodies. It does not publish v0.3.5. Native Wiki changes are separately synchronized and independently fresh-cloned; actual served HTTP bodies are compared with the full deployment manifest. Exact-source hosted/native Wiki/HTTP completion is recorded in [#55](https://github.com/ArazSaieArasi3/riskium/issues/55), distinct from source generation.

Model 0.3.1, ORSD 0.4.3, original DRSD 0.1.0, approved manuscript 7.0.8, historical HermiT/SHACL/CQ populations, all eleven WITHHELD admissions and zero independent semantic ratings remain unchanged. Final compatible v0.3.5 selection, affected trace replay, freeze/new assets/independent download and submission gates remain under #51 and the original research issues.
