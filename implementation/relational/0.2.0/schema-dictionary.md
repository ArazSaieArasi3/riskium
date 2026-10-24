# Relational schema dictionary and design review

Actual SQLite PRAGMAs plus authored purpose/FD/dictionary review; not automatic normalization proof.

Table and column counts are inventory, not a quality score. A one-column subtype/key-membership table can be valid when its purpose, key, FK and consumers are explicit. Unexplained tables or undocumented columns are findings. Guarded redundant direct/version assertions are disclosed rather than falsely called a proved normal form.

Summary: {"tables": 16, "columns": 86, "foreign_key_columns": 57, "named_indexes": 40, "one_column_tables": 0, "findings": 0}.

## artifact_typing

Explicit selected concrete native type of an existing generic artifact, with vocabulary keys when applicable.

Declared FD: `artifact_id -> native_class, qualifiers, source`. Conditional scheme/edition/code key applies only to vocabulary members; membership is separate from stable artifact identity.

| Column | Type | Required | Meaning |
| --- | --- | --- | --- |
| artifact_id | TEXT | True | Stable InformationArtifact identity. |
| native_class | TEXT | True | Concrete selected native membership, with an exact model element and no label-derived typing. |
| scheme_uri | TEXT | False | Governed vocabulary scheme IRI; required only for selected vocabulary members. |
| scheme_edition | TEXT | False | Explicit scheme edition IRI; different editions retain distinct keys. |
| local_code | TEXT | False | Nonempty scheme/edition-qualified code; not a bare global identity key. |
| source_record_id | TEXT | True | Exact source_record provenance key for this row. |

Primary key: `artifact_id`. Foreign keys: `[{"id": 0, "sequence": 0, "target_table": "source_record", "column": "source_record_id", "target_column": "record_id", "on_delete": "NO ACTION"}, {"id": 1, "sequence": 0, "target_table": "information_artifact", "column": "artifact_id", "target_column": "artifact_id", "on_delete": "NO ACTION"}]`.

Indexes: `[{"name": "a_fk_artifact_typing_source_record_id", "unique": false, "origin": "c", "columns": ["source_record_id"]}, {"name": "sqlite_autoindex_artifact_typing_3", "unique": true, "origin": "u", "columns": ["scheme_uri", "scheme_edition", "local_code"]}, {"name": "sqlite_autoindex_artifact_typing_2", "unique": true, "origin": "u", "columns": ["artifact_id", "native_class"]}, {"name": "sqlite_autoindex_artifact_typing_1", "unique": true, "origin": "pk", "columns": ["artifact_id"]}]`.

## assessment_snapshot

Version-owned basis, context, method and distinct temporal qualifiers.

Declared FD: `assessment_version_id -> selected role pins, qualifiers, source`. Optional direct references preserve whether a native assertion was supplied; guarded version targets are deliberate constrained redundancy, not an unreviewed latest join.

| Column | Type | Required | Meaning |
| --- | --- | --- | --- |
| assessment_version_id | TEXT | True | Version owning assessment interpretation and result membership. |
| assessment_id | TEXT | True | Stable AssessmentInformation identity. |
| basis_id | TEXT | True | Required native AssessmentBasis assertion. |
| basis_version_id | TEXT | False | Supplementary selected basis version; absence makes strict comparison not ready. |
| context_id | TEXT | False | Optional/direct RiskContextSpecification assertion. |
| context_version_id | TEXT | True | Required pinned issued context version. |
| method_id | TEXT | False | Optional/direct method assertion; absence is not fabricated from a version. |
| method_version_id | TEXT | False | Pinned issued version of AssessmentMethodSpecification. |
| temporal_context_id | TEXT | False | Opaque relevant time-interpretation identity for exact-join policy; not an interval computation. |
| recorded_at | TEXT | True | When the assessment information was recorded; supplied canonical UTC value. |
| reference_at | TEXT | False | Optional reference instant; SQL NULL means unknown. |
| valid_from | TEXT | False | Optional declared validity start; not inferred from recording or issue. |
| valid_to | TEXT | False | Optional declared validity end; simple endpoint order is checked only when both endpoints are supplied. |
| source_record_id | TEXT | True | Exact source_record provenance key for this row. |

Primary key: `assessment_version_id`. Foreign keys: `[{"id": 0, "sequence": 0, "target_table": "source_record", "column": "source_record_id", "target_column": "record_id", "on_delete": "NO ACTION"}, {"id": 1, "sequence": 0, "target_table": "version_snapshot", "column": "method_version_id", "target_column": "version_id", "on_delete": "NO ACTION"}, {"id": 2, "sequence": 0, "target_table": "information_artifact", "column": "method_id", "target_column": "artifact_id", "on_delete": "NO ACTION"}, {"id": 3, "sequence": 0, "target_table": "version_snapshot", "column": "context_version_id", "target_column": "version_id", "on_delete": "NO ACTION"}, {"id": 4, "sequence": 0, "target_table": "information_artifact", "column": "context_id", "target_column": "artifact_id", "on_delete": "NO ACTION"}, {"id": 5, "sequence": 0, "target_table": "version_snapshot", "column": "basis_version_id", "target_column": "version_id", "on_delete": "NO ACTION"}, {"id": 6, "sequence": 0, "target_table": "artifact_typing", "column": "basis_id", "target_column": "artifact_id", "on_delete": "NO ACTION"}, {"id": 7, "sequence": 0, "target_table": "artifact_typing", "column": "assessment_id", "target_column": "artifact_id", "on_delete": "NO ACTION"}, {"id": 8, "sequence": 0, "target_table": "version_snapshot", "column": "assessment_version_id", "target_column": "version_id", "on_delete": "NO ACTION"}]`.

Indexes: `[{"name": "a_fk_assessment_snapshot_assessment_id", "unique": false, "origin": "c", "columns": ["assessment_id"]}, {"name": "a_fk_assessment_snapshot_basis_id", "unique": false, "origin": "c", "columns": ["basis_id"]}, {"name": "a_fk_assessment_snapshot_basis_version_id", "unique": false, "origin": "c", "columns": ["basis_version_id"]}, {"name": "a_fk_assessment_snapshot_context_id", "unique": false, "origin": "c", "columns": ["context_id"]}, {"name": "a_fk_assessment_snapshot_context_version_id", "unique": false, "origin": "c", "columns": ["context_version_id"]}, {"name": "a_fk_assessment_snapshot_method_id", "unique": false, "origin": "c", "columns": ["method_id"]}, {"name": "a_fk_assessment_snapshot_method_version_id", "unique": false, "origin": "c", "columns": ["method_version_id"]}, {"name": "a_fk_assessment_snapshot_source_record_id", "unique": false, "origin": "c", "columns": ["source_record_id"]}, {"name": "sqlite_autoindex_assessment_snapshot_1", "unique": true, "origin": "pk", "columns": ["assessment_version_id"]}]`.

## draft_dependency

Pending version dependency slots belonging to a working draft.

Declared FD: `Primary key -> stored row attributes within the original bounded profile`. Original 0.1.0 dictionary/guards retained; full domain normalization is not inferred from schema inspection.

| Column | Type | Required | Meaning |
| --- | --- | --- | --- |
| draft_id | TEXT | True | Editable staging identity, excluded from native issued-version export. |
| slot | TEXT | True | Application dependency role Context, Method, Scale or Criteria. |
| target_version_id | TEXT | True | Pinned target ArtifactVersion. |
| direct_artifact_id | TEXT | False | Optional explicitly asserted direct target; must agree with versionOf. |

Primary key: `draft_id, slot`. Foreign keys: `[{"id": 0, "sequence": 0, "target_table": "information_artifact", "column": "direct_artifact_id", "target_column": "artifact_id", "on_delete": "NO ACTION"}, {"id": 1, "sequence": 0, "target_table": "version_snapshot", "column": "target_version_id", "target_column": "version_id", "on_delete": "NO ACTION"}, {"id": 2, "sequence": 0, "target_table": "working_draft", "column": "draft_id", "target_column": "draft_id", "on_delete": "CASCADE"}]`.

Indexes: `[{"name": "a_fk_draft_dependency_target_version_id", "unique": false, "origin": "c", "columns": ["target_version_id"]}, {"name": "a_fk_draft_dependency_direct_artifact_id", "unique": false, "origin": "c", "columns": ["direct_artifact_id"]}, {"name": "sqlite_autoindex_draft_dependency_1", "unique": true, "origin": "pk", "columns": ["draft_id", "slot"]}]`.

## identity_registry

Global governed identifier/family registry; display labels never establish identity.

Declared FD: `Primary key -> stored row attributes within the original bounded profile`. Original 0.1.0 dictionary/guards retained; full domain normalization is not inferred from schema inspection.

| Column | Type | Required | Meaning |
| --- | --- | --- | --- |
| resource_id | TEXT | True | Globally unique governed identifier across supported resource families. |
| family | TEXT | True | Enforced local identity family; not inferred from a label. |

Primary key: `resource_id`. Foreign keys: `[]`.

Indexes: `[{"name": "sqlite_autoindex_identity_registry_2", "unique": true, "origin": "u", "columns": ["resource_id", "family"]}, {"name": "sqlite_autoindex_identity_registry_1", "unique": true, "origin": "pk", "columns": ["resource_id"]}]`.

## information_artifact

Stable documentary identity and existing native kind; selected new subtype memberships live separately.

Declared FD: `Primary key -> stored row attributes within the original bounded profile`. Original 0.1.0 dictionary/guards retained; full domain normalization is not inferred from schema inspection.

| Column | Type | Required | Meaning |
| --- | --- | --- | --- |
| artifact_id | TEXT | True | Stable InformationArtifact identity. |
| family | TEXT | True | Enforced local identity family; not inferred from a label. |
| kind | TEXT | True | Original bounded native kind discriminator. |
| label | TEXT | True | Non-unique human display label; not an identity key. |
| source_record_id | TEXT | True | Exact source_record provenance key for this row. |

Primary key: `artifact_id`. Foreign keys: `[{"id": 0, "sequence": 0, "target_table": "identity_registry", "column": "artifact_id", "target_column": "resource_id", "on_delete": "NO ACTION"}, {"id": 0, "sequence": 1, "target_table": "identity_registry", "column": "family", "target_column": "family", "on_delete": "NO ACTION"}, {"id": 1, "sequence": 0, "target_table": "source_record", "column": "source_record_id", "target_column": "record_id", "on_delete": "NO ACTION"}]`.

Indexes: `[{"name": "a_fk_information_artifact_source_record_id", "unique": false, "origin": "c", "columns": ["source_record_id"]}, {"name": "sqlite_autoindex_information_artifact_2", "unique": true, "origin": "u", "columns": ["artifact_id", "kind"]}, {"name": "sqlite_autoindex_information_artifact_1", "unique": true, "origin": "pk", "columns": ["artifact_id"]}]`.

## method_scope

Version-qualified many-to-many permission for method, scale and dimension.

Declared FD: `(method_version_id, scale_id, dimension_id) -> source`. Association table has a composite key and no arbitrary one-column surrogate; version ownership preserves prior permissions.

| Column | Type | Required | Meaning |
| --- | --- | --- | --- |
| method_version_id | TEXT | True | Pinned issued version of AssessmentMethodSpecification. |
| scale_id | TEXT | True | Optional/direct native AssessmentScale assertion, checked against its version. |
| dimension_id | TEXT | True | Governed AssessmentDimension artifact; missing cannot become a default dimension. |
| source_record_id | TEXT | True | Exact source_record provenance key for this row. |

Primary key: `method_version_id, scale_id, dimension_id`. Foreign keys: `[{"id": 0, "sequence": 0, "target_table": "source_record", "column": "source_record_id", "target_column": "record_id", "on_delete": "NO ACTION"}, {"id": 1, "sequence": 0, "target_table": "artifact_typing", "column": "dimension_id", "target_column": "artifact_id", "on_delete": "NO ACTION"}, {"id": 2, "sequence": 0, "target_table": "information_artifact", "column": "scale_id", "target_column": "artifact_id", "on_delete": "NO ACTION"}, {"id": 3, "sequence": 0, "target_table": "version_snapshot", "column": "method_version_id", "target_column": "version_id", "on_delete": "NO ACTION"}]`.

Indexes: `[{"name": "a_fk_method_scope_scale_id", "unique": false, "origin": "c", "columns": ["scale_id"]}, {"name": "a_fk_method_scope_dimension_id", "unique": false, "origin": "c", "columns": ["dimension_id"]}, {"name": "a_fk_method_scope_source_record_id", "unique": false, "origin": "c", "columns": ["source_record_id"]}, {"name": "sqlite_autoindex_method_scope_1", "unique": true, "origin": "pk", "columns": ["method_version_id", "scale_id", "dimension_id"]}]`.

## register_entry

Selected case/register membership with typed references.

Declared FD: `Primary key -> stored row attributes within the original bounded profile`. Original 0.1.0 dictionary/guards retained; full domain normalization is not inferred from schema inspection.

| Column | Type | Required | Meaning |
| --- | --- | --- | --- |
| entry_id | TEXT | True | Register-entry identity or optional selected revision target. |
| entry_kind | TEXT | True | Fixed native entry type used by a composite FK. |
| case_id | TEXT | True | Selected RiskCase identifier. |
| register_id | TEXT | True | Selected RiskRegister artifact. |
| register_kind | TEXT | True | Fixed native register type used by a composite FK. |

Primary key: `entry_id`. Foreign keys: `[{"id": 0, "sequence": 0, "target_table": "information_artifact", "column": "register_id", "target_column": "artifact_id", "on_delete": "NO ACTION"}, {"id": 0, "sequence": 1, "target_table": "information_artifact", "column": "register_kind", "target_column": "kind", "on_delete": "NO ACTION"}, {"id": 1, "sequence": 0, "target_table": "information_artifact", "column": "entry_id", "target_column": "artifact_id", "on_delete": "NO ACTION"}, {"id": 1, "sequence": 1, "target_table": "information_artifact", "column": "entry_kind", "target_column": "kind", "on_delete": "NO ACTION"}, {"id": 2, "sequence": 0, "target_table": "risk_case", "column": "case_id", "target_column": "case_id", "on_delete": "NO ACTION"}]`.

Indexes: `[{"name": "a_fk_register_entry_case_id", "unique": false, "origin": "c", "columns": ["case_id"]}, {"name": "a_fk_register_entry_register_id_register_kind", "unique": false, "origin": "c", "columns": ["register_id", "register_kind"]}, {"name": "sqlite_autoindex_register_entry_1", "unique": true, "origin": "pk", "columns": ["entry_id"]}]`.

## result_snapshot

One qualified result version owned by one assessment version; source, missingness and supplied lexical value stay explicit.

Declared FD: `result_version_id -> result_id, owning assessment version, dimension, selection, source/value qualifiers`. Multiple values use distinct qualified rows, not comma-separated values or an unqualified single scalar; source/version dependencies are explicit.

| Column | Type | Required | Meaning |
| --- | --- | --- | --- |
| result_version_id | TEXT | True | Distinct issued/staged version of the result artifact. |
| result_id | TEXT | True | Stable DimensionAssessmentResult identity; labels/values do not merge it. |
| assessment_version_id | TEXT | True | Version owning assessment interpretation and result membership. |
| dimension_id | TEXT | True | Governed AssessmentDimension artifact; missing cannot become a default dimension. |
| scale_id | TEXT | False | Optional/direct native AssessmentScale assertion, checked against its version. |
| scale_version_id | TEXT | False | Pinned ArtifactVersion of the exact scale, with frozen declared dimension. |
| level_id | TEXT | False | Optional selected AssessmentScaleLevel artifact, bound to its scale version. |
| score_kind | TEXT | True | REPORTED or UNKNOWN; computed claims are explicitly unsupported in this profile. |
| reported_value | TEXT | False | Source lexical text, including literal zero and high-precision spelling; never used as verified arithmetic. |
| source_record_id | TEXT | True | Exact source_record provenance key for this row. |
| source_locator | TEXT | True | Nonempty exact source location for this result assertion. |
| interpretation_origin | TEXT | True | Nonempty attribution of extraction/interpretation; existence is not source truth. |

Primary key: `result_version_id`. Foreign keys: `[{"id": 0, "sequence": 0, "target_table": "source_record", "column": "source_record_id", "target_column": "record_id", "on_delete": "NO ACTION"}, {"id": 1, "sequence": 0, "target_table": "scale_level", "column": "level_id", "target_column": "level_id", "on_delete": "NO ACTION"}, {"id": 2, "sequence": 0, "target_table": "scale_snapshot", "column": "scale_version_id", "target_column": "scale_version_id", "on_delete": "NO ACTION"}, {"id": 3, "sequence": 0, "target_table": "information_artifact", "column": "scale_id", "target_column": "artifact_id", "on_delete": "NO ACTION"}, {"id": 4, "sequence": 0, "target_table": "artifact_typing", "column": "dimension_id", "target_column": "artifact_id", "on_delete": "NO ACTION"}, {"id": 5, "sequence": 0, "target_table": "assessment_snapshot", "column": "assessment_version_id", "target_column": "assessment_version_id", "on_delete": "NO ACTION"}, {"id": 6, "sequence": 0, "target_table": "artifact_typing", "column": "result_id", "target_column": "artifact_id", "on_delete": "NO ACTION"}, {"id": 7, "sequence": 0, "target_table": "version_snapshot", "column": "result_version_id", "target_column": "version_id", "on_delete": "NO ACTION"}]`.

Indexes: `[{"name": "a_fk_result_snapshot_result_id", "unique": false, "origin": "c", "columns": ["result_id"]}, {"name": "a_fk_result_snapshot_assessment_version_id", "unique": false, "origin": "c", "columns": ["assessment_version_id"]}, {"name": "a_fk_result_snapshot_dimension_id", "unique": false, "origin": "c", "columns": ["dimension_id"]}, {"name": "a_fk_result_snapshot_scale_id", "unique": false, "origin": "c", "columns": ["scale_id"]}, {"name": "a_fk_result_snapshot_scale_version_id", "unique": false, "origin": "c", "columns": ["scale_version_id"]}, {"name": "a_fk_result_snapshot_level_id", "unique": false, "origin": "c", "columns": ["level_id"]}, {"name": "a_fk_result_snapshot_source_record_id", "unique": false, "origin": "c", "columns": ["source_record_id"]}, {"name": "sqlite_autoindex_result_snapshot_1", "unique": true, "origin": "pk", "columns": ["result_version_id"]}]`.

## risk_case

Original selected RiskCase identity; no new actual cases are admitted by assessment fixtures.

Declared FD: `Primary key -> stored row attributes within the original bounded profile`. Original 0.1.0 dictionary/guards retained; full domain normalization is not inferred from schema inspection.

| Column | Type | Required | Meaning |
| --- | --- | --- | --- |
| case_id | TEXT | True | Selected RiskCase identifier. |
| family | TEXT | True | Enforced local identity family; not inferred from a label. |
| label | TEXT | True | Non-unique human display label; not an identity key. |
| source_record_id | TEXT | True | Exact source_record provenance key for this row. |

Primary key: `case_id`. Foreign keys: `[{"id": 0, "sequence": 0, "target_table": "identity_registry", "column": "case_id", "target_column": "resource_id", "on_delete": "NO ACTION"}, {"id": 0, "sequence": 1, "target_table": "identity_registry", "column": "family", "target_column": "family", "on_delete": "NO ACTION"}, {"id": 1, "sequence": 0, "target_table": "source_record", "column": "source_record_id", "target_column": "record_id", "on_delete": "NO ACTION"}]`.

Indexes: `[{"name": "a_fk_risk_case_source_record_id", "unique": false, "origin": "c", "columns": ["source_record_id"]}, {"name": "sqlite_autoindex_risk_case_1", "unique": true, "origin": "pk", "columns": ["case_id"]}]`.

## scale_level

Governed vocabulary level membership in one immutable selected scale version.

Declared FD: `level_id -> scale_version_id, source`. A distinct level resource belongs to one governed version in this local profile; reissued levels use distinct identities.

| Column | Type | Required | Meaning |
| --- | --- | --- | --- |
| level_id | TEXT | True | Optional selected AssessmentScaleLevel artifact, bound to its scale version. |
| scale_version_id | TEXT | True | Pinned ArtifactVersion of the exact scale, with frozen declared dimension. |
| source_record_id | TEXT | True | Exact source_record provenance key for this row. |

Primary key: `level_id`. Foreign keys: `[{"id": 0, "sequence": 0, "target_table": "source_record", "column": "source_record_id", "target_column": "record_id", "on_delete": "NO ACTION"}, {"id": 1, "sequence": 0, "target_table": "scale_snapshot", "column": "scale_version_id", "target_column": "scale_version_id", "on_delete": "NO ACTION"}, {"id": 2, "sequence": 0, "target_table": "artifact_typing", "column": "level_id", "target_column": "artifact_id", "on_delete": "NO ACTION"}]`.

Indexes: `[{"name": "a_fk_scale_level_scale_version_id", "unique": false, "origin": "c", "columns": ["scale_version_id"]}, {"name": "a_fk_scale_level_source_record_id", "unique": false, "origin": "c", "columns": ["source_record_id"]}, {"name": "sqlite_autoindex_scale_level_1", "unique": true, "origin": "pk", "columns": ["level_id"]}]`.

## scale_snapshot

Version-owned declared scale dimension and explicit scale target.

Declared FD: `scale_version_id -> scale_id, dimension_id, source`. The direct scale target repeats versionOf deliberately as an explicit assertion; equality is guarded. No automatic claim of BCNF.

| Column | Type | Required | Meaning |
| --- | --- | --- | --- |
| scale_version_id | TEXT | True | Pinned ArtifactVersion of the exact scale, with frozen declared dimension. |
| scale_id | TEXT | True | Optional/direct native AssessmentScale assertion, checked against its version. |
| dimension_id | TEXT | True | Governed AssessmentDimension artifact; missing cannot become a default dimension. |
| source_record_id | TEXT | True | Exact source_record provenance key for this row. |

Primary key: `scale_version_id`. Foreign keys: `[{"id": 0, "sequence": 0, "target_table": "source_record", "column": "source_record_id", "target_column": "record_id", "on_delete": "NO ACTION"}, {"id": 1, "sequence": 0, "target_table": "artifact_typing", "column": "dimension_id", "target_column": "artifact_id", "on_delete": "NO ACTION"}, {"id": 2, "sequence": 0, "target_table": "information_artifact", "column": "scale_id", "target_column": "artifact_id", "on_delete": "NO ACTION"}, {"id": 3, "sequence": 0, "target_table": "version_snapshot", "column": "scale_version_id", "target_column": "version_id", "on_delete": "NO ACTION"}]`.

Indexes: `[{"name": "a_fk_scale_snapshot_scale_id", "unique": false, "origin": "c", "columns": ["scale_id"]}, {"name": "a_fk_scale_snapshot_dimension_id", "unique": false, "origin": "c", "columns": ["dimension_id"]}, {"name": "a_fk_scale_snapshot_source_record_id", "unique": false, "origin": "c", "columns": ["source_record_id"]}, {"name": "sqlite_autoindex_scale_snapshot_1", "unique": true, "origin": "pk", "columns": ["scale_version_id"]}]`.

## schema_migration

Executed migration numbers and exact SQL digests, matching user_version.

Declared FD: `Primary key -> stored row attributes within the original bounded profile`. Original 0.1.0 dictionary/guards retained; full domain normalization is not inferred from schema inspection.

| Column | Type | Required | Meaning |
| --- | --- | --- | --- |
| version | INTEGER | False | Applied schema migration number. |
| sha256 | TEXT | True | Digest of exact applied SQL bytes. |

Primary key: `version`. Foreign keys: `[]`.

Indexes: `[]`.

## source_record

Append-only exact raw source JSON; preserves unknown and received evidence before admission.

Declared FD: `Primary key -> stored row attributes within the original bounded profile`. Original 0.1.0 dictionary/guards retained; full domain normalization is not inferred from schema inspection.

| Column | Type | Required | Meaning |
| --- | --- | --- | --- |
| record_id | TEXT | True | Exact source-record identifier. |
| original_json | TEXT | True | Exact received JSON; null and unresolved fields are preserved. |

Primary key: `record_id`. Foreign keys: `[]`.

Indexes: `[{"name": "sqlite_autoindex_source_record_1", "unique": true, "origin": "pk", "columns": ["record_id"]}]`.

## version_dependency

Immutable version-owned effective dependency pins in the original profile.

Declared FD: `Primary key -> stored row attributes within the original bounded profile`. Original 0.1.0 dictionary/guards retained; full domain normalization is not inferred from schema inspection.

| Column | Type | Required | Meaning |
| --- | --- | --- | --- |
| owner_version_id | TEXT | True | Version owning an immutable dependency pin. |
| slot | TEXT | True | Application dependency role Context, Method, Scale or Criteria. |
| target_version_id | TEXT | True | Pinned target ArtifactVersion. |
| direct_artifact_id | TEXT | False | Optional explicitly asserted direct target; must agree with versionOf. |

Primary key: `owner_version_id, slot`. Foreign keys: `[{"id": 0, "sequence": 0, "target_table": "information_artifact", "column": "direct_artifact_id", "target_column": "artifact_id", "on_delete": "NO ACTION"}, {"id": 1, "sequence": 0, "target_table": "version_snapshot", "column": "target_version_id", "target_column": "version_id", "on_delete": "NO ACTION"}, {"id": 2, "sequence": 0, "target_table": "version_snapshot", "column": "owner_version_id", "target_column": "version_id", "on_delete": "NO ACTION"}]`.

Indexes: `[{"name": "a_fk_version_dependency_direct_artifact_id", "unique": false, "origin": "c", "columns": ["direct_artifact_id"]}, {"name": "dependency_by_target", "unique": false, "origin": "c", "columns": ["target_version_id"]}, {"name": "sqlite_autoindex_version_dependency_1", "unique": true, "origin": "pk", "columns": ["owner_version_id", "slot"]}]`.

## version_snapshot

Sealed payload, source and issue state for a distinct artifact version.

Declared FD: `Primary key -> stored row attributes within the original bounded profile`. Original 0.1.0 dictionary/guards retained; full domain normalization is not inferred from schema inspection.

| Column | Type | Required | Meaning |
| --- | --- | --- | --- |
| version_id | TEXT | True | Distinct version identity. |
| family | TEXT | True | Enforced local identity family; not inferred from a label. |
| artifact_id | TEXT | True | Stable InformationArtifact identity. |
| entry_id | TEXT | False | Register-entry identity or optional selected revision target. |
| previous_version_id | TEXT | False | Explicit predecessor version; original entry lineage remains same-entry and acyclic. |
| payload_json | TEXT | True | Serialized issued/staged content; new bundle payloads preserve the exact declared metadata dictionary. |
| source_record_id | TEXT | True | Exact source_record provenance key for this row. |
| issued_at | TEXT | False | Canonical issue timestamp; distinct from recorded, reference and validity time. |
| is_issued | INTEGER | True | 0 staging / 1 sealed; sealed content and owned metadata are immutable. |

Primary key: `version_id`. Foreign keys: `[{"id": 0, "sequence": 0, "target_table": "identity_registry", "column": "version_id", "target_column": "resource_id", "on_delete": "NO ACTION"}, {"id": 0, "sequence": 1, "target_table": "identity_registry", "column": "family", "target_column": "family", "on_delete": "NO ACTION"}, {"id": 1, "sequence": 0, "target_table": "source_record", "column": "source_record_id", "target_column": "record_id", "on_delete": "NO ACTION"}, {"id": 2, "sequence": 0, "target_table": "version_snapshot", "column": "previous_version_id", "target_column": "version_id", "on_delete": "NO ACTION"}, {"id": 3, "sequence": 0, "target_table": "register_entry", "column": "entry_id", "target_column": "entry_id", "on_delete": "NO ACTION"}, {"id": 4, "sequence": 0, "target_table": "information_artifact", "column": "artifact_id", "target_column": "artifact_id", "on_delete": "NO ACTION"}]`.

Indexes: `[{"name": "a_fk_version_snapshot_source_record_id", "unique": false, "origin": "c", "columns": ["source_record_id"]}, {"name": "version_by_predecessor", "unique": false, "origin": "c", "columns": ["previous_version_id"]}, {"name": "version_by_entry", "unique": false, "origin": "c", "columns": ["entry_id", "is_issued"]}, {"name": "version_by_artifact", "unique": false, "origin": "c", "columns": ["artifact_id", "is_issued"]}, {"name": "sqlite_autoindex_version_snapshot_1", "unique": true, "origin": "pk", "columns": ["version_id"]}]`.

## working_draft

Editable application staging for original issue API; not an issued native version.

Declared FD: `Primary key -> stored row attributes within the original bounded profile`. Original 0.1.0 dictionary/guards retained; full domain normalization is not inferred from schema inspection.

| Column | Type | Required | Meaning |
| --- | --- | --- | --- |
| draft_id | TEXT | True | Editable staging identity, excluded from native issued-version export. |
| artifact_id | TEXT | True | Stable InformationArtifact identity. |
| entry_id | TEXT | False | Register-entry identity or optional selected revision target. |
| previous_version_id | TEXT | False | Explicit predecessor version; original entry lineage remains same-entry and acyclic. |
| payload_json | TEXT | True | Serialized issued/staged content; new bundle payloads preserve the exact declared metadata dictionary. |
| source_record_id | TEXT | True | Exact source_record provenance key for this row. |

Primary key: `draft_id`. Foreign keys: `[{"id": 0, "sequence": 0, "target_table": "source_record", "column": "source_record_id", "target_column": "record_id", "on_delete": "NO ACTION"}, {"id": 1, "sequence": 0, "target_table": "version_snapshot", "column": "previous_version_id", "target_column": "version_id", "on_delete": "NO ACTION"}, {"id": 2, "sequence": 0, "target_table": "register_entry", "column": "entry_id", "target_column": "entry_id", "on_delete": "NO ACTION"}, {"id": 3, "sequence": 0, "target_table": "information_artifact", "column": "artifact_id", "target_column": "artifact_id", "on_delete": "NO ACTION"}]`.

Indexes: `[{"name": "a_fk_working_draft_artifact_id", "unique": false, "origin": "c", "columns": ["artifact_id"]}, {"name": "a_fk_working_draft_entry_id", "unique": false, "origin": "c", "columns": ["entry_id"]}, {"name": "a_fk_working_draft_previous_version_id", "unique": false, "origin": "c", "columns": ["previous_version_id"]}, {"name": "a_fk_working_draft_source_record_id", "unique": false, "origin": "c", "columns": ["source_record_id"]}, {"name": "sqlite_autoindex_working_draft_1", "unique": true, "origin": "pk", "columns": ["draft_id"]}]`.

