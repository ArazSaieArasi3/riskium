CREATE TABLE metadata(key TEXT PRIMARY KEY,value TEXT NOT NULL) STRICT;
CREATE TABLE artifact(id TEXT PRIMARY KEY,label TEXT NOT NULL) STRICT;
CREATE TABLE artifact_version(id TEXT PRIMARY KEY,artifact_id TEXT NOT NULL REFERENCES artifact(id),payload_sha256 TEXT NOT NULL) STRICT;
CREATE TABLE reference_snapshot(version_id TEXT PRIMARY KEY REFERENCES artifact_version(id),item_version TEXT NOT NULL REFERENCES artifact_version(id),proposed_purpose TEXT NOT NULL,locator TEXT NOT NULL) STRICT;
CREATE TABLE reference_context(reference_version TEXT NOT NULL REFERENCES reference_snapshot(version_id),context_version TEXT NOT NULL REFERENCES artifact_version(id),PRIMARY KEY(reference_version,context_version)) STRICT;
CREATE TABLE grounding_record(version_id TEXT PRIMARY KEY,artifact_id TEXT NOT NULL,body TEXT NOT NULL CHECK(length(trim(body))>0),locator TEXT NOT NULL CHECK(length(trim(locator))>0)) STRICT;
CREATE TABLE explicit_alias(left_id TEXT NOT NULL REFERENCES artifact(id),right_id TEXT NOT NULL REFERENCES artifact(id),PRIMARY KEY(left_id,right_id),CHECK(left_id<>right_id)) STRICT;
CREATE TABLE evidence_use(
 id TEXT PRIMARY KEY,
 reference_version TEXT NOT NULL REFERENCES reference_snapshot(version_id),
 item_version TEXT NOT NULL REFERENCES artifact_version(id),
 context_version TEXT NOT NULL REFERENCES artifact_version(id),
 grounding_version TEXT NOT NULL REFERENCES grounding_record(version_id),
 purpose TEXT NOT NULL CHECK(purpose IN ('support','challenge','context')),
 recorded_at TEXT NOT NULL CHECK(recorded_at GLOB '????-??-??T??:??:??Z' AND strftime('%Y-%m-%dT%H:%M:%SZ',recorded_at,'+0 days') IS recorded_at),
 justification TEXT NOT NULL CHECK(length(trim(justification))>0),
 UNIQUE(reference_version,item_version,context_version,grounding_version,purpose),
 FOREIGN KEY(reference_version,context_version) REFERENCES reference_context(reference_version,context_version)
) STRICT;
CREATE VIEW v_use_invalid AS
 WITH RECURSIVE links(a,b) AS (
  SELECT left_id,right_id FROM explicit_alias UNION SELECT right_id,left_id FROM explicit_alias
  UNION SELECT l.a,e.right_id FROM links l JOIN explicit_alias e ON e.left_id=l.b
  UNION SELECT l.a,e.left_id FROM links l JOIN explicit_alias e ON e.right_id=l.b
 )
 SELECT u.id FROM evidence_use u
 JOIN reference_snapshot r ON r.version_id=u.reference_version
 JOIN artifact_version rv ON rv.id=u.reference_version
 JOIN artifact_version iv ON iv.id=u.item_version
 WHERE r.item_version<>u.item_version OR rv.artifact_id=iv.artifact_id
 OR EXISTS(SELECT 1 FROM links WHERE a=rv.artifact_id AND b=iv.artifact_id);
CREATE TRIGGER use_coherence AFTER INSERT ON evidence_use BEGIN
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_use_invalid) THEN RAISE(ABORT,'R-EU-COHERENCE') END;
END;
CREATE TRIGGER alias_coherence AFTER INSERT ON explicit_alias BEGIN
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_use_invalid) THEN RAISE(ABORT,'R-EU-ALIAS') END;
END;
