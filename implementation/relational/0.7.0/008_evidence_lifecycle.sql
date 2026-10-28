-- Supplementary application ledger. Native model and migrations 1..7 are unchanged.
CREATE TABLE evidence_lifecycle_event (
 ordinal INTEGER PRIMARY KEY AUTOINCREMENT CHECK(ordinal>0 AND ordinal<=922337203685477580),
 event_id TEXT NOT NULL UNIQUE,
 kind TEXT NOT NULL,
 artifact_id TEXT NOT NULL REFERENCES information_artifact(artifact_id),
 context_id TEXT,
 version_id TEXT REFERENCES version_snapshot(version_id),
 prior_version_id TEXT REFERENCES version_snapshot(version_id),
 actor_id TEXT NOT NULL,
 reason TEXT NOT NULL,
 recorded_at TEXT NOT NULL,
 source_record_id TEXT NOT NULL REFERENCES source_record(record_id),
 source_locator TEXT NOT NULL,
 interpretation_origin TEXT NOT NULL
) STRICT;
CREATE UNIQUE INDEX evidence_lifecycle_one_parent ON evidence_lifecycle_event(version_id) WHERE kind='CORRECT';
CREATE INDEX evidence_lifecycle_parent ON evidence_lifecycle_event(prior_version_id,version_id) WHERE kind='CORRECT';
CREATE INDEX evidence_lifecycle_context ON evidence_lifecycle_event(context_id,artifact_id,ordinal) WHERE kind IN ('SELECT','CLEAR');
CREATE INDEX evidence_lifecycle_withdrawal ON evidence_lifecycle_event(context_id,artifact_id,version_id,ordinal) WHERE kind='WITHDRAW';
CREATE VIEW v_evidence_lifecycle_ledger AS
 SELECT ordinal*10 AS sequence,event_id,kind,artifact_id,context_id,version_id,prior_version_id,
 actor_id,reason,recorded_at,source_record_id,source_locator,interpretation_origin
 FROM evidence_lifecycle_event;
CREATE VIEW v_evidence_lifecycle_invalid AS
 WITH RECURSIVE walk(root,id) AS (
 SELECT version_id,prior_version_id FROM evidence_lifecycle_event WHERE kind='CORRECT'
 UNION SELECT w.root,e.prior_version_id FROM walk w
 JOIN evidence_lifecycle_event e ON e.version_id=w.id AND e.kind='CORRECT'
 )
 SELECT e.event_id,'MISSING_PROVENANCE' AS code FROM evidence_lifecycle_event e
 WHERE length(trim(e.event_id))=0 OR length(trim(e.actor_id))=0 OR length(trim(e.reason))=0
 OR length(trim(e.source_locator))=0 OR length(trim(e.interpretation_origin))=0
 OR NOT EXISTS(SELECT 1 FROM source_record s WHERE s.record_id=e.source_record_id)
 UNION SELECT e.event_id,'INVALID_RECORDED_TIME' FROM evidence_lifecycle_event e
 WHERE length(e.recorded_at)<>20 OR e.recorded_at NOT GLOB '????-??-??T??:??:??Z'
 OR substr(e.recorded_at,1,4)<'0001'
 OR strftime('%Y-%m-%dT%H:%M:%SZ',e.recorded_at) IS NOT e.recorded_at
 OR date(e.recorded_at,'+0 days') IS NOT substr(e.recorded_at,1,10)
 UNION SELECT e.event_id,'INVALID_EVENT' FROM evidence_lifecycle_event e
 WHERE e.kind NOT IN ('CORRECT','SELECT','WITHDRAW','CLEAR')
 OR (e.kind='CORRECT' AND (e.context_id IS NOT NULL OR e.version_id IS NULL OR e.prior_version_id IS NULL))
 OR (e.kind IN ('SELECT','WITHDRAW') AND (e.version_id IS NULL OR e.prior_version_id IS NOT NULL))
 OR (e.kind='CLEAR' AND (e.version_id IS NOT NULL OR e.prior_version_id IS NOT NULL))
 UNION SELECT e.event_id,'INVALID_CONTEXT' FROM evidence_lifecycle_event e
 WHERE e.kind<>'CORRECT' AND (e.context_id IS NULL OR length(trim(e.context_id))=0)
 UNION SELECT e.event_id,'UNKNOWN_ENDPOINT' FROM evidence_lifecycle_event e
 WHERE (e.version_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM version_snapshot v WHERE v.version_id=e.version_id))
 OR (e.prior_version_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM version_snapshot v WHERE v.version_id=e.prior_version_id))
 OR NOT EXISTS(SELECT 1 FROM information_artifact a WHERE a.artifact_id=e.artifact_id)
 UNION SELECT e.event_id,'UNISSUED_ENDPOINT' FROM evidence_lifecycle_event e
 WHERE EXISTS(SELECT 1 FROM version_snapshot v WHERE v.version_id IN (e.version_id,e.prior_version_id) AND v.is_issued<>1)
 UNION SELECT e.event_id,'UNSUPPORTED_ENDPOINT_FAMILY' FROM evidence_lifecycle_event e
 WHERE NOT EXISTS(SELECT 1 FROM evidence_reference_type t WHERE t.artifact_id=e.artifact_id)
 OR (e.version_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM evidence_snapshot r WHERE r.version_id=e.version_id))
 OR (e.prior_version_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM evidence_snapshot r WHERE r.version_id=e.prior_version_id))
 UNION SELECT e.event_id,'CROSS_ARTIFACT' FROM evidence_lifecycle_event e
 WHERE EXISTS(SELECT 1 FROM version_snapshot v WHERE v.version_id IN (e.version_id,e.prior_version_id) AND v.artifact_id<>e.artifact_id)
 UNION SELECT e.event_id,'SELF_CORRECTION' FROM evidence_lifecycle_event e
 WHERE e.kind='CORRECT' AND e.version_id=e.prior_version_id
 UNION SELECT e.event_id,'PARENT_ALREADY_DECLARED' FROM evidence_lifecycle_event e
 WHERE e.kind='CORRECT' AND (SELECT count(*) FROM evidence_lifecycle_event p WHERE p.kind='CORRECT' AND p.version_id=e.version_id)>1
 UNION SELECT e.event_id,'CYCLE' FROM evidence_lifecycle_event e
 WHERE e.kind='CORRECT' AND EXISTS(SELECT 1 FROM walk WHERE root=e.version_id AND root=id)
 UNION SELECT e.event_id,'WITHDRAWN_IN_CONTEXT' FROM evidence_lifecycle_event e
 WHERE e.kind='SELECT' AND EXISTS(SELECT 1 FROM evidence_lifecycle_event w
 WHERE w.kind='WITHDRAW' AND w.context_id=e.context_id AND w.artifact_id=e.artifact_id
 AND w.version_id=e.version_id AND w.ordinal<e.ordinal)
 UNION SELECT e.event_id,'INVALID_SEQUENCE' FROM evidence_lifecycle_event e
 WHERE e.ordinal<=0 OR e.ordinal>922337203685477580
 OR (SELECT count(*) FROM evidence_lifecycle_event p WHERE p.ordinal<=e.ordinal)<>e.ordinal;
CREATE TRIGGER evidence_lifecycle_insert BEFORE INSERT ON evidence_lifecycle_event BEGIN
 SELECT CASE WHEN EXISTS(SELECT 1 FROM evidence_lifecycle_event WHERE event_id=NEW.event_id)
 THEN RAISE(ABORT,'ELC-DUPLICATE_EVENT_ID') END;
 SELECT CASE WHEN NEW.kind='CORRECT' AND EXISTS(
 SELECT 1 FROM evidence_lifecycle_event WHERE kind='CORRECT' AND version_id=NEW.version_id)
 THEN RAISE(ABORT,'ELC-PARENT_ALREADY_DECLARED') END;
END;
CREATE TRIGGER evidence_lifecycle_validate AFTER INSERT ON evidence_lifecycle_event BEGIN
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_evidence_lifecycle_invalid WHERE event_id=NEW.event_id AND code='MISSING_PROVENANCE') THEN RAISE(ABORT,'ELC-MISSING_PROVENANCE') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_evidence_lifecycle_invalid WHERE event_id=NEW.event_id AND code='INVALID_RECORDED_TIME') THEN RAISE(ABORT,'ELC-INVALID_RECORDED_TIME') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_evidence_lifecycle_invalid WHERE event_id=NEW.event_id AND code='INVALID_EVENT') THEN RAISE(ABORT,'ELC-INVALID_EVENT') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_evidence_lifecycle_invalid WHERE event_id=NEW.event_id AND code='INVALID_CONTEXT') THEN RAISE(ABORT,'ELC-INVALID_CONTEXT') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_evidence_lifecycle_invalid WHERE event_id=NEW.event_id AND code='UNKNOWN_ENDPOINT') THEN RAISE(ABORT,'ELC-UNKNOWN_ENDPOINT') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_evidence_lifecycle_invalid WHERE event_id=NEW.event_id AND code='UNISSUED_ENDPOINT') THEN RAISE(ABORT,'ELC-UNISSUED_ENDPOINT') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_evidence_lifecycle_invalid WHERE event_id=NEW.event_id AND code='UNSUPPORTED_ENDPOINT_FAMILY') THEN RAISE(ABORT,'ELC-UNSUPPORTED_ENDPOINT_FAMILY') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_evidence_lifecycle_invalid WHERE event_id=NEW.event_id AND code='CROSS_ARTIFACT') THEN RAISE(ABORT,'ELC-CROSS_ARTIFACT') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_evidence_lifecycle_invalid WHERE event_id=NEW.event_id AND code='SELF_CORRECTION') THEN RAISE(ABORT,'ELC-SELF_CORRECTION') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_evidence_lifecycle_invalid WHERE event_id=NEW.event_id AND code='PARENT_ALREADY_DECLARED') THEN RAISE(ABORT,'ELC-PARENT_ALREADY_DECLARED') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_evidence_lifecycle_invalid WHERE event_id=NEW.event_id AND code='CYCLE') THEN RAISE(ABORT,'ELC-CYCLE') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_evidence_lifecycle_invalid WHERE event_id=NEW.event_id AND code='WITHDRAWN_IN_CONTEXT') THEN RAISE(ABORT,'ELC-WITHDRAWN_IN_CONTEXT') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_evidence_lifecycle_invalid WHERE event_id=NEW.event_id AND code='INVALID_SEQUENCE') THEN RAISE(ABORT,'ELC-INVALID_SEQUENCE') END;
END;
CREATE TRIGGER evidence_lifecycle_update BEFORE UPDATE ON evidence_lifecycle_event BEGIN
 SELECT RAISE(ABORT,'ELC-IMMUTABLE');
END;
CREATE TRIGGER evidence_lifecycle_delete BEFORE DELETE ON evidence_lifecycle_event BEGIN
 SELECT RAISE(ABORT,'ELC-IMMUTABLE');
END;
