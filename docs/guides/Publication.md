# Publication surfaces and versions

The repository owns the conceptual model, requirements, implementation and evidence. Wiki explains those sources; Pages exposes the same explanations alongside the ontology reference. A [shared guide registry](../../tools/publication/guide-registry.json) projects one explanatory source per subject to native Wiki Markdown and Pages HTML.

## Model, distribution and documentation

Use [Latest published source release](https://github.com/ArazSaieArasi3/riskium/releases/latest) for the live release destination. The following is an explicit **28 October 2026** checkpoint, not a promise that a frozen page will always identify Latest.

| Identity | Record | Meaning |
| --- | --- | --- |
| Ontology model | 0.3.1 | Unchanged conceptual/native/derived OWL definitions |
| Published source distribution | [v0.3.3](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.3) | 24 selected components and six verified release assets |
| Next source distribution | v0.3.4, planned under #45 | Component selection, new documentation snapshot, freeze and publication remain separate gates |
| Frozen documentation | 0.2.0 at releases/v0.3.3, plus earlier registered snapshots | Exact historical explanatory source, renderer and file bytes |
| Current documentation | 0.3.0, mutable current route | Refreshed descriptions of #41/#42/#43/#44 and v0.3.4 preparation; not a new source release or registered snapshot |
| Development SQLite | 0.4.0 / 0.5.0 / 0.6.0, migrations 5 / 6 / 7 | Separately hashed scenario/source, correction-lineage and qualified-evidence components proposed for v0.3.4 |

[The v0.3.3 publication receipt](../../evaluation/releases/v0.3.3-publication.json) binds exact source `3380b6b31f4830417946105e17f023118c7be6ee` and downloaded assets. Current model/RDF downloads preserve semantic source `8afe169968b5c1396c02834dbc499af691b894b4`, published with v0.3.1. Current descriptions do not replace either package's original selection or invent newer article/owner acceptance.

## Current pages and frozen snapshots

Use the [current portal](https://arazsaiearasi3.github.io/riskium/current/index.html) for maintained explanations and the [version index](https://arazsaiearasi3.github.io/riskium/versions/index.html) for registered frozen snapshots. Documentation 0.2.0 deliberately retains pre-publication #41/v0.3.2 wording under its explicit historical banner. Current 0.3.0 descriptions supersede that current-status wording without rewriting the snapshot. Legacy rc.1 and documentation 0.1.0 likewise retain exact registered bytes.

This refresh does not register a v0.3.4 snapshot. The [release plan](../../plans/v0.3.4.md) requires an exact committed documentation source, explicit component selection and successful final-source gates before freezing/publishing v0.3.4. Model, source-distribution and documentation versions are different identities.

## Verify a publication

Pages deployment follows successful documentation CI for the same main-branch source; its root manifest identifies that source and deployed file hashes. Generation, tests, CI, deployment, actual HTTPS bodies and browser interactions are separate evidence. Passing a build is not a live readback.

Native Wiki requires its own write and a fresh Git readback against the generated projection. Markdown in the repository alone does not establish live synchronization. The [work plan](../work-plan.md) and [artifact register](../artifact-versions.md) distinguish current and historical results. No new HermiT/SHACL outcome, independent semantic rating, organizational admission or production acceptance follows from this documentation publication.
