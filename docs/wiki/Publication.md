# Publication surfaces and documentation versions

The repository owns model, requirements, implementation and evidence sources. One [guide registry](https://github.com/ArazSaieArasi3/riskium/blob/main/tools/publication/guide-registry.json) names the source of each explanation; Wiki Markdown and Pages guide HTML are generated from that same source. They are views, not independent definitions.

The [current portal](https://arazsaiearasi3.github.io/riskium/current/index.html) can change. The [documentation version index](https://arazsaiearasi3.github.io/riskium/versions/index.html) identifies separately registered frozen snapshots and their exact explanatory source, model source and file hashes. The root deployment manifest records the exact source commit deployed as current. A model release, documentation version and engineering component version need not have the same number.

The original rc.1 semantic reference remains available under its historical route. Its entire explanatory snapshot is preserved as observed at commit `3f332ea56cb27263d2435fa0ae20afb7a5d5f432`; this does not pretend the guides were immutable when rc.1 first shipped. New frozen documentation registrations bind an exact source tree and exact output files. Changing/removing a registered snapshot or colliding with current/system routes is rejected.

Current semantic/reference downloads are bound to published model source `8afe169968b5c1396c02834dbc499af691b894b4` (v0.3.1). Later SQLite/integration/DRSD supplements are labeled as development, separately from the six immutable stable release assets. The [artifact table](Artifact-Versions) and [work plan](Work-Plan) identify those boundaries.

Pages deployment follows successful documentation CI for the exact same main-branch source. Native Wiki publication is followed by an independent Git readback, link/source checks and rendered review. CI success, source generation, deployment, HTTP byte checks and browser/interface checks remain separate evidence. Documentation publication does not establish independent semantic validation.

---

[Equivalent Pages guide](https://arazsaiearasi3.github.io/riskium/current/guide/Publication.html) · [WIDOCO](https://arazsaiearasi3.github.io/riskium/current/widoco/index-en.html) · [OWL explorer](https://arazsaiearasi3.github.io/riskium/current/explore/index.html) · [Published v0.3.1](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.1).

Explanatory source: [docs/guides/Publication.md](https://github.com/ArazSaieArasi3/riskium/blob/main/docs/guides/Publication.md). Source SHA-256: `d746ff29590f16947ca891ebfbd653c8806b1d70ffa70f2d122662ccd54d3041`. This current explanation and later development evidence are separate from the immutable v0.3.1 source assets.
