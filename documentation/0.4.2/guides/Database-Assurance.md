# Database assurance

The current public SQLite implementation is a sequence of additive, separately versioned profiles. It preserves original model identities and declares supplementary application fields explicitly. The [original DRSD](https://github.com/ArazSaieArasi3/riskium/blob/8a9a95bba17327d04c5560879819b2e61b48ff19/requirements/relational-requirements.json) and [earlier assessment assurance](https://github.com/ArazSaieArasi3/riskium/blob/8a9a95bba17327d04c5560879819b2e61b48ff19/docs/relational-assurance.md) retain their original source populations.

| Profile | Bounded behavior | Actual evidence |
| --- | --- | --- |
| 0.1.0 | Identity, records and issued history | [Source and receipt](https://github.com/ArazSaieArasi3/riskium/blob/8a9a95bba17327d04c5560879819b2e61b48ff19/implementation/relational/0.1.0/README.md) |
| 0.2.0 | Selected assessment/result mapping | [Assurance](https://github.com/ArazSaieArasi3/riskium/blob/8a9a95bba17327d04c5560879819b2e61b48ff19/evaluation/relational/assessment/assurance.json) |
| 0.3.0 | Selected assessment corrections | [Correction receipt](https://github.com/ArazSaieArasi3/riskium/blob/8a9a95bba17327d04c5560879819b2e61b48ff19/evaluation/relational/correction/report.json) |
| 0.4.0, migration 5 | Version-owned scenarios/source references | [54 fixed controls](https://github.com/ArazSaieArasi3/riskium/blob/8a9a95bba17327d04c5560879819b2e61b48ff19/evaluation/relational/source-scenario/report.json) |
| 0.5.0, migration 6 | Explicit same-artifact correction branches | [54 fixed controls](https://github.com/ArazSaieArasi3/riskium/blob/8a9a95bba17327d04c5560879819b2e61b48ff19/evaluation/relational/source-scenario-lineage/report.json) |
| 0.6.0, migration 7 | Qualified EvidenceReference and contextual EvidenceItem graphs | [62 fixed controls](https://github.com/ArazSaieArasi3/riskium/blob/8a9a95bba17327d04c5560879819b2e61b48ff19/evaluation/relational/qualified-evidence/report.json) |
| 0.7.0, migration 8 | C065 correction, documentary SELECT/WITHDRAW/CLEAR and exact as-of retrieval | [43 fixed controls](https://github.com/ArazSaieArasi3/riskium/blob/8a9a95bba17327d04c5560879819b2e61b48ff19/evaluation/relational/evidence-lifecycle/report.json) |

## Assessment selection in development

The proposed **0.8.0 / migration 9** profile lets an application explicitly choose one *issued assessment version* for a named decision context. A later correction creates another version; it does not choose that version. A choice returns the original assessment and **all results owned by that version**, including their source and interpretation pins. It does not combine scores from different versions.

For example, context X chooses A-v1, then A-v2; context Y independently chooses A-v3. At ledger sequence 1, asking for X returns A-v1. After X withdraws A-v2, X reports **WITHDRAWN** without falling back to A-v1, while Y still returns A-v3. The query needs an explicit as-of ledger sequence; an unknown assessment is an error, while a known assessment without a decision reports **NO_SELECTION**. An added correction does not change these choices.

The decision context is application metadata, distinct from the assessment's native context. SELECT, WITHDRAW and CLEAR are documentary operations, not a claim that a version is true, comparable or approved. The internal [Python API and exact example](https://github.com/ArazSaieArasi3/riskium/blob/12fb2011801fe47f3245f3f7367952bc0e749448/implementation/relational/0.8.0/README.md) and [44 synthetic control outcomes](https://github.com/ArazSaieArasi3/riskium/blob/12fb2011801fe47f3245f3f7367952bc0e749448/evaluation/relational/assessment-selection/report.json) belong to the development source. [Traceability](Traceability.md) distinguishes their scope from the released component and approved paper.

## What the internal API does

API here means internal Python functions, with SQL constraints and audited transactions. No HTTP service is deployed. In 0.7.0, callers explicitly declare correction edges and context-specific decisions. New issuance does not select a version. Withdrawal preserves history and does not silently choose a replacement; CLEAR removes a selection without undoing a withdrawal. Retrieval requires an explicit ledger boundary.

Sources, locators, interpretations, immutable issued payloads and exact item/target versions stay distinct. A documentary actor/context is not authenticated organizational authority. Native graphs remain per-version projections; the extension adds no new native assertion/correction predicate.

## What remains open

All 306 native IDs retain current dispositions. **236 are deferred**, with fourteen partial source/scenario/evidence routes. General assertions, reinstatement, unsupported native rules, formulas/workflow, PostgreSQL/private migration, real workloads, recovery objectives, roles and operational acceptance remain open; [the work plan](Work-Plan.md) links their tracking records. The fixed SQL controls and software regressions do not establish semantic truth, production performance, independent validation or complete native mapping.

[Current accounting](https://github.com/ArazSaieArasi3/riskium/blob/8a9a95bba17327d04c5560879819b2e61b48ff19/evaluation/relational/evidence-lifecycle/mapping-accounting.json) · [Lifecycle design and dictionary](https://github.com/ArazSaieArasi3/riskium/blob/8a9a95bba17327d04c5560879819b2e61b48ff19/implementation/relational/0.7.0/schema-dictionary.md) · [Work plan](Work-Plan.md).
