-- SQLite >= 3.38. Synthetic public identity/history slice, not the private full DB.
CREATE TABLE source_record (
  record_id TEXT PRIMARY KEY NOT NULL CHECK(instr(record_id, ':') > 1),
  original_json TEXT NOT NULL CHECK(json_valid(original_json))
) STRICT;
CREATE TABLE identity_registry (
  resource_id TEXT PRIMARY KEY NOT NULL CHECK(instr(resource_id, ':') > 1 AND trim(resource_id)=resource_id),
  family TEXT NOT NULL CHECK(family IN ('case','artifact','version')),
  UNIQUE(resource_id,family)
) STRICT;
CREATE TABLE risk_case (
  case_id TEXT PRIMARY KEY NOT NULL,
  family TEXT NOT NULL DEFAULT 'case' CHECK(family='case'),
  label TEXT NOT NULL CHECK(length(trim(label))>0),
  source_record_id TEXT NOT NULL REFERENCES source_record(record_id),
  FOREIGN KEY(case_id,family) REFERENCES identity_registry(resource_id,family)
) STRICT;
CREATE TABLE information_artifact (
  artifact_id TEXT PRIMARY KEY NOT NULL,
  family TEXT NOT NULL DEFAULT 'artifact' CHECK(family='artifact'),
  kind TEXT NOT NULL CHECK(kind IN ('RKM-C014','RKM-C022','RKM-C030','RKM-C002','RKM-C035','RKM-C036','RKM-C072')),
  label TEXT NOT NULL CHECK(length(trim(label))>0),
  source_record_id TEXT NOT NULL REFERENCES source_record(record_id),
  UNIQUE(artifact_id,kind),
  FOREIGN KEY(artifact_id,family) REFERENCES identity_registry(resource_id,family)
) STRICT;
CREATE TABLE register_entry (
  entry_id TEXT PRIMARY KEY NOT NULL,
  entry_kind TEXT NOT NULL DEFAULT 'RKM-C022' CHECK(entry_kind='RKM-C022'),
  case_id TEXT NOT NULL REFERENCES risk_case(case_id),
  register_id TEXT NOT NULL,
  register_kind TEXT NOT NULL DEFAULT 'RKM-C030' CHECK(register_kind='RKM-C030'),
  FOREIGN KEY(entry_id,entry_kind) REFERENCES information_artifact(artifact_id,kind),
  FOREIGN KEY(register_id,register_kind) REFERENCES information_artifact(artifact_id,kind)
) STRICT;
CREATE TABLE working_draft (
  draft_id TEXT PRIMARY KEY NOT NULL CHECK(instr(draft_id, ':')>1),
  artifact_id TEXT NOT NULL REFERENCES information_artifact(artifact_id),
  entry_id TEXT REFERENCES register_entry(entry_id),
  previous_version_id TEXT REFERENCES version_snapshot(version_id),
  payload_json TEXT NOT NULL CHECK(json_valid(payload_json) AND json_type(payload_json)='object'),
  source_record_id TEXT NOT NULL REFERENCES source_record(record_id),
  CHECK(entry_id IS NULL OR entry_id=artifact_id),
  CHECK(previous_version_id IS NULL OR entry_id IS NOT NULL)
) STRICT;
CREATE TABLE draft_dependency (
  draft_id TEXT NOT NULL REFERENCES working_draft(draft_id) ON DELETE CASCADE,
  slot TEXT NOT NULL CHECK(slot IN ('Context','Method','Scale','Criteria')),
  target_version_id TEXT NOT NULL REFERENCES version_snapshot(version_id),
  direct_artifact_id TEXT REFERENCES information_artifact(artifact_id),
  PRIMARY KEY(draft_id,slot)
) STRICT;
CREATE TABLE version_snapshot (
  version_id TEXT PRIMARY KEY NOT NULL,
  family TEXT NOT NULL DEFAULT 'version' CHECK(family='version'),
  artifact_id TEXT NOT NULL REFERENCES information_artifact(artifact_id),
  entry_id TEXT REFERENCES register_entry(entry_id),
  previous_version_id TEXT REFERENCES version_snapshot(version_id),
  payload_json TEXT NOT NULL CHECK(json_valid(payload_json) AND json_type(payload_json)='object'),
  source_record_id TEXT NOT NULL REFERENCES source_record(record_id),
  issued_at TEXT,
  is_issued INTEGER NOT NULL DEFAULT 0 CHECK(is_issued IN (0,1)),
  CONSTRAINT revision_target CHECK(entry_id IS NULL OR entry_id=artifact_id),
  CONSTRAINT predecessor_owner CHECK(previous_version_id IS NULL OR entry_id IS NOT NULL),
  CONSTRAINT predecessor_not_self CHECK(previous_version_id IS NULL OR previous_version_id<>version_id),
  CONSTRAINT issued_timestamp CHECK(issued_at IS NULL OR
    (length(issued_at)=20 AND issued_at GLOB '????-??-??T??:??:??Z' AND datetime(issued_at) IS NOT NULL)),
  FOREIGN KEY(version_id,family) REFERENCES identity_registry(resource_id,family)
) STRICT;
CREATE TABLE version_dependency (
  owner_version_id TEXT NOT NULL REFERENCES version_snapshot(version_id),
  slot TEXT NOT NULL CHECK(slot IN ('Context','Method','Scale','Criteria')),
  target_version_id TEXT NOT NULL REFERENCES version_snapshot(version_id),
  direct_artifact_id TEXT REFERENCES information_artifact(artifact_id),
  PRIMARY KEY(owner_version_id,slot)
) STRICT;
