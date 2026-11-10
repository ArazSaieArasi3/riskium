# source constraints

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

These 26 source statements are not all executable OWL or SHACL rules. Their source status and statement are preserved below; engine-specific coverage stays in the execution receipts.

## C-01 · Risk Case is not ISO Risk

Source status: `DESIGN_CONSTRAINT`.

Case identity is preserved across descriptions, scores, owners and administrative states. Equal labels do not establish case identity.

## C-02 · No realization from description

Source status: `DESIGN_CONSTRAINT`.

A scenario, consequence statement, signal, plan or report alone must not create actual occurrences, outcomes, controls or effectiveness assertions.

## C-03 · Issued version immutability

Source status: `DESIGN_CONSTRAINT`.

Issued semantic content and effective dependency versions are immutable. Correction and supersession create lineage-preserving new versions.

## C-04 · Assessment interpretation

Source status: `DESIGN_CONSTRAINT`.

Results retain method/scale version, dimension, basis, relevant context and time semantics. A score is not the risk, and estimated likelihood need not be numeric.

## C-05 · Temporal and administrative distinction

Source status: `DESIGN_CONSTRAINT`.

Recorded time, reference time and validity intervals are distinct. Workflow closure does not prove risk cessation or successful treatment.

## C-06 · Relator participant distinctness

Source status: `IMPLEMENTED_CONDITIONAL_CONTRACT`.

An asserted ResponsibilityRelator requires at least two distinct mediated individuals. If bearer and authority resolve to one actor and no further grounding exists, retain ResponsibilityAssignmentInformation without asserting the relator.

## C-07 · Role-qualified ownership

Source status: `DESIGN_CONSTRAINT`.

ResponsibleAgentRole does not automatically mean Risk Owner. Ownership mapping requires recorded responsibility type, accountability, authority and applicable context.

## C-08 · Threshold anchor

Source status: `DESIGN_CONSTRAINT`.

At least one of thresholdForIndicator or thresholdOnScale is present. If both are present, their scale/unit interpretation is compatible. Qualitative boundaries use scale semantics rather than invented numeric units.

## C-09 · Description aboutness

Source status: `PROFILE_CONSTRAINT`.

Every published RiskDescription has at least one case, pattern or scenario target. Multiple valid targets are permitted and require explicit interpretation.

## C-10 · Framework-qualified tolerance

Source status: `DESIGN_CONSTRAINT`.

Tolerance statements retain source framework/version, original meaning and context. Permissible deviation is not automatically equivalent to readiness to bear remaining risk.

## C-11 · Vocabulary resource identity

Source status: `DESIGN_CONSTRAINT`.

Vocabulary resources retain scheme-qualified identity. Labels are representations and are not OWL classes by default.

## C-12 · Evidence does not endorse

Source status: `DESIGN_CONSTRAINT`.

EvidenceReference states an evidential role such as support, challenge or context. Linking a source does not automatically prove the target claim.

## C-13 · Scale and dimension compatibility

Source status: `PROFILE_CONSTRAINT`.

A selected level belongs to the selected scale version and dimension. Results on incompatible methods/scales are not ranked merely by equal labels or numeric codes.

## C-14 · Heterogeneous boundaries

Source status: `IMPLEMENTED_DESIGN_BOUNDARY`.

RiskSource, Consequence and RiskControl remain catalog notions and optional external boundaries, excluded from native formal-core class assertions. Source, outcome and control content is represented by RiskSourceReference, ConsequenceStatement and ControlReference.

## C-15 · Intrinsic vulnerability bearer

Source status: `APPROVED_PROFILE_CONTRACT`.

Every asserted intrinsic Vulnerability has exactly one substantial-endurant bearer. A reported hypothesis alone is information, not an actual mode.

## C-16 · Admission profiles

Source status: `APPROVED_PROFILE_CONTRACT`.

Raw source content is retained in staging. Managed documentary records require their own identity, aboutness, title and provenance under the declared record profile. Analytical task readiness additionally requires the context, method, scale, basis, dimension and time selected for that task. These completeness conditions do not make organizational register approval a universal condition for the existence of an identifiable analytical RiskCase.

## C-17 · Multiple assertions

Source status: `APPROVED_PROFILE_CONTRACT`.

Multiple classifications, descriptions, actors and evidence assertions are retained with role, context, provenance and time. Scalar export requires an explicit selection rule when several values apply.

## C-18 · Comparable assessments

Source status: `APPROVED_PROFILE_CONTRACT`.

Direct comparison requires matching pinned method, scale, dimension, basis and temporal context; a governed explicit transformation may enable a different comparison. Missing data is not zero. Reported scores do not imply a reproducible computation.

## C-19 · Workflow semantics

Source status: `APPROVED_PROFILE_CONTRACT`.

State labels are scheme/version qualified. Transition rules and authority are source-backed content. Missing rule means UNKNOWN; Closed does not imply ceased risk and Treated does not imply effectiveness.

## C-20 · Risk Item vocabulary

Source status: `APPROVED_PROFILE_CONTRACT`.

In the terminology adopted by this profile, Risk Item denotes the managed risk subject modeled as RiskCase. This context-qualified mapping does not equate RiskCase with RiskRegisterEntry, RiskScenarioSpecification, ISO risk or any global Risk Item class.

## C-21 · Reported and computed scores

Source status: `REVIEW_DESIGN_CONSTRAINT_SELECTED_TESTS_ONLY`.

A reported RiskScoreResult may have no derivedFrom links. A computed RiskScoreResult requires at least one linked DimensionAssessmentResult, a pinned method and adequate inputs. The score kind must be recorded.

## C-22 · Responsibility identity

Source status: `REVIEW_DESIGN_CONSTRAINT_SELECTED_TESTS_ONLY`.

Repeated mandates between the same participants are permitted when grounding assignment, responsibility scope or validity differs. Duplicate representations of the same grounded mandate must resolve to one relator identity; participant equality alone is not an identity key.

## C-23 · Context relation coherence

Source status: `REVIEW_DESIGN_CONSTRAINT_SELECTED_TESTS_ONLY`.

Every analyzedInContext link is also a hasContext link for the same RiskCase and RiskContextSpecification. The broader hasContext relation may include non-analysis context.

## C-24 · Revision coherence

Source status: `REVIEW_DESIGN_CONSTRAINT_SELECTED_TESTS_ONLY`.

For each EntryRevision, revisionOf and inherited versionOf identify the same RiskRegisterEntry. previousRevision is irreflexive and acyclic and, when present, relates revisions of the same entry.

## C-25 · Version target coherence

Source status: `REVIEW_DESIGN_CONSTRAINT_SELECTED_TESTS_ONLY`.

usesContextVersion targets a version of RiskContextSpecification; usesMethodVersion a version of AssessmentMethodSpecification; usesScaleVersion a version of AssessmentScale; usesCriteriaVersion a version of RiskCriteria. Artifact-level references, when present, agree with versionOf.

## C-26 · Grounded evidential use

Source status: `ISOLATED_CANDIDATE_CONSTRAINT`.

An EvidenceUseRelator mediates a distinct EvidenceItem and EvidenceReferenceRole, has a grounding use record, and is qualified by context and purpose (support, challenge or context). Its reference points to that item and records that context. An ungrounded citation remains information. Use as evidence does not establish claim truth. Duplicate descriptions of one grounded use preserve its identity.

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
