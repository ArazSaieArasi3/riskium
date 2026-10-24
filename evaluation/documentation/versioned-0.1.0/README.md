# Documentation publication 0.1.0

This packet completes the shared Wiki/Pages and versioned-publication objectives of #30/#31. It publishes documentation for model **0.3.1**, not another stable ontology/source release. Published source **v0.3.1**, its six assets, accepted matrix, prior prereleases, ORSD/article and historical scientific receipts remain unchanged.

| Object | Exact identity / evidence |
| --- | --- |
| Implementation and shared explanatory source | `609c7cd0fd07053262fffe5720ff0b2605062778`; one registry, 21 subjects, both Wiki and Pages projections; 12 new route/source/tampering regressions |
| New frozen documentation 0.1.0 | `/releases/v0.3.1/`, 53 files, generated from the committed implementation/current tree; source/model/version/output hashes registered at `f9cdf60b84ea0ab32aa926d3bb561ddf6962e6c1` |
| Current semantic source | Published v0.3.1 at `8afe169968b5c1396c02834dbc499af691b894b4`; WIDOCO 1.4.25 rerun from that exact OWL source, with preserved original Turtle and four isomorphic RDF serializations |
| Legacy route | Exact rc.1 website bytes at `3f332ea56cb27263d2435fa0ae20afb7a5d5f432`; it is frozen as observed, not retrospectively described as originally immutable |
| Native Wiki initial readback | [Fresh independent Git clone](wiki-readback.json): commit `9913212c909a9e9b98b6dd75bc8a932b40549f23`, 21 reader pages plus sidebar/footer, all 23 files byte-identical, 70 internal links checked |
| Deployed HTTPS | [Complete readback](http-readback.json): root manifest and all 160 public files returned the exact declared bytes; the empty `.nojekyll` build marker is explicitly outside reader-facing HTTP routes |
| Browser/interface | [Actual connected-browser observations](browser-readback.json): current/frozen navigation, keyboard skip link, frozen explorer filtering/WIDOCO fragment, Wiki navigation and eight 390/760-pixel current-frame measurements |
| Exact source CI | [Documentation integrity](https://github.com/ArazSaieArasi3/riskium/actions/runs/40125387228) passed before [Pages deployment](https://github.com/ArazSaieArasi3/riskium/actions/runs/40125423846); Pages settings explicitly use GitHub Actions, not branch deployment |
| Full candidate | [Downloaded ZIP/source verification](candidate-readback.json): source `f9cdf60b84ea0ab32aa926d3bb561ddf6962e6c1`, all 24 gates, 187 software regressions, 568 source files and exact archive/checksum inventory; publication false |

The subsequent maintenance commit records this evidence, updates current work/status and adds explicit historical-context notes to current projections. Those notes keep original report populations and original pending-state checkpoints intact while making current owner/publication/remaining-work status clear. The shared source/registry hashes bind the final projection; the new frozen snapshot retains its earlier declared exact tree. The [final Wiki readback](wiki-final-readback.json) binds all final shared-source/registry/projection hashes to the actual native Wiki commit after the seven current-guide context/status updates. Initial readback receipts identify the source they actually checked, rather than inventing a self-referential future commit. Any later current deployment receives its own manifest/readback evidence in the issue completion record.

## Reproduce

```sh
python tools/build_reference.py --check
python tools/publication/build_wiki.py --check
python tools/publication/audit_portal.py
python tools/publication/build_versioned_site.py --check --previous-ref HEAD^
python -m unittest discover -s tests -p test_documentation_routes.py -v
```

The assembled site has 80 HTML pages across current, legacy and new frozen routes; all 12,140 local targets/fragments were checked at the frozen-registration source; the final maintenance adds one current-only link (12,141). The current reference audit is a separate 30-page/4,149-link population; the candidate's source-file count is another population. None is a semantic-correctness score.

The source registry rejects route collisions, source-tree/hash mismatches, removal/replacement of an existing registered snapshot and altered frozen bytes. Link projection no longer chooses an old release merely because a changed file existed at that path. CI only deploys the exact successful main-repository/main-branch documentation source; unrelated/fork/failed runs do not qualify.

## Limits and publication method

The prepared direct Wiki Git push had no terminal credential, so actual Wiki publication used the existing signed-in native editor. Its saved result was verified independently by a fresh Git clone; no authentication credential was copied or created. Screenshots retain public GitHub interface context; third-party interface material is not relicensed as original scientific content.

Responsive observations use real iframe viewports at 390 and 760 pixels, not physical devices or full accessibility certification. The quantified frames are current views; frozen navigation/filtering were checked at full desktop size. No graphical WebVOWL is claimed. No complete FOL/SQL/SHACL task admission, private database migration, new HermiT acceptance, actual independent semantic rating, production readiness, DOI or published-article status follows from this publication. Continue the bounded successor distribution/profile in #34.
