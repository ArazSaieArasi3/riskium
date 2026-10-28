# v0.3.4 documentation snapshot

Bounded child #48 under #45 registers **documentation 0.3.0 / model 0.3.1**, frozen from reviewed commit `868dd543538857bb5c9ffbdfde458c4323981d01`, source tree `efbb44909652a4a0df5bb5bfe167df78dcc93785`. [Compatibility policy](../../../tools/publication/snapshot-policy-v0.3.4.json), [additive registration](../../../tools/publication/snapshot-additions-v0.3.4.json) and [separate snapshot component](component.json) bind all 68 output files and the exact presentation/source-reference projection.

The original three-entry pages registry, three snapshots, current documentation 0.3.0 component/receipts and all 286 selected #47 files are unchanged. That current component's `freeze_registered: false` and #47's `new_snapshot_registered: false` remain their dated pre-snapshot checkpoint fields. The new addition records the subsequent snapshot explicitly; it does not silently rewrite either historical packet. The successor snapshot/tooling has its own **DOCUMENTATION_SNAPSHOT 0.1.0** identity, still awaiting explicit distribution selection. The four RDF serializations are copied byte for byte; no model definition or scientific/owner result is revised.

The original assembly remains reproducible for its three-snapshot scope. Actual documentation CI and Pages now require the additive assembly, which validates both registries, all four snapshots, the exact new component and every deployed file/link. Its generated version index separates the frozen documentation snapshot from a source distribution and uses live GitHub `releases/latest` routing. The former version-index body's stale v0.3.2 Latest label is replaced in the additive output; original #46 source/tool bindings stay intact.

Reproduce with:

```bash
python tools/publication/snapshot_registry.py --check
python -m unittest discover -s tests -p test_documentation_snapshot.py -v
python tools/publication/build_snapshot_site.py --check --previous-ref HEAD^
```

Registration rejects a different source/label/documentation/model/rendering pair, tree/manifest mismatch, changed current inputs, omitted/altered old checkpoint bindings, route collisions, unsafe paths and replacement/removal/tampering of registered output. All writes follow compatibility/source checks. Final component/hash/deployment and invalid-input checks are software evidence, not independent domain acceptance.

The new snapshot is available at `releases/v0.3.4/index.html` after the checked deployment. Native Wiki/current guide source content is unchanged; fresh Git/HTTP readback is recorded separately. A snapshot does **not** create a v0.3.4 stable profile, source freeze, tag or assets. The next #45 gate must explicitly refresh selection to include this separate component/tooling, rerun final-source checks and fresh channel evidence, then freeze/publish and independently verify actual assets/Latest and prior-release preservation. All eleven admissions stay WITHHELD and independent ratings remain zero.
