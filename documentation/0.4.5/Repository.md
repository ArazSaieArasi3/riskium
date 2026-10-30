# Riskium — Organizational Risk Knowledge

Riskium is a conceptual ontology for representing organizational risk knowledge. It connects a continuing risk case with its scenarios, objectives, assessments, register entries and evidence while preserving their identities, versions and sources.

A report may describe an unfavorable effect, another source may disagree, and a later correction may change the stated nature or context. Riskium retains these documentary versions and their explicit relationships so a reader can recover what each source actually recorded.

**[Published source v0.3.7](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.7)** · **Model and OWL 0.3.1** · **[Release notes](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.7)**

[Read the guides](https://arazsaiearasi3.github.io/riskium/current/index.html) · [Browse the Wiki](https://github.com/ArazSaieArasi3/riskium/wiki) · [Explore WebVOWL](https://arazsaiearasi3.github.io/riskium/current/webvowl/index.html) · [Download the published package](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.7)

## Start with your task

| Your goal | Recommended path |
| --- | --- |
| Understand the domain | [Scope](https://arazsaiearasi3.github.io/riskium/current/guide/Scope.html) → [report and correction example](https://arazsaiearasi3.github.io/riskium/current/guide/Using-the-Model.html#risk-nature-history) → [conceptual reference](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html) |
| Review the research | [Rationale](https://arazsaiearasi3.github.io/riskium/current/guide/Decisions.html) → [source-to-result trace](https://arazsaiearasi3.github.io/riskium/current/guide/Traceability.html) → [evaluation](https://arazsaiearasi3.github.io/riskium/current/guide/Evaluation.html) → [limitations](https://arazsaiearasi3.github.io/riskium/current/guide/Limitations.html) |
| Integrate the SQL/API | [Query contract](https://arazsaiearasi3.github.io/riskium/current/guide/Database-Assurance.html#risk-nature-retrieval) → [executable example](https://arazsaiearasi3.github.io/riskium/current/guide/Reproduce.html#risk-nature-example) → [distribution status](https://arazsaiearasi3.github.io/riskium/current/guide/Publication.html) |
| Inspect the model | [Selected and complete diagrams](https://arazsaiearasi3.github.io/riskium/current/reference/diagrams/index.html), [WebVOWL](https://arazsaiearasi3.github.io/riskium/current/webvowl/index.html) and [bounded OWL reference](https://arazsaiearasi3.github.io/riskium/current/widoco/index-en.html) |

## Risk-nature history

The released nature task retains an original unfavorable report **A-v1**, two explicit correction branches **A-v2/A-v3** and a separate source's report **B-v1**. A later **A-v4** without a correction declaration stays outside the A-v1 correction family. Exact retrieval preserves each version's term, scheme, context, objective references and original source JSON. It makes no implicit latest or truth choice.

[Version-by-version explanation](https://arazsaiearasi3.github.io/riskium/current/guide/Using-the-Model.html#risk-nature-history) · [exact expected answers](https://arazsaiearasi3.github.io/riskium/current/guide/Reproduce.html#risk-nature-example) · [runtime and schema dictionary](https://github.com/ArazSaieArasi3/riskium/blob/7f3f8440b22690d28cea750bd441dde78b1e0337/implementation/relational/0.9.0/README.runtime.md).

## Artifacts and versions

| Artifact | Current role |
| --- | --- |
| Source distribution v0.3.7 | Published; 31 components and six verified assets |
| Prior source v0.3.6 | Preserved historical release; assessment selection 0.8.0/schema 9 |
| SQL 0.9.0/schema 10 | Released nature retrieval: 60 controls and 51 malformed-request variants |
| Consistency 0.5.0 | 470 routes; all 306 native dispositions retained, with 31 bounded nature-task witnesses |
| Native model / OWL | 0.3.1; distinct from the package and software versions |
| ORSD / original DRSD / manuscript | 0.4.3 / 0.1.0 / 7.0.8 |
| Maintained documentation | 0.4.5; shared guide source for Wiki and Pages |

## Current status and next work

The [actual channel verification record](https://github.com/ArazSaieArasi3/riskium/issues/66) identifies the exact reviewed repository source, native Wiki files and served Pages. Documentation sources and actual channel delivery have separate evidence. The [publication record](https://github.com/ArazSaieArasi3/riskium/issues/66) links the authenticated freeze, six actual public downloads and final channel observations. The [ordered work plan](https://arazsaiearasi3.github.io/riskium/current/guide/Work-Plan.html) continues with #37, then #13, before supported manuscript and evaluation consolidation. Later release numbers remain unallocated.

## Evidence, citation and reuse

[Actual R2 evidence](https://github.com/ArazSaieArasi3/riskium/blob/674886381b5520e0771b3a958919e735327572c2/evaluation/integration/v0.3.7/inputs/r2-completion.json) · [R3 reconciliation](https://github.com/ArazSaieArasi3/riskium/blob/674886381b5520e0771b3a958919e735327572c2/evaluation/consistency/current-0.5.0/README.md) · [reproduction](https://arazsaiearasi3.github.io/riskium/current/guide/Reproduce.html) · [publication and citation](https://arazsaiearasi3.github.io/riskium/current/guide/Publication.html).

The exact released source passed **577 current software tests plus 16 unchanged historical tests**. These are engineering results, separate from original HermiT/SHACL populations and semantic review. All eleven organizational admissions remain **WITHHELD**; independent semantic ratings remain **zero**. Historical deferred mappings remain **236**. Later engineering is not silently added to manuscript 7.0.8's claims.

Research content is **CC BY 4.0**; original software is **MIT**, subject to [rights and third-party notices](https://github.com/ArazSaieArasi3/riskium/blob/58ff468ec4e8f3500ace6869601a25ea263c3d9f/NOTICE.md). Credit Araz Saie Arasi, Hassan Haghighi and Hossein Azgomi for their respective contributions; see [citation and attribution](https://arazsaiearasi3.github.io/riskium/current/guide/Citation.html).

<details>
<summary>Exact source and publication history</summary>

Published v0.3.7 is at `86accc6695e4738dd1337d5b9addd73b82c73c3d`, with six independently verified assets. Its reviewed documentation 0.4.4 remains a dated prepublication checkpoint. Published v0.3.6 remains at `58ff468ec4e8f3500ace6869601a25ea263c3d9f` with its original assets. The nature runtime was executed at `7f3f8440b22690d28cea750bd441dde78b1e0337`; its integration trace is `674886381b5520e0771b3a958919e735327572c2`. Documentation 0.4.3 and v0.3.6's 0.4.2 checkpoint remain preserved, together with all four frozen website snapshots. [Release history](https://github.com/ArazSaieArasi3/riskium/releases) · [Documentation versions](https://arazsaiearasi3.github.io/riskium/versions/index.html).

</details>
