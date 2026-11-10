# N2 — changed and new concept curation

Date: 10 November 2026. Planning target: v0.3.10; issue #85. **The eight-record N2 scope is complete. Full current curation and publication are pending.**

## Result

Selected primary passages were inspected for six changed concepts and two new concepts against model 0.3.2. Each authored definition is preserved verbatim, its complete concept record is hashed, and the prior review and N1 impact inventory are bound. These are assistant-supported documentary decisions, not independent expert ratings or formal alignment axioms.

| Concept | Previous → current documentary disposition | Decision |
|---|---|---|
| [Information Artifact](previews/RKM-C014.md) | RELATED → RELATED | Retain the documentary comparison. Riskium adds continuity across descriptions and issued versions; the revised typing rationale separates documentary institution from RiskCase approval. No universal admission rule follows. |
| [Artifact Version](previews/RKM-C015.md) | CONTRAST → CONTRAST | Retain the distinction: the issued version is the documentary object; Revision qualifies a derivation. First issue need not revise a predecessor. Issuance policy does not determine whether a RiskCase exists. |
| [Person](previews/RKM-C048.md) | RELATED → RELATED | Retain a human-agent comparison without adopting external identity or typing axioms. Riskium preserves the person identity owned by the external domain; participation and a responsibility mandate need separate evidence. |
| [Organization](previews/RKM-C049.md) | RELATED → RELATED | Retain an institutional-agent comparison. Capacity to carry responsibilities is distinct from a demonstrated mandate. Organization identity does not require local register approval of every analytical RiskCase. |
| [Evidence Item](previews/RKM-C066.md) | RELATED → RELATED | Retain the external comparison and separately document the role foundation. EvidenceItem inherits artifact identity; RE-001 makes participation depend on grounded use. It does not classify every artifact as evidence everywhere. |
| [Risk Case](previews/RKM-X01.md) | NO_DIRECT_EQUIVALENT_REVIEWED → CONTRAST | Replace the old scoped absence label with an explicit comparison boundary. RiskCase is the continuing analytical item for objectives and context, including threat or opportunity perspectives. A generic Entity comparison does not supply its continuity rule. Register admission remains a local application policy. This disposition makes no novelty or universal absence claim. |
| [Evidence Use Relator](previews/RKM-C075.md) | NEW → ANALOGY | Use an analogy to provenance usage while preserving the different participant structure. Riskium objectifies a grounded use linking a qualified reference and an evidence artifact, with context and purpose. RE-001 and RE-002 mediate the participants; RE-003 records grounding. OntoUML C2 supplies a minimum-count rule; distinct participants are an additional Riskium C-26 commitment, not a conclusion from that sum. |
| [Evidence Reference Role](previews/RKM-C076.md) | NEW → CONTRAST | Distinguish a function description from the documentary reference that participates in grounded use. GE-001 preserves reference identity through EvidenceReference and InformationArtifact; RE-002 supplies the role dependency. The reference can exist as a record of proposed use without this role membership. |

## Primary-source scope

- [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/) — W3C Recommendation, 30 April 2013; accessed 2026-11-10. Selected Entity, Person, Organization, Revision, Role, Usage and qualifiedUsage passages only; no import or PROV conformance asserted.
- [OntoUML specification: Relator](https://ontouml.readthedocs.io/en/latest/classes/sortals/relator/index.html) — Unversioned latest documentation; response body hash and access date retained; accessed 2026-11-10. Definition and constraints C1-C2 only; modeling foundation rather than an external definition of evidential use.
- [OntoUML specification: Role](https://ontouml.readthedocs.io/en/latest/classes/sortals/role/index.html) — Unversioned latest documentation; response body hash and access date retained; accessed 2026-11-10. Definition and constraints C1-C2 only; modeling foundation, not a domain definition.

Source response-body digests and sizes are in source-access.json; the packet does not redistribute the source documents. Selected term locators and short paraphrases are in review.json. A response digest binds the retrieved page, not every future edition or the truth of a proposed alignment.

## Important interpretation boundaries

- RiskCase remains an analytical item whose existence does not require organizational register acceptance. The revised disposition is a scoped contrast with a generic provenance entity, not an absence or superiority claim.
- Artifact versions and qualified revision relationships remain distinct. Contextual evidence roles do not follow from a citation alone.
- OntoUML relator C2 counts the sum of minimum multiplicities. The requirement for two distinct participants comes additionally from Riskium C-26; counting two ends alone does not prove distinctness.
- Carried source labels such as ISOLATED_CANDIDATE remain verbatim. The existing v0.3.9 publication/qualification receipt provides the later bounded execution context. These historical labels are not silently upgraded, and independent semantic acceptance is not inferred.
- Exact PRINCE2/ISACA/ISO clause adoption remains #78; no licensed normative full text is claimed inspected here. #23 remains independent. The 0.1.0 curation, scientific source, reader 0.4.9, released v0.3.9 and article 7.2.21 are unchanged.

## Verification

Run from the repository root:

```sh
python evaluation/releases/v0.3.9/followups/issue85-changed-review/build.py
python evaluation/releases/v0.3.9/followups/issue85-changed-review/build.py --check
```

The builder checks the exact eight-record population, source/definition/prior/impact/reader digests, selected locators, identity inheritance and mediation anchors, plus claim boundaries. Eight negative controls include a separately tampered rendered preview. These are documentary integrity controls; the examples in the previews are authored illustrations, not HermiT/SHACL runs. Rebuilding is deterministic. validation.json records the actual local controls and output digests; reproduction.json records the separate byte-equality check. No CI run is invented.

## Next finite steps

1. N3a: confirm the 17 reuse candidates with edition/locator and comparison-scope checks. N3b: recheck the 57 structural-context records in bounded subdomain batches. Only after those 74 decisions can the current 82-concept curation be called complete.
2. Qualify and select a complete successor curation component, retaining the historical review and its deferrals. Repair any status presentation through the documented source policy rather than editing frozen scientific bytes.
3. Publish the selected v0.3.10 documentation package and read back affected repository/Wiki/Pages bodies. Close #85 only after this endpoint. N2 preview pages do not count as deployed bodies.
