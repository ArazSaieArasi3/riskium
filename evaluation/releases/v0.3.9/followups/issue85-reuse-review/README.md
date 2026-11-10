# N3a — compatible reuse confirmed for 17 concepts

Date: 10 November 2026. Planning target v0.3.10; #85 remains open. **N3a is complete; full current curation is not yet complete.**

## Result and scope

All 17 reuse candidates have current-source documentary dispositions: eight CONTRAST, five RELATED and four ANALOGY. Fourteen disposition labels are retained; three scoped absence labels (C010/C013/C064) are clarified as explicit contrasts with the selected terms. No authored definition or scientific identity rule changes.

Together with N2, 25 of 82 current catalog concepts now have recorded current-source documentary dispositions (30.5% of this curation population). The remaining 57 are structural-context checks. This fraction is not overall research completion, semantic correctness or independent expert acceptance.

| Concept | Previous → current | Documentary decision |
|---|---|---|
| [Risk Occurrence](previews/RKM-C004.md) | CONTRAST → CONTRAST | Retain the actuality boundary. Riskium requires an actual occurrence supported in context; a source entry permitting a potential event does not establish realization. |
| [Risk Source](previews/RKM-C007.md) | ANALOGY → ANALOGY | Retain a bounded analogy. Riskium allows heterogeneous contextual contributors and opportunity perspectives; the security-specific source does not supply that whole cross-category profile. |
| [Predisposing Condition](previews/RKM-C008.md) | RELATED → RELATED | Retain the comparison with an explicit direction boundary. The authored Riskium situation increases susceptibility, whereas the inspected source allows likelihood changes in either direction. |
| [Trigger](previews/RKM-C009.md) | CONTRAST → CONTRAST | Retain the actuality and initiation boundary. A Riskium Trigger is actual and initiating in its context; the compared potential-event entry alone supplies neither commitment. |
| [Consequence](previews/RKM-C010.md) | NO_DIRECT_EQUIVALENT_REVIEWED → CONTRAST | Replace the scoped absence label with a positive comparison boundary: Riskium Consequence is an objective-relevant outcome referent, distinct from the compared potential event. No universal absence claim is made. |
| [Vulnerability](previews/RKM-C011.md) | RELATED → RELATED | Retain the security comparison and identify Mode separately as a modeling foundation. The current intrinsic-susceptibility interpretation requires a supported bearer; exactly-one characterization is distinct from a documentary weakness report. |
| [Exposure](previews/RKM-C012.md) | ANALOGY → ANALOGY | Retain the bounded exposure analogy. The authored Riskium referent is a time-qualified bearer/source situation; the inspected security discussion does not itself define that formal situation model. |
| [Risk State](previews/RKM-C013.md) | NO_DIRECT_EQUIVALENT_REVIEWED → CONTRAST | Replace the scoped absence label with a contrast. Riskium explicitly individuates a temporally qualified risk situation; generic entity description does not supply its state identity or a workflow interpretation. |
| [Information Content](previews/RKM-C016.md) | RELATED → RELATED | Retain conceptual-entity context without importing a content identity policy. Riskium keeps abstract meaning separate from artifacts and versions and requires its own explicit equivalence criteria. |
| [Entry Revision](previews/RKM-C023.md) | CONTRAST → CONTRAST | Retain the object/derivation distinction. Riskium EntryRevision is a version object with effective links; a qualified revision describes derivation rather than being that version or its creation activity. |
| [Assessment Activity](previews/RKM-C031.md) | CONTRAST → CONTRAST | Retain the activity/process scope distinction. A Riskium AssessmentActivity may contribute only one actual part of identification, analysis or evaluation; it is not automatically the complete security assessment process. |
| [Treatment Activity](previews/RKM-C044.md) | ANALOGY → ANALOGY | Retain the response analogy and separate actual treatment performance from its plan. Intended risk modification does not by itself establish observed effectiveness. |
| [Risk Control](previews/RKM-C045.md) | ANALOGY → ANALOGY | Retain the security-control analogy as one contextual use of Riskium RiskControl. The authored profile permits different bearer categories and separates implementation from effectiveness. |
| [Responsibility Relator](previews/RKM-C052.md) | RELATED → RELATED | Retain Relator as a modeling foundation rather than an external responsibility definition. Riskium adds grounding, temporal scope and responsibility semantics; its distinct-participant identity rule is additional to the C2 minimum-cardinality sum. |
| [Workflow Scheme Version](previews/RKM-C063.md) | CONTRAST → CONTRAST | Retain the comparison boundary. Riskium WorkflowSchemeVersion is an issued transition specification; concept-scheme aggregation or a revision qualification does not define its transitions or authorization rules. |
| [Workflow Assignment](previews/RKM-C064.md) | NO_DIRECT_EQUIVALENT_REVIEWED → CONTRAST | Replace the scoped absence label with a contrast. Riskium WorkflowAssignment is a timed record-state situation under a scheme version, rather than an activity-function description. |
| [Observation Activity](previews/RKM-C067.md) | RELATED → RELATED | Retain the procedure/feature/value observation comparison. Riskium keeps its stated subject, procedure and temporal context without automatically importing every source restriction. |

## Primary evidence and qualifications

- [Guide for Conducting Risk Assessments, NIST SP 800-30 Revision 1](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf) — September 2012; DOI 10.6028/NIST.SP.800-30r1; accessed 2026-11-10. Security-specific terms, selected glossary entries and tables only; not a universal enterprise-risk vocabulary. Glossary entries retain their original attributions.
- [OntoUML specification: Mode](https://ontouml.readthedocs.io/en/latest/classes/aspects/mode/index.html) — Unversioned latest documentation; response digest and current access date retained; accessed 2026-11-10. Definition and constraints C1-C2 only; direct HTTP succeeds in this execution. The older null hash/HTTP-403 record is retained in historical review 0.1.0.
- [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/) — W3C Recommendation, 30 April 2013; accessed 2026-11-10. Terms listed below only; no PROV conformance or import asserted.
- [OntoUML specification: Relator](https://ontouml.readthedocs.io/en/latest/classes/sortals/relator/index.html) — Unversioned latest documentation; response digest and current access date retained; accessed 2026-11-10. Definition and constraints C1-C2 only; this modeling construct is not the definition of a responsibility mandate.
- [SKOS Simple Knowledge Organization System Reference](https://www.w3.org/TR/2009/REC-skos-reference-20090818/) — W3C Recommendation, 18 August 2009; accessed 2026-11-10. Concept, scheme and lexical-label distinctions; no SKOS mapping triples asserted.
- [Semantic Sensor Network Ontology](https://www.w3.org/TR/2017/REC-vocab-ssn-20171019/) — W3C Recommendation, 19 October 2017; SOSA/SSN; accessed 2026-11-10. Selected core classes only; observed properties and their specifications remain distinct.

All six source responses were retrieved directly. Five prior non-null response hashes match exactly. The Mode source now also has a direct-response hash; the older failed-access/null-hash history remains intact. Selected PDF page/HTML anchor evidence is fingerprinted in passage-checks.json. It records inspected passages without redistributing the documents. Glossary attributions identify what SP 800-30 itself attributes; they do not claim that the attributed originals were independently reread.

Modeling foundations (Mode and Relator) are kept separate from domain comparisons. A relator cardinality-minimum sum alone does not establish distinct individuals. For Observation, the selected definition is used without importing displayed SOSA/SSN restrictions. NIST security-specific readings are not silently generalized to all ecosystem/enterprise risk.

## Verification

From the repository root:

```sh
python evaluation/releases/v0.3.9/followups/issue85-reuse-review/build.py
python evaluation/releases/v0.3.9/followups/issue85-reuse-review/build.py --check
```

The validator checks source/prior/impact/N2 bindings, all 17 unchanged concept/direct-neighborhood records, selected evidence routes, source attribution and the complete disjoint 8 + 17 + 57 population. Negative controls exercise documentary integrity, not ontology engines. validation.json records those checks; reproduction.json records a separate byte-identical rebuild. No CI or new HermiT/SHACL execution is claimed.

## Remaining finite batches

These are planned, not reviewed by N3a:

| Execution | Subdomains | Concepts |
|---|---|---|
| N3b-1 | D01, D03 | 11 |
| N3b-2 | D07 | 10 |
| N3b-3 | D04, D08 | 11 |
| N3b-4 | D05 | 11 |
| N3b-5 | D06, D11 | 9 |
| N3b-6 | D09, D10 | 5 |

Exact IDs are in remaining-batches.json. N3b-1 (D01/D03, 11 concepts) is next. After all 82 decisions, qualify the successor curation component, select the package, then publish/read back repository/Wiki/Pages. Close #85 only after its final gate. Main, published v0.3.9, reader 0.4.9, historical curation 0.1.0 and article 7.2.21 are unchanged by this planning packet. Exact normative adoption remains #78 and independent semantic review remains #23.
