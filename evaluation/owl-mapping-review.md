# Reviewed OWL mapping, conceptual design 0.3.1

This is the bounded formal export for issue #3. Generate it with `python3 tools/build_owl.py` and check it with `python3 tools/build_owl.py --check`. The committed Turtle and receipt are derived from three inputs: `ontology/riskium-model.json`, `ontology/native/riskium.ontouml.json`, and `evaluation/native-review-decisions.json`. The exporter checks their digests, identifiers, directions, relation ends, multiplicities and set policy. The receipt pins all three SHA-256 digests and the output digest. The source conceptual model was not changed.

## Namespace and import decision

The logical ontology IRI is `https://github.com/ArazSaieArasi3/riskium/ontologies/riskium`; its version IRI is that IRI followed by `/0.3.1`, and its term namespace is the version IRI followed by `#`. These are identifiers, **not claims of deployed or dereferenceable web endpoints**. Local terms use stable source IDs (`RKM-C...`, `R-...`, etc.); labels remain annotations. A new reviewed version must receive a deliberate IRI decision and a fresh receipt. No external ontology is bundled or asserted through `owl:imports`. `EXT-OBJECT` is a separately annotated local proxy for the foundational Object category; external kind identities and the eventual gUFO/UFO alignment remain unresolved. Import closure for this export consists only of its own graph. There is no placeholder external import that a reasoner might silently fail to retrieve.

## Encoding choices

| Source commitment | OWL encoding | Interpretation boundary |
| --- | --- | --- |
| 77 typed local classes, one external anchor | 78 named classes, source ID and OntoUML stereotype annotations | The anchor is a local proxy. `isAbstract` and stereotypes are annotations, not OWL abstract-class semantics. Three optional boundary notions and seven bridges are excluded. |
| 66 directed generalizations | `rdfs:subClassOf` | No equivalence or exhaustive specialization is inferred. |
| 127 typed binary associations | Unique ID-based object properties with declared domain and range; predicate text is a label | Domain/range infer types from assertions. Reading direction is source to target, independent of diagram navigability. No mediation or characterization axiom is invented from the stereotype alone. |
| Multiplicities on ordered relation ends | Qualified class restrictions for each nontrivial end; target end on source class, source end through inverse property on target class | Applies to admitted instances of typed classes in the managed profile. An OWL reasoner may satisfy a missing required value with an anonymous individual or equate two named values to satisfy an upper bound. Explicit-data completeness and distinctness require SHACL or other separately reviewed evidence. |
| Ten reviewed generalization sets | Three declared disjoint sets become `owl:AllDisjointClasses`; seven remain without blanket disjointness | All ten are incomplete. No `unionOf` covering or global sibling disjointness is added. Non-disjoint does not assert actual overlap. |
| Identity and dependence rationale | Source annotations and explicit class/relation restrictions only | No `owl:hasKey`, unique-name assumption, global class equivalence, relator existence rule or automated identity merge. |

The 88 generated qualified restrictions represent nontrivial ends among the 254 ordered ends; unconstrained `0..*` ends have no restriction. Even a syntactically valid OWL graph is not an executed HermiT check, a SHACL validation result, a consistency proof or independent semantic acceptance.

## Constraint disposition

The table accounts for every one of the 25 interpretation constraints. “Partial” means the listed structural portion is encoded; the rest remains an obligation for #4–#6, database/application rules or independent review. An annotation alone does not execute a rule.

| ID | OWL disposition | Remaining obligation |
| --- | --- | --- |
| C-01 | Separate Case, Entry, Scenario and Result classes; no label key | Verify intended identity examples and non-entailment without assuming unique names. |
| C-02 | No description-to-occurrence realization property chain | Verify prohibited inferences; source statements alone cannot certify absence in an open world. |
| C-03 | Version classes/links only; no immutable issued payload semantics | Enforce immutable payloads and lineage in data governance/database. |
| C-04 | Assessment classes, typed links and applicable end bounds | Verify method, scale, dimension, basis, context and time joins in data rules. |
| C-05 | Distinct class/link vocabulary only | Temporal interval and administrative-state rules require explicit data validation. |
| C-06 | Mediation properties and their local end bounds | Distinct participants and actual grounding are not inferred; test or validate separately. |
| C-07 | Responsible/authorizing roles stay separate; no automatic owner equivalence | Ownership interpretation depends on mandate, scope and evidence review. |
| C-08 | Threshold links and their individual end bounds | At-least-one alternative and cross-field unit/scale compatibility require conditional validation. |
| C-09 | Aboutness links and individual end bounds | At-least-one target across several alternative properties requires a separate rule. |
| C-10 | Source-qualified tolerance vocabulary retained | Framework/version meaning and applicability are not a universal OWL equivalence. |
| C-11 | Vocabulary resources are classes of resources, labels annotations | Scheme-qualified identity and label governance require data checks. |
| C-12 | Evidence links carry types, no endorsement implication | Evidential role and truth/endorsement require interpretation. |
| C-13 | Scale/dimension classes and links | Pinning, compatibility and numerical ordering require explicit data rules. |
| C-14 | Three optional boundaries and seven bridges excluded from class/property export | External alignment requires a separately reviewed import or bridge. |
| C-15 | Characterization bearer relation has its reviewed exactly-one source-end restriction | OWL can satisfy existence anonymously or merge named bearers; actual substantial bearer/admission needs separate evidence. |
| C-16 | Typed managed profile is documented | Raw, managed and task-ready admission are SHACL/application profiles, not inferred from absent triples. |
| C-17 | No scalar collapse or forced functional property beyond stated end bounds | Assertion-level provenance, context and export selection remain data obligations. |
| C-18 | Distinct pinned interpretation vocabulary | Comparison and approved transformations need governed calculation rules. |
| C-19 | Workflow labels and state classes remain source-qualified | Transitions, authorization and UNKNOWN handling need data/application rules. |
| C-20 | Risk Item contextual synonym retained in requirements, no OWL equivalence | Context-sensitive terminology needs human review. |
| C-21 | Score/result properties retain local bounds, no universal derivedFrom minimum | Conditional reported-versus-computed dependency and arithmetic need data rules. |
| C-22 | No keys based solely on mediated participant pairs | Mandate identity and duplicate adjudication depend on assignment, scope and validity. |
| C-23 | Both context relations are exported independently | Same-pair `analyzedInContext` implication to `hasContext` is reserved for a reviewed rule/axiom; no unsupported global subproperty claim is made here. |
| C-24 | Revision relations and local end bounds | Join coherence, irreflexivity, acyclicity and ordering need reviewed data rules; no OWL acyclicity claim. |
| C-25 | Version-target properties and ranges | Coherence between a version and its corresponding artifact kind is a version join, requiring separate validation. |

## Review and remaining gates

The generated graph is parsed and its expected terms and axiom patterns are checked in `tests/test_owl_mapping.py`. Those tests detect omitted elements, reversed cardinalities, accidental boundary promotion, unexpected covering/disjointness, stale inputs and a changed native relation end. The syntax pass is performed with the pinned RDFLib dependency; it is not an OWL 2 DL profile classification or a HermiT run. Issue #4 must test consistency, satisfiability, entailment and non-entailment with exact imports and runtime. Issue #5 must test explicit-data obligations using declared SHACL profiles. Issue #6 must connect the resulting evidence to requirements and competency questions.
