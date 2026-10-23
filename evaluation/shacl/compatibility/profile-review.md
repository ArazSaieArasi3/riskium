# C-08 application declaration compatibility — policy 0.6.0

This bounded child of #5 is the `v0.3.1-rc.3` packet. The project owner authorized implementation and publication. This is an author-maintained engineering interpretation, not independent domain approval. The conceptual JSON, native exchange, OWL and original 359-row ledger are unchanged.

## Task and supplementary vocabulary

The caller selects a nonempty list of named Threshold resources. This task requires both native `RX-025 thresholdForIndicator` and `RK2-020 thresholdOnScale`; this does not make both anchors mandatory in the native model or the original managed profile. On the selected indicator and scale, the versioned **application** namespace `profiles/compatibility/0.6.0#` supplies `scaleVersion`, `kind`, `source` and conditional unit/scheme/term-set declarations. `dimension` on the indicator is supplementary; the scale uses native `RK2-019 scaleForDimension`. Each scale version must be an explicitly supported ArtifactVersion with exactly one native `RX-006 versionOf` target identifying the actual scale. `source` is a declaration provenance IRI; presence does not establish source truth. Scale-version identity is the edition boundary. No native Indicator-to-scale relation is invented.

Every required interpretation field is singleton, named and explicitly present. Only the exact declared version/dimension/kind is compared. Numeric declarations require canonical unit IRIs on both sides. Qualitative declarations require scheme and term-set IRIs on both sides and forbid numeric units. Matching qualitative metadata establishes agreement of declared interpretation identifiers; it does **not** verify permissible terms, order, comparator, boundary value, contextual appropriateness or the external scheme's meaning. There is no physical unit calculator or implicit conversion.

## Identity and decisions

Named instance `sameAs` assertions normalize before comparison; labels do not identify resources. The two kind codes Numeric/Qualitative are mutually exclusive by this application policy. For other fields, differing IRIs without explicit `differentFrom` evidence remain **NOT_READY**. Explicitly distinct declarations fail the exact-match policy; this is **INCOMPATIBLE** within this task, not proof that physical units cannot be converted. A version target with unresolved scale identity likewise remains NOT_READY. Asserted sameAs/differentFrom conflicts, schema/import injection, reserved-vocabulary aliases and empty/non-named caller focus reject before engine execution.

| Result | Exact meaning |
| --- | --- |
| COMPATIBLE_FOR_DECLARED_TASK | Explicit selected declarations conform to this exact metadata policy; not full threshold or risk-assessment readiness. |
| NOT_READY | Required metadata or identity/compatibility evidence is missing. |
| INCOMPATIBLE | A known declared difference fails this exact-match policy. This outcome takes priority over additional missing fields. |
| INVALID | A malformed/type/cardinality/unsupported-kind declaration is present, including invented qualitative units. This takes priority over incompatibility. |
| PROFILE_REJECTED | Caller/identity/schema policy rejected before SHACL; not counted as an engine validation. |
| STAGING_ONLY | Raw graph preserved and parsed; no managed compatibility claim. |

There is no unique-name assumption. Only the pinned source subclass triples support class checks; inference is `none`, imports disabled, no anonymous fillers or repair. Unselected thresholds remain outside the requested task, not accepted by omission. Inputs are not mutated. Error outcomes cannot become a PASS.

## Tests, integration and release interpretation

Fixed author-written fixtures cover numeric and qualitative matching, explicit mismatches, missing versions/dimensions/units/sources/kinds, unbound version targets, alias resolution, equal labels, unknown unit mapping, conflicting/literal units, incorrect types, staging, injected schema and identity errors. Expected source-shape, component and focus sets are fixed independently of validator output. Deleted unit and completeness rules admit their previously rejected fixtures; this demonstrates sensitivity of those selected controls, not a universal mutation score.

Five selected integration cases run the entire compatibility module with both endpoint directions of RX-025, RK2-020 and RK2-019, and metadata admission for the threshold, indicator, scale, dimension and artifact version. One deliberately missing threshold type verifies that record envelopes do not repair missing domain evidence. The catalog task remains CatalogInspection. The versionOf target is checked by this module; full endpoint closure across every source relation and full-profile application acceptance remain #5.

The report retains raw/effective/shapes/result snapshots, exact inputs, runtime, caller focus and alias maps. Its `--check` re-executes fixtures and compares saved accounting, oracles, source hashes and graphs. Engineering regressions, preflight rejections and actual SHACL executions have separate counts. The original C-08 PARTIAL outcome and historical blocked task fixture are preserved. The new source-bound receipt is a **supplement**, not an overwrite or an automatic extra PASS in the 359-row ledger. The frozen quality synthesis remains historically accurate and does not include the new module; read this supplement for current C-08 work.

Manuscript 7.0.7 can retain its bounded statement that C-08 is partial and full/independent acceptance is incomplete. A later manuscript update may cite the explicit-metadata compatibility result, with the exact profile and counts, but may not claim a new native unit axiom, complete C-08 acceptance, physical unit conversion or new HermiT results. No article binary is edited or included by this repository packet.

Technical basis: [W3C SHACL recommendation](https://www.w3.org/TR/shacl/), particularly explicit targets, cardinality/type constraints, validation-result provenance and SPARQL constraints. The compatibility policy and scientific interpretation are project decisions, not W3C-defined risk semantics.
