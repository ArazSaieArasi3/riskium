# Candidate catalog associations

Candidate **0.3.2-structural.2**; not the published current dictionary. Source SHA-256: `c1556811a468919b75521d1a93b8ef8f91c24bf2799deae274b1d211d5e4d5b7`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

All 137 catalog associations are listed; 130 are typed-core relations. The remaining seven retain their optional-boundary scope.

| ID | Source | Predicate | Target | Source-end | Target-end | Layer |
|---|---|---|---|---|---|---|
| R-01 | [Risk Register Entry](RKM-C022.md) | recordsAbout | [Risk Case](RKM-X01.md) | 0..* | 1 | FORMAL_CORE |
| R-02 | [Entry Revision](RKM-C023.md) | hasDescription | [Risk Description](RKM-C024.md) | 1 | 0..* | FORMAL_CORE |
| R-03 | [Classification Assertion](RKM-C020.md) | classifies | [Risk Case](RKM-X01.md) | 0..* | 1 | FORMAL_CORE |
| R-04 | [Classification Assertion](RKM-C020.md) | selectsTerm | [Classification Term](RKM-C019.md) | 0..* | 1 | FORMAL_CORE |
| R-05 | [Classification Term](RKM-C019.md) | belongsToScheme | [Classification Scheme](RKM-C018.md) | 0..* | 1 | FORMAL_CORE |
| R-06 | [Classification Term](RKM-C019.md) | hasBroaderTerm | [Classification Term](RKM-C019.md) | 0..* | 0..* | FORMAL_CORE |
| R-07 | [Identification Information](RKM-C026.md) | identifiedRisk | [Risk Case](RKM-X01.md) | 0..* | 1 | FORMAL_CORE |
| R-08 | [Identification Information](RKM-C026.md) | hasParticipantReference | [Actor Reference](RKM-C050.md) | 0..* | 0..* | FORMAL_CORE |
| R-09 | [Responsibility Assignment Information](RKM-C051.md) | assignmentAbout | [Risk Case](RKM-X01.md) | 0..* | 1 | FORMAL_CORE |
| R-10 | [Responsibility Assignment Information](RKM-C051.md) | hasBearerReference | [Actor Reference](RKM-C050.md) | 0..* | 1 | FORMAL_CORE |
| R-11 | [Assessment Information](RKM-C032.md) | assesses | [Risk Case](RKM-X01.md) | 0..* | 1 | FORMAL_CORE |
| R-12 | [Assessment Information](RKM-C032.md) | hasBasis | [Assessment Basis](RKM-C033.md) | 0..* | 1 | FORMAL_CORE |
| R-13 | [Assessment Information](RKM-C032.md) | hasDimensionResult | [Dimension Assessment Result](RKM-C034.md) | 1 | 0..* | FORMAL_CORE |
| R-14 | [Dimension Assessment Result](RKM-C034.md) | usesScale | [Assessment Scale](RKM-C036.md) | 0..* | 0..1 | FORMAL_CORE |
| R-15 | [Dimension Assessment Result](RKM-C034.md) | selectsLevel | [Assessment Scale Level](RKM-C038.md) | 0..* | 0..1 | FORMAL_CORE |
| R-16 | [Assessment Scale Level](RKM-C038.md) | levelOf | [Assessment Scale](RKM-C036.md) | 0..* | 1 | FORMAL_CORE |
| R-17 | [Assessment Information](RKM-C032.md) | hasScoreResult | [Risk Score Result](RKM-C037.md) | 1 | 0..* | FORMAL_CORE |
| R-18 | [Risk Score Result](RKM-C037.md) | derivedFrom | [Dimension Assessment Result](RKM-C034.md) | 0..* | 0..* | FORMAL_CORE |
| R-19 | [Treatment Decision Information](RKM-C041.md) | decisionAbout | [Risk Case](RKM-X01.md) | 0..* | 1 | FORMAL_CORE |
| R-20 | [Treatment Decision Information](RKM-C041.md) | selectsStrategy | [Treatment Strategy Term](RKM-C042.md) | 0..* | 1 | FORMAL_CORE |
| R-21 | [Plan Specification](RKM-C043.md) | planAbout | [Risk Case](RKM-X01.md) | 0..* | 1..* | FORMAL_CORE |
| R-22 | [Consequence Statement](RKM-C025.md) | statementAbout | [Risk Case](RKM-X01.md) | 0..* | 1 | FORMAL_CORE |
| R-23 | [Entry Revision](RKM-C023.md) | hasStateAssertion | [Record State Assertion](RKM-C062.md) | 1 | 0..* | FORMAL_CORE |
| R-24 | [Entry Revision](RKM-C023.md) | hasTag | [Tag](RKM-C021.md) | 0..* | 0..* | FORMAL_CORE |
| R-25 | [Risk Scenario Specification](RKM-C003.md) | mayBeRealizedBy | [Risk Occurrence](RKM-C004.md) | 0..* | 0..* | FORMAL_CORE |
| R-26 | [Assessment Activity](RKM-C031.md) | producesAssessmentInformation | [Assessment Information](RKM-C032.md) | 0..* | 0..* | FORMAL_CORE |
| R-27 | [Identification Information](RKM-C026.md) | declaresIntakeChannel | [Intake Channel Term](RKM-C027.md) | 0..* | 0..* | FORMAL_CORE |
| R-28 | [Entry Revision](RKM-C023.md) | documentsAssessment | [Assessment Information](RKM-C032.md) | 1..* | 0..* | FORMAL_CORE |
| R-29 | [Entry Revision](RKM-C023.md) | documentsClassification | [Classification Assertion](RKM-C020.md) | 1..* | 0..* | FORMAL_CORE |
| R-30 | [Entry Revision](RKM-C023.md) | documentsAssignment | [Responsibility Assignment Information](RKM-C051.md) | 1..* | 0..* | FORMAL_CORE |
| R-31 | [Record State Assertion](RKM-C062.md) | declaresAnalysisState | [Analysis State Term](RKM-C060.md) | 0..* | 0..1 | FORMAL_CORE |
| R-32 | [Record State Assertion](RKM-C062.md) | declaresWorkflowState | [Workflow State Term](RKM-C061.md) | 0..* | 0..1 | FORMAL_CORE |
| R-33 | [Entry Revision](RKM-C023.md) | revisionOf | [Risk Register Entry](RKM-C022.md) | 0..* | 1 | FORMAL_CORE |
| R-34 | [Entry Revision](RKM-C023.md) | previousRevision | [Entry Revision](RKM-C023.md) | 0..* | 0..1 | FORMAL_CORE |
| R-35 | [Risk Case](RKM-X01.md) | analyzedInContext | [Risk Context Specification](RKM-C002.md) | 0..* | 0..* | FORMAL_CORE |
| R-36 | [Risk Scenario Specification](RKM-C003.md) | scenarioAbout | [Risk Case](RKM-X01.md) | 0..* | 1..* | FORMAL_CORE |
| R-37 | [Risk Description](RKM-C024.md) | expressesScenario | [Risk Scenario Specification](RKM-C003.md) | 0..* | 0..* | FORMAL_CORE |
| R-38 | [Entry Revision](RKM-C023.md) | recordsConsequence | [Consequence Statement](RKM-C025.md) | 1 | 0..* | FORMAL_CORE |
| R-39 | [Risk Description](RKM-C024.md) | descriptionRole | [Description Role Term](RKM-C028.md) | 0..* | 1 | FORMAL_CORE |
| R-40 | [Consequence Statement](RKM-C025.md) | sourceSlot | [Consequence Slot Term](RKM-C029.md) | 0..* | 1 | FORMAL_CORE |
| R-41 | [Risk Nature Assertion](RKM-C005.md) | natureOf | [Risk Case](RKM-X01.md) | 0..* | 1 | FORMAL_CORE |
| R-42 | [Risk Nature Assertion](RKM-C005.md) | declaresNature | [Nature Term](RKM-C006.md) | 0..* | 1 | FORMAL_CORE |
| R-43 | [Risk Nature Assertion](RKM-C005.md) | natureInContext | [Risk Context Specification](RKM-C002.md) | 0..* | 0..1 | FORMAL_CORE |
| R-44 | [Entry Revision](RKM-C023.md) | recordsNature | [Risk Nature Assertion](RKM-C005.md) | 1..* | 0..* | FORMAL_CORE |
| R-45 | [Assessment Information](RKM-C032.md) | assessmentContext | [Risk Context Specification](RKM-C002.md) | 0..* | 0..1 | FORMAL_CORE |
| R-46 | [Assessment Information](RKM-C032.md) | usesMethod | [Assessment Method Specification](RKM-C035.md) | 0..* | 0..1 | FORMAL_CORE |
| R-47 | [Assessment Information](RKM-C032.md) | epistemicStatus | [Epistemic Status Term](RKM-C040.md) | 0..* | 0..1 | FORMAL_CORE |
| R-48 | [Dimension Assessment Result](RKM-C034.md) | dimension | [Assessment Dimension](RKM-C039.md) | 0..* | 1 | FORMAL_CORE |
| R-49 | [Assessment Method Specification](RKM-C035.md) | permitsScale | [Assessment Scale](RKM-C036.md) | 0..* | 0..* | FORMAL_CORE |
| R-50 | [Risk Score Result](RKM-C037.md) | scoreMethod | [Assessment Method Specification](RKM-C035.md) | 0..* | 1 | FORMAL_CORE |
| R-51 | [Assessment Activity](RKM-C031.md) | assessmentPerformer | [Agent](RKM-C047.md) | 0..* | 0..* | FORMAL_CORE |
| R-52 | [Entry Revision](RKM-C023.md) | recordsIdentification | [Identification Information](RKM-C026.md) | 1..* | 0..* | FORMAL_CORE |
| R-53 | [Actor Reference](RKM-C050.md) | resolvesToAgent | [Agent](RKM-C047.md) | 0..* | 0..1 | FORMAL_CORE |
| R-54 | [Responsibility Assignment Information](RKM-C051.md) | assignmentRole | [Responsibility Role Term](RKM-C059.md) | 0..* | 1 | FORMAL_CORE |
| R-55 | [Responsibility Assignment Information](RKM-C051.md) | documentsActualMandate | [Responsibility Relator](RKM-C052.md) | 0..* | 0..1 | FORMAL_CORE |
| R-56 | [Responsibility Relator](RKM-C052.md) | mediatesBearer | [Responsible Agent Role](RKM-C053.md) | 1..* | 1 | FORMAL_CORE |
| R-57 | [Responsibility Relator](RKM-C052.md) | mediatesAuthority | [Authorizing Agent Role](RKM-C054.md) | 1..* | 1 | FORMAL_CORE |
| R-58 | [Responsibility Relator](RKM-C052.md) | mandateAbout | [Risk Case](RKM-X01.md) | 0..* | 1..* | FORMAL_CORE |
| R-59 | [Responsibility Relator](RKM-C052.md) | mandateRole | [Responsibility Role Term](RKM-C059.md) | 0..* | 1 | FORMAL_CORE |
| R-60 | [Entry Revision](RKM-C023.md) | recordsDecision | [Treatment Decision Information](RKM-C041.md) | 1..* | 0..* | FORMAL_CORE |
| R-61 | [Entry Revision](RKM-C023.md) | recordsPlan | [Plan Specification](RKM-C043.md) | 1..* | 0..* | FORMAL_CORE |
| R-62 | [Plan Specification](RKM-C043.md) | planRole | [Plan Role Term](RKM-C046.md) | 0..* | 1 | FORMAL_CORE |
| R-63 | [Treatment Decision Information](RKM-C041.md) | isSpecifiedByPlan | [Plan Specification](RKM-C043.md) | 0..* | 0..* | FORMAL_CORE |
| R-64 | [Treatment Activity](RKM-C044.md) | executesPlan | [Plan Specification](RKM-C043.md) | 0..* | 0..* | FORMAL_CORE |
| R-65 | [Treatment Activity](RKM-C044.md) | treatmentPerformer | [Agent](RKM-C047.md) | 0..* | 0..* | FORMAL_CORE |
| R-66 | [Treatment Activity](RKM-C044.md) | implementsControl | [Risk Control](RKM-C045.md) | 0..* | 0..* | OPTIONAL_EXTERNAL_BRIDGE |
| R-67 | [Risk Control](RKM-C045.md) | controlAddressing | [Risk Case](RKM-X01.md) | 0..* | 0..* | OPTIONAL_EXTERNAL_BRIDGE |
| R-68 | [Evidence Reference](RKM-C065.md) | supportsRecordedArtifact | [Information Artifact](RKM-C014.md) | 0..* | 1..* | FORMAL_CORE |
| R-69 | [Evidence Reference](RKM-C065.md) | refersToOccurrence | [Risk Occurrence](RKM-C004.md) | 0..* | 0..* | FORMAL_CORE |
| R-70 | [Evidence Reference](RKM-C065.md) | refersToAgent | [Agent](RKM-C047.md) | 0..* | 0..* | FORMAL_CORE |
| R-71 | [Evidence Reference](RKM-C065.md) | refersToAssessmentActivity | [Assessment Activity](RKM-C031.md) | 0..* | 0..* | FORMAL_CORE |
| R-72 | [Evidence Reference](RKM-C065.md) | refersToTreatmentActivity | [Treatment Activity](RKM-C044.md) | 0..* | 0..* | FORMAL_CORE |
| RX-001 | [Risk Case](RKM-X01.md) | hasContext | [Risk Context Specification](RKM-C002.md) | 0..* | 1..* | FORMAL_CORE |
| RX-002 | [Risk Case](RKM-X01.md) | appliesPattern | [Risk Pattern Specification](RKM-C001.md) | 0..* | 0..* | FORMAL_CORE |
| RX-003 | [Risk Case](RKM-X01.md) | concernsObjective | [Objective Reference](RKM-X02.md) | 0..* | 1..* | FORMAL_CORE |
| RX-004 | [Uncertainty Statement](RKM-X03.md) | uncertaintyAbout | [Risk Case](RKM-X01.md) | 0..* | 1 | FORMAL_CORE |
| RX-005 | [Risk Case](RKM-X01.md) | hasSource | [Risk Source](RKM-C007.md) | 0..* | 0..* | OPTIONAL_EXTERNAL_BRIDGE |
| RX-006 | [Artifact Version](RKM-C015.md) | versionOf | [Information Artifact](RKM-C014.md) | 0..* | 1 | FORMAL_CORE |
| RX-007 | [Artifact Version](RKM-C015.md) | expressesContent | [Information Content](RKM-C016.md) | 0..* | 1..* | FORMAL_CORE |
| RX-008 | [Risk Register Entry](RKM-C022.md) | memberOfRegister | [Risk Register](RKM-C030.md) | 0..* | 1 | FORMAL_CORE |
| RX-009 | [Risk Scenario Specification](RKM-C003.md) | hasPossibleConsequenceStatement | [Consequence Statement](RKM-C025.md) | 0..* | 0..* | FORMAL_CORE |
| RX-010 | [Consequence Statement](RKM-C025.md) | refersToActualOutcome | [Consequence](RKM-C010.md) | 0..* | 0..1 | OPTIONAL_EXTERNAL_BRIDGE |
| RX-011 | [Risk Evaluation Outcome](RKM-X04.md) | evaluatesCase | [Risk Case](RKM-X01.md) | 0..* | 1 | FORMAL_CORE |
| RX-012 | [Risk Evaluation Outcome](RKM-X04.md) | usesAssessment | [Assessment Information](RKM-C032.md) | 0..* | 1..* | FORMAL_CORE |
| RX-013 | [Risk Evaluation Outcome](RKM-X04.md) | usesCriteriaVersion | [Artifact Version](RKM-C015.md) | 0..* | 1 | FORMAL_CORE |
| RX-014 | [Assessment Information](RKM-C032.md) | usesContextVersion | [Artifact Version](RKM-C015.md) | 0..* | 1 | FORMAL_CORE |
| RX-015 | [Assessment Information](RKM-C032.md) | usesMethodVersion | [Artifact Version](RKM-C015.md) | 0..* | 0..1 | FORMAL_CORE |
| RX-016 | [Dimension Assessment Result](RKM-C034.md) | usesScaleVersion | [Artifact Version](RKM-C015.md) | 0..* | 0..1 | FORMAL_CORE |
| RX-017 | [Risk Criteria](RKM-C072.md) | criteriaForContext | [Risk Context Specification](RKM-C002.md) | 0..* | 1..* | FORMAL_CORE |
| RX-018 | [Risk Criteria](RKM-C072.md) | considersAppetiteStatement | [Risk Appetite Statement](RKM-C073.md) | 0..* | 0..* | FORMAL_CORE |
| RX-019 | [Risk Criteria](RKM-C072.md) | considersToleranceStatement | [Risk Tolerance Statement](RKM-C074.md) | 0..* | 0..* | FORMAL_CORE |
| RX-020 | [Control Reference](RKM-X05.md) | resolvesToControl | [Risk Control](RKM-C045.md) | 0..* | 0..1 | OPTIONAL_EXTERNAL_BRIDGE |
| RX-021 | [Evidence Reference](RKM-C065.md) | pointsToEvidence | [Evidence Item](RKM-C066.md) | 1..* | 1 | FORMAL_CORE |
| RX-022 | [Observation Activity](RKM-C067.md) | producesObservation | [Observation Result](RKM-C068.md) | 1 | 0..* | FORMAL_CORE |
| RX-023 | [Observation Result](RKM-C068.md) | reportsIndicator | [Indicator](RKM-C069.md) | 0..* | 1 | FORMAL_CORE |
| RX-024 | [Observation Result](RKM-C068.md) | observesCase | [Risk Case](RKM-X01.md) | 0..* | 1 | FORMAL_CORE |
| RX-025 | [Threshold](RKM-C070.md) | thresholdForIndicator | [Indicator](RKM-C069.md) | 0..* | 0..1 | FORMAL_CORE |
| RX-026 | [Signal](RKM-C071.md) | basedOnObservation | [Observation Result](RKM-C068.md) | 0..* | 1..* | FORMAL_CORE |
| RX-027 | [Signal](RKM-C071.md) | evaluatedAgainstThreshold | [Threshold](RKM-C070.md) | 0..* | 0..* | FORMAL_CORE |
| RX-028 | [Signal](RKM-C071.md) | promptsReviewOf | [Risk Case](RKM-X01.md) | 0..* | 0..* | FORMAL_CORE |
| RX-029 | [Workflow Assignment](RKM-C064.md) | assignsState | [Workflow State Term](RKM-C061.md) | 0..* | 1 | FORMAL_CORE |
| RX-030 | [Workflow Assignment](RKM-C064.md) | underSchemeVersion | [Workflow Scheme Version](RKM-C063.md) | 0..* | 1 | FORMAL_CORE |
| RX-031 | [Workflow Assignment](RKM-C064.md) | assignmentForRevision | [Entry Revision](RKM-C023.md) | 0..* | 1 | FORMAL_CORE |
| RX-032 | [Record State Assertion](RKM-C062.md) | documentsWorkflowAssignment | [Workflow Assignment](RKM-C064.md) | 0..* | 0..1 | FORMAL_CORE |
| RK2-001 | [Risk Context Specification](RKM-C002.md) | refersToCondition | [Predisposing Condition](RKM-C008.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-002 | [Risk Context Specification](RKM-C002.md) | refersToVulnerability | [Vulnerability](RKM-C011.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-003 | [Risk Context Specification](RKM-C002.md) | refersToExposure | [Exposure](RKM-C012.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-004 | [Risk Case](RKM-X01.md) | hasEstablishedState | [Risk State](RKM-C013.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-005 | [Risk Occurrence](RKM-C004.md) | initiatedBy | [Trigger](RKM-C009.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-006 | [Risk Occurrence](RKM-C004.md) | hasEstablishedConsequence | [Consequence](RKM-C010.md) | 0..* | 0..* | OPTIONAL_EXTERNAL_BRIDGE |
| RK2-007 | [Risk Description](RKM-C024.md) | describesCase | [Risk Case](RKM-X01.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-008 | [Risk Description](RKM-C024.md) | describesPattern | [Risk Pattern Specification](RKM-C001.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-009 | [Risk Description](RKM-C024.md) | descriptionContext | [Risk Context Specification](RKM-C002.md) | 0..* | 0..1 | FORMAL_CORE |
| RK2-010 | [Risk Scenario Specification](RKM-C003.md) | scenarioContext | [Risk Context Specification](RKM-C002.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-011 | [Risk Context Specification](RKM-C002.md) | referencesObjective | [Objective Reference](RKM-X02.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-012 | [Uncertainty Statement](RKM-X03.md) | uncertaintyContext | [Risk Context Specification](RKM-C002.md) | 0..* | 0..1 | FORMAL_CORE |
| RK2-013 | [Assessment Information](RKM-C032.md) | recordsUncertainty | [Uncertainty Statement](RKM-X03.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-014 | [Treatment Decision Information](RKM-C041.md) | basedOnEvaluation | [Risk Evaluation Outcome](RKM-X04.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-015 | [Treatment Decision Information](RKM-C041.md) | recordsRemainingRiskAssessment | [Assessment Information](RKM-C032.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-016 | [Entry Revision](RKM-C023.md) | recordsControlReference | [Control Reference](RKM-X05.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-017 | [Entry Revision](RKM-C023.md) | recordsObservation | [Observation Result](RKM-C068.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-018 | [Assessment Method Specification](RKM-C035.md) | specifiesDimension | [Assessment Dimension](RKM-C039.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-019 | [Assessment Scale](RKM-C036.md) | scaleForDimension | [Assessment Dimension](RKM-C039.md) | 0..* | 1 | FORMAL_CORE |
| RK2-020 | [Threshold](RKM-C070.md) | thresholdOnScale | [Assessment Scale](RKM-C036.md) | 0..* | 0..1 | FORMAL_CORE |
| RK2-021 | [Workflow State Term](RKM-C061.md) | availableInWorkflowScheme | [Workflow Scheme Version](RKM-C063.md) | 0..* | 1..* | FORMAL_CORE |
| RK2-022 | [Assessment Basis](RKM-C033.md) | referencesControlBaseline | [Control Reference](RKM-X05.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-023 | [Risk Appetite Statement](RKM-C073.md) | appetiteContext | [Risk Context Specification](RKM-C002.md) | 0..* | 1..* | FORMAL_CORE |
| RK2-024 | [Risk Tolerance Statement](RKM-C074.md) | toleranceContext | [Risk Context Specification](RKM-C002.md) | 0..* | 1..* | FORMAL_CORE |
| RK2-025 | [Responsibility Assignment Information](RKM-C051.md) | authorizerReference | [Actor Reference](RKM-C050.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-026 | [Observation Result](RKM-C068.md) | observationContext | [Risk Context Specification](RKM-C002.md) | 0..* | 0..1 | FORMAL_CORE |
| RK3-001 | [Risk Case](RKM-X01.md) | hasSourceReference | [Risk Source Reference](RKM-X06.md) | 0..* | 0..* | FORMAL_CORE |
| RK3-002 | [Risk Source Reference](RKM-X06.md) | resolvesToSource | [Risk Source](RKM-C007.md) | 0..* | 0..1 | OPTIONAL_EXTERNAL_BRIDGE |
| RK3-003 | [Risk Source Reference](RKM-X06.md) | sourceReferenceContext | [Risk Context Specification](RKM-C002.md) | 0..* | 0..1 | FORMAL_CORE |
| RK3-004 | [External Object](EXT-OBJECT.md) | bearsVulnerability | [Vulnerability](RKM-C011.md) | 1 | 0..* | FORMAL_CORE |
| RE-001 | [Evidence Use Relator](RKM-C075.md) | mediatesEvidenceItem | [Evidence Item](RKM-C066.md) | 1..* | 1 | FORMAL_CORE |
| RE-002 | [Evidence Use Relator](RKM-C075.md) | mediatesEvidenceReference | [Evidence Reference Role](RKM-C076.md) | 1..* | 1 | FORMAL_CORE |
| RE-003 | [Evidence Use Relator](RKM-C075.md) | groundedInUseRecord | [Information Artifact](RKM-C014.md) | 0..* | 1 | FORMAL_CORE |
