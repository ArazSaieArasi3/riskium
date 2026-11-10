# N3b-1 — structural-context documentary review

Date: 2026-11-10. Planning target v0.3.10; #85 remains open.

**This batch is complete: 11 concepts. Current-source documentary coverage is 36/82 (43.9%); 46 remain.** This fraction is not overall research completion, semantic correctness or independent acceptance.

## What was reviewed

The selected current concept definitions, direct associations/generalizations, complete ancestry, changed ancestor records, changed association-neighbor records, applicable explicit set policy and analytical-case application policy were compared with the historical source. Primary source editions, locators and selected passages were checked separately. An unchanged edge does not hide the change in its endpoint's meaning.

| Concept | Disposition | Current-context interpretation |
|---|---|---|
| [Risk Pattern Specification](previews/RKM-C001.md) | RELATED | RX-002 links a continuing analytical case to its pattern; it does not identify the two. The inherited documentary identity and excluded blanket artifact set do not supply a Plan equivalence or register-approval condition. |
| [Risk Context Specification](previews/RKM-C002.md) | RELATED | R-35/RX-001 now refer to the explicitly analytical RiskCase. Missing task inputs concern readiness under a declared profile, not nonexistence or formal admission of that case. |
| [Risk Scenario Specification](previews/RKM-C003.md) | ANALOGY | R-36 separates a scenario from its analytical case and R-25 does not turn a specification into an actual occurrence. Inherited artifact identity remains documentary, without blanket sibling exclusion. |
| [Risk Nature Assertion](previews/RKM-C005.md) | RELATED | R-41/R-42/R-43 keep the claim about a case, selected nature value and context separate. The analytical case reading leaves nature objective-relative; the claim does not establish truth by classification. |
| [Nature Term](previews/RKM-C006.md) | RELATED | The path through ClassificationTerm and VocabularyConcept preserves InformationArtifact identity. The retained GS-RKM-C019/GS-RKM-C017 groups are non-disjoint and incomplete; their source labels remain carried, not independently validated here. |
| [Vocabulary Concept](previews/RKM-C017.md) | RELATED | G2-052 preserves documentary identity and the explicit GS-RKM-C017 policy does not make its listed subtypes exhaustive. Excluding the blanket artifact set leaves these subtype edges intact. |
| [Classification Scheme](previews/RKM-C018.md) | RELATED | GX-049 preserves artifact identity. R-05 records term membership under this profile; it is not a claim that the external scheme is closed or that the listed terms exhaust every possible member. |
| [Classification Term](previews/RKM-C019.md) | RELATED | G2-053/G2-052 preserve the inherited documentary identity. GS-RKM-C019 and GS-RKM-C017 remain explicitly non-disjoint and incomplete; no new covering, exclusivity or semantic-module claim is added. |
| [Classification Assertion](previews/RKM-C020.md) | RELATED | R-03 can classify an analytically identified RiskCase before organizational register admission. R-04/R-29 keep the selected term and documenting entry separate from the case and assertion. |
| [Tag](previews/RKM-C021.md) | RELATED | G2-054 preserves artifact identity and R-24 links the tag to an entry revision. Excluding blanket artifact sibling grouping neither merges tags with classification terms nor makes all document types exclusive. |
| [Risk Source Reference](previews/RKM-X06.md) | CONTRAST | G3-001 supplies documentary identity. RK3-001 concerns an analytical RiskCase; RK3-002 is the distinct source-resolution link and RK3-003 supplies context. No universal bearer category or operational-admission requirement is introduced. |

## Findings and limits

All eleven authored definitions and local edge records are unchanged. InformationArtifact has a revised typing rationale in every selected ancestor context. Six selected concepts have the revised RiskCase as a direct association neighbor. Current policy excludes the blanket artifact set while retaining subtype edges; the retained GS-RKM-C017/GS-RKM-C019 groups remain non-disjoint, incomplete and explicitly carried rather than independently reapproved.

Vocabulary resources, their labels, classification statements and their referents remain distinct in the adopted profile. SKOS does not automatically make a concept an OWL domain universal, but also permits dual typing; no global disjointness is imposed. Web Annotation classifying/tagging are motivation instances, not classes equivalent to Riskium assertions/tags. RiskScenarioSpecification remains distinct from its analytical case and actual occurrence. A RiskSourceReference remains distinct from a claimed contributor and does not establish causation.

The old model has no explicit generalization_set_policy field. This packet does not manufacture an old set policy from that absence. The current policy and published qualification are separate evidence routes. This is a documentary contextual review; no independent semantic approval of all retained set criteria is implied.

## Primary sources

- [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/) — W3C Recommendation, 30 April 2013; accessed 2026-11-10. Terms listed below only; no PROV conformance or import asserted.
- [Guide for Conducting Risk Assessments, NIST SP 800-30 Revision 1](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf) — September 2012; DOI 10.6028/NIST.SP.800-30r1; accessed 2026-11-10. Security-specific terms, selected glossary entries and tables only; not a universal enterprise-risk vocabulary. Glossary entries retain their original attributions.
- [Web Annotation Data Model](https://www.w3.org/TR/2017/REC-annotation-model-20170223/) — W3C Recommendation, 23 February 2017; accessed 2026-11-10. Selected motivations and annotation/body distinction only; no serialization conformance asserted.
- [SKOS Simple Knowledge Organization System Reference](https://www.w3.org/TR/2009/REC-skos-reference-20090818/) — W3C Recommendation, 18 August 2009; accessed 2026-11-10. Concept, scheme and lexical-label distinctions; no SKOS mapping triples asserted.

All four primary responses were retrieved directly and match their previously recorded hashes. source-access.json and passage-checks.json retain retrieval identities and inspected-location fingerprints without redistributing the source documents. The NIST glossary attribution is retained; its attributed original is not claimed independently reread.

## Verification and reproduction

From the repository root:

```sh
python -B evaluation/releases/v0.3.9/followups/issue85-structural-review/build.py --batch batch-01
python -B evaluation/releases/v0.3.9/followups/issue85-structural-review/build.py --batch batch-01 --check
```

The validator binds raw source/prior/allocation/passage/context files; recomputes the structural context; checks the declared population and disjoint cumulative coverage; preserves authored definitions and separates comparison targets and policy conclusions. validation.json records local negative integrity controls; reproduction.json records separate-process byte equality. These are not CI, HermiT, SHACL or independent expert results.

## Next execution

N3b-2 reviews ten D07 responsibility concepts. The remaining sequence is D04/D08 (11), D05 (11), D06/D11 (9), D09/D10 (5). progress.json records all exact remaining IDs. After all 82 dispositions, qualify the full successor curation component, then publish/read back the selected documentation package before closing #85. Main, release v0.3.9, historical curation 0.1.0, scientific source 0.3.2, reader 0.4.9 and article 7.2.21 are unchanged. #23 retains independent semantic review and #78 exact normative adoption.
