-- Application-only assessment correction; original migrations and native views unchanged.
CREATE TABLE assessment_correction (
 corrected_version_id TEXT PRIMARY KEY NOT NULL REFERENCES assessment_snapshot(assessment_version_id),
 prior_version_id TEXT NOT NULL REFERENCES assessment_snapshot(assessment_version_id),
 reason TEXT NOT NULL CHECK(length(trim(reason))>0),
 recorded_at TEXT NOT NULL,
 source_record_id TEXT NOT NULL REFERENCES source_record(record_id),
 CHECK(corrected_version_id<>prior_version_id),
 CHECK(length(recorded_at)=20 AND recorded_at GLOB '????-??-??T??:??:??Z'
   AND strftime('%Y-%m-%dT%H:%M:%SZ',recorded_at) IS recorded_at
   AND date(recorded_at,'+0 days') IS substr(recorded_at,1,10))
) STRICT;
CREATE INDEX correction_parent ON assessment_correction(prior_version_id);
CREATE INDEX correction_source ON assessment_correction(source_record_id);
CREATE VIEW v_correction_invalid AS
 SELECT c.corrected_version_id FROM assessment_correction c
 LEFT JOIN assessment_snapshot n ON n.assessment_version_id=c.corrected_version_id
 LEFT JOIN assessment_snapshot p ON p.assessment_version_id=c.prior_version_id
 LEFT JOIN version_snapshot nv ON nv.version_id=c.corrected_version_id
 LEFT JOIN version_snapshot pv ON pv.version_id=c.prior_version_id
 WHERE n.assessment_version_id IS NULL OR p.assessment_version_id IS NULL
 OR n.assessment_id<>p.assessment_id OR nv.is_issued<>1 OR pv.is_issued<>1
 OR c.recorded_at<n.recorded_at OR c.recorded_at<p.recorded_at;
CREATE TRIGGER correction_insert BEFORE INSERT ON assessment_correction BEGIN
 SELECT CASE WHEN EXISTS(SELECT 1 FROM assessment_correction WHERE corrected_version_id=NEW.corrected_version_id)
 THEN RAISE(ABORT,'R-CORRECTION-DUPLICATE') END;
 SELECT CASE WHEN NOT EXISTS(
 SELECT 1 FROM assessment_snapshot n JOIN assessment_snapshot p ON n.assessment_id=p.assessment_id
 JOIN version_snapshot nv ON nv.version_id=n.assessment_version_id
 JOIN version_snapshot pv ON pv.version_id=p.assessment_version_id
 WHERE n.assessment_version_id=NEW.corrected_version_id AND p.assessment_version_id=NEW.prior_version_id
 AND nv.is_issued=1 AND pv.is_issued=1 AND NEW.recorded_at>=n.recorded_at AND NEW.recorded_at>=p.recorded_at)
 THEN RAISE(ABORT,'R-CORRECTION-PARENT-OR-TIME') END;
 SELECT CASE WHEN EXISTS(WITH RECURSIVE ancestors(id) AS (
 SELECT NEW.prior_version_id UNION
 SELECT c.prior_version_id FROM assessment_correction c JOIN ancestors a ON c.corrected_version_id=a.id
 ) SELECT 1 FROM ancestors WHERE id=NEW.corrected_version_id)
 THEN RAISE(ABORT,'R-CORRECTION-CYCLE') END;
END;
CREATE TRIGGER correction_update BEFORE UPDATE ON assessment_correction BEGIN
 SELECT RAISE(ABORT,'R-CORRECTION-IMMUTABLE');
END;
CREATE TRIGGER correction_delete BEFORE DELETE ON assessment_correction BEGIN
 SELECT RAISE(ABORT,'R-CORRECTION-IMMUTABLE');
END;
