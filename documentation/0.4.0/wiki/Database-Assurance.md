# Database assurance

The current public SQLite implementation is a sequence of additive, separately versioned profiles. It preserves original model identities and declares supplementary application fields explicitly. The [original DRSD](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/requirements/relational-requirements.json) and [earlier assessment assurance](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/docs/relational-assurance.md) retain their original source populations.

| Profile | Bounded behavior | Actual evidence |
| --- | --- | --- |
| 0.1.0 | Identity, records and issued history | [Source and receipt](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/implementation/relational/0.1.0/README.md) |
| 0.2.0 | Selected assessment/result mapping | [Assurance](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/relational/assessment/assurance.json) |
| 0.3.0 | Selected assessment corrections | [Correction receipt](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/relational/correction/report.json) |
| 0.4.0, migration 5 | Version-owned scenarios/source references | [54 fixed controls](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/relational/source-scenario/report.json) |
| 0.5.0, migration 6 | Explicit same-artifact correction branches | [54 fixed controls](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/relational/source-scenario-lineage/report.json) |
| 0.6.0, migration 7 | Qualified EvidenceReference and contextual EvidenceItem graphs | [62 fixed controls](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/relational/qualified-evidence/report.json) |
| 0.7.0, migration 8 | C065 correction, documentary SELECT/WITHDRAW/CLEAR and exact as-of retrieval | [43 fixed controls](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/relational/evidence-lifecycle/report.json) |

## What the internal API does

API here means internal Python functions, with SQL constraints and audited transactions. No HTTP service is deployed. In 0.7.0, callers explicitly declare correction edges and context-specific decisions. New issuance does not select a version. Withdrawal preserves history and does not silently choose a replacement; CLEAR removes a selection without undoing a withdrawal. Retrieval requires an explicit ledger boundary.

Sources, locators, interpretations, immutable issued payloads and exact item/target versions stay distinct. A documentary actor/context is not authenticated organizational authority. Native graphs remain per-version projections; the extension adds no new native assertion/correction predicate.

## What remains open

All 306 native IDs retain current dispositions. **236 are deferred**, with fourteen partial source/scenario/evidence routes. General assertions, reinstatement, unsupported native rules, formulas/workflow, PostgreSQL/private migration, real workloads, recovery objectives, roles and operational acceptance remain under #12/#35/#4/#5/#36. The fixed SQL controls and software regressions do not establish semantic truth, production performance, independent validation or complete native mapping.

[Current accounting](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/evaluation/relational/evidence-lifecycle/mapping-accounting.json) · [Lifecycle design and dictionary](https://github.com/ArazSaieArasi3/riskium/blob/ccc89a184a618ccc2c107ccbf27a15232060557e/implementation/relational/0.7.0/schema-dictionary.md) · [Work plan](Work-Plan).


---

Documentation **0.4.0** · Model **0.3.1** · [Published source v0.3.4](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.4) · [Target v0.3.5](https://github.com/ArazSaieArasi3/riskium/issues/51) · [Equivalent Pages guide](https://arazsaiearasi3.github.io/riskium/current/guide/Database-Assurance.html).

Reviewed explanatory source: [documentation/0.4.0/guides/Database-Assurance.md](https://github.com/ArazSaieArasi3/riskium/blob/2c4b0c46f22c90a3a5782e7c918e79f791aa4816/documentation/0.4.0/guides/Database-Assurance.md). Source SHA-256: `4dbb51664678909267f6104876eba6937eea748d187fbb116eb96f4395630c67`. Actual channel/source closure: [#55](https://github.com/ArazSaieArasi3/riskium/issues/55).
