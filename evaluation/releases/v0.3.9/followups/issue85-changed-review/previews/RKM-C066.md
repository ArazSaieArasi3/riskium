# Evidence Item — current-source curation preview

**N2 documentary preview; not a deployed reader or independent validation.**

## Authored source, preserved verbatim

An information artifact playing an evidential role for a specified claim or analytical activity. The same artifact may be used as evidence in one context and not another.

- Source: [RKM-C066, model 0.3.2](https://github.com/ArazSaieArasi3/riskium/blob/70538985cc74179505260e3167517d93579cdc66/ontology/0.3.2/riskium-model.json)
- Subdomain: D09 — Risk Evidence
- Stereotype: role; identity supplier: RKM-C014
- Identity basis: Inherits bearer identity; role membership depends on an explicit responsibility or evidential context.
- Typing rationale: Anti-rigid documentary role founded through mandatory mediation by EvidenceUseRelator. The artifact retains InformationArtifact identity when not used as evidence.
- Authored verification status: Bounded review and finite tests; native OntoUML and independent semantic validation pending

Historical source status strings are retained. The [publication receipt](https://github.com/ArazSaieArasi3/riskium/blob/70538985cc74179505260e3167517d93579cdc66/evaluation/releases/v0.3.9/R2b-outcome.md) separately records the actual bounded qualification and delivery; neither is an independent semantic rating.

## Documentary decision

**RELATED**, replacing/retaining the prior disposition `RELATED`.

Retain the external comparison and separately document the role foundation. EvidenceItem inherits artifact identity; RE-001 makes participation depend on grounded use. It does not classify every artifact as evidence everywhere.

| Purpose | Selected term / locator |
|---|---|
| External comparison | [prov:Entity](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Entity) — §4.1, Entity |
| External comparison | [prov:Role](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Role) — §4.3, Role |
| Modeling foundation | [OntoUML Role](https://ontouml.readthedocs.io/en/latest/classes/sortals/role/index.html) — Definition; constraints C1-C2 |

## Illustrations, not executed tests

Illustration: A retained report plays an evidential role in one grounded analysis and remains the same artifact afterwards.

Counterexample: A bibliography mention alone does not establish actual evidential participation or claim truth.

## Traceability and limits

Authored concept SHA-256: `b696da9d9a1575566fcd206f41ff129f9354588ae16cfa4280e5db660388be17`.

Definition SHA-256: `c6502f7d2313be099df7c4e02c48ed72042d7aa9041d20869e6baaeaead2a77b`.

Formal alignment remains unassessed; no equivalence or subclass axiom is emitted. Independent validation was not performed in this packet. Exact normative crosswalks remain separate in #78; #23 owns independent review. Full current curation still needs the other 74 dispositions and publication/readback.
