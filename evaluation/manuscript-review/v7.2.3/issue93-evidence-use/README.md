# EvidenceItem dependency candidate

Status: **isolated candidate**, 2026-11-08. Related issue: [#93](https://github.com/ArazSaieArasi3/riskium/issues/93).

This packet implements and exercises the first of the three repairs identified in #93. It does not change `ontology/riskium-model.json`, the current native/OWL exports, the database schema, released readers, historical receipts or manuscript 7.2.21. The candidate is not a release and has not been promoted to the production model. The two mixed-criterion generalization sets remain open.

## Decision

Retain EvidenceItem (RKM-C066) as an anti-rigid documentary role with InformationArtifact identity. Add EvidenceUseRelator (RKM-C075) as the proposed foundation of a grounded, context-qualified evidential use. It mediates an EvidenceItem and a distinct EvidenceReferenceRole (RKM-C076). The latter inherits documentary identity through EvidenceReference; a reference record alone need not instantiate this participation role.

The relationship is a truthmaker for **participation in an evidential use**, not for the truth of the claim described by the reference. Support, challenge and context are distinct intended purposes. Instantiation requires a justified use-grounding record; a URL, citation or AI-generated interpretation alone is insufficient evidence that this relationship actually exists. The packet uses synthetic data to test the representation, not to attest real use episodes.

The selected representation preserves the idea that the same report can be evidence in one analysis and merely available information in another. Retyping EvidenceItem as a rigid Subkind would change that intended meaning. Merely changing RX-021 to mediation would confuse a documentary pointer with the relationship it describes. RX-021 is therefore retained unchanged as an ordinary association.

The extra reference participation role prevents a record of proposed use from being identified with the use relationship. Information-only records can remain InformationArtifact/EvidenceReference records; explicit instances of the candidate participation roles require their named use witnesses in the selected data profile. The candidate does not establish a new general organizational approval requirement.

## Semantic and data contract

| Concern | Candidate representation | Executable boundary |
|---|---|---|
| Documentary identity | EvidenceItem retains its existing InformationArtifact identity; EvidenceReferenceRole inherits it through EvidenceReference. | The original subtype links and pointer remain; one additional subtype link introduces the reference participation role. |
| Role dependence | RE-001 and RE-002 mediate the two documentary roles through EvidenceUseRelator; each role has a positive lower bound on incoming use relationships. | Native source inspection, OWL inverse cardinalities and explicit named-witness SHACL checks address different parts of this contract. |
| Relator participation | Each use has one evidence item and one distinct participating reference. | Native minimum participant counts, OWL property disjointness and SHACL endpoint disjointness are tested. Two different labels alone do not establish distinct individuals. |
| Grounding | RE-003 links the use to a grounding information record. | OWL requires a filler; SHACL requires a named, typed record. Its factual adequacy remains a semantic judgment. |
| Context and purpose | The selected data profile records a claim/analysis context and support, challenge or context as purpose. | SHACL checks the fields and their agreement with RX-021 and R-68. These coherence rules are not advertised as OWL property-chain axioms. |
| Continuing use identity | Different grounded episodes, contexts or purposes may involve the same artifact/reference pair. | The identity criterion is documented; comprehensive duplicate adjudication, temporal identity and database enforcement are not implemented here. |
| Non-endorsement | A grounded use does not establish that the described risk occurred or that the referenced claim is true. | A selected negative entailment test checks that the context is not inferred to be an actual RiskOccurrence. This is not a general theorem about all possible additions. |

Example: an analysis actually uses a laboratory report to challenge a medicine-quality statement. The report retains its documentary identity, while a grounded use links it to the participating reference, the quality statement, the intended purpose and the use record. A later analysis may use the same report as context without creating a new report identity.

Counterexample: a bibliography row containing a report URL can record potential relevance, but it does not by itself establish a grounded use, prove medicine failure or license an occurrence assertion. Incomplete import records stay informational until the selected profile is satisfied. Native RX-021 is a typed core relation: its OWL range can imply an EvidenceItem with anonymous existential fillers, so raw source pointers should not be asserted as accepted native relations without qualification. The explicit-data profile requires named witnesses separately.

## Actual checks

See [candidate-report.json](candidate-report.json) for results, input digests, engine versions and scope. The suite includes source/native-fidelity checks, the pinned OntoUML exchange schema, valid and invalid SHACL fixtures, shape-removal mutation controls, HermiT consistency/negative entailment tests and ROBOT's OWL 2 DL profile check.

The selected anti-pattern screen is rerun on the candidate. Both original GSRig sets remain visible. EvidenceUseRelator also triggers the repeatable-relator screen: repeatability is intentional when grounding, context or purpose distinguishes uses; duplicate descriptions of the same use must still resolve to one identity. This criterion is not a claim of complete instance-level identity enforcement. Topological relation-specialization candidates do not imply equivalent relation meanings. No full catalogue or independent semantic acceptance is claimed.

Open-world consistency can hold when explicit use or grounding records are absent because anonymous witnesses remain possible. The corresponding SHACL cases reject missing named records. These outcomes are complementary and are not pooled into a semantic-correctness percentage. HermiT 1.4.5.456 in this packet differs from the engine version in the historical manuscript receipts; its new counts must not replace their denominators.

## Replay

From the repository root, using Python 3.12 and Java 21:

```sh
python -m pip install rdflib==7.6.0 pyshacl==0.30.1 'jsonschema[format]==4.25.1'
curl -fL https://raw.githubusercontent.com/OntoUML/ontouml-schema/7a0fe7ef7d4caea8d62f2782fb3681261a75f452/dist/ontouml-schema.json -o /tmp/ontouml-schema.json
python evaluation/manuscript-review/v7.2.3/issue93-evidence-use/verify_candidate.py --schema /tmp/ontouml-schema.json --robot /path/to/robot-1.9.11.jar
```

ROBOT jar SHA-256: `53cd275c8e4c0dad1fc2c1c34174876795cd7d6b6926e1444adcbb0cb3c7ab26`. Schema SHA-256: `094324d8e6ac4505ef5ae983a45bb9b56a8b3b6960151c57736756a037344d38`.

The builder writes only this packet's candidate artifacts. The verification command writes its new receipts and generated reasoner inputs here. RDF blank-node serialization may change byte hashes on replay; the receipt always identifies the actual inputs of that run. Compare semantic graphs rather than treating a new serialization as a new scientific result.

## Sources and remaining work

The inspected [Role constraints C1/C2](https://ontouml.readthedocs.io/en/latest/classes/sortals/role/index.html), [Relator constraints](https://ontouml.readthedocs.io/en/latest/classes/sortals/relator/index.html) and [Mediation definition](https://ontouml.readthedocs.io/en/latest/relationships/mediation/index.html), accessed 2026-11-08, inform this candidate. They support the dependency and participation requirements, not the independent adequacy of this particular evidential-use interpretation.

Next, repair the InformationArtifact and Agent mixed-criterion sets while preserving valid subtype links, bearer-kind exclusivity and legitimate role overlap. Then review the combined candidate and its consequences for definitions, OWL/SHACL, database mappings and generated readers. Promotion, a stable release, real source-data migration and whole-model quality claims remain separate steps. The current paper continues to report the original pinned baseline and its disclosed limitations.
