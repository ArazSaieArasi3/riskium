# Versioned documentation publication

This page preserves the original **22 October 2026 publication receipt** and its historical page/link/interface counts. It is not the current backlog. The [24 October comparison](publication-comparison.md), [fresh HTTP/Wiki readback](../evaluation/publication-comparison/2026-10-24.json) and [ordered work plan](work-plan.md) record later state: stable v0.3.1 is published; Wiki/common-guide maintenance, stable/current routes and graphical WebVOWL are separately tracked as #30–#32. Current local page/link counts are in `evaluation/documentation-audit.json`.

The post-release Riskium documentation uses the reading structure selected for OntoSPK: overview, sidebar guide, conceptual reference, WIDOCO OWL reference, evaluation, local explorer and downloads. [Open the versioned portal](https://arazsaiearasi3.github.io/riskium/releases/v0.3.1-rc.1/index.html).

Semantic source: `cfb85905ab37549c7090f00a41ca62cdd3364ab5`, tag `v0.3.1-rc.1`. Documentation implementation: `b83599a2f6cd5b8fe76ee91cce3ab76986721dd3`, followed by download controls and fully pinned dependencies at `f5f7571f3fffb6bad2e9d01a99246be7fb52a63d`. The existing release tag and archive are unchanged. The website was generated after the release; its manifest separates frozen semantic inputs from current explanatory-source hashes.

| Publication gate | Evidence and observed result |
| --- | --- |
| Version and source | Semantic inputs read from the exact tagged commit; tag resolution, model digest and HermiT/SHACL input receipts checked. |
| Portal and template | 17 audited HTML pages/entry routes; OntoSPK-style navigation plus actual WIDOCO 1.4.25 output. Jar SHA-256 `be57a270fffb91e55810fa308717e704a44e2e7c027a3d68125a49da6c8b4e2b`. Upstream credits, Apache license and modification notices retained. |
| Conceptual reference | All 80 concepts, 134 associations/bridges, 66 generalizations and 25 interpretation constraints are represented: 305 filterable entries. Imported anchor listed separately. |
| OWL explorer | 78 named classes (77 local plus anchor proxy), 127 object properties, 2,087 RDF triples. Named parents/children and property endpoints independently compared with the original graph. Optional boundaries and seven bridges remain excluded. |
| Links and assets | All 3,463 local targets/fragments passed. All 45 deployed version files, entry routes and shared notices returned HTTP 200 and matched the local source byte for byte. |
| Downloads | Original JSON/native files and Turtle preserved exactly. RDF/XML, JSON-LD and N-Triples are graph-isomorphic to the source. File and serialization checksums passed. Direct-download filename attributes observed in the live UI. |
| Keyboard and filtering | Skip link focused main content; Tab/Enter opened an OWL neighborhood. `Risk Case` showed 29/305 conceptual entries; `RKM-X01` showed 23/205 explorer entries. A jump to hidden Agent cleared the filter, revealed the target and restored 205 entries. Its WIDOCO link opened the correct declaration. |
| Responsive reading | Overview, conceptual reference, WIDOCO and explorer rendered in both 390- and 760-pixel frames: all eight had no horizontal page overflow. Content widths after the vertical scrollbar were 375 and 745 pixels. Explorer filtering also passed in the 390-pixel frame. |
| CI and deployment | [Documentation integrity run 39842601600](https://github.com/ArazSaieArasi3/riskium/actions/runs/39842601600) and [Pages run 39842598463](https://github.com/ArazSaieArasi3/riskium/actions/runs/39842598463) succeeded for `f5f7571`. Initial implementation runs 39841684144 and 39841682003 also succeeded. |

## Reproduce and inspect

Use the pinned environment and commands in [publication instructions](../tools/publication/README.md). The [local audit](../evaluation/documentation-audit.json), [HTTPS readback](../evaluation/documentation/http-readback.json), [browser readback](../evaluation/documentation/browser-readback.json), [desktop screenshot](../evaluation/documentation/portal-desktop.jpg) and public [responsive review surface](https://arazsaiearasi3.github.io/riskium/interface-review.html) record distinct methods and limits.

The connected cloud browser did not return a completed downloaded artifact within its timeout. Availability and exact file contents were verified independently by HTTPS GET for all 45 public artifacts. Responsive frames do not replace physical-device, screen-reader or comprehensive accessibility testing. No broad accessibility certification or zero-console-error claim is made. External source and citation hyperlinks are intentional navigation; the published pages have no remote runtime assets or upload service.

Publication and serialization checks do not rerun HermiT/SHACL, establish independent semantic correctness, or close requirement/CQ acceptance. HermiT remains 281/295 baseline obligations with 14 NOT_RUN; SHACL remains 341 scoped PASS, 1 PARTIAL and 17 NOT_RUN of 359. Continue requirement and query evidence in #6, then manuscript reconciliation in #14.
