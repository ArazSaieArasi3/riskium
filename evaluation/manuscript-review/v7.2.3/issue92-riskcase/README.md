# Analytical RiskCase successor candidate

B2 implements the approved B1 source delta while retaining the EvidenceItem dependency repair and explicit generalization-set policy. Source design version `0.3.2-case.1` is a candidate identifier, not a published release tag. The frozen 0.3.1 scientific baseline and earlier B0 packets remain unchanged.

The candidate distinguishes analytical item identity, explicit analytical task readiness, and local operational-register eligibility. Context/objective minima and stable case/entry distinctions are retained. Approval is not a universal ontology requirement. The local operational profile requires a selected entry, recorded approval and a named approval-source reference; these are explicit-data conditions, not independent verification of an authorization event.

[Input contract](input-contract.json) · [Source model](candidate-model.json) · [Native exchange](candidate.ontouml.json) · [OWL](candidate.owl.ttl) · [Reader](reader/README.md) · [Profiles](case_profiles.py) · [B1 oracles](../issue92-impact/acceptance-oracles.json)

Execution results are recorded by the verifier in a distinct output directory. Live publication/current-source selection is a later coordinated-release gate; local generation does not close #92/#93 or revise manuscript 7.2.21.

The first CI run exposed an untracked generated B0 source dependency before B2 tests started. The successor now reconstructs that exact prior model in a temporary input route, verifies its B1/B0 hash and uses the unchanged historical validator. No old model or receipt is overwritten. Other tracked prior bindings retain their original checks.
