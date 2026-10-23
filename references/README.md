# Sources, standards and prior-art interpretation

Post-prerelease editorial review dated **2026-10-23**, against conceptual design **0.3.1** at `cfb85905ab37549c7090f00a41ca62cdd3364ab5`. Eleven selected method, standards/framework and risk-ontology sources are recorded with their actual inspected portions. This completes the bounded public corpus in #8, not a full normative or systematic literature review.

The machine-readable [corpus](corpus.json) owns source identities, reading locators, uses, interpretations and remaining limits. The [integrity receipt](../evaluation/references/report.json) checks this register against the model; it does not assess the truth of the external sources or establish semantic correctness.

## Review method and selection

Start from the five references already public at commit 7c2eed823a4d1e2df75c43bbdbf13b0c58960b2f; add official ISACA scope sources named by the model and a targeted COVER/ROSE research lineage update. Search primary publisher, author, standards-body and versioned repository records. Retain sources with a stated use in this model; do not rank ontologies by unmeasured quality. Search snippets identify candidates only. Selected public abstracts and selected method text support scope comparisons; they do not substitute for unseen chapters, clauses, experiments or formal mappings. The search is purposive and non-exhaustive through the review date.

The public baseline had a bibliography but no edition/portion-qualified comparison matrix. This is a new post-prerelease review, not a reconstruction of inaccessible pre-public acquisition records. Retained findings preserve the model's case/record, reference/referent, source-qualified vocabulary and knowledge/process distinctions. The model's historical claim ceiling is not inherited as proof that all source clauses were screened. No private text, unpublished review or reviewer approval is asserted.

| Search family | Queries / route | Selection |
| --- | --- | --- |
| Existing methods | Exact SABiO and ORSD titles; OntoUML Role and Relator documentation | Retain REF-SABIO, REF-ORSD and REF-ONTOUML; correct the old no-native-validation wording. |
| Standards and frameworks | site:iso.org ISO 31000:2018 / ISO 31073:2022; site:isaca.org Risk IT 2nd Edition / COBIT 2019 | Retain official catalog, committee, public announcement and publication-overview portions only; no paywalled full-work reading. |
| Risk-ontology lineage | Common Ontology of Value and Risk Sales Guizzardi; An Ontology of Security from a Risk Treatment Perspective | Retain COVER publisher/author abstract and introduction plus selected pinned OWL declarations; retain ROSE publisher abstract. |
| Recent related work | COVER risk ontology Guizzardi 2025 / 2026; DODGE ontology-aware risk; ontological lens attack trees | Retain versioned WATCHDOG v2 and attack-tree v1 records; explicitly reconcile the older DODGE title. No claim that these exhaust later work. |
| 2026 candidate screening | site:foisconference.org/assets/pdfs/jowo risk ontology 2026 | Towards a Conceptual Clarification of Cybersecurity candidate at fomi-6.pdf returned HTTP 403 on opening; not interpreted from its snippet or counted as reviewed. It remains an access-limited literature-update candidate. |

## Verified source identities and inspected portions

### REF-SABIO — SABiO

Ricardo de Almeida Falbo (2014). SABiO: Systematic Approach for Building Ontologies. ONTO.COM/ODISE, CEUR Workshop Proceedings, vol. 1301.

**Version:** 2014 paper describing SABiO 2.0; not the original 1997 method

**Inspected:** Author/title, abstract, sections 1–2, and selected section 3 text on requirements, conceptual capture, operational design and testing (PDF pages 1–8).

**Source finding (paraphrase):** Distinguishes reference conceptualizations from operational implementations and uses requirements and competency questions to organize development and finite testing.

**Actual use in Riskium:** Method context for requirements/ontology-requirements.md, evaluation/owl-mapping-review.md and requirements/cq/README.md; keep conceptual adequacy separate from executable query checks.

**Access and interpretation limits:** Selected sections only. This is a methodological influence, not evidence that every SABiO activity or stakeholder validation has been completed.

Primary reading locators:

- [Title/abstract; sections 1–2 and selected section 3 text, PDF pp. 1–8](https://ceur-ws.org/Vol-1301/ontocomodise2014_2.pdf), checked 2026-10-23.

### REF-ORSD — Ontology requirements specification

Mari Carmen Suárez-Figueroa, Asunción Gómez-Pérez and Boris Villazón-Terrazas (2009). How to Write and Use the Ontology Requirements Specification Document. OTM 2009, LNCS 5871, pp. 966–982. DOI: 10.1007/978-3-642-05151-7_16.

**Version:** 2009 publisher chapter record

**Inspected:** Publisher title, authors, bibliographic metadata, abstract and access notice; full chapter not inspected.

**Source finding (paraphrase):** Requirements specification states purpose, intended use, users and requirements, supporting reuse and verification.

**Actual use in Riskium:** Organization of requirements/ontology-requirements.md and the distinction between a requirement specification and its evaluation/traceability evidence.

**Access and interpretation limits:** Abstract-level method context only; no claim that the detailed chapter guidelines or its example projects were assessed. The DOI redirect initially failed; the explicit publisher chapter URL was readable.

Primary reading locators:

- [Bibliographic header, Abstract and subscription-content notice](https://link.springer.com/chapter/10.1007/978-3-642-05151-7_16), checked 2026-10-23.

### REF-ONTOUML — OntoUML Role and Relator

OntoUML specification documentation. Role; Relator. Read the Docs, latest channel, accessed 23 October 2026.

**Version:** Mutable latest documentation; no numbered specification release or commit inferred

**Inspected:** Role and Relator definition/constraint tables and prose; example images and the full language were not reviewed in this batch.

**Source finding (paraphrase):** Roles depend on relational contexts and inherit identity; relators ground material relations and require mediation with aggregate minimum participation of at least two.

**Actual use in Riskium:** Interpretation context for responsibility roles/relators and C-06/C-07/C-22; source-schema/SDK checks are separately reported in evaluation/native-model-review.md.

**Access and interpretation limits:** C-06 participant distinctness and mandate-grounding policies remain explicit local decisions. The selected documentation is not a proof of full OntoUML conformance or independent semantic acceptance.

Primary reading locators:

- [Role definition and C1–C4](https://ontouml.readthedocs.io/en/latest/classes/sortals/role/index.html), checked 2026-10-23.
- [Relator definition and C1–C6](https://ontouml.readthedocs.io/en/latest/classes/sortals/relator/index.html), checked 2026-10-23.

### REF-ISO31000 — ISO 31000:2018

International Organization for Standardization (2018). ISO 31000:2018, Risk management — Guidelines. Second edition, February 2018.

**Version:** Edition 2 (2018-02), catalog status Published; page reports 2023 confirmation and also flags stage 90.92 (to be revised). No successor edition assumed.

**Inspected:** Official catalog header/status, public overview and certification FAQ; ISO's 15 February 2018 news explanation of risk, context and guidelines.

**Source finding (paraphrase):** The public explanation relates risk to uncertainty affecting objectives. Guidance covers organizational risk management and is not a certification requirements standard.

**Actual use in Riskium:** Scope screening and the deliberate separation of RiskCase, objective/uncertainty information and a whole management process; not a clause-conformance crosswalk.

**Access and interpretation limits:** Full standard not read. The OBP route exposed a JavaScript shell, not readable clauses. Do not assign an inspected clause number from the news article or infer universal multiplicities.

Primary reading locators:

- [Edition/status, public overview and certification FAQ](https://www.iso.org/standard/31000), checked 2026-10-23.
- [15 February 2018 news: risk definition and certification explanation](https://www.iso.org/news/ref2263.html), checked 2026-10-23.

### REF-ISO31073 — ISO 31073:2022

International Organization for Standardization (2022). ISO 31073:2022, Risk management — Vocabulary. First edition, February 2022.

**Version:** Edition 1 (2022-02), catalog status Published; French corrected version 2023-01 is listed but was not inspected

**Inspected:** Official catalog identity/abstract and TC 262 committee publication summary; normative term entries not inspected.

**Source finding (paraphrase):** Addresses organizational risk vocabulary, including threats and opportunities; its committee summary allows application-specific terminology qualification.

**Actual use in Riskium:** Keep source/version-qualified vocabulary in nature and tolerance statements; record detailed appetite/tolerance mappings as NOT_ASSESSED in this review.

**Access and interpretation limits:** Committee summary is explanatory and carries a third-party-maintained-content disclaimer; catalog is the edition authority. Neither summary nor indexed snippets establish current normative definitions or full compatibility.

Primary reading locators:

- [Edition, publication metadata and Abstract](https://www.iso.org/standard/79637.html), checked 2026-10-23.
- [Publication summary, application-specific terminology and disclaimer](https://committee.iso.org/sites/tc262/home/projects/published/iso-310732022-risk-management--v.html), checked 2026-10-23.

### REF-RISKIT — Risk IT Framework, second edition

ISACA (2020). Risk IT Framework, 2nd Edition. Edition and release verified through ISACA's public 25 June 2020 announcement and current IT Risk resources page.

**Version:** Second edition, 2020; Practitioner Guide is a separate work and is not silently merged with the Framework

**Inspected:** Public announcement and the Risk IT Framework resource description; not the paid/member framework or practitioner guide.

**Source finding (paraphrase):** Addresses enterprise information-and-technology risk in business context and links its practices to broader governance guidance.

**Actual use in Riskium:** Check the model's knowledge/process scope boundary and retain source context for scenario, treatment and responsibility information.

**Access and interpretation limits:** No detailed scenario taxonomy, Risk Item identity, tolerance definition, activity or role crosswalk established. Historical 2009 terminology is not assumed to equal the 2020 edition.

Primary reading locators:

- [25 June 2020 announcement, edition and business-context description](https://www.isaca.org/about-us/newsroom/press-releases/2020/isacas-risk-it-framework-offers-a-structured-methodology), checked 2026-10-23.
- [Risk IT Framework, 2nd Edition resource description](https://www.isaca.org/resources/it-risk), checked 2026-10-23.

### REF-COBIT — COBIT 2019

ISACA. COBIT 2019 Framework: Governance and Management Objectives. Publication identity verified on ISACA's COBIT resources page.

**Version:** COBIT 2019 named framework; year in the edition name is not an assertion about the copyright date of each volume

**Inspected:** Official public publication description for Governance and Management Objectives and overview of the framework; not its objective/practice tables.

**Source finding (paraphrase):** The described core contains 40 governance/management objectives connected to processes and enterprise/alignment goals.

**Actual use in Riskium:** Bound the claim: storing responsibility, policies, decisions and evidence does not implement the whole governance framework.

**Access and interpretation limits:** No APO12/EDM03 practice, RACI or process-capability conformance reviewed. Other COBIT volumes and focus-area publications are distinct works outside this inspected portion.

Primary reading locators:

- [COBIT 2019 Framework: Governance and Management Objectives publication description](https://www.isaca.org/resources/cobit), checked 2026-10-23.

### REF-COVER — COVER

Tiago Prince Sales, Fernanda Baião, Giancarlo Guizzardi, João Paulo A. Almeida, Nicola Guarino and John Mylopoulos (2018). The Common Ontology of Value and Risk. ER 2018, LNCS 11157, pp. 121–135. DOI: 10.1007/978-3-030-00847-5_11.

**Version:** 2018 paper; separate implementation inspected at unibz-core/value-and-risk-ontology commit 898a7d87d1da0f8c292620d966754a630ae3b57b (29 April 2024)

**Inspected:** Publisher abstract and citation; author-hosted PDF title/abstract/introduction (PDF pp. 1–2); repository README and selected OWL declarations for Vulnerability, RiskSubject, RiskAssessment and Risk. No full paper/model verification.

**Source finding (paraphrase):** Connects risk assessment with value ascription. The inspected implementation distinguishes risk subjects and assessment notions; Vulnerability specializes an intrinsic mode and is metatyped RoleMixin.

**Actual use in Riskium:** Compare case identity with a risk subject; compare vulnerability bearer interpretation without asserting equivalent classes or adopting the entire value/risk account.

**Access and interpretation limits:** Paper and later OWL implementation have separate identities. No import, alignment proof, reasoning benchmark or full artifact assessment. The repository's Apache-2.0 notice does not establish the paper's license; no external implementation is redistributed. The author PDF later timed out/returned 503, so unread later sections are not included.

Primary reading locators:

- [Bibliographic header and Abstract](https://link.springer.com/chapter/10.1007/978-3-030-00847-5_11), checked 2026-10-23.
- [Author PDF title, abstract and introduction, PDF pp. 1–2 only](https://www.inf.ufes.br/~gguizzardi/ER2018-Risk.pdf), checked 2026-10-23.
- [README project structure and paper citation](https://github.com/unibz-core/value-and-risk-ontology/blob/898a7d87d1da0f8c292620d966754a630ae3b57b/README.md), checked 2026-10-23.
- [Selected cover:Vulnerability, cover:RiskSubject, cover:RiskAssessment and cover:Risk declarations](https://github.com/unibz-core/value-and-risk-ontology/blob/898a7d87d1da0f8c292620d966754a630ae3b57b/owl/cover.ttl), checked 2026-10-23.

### REF-ROSE — ROSE

Ítalo Oliveira, Tiago Prince Sales, Riccardo Baratella, Mattia Fumagalli and Giancarlo Guizzardi (2022). An Ontology of Security from a Risk Treatment Perspective. ER 2022, LNCS 13607, pp. 365–379. DOI: 10.1007/978-3-031-17995-2_26.

**Version:** Publisher chapter first online 10 October 2022; artifact named Reference Ontology for Security Engineering (ROSE)

**Inspected:** Publisher citation metadata, abstract and access notice; full chapter/implementation not inspected.

**Source finding (paraphrase):** Uses COVER and prevention foundations to clarify security engineering and security mechanisms from a treatment perspective.

**Actual use in Riskium:** Bound Riskium treatment/control references against a security-phenomena ontology; do not promote recorded references into established mechanisms or effectiveness.

**Access and interpretation limits:** Scope comparison from the abstract only. No class-by-class mapping, domain coverage ranking or experimental replication; absence of a feature in the abstract is not evidence it is absent from ROSE.

Primary reading locators:

- [Bibliographic header, Abstract and subscription notice](https://link.springer.com/chapter/10.1007/978-3-031-17995-2_26), checked 2026-10-23.

### REF-WATCHDOG — WATCHDOG, formerly DODGE

Stefano M. Nicoletti, E. Moritz Hahn, Mattia Fumagalli, Giancarlo Guizzardi and Mariëlle Stoelinga (2025). WATCHDOG: an ontology-aWare risk AssessmenT approaCH via object-oriented DisruptiOn Graphs. arXiv:2412.13964v2. Related CAiSE 2025 DOI recorded by arXiv: 10.1007/978-3-031-94571-7_18.

**Version:** v2, revised 30 June 2025; v1 of 18 December 2024 was titled DODGE: Ontology-Aware Risk Assessment via Object-Oriented Disruption Graphs

**Inspected:** Versioned arXiv v1/v2 metadata, abstracts and submission history. Related publisher chapter and full experimental results not inspected.

**Source finding (paraphrase):** Operationalizes selected COVER ideas using object-oriented disruption graphs and dedicated logic/query machinery for quantitative risk questions.

**Actual use in Riskium:** Separate an ontology-aware computational assessment framework from Riskium's knowledge representation and bounded synthetic SPARQL retrieval.

**Access and interpretation limits:** Version names are not interchangeable citations. No imported computation, probability propagation capability, predictive accuracy or performance comparison is established for Riskium.

Primary reading locators:

- [DODGE v1 title, abstract and submission history](https://arxiv.org/abs/2412.13964v1), checked 2026-10-23.
- [WATCHDOG v2 title, abstract, submission history and related publication DOI](https://arxiv.org/abs/2412.13964v2), checked 2026-10-23.

### REF-ATTACKTREES — Ontological lens on attack trees

Ítalo Oliveira, Stefano M. Nicoletti, Gal Engelberg, Mattia Fumagalli, Dan Klein and Giancarlo Guizzardi (2025). An ontological lens on attack trees: Toward adequacy and interoperability. arXiv:2506.23841v1. DOI: 10.48550/arXiv.2506.23841.

**Version:** arXiv v1, submitted 30 June 2025; no journal publication status inferred

**Inspected:** Versioned arXiv citation metadata, abstract and submission history only.

**Source finding (paraphrase):** Analyzes attack-tree conceptual adequacy and interoperability using COVER, distinguishing ontological analysis from quantitative formalism services.

**Actual use in Riskium:** Explain why engineering passes and executable retrieval alone do not establish semantic adequacy; delimit interoperability and independent-review claims.

**Access and interpretation limits:** Full analysis, proposed repairs and experiments not reviewed. This is not an independently replicated finding about Riskium or a superiority comparison.

Primary reading locators:

- [Title, authors, Abstract and v1 submission history](https://arxiv.org/abs/2506.23841v1), checked 2026-10-23.

## Retained comparison findings

These are author-side interpretations of inspected portions, not independently adjudicated mappings. Correspondence is thematic or representational; divergence preserves distinct meanings. No row asserts OWL equivalence, universal terminology identity or compliance.

| ID / source | Disposition / model targets | Interpretation | Restriction |
| --- | --- | --- | --- |
| INT-01 / REF-SABIO | METHOD_USE: D02, D05 | Keep conceptual design, operational export and finite CQ tests as distinct evidence layers. | Method influence does not establish full process execution or stakeholder consensus. |
| INT-02 / REF-ORSD | METHOD_USE: D01, D04 | Record purpose, scope and intended use before tracing requirements to evidence. | The inspected abstract supports organization, not full adherence to detailed ORSD guidelines. |
| INT-03 / REF-ONTOUML | VOCABULARY_CORRESPONDENCE: RKM-C052, RKM-C053, RKM-C054, C-06, C-22 | Responsibility roles and relators use relational dependence and mediated participation as conceptual anchors. | Two distinct participants, assignment grounding and mandate identity are reviewed local policies; no complete language-conformance proof follows. |
| INT-04 / REF-ISO31000 | SEMANTIC_DIVERGENCE: RKM-X01, RKM-X02, RKM-X03, C-01, C-20 | RiskCase is a governed tracking subject; it is not the uncertainty-related effect described by ISO's public explanation. | Neither RiskCase nor a local Risk Item label is declared universally equivalent to ISO risk. |
| INT-05 / REF-ISO31000, REF-ISO31073 | VOCABULARY_CORRESPONDENCE: RKM-C002, RKM-C005, RKM-C006, RKM-X02 | Source-qualified nature assertions can retain favorable, unfavorable or mixed effects relative to objective/context references. | This is a representation choice consistent with the inspected public scope; it is not a complete term-by-term normative mapping. |
| INT-06 / REF-ISO31073, REF-RISKIT, REF-COBIT | NOT_ASSESSED: RKM-C073, RKM-C074, C-10 | Preserve framework/version/original meaning on appetite and tolerance statements; retain distinct source meanings in the local contract. | Exact current normative definitions and their cross-edition relationship were not read here. No attribution of either local tolerance meaning to an unseen current clause. |
| INT-07 / REF-RISKIT | SCOPE_BOUNDARY: RKM-C003, RKM-C041, RKM-C051 | Riskium retains scenario, treatment and responsibility information; a framework describing enterprise IT risk practice has broader process aims. | The inspected overview does not verify the local scenario structure, mandatory fields or role identity against Risk IT's detailed definitions. |
| INT-08 / REF-COBIT | SCOPE_BOUNDARY: RKM-C051, RKM-C059, C-07 | Recorded responsibility is not implementation of COBIT governance objectives or proof of accountable ownership. | No RACI, APO12, EDM03 or capability assessment has been performed. |
| INT-09 / REF-COVER | SEMANTIC_DIVERGENCE: RKM-X01, RKM-C031, RKM-C037, C-01, C-04 | Do not identify a governed RiskCase with COVER's role-mixin RiskSubject or collapse a recorded result into its value/risk conceptualization. | Selected implementation declarations and the paper abstract do not prove cross-ontology alignment; no sameAs/equivalentClass bridge is asserted. |
| INT-10 / REF-COVER | VOCABULARY_CORRESPONDENCE: RKM-C011, C-15 | Both interpretations connect vulnerability to intrinsic dependence; the inspected COVER declaration additionally uses RoleMixin metatyping. | Riskium's local mode/bearer contract is not the same typing decision. Retain this difference for independent review; no equivalence claimed. |
| INT-11 / REF-ROSE | SCOPE_BOUNDARY: RKM-C041, RKM-C045, RKM-X05, C-02, C-14 | ROSE's abstract concerns security mechanisms and treatment phenomena; Riskium can preserve unresolved control references as information. | A reference or treatment plan proves neither mechanism existence nor effectiveness. No conclusion that ROSE lacks documentary features. |
| INT-12 / REF-WATCHDOG | SCOPE_BOUNDARY: RKM-C035, RKM-C037, C-18, C-21 | WATCHDOG's declared computational services are distinct from retrieval of supplied Riskium assessment information. | A SPARQL result is not a risk-propagation calculation, predictive validation or comparative performance result. |
| INT-13 / REF-ATTACKTREES | SCOPE_BOUNDARY: RKM-C003, RKM-C035, C-12 | Use conceptual adequacy as a separate evaluation question from executable formal/query services. | Riskium has no implemented attack-tree interoperability or independent semantic acceptance from citing this abstract. |

## Open limits and claim ceiling

- LIM-01: Full ISO/Risk IT/COBIT clause and term-definition crosswalks are unassessed; exact appetite/tolerance and risk-owner interpretations require legitimate source access and qualified review. Follow-up: [#7](https://github.com/ArazSaieArasi3/riskium/issues/7), [#14](https://github.com/ArazSaieArasi3/riskium/issues/14).
- LIM-02: All interpretation rows are author-side. Independent adjudication, especially vulnerability typing, case identity and responsibility grounding, remains outstanding. Follow-up: [#7](https://github.com/ArazSaieArasi3/riskium/issues/7), [#11](https://github.com/ArazSaieArasi3/riskium/issues/11).
- LIM-03: The selected prior-art comparison is not a systematic review, novelty proof, feature-absence proof or head-to-head benchmark. Full ROSE/WATCHDOG/attack-tree analyses and the access-blocked 2026 candidate are not assessed. Follow-up: [#13](https://github.com/ArazSaieArasi3/riskium/issues/13), [#14](https://github.com/ArazSaieArasi3/riskium/issues/14).
- LIM-04: The conceptual source's historical no-fundamental-contradiction statement has no reconstructed historical reading corpus here; this review supports only the explicit inspected-portion findings, not universal compatibility or compliance. Follow-up: [#11](https://github.com/ArazSaieArasi3/riskium/issues/11), [#14](https://github.com/ArazSaieArasi3/riskium/issues/14).

Riskium has a discoverable, edition/portion-qualified public source register and explicit bounded comparison findings. No universal standards equivalence, exhaustive contradiction screening, full normative compliance, novel superiority, independent validation or overall semantic-correctness percentage follows. The immutable v0.3.1-rc.1 semantic source and its historical evidence remain unchanged.

## Reproduce the register check

```sh
python3 tools/review_references.py --check
```

Run without `--check` only after deliberately reviewing a corpus change. The command checks source/model identifiers and frozen model bytes, requires dated locators and explicit access/equivalence/compliance limits, then regenerates this page and the integrity receipt. It does not repeat online reading or run HermiT, SHACL or an expert review.

## Rights

Only bibliographic metadata, source links and original Riskium synthesis are distributed here. Third-party papers, standards, code and diagrams retain their own terms; public access alone grants no relicensing permission. No full third-party work, standard clause set or external ontology implementation is copied into this corpus. Riskium scientific synthesis remains under CC BY 4.0; the checking tool is under MIT.
