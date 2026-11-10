# Risk Register Entry — N3b-3 documentary preview

**Planning preview; not deployed or independently validated.**

## Authored definition, unchanged

A managed register record about exactly one RiskCase in this profile. Distinct entries, source systems or registers can record the same case. A software record is an implementation record, not an additional risk subject.

[Source model 0.3.2](https://github.com/ArazSaieArasi3/riskium/blob/446f412e737a9f456addb2b12c63e867a33b70d3/ontology/0.3.2/riskium-model.json); subdomain D04; stereotype subkind; identity supplier RKM-C014.

Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.

Authored verification status, preserved verbatim: Bounded review and finite tests; native OntoUML and independent semantic validation pending

Later bounded qualification/publication evidence is in the [v0.3.9 receipt](https://github.com/ArazSaieArasi3/riskium/blob/446f412e737a9f456addb2b12c63e867a33b70d3/evaluation/releases/v0.3.9/R2b-outcome.md). Source labels and documentary comparisons are not independent semantic ratings.

## Documentary comparison

**RELATED → RELATED**.

Retain generic documentary-entity context without importing case identity or cardinality rules. A register entry is a record about the analytical risk item, not another risk subject.

| Selected term | Source kind and locator |
|---|---|
| [prov:Entity](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Entity) | PROVENANCE_CLASS; §4.1, Entity |

## Current structural context

R-01 targets one RiskCase in this profile and permits zero or many entries per case. R-33 relates distinct entry revisions to their entry; RX-008 assigns register membership. Neither an entry identifier nor organizational admission is the case's universal existence condition.

Source continuity: concept record unchanged=True; direct edges unchanged=True; inherited edges unchanged=True. Ancestor and neighbor changes are reported separately.

| Observation | Source-bound result |
|---|---|
| Inheritance path | G-01: RKM-C022 → RKM-C014 |
| Source constraint route | C-01, C-16, C-24 — [selected source statements](../registration-checks.json) |
| Changed ancestor | RKM-C014: typing_rationale |
| Changed relation neighbor | RKM-X01: definition, identity_basis, typing_rationale |
| Excluded blanket sets | GS-RKM-C014 |

Documentary identity is separate from analytical RiskCase identity and local operational admission. Shared parenthood creates no blanket exclusivity or covering axiom. Vocabulary values, qualified statements and their referents remain distinct; closure and missing authorization do not supply new risk/effectiveness/permission facts.

Complete source observations are in [contexts.json](../contexts.json). Context SHA-256: `2f0cf872897643b397ccdb5c03bfbc112acc09b3a056f9690b99e5f35f8f1fb6`.

Authored definition SHA-256: `0e31304800e9deef5ebc036bc75dfe968fa53a2944312994b78e67918b257e4d`.

No formal alignment axiom, new ontology-engine execution or independent expert rating is supplied. Remaining documentary batches, full component qualification and actual publication/readback retain their separate gates. #23 and #78 remain separate.
