# Riskium

Riskium is a conceptual ontology for organizing organizational risk knowledge. It distinguishes a continuing **RiskCase** from its register entries, possible scenarios, occurrences, contextual assessments, decisions and evidence. The ontology's domain is general; the pharmaceutical literature corpus is a development case, not its defining domain or an independently validated organizational deployment.

**Published source:** [v0.3.8](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.8) · **conceptual model and OWL:** 0.3.1 · **published reader:** 0.4.7 · **author-held article candidate:** [7.2.3 receipt](evaluation/manuscript-review/v7.2.3/receipt.json). The article's Word/PDF are supplied to the author separately; they are not assets of the published source distribution. [Artifact roles](documentation/0.4.7/guides/Artifact-Versions.md) and the [manuscript/release roadmap](docs/manuscript-and-release-roadmap.md) explain the distinct version numbers.

[Read the Pages guide](https://arazsaiearasi3.github.io/riskium/current/index.html) · [Browse concepts](https://arazsaiearasi3.github.io/riskium/current/concepts/index.html) · [Open the Wiki](https://github.com/ArazSaieArasi3/riskium/wiki) · [Explore the conceptual reference](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html) · [Download v0.3.8](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.8)

**Verified package:** v0.3.8 selects 32 component families. All six uploaded assets were independently downloaded and verified against the exact source, component closure and unchanged predecessor inventory. The [publication record](evaluation/releases/v0.3.8/publication.json) retains those observations; [#76](https://github.com/ArazSaieArasi3/riskium/issues/76) records current-channel reconciliation.

## Choose a path

| Goal | Start here | Continue with |
| --- | --- | --- |
| Understand the research | [Scope](docs/guides/Scope.md) and [modeling decisions](docs/modeling-decisions.md) | [Requirements](requirements/ontology-requirements.md), [competency questions](requirements/cq/README.md), [evaluation and limits](evaluation/quality/README.md) |
| Inspect or reuse the model | [Selected view](diagrams/selected-view.svg), [subdomain package map](diagrams/subdomain-relationships.svg), [relationship matrix](diagrams/subdomain-relationships-matrix.svg) and [concept dictionary](documentation/concepts/0.3.1/README.md) | [Catalog search](https://arazsaiearasi3.github.io/riskium/current/reference/search.html), [WIDOCO](https://arazsaiearasi3.github.io/riskium/current/widoco/index-en.html), [WebVOWL](https://arazsaiearasi3.github.io/riskium/current/webvowl/index.html), [bounded OWL mapping](evaluation/owl-mapping-review.md) |
| Reproduce and assess results | [Reproduction guide](documentation/0.4.7/guides/Reproduce.md), [source-aware CI policy](docs/source-transition-validation.md) | [Experiments and workflow inventory](docs/experiment-and-flow-inventory.md), [claim-based quality report](evaluation/quality/README.md), [release/channel checklist](docs/publication-consistency-checklist.md) |
| Use the relational companion | [Database assurance](docs/relational-assurance.md) | [Risk-nature SQL profile](implementation/relational/0.9.0/README.md) and [traceability](docs/traceability.md) |

The source catalog is [ontology/riskium-model.json](ontology/riskium-model.json). Its eleven subdomains organize one overall domain. The [native OntoUML exchange](ontology/native/riskium.ontouml.json), [typed OWL projection](ontology/derived/riskium.owl.ttl), [requirements](requirements/ontology-requirements.md) and [evidence](evaluation/README.md) have different roles. Passing a structural, reasoning, SHACL or SQL check does not establish an overall semantic-correctness percentage. Independent semantic review is tracked in [#23](https://github.com/ArazSaieArasi3/riskium/issues/23), and independently prepared literature case populations remain [#13](https://github.com/ArazSaieArasi3/riskium/issues/13).

## Repository map

| Folder | Purpose |
| --- | --- |
| [`ontology/`](ontology/) and [`diagrams/`](diagrams/) | Source catalog, projections and selected visual views |
| [`requirements/`](requirements/) | ORSD, competency questions and declared contracts |
| [`evaluation/`](evaluation/) | Executed receipts, limits and separately scoped populations |
| [`implementation/`](implementation/) and [`tools/`](tools/) | Relational companion, transformations and reproducible checks |
| [`docs/`](docs/) and [`documentation/`](documentation/) | Reading guides, current and versioned publication sources |
| [`releases/`](releases/) and [`plans/`](plans/) | Component selection, source distribution and prospective work |

For the [current Wiki Home](https://github.com/ArazSaieArasi3/riskium/wiki) and [Pages Home](https://arazsaiearasi3.github.io/riskium/current/index.html), use their navigation to switch among the model, evaluation, tools and version policy. [All releases](https://github.com/ArazSaieArasi3/riskium/releases) and [documentation versions](https://arazsaiearasi3.github.io/riskium/versions/index.html) are historical indexes, separate from the current reading route. Frozen tags and site snapshots retain their own dated claims.

Historical implementation and publication decisions remain traceable through [#40](https://github.com/ArazSaieArasi3/riskium/issues/40), [#41](https://github.com/ArazSaieArasi3/riskium/issues/41), [#44](https://github.com/ArazSaieArasi3/riskium/issues/44) and [#45](https://github.com/ArazSaieArasi3/riskium/issues/45). Their source-bound results are not current release totals; follow the version index for their original artifacts.

## Citation, rights and status

The authors are Araz Saie Arasi, Hassan Haghighi and Hossein Azgomi; use [CITATION.cff](CITATION.cff) and [AUTHORS.md](AUTHORS.md) for exact attribution. Original research content uses CC BY 4.0 and original software uses MIT; [RIGHTS.md](RIGHTS.md) and [NOTICE.md](NOTICE.md) identify retained third-party terms. The repository does not redistribute the privately held literature PDFs or pharmaceutical case database.

The [release roadmap](docs/manuscript-and-release-roadmap.md) keeps subsequent evidence work and the finite first-major-release goal separate from published v0.3.8. Full native-to-SQL mapping, independent expert ratings and general enterprise/holding/ecosystem use validation remain open. [Open issues](https://github.com/ArazSaieArasi3/riskium/issues) record the remaining work.
