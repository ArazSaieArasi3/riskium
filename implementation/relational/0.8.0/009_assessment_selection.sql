-- Documentary decision context is distinct from native assessment context.
CREATE TABLE assessment_selection_event (
 ordinal INTEGER PRIMARY KEY AUTOINCREMENT,
 event_id TEXT NOT NULL UNIQUE,
 kind TEXT NOT NULL,
 assessment_id TEXT NOT NULL REFERENCES information_artifact(artifact_id),
 decision_context_id TEXT NOT NULL,
 target_version TEXT REFERENCES version_snapshot(version_id),
 actor TEXT NOT NULL,
 reason TEXT NOT NULL,
 source_record_id TEXT NOT NULL REFERENCES source_record(record_id),
 source_locator TEXT NOT NULL,
 interpretation_origin TEXT NOT NULL,
 recorded_at TEXT NOT NULL
) STRICT;
CREATE INDEX assessment_selection_context ON assessment_selection_event(assessment_id,decision_context_id,ordinal);
CREATE INDEX assessment_selection_withdrawal ON assessment_selection_event(assessment_id,decision_context_id,target_version,ordinal) WHERE kind='WITHDRAW';
CREATE VIEW v_assessment_selection_invalid AS
SELECT e.event_id,'PROVENANCE' AS code FROM assessment_selection_event e WHERE length(trim(e.event_id,char(9)||char(10)||char(13)||' '))=0 OR length(trim(e.actor,char(9)||char(10)||char(13)||' '))=0 OR length(trim(e.reason,char(9)||char(10)||char(13)||' '))=0 OR length(trim(e.source_locator,char(9)||char(10)||char(13)||' '))=0 OR length(trim(e.interpretation_origin,char(9)||char(10)||char(13)||' '))=0 OR length(trim(e.decision_context_id,char(9)||char(10)||char(13)||' '))=0 OR NOT EXISTS(SELECT 1 FROM source_record s WHERE s.record_id=e.source_record_id)
UNION
SELECT e.event_id,'TIME' AS code FROM assessment_selection_event e WHERE length(e.recorded_at)<>20 OR e.recorded_at NOT GLOB '????-??-??T??:??:??Z' OR substr(e.recorded_at,1,4)<'0001' OR strftime('%Y-%m-%dT%H:%M:%SZ',e.recorded_at) IS NOT e.recorded_at OR date(e.recorded_at,'+0 days') IS NOT substr(e.recorded_at,1,10) OR EXISTS(SELECT 1 FROM version_snapshot v WHERE v.version_id=e.target_version AND v.issued_at>e.recorded_at)
UNION
SELECT e.event_id,'KIND' AS code FROM assessment_selection_event e WHERE e.kind NOT IN ('SELECT','WITHDRAW','CLEAR') OR (e.kind='CLEAR' AND e.target_version IS NOT NULL) OR (e.kind<>'CLEAR' AND e.target_version IS NULL)
UNION
SELECT e.event_id,'ASSESSMENT' AS code FROM assessment_selection_event e WHERE NOT EXISTS(SELECT 1 FROM artifact_typing t WHERE t.artifact_id=e.assessment_id AND t.native_class='RKM-C032')
UNION
SELECT e.event_id,'TARGET' AS code FROM assessment_selection_event e WHERE e.target_version IS NOT NULL AND NOT EXISTS(SELECT 1 FROM assessment_snapshot s JOIN version_snapshot v ON v.version_id=s.assessment_version_id WHERE v.is_issued=1 AND s.assessment_version_id=e.target_version AND s.assessment_id=e.assessment_id AND v.artifact_id=e.assessment_id)
UNION
SELECT e.event_id,'WITHDRAWN' AS code FROM assessment_selection_event e WHERE e.kind='SELECT' AND EXISTS(SELECT 1 FROM assessment_selection_event w WHERE w.kind='WITHDRAW' AND w.assessment_id=e.assessment_id AND w.decision_context_id=e.decision_context_id AND w.target_version=e.target_version AND w.ordinal<e.ordinal)
UNION
SELECT e.event_id,'SEQUENCE' AS code FROM assessment_selection_event e WHERE e.ordinal<=0 OR (SELECT count(*) FROM assessment_selection_event p WHERE p.ordinal<=e.ordinal)<>e.ordinal;

CREATE TRIGGER assessment_selection_insert BEFORE INSERT ON assessment_selection_event BEGIN
 SELECT CASE WHEN NEW.ordinal<>-1 THEN RAISE(ABORT,'ASL-ASSIGNED_SEQUENCE') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM assessment_selection_event WHERE event_id=NEW.event_id) THEN RAISE(ABORT,'ASL-DUPLICATE') END;
END;
CREATE TRIGGER assessment_selection_validate AFTER INSERT ON assessment_selection_event BEGIN
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_assessment_selection_invalid WHERE event_id=NEW.event_id AND code='PROVENANCE') THEN RAISE(ABORT,'ASL-PROVENANCE') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_assessment_selection_invalid WHERE event_id=NEW.event_id AND code='TIME') THEN RAISE(ABORT,'ASL-TIME') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_assessment_selection_invalid WHERE event_id=NEW.event_id AND code='KIND') THEN RAISE(ABORT,'ASL-KIND') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_assessment_selection_invalid WHERE event_id=NEW.event_id AND code='ASSESSMENT') THEN RAISE(ABORT,'ASL-ASSESSMENT') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_assessment_selection_invalid WHERE event_id=NEW.event_id AND code='TARGET') THEN RAISE(ABORT,'ASL-TARGET') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_assessment_selection_invalid WHERE event_id=NEW.event_id AND code='WITHDRAWN') THEN RAISE(ABORT,'ASL-WITHDRAWN') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_assessment_selection_invalid WHERE event_id=NEW.event_id AND code='SEQUENCE') THEN RAISE(ABORT,'ASL-SEQUENCE') END;
END;
CREATE TRIGGER assessment_selection_update BEFORE UPDATE ON assessment_selection_event BEGIN
 SELECT RAISE(ABORT,'ASL-IMMUTABLE');
END;
CREATE TRIGGER assessment_selection_delete BEFORE DELETE ON assessment_selection_event BEGIN
 SELECT RAISE(ABORT,'ASL-IMMUTABLE');
END;
