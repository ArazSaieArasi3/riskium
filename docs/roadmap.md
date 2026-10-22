# Roadmap

The remaining work is organized by outcome. Migration established a public conceptual-design snapshot; it did not complete scientific validation, a native Wiki, Pages deployment or a stable release.

| Work item | State |
| --- | --- |
| [Define the formal validation coverage contract](https://github.com/ArazSaieArasi3/riskium/issues/1) | Coverage design complete; [contract](../evaluation/coverage-contract.md) and [row review](../evaluation/coverage-review.json) recorded |
| [Validate the native conceptual model and resolve semantic candidates](https://github.com/ArazSaieArasi3/riskium/issues/2) | Exchange representation and bounded design review complete; [results and limits](../evaluation/native-model-review.md) |
| [Implement and review the OWL mapping](https://github.com/ArazSaieArasi3/riskium/issues/3) | Bounded typed-core export and [review](../evaluation/owl-mapping-review.md) complete; HermiT and SHACL remain open |
| [Implement the HermiT consistency and inference suite](https://github.com/ArazSaieArasi3/riskium/issues/4) | Scoped suite executed and [reasoning report](../evaluation/hermit/report.md) recorded; 14 constraint obligations await justified formal or alternative disposition |
| [Implement SHACL validation profiles and fixtures](https://github.com/ArazSaieArasi3/riskium/issues/5) | Endpoint and [80-row catalog metadata admission](../evaluation/shacl/admission/report.md) batches executed; children [#17](https://github.com/ArazSaieArasi3/riskium/issues/17) and [#18](https://github.com/ArazSaieArasi3/riskium/issues/18) completed within their scopes; [ledger](../evaluation/shacl/coverage-status.md): 339 scoped PASS, C-08 PARTIAL, 19/359 NOT_RUN |
| [Complete requirement and competency-question traceability](https://github.com/ArazSaieArasi3/riskium/issues/6) | Open |
| [Conduct independent semantic and case-interpretation review](https://github.com/ArazSaieArasi3/riskium/issues/7) | [Review inventory](../evaluation/semantic-review-register.json) prepared; independent adjudications pending; overall semantic correctness unestimated |
| [Complete the public reference corpus and standards interpretation](https://github.com/ArazSaieArasi3/riskium/issues/8) | Open |
| [Publish and verify the curated Wiki](https://github.com/ArazSaieArasi3/riskium/issues/9) | Open |
| [Publish the versioned reference and ontology explorer](https://github.com/ArazSaieArasi3/riskium/issues/10) | Open |
| [Build the claim-based evaluation and quality report](https://github.com/ArazSaieArasi3/riskium/issues/11) | Open |
| [Reconcile the separate relational implementation with the reviewed model](https://github.com/ArazSaieArasi3/riskium/issues/12) | Open |
| [Prepare and review the independent literature case study](https://github.com/ArazSaieArasi3/riskium/issues/13) | Open |
| [Complete the final manuscript review and reconcile claims, tests and numbers](https://github.com/ArazSaieArasi3/riskium/issues/14) | Open; [review checklist](manuscript-review-checklist.md) |
| [Prepare the first reviewed Riskium release](https://github.com/ArazSaieArasi3/riskium/issues/15) | Open |
| [Maintain future extensions and interoperability boundaries](https://github.com/ArazSaieArasi3/riskium/issues/16) | Open |

## Recommended sequence

The coverage-design, native-exchange and bounded OWL-mapping stages are complete within their documented limits. HermiT retains 14 engine-specific NOT_RUN rows; C-09 has alternative evidence in the first scoped SHACL batch. All 254 ordered endpoint obligations now have isolated and paired-end evidence. All 80 catalog admission rows now have scoped metadata or boundary-exclusion evidence. CatalogInspection is the sole supported metadata task; risk-assessment readiness remains unclaimed. C-23/C-24 now have [explicit graph coherence evidence](../evaluation/shacl/coherence/report.md), with static/history limits retained. Continue #5 with the 19 remaining NOT_RUN constraint routes and full multi-relation/conditional-profile integration. Resolve C-08 compatibility through an approved unit/scale schema. Reconcile requirement and query evidence in #6, independent semantic review in #7 and reference interpretation in #8. The [semantic assurance plan](../evaluation/semantic-assurance-plan.md) defines the evidence and limits; an executed subset must not be reported as universal validation.

The curated Wiki can be initialized from its prepared source now. The generated reference can be deployed separately; an ontology explorer depends on a justified formal export. Public rendering must be verified after publication.

Database, literature case study and manuscript work remain distinct. Future extensions are not current capabilities. The first release selects an explicit maturity and evidence profile using the release checklist.

