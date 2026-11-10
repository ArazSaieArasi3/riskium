# Evidence Reference Role — current-source curation preview

**N2 documentary preview; not a deployed reader or independent validation.**

## Authored source, preserved verbatim

A qualified EvidenceReference participating in an actual grounded evidential-use relationship. The reference retains documentary identity when it is only a record of a proposed use.

- Source: [RKM-C076, model 0.3.2](https://github.com/ArazSaieArasi3/riskium/blob/70538985cc74179505260e3167517d93579cdc66/ontology/0.3.2/riskium-model.json)
- Subdomain: D09 — Risk Evidence
- Stereotype: role; identity supplier: RKM-C014
- Identity basis: Inherits InformationArtifact identity through EvidenceReference; role membership depends on grounded evidential use.
- Typing rationale: Anti-rigid participation of a documentary reference, distinct from merely recording a proposed use.
- Authored verification status: ISOLATED_CANDIDATE; scoped tests recorded separately

Historical source status strings are retained. The [publication receipt](https://github.com/ArazSaieArasi3/riskium/blob/70538985cc74179505260e3167517d93579cdc66/evaluation/releases/v0.3.9/R2b-outcome.md) separately records the actual bounded qualification and delivery; neither is an independent semantic rating.

## Documentary decision

**CONTRAST**, replacing/retaining the prior disposition `NO_PRIOR_ROW`.

Distinguish a function description from the documentary reference that participates in grounded use. GE-001 preserves reference identity through EvidenceReference and InformationArtifact; RE-002 supplies the role dependency. The reference can exist as a record of proposed use without this role membership.

| Purpose | Selected term / locator |
|---|---|
| External comparison | [prov:Role](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Role) — §4.3, Role |
| Modeling foundation | [OntoUML Role](https://ontouml.readthedocs.io/en/latest/classes/sortals/role/index.html) — Definition; constraints C1-C2 |

## Illustrations, not executed tests

Illustration: An existing qualified reference participates in an actual grounded use while keeping its documentary identity.

Counterexample: Assigning a PROV function label or recording a proposed use alone does not instantiate this participation role.

## Traceability and limits

Authored concept SHA-256: `21588385b2c67f06002dd2d393f0ea3c1e58a155b6b2ba4b71a9363c53933fd1`.

Definition SHA-256: `5b298a854b7c9de8dcfbe165c84fae2e7955d16c05b0a9ad86acfa7cb22145b4`.

Formal alignment remains unassessed; no equivalence or subclass axiom is emitted. Independent validation was not performed in this packet. Exact normative crosswalks remain separate in #78; #23 owns independent review. Full current curation still needs the other 74 dispositions and publication/readback.
