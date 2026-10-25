# WebVOWL view 0.1.0 — issue #32

This documentation component projects the exact released model 0.3.1 OWL at `8afe169968b5c1396c02834dbc499af691b894b4`. It is later development/publication on main, separate from the unchanged v0.3.2 source assets and accepted model/ORSD/article components.

The graph contains all 78 named classes, 127 declared object properties and 66 named subclass edges. Every property has its exact single asserted named-class domain/range. The generator refuses an empty class graph; missing, ambiguous or anonymous endpoints are individually omitted, never supplied. The source's 2,087 RDF triples have explicit represented/omitted accounting; anonymous expressions, disjointness and metadata remain identifiable in the canonical omission inventory. Three optional conceptual boundaries are not OWL class admissions. This is visualization accounting, not semantic validation or a fresh HermiT/SHACL/SQL run.

## Source and runtime

- Generator: `tools/publication/build_webvowl.py`; output: `docs/current/webvowl/data/riskium.json` and `coverage.json`.
- Official upstream: VisualDataWeb/WebVOWL v1.1.7, exact commit `28e7dd9540622e8cb723dc000824b5eef5ae775f`.
- The exact build dependency lock, documented read-only source patch and license/provenance records are committed. The core renderer includes lodash/core 4.18.1; local D3 is 3.5.17. WebVOWL/Lodash MIT and D3 BSD notices are shipped beside the viewer.
- The original shell bundles only core renderer, D3 and local controls. The upstream full application, ontology upload/drop/remote loading/converter/editor and server are absent. Core editing defaults false and refuses enabling; a fixed same-origin JSON is fetched without credentials. CSP restricts active resources/connects to self. No shell analytics or persistent browser storage is used.
- Search, keyboard term buttons, selected definitions and exact native/WIDOCO/text-neighborhood links complement the SVG. Text explorer/reference remain available without JavaScript. Download exports the fixed JSON, not an edited ontology.

## Verification

```sh
python tools/build_reference.py --check
python tools/publication/audit_portal.py
python tools/publication/build_versioned_site.py --check
python -m unittest discover -s tests -p test_webvowl.py -v
python tools/review_distribution.py
```

Eight projection/runtime tests cover source-exact class/property/subclass sets, missing/ambiguous endpoint mutants, repeatable canonical omissions, empty graphs, shell boundaries and source/runtime byte checks. Existing successor-package tests use a clean exact published-source fixture: mutable current documentation is not silently substituted for v0.3.2's immutable component selection. The ordinary maintenance workflow no longer tries to re-freeze an already published tag; an explicit new publication request still requires its full gates and cannot overwrite it.

Browser/deployment evidence is now recorded in [browser-readback.json](browser-readback.json), [HTTP readback](http-readback.json) and [actual download files](download-readback.json), with the [RiskCase screenshot](screenshots/RiskCase-desktop.jpg). Source `742267faac3c2d50f083b5f5101b394172f4a446` passed [all 25 candidate gates](https://github.com/ArazSaieArasi3/riskium/actions/runs/40199446072), [documentation integrity](https://github.com/ArazSaieArasi3/riskium/actions/runs/40199446166) and [actual Pages deployment](https://github.com/ArazSaieArasi3/riskium/actions/runs/40199478226). All 208 local software regressions passed on the final code (90.709 seconds). Actual rendered class and property ID sets matched the projection exactly; search/selection, keyboard skip, pause/resume, zoom/reset, text-neighborhood/WIDOCO navigation and 390/760-pixel iframe interactions passed. Both embedded documents had 78 actual named classes, opacity 1 and zero horizontal page overflow. The HTTP readback matched 172 public file bodies plus the root source manifest; the empty build marker is outside public reader routes. Browser download event-reporting timed out, but both actual resulting shared files matched the exact 162,349-byte projection, SHA-256 `4b96dfd769858256a13aedf760e32bb64aa740437d9dc5cfc278787ae41fbdc2`. No site errors occurred in the final interaction sequence.

Browser and source checks retain separate scopes. File/hash checks do not prove actual SVG layout, searching, selection, pause/resume, zoom, download, keyboard behavior or embedded responsive usability. No result for an unperformed UI action is implied by these source checks. Frozen documentation 0.1.0 and every prior source tag/asset retain their exact bytes.
