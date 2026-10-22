# Semantic assurance: what can and cannot be quantified

## Current answer for Riskium

**An overall semantic-correctness percentage is not currently estimable from the recorded evidence.** The HermiT obligation coverage (281/295, 95.25%), its 693 matching case outcomes, and the scoped SHACL results are engineering evidence for specified questions on exact artifacts. They cannot be converted into the probability that the entire ontology accurately represents risk knowledge. No numerical overall correctness score is assigned.

The [semantic review register](semantic-review-register.json) starts an independent evidence track: **295 typed-core element groups**, plus **4 boundary/anchor groups** and **20 requirement/CQ groups**. Every group lists its review aspects. It currently records no independent adjudications, so review completion is 0/295 for the core. This is a statement about recorded review progress, not a claim that the ontology is 0% correct. The 295 here happens to use the same class/relation/generalization/constraint grouping as the HermiT plan, but its judgments and denominator meaning are independent. A group is not a single atomic semantic proposition; all listed aspects must be assessed before acceptance.

## The distinction that governs the claims

OWL consistency asks whether an interpretation satisfying the axioms exists. Entailment asks whether a conclusion follows in the relevant models. These are formal properties of the encoded axioms. They do not verify that the chosen definitions, identity conditions or axioms match the intended risk domain. SHACL conformance asks whether one supplied data graph satisfies one supplied shapes graph, under its declared targets and inference policy. An omitted or mistaken shape can still yield a green report. W3C specifies these respective formal tasks in [OWL 2 Direct Semantics, section 2.5](https://www.w3.org/TR/2012/REC-owl2-direct-semantics-20121211/#Inference_Problems) and [SHACL 2017, section 3](https://www.w3.org/TR/2017/REC-shacl-20170720/#validation).

SABiO separates building an ontology according to its specifications (verification) from building one adequate for its intended purpose (validation). It calls for expert/user participation and real-world instantiation in addition to CQ-driven tests. SABiOx likewise separates CQ verification, instance validation and operational query testing. See [Falbo 2014, sections 3–4](https://nemo.inf.ufes.br/wp-content/papercite-data/pdf/sabio__systematic_approach_for_building_ontologies_2014.pdf) and [Aguiar and Souza 2024, section 2](https://ceur-ws.org/Vol-3905/paper1.pdf).

Our assurance decision is therefore relative to a declared version, domain boundary, intended uses, requirements, interpretation policy, evidence population and reviewer process. It does not claim exhaustive knowledge of all possible real situations or interpretations.

## Required evidence and measures

| Evidence axis | Measure and denominator | Acceptance proposal for a scoped release | Current recorded status |
| --- | --- | --- | --- |
| Domain/requirement scope | Adjudicated in-scope requirements and CQs / declared requirements and CQs | Every MUST requirement and CQ has an independent oracle and a traceable result | 12 requirement and 8 CQ execution/adequacy tasks remain #6 |
| Meaning and grounding | Accepted element groups / independently reviewed element groups; separately reviewed / total in-scope groups | Domain expert and ontology engineer independently assess definitions, identity, dependence, stereotypes, relations and constraints; all critical disagreements resolved | Register initialized; no independent adjudications recorded in it (#7) |
| Source interpretation | Accepted source-to-claim mappings / inspected mappings; reviewed portions / declared relevant source portions | Exact document versions, source locators, original meaning and same/close/different judgments retained | Public reference-corpus review open (#8) |
| Formal logic | Executed obligations / all applicable obligations; intended entailment and forbidden-inference accuracy by family | No unexplained inconsistency, unsatisfiable core class or critical false inference; unsupported rules retain replacement evidence | HermiT 281/295 scoped passes; 14 NOT_RUN routes retained (#4) |
| Explicit-data rules | PASS, PARTIAL, BLOCKED and NOT_RUN counts against the full 359-row baseline | Each admission rule has valid, invalid, incomplete and boundary cases with the intended violation; profile and inference policy explicit | First four-constraint SHACL batch executed; C-08 compatibility remains partial (#5) |
| Representation adequacy | Correctly mapped independently selected real cases / adjudicated cases, by domain/stratum | Held-out real risk cases with sources, counterexamples and ambiguous/missing-data scenarios; record loss and invented facts | Independent literature case study open (#13), expert interpretation #7 |
| Query usefulness | Correct answer sets / held-out CQ tasks, with precision/recall where applicable | Compare exact expected answers, including unknown and prohibited inference cases | Formal CQ execution pending (#6) |
| Operational preservation | Passing history, calculation and mapping requirements / approved operational requirements | Test version immutability, joins, identity preservation, round trips and calculations; log semantic loss explicitly | Relational/application reconciliation open (#12) |
| Test sensitivity | Rejected non-equivalent mutants / reviewed non-equivalent mutants | Important omitted/reversed/weakened constraints are detected; equivalent mutants separately justified | Selected HermiT and SHACL mutations executed; no universal mutation score claimed |
| Reproducibility and claims | Reproduced claims / published claims; unresolved critical findings | Exact source/input hashes, commands, versions, receipts and manuscript wording agree | Versioned receipts available; final manuscript reconciliation open (#14) |

These acceptance proposals are a project policy, not universal scientific thresholds. An average must not hide an unresolved critical identity or interpretation error. Predefine severity and release-blocking criteria before adjudication.

## How a defensible percentage would be calculated

1. **Review completion:** independently adjudicated groups divided by all declared groups. This measures review coverage. It never measures truth by itself.
2. **Semantic acceptance among reviewed groups:** accepted groups divided by reviewed groups; report unresolved/ambiguous groups separately. Also report accepted groups divided by the full inventory so selective review cannot inflate apparent completion. Preserve reviewer roles, exact source evidence, counterexamples and decisions.
3. **Held-out task accuracy:** number of independently specified expected outcomes matched divided by held-out tasks. Define the population and outcome classes first; an unknown claim must not be relabeled false. For query answers, report precision (correct returned answers / returned answers) and recall (correct returned answers / all expected answers) separately.
4. **Agreement:** report raw reviewer agreement and, for two independent categorical raters, Cohen's kappa (or an appropriate multi-rater measure). Agreement reflects reproducibility of judgments, not their infallibility. A third reviewer adjudicates disagreements while preserving initial ratings.
5. **Sampling uncertainty:** only when sampling is representative and sufficiently independent, attach confidence intervals to the observed task performance. Avoid treating correlated template fixtures as independent real-world samples.

For example, if a representative independent sample has **zero errors in n cases**, an exact one-sided 95% binomial upper bound on error probability is `1 - 0.05^(1/n)`. For n=300 this is about **0.994%**. Observing 300/300 successes can support a conditional bound near 99% for that sampled task population; it cannot prove a 100% error-free ontology. This calculation is a proposed statistical interpretation, not a Riskium result and not applicable to the current synthetic suite without the sampling assumptions.

A weighted composite may summarize agreed quality dimensions only if its weights and missing-evidence rules are declared in advance. It must be named an **assurance/quality score**, never a probability of universal semantic truth. No such composite is currently assigned to Riskium.

## What a 100% statement may legitimately mean

It is possible to report **100% of a finite declared review inventory adjudicated**, **100% of a named test suite matched**, or, with a formal proof, **a precise property established under explicit axioms and assumptions**. Those claims have bounded denominators. None establishes the correctness and completeness of every domain statement for all real-world situations.

For a formal target semantics, one could seek soundness (the encoding permits no interpretations excluded by the specification) and completeness (it does not exclude intended interpretations), with an explicit translation and proof obligations. Even a successful proof is conditional on the reference specification and assumptions being adequate for the domain. The ordinary risk domain has no independently known exhaustive inventory of all true facts and intended interpretations against which a universal 100% figure could be measured.

The release claim should instead say: **evaluated for the declared risk-knowledge scope and intended tasks, with complete execution of the stated acceptance suite, no unresolved critical findings, documented expert judgments and explicit residual limitations**. The exact wording must follow the evidence actually obtained; Riskium does not yet meet all of these gates.

## Next semantic review batch

In #7, independently adjudicate the identity cluster first: RiskCase, register entry/revision, scenario specification, description/occurrence, responsibility assignment/relator, and selected artifact versions. Use sourced real and counterexample instances, not just the fixture generator. Domain-expert review and ontology-engineer review should be independent before adjudication. Expand to all 295 core groups and the boundary/acceptance cohorts; reconcile #6, #8 and #13 evidence. Do not overwrite these pending rows with automated PASS outcomes.
