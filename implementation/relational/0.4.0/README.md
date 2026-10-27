# Source-reference and scenario profile 0.4.0

This additive SQLite **migration 5** extends public assessment-correction 0.3.0 for unchanged Riskium **0.3.1**. Bounded child #42 implements part of #35/#12. Stable v0.3.3, the native model, ORSD 0.4.3, DRSD 0.1.0, manuscript 7.0.8 and all previous profiles/receipts remain unchanged.

## Exact meaning of source

**RiskSourceReference (RKM-X06)** describes a claimed contributor to risk. A **documentary source_record** preserves received JSON and provenance. They are different subjects. This profile neither creates a RiskSource bearer (RKM-C007) nor admits native EvidenceReference/EvidenceItem instances. A claim, a locator or an interpretation does not establish causation, occurrence or independent corroboration.

**RiskScenarioSpecification (RKM-C003)** is an information artifact about one or more explicitly identified managed cases. A raw candidate with unknown case identity stays in source_record, with its original JSON, and is excluded from the managed projection. All eleven original organizational admissions remain WITHHELD.

## Native mapping and optional context

| Native source | Scoped storage/export |
| --- | --- |
| RKM-C003 / RKM-X06 | knowledge_type plus issued knowledge_snapshot; both retain the InformationArtifact representation |
| R-36 scenarioAbout | scenario artifact → each explicitly linked case; at least one case at seal |
| RK3-001 hasSourceReference | case → source-reference artifact; source references may remain unlinked |
| RK2-010 scenarioContext | scenario artifact → each explicit context; zero or many context artifacts |
| RK3-003 sourceReferenceContext | source-reference artifact → optional context; at most one |
| GX-048 / G3-001 | Both selected classes also export RKM-C014 typing; no new rdfs/subclass axiom is invented |
| RKM-C015 / RX-006 | Reused version typing and versionOf projection; context version pins are explicit supporting records |

Each supplied context is correctly typed, issued and pinned by exact version. Unknown context creates no context assertion. One owner version pins at most one version of a given context artifact; this is a declared application policy, not a universal ontology cardinality. Contexts are not resolved to current mutable values.

The bounded storage profile selects one knowledge class per artifact and keeps it separate from assessment typing. This is an application restriction, not a new native disjointness axiom.

## Version and provenance ownership

The native projection is a named graph selected by exact **issued version ID**. Different versions retain separate graphs, even when the artifact identity is the same. by_case returns **all explicit issued versions**, preserving multiple sources and disagreements; it has no latest-wins or authoritative-value rule. A new version here asserts no native or general correction relationship. General assertion correction remains #35.

Narrative, documentary source, locator, interpretation origin, UTC recorded time, explicit cases and pinned contexts are sealed together atomically. The serialized payload is audited against normalized rows. List order is canonicalized for storage without dropping duplicates; duplicate bindings are rejected. Artifact origin may differ from a later version's documentary source. Existing source JSON, old snapshots and assessment-correction branches are not overwritten.

The API requires configured foreign keys and recursive triggers. SQL guards reject type/owner/source drift, missing cases, wrong/unissued/misowned contexts, multiplicity violations, empty provenance, invalid calendar time, payload mismatch, replaced or changed rows and additions to issued links. A health audit verifies exact schema, all five migration hashes, old v4 semantics and current normalized content, including after controlled dump restoration. Administrative bypass cannot authenticate the truth of documentary content; this is engineering validation only.

## Storage and recovery

[Dictionary and ownership diagram](schema-dictionary.md) explain four new tables and their indexes. No earlier table/view is replaced. Actual populated v4→v5 migration, idempotence, failed-upgrade rollback, nested atomic issuance, file reopen, backup and dump restoration are exercised. Older exact-schema readers intentionally reject v5; use the version-5 reader rather than silently opening it with the old profile.

[Contract/derived requirements](contract.json) and [fixed fixtures/oracles](fixtures.json) were committed before implementation at the declaration checkpoint linked from issue #42. [Case query](queries/by_case.sql) and [provenance query](queries/provenance.sql) use bound parameters. No field/predicate is added to the ontology by these supplementary provenance/time records.

## Reproduce and inspect

Install the repository's pinned SHACL/publication requirements. Run:

```bash
python tools/run_relational_source_scenario.py --check
python tools/build_source_scenario_inventory.py --check
python -m unittest discover -s tests -p test_source_scenario.py -v
```

The [execution report](../../../evaluation/relational/source-scenario/report.json) contains 54 fixed controls: SQL answers, six independently hand-authored native graph oracles, rejection diagnostics, migration/recovery checks and three weakened-rule/direction controls. Software regressions include additional same-update payload/source, multiple-context, nested-transaction and wrong-document-join checks. [Requirement/source accounting](../../../evaluation/relational/source-scenario/traceability.json) and the [306-element overlay](../../../evaluation/relational/source-scenario/mapping-accounting.json) preserve historical source IDs and explicit omissions.

## Retained limits

This component is development work after stable v0.3.3; no new stable distribution is published here. The historical 423-row release trace stays unchanged, with this separately hashed requirement/mapping extension linked through original IDs. Eight formerly deferred source elements gain bounded routes (two classes, four associations and two inherited typing routes). The remaining broader core mapping, EvidenceReference admission, general correction, formulas/workflow/interval policies, actual PostgreSQL/private migration and independent/user acceptance remain open. Historical HermiT/SHACL populations and zero independent ratings are not promoted by this work.
