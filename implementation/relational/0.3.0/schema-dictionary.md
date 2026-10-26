# Assessment correction overlay dictionary

Profile 0.3.0 adds one application metadata table to public SQLite schema v3, producing schema v4. Existing tables, guards, native predicates and payloads are unchanged. `assessment_correction` has the functional dependency `corrected_version_id → prior_version_id, reason, recorded_at, source_record_id`. The stable assessment identity is joined through the existing snapshots rather than duplicated.

| Column | Constraint | Meaning |
| --- | --- | --- |
| corrected_version_id | Required primary key; FK to assessment_snapshot | An issued corrected assessment version. One declaration per corrected version. |
| prior_version_id | Required FK to assessment_snapshot; distinct from child | Issued predecessor of the same assessment artifact. Multiple children are permitted. |
| reason | Required nonblank text | Supplied explanation; not an automatically verified judgment. |
| recorded_at | Required canonical UTC calendar text | Declaration timestamp, no earlier than either assessment's recorded timestamp. No general interval or causal-order semantics. |
| source_record_id | Required FK to source_record | Provenance of the correction declaration, distinct from the assessment/result source qualifiers. |

The primary key supports child lookup. `correction_parent` supports descendant traversal and parent-FK checks. `correction_source` supports source-FK checks and provenance retrieval. No extra assessment-identity or label index is needed. This is a selected FD/index review, not a universal normalization or performance claim.

Insert guards check issued roles, same assessment identity, time, duplicate replacement and cycles. Update/delete guards freeze declarations; original version/assessment/result guards freeze issued payloads. Restore health checks repeat semantic joins and cycle checks because restored rows are inserted before triggers. Schema and migration ledger hashes are also checked.

Administrative DDL/PRAGMA bypass is outside the writer guarantee. A valid-looking rewrite of a reason cannot be authenticated as truthful by SQL, even if a missing guard or cross-identity graph can be detected. The source/oracle receipt and human governance remain necessary.
