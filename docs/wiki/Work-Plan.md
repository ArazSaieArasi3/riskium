# Current work and release plan

The latest source distribution, **[v0.3.2](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.2)**, is published and its downloaded source inventory is verified. The ontology remains **0.3.1**. The [publication record](https://github.com/ArazSaieArasi3/riskium/blob/main/docs/release-v0.3.2-publication.md) identifies exact sources and checks; the [artifact register](Artifact-Versions) separates model, requirements, manuscript, implementation and documentation versions.

## Current documentation work

WIDOCO, the conceptual reference, the text explorer and WebVOWL are deployed. The current Pages upgrade, [#38](https://github.com/ArazSaieArasi3/riskium/issues/38), brings those views into one reading experience and corrects stale explanations. Its implementation and browser review are recorded separately from the released scientific evidence. Frozen documentation and source assets remain historical records.

The formal reference task is [#33](https://github.com/ArazSaieArasi3/riskium/issues/33): explain the formal-method routes and all 25 constraint dispositions with direct evidence and reproduction paths. The maintained [formal-method guide](Formalization) now connects the languages, assumptions, all 25 clause dispositions, original obligation/case IDs, later bounded alternatives and reproduction routes. Publication verification determines closure of #33; this explanation adds no scientific execution.

## Cross-document consistency checkpoint

[#39](https://github.com/ArazSaieArasi3/riskium/issues/39) is a mandatory review before the next stable source freeze. Execute it after #33 and the selected next SQL packet (#35/#12) are stable and CI is green. If a documentation-only stable release comes first, audit that candidate without waiting for SQL. Bind the review to one commit and all artifact versions/digests; recheck affected rows after any change and verify the deployed channels after publication.

Extend the existing requirement/CQ, constraint, manuscript and SQL ledgers into one source-to-claim table. Each row must connect the source/requirement ID, model element, implementation or exclusion, fixture/oracle, observed receipt, retained claim and limit, manuscript/guide/Wiki/Pages location, exact version/hash and unresolved issue. Review terminology, denominators, examples, source citations, commands, links and historical/current status across README, ORSD/DRSD, sources, article, Wiki, Pages and release assets. Resolve critical contradictions before tagging; record bounded exclusions explicitly. Preserve frozen snapshots.

This gate checks documentation consistency and trace completeness; it does not wait for every research issue or imply scientific correctness. The full acceptance checklist is in #39.

## Remaining work by purpose

| Purpose | Required result | Tracking |
| --- | --- | --- |
| Formal reference publication | Verify the new method/25-clause explanation and close its bounded publication task | [#33](https://github.com/ArazSaieArasi3/riskium/issues/33) |
| Relational coverage | Next finite source/scenario/correction mapping, fixed query answers and additive populated migration | [#35](https://github.com/ArazSaieArasi3/riskium/issues/35), [#12](https://github.com/ArazSaieArasi3/riskium/issues/12) |
| Remaining rules | Justified formal and application policies for time, workflow, multiple values and computation | [#4](https://github.com/ArazSaieArasi3/riskium/issues/4), [#5](https://github.com/ArazSaieArasi3/riskium/issues/5) |
| Source and case adequacy | Legitimate normative/prior-art interpretation and broader source-backed cases | [#37](https://github.com/ArazSaieArasi3/riskium/issues/37), [#13](https://github.com/ArazSaieArasi3/riskium/issues/13) |
| Release consistency | Commit-bound cross-document trace table, mismatch resolution and live readback before the next stable freeze | [#39](https://github.com/ArazSaieArasi3/riskium/issues/39) |
| Independent judgment | Actual independent initial ratings and adjudication | [#23](https://github.com/ArazSaieArasi3/riskium/issues/23) |
| Deployment acceptance | Actual PostgreSQL/private migration, workloads, recovery/roles and user acceptance | [#36](https://github.com/ArazSaieArasi3/riskium/issues/36) |

Each packet needs a declared task, exact inputs, expected positive and negative outcomes, executed evidence and explicit limits. A small reviewed release can advance one bounded packet without waiting for every wider research objective.

## Evidence boundaries

The original HermiT 281/295 scoped PASS and 14 NOT_RUN remain unchanged. The historical SHACL ledger remains 341 scoped PASS, one PARTIAL and 17 NOT_RUN out of 359. Later alternatives do not relabel those engine-specific rows. Independent-review responses remain zero, and all eleven organizational identity candidates remain WITHHELD.

A better reference interface, a passing CI build or a verified release download does not establish overall ontology correctness, independent scientific acceptance or production readiness. [Evaluation](Evaluation) explains the support each evidence population provides.

---

[Equivalent Pages guide](https://arazsaiearasi3.github.io/riskium/current/guide/Work-Plan.html) · [WIDOCO](https://arazsaiearasi3.github.io/riskium/current/widoco/index-en.html) · [OWL explorer](https://arazsaiearasi3.github.io/riskium/current/explore/index.html) · [Published v0.3.1](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.1).

Explanatory source: [docs/work-plan.md](https://github.com/ArazSaieArasi3/riskium/blob/main/docs/work-plan.md). Source SHA-256: `74a67e395ef3365c24a535cee9dea27112b5f8c59df368ecb601551b9107f1e2`. This current explanation and later development evidence are separate from the immutable v0.3.1 source assets.
