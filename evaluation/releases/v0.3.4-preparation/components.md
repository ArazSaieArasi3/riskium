# Prepared v0.3.4 distribution components

**COMPONENTS_PREPARED_NOT_FROZEN** — #49 under #45. Stable remains v0.3.3.

[Distribution matrix](../../../releases/distribution-v0.3.4.json) · [Policy](../../../releases/preparation-policy-v0.3.4.json) · [Prepared overlay](../../../releases/prepared-components-v0.3.4.json).

| Component | Version | Change from #47 | Declared direct prerequisites | Files |
| --- | --- | --- | --- | ---: |
| MODEL | 0.3.1 | RETAINED | None | 3 |
| DIAGRAM | model-0.3.1 | RETAINED | MODEL 0.3.1 | 2 |
| ORSD | 0.4.3 | RETAINED | MODEL 0.3.1 | 2 |
| RELATIONAL | 0.1.0 | RETAINED | MODEL 0.3.1 | 4 |
| C08 | 0.6.0 | RETAINED | MODEL 0.3.1 | 2 |
| CQ06 | 0.2.0 | RETAINED | MODEL 0.3.1 | 1 |
| WEBVOWL | 0.1.0 | RETAINED | MODEL 0.3.1 | 4 |
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
| CONSISTENCY | 0.2.0 | RETAINED | MODEL 0.3.1, ORSD 0.4.3, OWNER 0.1.0, MANUSCRIPT 7.0.8, ASSESSMENT_CORRECTION 0.3.0 | 8 |
| SOURCE_SCENARIO | 0.4.0 | RETAINED | ASSESSMENT_CORRECTION 0.3.0, DATABASE_REQUIREMENTS 0.1.0 | 29 |
| SOURCE_SCENARIO_LINEAGE | 0.5.0 | RETAINED | SOURCE_SCENARIO 0.4.0 | 29 |
| QUALIFIED_EVIDENCE | 0.6.0 | RETAINED | SOURCE_SCENARIO_LINEAGE 0.5.0 | 28 |
| DOCUMENTATION | 0.3.0 | RETAINED | MODEL 0.3.1, CONSISTENCY 0.2.0, FORMAL_REFERENCE 0.1.0, WEBVOWL 0.1.0, SOURCE_SCENARIO 0.4.0, SOURCE_SCENARIO_LINEAGE 0.5.0, QUALIFIED_EVIDENCE 0.6.0 | 143 |
| DOCUMENTATION_SNAPSHOT | 0.1.0 | ADDED | MODEL 0.3.1, DOCUMENTATION 0.3.0 | 82 |

All 27 initial component rows are unchanged. The new snapshot adds its exact descriptor, 75 component files and six retained receipt/log files. The 61 declared prerequisite edges describe selection compatibility, not exhaustive runtime/code dependency discovery. Shared paths require identical hashes and retain all owners. The selected union contains 380 unique files, including preparation inputs/tooling and five publication-support sources.

The matrix selects four frozen documentation snapshots, current documentation 0.3.0/model 0.3.1, the canonical additive deployment entrypoint/workflow and the generated live version-index hash. The 311-body HTTP and 23-file Wiki receipts remain dated #48 evidence; final-source readback is still required. Earlier profiles/registers are verified at their original source and are not relabeled as fresh freeze evidence. SQLite schemas 2 through 7, all ten prior releases, model/ORSD/DRSD/manuscript versions, eleven WITHHELD admissions and zero independent ratings remain unchanged.

Next integrate the reviewed release profile/critical screen/notes and this matrix into the exact-source freeze path, run final-source checks/fresh channel evidence and freeze; then publish and independently verify actual assets/tag/Latest and prior preservation before closing #45.
