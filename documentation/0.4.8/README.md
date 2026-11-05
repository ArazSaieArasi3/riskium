# Maintained reader 0.4.8

This additive reader projects documentary source review 0.1.0 for all 80 model 0.3.1 concepts. It starts by executing the exact inherited reader at `9cfc399229d4a65d6372b4bef6586b5b10ae5c89`; its 21 guide bodies and four frozen snapshots retain their original source roles. The new dictionary has 83 Markdown pages: 80 concept dossiers, the index, subdomain overview and source-review report. Native Wiki additionally contains 21 existing guides and two navigation files: 106 Markdown files in total.

[All decisions and primary sources](concepts/External-Definitions.md) · [Concept index](concepts/README.md) · [Tracking #85](https://github.com/ArazSaieArasi3/riskium/issues/85).

## Evidence roles

- The authored definition, identity/typing rationale and model relations are copied exactly from the historical dictionary. Only the external-definition section receives reviewed source comparisons.
- [The source registry](../../references/concept-definitions/0.1.0/review.json) owns source identity, version/date, inspected portion, term locator, short paraphrase, comparison reason and follow-up. The generated Markdown, HTML and Wiki are projections.
- Documentary dispositions are distinct from independently verified semantic equivalence. No OWL/SKOS axioms are emitted, no human rating is invented, and no comprehensive literature search is claimed.
- Three normative deferrals retain #78. Semantic judgments retain #23. Source distribution remains v0.3.8; model/OWL remain 0.3.1; SQL remains 0.9.0/schema 10. This reader is post-release documentation maintenance, not a new source freeze.

## Reproduce

```sh
python tools/build_external_definitions.py --check
python tools/publication/external_definition_documentation.py --output build/site --wiki-output build/wiki
python -m unittest discover -s tests -p test_external_definitions.py -v
python -m unittest discover -s tests -p test_dictionary_documentation.py -v
```

The inherited reader verifies the actual v0.3.8 public release identity before building. An authenticated GitHub token is useful for rate limits in CI. Local source checks do not establish publication: #85 closes only after successful main deployment, actual HTTP readback and exact native Wiki readback.
