# Explicit-data profile 0.1.0: decisions and boundary

This engineering review implements the first batch of issue #5. It does not modify conceptual model 0.3.1, redefine domain publication, or supply independent semantic acceptance. The [run report](report.md) and [full JSON snapshots](report.json) record the execution evidence. Base shapes and their receipt are in `ontology/shacl/0.1.0/`.

| Decision | Implemented interpretation | Remaining obligation |
| --- | --- | --- |
| Raw staging | Empty managed-content shapes; preserve incomplete and conflicting assertions | Syntax/parsing succeeds, but no managed or task-readiness claim follows. |
| Managed focus | Explicit class members (including source-subclass paths) and subjects of the selected properties | Other classes, endpoints, datatype/provenance fields and catalog admission are not implemented in this batch. |
| C-06 identity | For admitted relators require exactly one bearer and authority, matching role types, and explicit `differentFrom` evidence after asserted `sameAs` normalization | This conservative admission policy does not verify identities in the real world or prove assignment grounding. No unique-name assumption. |
| C-08 anchor | At least one explicit indicator or scale, with reviewed local maxima and target kinds | Dual-anchor unit/scale compatibility lacks an approved schema; managed structural conformance is not compatibility. Dual-anchor task-ready cases are BLOCKED. |
| C-09 publication | The caller explicitly supplies the published-description targetNode list; published focus must be typed RiskDescription and have a case/pattern/scenario target | An omitted target list is an empty C-09 focus population, not evidence that ordinary descriptions are publication-ready. No publication class is added to the ontology. |
| C-25 selected versions | Every selected version has exactly one named `versionOf` target of the proper artifact kind; aliases normalize before counting/comparison | Presence of each optional/required uses-version link belongs to endpoint validation, which is not implemented here. |
| C-25 direct references | Context uses `R-45 assessmentContext`, Method uses `R-46 usesMethod`, Scale uses `R-14 usesScale`; require equality to the version target whenever the direct link is present | The source has no direct criteria-artifact reference, so no criteria direct-link check is invented. |
| Type checking | Append only the 66 source subclass triples; run SHACL with inference `none` | No domain/range typing, OWL existential fillers, sameAs reasoner or imports can conceal missing explicit data. |
| Identity normalization | For non-raw profiles, transitive undirected asserted sameAs closure on named IRIs; lexical canonical representative; retain types/links; symmetrize differentFrom | Unsupported blank-node identity assertions are rejected as an identity-profile error, not a domain contradiction; raw data are preserved. |
| Negative oracle | Compare exact top-level source-shape and constraint-component sets | Persist full validation text/RDF, including nested shape details; do not accept an unrelated failure. |

The publication list, identity policy and profile name are required operational inputs, not truths inferred from the risk domain. The current scalar/units vocabulary remains undecided. None of the three scoped PASS constraint rows stands for independent semantic correctness or for all 359 SHACL obligations.

The next batch should implement all 254 ordered endpoint obligations, including deliberate direct/inverse path controls and explicit reasons for non-applicable below-minimum/above-maximum fixtures. Then implement the 80 catalog-admission rows and remaining constraint profiles. Independent reviewer decisions, real-case adequacy and acceptance/CQ tests remain in #6/#7/#8/#13.
