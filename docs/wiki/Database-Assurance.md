# Relational mapping and database assurance

The ontology owns domain meaning. The database implements selected storage and task policies under a separately versioned contract. Mapping confidence needs semantic trace, actual SQL behavior and useful task evidence together; class/table counts or passing synthetic tests alone cannot establish universal correctness or production usefulness.

[The executable brief and organized questions](https://github.com/ArazSaieArasi3/riskium/blob/main/docs/relational-assurance-request.md), [database requirements specification](https://github.com/ArazSaieArasi3/riskium/blob/main/requirements/relational-requirements.json), [profile 0.2.0](https://github.com/ArazSaieArasi3/riskium/blob/main/implementation/relational/0.2.0/README.md), [mapping](https://github.com/ArazSaieArasi3/riskium/blob/main/implementation/relational/0.2.0/mapping.json), [actual schema dictionary](https://github.com/ArazSaieArasi3/riskium/blob/main/implementation/relational/0.2.0/schema-dictionary.md), [executed results](https://github.com/ArazSaieArasi3/riskium/blob/main/evaluation/relational/assessment/README.md) and [trace/readiness record](https://github.com/ArazSaieArasi3/riskium/blob/main/evaluation/relational/assessment/assurance.json) form one source-bound evidence chain.

## When and how mapping is reviewed

Before DDL, assign every ontology element and intended CQ to storage, derivation, external ownership or a documented unimplemented boundary. Choose identity and inheritance strategies explicitly. A kind, a role, a relator, a vocabulary member and an issued version do not all imply the same table pattern. Preserve source direction, endpoint cardinalities, identity, missingness, time and source qualification. Record any stricter task policy separately from native semantics.

After implementation, compare actual schema and SQL behavior with that mapping: typed keys and references, role/version target checks, expected joins, exact native RDF facts and task answers. During migration and recovery, compare old rows, issued payloads, source data, pinned dependencies and historical queries before/after. CI checks source hashes and repeats the applicable suites on every relevant change; a future release pins an exact component set and immutable tag.

OWL and SQL have different operational assumptions. In particular, missing explicit RDF facts and SQL NULL do not automatically mean false, zero or an admissible record. We use explicitly declared closed task checks where appropriate; we do not mechanically convert every OWL axiom into NOT NULL/UNIQUE. [W3C OWL Primer](https://www.w3.org/TR/owl2-primer/) explains OWL semantics; [R2RML](https://www.w3.org/TR/r2rml/) specifies relational-data-to-RDF mappings. The supplied `mapping.ttl` expresses the selected export; no external R2RML processor or whole-ontology inverse-design correctness is claimed.

## Database requirements and traceability

The original ORSD keeps its semantic IDs, MUST/SHOULD priorities and accepted scope. The DRSD derives selected database obligations from those IDs and adds implementation-specific requirements for integrity, migrations, recovery, design review, workloads, concurrency, security and lifecycle. Not every ontology requirement is implemented by this database slice. The trace record keeps all 12 original requirements and eight CQs visible, including unimplemented responsibility, scenario, threshold/workflow and general correction tasks.

Each retained DBR links to source clauses, schema/mapping/query artifacts, fixed cases or static/design/workload evidence and the actual receipt. Future requirements have explicit NOT_RUN scope and issue links. Missing evidence is not acceptance. Every component has its own version and hash; a changed semantic definition, schema, query, source/cohort or policy invalidates its affected evidence and requires a fresh review/replay. Explanatory documentation does not become an independent definition owner.

## Quality checklist

| Axis | Required evidence | What the current profile establishes |
| --- | --- | --- |
| Scope completeness | Full element and requirement disposition, including omissions | Source accounting, not complete implementation |
| Identity and inheritance | Keys, native membership, identity/label counterexamples | Selected artifact/version/subtype behavior |
| Mapping semantics | Directions, multiplicities, role/scale/dimension/version checks | Selected predicates and guarded task subclauses |
| Physical design | Every table's purpose, key, FDs, consumers and documented redundancy | Actual structure plus authored review; no automatic normal-form proof |
| Columns and datatypes | Dictionary, nullability, units/lexemes, defaults and constraints | All actual columns documented; lexical reported values retained |
| One-column/key-only tables | Justification, subtype/membership FK and concrete task use | Unexplained tables are flagged; justified membership is permitted |
| Referential/data integrity | PK/UNIQUE/FK/CHECK/STRICT and exact negative results | Configured SQLite enforcement; [FK enablement](https://www.sqlite.org/foreignkeys.html) is checked per connection |
| Missing/conflicting data | Raw staging, NULL/zero and distinct qualified assertions | No fabricated readiness or one-value collapse |
| Time and computation | Separate time fields, justified arithmetic policy | UTC calendar/order checks; reported values only; general engines deferred |
| Versioned history | Immutable payload/metadata and exact version-based retrieval | No latest-metadata substitution; no generic assessment correction relation |
| Migration and rollback | Populated upgrade, failures and unchanged prior state | Additive migration 3 and atomic bundle/upgrade behavior |
| Backup/restore | Exact logical rows, queries and data audit after restore | Actual SQLite backup/dump/reopen controls; not disaster-recovery certification |
| Query utility | Named user task, bound SQL, independently specified answers | Executable version/history/source/comparison examples |
| Performance and indexes | Defined data shape/size, query answers/plans and latency samples | Four synthetic workload observations; no approved production SLO |
| Concurrency | Declared isolation/journal/busy policy and actual connections | Bounded WAL snapshot/writer-conflict/retry test |
| Security and privacy | Bound inputs, configuration/schema drift, actual deployment threat model | Logical/configuration guards; production roles, encryption and file privileges remain separate |
| Test sensitivity | Invalid, boundary, mutation and metamorphic controls | Missing rules can be exposed; unrelated errors cannot count as success |
| Usability and acceptance | Actual users, task outcomes and deployment context | Technical examples supplied; human/production acceptance unexecuted |
| Provenance and reproducibility | Raw source, locator, origin, seed, command and exact input/result hashes | Finite reproducible engineering evidence, not source truth |
| Release lifecycle | Component compatibility and fresh affected checks | Model/paper/ORSD/base SQL remain separately bound |

A table with only a primary/foreign key can implement valid subtype or set membership. Conversely, many columns can conceal mixed subjects, repeated groups, uncontrolled JSON or update anomalies. The design audit therefore reviews purpose and dependencies rather than imposing a minimum column count. Repeating a direct artifact assertion alongside a version target is deliberate guarded redundancy here because absence of the direct assertion must remain distinguishable; we disclose that decision instead of claiming all tables are automatically in BCNF.

## Synthetic data and practical confidence

Synthetic data can test key/reference and cardinality rules, unknown/zero handling, version pins, multi-value preservation, mutation sensitivity, migration/backup/rollback, query answers and declared workloads without a real case study. Seeded generation is reproducible; fixtures and expectations are frozen separately from execution. High precision, Unicode, duplicate labels, malicious-looking lexical text, missing fields and incompatible versions are deliberate inputs. LLM-generated suggestions may be retained as untrusted candidates, but cannot supply independent ground truth or scientific validation.

Real studies remain necessary for empirical representational adequacy and usefulness in the target domain. Real users/deployment measurements are necessary for acceptance, permissions and workload SLOs. This profile declares an offline research target; it does not silently adopt production healthcare, PostgreSQL or the private historical schema.

SQLite [STRICT tables](https://www.sqlite.org/stricttables.html), [constraint rules](https://www.sqlite.org/lang_createtable.html), [date handling](https://www.sqlite.org/lang_datefunc.html), [isolation](https://www.sqlite.org/isolation.html) and [backup API](https://www.sqlite.org/backup.html) inform the implementation. [EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html) is an observed diagnostic; its text can change across SQLite releases, so the replay does not demand identical plan strings or timing samples. Inventory/index counts are not quality grades.

## Current operating commands

```sh
python tools/build_relational_assessment.py --check
python tools/run_relational_assessment.py --check
python tools/check_database_assurance.py --check
python -m unittest discover -s tests -p test_relational_assessment.py -v
```

The separate post-release workflow runs these alongside the existing base SQL, source and integration suites. New changes on main are development components, not an automatic replacement of the published v0.3.1. Broader mapping, formulas/workflow, private migration, PostgreSQL and independent/user acceptance remain visible in #12/#4/#5/#13/#23.

---

[Equivalent Pages guide](https://arazsaiearasi3.github.io/riskium/current/guide/Database-Assurance.html) · [WIDOCO](https://arazsaiearasi3.github.io/riskium/current/widoco/index-en.html) · [OWL explorer](https://arazsaiearasi3.github.io/riskium/current/explore/index.html) · [Published v0.3.1](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.1).

Explanatory source: [docs/relational-assurance.md](https://github.com/ArazSaieArasi3/riskium/blob/main/docs/relational-assurance.md). Source SHA-256: `595f9a8e6a1bf0d2e46b4c38ab308b5dca475feb6e764051d60cb17d8aad3337`. This current explanation and later development evidence are separate from the immutable v0.3.1 source assets.
