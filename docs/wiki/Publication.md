# Publication surfaces and versions

The repository owns the conceptual model, requirements, implementation and evidence. Wiki explains those sources; Pages exposes the explanations alongside the generated ontology reference. A [shared guide registry](https://github.com/ArazSaieArasi3/riskium/blob/main/tools/publication/guide-registry.json) produces equivalent Wiki Markdown and Pages HTML from one source per subject.

## Model, distribution and documentation

These versions identify different artifacts:

| Identity | Current record | Meaning |
| --- | --- | --- |
| Ontology model | 0.3.1 | Conceptual, native and derived OWL definitions |
| Latest source distribution | [v0.3.2](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.2) | Published package selecting 20 independently versioned components |
| Frozen documentation | 0.1.0 for model 0.3.1 | Registered exact presentation and explanatory source |
| Current Pages | Mutable current route | Maintained explanations and interface, including the later WebVOWL view and Pages upgrade |

The v0.3.2 [publication receipt](https://github.com/ArazSaieArasi3/riskium/blob/main/evaluation/releases/v0.3.2-publication.json) binds its exact source and downloaded assets. The current conceptual and OWL downloads still preserve model source `8afe169968b5c1396c02834dbc499af691b894b4`, published with v0.3.1. Later interface changes are not retroactively inserted into either source release.

## Current pages and frozen snapshots

Use the [current portal](https://arazsaiearasi3.github.io/riskium/current/index.html) for the maintained reading experience. The [version index](https://arazsaiearasi3.github.io/riskium/versions/index.html) identifies frozen snapshots, exact sources and model identities. Their older layouts remain part of their historical record.

The legacy rc.1 route preserves the complete website as observed at source `3f332ea56cb27263d2435fa0ae20afb7a5d5f432`. It does not imply that all earlier guides had always been immutable. Registered snapshots cannot be replaced silently. Model versions, source-distribution tags and documentation versions must not be treated as interchangeable.

## Verify a publication

Documentation deployment follows successful CI for the same main-branch source. The root deployment manifest identifies that source and every deployed file hash. Generation, CI, deployment, HTTPS readback and browser interaction checks provide different evidence; each is recorded separately.

The repository's Wiki projections can be checked against the shared guides. Publishing them to the live Wiki requires a separate write and readback; generating Markdown alone is not live publication. The [artifact register](Artifact-Versions) and [current work plan](Work-Plan) identify the scientific and implementation boundaries that remain after documentation publication.

---

[Equivalent Pages guide](https://arazsaiearasi3.github.io/riskium/current/guide/Publication.html) · [WIDOCO](https://arazsaiearasi3.github.io/riskium/current/widoco/index-en.html) · [OWL explorer](https://arazsaiearasi3.github.io/riskium/current/explore/index.html) · [Published v0.3.1](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.1).

Explanatory source: [docs/guides/Publication.md](https://github.com/ArazSaieArasi3/riskium/blob/main/docs/guides/Publication.md). Source SHA-256: `49508373d062b1cef4ded403bfe1bedde4a25131a6bb1799c613e9e44a9e4596`. This current explanation and later development evidence are separate from the immutable v0.3.1 source assets.
