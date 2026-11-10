# Evidence Use Relator — current-source curation preview

**N2 documentary preview; not a deployed reader or independent validation.**

## Authored source, preserved verbatim

A context-qualified evidential-use relationship connecting a qualified reference and a distinct information artifact used as support, challenge or context in an analysis. Its grounding concerns that use, not the truth of the referenced claim.

- Source: [RKM-C075, model 0.3.2](https://github.com/ArazSaieArasi3/riskium/blob/70538985cc74179505260e3167517d93579cdc66/ontology/0.3.2/riskium-model.json)
- Subdomain: D09 — Risk Evidence
- Stereotype: relator; identity supplier: RKM-C075
- Identity basis: One grounded use episode qualified by its reference, evidence artifact, analysis context and evidential purpose; different descriptions of that same use do not supply new identities.
- Typing rationale: Relator candidate: a grounded evidential-use relationship, with two distinct mediated documentary participants. The information describing a proposed use is not automatically an instance of this relator.
- Authored verification status: ISOLATED_CANDIDATE; scoped source, OWL and explicit-data tests recorded separately

Historical source status strings are retained. The [publication receipt](https://github.com/ArazSaieArasi3/riskium/blob/70538985cc74179505260e3167517d93579cdc66/evaluation/releases/v0.3.9/R2b-outcome.md) separately records the actual bounded qualification and delivery; neither is an independent semantic rating.

## Documentary decision

**ANALOGY**, replacing/retaining the prior disposition `NO_PRIOR_ROW`.

Use an analogy to provenance usage while preserving the different participant structure. Riskium objectifies a grounded use linking a qualified reference and an evidence artifact, with context and purpose. RE-001 and RE-002 mediate the participants; RE-003 records grounding. OntoUML C2 supplies a minimum-count rule; distinct participants are an additional Riskium C-26 commitment, not a conclusion from that sum.

| Purpose | Selected term / locator |
|---|---|
| External comparison | [prov:Usage](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Usage) — §4.3, Usage |
| External comparison | [prov:qualifiedUsage](https://www.w3.org/TR/2013/REC-prov-o-20130430/#qualifiedUsage) — §4.3, qualifiedUsage: domain Activity, range Usage |
| Modeling foundation | [OntoUML Relator](https://ontouml.readthedocs.io/en/latest/classes/sortals/relator/index.html) — Definition; constraints C1-C2 |

## Illustrations, not executed tests

Illustration: A documented analysis uses a particular report as support through a distinct qualified reference and a grounding record.

Counterexample: A proposed citation without grounded use is information; reusing one individual at both mediated ends violates Riskium C-26.

## Traceability and limits

Authored concept SHA-256: `8b0054d4f2a202d97fdd004a8943ef53295b4397f63fbe756e1bf72e09edb0bc`.

Definition SHA-256: `45f3009f515aa0004ba84ae3ce330d6d4e93cd362ba56249d2ddf8159d796639`.

Formal alignment remains unassessed; no equivalence or subclass axiom is emitted. Independent validation was not performed in this packet. Exact normative crosswalks remain separate in #78; #23 owns independent review. Full current curation still needs the other 74 dispositions and publication/readback.
