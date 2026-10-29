# Riskium — Organizational Risk Knowledge

Riskium is a conceptual ontology for representing organizational risk knowledge. It connects a continuing risk case with its register entries, scenarios, objectives, assessments and evidence, while keeping their identities, versions and sources distinct.

**[Published source v0.3.6](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.6)** · **Model 0.3.1** · **SQLite profile 0.8.0 / schema 9**

[Read the guides](https://arazsaiearasi3.github.io/riskium/current/index.html) · [Browse the Wiki](https://github.com/ArazSaieArasi3/riskium/wiki) · [Explore WebVOWL](https://arazsaiearasi3.github.io/riskium/current/webvowl/index.html) · [Download v0.3.6](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.6)

## Start with your task

| Your goal | Recommended path |
| --- | --- |
| Understand the ontology | [Problem and scope](https://arazsaiearasi3.github.io/riskium/current/guide/Overview.html) → [using the model](https://arazsaiearasi3.github.io/riskium/current/guide/Using-the-Model.html) → [conceptual reference](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html) |
| Inspect the structure | [Selected and complete diagrams](https://arazsaiearasi3.github.io/riskium/current/reference/diagrams/index.html), [WebVOWL](https://arazsaiearasi3.github.io/riskium/current/webvowl/index.html) and the [bounded OWL reference](https://arazsaiearasi3.github.io/riskium/current/widoco/index-en.html) |
| Review the research | [Competency questions](https://arazsaiearasi3.github.io/riskium/current/guide/Competency-Questions.html) → [formalization](https://arazsaiearasi3.github.io/riskium/current/guide/Formalization.html) → [evaluation](https://arazsaiearasi3.github.io/riskium/current/guide/Evaluation.html) → [limitations](https://arazsaiearasi3.github.io/riskium/current/guide/Limitations.html) |
| Reuse the database/API | [Released assessment-selection guide](https://github.com/ArazSaieArasi3/riskium/blob/58ff468ec4e8f3500ace6869601a25ea263c3d9f/implementation/relational/0.8.0/README.md), [schema dictionary](https://github.com/ArazSaieArasi3/riskium/blob/58ff468ec4e8f3500ace6869601a25ea263c3d9f/implementation/relational/0.8.0/schema-dictionary.md) and [reproduction](https://arazsaiearasi3.github.io/riskium/current/guide/Reproduce.html) |
| Verify the distribution | [Six release assets](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.6) and the [independent publication record](https://github.com/ArazSaieArasi3/riskium/issues/61#issuecomment-6507087968) |

## What v0.3.6 adds

An application can retrieve the complete assessment version explicitly selected for one decision context at a stated ledger boundary. Corrections retain their original values and branches. Withdrawal returns **WITHDRAWN** without silently falling back to another version; other contexts and earlier historical queries keep their own answers. Selection records a documentary choice, not truth or organizational authority.

The distribution selects **30 components**. Its final source-qualified execution passed **533 software tests plus 10 pinned historical tests**; the assessment task has a separate population of **44 declared controls**. These are engineering results, not a whole-ontology accuracy score.

## Artifacts and versions

| Artifact | Released baseline | Exact source |
| --- | --- | --- |
| Native conceptual model | 0.3.1 | [Authoritative model](https://github.com/ArazSaieArasi3/riskium/blob/58ff468ec4e8f3500ace6869601a25ea263c3d9f/ontology/riskium-model.json) |
| Requirements | ORSD 0.4.3; original DRSD 0.1.0 | [Requirement sources](https://github.com/ArazSaieArasi3/riskium/tree/58ff468ec4e8f3500ace6869601a25ea263c3d9f/requirements) |
| Relational assessment selection | 0.8.0 / schema 9 | [Bounded implementation](https://github.com/ArazSaieArasi3/riskium/tree/58ff468ec4e8f3500ace6869601a25ea263c3d9f/implementation/relational/0.8.0) |
| Current traceability | 0.4.0; 460 accounted routes | [Current overlay](https://github.com/ArazSaieArasi3/riskium/tree/58ff468ec4e8f3500ace6869601a25ea263c3d9f/evaluation/consistency/current-0.4.0) |
| Approved manuscript | 7.0.8 | [Review packet](https://github.com/ArazSaieArasi3/riskium/tree/58ff468ec4e8f3500ace6869601a25ea263c3d9f/evaluation/manuscript-review/v7.0.8) |
| Reader checkpoint in v0.3.6 | Documentation 0.4.2 | [Frozen reader source](https://github.com/ArazSaieArasi3/riskium/tree/58ff468ec4e8f3500ace6869601a25ea263c3d9f/documentation/0.4.2) |

The model, software, manuscript and source distribution have separate versions. The release's `artifact-versions.json` lists the exact selected files and dependencies.

## Current status and next work

**Reader status:** documentation **0.4.3** is the shared maintained guide source for Wiki and Pages over published v0.3.6. The [channel verification record](https://github.com/ArazSaieArasi3/riskium/issues/63) identifies the reviewed source and actual served outputs. The release itself retains its documentation 0.4.2 checkpoint; use its release notes and `artifact-versions.json` for the selected distribution.

The [ordered plan after v0.3.6](https://github.com/ArazSaieArasi3/riskium/blob/main/plans/post-v0.3.6.md) separates immediate maintenance, proposed v0.3.7 work and later research/deployment outcomes. The next proposed source package focuses on **RiskNatureAssertion**: [declare the contract](https://github.com/ArazSaieArasi3/riskium/issues/64) → [implement and verify](https://github.com/ArazSaieArasi3/riskium/issues/65) → [reconcile and publish](https://github.com/ArazSaieArasi3/riskium/issues/66). It is planned, not implemented or released.

## Evidence, citation and reuse

Riskium is a bounded research artifact. All eleven organizational case admissions remain **WITHHELD**; actual independent semantic ratings remain **zero**. Source links and software tests do not establish occurrence, complete semantic correctness, production readiness or regulatory compliance. Later engineering is not silently added to manuscript 7.0.8's claims.

Research content is **CC BY 4.0**; original software is **MIT**, subject to [rights and third-party notices](https://github.com/ArazSaieArasi3/riskium/blob/58ff468ec4e8f3500ace6869601a25ea263c3d9f/NOTICE.md). Credit Araz Saie Arasi, Hassan Haghighi and Hossein Azgomi for their respective contributions; see [citation and attribution](https://arazsaiearasi3.github.io/riskium/current/guide/Citation.html).

<details>
<summary>Publication and documentation history</summary>

The v0.3.6 tag and six assets remain frozen at source `58ff468ec4e8f3500ace6869601a25ea263c3d9f`. This live landing update is not a new source distribution or a semantic/model revision. Actual Wiki/Pages verification is recorded separately in [#63](https://github.com/ArazSaieArasi3/riskium/issues/63). The previous landing remains in documentation 0.4.1 and the v0.3.6 archive. Documentation 0.4.2 and all four frozen snapshots remain preserved. [Release history](https://github.com/ArazSaieArasi3/riskium/releases) · [Version index](https://arazsaiearasi3.github.io/riskium/versions/index.html).

</details>
