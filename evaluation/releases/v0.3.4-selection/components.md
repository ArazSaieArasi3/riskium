# Selected components for v0.3.4

**COMPONENT_SELECTION_NOT_FROZEN** — child #47 under #45. No new snapshot, stable profile, tag, assets or publication request is created. Stable remains v0.3.3.

[Machine-readable selection](../../../releases/selection-v0.3.4.json) · [Declared policy](../../../releases/selection-policy-v0.3.4.json) · [Successor overlay](../../../releases/development-components-v0.3.4.json).

| Component | Version | Change | Direct declared prerequisites | Selected file entries |
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
| CONSISTENCY | 0.2.0 | REPLACED | MODEL 0.3.1, ORSD 0.4.3, OWNER 0.1.0, MANUSCRIPT 7.0.8, ASSESSMENT_CORRECTION 0.3.0 | 8 |
| SOURCE_SCENARIO | 0.4.0 | ADDED | ASSESSMENT_CORRECTION 0.3.0, DATABASE_REQUIREMENTS 0.1.0 | 29 |
| SOURCE_SCENARIO_LINEAGE | 0.5.0 | ADDED | SOURCE_SCENARIO 0.4.0 | 29 |
| QUALIFIED_EVIDENCE | 0.6.0 | ADDED | SOURCE_SCENARIO_LINEAGE 0.5.0 | 28 |
| DOCUMENTATION | 0.3.0 | REPLACED | MODEL 0.3.1, CONSISTENCY 0.2.0, FORMAL_REFERENCE 0.1.0, WEBVOWL 0.1.0, SOURCE_SCENARIO 0.4.0, SOURCE_SCENARIO_LINEAGE 0.5.0, QUALIFIED_EVIDENCE 0.6.0 | 143 |

There are 27 selected components: 22 retained, two revised and three added. Duplicate shared file paths must bind identical bytes; the union is hashed once and records all owners. The declared prerequisite graph has 59 edges and is ordered before dependents. It is not a complete runtime/static code ontology.

## SQLite reader and migration chain

| Profile | Schema transition | Reader |
| --- | --- | --- |
| RELATIONAL 0.1.0 | 0 → 2 | tools/relational_history.py |
| RELATIONAL_ASSESSMENT 0.2.0 | 2 → 3 | tools/relational_assessment.py |
| ASSESSMENT_CORRECTION 0.3.0 | 3 → 4 | tools/relational_correction.py |
| SOURCE_SCENARIO 0.4.0 | 4 → 5 | tools/relational_source_scenario.py |
| SOURCE_SCENARIO_LINEAGE 0.5.0 | 5 → 6 | tools/relational_source_scenario_lineage.py |
| QUALIFIED_EVIDENCE 0.6.0 | 6 → 7 | tools/relational_evidence.py |

Each step pins selected SQL/reader source hashes and the original ledger digest(s). This is compatibility/selection validation; it is not a new populated database or PostgreSQL/private migration execution. Older exact-schema readers still reject newer schemas. Original executed SQL receipts remain source-bound.

## Consistency and future gates

CONSISTENCY advances from 0.1.0 to 0.2.0 because current routing/input-binding metadata changed during #46. The original 423 rows are identical; [comparison](../../consistency/current-0.2.0/source-comparison.json) preserves the old source and explicitly lists the four changed top-level metadata keys. DOCUMENTATION advances from frozen 0.2.0 to completed current 0.3.0. Previous release matrices and component bytes are not rewritten.

The documentation component and its 23-file Wiki/243-body HTTP receipts remain the completed #46 checkpoint. Those receipts do not establish freshness for a later source freeze. The next action under #45 is a new documentation snapshot, followed by explicit selection refresh/final-source checks, freeze and independently verified publication. Model 0.3.1, ORSD 0.4.3, original DRSD 0.1.0 and article 7.0.8 remain unchanged; all eleven admissions stay WITHHELD and independent ratings remain zero.
