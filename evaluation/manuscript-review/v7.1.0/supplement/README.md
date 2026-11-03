# Bounded 7.1.0 supplementary experiments

These scripts and original report snapshots accompany the author-held ten-page manuscript. The experiment's source baseline is `50f731aa5e065233c81fceeadaab8d87f5569de6`, with model SHA-256 `4a052bb0b7321e5209417c69e96644089aa7dba1734cce4a70e5223f2ebbaf59`. The scripts here have been relocated from the author-held packet to run from a repository checkout; the original report receipts still identify the baseline. Replaying on a later checkout is valid only after checking the model digest and compatible source inputs. This directory is part of the draft roadmap PR, not a published source release.

From the repository root, with Python 3.12 and `rdflib==7.6.0` installed:

```sh
python evaluation/manuscript-review/v7.1.0/supplement/analyze_model.py /tmp/riskium-710-replay
python evaluation/manuscript-review/v7.1.0/supplement/query_parity.py /tmp/riskium-710-replay
python evaluation/manuscript-review/v7.1.0/supplement/verify_reports.py /tmp/riskium-710-replay
```

Use another writable directory instead of `/tmp/riskium-710-replay` if appropriate. The scripts write the generated query pairs, SQLite population, named-graph TriG export and JSON reports there. The check compares substantive report fields and the model digest with the original snapshots; source commit, script digest, Python/runtime metadata and generated file hashes may differ after relocation. No binary database, RDF export or manuscript is committed here. The source scripts derive the synthetic population from the existing repository tools and declare expected answers before evaluating the two query languages.

`structural-report.json` records graph counts for 11 catalog subdomains. It does **not** calculate semantic COH/COP. `pattern-report.json` implements eight selected structural OntoUML catalogue triggers with six detector controls; its candidates require interpretation and are not confirmed defects or full anti-pattern certification. `query-contract.json` declares literal expected answers. `query-parity-report.json` contains 14 matched SQL–SPARQL retrieval cases in three bounded families and three detected mutants. This is not full SQL/RDF semantic preservation, score parity, or production performance. Original HermiT, SHACL, relational and case-study results have different archived populations and are not rerun by these scripts. Independent expert ratings and organizational applicability remain unobserved.

The original author-held packet contains more assets, including the diagram, concept-admission notes and detailed remaining-catalogue inventory; this public subset is sufficient to replay **only** the experiments above. See the [intake](../README.md) and [claim ledger](../claim-ledger.md) for the remaining evidence boundaries. New results should be interpreted with the original source and code licenses.
