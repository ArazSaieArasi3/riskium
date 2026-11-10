# N3b-2 — structural-context documentary review

Date: 2026-11-10. Planning target v0.3.10; #85 remains open.

**This batch is complete: 10 concepts. Current-source documentary coverage is 46/82 (56.1%); 36 remain.** This fraction is not overall research completion, semantic correctness or independent acceptance.

## What was reviewed

The selected current concept definitions, direct associations/generalizations, complete ancestry, changed ancestor records, changed association-neighbor records, applicable explicit set policy and analytical-case application policy were compared with the historical source. Primary source editions, locators and selected passages were checked separately. An unchanged edge does not hide the change in its endpoint's meaning.

| Concept | Disposition | Current-context interpretation |
|---|---|---|
| [Agent](previews/RKM-C047.md) | RELATED | The explicit AgentKinds set distinguishes human Person from Organization and remains incomplete. Excluding GS-RKM-C047 prevents bearer-kind classification from competing with responsible/authorizing participation. Changed Person/Organization typing rationales are checked at the generalization endpoints. |
| [Actor Reference](previews/RKM-C050.md) | CONTRAST | G-05 inherits InformationArtifact identity; R-53 permits no resolved agent (0..1). The revised documentary rationale does not turn a name, an identifier or local register approval into evidence of an actual mandate. |
| [Responsibility Assignment Information](previews/RKM-C051.md) | CONTRAST | R-55 links the statement to at most one actual mandate and allows none. R-09 concerns an analytical RiskCase; neither this statement nor missing approval determines that case's existence. A named owner alone does not establish responsibility, accountability and approval authority together. |
| [Responsible Agent Role](previews/RKM-C053.md) | ANALOGY | The abstract roleMixin inherits no single sortal identity; its person and organization specializations retain their different identities. R-56 supplies a mandatory inherited mediation dependency. This source structure does not prove that a particular mandate actually exists. |
| [Authorizing Agent Role](previews/RKM-C054.md) | ANALOGY | The abstract roleMixin aggregates person and organization bearers without supplying identity. R-57 supplies the selected mandatory dependency. Responsible and authorizing participation are not globally exclusive merely because they share Agent as a parent. |
| [Responsible Person](previews/RKM-C055.md) | ANALOGY | G-24 provides the sole inherited identity supplier Person; G-25 supplies the ResponsibleAgentRole path and inherited R-56 mediation. The same human can bear different roles across contexts without being duplicated or merged with an organization. |
| [Responsible Organization](previews/RKM-C056.md) | ANALOGY | G-26 preserves the sole Organization identity and G-27 supplies the responsible-role path and inherited R-56 mediation. A corporate representative is not the organization; an organizational record alone is not evidence of a grounded mandate. |
| [Authorizing Person](previews/RKM-C057.md) | ANALOGY | G-28 preserves Person identity, G-29 supplies the authorizing-role path and R-57 is inherited. The non-disjoint Person sibling policy permits different contextual roles without asserting that one person fills both distinct participants of one mandate. |
| [Authorizing Organization](previews/RKM-C058.md) | ANALOGY | G-30 preserves Organization identity; G-31 supplies the authorizing-role path and inherited R-57 dependency. Organizational bearer kinds remain distinct from human representatives, while responsible/authorizing participation is not made globally exclusive. |
| [Responsibility Role Term](previews/RKM-C059.md) | RELATED | The path through ClassificationTerm and VocabularyConcept preserves InformationArtifact identity. R-54 records an assignment's selected term and R-59 a mandate's term; lexical equality alone establishes neither mandate identity nor actual authorization. |

## Findings and limits

All ten authored definitions and local edge records are unchanged. Seven concepts have changed ancestor typing context; ResponsibilityAssignmentInformation also has the revised RiskCase as an association neighbor. Direct generalization endpoints are additionally checked so changes to Person/Organization are visible even at the Agent category.

The four concrete person/organization roles each retain exactly one declared ancestor identity provider and inherit their selected mandatory mediation. Agent and the two roleMixins remain abstract non-sortals; their currently modeled descendant bearer identities are Person and Organization. These are selected static source checks, not ontology-engine executions or evidence that a particular mandate is realized.

The disjoint, incomplete AgentKinds set distinguishes bearer kinds. This differs from global exclusion between responsible and authorizing participation, which is not imposed by the blanket mixed-criterion set. Carried role-subtype criteria retain their source statuses and are not independently reapproved here.

ActorReference may remain unresolved under R-53 (0..1), and the assignment statement may lack an actual mandate under R-55 (0..1). An owner name, a PROV function or a controlled responsibility term alone establishes none of the actual relationship, authorization and accountability commitments.

## Primary sources

- [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/) — W3C Recommendation, 30 April 2013; accessed 2026-11-10. Terms listed below only; no PROV conformance or import asserted.
- [SKOS Simple Knowledge Organization System Reference](https://www.w3.org/TR/2009/REC-skos-reference-20090818/) — W3C Recommendation, 18 August 2009; accessed 2026-11-10. Concept, scheme and lexical-label distinctions; no SKOS mapping triples asserted.
- [OntoUML specification: Role](https://ontouml.readthedocs.io/en/latest/classes/sortals/role/index.html) — Unversioned latest documentation; access date and response digest retained; accessed 2026-11-10. Definition and selected identity/dependency/abstractness constraints only; not an external domain definition or conformance certificate.
- [OntoUML specification: RoleMixin](https://ontouml.readthedocs.io/en/latest/classes/nonsortals/rolemixin/index.html) — Unversioned latest documentation; access date and response digest retained; accessed 2026-11-10. Definition and selected identity/dependency/abstractness constraints only; not an external domain definition or conformance certificate.
- [OntoUML specification: Category](https://ontouml.readthedocs.io/en/latest/classes/nonsortals/category/index.html) — Unversioned latest documentation; access date and response digest retained; accessed 2026-11-10. Definition and selected identity/dependency/abstractness constraints only; not an external domain definition or conformance certificate.

All five primary responses were retrieved directly. The PROV-O and SKOS response hashes match the historical review; the three selected OntoUML foundation pages have access dates and response-body digests of their own. source-access.json and passage-checks.json retain retrieval/locator fingerprints without redistributing documents. Modeling foundations are separate from external domain definitions; no new formal alignment or conformance certificate is issued.

## Verification and reproduction

From the repository root:

```sh
python -B evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-02/build.py --batch batch-02
python -B evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-02/build.py --batch batch-02 --check
```

The validator binds raw source/prior/allocation/passage/context files; recomputes the structural context; checks the declared population and disjoint cumulative coverage; preserves authored definitions and separates comparison targets and policy conclusions. validation.json records local negative integrity controls; reproduction.json records separate-process byte equality. These are not CI, HermiT, SHACL or independent expert results.

## Next execution

N3b-3 reviews eleven D04/D08 registration/workflow concepts. Then D05 (11), D06/D11 (9), D09/D10 (5). After all 82 dispositions, qualify the complete successor curation and publish/read back the selected package before closing #85. Main, release v0.3.9, scientific source 0.3.2, reader 0.4.9 and article 7.2.21 are unchanged.
