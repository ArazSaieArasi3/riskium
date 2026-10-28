<p class="eyebrow">Riskium · Ontology model 0.3.1</p>

# Risk knowledge, with its meaning intact

A risk register brings together scenarios, judgments, responsibilities and evidence. Those records can refer to the same risk while describing different things. Riskium makes these distinctions explicit so that a changing description or assessment need not be mistaken for a new risk case.

<p class="lead">Start with the conceptual explanation, inspect the formal commitments, then examine what the recorded evaluation actually supports.</p>

<div class="actions"><a class="button primary" href="guide/Overview.html">Understand the model</a><a class="button" href="reference/search.html">Find a concept or relation</a></div>

<div class="stat-strip"><div><strong>80</strong><span>catalog concepts</span></div><div><strong>134</strong><span>relations and bridges</span></div><div><strong>25</strong><span>interpretation constraints</span></div><div><strong>78 / 127</strong><span>OWL classes / properties</span></div></div>

## Choose a reading route

<div class="cards"><section class="card"><p class="eyebrow">Meaning</p><h3>Understand the distinctions</h3><p>Why a risk case, a register entry, a possible scenario and an actual occurrence have different identities.</p><a href="guide/Overview.html">Read the conceptual guide</a></section><section class="card"><p class="eyebrow">Specification</p><h3>Inspect the commitments</h3><p>Browse the full conceptual catalog or the narrower asserted OWL profile, with links between them.</p><a href="widoco/index-en.html">Open the WIDOCO reference</a></section><section class="card"><p class="eyebrow">Evidence</p><h3>Assess the support</h3><p>Read the purpose, populations and limits of reasoning, explicit-data, integration and database checks.</p><a href="guide/Evaluation.html">Read evaluation and limitations</a></section></div>

## Follow one case through the model

A continuing **RiskCase** can have a register entry and successive descriptions. A **RiskScenarioSpecification** describes a possibility; a **RiskOccurrence** is an actual occurrence. An **AssessmentInformation** artifact documents an assessment, while a **DimensionAssessmentResult** records a result under a declared dimension and scale. These distinctions let a reader ask what changed: the case, its description, the assessment basis, or the evidence available.

<p><a href="reference/native/index.html#RKM-X01">Read the RiskCase definition</a> · <a href="reference/diagrams/index.html">Read the conceptual diagrams</a> · <a href="WEBVOWL_ROUTE">Explore the asserted connections</a></p>

## What the evaluation supports

The recorded HermiT suite has 693 matching cases and covers 281 of 295 baseline obligations; 14 remain NOT_RUN. The historical SHACL ledger records 341 scoped PASS, one PARTIAL and 17 NOT_RUN out of 359 obligations. Later integration, SQL and source-query evidence has its own inputs and scope.

These populations answer different questions. They do not yield an overall ontology-correctness percentage. Independent semantic review has no recorded responses; eleven organizational identity candidates remain WITHHELD. [Evaluation](guide/Evaluation.html) connects each result to its receipt and explains the remaining limits.

## Use the sources

Use [Latest published source release](https://github.com/ArazSaieArasi3/riskium/releases/latest) for the live source-distribution destination. At the **28 October 2026** checkpoint, **v0.3.3** is published and **v0.3.4** is being prepared under [#45](https://github.com/ArazSaieArasi3/riskium/issues/45). The ontology model remains **0.3.1**; this maintained documentation component is **0.3.0**. The conceptual and OWL downloads preserve the original model source. [Version policy](guide/Publication.html) separates those identities.

Development after v0.3.3 adds source/scenario storage **0.4.0**, correction lineage **0.5.0** and qualified evidence **0.6.0 / migration 7**. Their bounded completion records retain exact old values, sources and contextual evidence roles; they are proposed components of v0.3.4. The checked evidence implementation has **62 fixed controls and 280 full software tests**; those are engineering results, not new HermiT/SHACL outcomes. [The work plan](guide/Work-Plan.html) identifies the remaining component selection, documentation snapshot, freeze and publication gates.

[Download the model and RDF](downloads/index.html) · [Reproduce the finite checks](guide/Reproduce.html) · [Authors and citation](guide/Citation.html) · [Scope and limitations](guide/Limitations.html)
