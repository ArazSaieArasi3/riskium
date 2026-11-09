# Complete candidate dictionary and structural binding

Date: 2026-11-09. Scope: **B0-6 / P3a** for [issue #93](https://github.com/ArazSaieArasi3/riskium/issues/93). This packet builds and checks the complete candidate Markdown reader and its subdomain matrix. It does not replace the published dictionary, Pages, Wiki, manuscript figures or production source.

Start at the [candidate concept index](reader/README.md). It covers all 82 catalog concepts, a separately indexed external foundational anchor, all eleven subdomains and their purposes, all 137 catalog associations, 67 direct generalizations, 26 source constraints and eight retained generalization sets. Three optional catalog boundaries remain native Notes. Their source vocabulary is not presented as three additional typed-core classes.

The [structural binding](reader/structural-binding.json) connects the reader to the accepted source, native and OWL hashes and the B0-4 export contract. The [reader manifest](reader/manifest.json) binds every generated page and figure. The new reader-binding extension is recorded separately from the historical B0-4 contract; its earlier six selected definition bindings are not silently rewritten.

Definitions, identity bases, typing rationales and authored verification-status fields are retained from the candidate source. The source status can refer to pending work in its original context; current bounded execution evidence is reported separately below. Generating a dossier does not turn its definition into independent semantic validation, supply an externally sourced definition or establish term-level standards equivalence. Wider definition curation remains separate in #85. The source RiskCase boundary is preserved with an explicit reference to the pending migration in #92.

The [candidate matrix SVG](reader/Subdomain-matrix.svg) and [subdomain table](reader/Subdomains.md) derive their population from the candidate: 23 unordered subdomain pairs carry 56 catalog associations. The extra association relative to the historical 55 comes from the new grounding-use link; it is not retroactively added to the manuscript's frozen population. The matrix excludes inheritance and imported-anchor endpoints, includes optional bridges, and asserts neither navigability nor importance, process order or semantic COH/COP. The existing selected [evidence fragment](../issue93-integration/evidence-fragment.svg) is linked as a separate candidate view.

## Verification and protected boundaries

The machine-readable verification receipt records exhaustive field/route checks, negative controls, fresh baseline regression and protected-tree hashes. The candidate export contract is validated before generation; stale candidate native/OWL outputs are rejected. The reader is deterministic and its exact file inventory is checked. External HTTP destinations and live Wiki/Pages publication are not verified by a local route audit.

The frozen 80-concept dictionary and its original generators/guards remain unchanged. This candidate lives only under its separate evaluation packet. Current readers and historical diagrams retain their own source bindings. No current GitHub Actions success, full independent semantic acceptance or production promotion follows from these reader checks.

## Replay

Use the Python dependencies in the [B0-1 replay instructions](../issue93-evidence-use/README.md#replay). On a fresh checkout:

```sh
python evaluation/manuscript-review/v7.2.3/issue93-generalization-sets/build_candidate.py
python evaluation/manuscript-review/v7.2.3/issue93-export-contract/export_candidate.py
python evaluation/manuscript-review/v7.2.3/issue93-dictionary/build_dictionary.py
python evaluation/manuscript-review/v7.2.3/issue93-dictionary/verify_dictionary.py
```

The first two commands prepare the ignored deterministic source/export inputs. This packet then regenerates only its own candidate reader and verification files. On an unchanged checkout, `build_dictionary.py --check` checks stale/missing outputs rather than rewriting them.

**Next is B0-7 / P3b:** candidate CI, reconciliation of the selected publication outputs, and a concrete artifact/promotion-readiness decision. Pages/Wiki publication and release acceptance remain pending there. Issue #93 remains open until the full criteria are satisfied; manuscript 7.2.21 and main are unchanged.
