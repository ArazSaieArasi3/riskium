-- Additive public SQLite assessment profile. Base migrations 1/2 stay unchanged.
CREATE TABLE artifact_typing (
  artifact_id TEXT PRIMARY KEY NOT NULL REFERENCES information_artifact(artifact_id),
  native_class TEXT NOT NULL CHECK(native_class IN ('RKM-C032','RKM-C033','RKM-C034','RKM-C038','RKM-C039')),
  scheme_uri TEXT,
  scheme_edition TEXT,
  local_code TEXT,
  source_record_id TEXT NOT NULL REFERENCES source_record(record_id),
  UNIQUE(artifact_id,native_class),
  UNIQUE(scheme_uri,scheme_edition,local_code),
  CHECK((native_class IN ('RKM-C038','RKM-C039') AND scheme_uri IS NOT NULL AND scheme_edition IS NOT NULL AND local_code IS NOT NULL
    AND instr(scheme_uri,':')>1 AND instr(scheme_edition,':')>1 AND length(trim(local_code))>0)
    OR (native_class NOT IN ('RKM-C038','RKM-C039') AND scheme_uri IS NULL AND scheme_edition IS NULL AND local_code IS NULL))
) STRICT;
CREATE TABLE scale_snapshot (
  scale_version_id TEXT PRIMARY KEY NOT NULL REFERENCES version_snapshot(version_id),
  scale_id TEXT NOT NULL REFERENCES information_artifact(artifact_id),
  dimension_id TEXT NOT NULL REFERENCES artifact_typing(artifact_id),
  source_record_id TEXT NOT NULL REFERENCES source_record(record_id)
) STRICT;
CREATE TABLE scale_level (
  level_id TEXT PRIMARY KEY NOT NULL REFERENCES artifact_typing(artifact_id),
  scale_version_id TEXT NOT NULL REFERENCES scale_snapshot(scale_version_id),
  source_record_id TEXT NOT NULL REFERENCES source_record(record_id)
) STRICT;
CREATE TABLE method_scope (
  method_version_id TEXT NOT NULL REFERENCES version_snapshot(version_id),
  scale_id TEXT NOT NULL REFERENCES information_artifact(artifact_id),
  dimension_id TEXT NOT NULL REFERENCES artifact_typing(artifact_id),
  source_record_id TEXT NOT NULL REFERENCES source_record(record_id),
  PRIMARY KEY(method_version_id,scale_id,dimension_id)
) STRICT;
CREATE TABLE assessment_snapshot (
  assessment_version_id TEXT PRIMARY KEY NOT NULL REFERENCES version_snapshot(version_id),
  assessment_id TEXT NOT NULL REFERENCES artifact_typing(artifact_id),
  basis_id TEXT NOT NULL REFERENCES artifact_typing(artifact_id),
  basis_version_id TEXT REFERENCES version_snapshot(version_id),
  context_id TEXT REFERENCES information_artifact(artifact_id),
  context_version_id TEXT NOT NULL REFERENCES version_snapshot(version_id),
  method_id TEXT REFERENCES information_artifact(artifact_id),
  method_version_id TEXT REFERENCES version_snapshot(version_id),
  temporal_context_id TEXT CHECK(temporal_context_id IS NULL OR instr(temporal_context_id,':')>1),
  recorded_at TEXT NOT NULL,
  reference_at TEXT,
  valid_from TEXT,
  valid_to TEXT,
  source_record_id TEXT NOT NULL REFERENCES source_record(record_id)
) STRICT;
CREATE TABLE result_snapshot (
  result_version_id TEXT PRIMARY KEY NOT NULL REFERENCES version_snapshot(version_id),
  result_id TEXT NOT NULL REFERENCES artifact_typing(artifact_id),
  assessment_version_id TEXT NOT NULL REFERENCES assessment_snapshot(assessment_version_id),
  dimension_id TEXT NOT NULL REFERENCES artifact_typing(artifact_id),
  scale_id TEXT REFERENCES information_artifact(artifact_id),
  scale_version_id TEXT REFERENCES scale_snapshot(scale_version_id),
  level_id TEXT REFERENCES scale_level(level_id),
  score_kind TEXT NOT NULL,
  reported_value TEXT,
  source_record_id TEXT NOT NULL REFERENCES source_record(record_id),
  source_locator TEXT NOT NULL,
  interpretation_origin TEXT NOT NULL
) STRICT;
