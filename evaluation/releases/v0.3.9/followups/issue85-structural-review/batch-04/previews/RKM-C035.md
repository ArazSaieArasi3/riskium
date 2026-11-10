# Assessment Method Specification — N3b-4 documentary preview

**Planning preview; not deployed or independently validated.**

## Authored definition, unchanged

A versioned specification of procedures and rules used to produce and interpret assessment results.

[Source model 0.3.2](https://github.com/ArazSaieArasi3/riskium/blob/8a115ef9c3fb6b0501c6ed9c9fd6b258d358028e/ontology/0.3.2/riskium-model.json); subdomain D05; stereotype subkind; identity supplier RKM-C014.

Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.

Authored verification status, preserved verbatim: Bounded review and finite tests; native OntoUML and independent semantic validation pending

Later bounded qualification/publication evidence is in the [v0.3.9 receipt](https://github.com/ArazSaieArasi3/riskium/blob/8a115ef9c3fb6b0501c6ed9c9fd6b258d358028e/evaluation/releases/v0.3.9/R2b-outcome.md). Source labels and documentary comparisons are not independent semantic ratings.

## Documentary comparison

**ANALOGY → ANALOGY**.

Retain the reusable procedure/execution distinction from SOSA. A risk assessment method specification adds risk-specific interpretation rules; no SOSA restriction or full method equivalence is adopted.

| Selected term | Source kind and locator |
|---|---|
| [sosa:Procedure](https://www.w3.org/TR/2017/REC-vocab-ssn-20171019/#SOSAProcedure) | SOSA_PROCEDURE_CLASS; §4.8.2.1 |

## Current structural context

R-46/R-50 relate information and scores to a method; R-49 and RK2-018 describe permitted scales/dimensions. The specification retains documentary identity; a separately pinned ArtifactVersion identifies which issued content was used. A procedure description alone is not execution evidence.

Source continuity: concept record unchanged=True; direct edges unchanged=True; inherited edges unchanged=True. Ancestor and neighbor changes are reported separately.

| Observation | Source-bound result |
|---|---|
| Inheritance path | G-11: RKM-C035 → RKM-C014 |
| Source constraint route | C-02, C-03, C-04, C-18, C-25 — [selected source statements](../assessment-checks.json) |
| Changed ancestor | RKM-C014: typing_rationale |
| Changed relation neighbor | None in this selected context |
| Excluded blanket sets | GS-RKM-C014 |

Documentary identity is separate from activity, risk identity and real-world values. Comparable interpretation requires the selected method/scale/dimension/basis/context/time or a justified transformation; missing input is not zero. A recorded score does not by itself establish acceptability, and a qualitative uncertainty statement need not contain probability.

Complete source observations are in [contexts.json](../contexts.json). Context SHA-256: `77d0bac1b91e8fffe84b9efd2e9558c571cd3d7da8fb88047d10a489a4203a49`.

Authored definition SHA-256: `0eff419744009802d6a0bd99de7205985cd8ab4ddc7f9523714220f9f806172a`.

No formal alignment axiom, new ontology-engine execution or independent expert rating is supplied. Remaining documentary batches, full component qualification and actual publication/readback retain their separate gates. #23 and #78 remain separate.
