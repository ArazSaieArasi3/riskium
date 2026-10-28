# Selected components for v0.3.5

**COMPONENT_SELECTION_NOT_FROZEN**. Source remains v0.3.4 published; final profile, selected-source replay, freeze and publication are future gates.

[Exact selection](../../../releases/selection-v0.3.5.json) · [Declared policy](../../../releases/selection-policy-v0.3.5.json).

| Component | Version | Change | Current assembly prerequisites | File entries |
| --- | --- | --- | --- | ---: |
| MODEL | 0.3.1 | RETAINED | None | 3 |
| DIAGRAM | model-0.3.1 | RETAINED | MODEL 0.3.1 | 2 |
| ORSD | 0.4.3 | RETAINED | MODEL 0.3.1 | 2 |
| RELATIONAL | 0.1.0 | RETAINED | MODEL 0.3.1 | 4 |
| C08 | 0.6.0 | RETAINED | MODEL 0.3.1 | 2 |
| CQ06 | 0.2.0 | RETAINED | MODEL 0.3.1 | 1 |
| WEBVOWL | 0.1.0 | RETAINED | MODEL 0.3.1 | 4 |
| DOCUMENTATION_SNAPSHOT | 0.1.0 | RETAINED | MODEL 0.3.1 | 82 |
| OWNER | 0.1.0 | RETAINED | MODEL 0.3.1, ORSD 0.4.3 | 2 |
| COMPARISON | 0.7.0 | RETAINED | MODEL 0.3.1, C08 0.6.0 | 2 |
| CQ0708 | 0.3.0 | RETAINED | MODEL 0.3.1, CQ06 0.2.0 | 1 |
| RELATIONAL_INVENTORY | 0.1.0 | RETAINED | MODEL 0.3.1, RELATIONAL 0.1.0 | 1 |
| EXTENSION_BOUNDARIES | 0.1.0 | RETAINED | MODEL 0.3.1, ORSD 0.4.3 | 1 |
| DATABASE_REQUIREMENTS | 0.1.0 | RETAINED | MODEL 0.3.1, ORSD 0.4.3 | 1 |
| MANUSCRIPT | 7.0.8 | RETAINED | MODEL 0.3.1, ORSD 0.4.3, OWNER 0.1.0 | 1 |
| INTEGRATED_VALIDATION | 0.1.0 | RETAINED | MODEL 0.3.1, C08 0.6.0, COMPARISON 0.7.0 | 6 |
| INDEPENDENT_PROTOCOL | 0.1.0 | RETAINED | MODEL 0.3.1, ORSD 0.4.3, OWNER 0.1.0 | 2 |
| SOURCE_PUBLICATION_REVIEW | 0.1.0 | RETAINED | CQ06 0.2.0, CQ0708 0.3.0 | 1 |
| RELATIONAL_ASSESSMENT | 0.2.0 | RETAINED | RELATIONAL 0.1.0, DATABASE_REQUIREMENTS 0.1.0, C08 0.6.0, COMPARISON 0.7.0 | 18 |
| DATABASE_ASSURANCE | 0.1.0 | RETAINED | RELATIONAL_ASSESSMENT 0.2.0, RELATIONAL_INVENTORY 0.1.0, DATABASE_REQUIREMENTS 0.1.0 | 4 |
| FORMAL_REFERENCE | 0.1.0 | RETAINED | MODEL 0.3.1, ORSD 0.4.3, RELATIONAL_ASSESSMENT 0.2.0 | 2 |
| RIGHTS_AND_MODEL_CITATION | model-0.3.1 | RETAINED | MODEL 0.3.1, MANUSCRIPT 7.0.8 | 8 |
| ASSESSMENT_CORRECTION | 0.3.0 | RETAINED | RELATIONAL_ASSESSMENT 0.2.0, DATABASE_ASSURANCE 0.1.0 | 33 |
| SOURCE_SCENARIO | 0.4.0 | RETAINED | ASSESSMENT_CORRECTION 0.3.0, DATABASE_REQUIREMENTS 0.1.0 | 29 |
| SOURCE_SCENARIO_LINEAGE | 0.5.0 | RETAINED | SOURCE_SCENARIO 0.4.0 | 29 |
| QUALIFIED_EVIDENCE | 0.6.0 | RETAINED | SOURCE_SCENARIO_LINEAGE 0.5.0 | 28 |
| EVIDENCE_REFERENCE_LIFECYCLE | 0.7.0 | ADDED | QUALIFIED_EVIDENCE 0.6.0, DATABASE_REQUIREMENTS 0.1.0 | 40 |
| CONSISTENCY | 0.3.0 | REPLACED | MODEL 0.3.1, ORSD 0.4.3, OWNER 0.1.0, MANUSCRIPT 7.0.8, ASSESSMENT_CORRECTION 0.3.0, SOURCE_SCENARIO 0.4.0, SOURCE_SCENARIO_LINEAGE 0.5.0, QUALIFIED_EVIDENCE 0.6.0, EVIDENCE_REFERENCE_LIFECYCLE 0.7.0 | 479 |
| DOCUMENTATION | 0.4.0 | REPLACED | MODEL 0.3.1, CONSISTENCY 0.3.0, FORMAL_REFERENCE 0.1.0, WEBVOWL 0.1.0, SOURCE_SCENARIO 0.4.0, SOURCE_SCENARIO_LINEAGE 0.5.0, QUALIFIED_EVIDENCE 0.6.0, EVIDENCE_REFERENCE_LIFECYCLE 0.7.0, DOCUMENTATION_SNAPSHOT 0.1.0 | 307 |

29 current components: 26 retained byte-for-byte, two revised and one added. The exact old documentation 0.3 / consistency 0.2 rows and generation dependency slices are archived separately; the frozen snapshot is assembled by copying its original packet, never by silently rebuilding it against current documentation 0.4.

Generated current-site hashes are separate output evidence, not hashes of the preserved docs/current source files. All 23 committed Wiki projections and current descriptor/runtime/input closures are selected. Shared paths must name the same exact bytes; the union records every owner. Migration coverage ends at schema 8, with prior steps unchanged.

No new snapshot, stable profile, release intent, tag, assets, publication, scientific execution, case admission or independent semantic rating is created. Final candidate/channel/critical-screen/freeze/publication checks remain required under #51.
