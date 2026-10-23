# Competency-question execution contracts

These eight SELECT contracts supplement the unchanged public CQ planning snapshot in `../competency-questions.json`. They use conceptual design 0.3.1 and its exact released OWL mapping. The post-prerelease implementation is not part of the historical `v0.3.1-rc.1` archive.

Each query has four separate named fixture graphs: positive, negative, incomplete and conflicting. The fixed expected binding rows in `contracts.json` were authored separately from execution; no answer is computed from the query and then installed as its own oracle. Each separate mutant query must run successfully on the unchanged positive graph and disagree with the unchanged expected rows. Parser/engine errors are errors, never successful mutation detection.

| CQ | Query representation | Declared source-population status |
| --- | --- | --- |
| CQ01: entries documenting one case | Native `R-01`; explicit RDF resource links, no equal-label grouping | Synthetic design task executed |
| CQ02: scenarios about a case | Native `R-36`; no scenario/case identity or occurrence inference | Synthetic design task executed |
| CQ03: equal scores with different pinned scales | Native `R-18 derivedFrom`, `RX-016 usesScaleVersion`, `RX-006 versionOf`; supplementary numeric envelope field | Synthetic design task executed within this explicit mixed profile; native-only scalar/comparability adequacy remains partial |
| CQ04: assignment without actual mandate | Native `R-10` and optional `R-55`; missing bindings stay unbound | Synthetic design task executed |
| CQ05: entry closure versus cessation | Native revision/state/case links plus synthetic state identifiers | Synthetic design task executed; no universal workflow meaning or OWL non-entailment result |
| CQ06: source traceability | Native evidence links plus supplementary locator/origin/source record metadata | Synthetic controls executed; declared independently prepared evidence population NOT_RUN |
| CQ07: correction lineage | Native version-of links plus explicit supplementary PROV revision links between records | Synthetic controls executed; declared independently prepared evidence population NOT_RUN |
| CQ08: unasserted case identity | Raw application record/candidate; optional native scenario-aboutness link; no promotion to a managed scenario | Synthetic controls executed; declared independently prepared evidence population NOT_RUN |

The [profile policy](profile.json) distinguishes native elements from supplementary scalar, provenance and staging terms. No class, property or axiom is silently added to Riskium. The fixed TriG fixtures are entirely author-created examples, not extracted literature data. The runner queries one named graph at a time, with no imports, identity normalization, inference or remote service.

Conflicting graphs deliberately preserve multiple answers and are not claimed conformant managed instances. An unbound value means no asserted match, not falsehood or an OWL negative assertion. These queries do not establish actual event occurrence, mandate authority, independent source corroboration, immutable history, verified arithmetic or standards compliance.

The eight new synthetic contracts execute 40 queries (32 answer cases plus eight mutation controls). Only CQ01–CQ05 match the original planning snapshot's synthetic population; CQ06–CQ08 still need independent data preparation and acceptance in #13/#7. All 28 public requirement/scope/CQ identities, current evidence and gaps are in [the traceability ledger](../../evaluation/traceability/README.md). Trace completeness does not imply that all requirements are accepted.

```sh
python3 -m venv .venv-owl
.venv-owl/bin/pip install -r tools/requirements-owl.txt
.venv-owl/bin/python tools/run_cq.py --check
.venv-owl/bin/python tools/build_traceability.py --check
.venv-owl/bin/python -m unittest discover -s tests -p test_cq.py -v
```

Run `--write` only after reviewing intentional changes to source, profile, query, fixture or expected answer. The 674-row planning baseline, eight supplementary scope rows and HermiT/SHACL outcomes retain their own denominators and actual provenance.
