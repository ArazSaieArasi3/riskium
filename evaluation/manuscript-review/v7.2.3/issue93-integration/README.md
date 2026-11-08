# Combined candidate integration and promotion decision

Date: 2026-11-08. Scope: **B0-3** for [issue #93](https://github.com/ArazSaieArasi3/riskium/issues/93), using the combined candidate at commit `74aedfb386f78210b17a2c87cafeee03f4093494`. The integration audit is complete. The decision is **do not replace the production source yet**.

## What was executed

The builder regenerated the combined 82-concept candidate, its native exchange and OWL projection. The integration run checked its pinned native schema, performed a direct `ontouml-js` 1.0.0 parse/serialize round trip, executed HermiT consistency, and combined the candidate evidential-use SHACL shapes with the existing managed profile. OWL was provided as the ontology graph; inference and imports were disabled for the explicit-data checks.

The [machine-readable receipt](integration-report.json) records thirteen integration expectations met, 20/20 explicit-data cases matching expectations (14 negative controls), 596 SDK elements preserved, six candidate definition pages, and the actual compatibility probes below. The eight HermiT cases in B0-2 remain their own prior receipt; this run adds one fresh whole-candidate consistency check, not a replacement denominator for those cases or the manuscript's historical engine totals.

An integration-specific guard rejects mediated participants linked by explicit bidirectional/transitive `owl:sameAs` paths. The earlier direct-node disjointness condition is retained. Two alias cases reject as intended; removing the alias guard lets its counterexample through. This handles declared alias paths, not arbitrary real-world identity reconciliation. The [combined managed shapes](combined-managed.shacl.ttl) have their own receipt and are not silently substituted into the older B0-1 packet.

## Concrete compatibility findings

| Surface | Actual observation | Consequence |
|---|---|---|
| Candidate native exchange | Schema checks and SDK round-trip invariants pass for 596 elements, including custom policy metadata. | The candidate representation is inspectable and interchangeable under these bounded checks. GUI import and full semantic acceptance are separate. |
| Candidate OWL | A fresh HermiT run reports consistency. | This supports consistency of this projection, not independent conceptual adequacy or production migration. |
| Combined explicit-data profile | All 20 expected accept/reject outcomes match. | Named grounding/use records, endpoint coherence and explicit alias boundaries are exercised on synthetic cases. |
| Current SQLite evidence export | All four selected synthetic reference projections lack the new use relator/reference participation role and fail the candidate profile. SQLite integrity remains `ok`, with zero foreign-key violations. | This is a version/profile mismatch, not a failure of the old database under its own contract. A citation must not be converted automatically into an actual use or an invented grounding record. |
| Production OWL generator | Its current source-version/review guard rejects the candidate when candidate input paths are supplied. | Introduce an explicit source/profile contract for candidate generation. Keep the historical 0.3.1 checks rather than weakening them to get a green result. |
| Production native emitter | Given the candidate source, its legacy common-parent rule recreates the two omitted mixed sets. | The explicit retained-set policy must become the selected input route for the new source. The separate B0-2 emitter already honors it. |
| Production concept dictionary | Its source-version/binding guard rejects the new candidate. | A new version-bound structural receipt and dictionary build are needed; archived 80-concept pages must not be relabeled as the 82-concept candidate. |

These incompatibilities are measured promotion blockers. The unchanged old model, database and historical checks are not retroactively declared invalid. Passing frozen historical CI alone would not validate the new candidate.

## Candidate documentation produced

The candidate-only definition pages cover [InformationArtifact](definitions/RKM-C014.md), [Agent](definitions/RKM-C047.md), [EvidenceReference](definitions/RKM-C065.md), [EvidenceItem](definitions/RKM-C066.md), [EvidenceUseRelator](definitions/RKM-C075.md) and [EvidenceReferenceRole](definitions/RKM-C076.md). They retain source IDs, authored definitions, identity commitments, direct parents and incident relations. They are not the published current dictionary or independent external definitions.

The [evidence fragment SVG](evidence-fragment.svg), generated from those source identifiers and relations, shows inheritance for both documentary roles, ordinary pointers, mediations and grounding. It is a selected class-level fragment, not a complete ontology or an instance diagram. The two new evidential-use concepts and conditional data profile remain candidate design choices; factual adequacy of a real grounding record still requires justified interpretation.

## Promotion path

1. **P1 — candidate source/export contract:** declare accepted source version, model/native/policy hashes, namespace/version binding and inventory; route native, OWL, SHACL and dictionary generation through it. Test both the frozen and new routes. Do not obtain acceptance by merely deleting count/version guards.
2. **P2 — evidential-use relational contract:** define how a justified use, its participating reference, evidence artifact, grounding record, context and purpose are recorded and exported. Preserve information-only records. Test positive, negative, missing-data and before/after migration cases on a small synthetic slice; do not backfill real source data without justification.
3. **P3 — reader and publication reconciliation:** generate current candidate definitions/diagrams/reader bindings from the accepted source contract, exercise the candidate CI route, and select which independently versioned artifacts are ready for promotion.

Issue #93 remains open. The three repair targets have candidate implementations and scoped tests, but production promotion and downstream reconciliation have not been completed. RiskCase migration in #92, broader independent review in #23 and relational tasks in #12/#35 remain separately tracked. Manuscript 7.2.21 and its Word/clean/highlighted PDFs remain unchanged and continue to describe their pinned baseline.

## Replay

Use the pinned [B0-1 Python/schema/ROBOT dependencies](../issue93-evidence-use/README.md#replay), and `ontouml-js` 1.0.0. From the repository root:

```sh
node --version
python evaluation/manuscript-review/v7.2.3/issue93-integration/check_integration.py --schema /tmp/ontouml-schema.json --robot /path/to/robot-1.9.11.jar --sdk /path/to/node_modules/ontouml-js --node /path/to/node
```

The SDK runner changes only the generated-ID seeding call to `networkInterfaces`; all source model IDs are explicit, and no serializer rule is modified. Compatibility probes redirect generator input paths in memory without modifying production files or validation rules. All SQLite inputs in this packet are existing synthetic fixtures, not the pharmaceutical archive or production data. Generated RDF serialization hashes identify the actual inputs of each execution; blank-node serialization may change on replay.
