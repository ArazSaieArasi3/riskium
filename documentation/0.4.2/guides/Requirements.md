# Requirements and acceptance

The governing ORSD remains **0.4.3** and the original relational requirements remain **0.1.0**. Their original priorities and acceptance criteria are unchanged. The public ledger accounts for twelve RKRS requirements, eight scope statements and eight competency-question contracts. Eleven RKRS requirements are MUST and one is SHOULD; a smaller passing implementation slice does not redefine those priorities.

Read the unchanged [ORSD source](https://github.com/ArazSaieArasi3/riskium/blob/8a9a95bba17327d04c5560879819b2e61b48ff19/requirements/ontology-requirements.md), [original requirement definitions](https://github.com/ArazSaieArasi3/riskium/blob/8a9a95bba17327d04c5560879819b2e61b48ff19/requirements/requirements.json), [relational requirements](https://github.com/ArazSaieArasi3/riskium/blob/8a9a95bba17327d04c5560879819b2e61b48ff19/requirements/relational-requirements.json) and [bounded owner acceptance](https://github.com/ArazSaieArasi3/riskium/blob/8a9a95bba17327d04c5560879819b2e61b48ff19/evaluation/owner-review/accepted-scope.json). These documents retain their dates and original source roles. Historical pending-publication text describes its own checkpoint; v0.3.5 is now published.

## Derived engineering requirements

| Supplement | Profile | Derived requirements | Actual fixed controls |
| --- | --- | ---: | ---: |
| Source/scenario storage, SSC | 0.4.0 | 6 | 54 |
| Source/scenario lineage, SCL | 0.5.0 | 6 | 54 |
| Qualified evidence, EQR | 0.6.0 | 6 | 62 |
| Evidence-reference lifecycle, ELC | 0.7.0 | 9 | 43 |

Each supplement retains exact source requirements/CQs, native clause boundaries, fixed expectations, code/query and observed results. The ELC contract and 43 expectations were committed before implementation; their declaration-time null/NOT_RUN fields remain unchanged, with actual observations in a separate receipt. These engineering supplements do not complete the original independent source populations or certify whole-model semantics. [Current traceability](Traceability.md) joins all 27 derived requirements with the unchanged 423-row historical ledger.
