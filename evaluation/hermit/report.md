# Riskium HermiT reasoning report

This report is the execution receipt for the reviewed typed-core OWL mapping of conceptual model **0.3.1**, based on commit `d5d32cad96f47d008f9120333eb3ff68e61c4880`. The exact [premise RDF/XML](premise.rdf) and [machine-readable result](report.json) are retained beside this report. HermiT 1.3.8.1099 was supplied by owlready2==0.51 (jar SHA-256 `97e53f519720a0a2e328556e03b806aa239347c85e57637a935e6433ed2ad3a8`), running on openjdk version "17.0.20" 2026-07-21. The import closure is empty; the separately annotated external Object anchor is a local proxy.

## How the reasoning was run

`tools/run_hermit.py` parses the reviewed Turtle with RDFLib 7.6.0, writes RDF/XML for HermiT's OWLAPI loader, then runs the HermiT CLI against that exact premise. It checks baseline consistency and the unsatisfiable-class list; it asks for satisfiability of each typed class, entailment of each declared generalization, and entailment of each relation's declared domain, range and nontrivial qualified cardinality restrictions. Each conclusion explicitly declares the relevant OWL classes and object property; a bare RDF triple can otherwise be ignored by the OWLAPI loader. Additional negative and boundary fixtures test the oracle and selected forbidden inferences. Every process return code, output and elapsed time is in JSON.

Run from the repository root after installing pinned dependencies:

```sh
python3 -m venv .venv-hermit
.venv-hermit/bin/pip install -r tools/requirements-hermit.txt
.venv-hermit/bin/python tools/run_hermit.py
```

The source Turtle SHA-256 is `fdc19d96eb7536251384d05b088f9e3577050118b0633fb7b927bd25523f0064`; the exact RDF/XML premise SHA-256 is `d507966fe2528537c750024cb0fc11a2517794324d5275aaba95e0948241117a`. The contract SHA-256 is `4fefe152a982be4e41fe6f9ba92c3f7ed65af9e35250d58ebad6330acd7606b5`. The generated RDF/XML is semantically checked against the Turtle before execution; byte-for-byte serialized RDF/XML can vary with blank-node identifiers on a fresh regeneration, so the committed premise and its digest identify this run.

## Results and coverage

Baseline ontology consistency: **PASS**. Unsatisfiable-class inventory (none other than `owl:Nothing` expected): **PASS**. Across the **295 predeclared HermiT-related obligations**, **278 passed, 0 failed, and 17 remain without a sound HermiT oracle**. Execution coverage is **94.24% (278/295)**. Source allocation is **295/295 (100%)**; this differs from execution coverage. All **679 executed cases** passed in this run. These fractions are not percentages of ontological correctness.

| Family | Passed / total | Interpretation |
| --- | ---: | --- |
| Class satisfiability | 77 / 77 | Named classes can have an instance in some model. |
| Declared subclass entailment | 66 / 66 | Mapped specialization axioms are entailed. |
| Relation mapping | 127 / 127 | Declared domain/range and nontrivial cardinality axioms are entailed. |
| Constraint encoding disposition | 8 / 25 | Only a bounded, separately listed subset has a HermiT oracle. |

The 127 relation results confirm entailment of mapped axioms, including 88 nontrivial qualified restrictions across 254 ordered ends. They do **not** establish closed-world completeness or distinctness of named fillers. The 25 constraint obligations are listed individually below, including those whose full meaning is not encoded in OWL. Treating a reasoner-inapplicable portion as a pass would inflate coverage.

Supplemental semantic controls go beyond rechecking asserted axioms. They infer general types from specific instances, infer endpoint types from actual property assertions, challenge reverse inheritance, and test every maximum-one relation end with one filler and then two explicitly different fillers. These tests are **additional cases**, not extra baseline obligations. Their results are:

| Supplemental family | Passed / total |
| --- | ---: |
| Boundary mutation | 3 / 3 |
| Cardinality boundary | 130 / 130 |
| Inferred relation typing | 127 / 127 |
| Inferred subclass membership | 66 / 66 |
| Negative control | 2 / 2 |
| Open-world boundary | 3 / 3 |
| Reverse hierarchy control | 66 / 66 |


### Negative, boundary and mutation controls

| Case | Expected | Observed | Purpose |
| --- | --- | --- | --- |
| `H-CONTROL-WRONG-RANGE` | false | `false`; PASS | Unjustified R-01 range |
| `H-CONTROL-REVERSE-G01` | false | `false`; PASS | Reversed subclass entailment |
| `H-DISJOINT-GS-RKM-C053` | false | `INCONSISTENT`; PASS | Shared individual in disjoint siblings |
| `H-DISJOINT-GS-RKM-C054` | false | `INCONSISTENT`; PASS | Shared individual in disjoint siblings |
| `H-DISJOINT-GS-AgentKinds` | false | `INCONSISTENT`; PASS | Shared individual in disjoint siblings |
| `H-C15-TWO-DISTINCT-BEARERS` | false | `INCONSISTENT`; PASS | At-most-one bearer with two named distinct objects |
| `H-C-01-IDENTITY-COUNTERMODEL` | true | `http://www.w3.org/2002/07/owl#Thing is satisfiable.`; PASS | Two named instances may remain distinct |
| `H-C-24-IDENTITY-COUNTERMODEL` | true | `http://www.w3.org/2002/07/owl#Thing is satisfiable.`; PASS | Two named instances may remain distinct |
| `H-C02-NO-REALIZATION` | false | `false`; PASS | Description alone does not entail occurrence |
| `H-C07-NO-AUTHORITY` | false | `false`; PASS | Responsibility alone does not entail authorization |
| `H-C23-NO-REVERSE-CONTEXT` | false | `false`; PASS | hasContext alone does not entail analyzedInContext |
| `H-C23-ANALYZED-IMPLIES-CONTEXT` | true | `true`; PASS | Source-backed same-pair property inclusion |
| `H-C24-REVISION-IMPLIES-VERSION` | true | `true`; PASS | Source-backed revision/version property inclusion |
| `H-C20-NO-CASE-ENTRY-EQUIVALENCE` | false | `false`; PASS | RiskCase is not globally a RiskRegisterEntry |
| `H-C22-NO-PARTICIPANT-PAIR-KEY` | true | `http://www.w3.org/2002/07/owl#Thing is satisfiable.`; PASS | Two distinct mandates can share mediated participants |

### Constraint obligation register

| Obligation | Constraint | Outcome | Evidence or remaining reason |
| --- | --- | --- | --- |
| `HERMIT-0605` | C-01 | PASS | H-C-01-IDENTITY-COUNTERMODEL |
| `HERMIT-0607` | C-02 | PASS | H-C02-NO-REALIZATION |
| `HERMIT-0609` | C-03 | NOT_RUN | Current OWL route: Not applicable to change prevention: monotonic axioms do not enforce immutability across transactions. Remaining route: Partial: check version links and required snapshot references within one graph. Application history test: change an issued payload, reject overwrite and create a new version with lineage. |
| `HERMIT-0611` | C-04 | NOT_RUN | Current OWL route: Partial: map result types and reference links without reducing risk to a number. Remaining route: Partial: task-ready shapes require task-specific pinned method, scale, dimension, basis and time. Review measurement interpretation and qualitative likelihood; scalar fields still need an approved schema. |
| `HERMIT-0613` | C-05 | NOT_RUN | Current OWL route: Partial: test that administrative state does not entail cessation or effectiveness. Remaining route: Partial: check distinct temporal fields and interval ordering after the datatype schema is approved. Application and semantic review define time zones, unknown endpoints and cessation evidence. |
| `HERMIT-0615` | C-06 | NOT_RUN | Current OWL route: Partial: reviewed mediation axioms can require distinct participants; missing named witnesses are not an OWL inconsistency. Remaining route: Planned: SHACL-SPARQL checks resolved participant distinctness using an explicit identity-normalization policy. Resolve alias/sameAs identity before counting actors; do not manufacture authority or a second actor. |
| `HERMIT-0617` | C-07 | PASS | H-C07-NO-AUTHORITY |
| `HERMIT-0619` | C-08 | NOT_RUN | Current OWL route: Partial: an anchor disjunction may be encoded after review; missing explicit data remains an open-world issue. Remaining route: Planned: Core sh:or for indicator or scale, plus SPARQL compatibility checks after unit/scale schema review. Review qualitative scale semantics and any governed conversion. |
| `HERMIT-0621` | C-09 | NOT_RUN | Current OWL route: Partial: an existential aboutness disjunction may be mapped, but publication completeness is a graph policy. Remaining route: Planned: Core alternativePath over describesCase, describesPattern and expressesScenario with minCount 1. Select the published-description profile and document multiple-target interpretation. |
| `HERMIT-0623` | C-10 | NOT_RUN | Current OWL route: Partial: preserve separate statement resources without asserting a global equivalence of tolerance meanings. Remaining route: Partial: require source framework/version and context once provenance properties are approved. Review source-specific meanings and inspected source portions. |
| `HERMIT-0625` | C-11 | NOT_RUN | Current OWL route: Partial: vocabulary individuals are not generated as OWL classes or equality axioms from labels. Remaining route: Planned: scheme membership, resource identity and label-data validation using an approved vocabulary profile. Review scheme identifiers and legitimate cross-scheme mappings. |
| `HERMIT-0627` | C-12 | NOT_RUN | Current OWL route: Partial: evidential links alone must not entail truth or endorsement of the target claim. Remaining route: Partial: require support/challenge/context qualification and source locators after the assertion schema is reviewed. Review evidential adequacy independently of presence or graph conformance. |
| `HERMIT-0629` | C-13 | NOT_RUN | Current OWL route: Partial: typed relationships can be represented; arbitrary joins across scale/version/dimension are not assumed expressible. Remaining route: Planned: SPARQL checks selected level, scale version and dimension against pinned interpretation. Review unit conversion, dimensions and missing-version policy. |
| `HERMIT-0631` | C-14 | NOT_RUN | Current OWL route: Planned: reject typed-core declarations for the three excluded catalog boundaries in the export. Remaining route: Planned: boundary-admission checks reject using those catalog notions as managed core classes. Record optional external bridges separately; adding an external ontology requires a new ownership decision. |
| `HERMIT-0633` | C-15 | PASS | H-C15-TWO-DISTINCT-BEARERS |
| `HERMIT-0635` | C-16 | NOT_RUN | Current OWL route: Not applicable to explicit-data completeness: OWL inference is not a record-admission decision. Remaining route: Planned: separate raw, managed and task-ready shapes; never run a managed requirement as raw rejection. Approve required identity, title and provenance properties and task-specific input sets. |
| `HERMIT-0637` | C-17 | NOT_RUN | Current OWL route: Partial: multiple assertions must remain consistent without unsupported functional properties or identity keys. Remaining route: Partial: check qualified assertion context, time and provenance after schema review. Application export test: multiple applicable values require a declared scalar selection rule. |
| `HERMIT-0639` | C-18 | NOT_RUN | Current OWL route: Partial: test absence of comparability entailments from equal numbers or labels. Remaining route: Planned: SPARQL task-readiness joins over pinned method, scale, dimension, basis and temporal context. Application calculation/comparison tests cover governed transformations and missing values. |
| `HERMIT-0641` | C-19 | NOT_RUN | Current OWL route: Partial: scheme-qualified workflow state does not entail actual risk cessation or effectiveness. Remaining route: Partial: validate scheme/version references and source-backed transition-rule records. Application transition tests enforce authority; absent rules yield UNKNOWN, not automatic permission. |
| `HERMIT-0643` | C-20 | PASS | H-C20-NO-CASE-ENTRY-EQUIVALENCE |
| `HERMIT-0645` | C-21 | NOT_RUN | Current OWL route: Partial: represent result and input relationships without treating a missing triple as proof of inconsistency. Remaining route: Planned: conditional reported/computed shapes require derivedFrom, pinned method and adequate inputs for computed results. Application tests rerun the formula; score-kind and formula/input scalar schema still need review. |
| `HERMIT-0647` | C-22 | PASS | H-C22-NO-PARTICIPANT-PAIR-KEY |
| `HERMIT-0649` | C-23 | PASS | H-C23-NO-REVERSE-CONTEXT, H-C23-ANALYZED-IMPLIES-CONTEXT |
| `HERMIT-0651` | C-24 | PASS | H-C-24-IDENTITY-COUNTERMODEL, H-C24-REVISION-IMPLIES-VERSION |
| `HERMIT-0653` | C-25 | NOT_RUN | Current OWL route: Partial: reviewed qualified version target restrictions may be encoded; arbitrary artifact/version joins remain explicit-data checks. Remaining route: Planned: SPARQL checks context/method/scale/criteria versionOf target type and agreement with artifact references. Pin which artifact-level references exist and which are optional before admitting data. |

### Full 295-row baseline register

| ID | Family | Source | Outcome | Case |
| --- | --- | --- | --- | --- |
| `HERMIT-0001` | Class satisfiability | `RKM-C001` | PASS | `HERMIT-0001` |
| `HERMIT-0002` | Class satisfiability | `RKM-C002` | PASS | `HERMIT-0002` |
| `HERMIT-0003` | Class satisfiability | `RKM-C003` | PASS | `HERMIT-0003` |
| `HERMIT-0004` | Class satisfiability | `RKM-C004` | PASS | `HERMIT-0004` |
| `HERMIT-0005` | Class satisfiability | `RKM-C005` | PASS | `HERMIT-0005` |
| `HERMIT-0006` | Class satisfiability | `RKM-C006` | PASS | `HERMIT-0006` |
| `HERMIT-0007` | Class satisfiability | `RKM-C008` | PASS | `HERMIT-0007` |
| `HERMIT-0008` | Class satisfiability | `RKM-C009` | PASS | `HERMIT-0008` |
| `HERMIT-0009` | Class satisfiability | `RKM-C011` | PASS | `HERMIT-0009` |
| `HERMIT-0010` | Class satisfiability | `RKM-C012` | PASS | `HERMIT-0010` |
| `HERMIT-0011` | Class satisfiability | `RKM-C013` | PASS | `HERMIT-0011` |
| `HERMIT-0012` | Class satisfiability | `RKM-C014` | PASS | `HERMIT-0012` |
| `HERMIT-0013` | Class satisfiability | `RKM-C015` | PASS | `HERMIT-0013` |
| `HERMIT-0014` | Class satisfiability | `RKM-C016` | PASS | `HERMIT-0014` |
| `HERMIT-0015` | Class satisfiability | `RKM-C017` | PASS | `HERMIT-0015` |
| `HERMIT-0016` | Class satisfiability | `RKM-C018` | PASS | `HERMIT-0016` |
| `HERMIT-0017` | Class satisfiability | `RKM-C019` | PASS | `HERMIT-0017` |
| `HERMIT-0018` | Class satisfiability | `RKM-C020` | PASS | `HERMIT-0018` |
| `HERMIT-0019` | Class satisfiability | `RKM-C021` | PASS | `HERMIT-0019` |
| `HERMIT-0020` | Class satisfiability | `RKM-C022` | PASS | `HERMIT-0020` |
| `HERMIT-0021` | Class satisfiability | `RKM-C023` | PASS | `HERMIT-0021` |
| `HERMIT-0022` | Class satisfiability | `RKM-C024` | PASS | `HERMIT-0022` |
| `HERMIT-0023` | Class satisfiability | `RKM-C025` | PASS | `HERMIT-0023` |
| `HERMIT-0024` | Class satisfiability | `RKM-C026` | PASS | `HERMIT-0024` |
| `HERMIT-0025` | Class satisfiability | `RKM-C027` | PASS | `HERMIT-0025` |
| `HERMIT-0026` | Class satisfiability | `RKM-C028` | PASS | `HERMIT-0026` |
| `HERMIT-0027` | Class satisfiability | `RKM-C029` | PASS | `HERMIT-0027` |
| `HERMIT-0028` | Class satisfiability | `RKM-C030` | PASS | `HERMIT-0028` |
| `HERMIT-0029` | Class satisfiability | `RKM-C031` | PASS | `HERMIT-0029` |
| `HERMIT-0030` | Class satisfiability | `RKM-C032` | PASS | `HERMIT-0030` |
| `HERMIT-0031` | Class satisfiability | `RKM-C033` | PASS | `HERMIT-0031` |
| `HERMIT-0032` | Class satisfiability | `RKM-C034` | PASS | `HERMIT-0032` |
| `HERMIT-0033` | Class satisfiability | `RKM-C035` | PASS | `HERMIT-0033` |
| `HERMIT-0034` | Class satisfiability | `RKM-C036` | PASS | `HERMIT-0034` |
| `HERMIT-0035` | Class satisfiability | `RKM-C037` | PASS | `HERMIT-0035` |
| `HERMIT-0036` | Class satisfiability | `RKM-C038` | PASS | `HERMIT-0036` |
| `HERMIT-0037` | Class satisfiability | `RKM-C039` | PASS | `HERMIT-0037` |
| `HERMIT-0038` | Class satisfiability | `RKM-C040` | PASS | `HERMIT-0038` |
| `HERMIT-0039` | Class satisfiability | `RKM-C041` | PASS | `HERMIT-0039` |
| `HERMIT-0040` | Class satisfiability | `RKM-C042` | PASS | `HERMIT-0040` |
| `HERMIT-0041` | Class satisfiability | `RKM-C043` | PASS | `HERMIT-0041` |
| `HERMIT-0042` | Class satisfiability | `RKM-C044` | PASS | `HERMIT-0042` |
| `HERMIT-0043` | Class satisfiability | `RKM-C046` | PASS | `HERMIT-0043` |
| `HERMIT-0044` | Class satisfiability | `RKM-C047` | PASS | `HERMIT-0044` |
| `HERMIT-0045` | Class satisfiability | `RKM-C048` | PASS | `HERMIT-0045` |
| `HERMIT-0046` | Class satisfiability | `RKM-C049` | PASS | `HERMIT-0046` |
| `HERMIT-0047` | Class satisfiability | `RKM-C050` | PASS | `HERMIT-0047` |
| `HERMIT-0048` | Class satisfiability | `RKM-C051` | PASS | `HERMIT-0048` |
| `HERMIT-0049` | Class satisfiability | `RKM-C052` | PASS | `HERMIT-0049` |
| `HERMIT-0050` | Class satisfiability | `RKM-C053` | PASS | `HERMIT-0050` |
| `HERMIT-0051` | Class satisfiability | `RKM-C054` | PASS | `HERMIT-0051` |
| `HERMIT-0052` | Class satisfiability | `RKM-C055` | PASS | `HERMIT-0052` |
| `HERMIT-0053` | Class satisfiability | `RKM-C056` | PASS | `HERMIT-0053` |
| `HERMIT-0054` | Class satisfiability | `RKM-C057` | PASS | `HERMIT-0054` |
| `HERMIT-0055` | Class satisfiability | `RKM-C058` | PASS | `HERMIT-0055` |
| `HERMIT-0056` | Class satisfiability | `RKM-C059` | PASS | `HERMIT-0056` |
| `HERMIT-0057` | Class satisfiability | `RKM-C060` | PASS | `HERMIT-0057` |
| `HERMIT-0058` | Class satisfiability | `RKM-C061` | PASS | `HERMIT-0058` |
| `HERMIT-0059` | Class satisfiability | `RKM-C062` | PASS | `HERMIT-0059` |
| `HERMIT-0060` | Class satisfiability | `RKM-C063` | PASS | `HERMIT-0060` |
| `HERMIT-0061` | Class satisfiability | `RKM-C064` | PASS | `HERMIT-0061` |
| `HERMIT-0062` | Class satisfiability | `RKM-C065` | PASS | `HERMIT-0062` |
| `HERMIT-0063` | Class satisfiability | `RKM-C066` | PASS | `HERMIT-0063` |
| `HERMIT-0064` | Class satisfiability | `RKM-C067` | PASS | `HERMIT-0064` |
| `HERMIT-0065` | Class satisfiability | `RKM-C068` | PASS | `HERMIT-0065` |
| `HERMIT-0066` | Class satisfiability | `RKM-C069` | PASS | `HERMIT-0066` |
| `HERMIT-0067` | Class satisfiability | `RKM-C070` | PASS | `HERMIT-0067` |
| `HERMIT-0068` | Class satisfiability | `RKM-C071` | PASS | `HERMIT-0068` |
| `HERMIT-0069` | Class satisfiability | `RKM-C072` | PASS | `HERMIT-0069` |
| `HERMIT-0070` | Class satisfiability | `RKM-C073` | PASS | `HERMIT-0070` |
| `HERMIT-0071` | Class satisfiability | `RKM-C074` | PASS | `HERMIT-0071` |
| `HERMIT-0072` | Class satisfiability | `RKM-X01` | PASS | `HERMIT-0072` |
| `HERMIT-0073` | Class satisfiability | `RKM-X02` | PASS | `HERMIT-0073` |
| `HERMIT-0074` | Class satisfiability | `RKM-X03` | PASS | `HERMIT-0074` |
| `HERMIT-0075` | Class satisfiability | `RKM-X04` | PASS | `HERMIT-0075` |
| `HERMIT-0076` | Class satisfiability | `RKM-X05` | PASS | `HERMIT-0076` |
| `HERMIT-0077` | Class satisfiability | `RKM-X06` | PASS | `HERMIT-0077` |
| `HERMIT-0078` | Declared subclass entailment | `G-01` | PASS | `HERMIT-0078` |
| `HERMIT-0079` | Declared subclass entailment | `G-02` | PASS | `HERMIT-0079` |
| `HERMIT-0080` | Declared subclass entailment | `G-03` | PASS | `HERMIT-0080` |
| `HERMIT-0081` | Declared subclass entailment | `G-04` | PASS | `HERMIT-0081` |
| `HERMIT-0082` | Declared subclass entailment | `G-05` | PASS | `HERMIT-0082` |
| `HERMIT-0083` | Declared subclass entailment | `G-06` | PASS | `HERMIT-0083` |
| `HERMIT-0084` | Declared subclass entailment | `G-07` | PASS | `HERMIT-0084` |
| `HERMIT-0085` | Declared subclass entailment | `G-08` | PASS | `HERMIT-0085` |
| `HERMIT-0086` | Declared subclass entailment | `G-09` | PASS | `HERMIT-0086` |
| `HERMIT-0087` | Declared subclass entailment | `G-10` | PASS | `HERMIT-0087` |
| `HERMIT-0088` | Declared subclass entailment | `G-11` | PASS | `HERMIT-0088` |
| `HERMIT-0089` | Declared subclass entailment | `G-12` | PASS | `HERMIT-0089` |
| `HERMIT-0090` | Declared subclass entailment | `G-13` | PASS | `HERMIT-0090` |
| `HERMIT-0091` | Declared subclass entailment | `G-14` | PASS | `HERMIT-0091` |
| `HERMIT-0092` | Declared subclass entailment | `G-15` | PASS | `HERMIT-0092` |
| `HERMIT-0093` | Declared subclass entailment | `G-16` | PASS | `HERMIT-0093` |
| `HERMIT-0094` | Declared subclass entailment | `G-17` | PASS | `HERMIT-0094` |
| `HERMIT-0095` | Declared subclass entailment | `G-18` | PASS | `HERMIT-0095` |
| `HERMIT-0096` | Declared subclass entailment | `G-19` | PASS | `HERMIT-0096` |
| `HERMIT-0097` | Declared subclass entailment | `G-20` | PASS | `HERMIT-0097` |
| `HERMIT-0098` | Declared subclass entailment | `G-21` | PASS | `HERMIT-0098` |
| `HERMIT-0099` | Declared subclass entailment | `G-22` | PASS | `HERMIT-0099` |
| `HERMIT-0100` | Declared subclass entailment | `G-23` | PASS | `HERMIT-0100` |
| `HERMIT-0101` | Declared subclass entailment | `G-24` | PASS | `HERMIT-0101` |
| `HERMIT-0102` | Declared subclass entailment | `G-25` | PASS | `HERMIT-0102` |
| `HERMIT-0103` | Declared subclass entailment | `G-26` | PASS | `HERMIT-0103` |
| `HERMIT-0104` | Declared subclass entailment | `G-27` | PASS | `HERMIT-0104` |
| `HERMIT-0105` | Declared subclass entailment | `G-28` | PASS | `HERMIT-0105` |
| `HERMIT-0106` | Declared subclass entailment | `G-29` | PASS | `HERMIT-0106` |
| `HERMIT-0107` | Declared subclass entailment | `G-30` | PASS | `HERMIT-0107` |
| `HERMIT-0108` | Declared subclass entailment | `G-31` | PASS | `HERMIT-0108` |
| `HERMIT-0109` | Declared subclass entailment | `GX-046` | PASS | `HERMIT-0109` |
| `HERMIT-0110` | Declared subclass entailment | `GX-047` | PASS | `HERMIT-0110` |
| `HERMIT-0111` | Declared subclass entailment | `GX-048` | PASS | `HERMIT-0111` |
| `HERMIT-0112` | Declared subclass entailment | `GX-049` | PASS | `HERMIT-0112` |
| `HERMIT-0113` | Declared subclass entailment | `GX-050` | PASS | `HERMIT-0113` |
| `HERMIT-0114` | Declared subclass entailment | `GX-051` | PASS | `HERMIT-0114` |
| `HERMIT-0115` | Declared subclass entailment | `GX-053` | PASS | `HERMIT-0115` |
| `HERMIT-0116` | Declared subclass entailment | `GX-054` | PASS | `HERMIT-0116` |
| `HERMIT-0117` | Declared subclass entailment | `GX-055` | PASS | `HERMIT-0117` |
| `HERMIT-0118` | Declared subclass entailment | `GX-056` | PASS | `HERMIT-0118` |
| `HERMIT-0119` | Declared subclass entailment | `GX-057` | PASS | `HERMIT-0119` |
| `HERMIT-0120` | Declared subclass entailment | `GX-058` | PASS | `HERMIT-0120` |
| `HERMIT-0121` | Declared subclass entailment | `GX-059` | PASS | `HERMIT-0121` |
| `HERMIT-0122` | Declared subclass entailment | `GX-060` | PASS | `HERMIT-0122` |
| `HERMIT-0123` | Declared subclass entailment | `GX-061` | PASS | `HERMIT-0123` |
| `HERMIT-0124` | Declared subclass entailment | `GX-062` | PASS | `HERMIT-0124` |
| `HERMIT-0125` | Declared subclass entailment | `GX-063` | PASS | `HERMIT-0125` |
| `HERMIT-0126` | Declared subclass entailment | `GX-064` | PASS | `HERMIT-0126` |
| `HERMIT-0127` | Declared subclass entailment | `G2-050` | PASS | `HERMIT-0127` |
| `HERMIT-0128` | Declared subclass entailment | `G2-051` | PASS | `HERMIT-0128` |
| `HERMIT-0129` | Declared subclass entailment | `G2-052` | PASS | `HERMIT-0129` |
| `HERMIT-0130` | Declared subclass entailment | `G2-053` | PASS | `HERMIT-0130` |
| `HERMIT-0131` | Declared subclass entailment | `G2-054` | PASS | `HERMIT-0131` |
| `HERMIT-0132` | Declared subclass entailment | `G2-055` | PASS | `HERMIT-0132` |
| `HERMIT-0133` | Declared subclass entailment | `G2-056` | PASS | `HERMIT-0133` |
| `HERMIT-0134` | Declared subclass entailment | `G2-057` | PASS | `HERMIT-0134` |
| `HERMIT-0135` | Declared subclass entailment | `G2-058` | PASS | `HERMIT-0135` |
| `HERMIT-0136` | Declared subclass entailment | `G2-059` | PASS | `HERMIT-0136` |
| `HERMIT-0137` | Declared subclass entailment | `G2-060` | PASS | `HERMIT-0137` |
| `HERMIT-0138` | Declared subclass entailment | `G2-061` | PASS | `HERMIT-0138` |
| `HERMIT-0139` | Declared subclass entailment | `G2-062` | PASS | `HERMIT-0139` |
| `HERMIT-0140` | Declared subclass entailment | `G2-063` | PASS | `HERMIT-0140` |
| `HERMIT-0141` | Declared subclass entailment | `G2-064` | PASS | `HERMIT-0141` |
| `HERMIT-0142` | Declared subclass entailment | `G2-065` | PASS | `HERMIT-0142` |
| `HERMIT-0143` | Declared subclass entailment | `G3-001` | PASS | `HERMIT-0143` |
| `HERMIT-0144` | Relation mapping | `R-01` | PASS | `HERMIT-0144` |
| `HERMIT-0147` | Relation mapping | `R-02` | PASS | `HERMIT-0147` |
| `HERMIT-0150` | Relation mapping | `R-03` | PASS | `HERMIT-0150` |
| `HERMIT-0153` | Relation mapping | `R-04` | PASS | `HERMIT-0153` |
| `HERMIT-0156` | Relation mapping | `R-05` | PASS | `HERMIT-0156` |
| `HERMIT-0159` | Relation mapping | `R-06` | PASS | `HERMIT-0159` |
| `HERMIT-0162` | Relation mapping | `R-07` | PASS | `HERMIT-0162` |
| `HERMIT-0165` | Relation mapping | `R-08` | PASS | `HERMIT-0165` |
| `HERMIT-0168` | Relation mapping | `R-09` | PASS | `HERMIT-0168` |
| `HERMIT-0171` | Relation mapping | `R-10` | PASS | `HERMIT-0171` |
| `HERMIT-0174` | Relation mapping | `R-11` | PASS | `HERMIT-0174` |
| `HERMIT-0177` | Relation mapping | `R-12` | PASS | `HERMIT-0177` |
| `HERMIT-0180` | Relation mapping | `R-13` | PASS | `HERMIT-0180` |
| `HERMIT-0183` | Relation mapping | `R-14` | PASS | `HERMIT-0183` |
| `HERMIT-0186` | Relation mapping | `R-15` | PASS | `HERMIT-0186` |
| `HERMIT-0189` | Relation mapping | `R-16` | PASS | `HERMIT-0189` |
| `HERMIT-0192` | Relation mapping | `R-17` | PASS | `HERMIT-0192` |
| `HERMIT-0195` | Relation mapping | `R-18` | PASS | `HERMIT-0195` |
| `HERMIT-0198` | Relation mapping | `R-19` | PASS | `HERMIT-0198` |
| `HERMIT-0201` | Relation mapping | `R-20` | PASS | `HERMIT-0201` |
| `HERMIT-0204` | Relation mapping | `R-21` | PASS | `HERMIT-0204` |
| `HERMIT-0207` | Relation mapping | `R-22` | PASS | `HERMIT-0207` |
| `HERMIT-0210` | Relation mapping | `R-23` | PASS | `HERMIT-0210` |
| `HERMIT-0213` | Relation mapping | `R-24` | PASS | `HERMIT-0213` |
| `HERMIT-0216` | Relation mapping | `R-25` | PASS | `HERMIT-0216` |
| `HERMIT-0219` | Relation mapping | `R-26` | PASS | `HERMIT-0219` |
| `HERMIT-0222` | Relation mapping | `R-27` | PASS | `HERMIT-0222` |
| `HERMIT-0225` | Relation mapping | `R-28` | PASS | `HERMIT-0225` |
| `HERMIT-0228` | Relation mapping | `R-29` | PASS | `HERMIT-0228` |
| `HERMIT-0231` | Relation mapping | `R-30` | PASS | `HERMIT-0231` |
| `HERMIT-0234` | Relation mapping | `R-31` | PASS | `HERMIT-0234` |
| `HERMIT-0237` | Relation mapping | `R-32` | PASS | `HERMIT-0237` |
| `HERMIT-0240` | Relation mapping | `R-33` | PASS | `HERMIT-0240` |
| `HERMIT-0243` | Relation mapping | `R-34` | PASS | `HERMIT-0243` |
| `HERMIT-0246` | Relation mapping | `R-35` | PASS | `HERMIT-0246` |
| `HERMIT-0249` | Relation mapping | `R-36` | PASS | `HERMIT-0249` |
| `HERMIT-0252` | Relation mapping | `R-37` | PASS | `HERMIT-0252` |
| `HERMIT-0255` | Relation mapping | `R-38` | PASS | `HERMIT-0255` |
| `HERMIT-0258` | Relation mapping | `R-39` | PASS | `HERMIT-0258` |
| `HERMIT-0261` | Relation mapping | `R-40` | PASS | `HERMIT-0261` |
| `HERMIT-0264` | Relation mapping | `R-41` | PASS | `HERMIT-0264` |
| `HERMIT-0267` | Relation mapping | `R-42` | PASS | `HERMIT-0267` |
| `HERMIT-0270` | Relation mapping | `R-43` | PASS | `HERMIT-0270` |
| `HERMIT-0273` | Relation mapping | `R-44` | PASS | `HERMIT-0273` |
| `HERMIT-0276` | Relation mapping | `R-45` | PASS | `HERMIT-0276` |
| `HERMIT-0279` | Relation mapping | `R-46` | PASS | `HERMIT-0279` |
| `HERMIT-0282` | Relation mapping | `R-47` | PASS | `HERMIT-0282` |
| `HERMIT-0285` | Relation mapping | `R-48` | PASS | `HERMIT-0285` |
| `HERMIT-0288` | Relation mapping | `R-49` | PASS | `HERMIT-0288` |
| `HERMIT-0291` | Relation mapping | `R-50` | PASS | `HERMIT-0291` |
| `HERMIT-0294` | Relation mapping | `R-51` | PASS | `HERMIT-0294` |
| `HERMIT-0297` | Relation mapping | `R-52` | PASS | `HERMIT-0297` |
| `HERMIT-0300` | Relation mapping | `R-53` | PASS | `HERMIT-0300` |
| `HERMIT-0303` | Relation mapping | `R-54` | PASS | `HERMIT-0303` |
| `HERMIT-0306` | Relation mapping | `R-55` | PASS | `HERMIT-0306` |
| `HERMIT-0309` | Relation mapping | `R-56` | PASS | `HERMIT-0309` |
| `HERMIT-0312` | Relation mapping | `R-57` | PASS | `HERMIT-0312` |
| `HERMIT-0315` | Relation mapping | `R-58` | PASS | `HERMIT-0315` |
| `HERMIT-0318` | Relation mapping | `R-59` | PASS | `HERMIT-0318` |
| `HERMIT-0321` | Relation mapping | `R-60` | PASS | `HERMIT-0321` |
| `HERMIT-0324` | Relation mapping | `R-61` | PASS | `HERMIT-0324` |
| `HERMIT-0327` | Relation mapping | `R-62` | PASS | `HERMIT-0327` |
| `HERMIT-0330` | Relation mapping | `R-63` | PASS | `HERMIT-0330` |
| `HERMIT-0333` | Relation mapping | `R-64` | PASS | `HERMIT-0333` |
| `HERMIT-0336` | Relation mapping | `R-65` | PASS | `HERMIT-0336` |
| `HERMIT-0339` | Relation mapping | `R-68` | PASS | `HERMIT-0339` |
| `HERMIT-0342` | Relation mapping | `R-69` | PASS | `HERMIT-0342` |
| `HERMIT-0345` | Relation mapping | `R-70` | PASS | `HERMIT-0345` |
| `HERMIT-0348` | Relation mapping | `R-71` | PASS | `HERMIT-0348` |
| `HERMIT-0351` | Relation mapping | `R-72` | PASS | `HERMIT-0351` |
| `HERMIT-0354` | Relation mapping | `RX-001` | PASS | `HERMIT-0354` |
| `HERMIT-0357` | Relation mapping | `RX-002` | PASS | `HERMIT-0357` |
| `HERMIT-0360` | Relation mapping | `RX-003` | PASS | `HERMIT-0360` |
| `HERMIT-0363` | Relation mapping | `RX-004` | PASS | `HERMIT-0363` |
| `HERMIT-0366` | Relation mapping | `RX-006` | PASS | `HERMIT-0366` |
| `HERMIT-0369` | Relation mapping | `RX-007` | PASS | `HERMIT-0369` |
| `HERMIT-0372` | Relation mapping | `RX-008` | PASS | `HERMIT-0372` |
| `HERMIT-0375` | Relation mapping | `RX-009` | PASS | `HERMIT-0375` |
| `HERMIT-0378` | Relation mapping | `RX-011` | PASS | `HERMIT-0378` |
| `HERMIT-0381` | Relation mapping | `RX-012` | PASS | `HERMIT-0381` |
| `HERMIT-0384` | Relation mapping | `RX-013` | PASS | `HERMIT-0384` |
| `HERMIT-0387` | Relation mapping | `RX-014` | PASS | `HERMIT-0387` |
| `HERMIT-0390` | Relation mapping | `RX-015` | PASS | `HERMIT-0390` |
| `HERMIT-0393` | Relation mapping | `RX-016` | PASS | `HERMIT-0393` |
| `HERMIT-0396` | Relation mapping | `RX-017` | PASS | `HERMIT-0396` |
| `HERMIT-0399` | Relation mapping | `RX-018` | PASS | `HERMIT-0399` |
| `HERMIT-0402` | Relation mapping | `RX-019` | PASS | `HERMIT-0402` |
| `HERMIT-0405` | Relation mapping | `RX-021` | PASS | `HERMIT-0405` |
| `HERMIT-0408` | Relation mapping | `RX-022` | PASS | `HERMIT-0408` |
| `HERMIT-0411` | Relation mapping | `RX-023` | PASS | `HERMIT-0411` |
| `HERMIT-0414` | Relation mapping | `RX-024` | PASS | `HERMIT-0414` |
| `HERMIT-0417` | Relation mapping | `RX-025` | PASS | `HERMIT-0417` |
| `HERMIT-0420` | Relation mapping | `RX-026` | PASS | `HERMIT-0420` |
| `HERMIT-0423` | Relation mapping | `RX-027` | PASS | `HERMIT-0423` |
| `HERMIT-0426` | Relation mapping | `RX-028` | PASS | `HERMIT-0426` |
| `HERMIT-0429` | Relation mapping | `RX-029` | PASS | `HERMIT-0429` |
| `HERMIT-0432` | Relation mapping | `RX-030` | PASS | `HERMIT-0432` |
| `HERMIT-0435` | Relation mapping | `RX-031` | PASS | `HERMIT-0435` |
| `HERMIT-0438` | Relation mapping | `RX-032` | PASS | `HERMIT-0438` |
| `HERMIT-0441` | Relation mapping | `RK2-001` | PASS | `HERMIT-0441` |
| `HERMIT-0444` | Relation mapping | `RK2-002` | PASS | `HERMIT-0444` |
| `HERMIT-0447` | Relation mapping | `RK2-003` | PASS | `HERMIT-0447` |
| `HERMIT-0450` | Relation mapping | `RK2-004` | PASS | `HERMIT-0450` |
| `HERMIT-0453` | Relation mapping | `RK2-005` | PASS | `HERMIT-0453` |
| `HERMIT-0456` | Relation mapping | `RK2-007` | PASS | `HERMIT-0456` |
| `HERMIT-0459` | Relation mapping | `RK2-008` | PASS | `HERMIT-0459` |
| `HERMIT-0462` | Relation mapping | `RK2-009` | PASS | `HERMIT-0462` |
| `HERMIT-0465` | Relation mapping | `RK2-010` | PASS | `HERMIT-0465` |
| `HERMIT-0468` | Relation mapping | `RK2-011` | PASS | `HERMIT-0468` |
| `HERMIT-0471` | Relation mapping | `RK2-012` | PASS | `HERMIT-0471` |
| `HERMIT-0474` | Relation mapping | `RK2-013` | PASS | `HERMIT-0474` |
| `HERMIT-0477` | Relation mapping | `RK2-014` | PASS | `HERMIT-0477` |
| `HERMIT-0480` | Relation mapping | `RK2-015` | PASS | `HERMIT-0480` |
| `HERMIT-0483` | Relation mapping | `RK2-016` | PASS | `HERMIT-0483` |
| `HERMIT-0486` | Relation mapping | `RK2-017` | PASS | `HERMIT-0486` |
| `HERMIT-0489` | Relation mapping | `RK2-018` | PASS | `HERMIT-0489` |
| `HERMIT-0492` | Relation mapping | `RK2-019` | PASS | `HERMIT-0492` |
| `HERMIT-0495` | Relation mapping | `RK2-020` | PASS | `HERMIT-0495` |
| `HERMIT-0498` | Relation mapping | `RK2-021` | PASS | `HERMIT-0498` |
| `HERMIT-0501` | Relation mapping | `RK2-022` | PASS | `HERMIT-0501` |
| `HERMIT-0504` | Relation mapping | `RK2-023` | PASS | `HERMIT-0504` |
| `HERMIT-0507` | Relation mapping | `RK2-024` | PASS | `HERMIT-0507` |
| `HERMIT-0510` | Relation mapping | `RK2-025` | PASS | `HERMIT-0510` |
| `HERMIT-0513` | Relation mapping | `RK2-026` | PASS | `HERMIT-0513` |
| `HERMIT-0516` | Relation mapping | `RK3-001` | PASS | `HERMIT-0516` |
| `HERMIT-0519` | Relation mapping | `RK3-003` | PASS | `HERMIT-0519` |
| `HERMIT-0522` | Relation mapping | `RK3-004` | PASS | `HERMIT-0522` |
| `HERMIT-0605` | Constraint encoding disposition | `C-01` | PASS | `H-C-01-IDENTITY-COUNTERMODEL` |
| `HERMIT-0607` | Constraint encoding disposition | `C-02` | PASS | `H-C02-NO-REALIZATION` |
| `HERMIT-0609` | Constraint encoding disposition | `C-03` | NOT_RUN | `—` |
| `HERMIT-0611` | Constraint encoding disposition | `C-04` | NOT_RUN | `—` |
| `HERMIT-0613` | Constraint encoding disposition | `C-05` | NOT_RUN | `—` |
| `HERMIT-0615` | Constraint encoding disposition | `C-06` | NOT_RUN | `—` |
| `HERMIT-0617` | Constraint encoding disposition | `C-07` | PASS | `H-C07-NO-AUTHORITY` |
| `HERMIT-0619` | Constraint encoding disposition | `C-08` | NOT_RUN | `—` |
| `HERMIT-0621` | Constraint encoding disposition | `C-09` | NOT_RUN | `—` |
| `HERMIT-0623` | Constraint encoding disposition | `C-10` | NOT_RUN | `—` |
| `HERMIT-0625` | Constraint encoding disposition | `C-11` | NOT_RUN | `—` |
| `HERMIT-0627` | Constraint encoding disposition | `C-12` | NOT_RUN | `—` |
| `HERMIT-0629` | Constraint encoding disposition | `C-13` | NOT_RUN | `—` |
| `HERMIT-0631` | Constraint encoding disposition | `C-14` | NOT_RUN | `—` |
| `HERMIT-0633` | Constraint encoding disposition | `C-15` | PASS | `H-C15-TWO-DISTINCT-BEARERS` |
| `HERMIT-0635` | Constraint encoding disposition | `C-16` | NOT_RUN | `—` |
| `HERMIT-0637` | Constraint encoding disposition | `C-17` | NOT_RUN | `—` |
| `HERMIT-0639` | Constraint encoding disposition | `C-18` | NOT_RUN | `—` |
| `HERMIT-0641` | Constraint encoding disposition | `C-19` | NOT_RUN | `—` |
| `HERMIT-0643` | Constraint encoding disposition | `C-20` | PASS | `H-C20-NO-CASE-ENTRY-EQUIVALENCE` |
| `HERMIT-0645` | Constraint encoding disposition | `C-21` | NOT_RUN | `—` |
| `HERMIT-0647` | Constraint encoding disposition | `C-22` | PASS | `H-C22-NO-PARTICIPANT-PAIR-KEY` |
| `HERMIT-0649` | Constraint encoding disposition | `C-23` | PASS | `H-C23-NO-REVERSE-CONTEXT, H-C23-ANALYZED-IMPLIES-CONTEXT` |
| `HERMIT-0651` | Constraint encoding disposition | `C-24` | PASS | `H-C-24-IDENTITY-COUNTERMODEL, H-C24-REVISION-IMPLIES-VERSION` |
| `HERMIT-0653` | Constraint encoding disposition | `C-25` | NOT_RUN | `—` |

## Quality limits and next work

The result establishes consistency and satisfiability for this exact mapped snapshot, with traceable HermiT oracle checks. It does not prove exhaustive semantic validity, requirement acceptance, empirical usefulness or independent expert agreement. Some negative probes demonstrate a countermodel or a non-entailment for a named fixture; absence of an asserted statement by itself is never treated as negation. The unrun constraint obligations need reviewed OWL extensions where justified, SHACL profiles, application checks or independent interpretation evidence. Issue #5 should implement explicit-data SHACL profiles; #6 must reconcile requirement and CQ execution. The [OWL mapping review](../owl-mapping-review.md) details every constraint's encoding boundary.
