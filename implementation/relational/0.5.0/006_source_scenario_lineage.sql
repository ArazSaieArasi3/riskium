-- Supplementary application metadata; all v1-v5 tables and native views retained.
CREATE TABLE knowledge_correction (
 corrected_version_id TEXT PRIMARY KEY NOT NULL REFERENCES knowledge_snapshot(version_id),
 prior_version_id TEXT NOT NULL REFERENCES knowledge_snapshot(version_id),
 reason TEXT NOT NULL CHECK(length(trim(reason))>0),
 recorded_at TEXT NOT NULL CHECK(length(recorded_at)=20 AND recorded_at GLOB '????-??-??T??:??:??Z'
   AND strftime('%Y-%m-%dT%H:%M:%SZ',recorded_at) IS recorded_at
   AND date(recorded_at,'+0 days') IS substr(recorded_at,1,10)),
 source_record_id TEXT NOT NULL REFERENCES source_record(record_id),
 source_locator TEXT NOT NULL CHECK(length(trim(source_locator))>0),
 interpretation_origin TEXT NOT NULL CHECK(length(trim(interpretation_origin))>0),
 CHECK(corrected_version_id<>prior_version_id)
) STRICT;
CREATE INDEX knowledge_correction_parent ON knowledge_correction(prior_version_id);
CREATE INDEX knowledge_correction_source ON knowledge_correction(source_record_id);
CREATE VIEW v_knowledge_lineage_invalid AS
 WITH RECURSIVE walk(root,id) AS (
   SELECT corrected_version_id,prior_version_id FROM knowledge_correction
   UNION SELECT w.root,c.prior_version_id FROM walk w
     JOIN knowledge_correction c ON c.corrected_version_id=w.id
 )
 SELECT c.corrected_version_id, 'ENDPOINT' AS code FROM knowledge_correction c
 LEFT JOIN knowledge_snapshot n ON n.version_id=c.corrected_version_id
 LEFT JOIN knowledge_snapshot p ON p.version_id=c.prior_version_id
 LEFT JOIN version_snapshot nv ON nv.version_id=c.corrected_version_id
 LEFT JOIN version_snapshot pv ON pv.version_id=c.prior_version_id
 WHERE n.version_id IS NULL OR p.version_id IS NULL OR nv.is_issued IS NOT 1 OR pv.is_issued IS NOT 1
 UNION SELECT c.corrected_version_id,'OWNER' FROM knowledge_correction c
 JOIN knowledge_snapshot n ON n.version_id=c.corrected_version_id
 JOIN knowledge_snapshot p ON p.version_id=c.prior_version_id
 JOIN knowledge_type nt ON nt.artifact_id=n.artifact_id
 JOIN knowledge_type pt ON pt.artifact_id=p.artifact_id
 WHERE n.artifact_id<>p.artifact_id OR nt.native_class<>pt.native_class
 UNION SELECT c.corrected_version_id,'PROVENANCE' FROM knowledge_correction c
 WHERE length(trim(c.reason))=0 OR length(trim(c.source_locator))=0 OR length(trim(c.interpretation_origin))=0
 UNION SELECT c.corrected_version_id,'TIME' FROM knowledge_correction c
 JOIN knowledge_snapshot n ON n.version_id=c.corrected_version_id
 JOIN knowledge_snapshot p ON p.version_id=c.prior_version_id
 JOIN version_snapshot nv ON nv.version_id=c.corrected_version_id
 JOIN version_snapshot pv ON pv.version_id=c.prior_version_id
 WHERE length(c.recorded_at)<>20 OR c.recorded_at NOT GLOB '????-??-??T??:??:??Z'
 OR strftime('%Y-%m-%dT%H:%M:%SZ',c.recorded_at) IS NOT c.recorded_at
 OR date(c.recorded_at,'+0 days') IS NOT substr(c.recorded_at,1,10)
 OR c.recorded_at<n.recorded_at OR c.recorded_at<p.recorded_at
 OR c.recorded_at<nv.issued_at OR c.recorded_at<pv.issued_at
 UNION SELECT root,'CYCLE' FROM walk WHERE root=id;
CREATE TRIGGER knowledge_correction_insert BEFORE INSERT ON knowledge_correction BEGIN
 SELECT CASE WHEN EXISTS(SELECT 1 FROM knowledge_correction WHERE corrected_version_id=NEW.corrected_version_id)
 THEN RAISE(ABORT,'R-LINEAGE-DUPLICATE') END;
 SELECT CASE WHEN NEW.corrected_version_id=NEW.prior_version_id THEN RAISE(ABORT,'R-LINEAGE-SELF') END;
 SELECT CASE WHEN NOT EXISTS(
 SELECT 1 FROM knowledge_snapshot n JOIN knowledge_snapshot p
 JOIN version_snapshot nv ON nv.version_id=n.version_id
 JOIN version_snapshot pv ON pv.version_id=p.version_id
 WHERE n.version_id=NEW.corrected_version_id AND p.version_id=NEW.prior_version_id
 AND nv.is_issued=1 AND pv.is_issued=1)
 THEN RAISE(ABORT,'R-LINEAGE-ENDPOINT') END;
 SELECT CASE WHEN EXISTS(
 SELECT 1 FROM knowledge_snapshot n JOIN knowledge_snapshot p
 JOIN knowledge_type nt ON nt.artifact_id=n.artifact_id
 JOIN knowledge_type pt ON pt.artifact_id=p.artifact_id
 WHERE n.version_id=NEW.corrected_version_id AND p.version_id=NEW.prior_version_id
 AND (n.artifact_id<>p.artifact_id OR nt.native_class<>pt.native_class))
 THEN RAISE(ABORT,'R-LINEAGE-OWNER') END;
 SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM source_record WHERE record_id=NEW.source_record_id)
 THEN RAISE(ABORT,'R-LINEAGE-SOURCE') END;
 SELECT CASE WHEN length(trim(NEW.reason))=0 OR length(trim(NEW.source_locator))=0 OR length(trim(NEW.interpretation_origin))=0
 THEN RAISE(ABORT,'R-LINEAGE-PROVENANCE') END;
 SELECT CASE WHEN length(NEW.recorded_at)<>20 OR NEW.recorded_at NOT GLOB '????-??-??T??:??:??Z'
 OR strftime('%Y-%m-%dT%H:%M:%SZ',NEW.recorded_at) IS NOT NEW.recorded_at
 OR date(NEW.recorded_at,'+0 days') IS NOT substr(NEW.recorded_at,1,10)
 OR EXISTS(SELECT 1 FROM knowledge_snapshot n JOIN knowledge_snapshot p
 JOIN version_snapshot nv ON nv.version_id=n.version_id
 JOIN version_snapshot pv ON pv.version_id=p.version_id
 WHERE n.version_id=NEW.corrected_version_id AND p.version_id=NEW.prior_version_id
 AND (NEW.recorded_at<n.recorded_at OR NEW.recorded_at<p.recorded_at
 OR NEW.recorded_at<nv.issued_at OR NEW.recorded_at<pv.issued_at))
 THEN RAISE(ABORT,'R-LINEAGE-TIME') END;
 SELECT CASE WHEN EXISTS(WITH RECURSIVE ancestors(id) AS (
 SELECT NEW.prior_version_id UNION
 SELECT c.prior_version_id FROM knowledge_correction c JOIN ancestors a ON c.corrected_version_id=a.id
 ) SELECT 1 FROM ancestors WHERE id=NEW.corrected_version_id)
 THEN RAISE(ABORT,'R-LINEAGE-CYCLE') END;
END;
CREATE TRIGGER knowledge_correction_update BEFORE UPDATE ON knowledge_correction BEGIN
 SELECT RAISE(ABORT,'R-LINEAGE-IMMUTABLE');
END;
CREATE TRIGGER knowledge_correction_delete BEFORE DELETE ON knowledge_correction BEGIN
 SELECT RAISE(ABORT,'R-LINEAGE-IMMUTABLE');
END;
