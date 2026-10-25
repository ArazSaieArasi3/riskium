# Generated Wiki publication

Current Wiki reader pages, sidebar and footer are generated from the same [guide registry](../../tools/publication/guide-registry.json) and explanatory sources as Pages. Edit the registered source, then run `python tools/build_reference.py` or `python tools/publication/build_wiki.py`; do not maintain a second definition or explanation here. `--check` rejects drift and unregistered page loss. Existing Home/Scope/Requirements/Modeling-Decisions/Evaluation/Using-the-Model slugs remain supported. Source generation is distinct from publishing and independently reading back the native Wiki.

## Historical readback

The source pages in this directory are the curated version-controlled Wiki source. The [native Wiki](https://github.com/ArazSaieArasi3/riskium/wiki) was synchronized on 22 October 2026: six pages and `_Sidebar.md` were rendered, then a clone at Wiki commit `55d80eb` matched all seven source files byte for byte.

Use `Home.md` for the Home page. Its visible heading follows the shared `docs/guides/Home.md` source.

For subsequent edits, synchronize the generated pages and verify links, source versions and rendered text. Do not edit definitions independently in the published Wiki.

Fresh read-only Git readback on 24 October at Wiki commit `709bcf003a43b692eb543d21fa0c61546e5e0d15` again matched all seven source files. The content nevertheless predates the final release and current engineering supplements. [Successor #30](https://github.com/ArazSaieArasi3/riskium/issues/30) owns current-content maintenance, shared Wiki/Pages explanatory sources and actual new publication/readback; the [ordered work plan](../work-plan.md) records its dependencies. This audit does not claim the new Wiki content has already been published.

The Pages upgrade updates the shared guide sources and generated Markdown in this directory. This records repository parity; it does not claim a new live Wiki synchronization. Current publication evidence belongs to `evaluation/pages-upgrade/`.

Formal reference task #33 projects the same method and all 25 clause routes into `Formalization.md` and Pages. This records source parity only; a new native Wiki publish/readback is not included in that receipt. Gate #39 explicitly verifies the live channel before the next stable freeze.
