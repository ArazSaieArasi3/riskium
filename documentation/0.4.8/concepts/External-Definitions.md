# External definitions and documentary dispositions

Review **0.1.0** · 2026-11-05 · model **0.3.1** · [Tracking #85](https://github.com/ArazSaieArasi3/riskium/issues/85).

Bounded documentary curation of all 80 concepts, not a systematic literature review or independent semantic acceptance.

## Review method

Each authored definition and modeling identity was read against the named selected primary-source passages. The record retains version/date, exact term or section locator, a short paraphrase, a concept-specific comparison and any follow-up. This is assistant-supported documentary curation, not a human independent rating. No exhaustive search or absence of other relevant ontologies is asserted. Existing COVER/IRISPortal comparisons retain their own inspected scope.

No definition in the authoritative model is replaced. No external class is imported; no equivalence, subclass or SKOS match axiom is generated. Normative adoption remains in [#78](https://github.com/ArazSaieArasi3/riskium/issues/78); independent interpretation remains in [#23](https://github.com/ArazSaieArasi3/riskium/issues/23).

## Decision vocabulary

| Disposition | Meaning | Count |
| --- | --- | ---: |
| RELATED | A relevant definitional precedent, without equivalence or formal subsumption. | 40 |
| ANALOGY | A pattern or restricted-domain analogy; extension and commitments differ. | 18 |
| CONTRAST | A documented distinction preventing a misleading identification. | 13 |
| NO_DIRECT_EQUIVALENT_REVIEWED | No direct equivalent adopted from the named inspected entries only; not a claim that none exists elsewhere. | 6 |
| NEEDS_LICENSED_SOURCE | Normative adoption deferred; source identity checked, term text unassessed. | 3 |

Formal equivalences: **0**. Independent ratings: **0**. All 80 documentary decisions are recorded; the three licensed-source deferrals are not claimed as completed normative mappings.

## Sources and inspected portions

### prov

[PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/). W3C Recommendation, 30 April 2013. Accessed 2026-11-05.

Terms listed below only; no PROV conformance or import asserted.

Response-body SHA-256: `6b96671ab84faf12ce3f041aca12c3f93a6df2ed242348810743179a68e69555`.

### skos

[SKOS Simple Knowledge Organization System Reference](https://www.w3.org/TR/2009/REC-skos-reference-20090818/). W3C Recommendation, 18 August 2009. Accessed 2026-11-05.

Concept, scheme and lexical-label distinctions; no SKOS mapping triples asserted.

Response-body SHA-256: `3aa00cd16ee4d86d3a19b75501bb317d0b0c134e1f4029e9f3098c4dd3669e4c`.

### sosa

[Semantic Sensor Network Ontology](https://www.w3.org/TR/2017/REC-vocab-ssn-20171019/). W3C Recommendation, 19 October 2017; SOSA/SSN. Accessed 2026-11-05.

Selected core classes only; observed properties and their specifications remain distinct.

Response-body SHA-256: `f563c81c267c36d9a59a163c0a1cafcd75a0eedb5664e20a778fed8547fee31f`.

### dqv

[Data on the Web Best Practices: Data Quality Vocabulary](https://www.w3.org/TR/2016/NOTE-vocab-dqv-20161215/). W3C Working Group Note, 15 December 2016. Accessed 2026-11-05.

Dataset-quality vocabulary used by analogy only. This Note is work in progress, not a W3C Recommendation.

Response-body SHA-256: `271d3e820c681127131595d2c8bf8345e925149192f6cab821f101f09d372a63`.

### oa

[Web Annotation Data Model](https://www.w3.org/TR/2017/REC-annotation-model-20170223/). W3C Recommendation, 23 February 2017. Accessed 2026-11-05.

Selected motivations and annotation/body distinction only; no serialization conformance asserted.

Response-body SHA-256: `a7513e022f56c0a6f4e99ac11aec03f3451d1ff1ce14054780b3ccfb38fa7980`.

### nist

[Guide for Conducting Risk Assessments, NIST SP 800-30 Revision 1](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf). September 2012; DOI 10.6028/NIST.SP.800-30r1. Accessed 2026-11-05.

Security-specific terms, selected glossary entries and tables only; not a universal enterprise-risk vocabulary. Glossary entries retain their original attributions.

Response-body SHA-256: `f214087f0bdb35932a28c16eb93932a33c67a6edfb5e6f1638866bd201c98e04`.

### relator

[OntoUML specification: Relator](https://ontouml.readthedocs.io/en/latest/classes/sortals/relator/index.html). Unversioned latest documentation, retrieved 5 November 2026; response SHA-256 retained. Accessed 2026-11-05.

Definition and constraints C1-C2 only; this modeling construct is not the definition of a responsibility mandate.

Response-body SHA-256: `639fcd67050a2dbb0d94fe6567a112e039d8b0ea429f636f3e7122d36c564757`.

### iso

[ISO 31073:2022, Risk management — Vocabulary](https://www.iso.org/standard/79637.html). Edition 1, February 2022. Accessed 2026-11-05.

Official identity and abstract inspected; normative term text NOT inspected. No exact term or clause number claimed; #78 owns adoption.

Response-body SHA-256: `562ac6054dcb28c3599118fee2757f4cdfd21bb8a037a3444a99ea7fb208e883`.

### mode

[OntoUML specification: Mode](https://ontouml.readthedocs.io/en/latest/classes/aspects/mode/index.html). Unversioned latest documentation, inspected 5 November 2026. Accessed 2026-11-05.

Definition and constraints C1-C2 inspected through public indexed full text; direct response returned HTTP 403, so no response-body hash is claimed.

No response-body hash claimed; the access route and its limit are documented above.

## D01 Risk Phenomena

| Concept | Decision | Source-comparison rationale |
| --- | --- | --- |
| [Risk Pattern Specification](RKM-C001.md) | RELATED | Reusable risk-pattern content is a managed specification; an intention to carry out steps is not required for every pattern. |
| [Risk Context Specification](RKM-C002.md) | RELATED | Riskium adds boundaries, horizon and objective references to a versioned information specification; PROV Entity supplies no such context schema. |
| [Risk Scenario Specification](RKM-C003.md) | ANALOGY | The security source organizes threat events; Riskium records general possible developments about continuing cases, including effects beyond security. |
| [Risk Occurrence](RKM-C004.md) | CONTRAST | NIST permits a potential event or situation; Riskium Occurrence requires an actual occurrence, so the source term cannot establish realization. |
| [Risk Nature Assertion](RKM-C005.md) | RELATED | Risk nature is an objective-relative source claim; a classification motivation alone supplies neither favorable/unfavorable meaning nor truth. |
| [Nature Term](RKM-C006.md) | RELATED | The controlled nature value is an identified vocabulary resource; its label is not its scheme-qualified identity. |
| [Risk Source](RKM-C007.md) | ANALOGY | Riskium permits heterogeneous contextual contributors and opportunities; the security threat-source definition is narrower in subject matter, without a proved class subsumption. |
| [Predisposing Condition](RKM-C008.md) | RELATED | The source allows likelihood to increase or decrease; the Riskium definition selects susceptibility-increasing conditions and does not assert causation. |
| [Trigger](RKM-C009.md) | CONTRAST | Riskium Trigger is actual and initiating in context; a potential threat event supplies neither actuality nor the initiating interpretation. |
| [Consequence](RKM-C010.md) | NO_DIRECT_EQUIVALENT_REVIEWED | A potentially harmful event is not its consequence. No direct definition for Riskium’s cross-category outcome boundary is adopted from this inspected entry. |
| [Vulnerability](RKM-C011.md) | RELATED | The security weakness account informs one use; the intrinsic-mode interpretation separately requires a bearer. Neither source equates all vulnerabilities with one domain class. |
| [Exposure](RKM-C012.md) | ANALOGY | The source links exposure/susceptibility to conditions; Riskium’s timed bearer-to-source situation is a separate authored interpretation, not that note’s formal model. |
| [Risk State](RKM-C013.md) | NO_DIRECT_EQUIVALENT_REVIEWED | Considering fixed aspects of an entity does not define the temporal state of a risk situation; the risk-state/workflow distinction remains authored. |
| [Risk Case](RKM-X01.md) | NO_DIRECT_EQUIVALENT_REVIEWED | PROV Entity does not specify continuing organizational risk-case identity. This scoped source comparison neither proves novelty nor replaces the existing COVER/IRISPortal comparison or independent review. |
| [Risk Source Reference](RKM-X06.md) | CONTRAST | A recorded contributor reference may remain hypothetical or unresolved; it cannot be identified with NIST’s threat source or establish actual causation. |

## D02 Risk Information

| Concept | Decision | Source-comparison rationale |
| --- | --- | --- |
| [Information Artifact](RKM-C014.md) | RELATED | A managed documentary identity persisting across versions has additional institution and content conditions not supplied by PROV Entity. |
| [Artifact Version](RKM-C015.md) | CONTRAST | An issued Artifact Version is an entity; prov:Revision describes a derivation, not the resulting version. First issue also need not be a revision. |
| [Information Content](RKM-C016.md) | RELATED | PROV permits conceptual entities but gives no policy for identity of abstract meanings; Riskium content equivalence remains application-governed. |

## D03 Risk Classification

| Concept | Decision | Source-comparison rationale |
| --- | --- | --- |
| [Vocabulary Concept](RKM-C017.md) | RELATED | SKOS separates vocabulary notions from their labels and from OWL classes; Riskium additionally manages the documentary resource’s identity. |
| [Classification Scheme](RKM-C018.md) | RELATED | ConceptScheme informs vocabulary organization; Riskium adds scope and governance/version policies without asserting identical extension. |
| [Classification Term](RKM-C019.md) | RELATED | A classification value is modeled as an identified scheme-qualified resource; it is not a lexical label or automatically an OWL universal. |
| [Classification Assertion](RKM-C020.md) | RELATED | A classification motivation helps distinguish the assignment statement from its subject; Riskium additionally requires source and context qualification. |
| [Tag](RKM-C021.md) | RELATED | The tagging motivation and its lexical content inform use; the Riskium tag artifact and any assignment still require explicit identities. |

## D04 Risk Registration

| Concept | Decision | Source-comparison rationale |
| --- | --- | --- |
| [Risk Register Entry](RKM-C022.md) | RELATED | The record is a documentary entity about one case in this profile; PROV Entity neither imposes that cardinality nor identifies the case with its entry. |
| [Entry Revision](RKM-C023.md) | CONTRAST | An Entry Revision is a version entity with qualified effective links; prov:Revision is the provenance relationship producing a revision. |
| [Risk Description](RKM-C024.md) | RELATED | Description motivation helps identify a documentary function; the Riskium item has a source and may concern a case, pattern or scenario. |
| [Consequence Statement](RKM-C025.md) | RELATED | Descriptive content about an outcome does not create that outcome; the source motivation does not supply consequence semantics. |
| [Identification Information](RKM-C026.md) | RELATED | Entity-to-agent attribution can document one part of identification provenance; it is not the full recorded identification, channel or time information. |
| [Intake Channel Term](RKM-C027.md) | RELATED | An intake channel value is a local vocabulary notion, separate from a real-world contributor to risk; SKOS supplies no specific channel taxonomy. |
| [Description Role Term](RKM-C028.md) | RELATED | Description roles are local controlled vocabulary resources; their actual allowed functions are defined by Riskium’s source profile. |
| [Consequence Slot Term](RKM-C029.md) | RELATED | A consequence slot preserves the source’s positional vocabulary; no universal consequence ordering follows from SKOS. |
| [Risk Register](RKM-C030.md) | RELATED | Membership organization is a useful information-level analogy; prov:Collection does not turn a register into an OntoUML collective or impose register governance. |

## D05 Risk Assessment

| Concept | Decision | Source-comparison rationale |
| --- | --- | --- |
| [Assessment Activity](RKM-C031.md) | CONTRAST | Riskium Activity may be only part of an assessment; the NIST process and security scope cannot be equated with every such activity. |
| [Assessment Information](RKM-C032.md) | ANALOGY | A security assessment report is a relevant documentary precedent; Riskium information also binds versions, methods, basis and temporal interpretation. |
| [Assessment Basis](RKM-C033.md) | NO_DIRECT_EQUIVALENT_REVIEWED | A generic information entity does not define a risk-specific assumption/control basis. The basis specification remains authored, with no exact external term adopted. |
| [Dimension Assessment Result](RKM-C034.md) | ANALOGY | DQV evaluates dataset quality; Riskium records a risk-dimension result. A measurement pattern is relevant without equating the assessment domains. |
| [Assessment Method Specification](RKM-C035.md) | ANALOGY | Reusable procedures distinguish a method from an execution; the SOSA domain and Riskium’s risk-assessment interpretation rules differ. |
| [Assessment Scale](RKM-C036.md) | ANALOGY | NIST’s example vulnerability-severity levels illustrate a scale, without defining all permissible Riskium dimensions, units or version-compatibility policies. |
| [Risk Score Result](RKM-C037.md) | ANALOGY | A metric-qualified output illustrates how to document a score; Riskium’s numeric risk output is not dataset quality or the risk itself. |
| [Assessment Scale Level](RKM-C038.md) | RELATED | An identified scale-level resource is distinct from both its label and an assessed value occurrence; the scale version supplies interpretation. |
| [Assessment Dimension](RKM-C039.md) | ANALOGY | DQV’s criterion is modeled as a SKOS concept; Riskium’s vocabulary aspect and its judged result remain distinct from dataset-quality criteria. |
| [Epistemic Status Term](RKM-C040.md) | RELATED | Observed/estimated/projected status is local controlled terminology; SKOS does not determine its epistemic adequacy. |
| [Uncertainty Statement](RKM-X03.md) | RELATED | An annotation can express uncertainty context, but supplies no probability or evidence-strength semantics; Riskium preserves the authored statement and its limitations. |
| [Risk Evaluation Outcome](RKM-X04.md) | CONTRAST | A significance/acceptability judgment against criteria is not merely an observed number or metric result; the decision semantics remain Riskium’s authored specification. |

## D06 Risk Treatment

| Concept | Decision | Source-comparison rationale |
| --- | --- | --- |
| [Treatment Decision Information](RKM-C041.md) | CONTRAST | A recorded decision selecting a response differs from implementing that response; the security process term does not establish authority or success. |
| [Treatment Strategy Term](RKM-C042.md) | RELATED | Treatment approach values are controlled resources; their selection and any realization are represented separately. |
| [Plan Specification](RKM-C043.md) | RELATED | Intended actions toward a goal are relevant; Riskium adds versioned resources, responsibility, timing and conditions, without asserting full class equivalence. |
| [Treatment Activity](RKM-C044.md) | ANALOGY | Actual treatment performance relates to security response actions but is general in domain; a plan does not prove performance or effectiveness. |
| [Risk Control](RKM-C045.md) | ANALOGY | Security safeguards cover one use of risk control; Riskium permits cross-category contextual measures and separates implementation from effectiveness. |
| [Plan Role Term](RKM-C046.md) | RELATED | Primary/contingency are locally governed plan-role values; SKOS provides a vocabulary pattern rather than those domain meanings. |
| [Control Reference](RKM-X05.md) | CONTRAST | A documentary identifier may describe a safeguard without proving that its bearer exists, is implemented or is effective. |

## D07 Risk Responsibility

| Concept | Decision | Source-comparison rationale |
| --- | --- | --- |
| [Agent](RKM-C047.md) | RELATED | Provenance responsibility provides useful agent context; Riskium’s scoped capabilities and accountabilities need a declared mapping, not label-based equivalence. |
| [Person](RKM-C048.md) | RELATED | The human-agent reading is compatible context; formal identity/typing alignment with Riskium Person remains unassessed. |
| [Organization](RKM-C049.md) | RELATED | The social/legal institutional reading informs scope; Riskium responsibility and authorization commitments are additional modeling choices. |
| [Actor Reference](RKM-C050.md) | CONTRAST | A source identifier or description is documentary information; it does not establish an actual agent or resolve the referred identity. |
| [Responsibility Assignment Information](RKM-C051.md) | CONTRAST | PROV Association attributes responsibility within an activity; Riskium Assignment Information records a claim whose grounding may remain unsupported. |
| [Responsibility Relator](RKM-C052.md) | RELATED | Relator gives the multiple-participant grounding pattern; mandate, temporal scope and responsibility semantics remain Riskium-specific and need semantic judgment. |
| [Responsible Agent Role](RKM-C053.md) | ANALOGY | An activity-qualified function is useful context; an OntoUML agent role and a grounded responsibility assignment are not identical to a PROV Role value. |
| [Authorizing Agent Role](RKM-C054.md) | ANALOGY | Approval/issue authority is Riskium-specific; a provenance role or participation does not by itself establish authorization. |
| [Responsible Person](RKM-C055.md) | ANALOGY | Being a person plus a provenance function does not establish the grounded responsible-person role for a particular mandate. |
| [Responsible Organization](RKM-C056.md) | ANALOGY | Being an organization plus a provenance function does not establish the grounded responsible-organization role. |
| [Authorizing Person](RKM-C057.md) | ANALOGY | Person identity is separate from supported approval authority; PROV does not supply the Riskium authorization policy. |
| [Authorizing Organization](RKM-C058.md) | ANALOGY | Organization identity is separate from supported approval authority; the source offers no Riskium mandate acceptance test. |
| [Responsibility Role Term](RKM-C059.md) | RELATED | The term names a responsibility type; an assigned vocabulary value is not the actual role or the relationship grounding it. |

## D08 Risk Workflow

| Concept | Decision | Source-comparison rationale |
| --- | --- | --- |
| [Analysis State Term](RKM-C060.md) | RELATED | Analysis-progress values belong to a declared local scheme; they do not imply anything about the real-world risk state. |
| [Workflow State Term](RKM-C061.md) | RELATED | Processing-status values belong to a declared workflow vocabulary; closure does not establish cessation of risk. |
| [Record State Assertion](RKM-C062.md) | RELATED | An annotation can express information about a target; Riskium additionally records source-qualified record-state claims and available time precision. |
| [Workflow Scheme Version](RKM-C063.md) | CONTRAST | A version of a workflow scheme defines transitions; SKOS scheme aggregation and a PROV revision derivation supply neither those transitions nor authorization rules. |
| [Workflow Assignment](RKM-C064.md) | NO_DIRECT_EQUIVALENT_REVIEWED | PROV Role is an activity-qualified function, not the timed record-state situation specified here. No direct external equivalent is adopted from that comparison. |

## D09 Risk Evidence

| Concept | Decision | Source-comparison rationale |
| --- | --- | --- |
| [Evidence Reference](RKM-C065.md) | RELATED | Provenance links can support traceability; a derivation does not define an evidence role, entail claim truth or establish independent corroboration. |
| [Evidence Item](RKM-C066.md) | RELATED | An artifact may play an evidential role in context; a generic entity/function does not make every information artifact evidence for every claim. |

## D10 Risk Monitoring

| Concept | Decision | Source-comparison rationale |
| --- | --- | --- |
| [Observation Activity](RKM-C067.md) | RELATED | The procedure/feature/value separation informs observations; Riskium’s subject, time and procedure qualification remains its own profile. |
| [Observation Result](RKM-C068.md) | RELATED | SOSA Result includes actuation and sampling outputs too; Riskium selects observation information and adds explicit interpretation context. |
| [Indicator](RKM-C069.md) | ANALOGY | The indicator is a versioned information specification; it is neither SOSA’s observable property nor a DQV dataset-quality metric as such. |
| [Threshold](RKM-C070.md) | NO_DIRECT_EQUIVALENT_REVIEWED | A measuring standard is not a comparator-qualified decision boundary. No direct threshold equivalent is adopted from the inspected DQV entry. |
| [Signal](RKM-C071.md) | RELATED | An informative signal may arise from results, but is not automatically an observation result or proof of a risk event. |

## D11 Risk Policy

| Concept | Decision | Source-comparison rationale |
| --- | --- | --- |
| [Risk Criteria](RKM-C072.md) | NEEDS_LICENSED_SOURCE | The ISO catalogue confirms edition identity only. Exact normative risk-criteria wording and clause mapping remain unassessed until legitimate text is inspected. |
| [Risk Appetite Statement](RKM-C073.md) | NEEDS_LICENSED_SOURCE | Riskium models the managed appetite statement. Exact ISO/Risk IT/COBIT term-level readings require the adopted editions and locators in #78; no normative definition is asserted here. |
| [Risk Tolerance Statement](RKM-C074.md) | NEEDS_LICENSED_SOURCE | The recorded tolerance statement retains source-specific meanings. Metadata cannot resolve permissible-deviation versus remaining-risk readings or justify a normative crosswalk. |
| [Objective Reference](RKM-X02.md) | CONTRAST | An informational objective reference and the objective referred to are distinct; PROV Entity’s broad scope cannot alone resolve their identity. |

