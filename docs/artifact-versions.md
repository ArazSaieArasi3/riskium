# Artifact versions and compatibility

This lightweight compatibility record implements the owner's 24 October 2026 request to keep the paper, ontology requirements, model and database coordinated. [The machine-readable matrix](../releases/artifact-matrix.json) pins exact component hashes. **[v0.3.1](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.1) is published and independently downloaded/verified**, source `8afe169968b5c1396c02834dbc499af691b894b4`. Current coordination matrix revision is 0.1.1; the release asset retains frozen matrix 0.1.0. [Publication receipt](../evaluation/releases/v0.3.1-publication.json) closes #28.

| Artifact | Own version | Compatible model | Current boundary |
| --- | --- | --- | --- |
| Conceptual ontology and derived representations | 0.3.1 | 0.3.1 | Conceptual/native/OWL bytes unchanged from accepted technical baseline; derived artifacts keep their generation/evidence bindings. |
| Selected ontology diagram | model-0.3.1 | 0.3.1 | Existing approved diagram and layout remain unchanged. |
| Ontology requirements specification | 0.4.3 | 0.3.1 | Documentation/evidence/scope revision; original MUST/SHOULD priorities, criteria and source JSON definitions preserved. |
| Owner scope review | 0.1.0 | 0.3.1 | Nine scoped acceptances, one implemented prose revision and one conditional technical publication gate; not independent. |
| Public SQLite identity/history profile | 0.1.0 | 0.3.1 | Unchanged bounded public schema/profile with migrations 1 and 2; distinct from private historical SQLite v0.3.0-rc.1. PostgreSQL/full migration not claimed. |
| Declared metadata compatibility profile | 0.6.0 | 0.3.1 | Historical separately bound supplement; global C-08 PARTIAL retained. |
| Selected comparison profile | 0.7.0 | 0.3.1 | Scoped C-13/C-18 task eligibility; no generic arithmetic/conversion. |
| Source trace cohort/profile | 0.2.0 | 0.3.1 | 13 inspected statements; 35 query/control outcomes; no independent population acceptance. |
| Correction and withheld-identity cohort/profile | 0.3.0 | 0.3.1 | Five selected old/reissued pairs and 11 still-withheld candidates; 59 query/control outcomes. |
| Article Word and equivalent PDF | 7.0.8 | 0.3.1 | Nine-page manuscript; seven necessary paragraphs updated and final delivery readback verified. Binaries stay outside public source repository. |

## Change rules

- Components retain independent versions. A package release pins an explicit set of component versions, exact content hashes and source commit.
- An editorial paper change increments the paper revision only; semantic model changes need reviewed model versioning and refreshed affected mappings/tests.
- An ORSD scope/evidence edit increments the ORSD documentation revision; no silent deletion/downgrading of original MUST priorities.
- Database schema/profile changes have their own migration sequence and version, ontology mapping and preservation evidence. Historical private and current public schemas never share implied compatibility.
- A changed model, requirement scope, schema, cohort or interpretation triggers review of its affected dependency links and evidence. No test receipt is inherited across changed evaluated inputs.
- A versioned JSON manifest and readable table are the current implementation. Broader artifact-lifecycle automation is future work and does not block v0.3.1.

The archived pharmaceutical dataset v0.6 and private SQLite v0.3.0-rc.1 retain their historical bindings; this matrix does not turn them into public reruns or the current SQL implementation. The historical quality synthesis and preparation package remain identifiable snapshots. The final release source commit and publication receipt are now recorded. Component versions and hashes below remain unchanged; the frozen release asset preserves its decision-time matrix, while this current table points to the publication outcome.

Check synchronization with `python tools/check_release_alignment.py`. This validates source/document bindings and recorded artifact relations; CI does not freshly render author-facing Word/PDF files or perform independent semantic review.
