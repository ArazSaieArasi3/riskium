# Analytical RiskCase successor candidate

B2 implements the approved B1 source delta while retaining the EvidenceItem dependency repair and explicit generalization-set policy. Source design version `0.3.2-case.1` is a candidate identifier, not a published release tag. The frozen 0.3.1 scientific baseline and earlier B0 packets remain unchanged.

The candidate distinguishes analytical item identity, explicit analytical task readiness, and local operational-register eligibility. Context/objective minima and stable case/entry distinctions are retained. Approval is not a universal ontology requirement. The local operational profile requires a selected entry, recorded approval and a named approval-source reference; these are explicit-data conditions, not independent verification of an authorization event.

[Input contract](input-contract.json) · [Source model](candidate-model.json) · [Native exchange](candidate.ontouml.json) · [OWL](candidate.owl.ttl) · [Reader](reader/README.md) · [Profiles](case_profiles.py) · [B1 oracles](../issue92-impact/acceptance-oracles.json)

Execution results are recorded by the verifier in a distinct output directory. Live publication/current-source selection is a later coordinated-release gate; local generation does not close #92/#93 or revise manuscript 7.2.21.

The first CI run exposed an untracked generated B0 source dependency before B2 tests started. The successor now reconstructs that exact prior model in a temporary input route, verifies its B1/B0 hash and uses the unchanged historical validator. No old model or receipt is overwritten. Other tracked prior bindings retain their original checks.

## Observed B2 outcome — 2026-11-09

**B2 is complete as a tested candidate.** [Actual CI run 42635305088](https://github.com/ArazSaieArasi3/riskium/actions/runs/42635305088) succeeded on executable commit `47a9fc1b966441898f967b6830d45c500955d0c0`. It first passed the nine B0 replay/staging phases, then passed all twenty B1-declared RiskCase acceptance cases. The [actual combined CI artifact](https://github.com/ArazSaieArasi3/riskium/actions/runs/42635305088/artifacts/13682158895) preserves each phase's own receipts and raw execution evidence. See [ci-receipt.json](ci-receipt.json) and [verification-report.json](verification-report.json).

| Check | Actual result and interpretation |
|---|---|
| Predeclared cases | 20/20 expected outcomes matched. This is finite acceptance coverage, not a semantic-correctness percentage. |
| Explicit-data checks | 13 pySHACL invocations, including the deliberate deleted-approval-rule mutant. Missing approval is unknown; denial and wrong-case joins are ineligible. A wrong entry remains ineligible even when approval is also unknown. |
| Logical checks | Eight fresh HermiT invocations matched: six satisfiable and two explicitly inconsistent controls. Missing explicit context/objective is distinct from denying their existence. The exact InconsistentOntologyException is recognized; arbitrary engine errors are not counted as negative successes. |
| Native / OWL | Zero pinned native-schema errors; direct ontouml-js 1.0.0 round-trip preserved 596 elements; ROBOT 1.9.11 accepted OWL 2 DL. The documentary-normalized logical graph is isomorphic to B0-4. |
| Reader | 82 catalog dossiers plus the external anchor, 92 files, 2,607 local links and 93 explicit anchor occurrences checked. The corrected source note matches 82 concepts, 137 associations, 130 formal relations and eight explicit sets. |
| SQLite / query | The unchanged identity/history slice stored a case without an entry, retained two entries about one case, distinguished equal-label identities and rejected cross-family identity. Selected two-column SQL/SPARQL answers agree. This does not persist all context/approval semantics or establish PostgreSQL behavior. |
| Preservation | The tracked scientific/SQL/source-cohort inputs stayed unchanged; the old withheld cohorts were not reclassified. Prior packets and their source-specific validators/receipts remain separate. |

The earlier failed CI run is retained and explained in the receipt; it was repaired through an explicit derived-input route, not a weakened guard or a blind rerun. The source reconstruction matches the original B1/B0 hash. A separately recorded local execution of the exact final executable commit also passed; it is not presented as the remote runner's raw receipt.

### Remaining coordinated-release gates

R1 selects and qualifies the next current scientific source and component closure, including successor HTML/Wiki projections. R2 packages and independently verifies the assets, publishes the selected distribution, then reads back maintained repository/Wiki/Pages bodies. This candidate has not been promoted or published; #92/#93 remain open for those acceptance steps. Manuscript 7.2.21 is unchanged. Wider expert, dataset, modularity, deployment and product work remain outside this finite release gate.
