# Treatment Decision Information — N3b-5 documentary preview

**Planning preview; not deployed or independently validated.**

## Authored definition, unchanged

A recorded decision about treating risk, including the selected option, rationale, responsible authority and relevant basis.

[Source model 0.3.2](https://github.com/ArazSaieArasi3/riskium/blob/64ebfa6c9bec92184f5671cb6d5aef6397b0a9e1/ontology/0.3.2/riskium-model.json); subdomain D06; stereotype subkind; identity supplier RKM-C014.

Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.

Authored verification status, preserved verbatim: Bounded review and finite tests; native OntoUML and independent semantic validation pending

Later bounded qualification/publication evidence is in the [v0.3.9 receipt](https://github.com/ArazSaieArasi3/riskium/blob/64ebfa6c9bec92184f5671cb6d5aef6397b0a9e1/evaluation/releases/v0.3.9/R2b-outcome.md). Source labels and documentary comparisons are not independent semantic ratings.

## Documentary comparison

**CONTRAST → CONTRAST**.

Retain the contrast between a recorded choice and a response process. The NIST glossary entry is security-specific and attributed there to SP 800-39; it does not establish that a Riskium decision was authorized, executed or successful.

| Selected term | Source kind and locator |
|---|---|
| [Risk Response](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf#page=60) | SECURITY_RISK_RESPONSE_PROCESS_TERM; Appendix B, printed B-10, PDF page 60; attributed there to SP 800-39 |

## Current structural context

R-19 relates the decision to the continuing RiskCase; R-20 selects a strategy. R-63 and RK2-014/RK2-015 may connect plans, evaluation and remaining-risk assessment. Those documentary links do not alone establish treatment execution or effectiveness.

Source continuity: concept record unchanged=True; direct edges unchanged=True; inherited edges unchanged=True. Ancestor and neighbor changes are reported separately.

| Observation | Source-bound result |
|---|---|
| Inheritance path | G-14: RKM-C041 → RKM-C014 |
| Source constraint route | C-01, C-02, C-04, C-07, C-19 — [selected source statements](../treatment-policy-checks.json) |
| Changed ancestor | RKM-C014: typing_rationale |
| Changed relation neighbor | RKM-X01: definition, identity_basis, typing_rationale |
| Excluded blanket sets | GS-RKM-C014 |

Recorded choices, plans and references remain information; actual activity, realized controls and effectiveness need their own support. Vocabulary labels do not establish resource identity, authority or cross-framework equivalence. Source-qualified appetite/tolerance statements and their contexts are preserved without importing unseen normative terms.

Complete source observations are in [contexts.json](../contexts.json). Context SHA-256: `0fc335d3b9dc77c3ffb8f5b159c44d30e3f3837187cae910d1d2a91e1e08e732`.

Authored definition SHA-256: `d1cd1366f12f99a04db3e865587c0ed549f239ae783735c38d10ac209ef11b0c`.

No formal alignment axiom, new ontology-engine execution or independent expert rating is supplied. Remaining documentary batches, full component qualification and actual publication/readback retain their separate gates. #23 and #78 remain separate.
