# Requirements and acceptance

The governing ORSD remains **0.4.3** and the original relational requirements remain **0.1.0**. Their original priorities and acceptance criteria are unchanged. The public ledger accounts for twelve RKRS requirements, eight scope statements and eight competency-question contracts. Eleven RKRS requirements are MUST and one is SHOULD; a smaller passing implementation slice does not redefine those priorities.

Read the unchanged [ORSD source](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/requirements/ontology-requirements.md), [original requirement definitions](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/requirements/requirements.json), [relational requirements](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/requirements/relational-requirements.json) and [bounded owner acceptance](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/owner-review/accepted-scope.json). These documents retain their dates and original source roles. Historical pending-publication text describes its own checkpoint; v0.3.4 is now published.

## Derived engineering requirements

| Supplement | Profile | Derived requirements | Actual fixed controls |
| --- | --- | ---: | ---: |
| Source/scenario storage, SSC | 0.4.0 | 6 | 54 |
| Source/scenario lineage, SCL | 0.5.0 | 6 | 54 |
| Qualified evidence, EQR | 0.6.0 | 6 | 62 |
| Evidence-reference lifecycle, ELC | 0.7.0 | 9 | 43 |

Each supplement retains exact source requirements/CQs, native clause boundaries, fixed expectations, code/query and observed results. The ELC contract and 43 expectations were committed before implementation; their declaration-time null/NOT_RUN fields remain unchanged, with actual observations in a separate receipt. These engineering supplements do not complete the original independent source populations or certify whole-model semantics. [Current traceability](Traceability) joins all 27 derived requirements with the unchanged 423-row historical ledger.


---

Documentation **0.4.0** · Model **0.3.1** · [Published source v0.3.4](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.4) · [Target v0.3.5](https://github.com/ArazSaieArasi3/riskium/issues/51) · [Equivalent Pages guide](https://arazsaiearasi3.github.io/riskium/current/guide/Requirements.html).

Reviewed explanatory source: [documentation/0.4.0/guides/Requirements.md](https://github.com/ArazSaieArasi3/riskium/blob/2c4b0c46f22c90a3a5782e7c918e79f791aa4816/documentation/0.4.0/guides/Requirements.md). Source SHA-256: `3fc50d5964cbc51387931fa736d015a845036918efa240117719ecba9f71cad0`. Actual channel/source closure: [#55](https://github.com/ArazSaieArasi3/riskium/issues/55).
