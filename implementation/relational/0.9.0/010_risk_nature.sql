-- SQLite schema 10: immutable source-qualified risk-nature task.

CREATE TABLE nature_membership (
 artifact_id TEXT PRIMARY KEY REFERENCES information_artifact(artifact_id),
 native_class TEXT NOT NULL CHECK(native_class IN ('RKM-C005','RKM-C006','RKM-C018','RKM-X02')),
 scheme_id TEXT REFERENCES nature_membership(artifact_id), code TEXT,
 UNIQUE(scheme_id,code),
 CHECK((native_class='RKM-C006' AND scheme_id IS NOT NULL AND code IS NOT NULL AND length(trim(code,char(9)||char(10)||char(13)||' '))>0)
 OR (native_class<>'RKM-C006' AND scheme_id IS NULL AND code IS NULL))) STRICT;

CREATE TABLE nature_support (
 version_id TEXT PRIMARY KEY REFERENCES version_snapshot(version_id),
 artifact_id TEXT NOT NULL REFERENCES nature_membership(artifact_id),
 native_class TEXT NOT NULL,
 narrative TEXT NOT NULL,
 source_record_id TEXT NOT NULL REFERENCES source_record(record_id),
 source_locator TEXT NOT NULL,
 interpretation_origin TEXT NOT NULL,
 recorded_at TEXT NOT NULL,
 code TEXT,
 scheme_version_id TEXT REFERENCES nature_support(version_id)) STRICT;

CREATE TABLE nature_context (
 version_id TEXT PRIMARY KEY REFERENCES version_snapshot(version_id),
 artifact_id TEXT NOT NULL REFERENCES information_artifact(artifact_id),
 narrative TEXT NOT NULL,
 source_record_id TEXT NOT NULL REFERENCES source_record(record_id),
 source_locator TEXT NOT NULL,
 interpretation_origin TEXT NOT NULL,
 recorded_at TEXT NOT NULL) STRICT;

CREATE TABLE nature_snapshot (
 version_id TEXT PRIMARY KEY REFERENCES version_snapshot(version_id),
 artifact_id TEXT NOT NULL REFERENCES nature_membership(artifact_id),
 case_id TEXT NOT NULL REFERENCES risk_case(case_id),
 term_version_id TEXT NOT NULL REFERENCES nature_support(version_id),
 context_version_id TEXT REFERENCES nature_context(version_id),
 narrative TEXT NOT NULL,
 source_record_id TEXT NOT NULL REFERENCES source_record(record_id),
 source_locator TEXT NOT NULL,
 interpretation_origin TEXT NOT NULL,
 recorded_at TEXT NOT NULL) STRICT;

CREATE TABLE nature_entry (
 version_id TEXT PRIMARY KEY REFERENCES version_snapshot(version_id),
 entry_id TEXT NOT NULL REFERENCES register_entry(entry_id),
 previous_version_id TEXT REFERENCES version_snapshot(version_id),
 narrative TEXT NOT NULL,
 source_record_id TEXT NOT NULL REFERENCES source_record(record_id),
 source_locator TEXT NOT NULL,
 interpretation_origin TEXT NOT NULL,
 recorded_at TEXT NOT NULL) STRICT;

CREATE TABLE nature_objective (
 context_version_id TEXT NOT NULL REFERENCES nature_context(version_id),
 objective_version_id TEXT NOT NULL REFERENCES nature_support(version_id),
 objective_id TEXT NOT NULL REFERENCES nature_membership(artifact_id),
 PRIMARY KEY(context_version_id,objective_version_id), UNIQUE(context_version_id,objective_id)) STRICT;

CREATE TABLE nature_entry_link (
 entry_version_id TEXT NOT NULL REFERENCES nature_entry(version_id),
 nature_version_id TEXT NOT NULL REFERENCES nature_snapshot(version_id),
 PRIMARY KEY(entry_version_id,nature_version_id)) STRICT;

CREATE TABLE nature_correction (
 corrected_version_id TEXT PRIMARY KEY REFERENCES nature_snapshot(version_id),
 prior_version_id TEXT NOT NULL REFERENCES nature_snapshot(version_id),
 actor TEXT NOT NULL, reason TEXT NOT NULL,
 source_record_id TEXT NOT NULL REFERENCES source_record(record_id),
 source_locator TEXT NOT NULL, interpretation_origin TEXT NOT NULL, recorded_at TEXT NOT NULL) STRICT;

CREATE VIEW v_nature_expected_payload AS
SELECT t.version_id,json_object('artifact_id',t.artifact_id,'code',t.code,'interpretation_origin',t.interpretation_origin,'narrative',t.narrative,'native_class',t.native_class,'recorded_at',t.recorded_at,'scheme_version_id',t.scheme_version_id,'source_locator',t.source_locator,'source_record_id',t.source_record_id,'version_id',t.version_id) AS expected_payload FROM nature_support t WHERE t.native_class='RKM-C006'
UNION ALL
SELECT t.version_id,json_object('artifact_id',t.artifact_id,'interpretation_origin',t.interpretation_origin,'narrative',t.narrative,'native_class',t.native_class,'recorded_at',t.recorded_at,'source_locator',t.source_locator,'source_record_id',t.source_record_id,'version_id',t.version_id) AS expected_payload FROM nature_support t WHERE t.native_class<>'RKM-C006'
UNION ALL
SELECT t.version_id,json_object('artifact_id',t.artifact_id,'interpretation_origin',t.interpretation_origin,'narrative',t.narrative,'objective_version_ids',json((SELECT json_group_array(objective_version_id) FROM (SELECT objective_version_id FROM nature_objective o WHERE o.context_version_id=t.version_id ORDER BY objective_version_id))),'recorded_at',t.recorded_at,'source_locator',t.source_locator,'source_record_id',t.source_record_id,'version_id',t.version_id) AS expected_payload FROM nature_context t WHERE 1
UNION ALL
SELECT t.version_id,json_object('artifact_id',t.artifact_id,'case_id',t.case_id,'context_version_id',t.context_version_id,'interpretation_origin',t.interpretation_origin,'narrative',t.narrative,'recorded_at',t.recorded_at,'source_locator',t.source_locator,'source_record_id',t.source_record_id,'term_version_id',t.term_version_id,'version_id',t.version_id) AS expected_payload FROM nature_snapshot t WHERE 1
UNION ALL
SELECT t.version_id,json_object('entry_id',t.entry_id,'interpretation_origin',t.interpretation_origin,'narrative',t.narrative,'nature_version_ids',json((SELECT json_group_array(nature_version_id) FROM (SELECT nature_version_id FROM nature_entry_link l WHERE l.entry_version_id=t.version_id ORDER BY nature_version_id))),'previous_version_id',t.previous_version_id,'recorded_at',t.recorded_at,'source_locator',t.source_locator,'source_record_id',t.source_record_id,'version_id',t.version_id) AS expected_payload FROM nature_entry t WHERE 1;

CREATE VIEW v_nature_invalid AS
SELECT t.version_id AS version_id,'PROVENANCE' AS code FROM nature_support t  WHERE length(trim(t.narrative,char(9)||char(10)||char(13)||' '))=0 OR length(trim(t.source_locator,char(9)||char(10)||char(13)||' '))=0 OR length(trim(t.interpretation_origin,char(9)||char(10)||char(13)||' '))=0
UNION ALL
SELECT t.version_id AS version_id,'TIME' AS code FROM nature_support t  WHERE length(t.recorded_at)<>20 OR substr(t.recorded_at,1,4)<'0001' OR t.recorded_at NOT GLOB '????-??-??T??:??:??Z' OR strftime('%Y-%m-%dT%H:%M:%SZ',t.recorded_at) IS NOT t.recorded_at OR date(t.recorded_at,'+0 days') IS NOT substr(t.recorded_at,1,10)
UNION ALL
SELECT t.version_id AS version_id,'OWNER' AS code FROM nature_support t JOIN version_snapshot v USING(version_id) WHERE t.artifact_id IS NOT v.artifact_id OR t.source_record_id IS NOT v.source_record_id OR (v.is_issued=1 AND t.recorded_at IS NOT v.issued_at)
UNION ALL
SELECT t.version_id AS version_id,'PROVENANCE' AS code FROM nature_context t  WHERE length(trim(t.narrative,char(9)||char(10)||char(13)||' '))=0 OR length(trim(t.source_locator,char(9)||char(10)||char(13)||' '))=0 OR length(trim(t.interpretation_origin,char(9)||char(10)||char(13)||' '))=0
UNION ALL
SELECT t.version_id AS version_id,'TIME' AS code FROM nature_context t  WHERE length(t.recorded_at)<>20 OR substr(t.recorded_at,1,4)<'0001' OR t.recorded_at NOT GLOB '????-??-??T??:??:??Z' OR strftime('%Y-%m-%dT%H:%M:%SZ',t.recorded_at) IS NOT t.recorded_at OR date(t.recorded_at,'+0 days') IS NOT substr(t.recorded_at,1,10)
UNION ALL
SELECT t.version_id AS version_id,'OWNER' AS code FROM nature_context t JOIN version_snapshot v USING(version_id) WHERE t.artifact_id IS NOT v.artifact_id OR t.source_record_id IS NOT v.source_record_id OR (v.is_issued=1 AND t.recorded_at IS NOT v.issued_at)
UNION ALL
SELECT t.version_id AS version_id,'PROVENANCE' AS code FROM nature_snapshot t  WHERE length(trim(t.narrative,char(9)||char(10)||char(13)||' '))=0 OR length(trim(t.source_locator,char(9)||char(10)||char(13)||' '))=0 OR length(trim(t.interpretation_origin,char(9)||char(10)||char(13)||' '))=0
UNION ALL
SELECT t.version_id AS version_id,'TIME' AS code FROM nature_snapshot t  WHERE length(t.recorded_at)<>20 OR substr(t.recorded_at,1,4)<'0001' OR t.recorded_at NOT GLOB '????-??-??T??:??:??Z' OR strftime('%Y-%m-%dT%H:%M:%SZ',t.recorded_at) IS NOT t.recorded_at OR date(t.recorded_at,'+0 days') IS NOT substr(t.recorded_at,1,10)
UNION ALL
SELECT t.version_id AS version_id,'OWNER' AS code FROM nature_snapshot t JOIN version_snapshot v USING(version_id) WHERE t.artifact_id IS NOT v.artifact_id OR t.source_record_id IS NOT v.source_record_id OR (v.is_issued=1 AND t.recorded_at IS NOT v.issued_at)
UNION ALL
SELECT t.version_id AS version_id,'PROVENANCE' AS code FROM nature_entry t  WHERE length(trim(t.narrative,char(9)||char(10)||char(13)||' '))=0 OR length(trim(t.source_locator,char(9)||char(10)||char(13)||' '))=0 OR length(trim(t.interpretation_origin,char(9)||char(10)||char(13)||' '))=0
UNION ALL
SELECT t.version_id AS version_id,'TIME' AS code FROM nature_entry t  WHERE length(t.recorded_at)<>20 OR substr(t.recorded_at,1,4)<'0001' OR t.recorded_at NOT GLOB '????-??-??T??:??:??Z' OR strftime('%Y-%m-%dT%H:%M:%SZ',t.recorded_at) IS NOT t.recorded_at OR date(t.recorded_at,'+0 days') IS NOT substr(t.recorded_at,1,10)
UNION ALL
SELECT t.version_id AS version_id,'OWNER' AS code FROM nature_entry t JOIN version_snapshot v USING(version_id) WHERE t.entry_id IS NOT v.artifact_id OR t.source_record_id IS NOT v.source_record_id OR (v.is_issued=1 AND t.recorded_at IS NOT v.issued_at)
UNION ALL
SELECT p.version_id,'PAYLOAD' FROM v_nature_expected_payload p JOIN version_snapshot v USING(version_id) WHERE json(v.payload_json) IS NOT p.expected_payload
UNION ALL
SELECT t.version_id AS version_id,'IDENTITY' AS code FROM nature_support t LEFT JOIN nature_membership m USING(artifact_id) WHERE m.native_class IS NOT t.native_class OR t.native_class NOT IN ('RKM-C006','RKM-C018','RKM-X02')
UNION ALL
SELECT t.version_id AS version_id,'TERM_VERSION' AS code FROM nature_support t LEFT JOIN nature_support s ON s.version_id=t.scheme_version_id LEFT JOIN version_snapshot v ON v.version_id=t.scheme_version_id JOIN nature_membership m ON m.artifact_id=t.artifact_id WHERE (t.native_class='RKM-C006' AND (s.native_class IS NOT 'RKM-C018' OR v.is_issued IS NOT 1 OR s.artifact_id IS NOT m.scheme_id OR t.code IS NOT m.code)) OR (t.native_class<>'RKM-C006' AND (t.code IS NOT NULL OR t.scheme_version_id IS NOT NULL))
UNION ALL
SELECT t.version_id AS version_id,'TIME' AS code FROM nature_support t JOIN nature_support s ON s.version_id=t.scheme_version_id WHERE s.recorded_at>t.recorded_at
UNION ALL
SELECT t.version_id AS version_id,'CONTEXT_VERSION' AS code FROM nature_context t JOIN information_artifact a USING(artifact_id) WHERE a.kind IS NOT 'RKM-C002'
UNION ALL
SELECT t.context_version_id AS version_id,'OBJECTIVE_VERSION' AS code FROM nature_objective t LEFT JOIN nature_support s ON s.version_id=t.objective_version_id LEFT JOIN version_snapshot v ON v.version_id=t.objective_version_id WHERE s.native_class IS NOT 'RKM-X02' OR s.artifact_id IS NOT t.objective_id OR v.is_issued IS NOT 1
UNION ALL
SELECT t.context_version_id AS version_id,'TIME' AS code FROM nature_objective t JOIN nature_support s ON s.version_id=t.objective_version_id JOIN nature_context c ON c.version_id=t.context_version_id WHERE s.recorded_at>c.recorded_at
UNION ALL
SELECT t.version_id AS version_id,'IDENTITY' AS code FROM nature_snapshot t LEFT JOIN nature_membership m USING(artifact_id) WHERE m.native_class IS NOT 'RKM-C005' OR EXISTS(SELECT 1 FROM nature_snapshot q WHERE q.artifact_id=t.artifact_id AND q.case_id<>t.case_id)
UNION ALL
SELECT t.version_id AS version_id,'TERM_VERSION' AS code FROM nature_snapshot t LEFT JOIN nature_support s ON s.version_id=t.term_version_id LEFT JOIN version_snapshot v ON v.version_id=t.term_version_id WHERE s.native_class IS NOT 'RKM-C006' OR v.is_issued IS NOT 1
UNION ALL
SELECT t.version_id AS version_id,'CONTEXT_VERSION' AS code FROM nature_snapshot t LEFT JOIN nature_context c ON c.version_id=t.context_version_id LEFT JOIN version_snapshot v ON v.version_id=t.context_version_id WHERE t.context_version_id IS NOT NULL AND (c.version_id IS NULL OR v.is_issued IS NOT 1)
UNION ALL
SELECT t.version_id AS version_id,'TIME' AS code FROM nature_snapshot t JOIN nature_support s ON s.version_id=t.term_version_id LEFT JOIN nature_context c ON c.version_id=t.context_version_id WHERE s.recorded_at>t.recorded_at OR c.recorded_at>t.recorded_at
UNION ALL
SELECT t.version_id AS version_id,'RECORDING' AS code FROM nature_snapshot t JOIN version_snapshot v USING(version_id) WHERE v.is_issued=1 AND (NOT EXISTS(SELECT 1 FROM nature_entry_link l WHERE l.nature_version_id=t.version_id) OR EXISTS(SELECT 1 FROM nature_entry_link l JOIN version_snapshot e ON e.version_id=l.entry_version_id WHERE l.nature_version_id=t.version_id AND e.is_issued<>1))
UNION ALL
SELECT t.version_id AS version_id,'RECORDING' AS code FROM nature_entry t JOIN version_snapshot v USING(version_id) WHERE t.previous_version_id IS NOT v.previous_version_id OR t.entry_id IS NOT v.entry_id OR NOT EXISTS(SELECT 1 FROM nature_entry_link l WHERE l.entry_version_id=t.version_id)
UNION ALL
SELECT t.entry_version_id AS version_id,'RECORDING' AS code FROM nature_entry_link t JOIN nature_entry q ON q.version_id=t.entry_version_id JOIN register_entry e ON e.entry_id=q.entry_id JOIN nature_snapshot n ON n.version_id=t.nature_version_id JOIN version_snapshot v ON v.version_id=t.entry_version_id JOIN version_snapshot nv ON nv.version_id=t.nature_version_id WHERE e.case_id<>n.case_id OR (v.is_issued=1 AND nv.is_issued<>1)
UNION ALL
SELECT t.version_id AS version_id,'TIME' AS code FROM nature_entry t JOIN version_snapshot p ON p.version_id=t.previous_version_id WHERE p.issued_at>t.recorded_at
UNION ALL
SELECT t.corrected_version_id AS version_id,'CORRECTION' AS code FROM nature_correction t JOIN nature_snapshot a ON a.version_id=t.corrected_version_id JOIN nature_snapshot p ON p.version_id=t.prior_version_id JOIN version_snapshot av ON av.version_id=a.version_id JOIN version_snapshot pv ON pv.version_id=p.version_id WHERE a.artifact_id<>p.artifact_id OR a.case_id<>p.case_id OR t.corrected_version_id=t.prior_version_id OR av.is_issued<>1 OR pv.is_issued<>1
UNION ALL
SELECT t.corrected_version_id AS version_id,'PROVENANCE' AS code FROM nature_correction t  WHERE length(trim(t.actor,char(9)||char(10)||char(13)||' '))=0 OR length(trim(t.reason,char(9)||char(10)||char(13)||' '))=0 OR length(trim(t.source_locator,char(9)||char(10)||char(13)||' '))=0 OR length(trim(t.interpretation_origin,char(9)||char(10)||char(13)||' '))=0
UNION ALL
SELECT t.corrected_version_id AS version_id,'TIME' AS code FROM nature_correction t JOIN nature_snapshot a ON a.version_id=t.corrected_version_id JOIN nature_snapshot p ON p.version_id=t.prior_version_id WHERE length(t.recorded_at)<>20 OR t.recorded_at NOT GLOB '????-??-??T??:??:??Z' OR strftime('%Y-%m-%dT%H:%M:%SZ',t.recorded_at) IS NOT t.recorded_at OR date(t.recorded_at,'+0 days') IS NOT substr(t.recorded_at,1,10) OR t.recorded_at<a.recorded_at OR t.recorded_at<p.recorded_at;

CREATE TRIGGER nature_membership_update BEFORE UPDATE ON nature_membership BEGIN SELECT RAISE(ABORT,'NRA-IMMUTABLE'); END;

CREATE TRIGGER nature_membership_delete BEFORE DELETE ON nature_membership BEGIN SELECT RAISE(ABORT,'NRA-IMMUTABLE'); END;

CREATE TRIGGER nature_membership_duplicate BEFORE INSERT ON nature_membership WHEN EXISTS(SELECT 1 FROM nature_membership WHERE artifact_id=NEW.artifact_id) BEGIN SELECT RAISE(ABORT,'NRA-IDENTITY'); END;

CREATE TRIGGER nature_support_update BEFORE UPDATE ON nature_support BEGIN SELECT RAISE(ABORT,'NRA-IMMUTABLE'); END;

CREATE TRIGGER nature_support_delete BEFORE DELETE ON nature_support BEGIN SELECT RAISE(ABORT,'NRA-IMMUTABLE'); END;

CREATE TRIGGER nature_support_duplicate BEFORE INSERT ON nature_support WHEN EXISTS(SELECT 1 FROM nature_support WHERE version_id=NEW.version_id) BEGIN SELECT RAISE(ABORT,'NRA-IDENTITY'); END;

CREATE TRIGGER nature_support_version_id_frozen BEFORE INSERT ON nature_support WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.version_id AND is_issued=1) BEGIN SELECT RAISE(ABORT,'NRA-IMMUTABLE'); END;

CREATE TRIGGER nature_context_update BEFORE UPDATE ON nature_context BEGIN SELECT RAISE(ABORT,'NRA-IMMUTABLE'); END;

CREATE TRIGGER nature_context_delete BEFORE DELETE ON nature_context BEGIN SELECT RAISE(ABORT,'NRA-IMMUTABLE'); END;

CREATE TRIGGER nature_context_duplicate BEFORE INSERT ON nature_context WHEN EXISTS(SELECT 1 FROM nature_context WHERE version_id=NEW.version_id) BEGIN SELECT RAISE(ABORT,'NRA-IDENTITY'); END;

CREATE TRIGGER nature_context_version_id_frozen BEFORE INSERT ON nature_context WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.version_id AND is_issued=1) BEGIN SELECT RAISE(ABORT,'NRA-IMMUTABLE'); END;

CREATE TRIGGER nature_snapshot_update BEFORE UPDATE ON nature_snapshot BEGIN SELECT RAISE(ABORT,'NRA-IMMUTABLE'); END;

CREATE TRIGGER nature_snapshot_delete BEFORE DELETE ON nature_snapshot BEGIN SELECT RAISE(ABORT,'NRA-IMMUTABLE'); END;

CREATE TRIGGER nature_snapshot_duplicate BEFORE INSERT ON nature_snapshot WHEN EXISTS(SELECT 1 FROM nature_snapshot WHERE version_id=NEW.version_id) BEGIN SELECT RAISE(ABORT,'NRA-IDENTITY'); END;

CREATE TRIGGER nature_snapshot_version_id_frozen BEFORE INSERT ON nature_snapshot WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.version_id AND is_issued=1) BEGIN SELECT RAISE(ABORT,'NRA-IMMUTABLE'); END;

CREATE TRIGGER nature_entry_update BEFORE UPDATE ON nature_entry BEGIN SELECT RAISE(ABORT,'NRA-IMMUTABLE'); END;

CREATE TRIGGER nature_entry_delete BEFORE DELETE ON nature_entry BEGIN SELECT RAISE(ABORT,'NRA-IMMUTABLE'); END;

CREATE TRIGGER nature_entry_duplicate BEFORE INSERT ON nature_entry WHEN EXISTS(SELECT 1 FROM nature_entry WHERE version_id=NEW.version_id) BEGIN SELECT RAISE(ABORT,'NRA-IDENTITY'); END;

CREATE TRIGGER nature_entry_version_id_frozen BEFORE INSERT ON nature_entry WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.version_id AND is_issued=1) BEGIN SELECT RAISE(ABORT,'NRA-IMMUTABLE'); END;

CREATE TRIGGER nature_objective_update BEFORE UPDATE ON nature_objective BEGIN SELECT RAISE(ABORT,'NRA-IMMUTABLE'); END;

CREATE TRIGGER nature_objective_delete BEFORE DELETE ON nature_objective BEGIN SELECT RAISE(ABORT,'NRA-IMMUTABLE'); END;

CREATE TRIGGER nature_objective_duplicate BEFORE INSERT ON nature_objective WHEN EXISTS(SELECT 1 FROM nature_objective WHERE context_version_id=NEW.context_version_id AND objective_version_id=NEW.objective_version_id) BEGIN SELECT RAISE(ABORT,'NRA-IDENTITY'); END;

CREATE TRIGGER nature_objective_context_version_id_frozen BEFORE INSERT ON nature_objective WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.context_version_id AND is_issued=1) BEGIN SELECT RAISE(ABORT,'NRA-IMMUTABLE'); END;

CREATE TRIGGER nature_entry_link_update BEFORE UPDATE ON nature_entry_link BEGIN SELECT RAISE(ABORT,'NRA-IMMUTABLE'); END;

CREATE TRIGGER nature_entry_link_delete BEFORE DELETE ON nature_entry_link BEGIN SELECT RAISE(ABORT,'NRA-IMMUTABLE'); END;

CREATE TRIGGER nature_entry_link_duplicate BEFORE INSERT ON nature_entry_link WHEN EXISTS(SELECT 1 FROM nature_entry_link WHERE entry_version_id=NEW.entry_version_id AND nature_version_id=NEW.nature_version_id) BEGIN SELECT RAISE(ABORT,'NRA-IDENTITY'); END;

CREATE TRIGGER nature_entry_link_entry_version_id_frozen BEFORE INSERT ON nature_entry_link WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.entry_version_id AND is_issued=1) BEGIN SELECT RAISE(ABORT,'NRA-IMMUTABLE'); END;

CREATE TRIGGER nature_entry_link_nature_version_id_frozen BEFORE INSERT ON nature_entry_link WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.nature_version_id AND is_issued=1) BEGIN SELECT RAISE(ABORT,'NRA-IMMUTABLE'); END;

CREATE TRIGGER nature_correction_update BEFORE UPDATE ON nature_correction BEGIN SELECT RAISE(ABORT,'NRA-IMMUTABLE'); END;

CREATE TRIGGER nature_correction_delete BEFORE DELETE ON nature_correction BEGIN SELECT RAISE(ABORT,'NRA-IMMUTABLE'); END;

CREATE TRIGGER nature_correction_duplicate BEFORE INSERT ON nature_correction WHEN EXISTS(SELECT 1 FROM nature_correction WHERE corrected_version_id=NEW.corrected_version_id) BEGIN SELECT RAISE(ABORT,'NRA-CORRECTION'); END;

CREATE TRIGGER nature_membership_validate BEFORE INSERT ON nature_membership BEGIN
 SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM information_artifact WHERE artifact_id=NEW.artifact_id AND kind='RKM-C014')
 OR EXISTS(SELECT 1 FROM version_snapshot WHERE artifact_id=NEW.artifact_id AND is_issued=1)
 OR EXISTS(SELECT 1 FROM artifact_typing WHERE artifact_id=NEW.artifact_id)
 OR EXISTS(SELECT 1 FROM knowledge_type WHERE artifact_id=NEW.artifact_id)
 OR EXISTS(SELECT 1 FROM evidence_reference_type WHERE artifact_id=NEW.artifact_id)
 OR (NEW.native_class='RKM-C006' AND (NOT EXISTS(SELECT 1 FROM nature_membership WHERE artifact_id=NEW.scheme_id AND native_class='RKM-C018') OR EXISTS(SELECT 1 FROM nature_membership WHERE scheme_id=NEW.scheme_id AND code=NEW.code)))
 THEN RAISE(ABORT,'NRA-IDENTITY') END;
 END;

CREATE TRIGGER nature_exclusive_artifact_typing BEFORE INSERT ON artifact_typing WHEN EXISTS(SELECT 1 FROM nature_membership WHERE artifact_id=NEW.artifact_id) BEGIN SELECT RAISE(ABORT,'NRA-IDENTITY'); END;

CREATE TRIGGER nature_exclusive_knowledge_type BEFORE INSERT ON knowledge_type WHEN EXISTS(SELECT 1 FROM nature_membership WHERE artifact_id=NEW.artifact_id) BEGIN SELECT RAISE(ABORT,'NRA-IDENTITY'); END;

CREATE TRIGGER nature_exclusive_evidence_reference_type BEFORE INSERT ON evidence_reference_type WHEN EXISTS(SELECT 1 FROM nature_membership WHERE artifact_id=NEW.artifact_id) BEGIN SELECT RAISE(ABORT,'NRA-IDENTITY'); END;

CREATE TRIGGER nature_support_validate AFTER INSERT ON nature_support BEGIN SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.version_id AND code='PROVENANCE') THEN RAISE(ABORT,'NRA-PROVENANCE') END; SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.version_id AND code='TIME') THEN RAISE(ABORT,'NRA-TIME') END; SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.version_id AND code='OWNER') THEN RAISE(ABORT,'NRA-OWNER') END; SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.version_id AND code='IDENTITY') THEN RAISE(ABORT,'NRA-IDENTITY') END; SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.version_id AND code='TERM_VERSION') THEN RAISE(ABORT,'NRA-TERM_VERSION') END; SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.version_id AND code='CONTEXT_VERSION') THEN RAISE(ABORT,'NRA-CONTEXT_VERSION') END; END;

CREATE TRIGGER nature_context_validate AFTER INSERT ON nature_context BEGIN SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.version_id AND code='PROVENANCE') THEN RAISE(ABORT,'NRA-PROVENANCE') END; SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.version_id AND code='TIME') THEN RAISE(ABORT,'NRA-TIME') END; SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.version_id AND code='OWNER') THEN RAISE(ABORT,'NRA-OWNER') END; SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.version_id AND code='IDENTITY') THEN RAISE(ABORT,'NRA-IDENTITY') END; SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.version_id AND code='TERM_VERSION') THEN RAISE(ABORT,'NRA-TERM_VERSION') END; SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.version_id AND code='CONTEXT_VERSION') THEN RAISE(ABORT,'NRA-CONTEXT_VERSION') END; END;

CREATE TRIGGER nature_snapshot_validate AFTER INSERT ON nature_snapshot BEGIN SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.version_id AND code='PROVENANCE') THEN RAISE(ABORT,'NRA-PROVENANCE') END; SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.version_id AND code='TIME') THEN RAISE(ABORT,'NRA-TIME') END; SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.version_id AND code='OWNER') THEN RAISE(ABORT,'NRA-OWNER') END; SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.version_id AND code='IDENTITY') THEN RAISE(ABORT,'NRA-IDENTITY') END; SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.version_id AND code='TERM_VERSION') THEN RAISE(ABORT,'NRA-TERM_VERSION') END; SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.version_id AND code='CONTEXT_VERSION') THEN RAISE(ABORT,'NRA-CONTEXT_VERSION') END; END;

CREATE TRIGGER nature_entry_validate AFTER INSERT ON nature_entry BEGIN SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.version_id AND code='PROVENANCE') THEN RAISE(ABORT,'NRA-PROVENANCE') END; SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.version_id AND code='TIME') THEN RAISE(ABORT,'NRA-TIME') END; SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.version_id AND code='OWNER') THEN RAISE(ABORT,'NRA-OWNER') END; SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.version_id AND code='IDENTITY') THEN RAISE(ABORT,'NRA-IDENTITY') END; SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.version_id AND code='TERM_VERSION') THEN RAISE(ABORT,'NRA-TERM_VERSION') END; SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.version_id AND code='CONTEXT_VERSION') THEN RAISE(ABORT,'NRA-CONTEXT_VERSION') END; END;

CREATE TRIGGER nature_objective_validate AFTER INSERT ON nature_objective BEGIN
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.context_version_id AND code IN ('OBJECTIVE_VERSION','TIME')) THEN RAISE(ABORT,'NRA-OBJECTIVE_VERSION') END; END;
 CREATE TRIGGER nature_entry_link_validate AFTER INSERT ON nature_entry_link BEGIN
 SELECT CASE WHEN EXISTS(SELECT 1 FROM nature_entry e JOIN register_entry r ON r.entry_id=e.entry_id JOIN nature_snapshot n ON n.version_id=NEW.nature_version_id WHERE e.version_id=NEW.entry_version_id AND r.case_id<>n.case_id) THEN RAISE(ABORT,'NRA-RECORDING') END; END;
 CREATE TRIGGER nature_correction_validate AFTER INSERT ON nature_correction BEGIN
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.corrected_version_id AND code IN ('CORRECTION','PROVENANCE','TIME')) THEN RAISE(ABORT,'NRA-CORRECTION') END;
 SELECT CASE WHEN EXISTS(WITH RECURSIVE w(id) AS (SELECT NEW.prior_version_id UNION SELECT c.prior_version_id FROM nature_correction c JOIN w ON c.corrected_version_id=w.id) SELECT 1 FROM w WHERE id=NEW.corrected_version_id) THEN RAISE(ABORT,'NRA-CORRECTION') END; END;
 CREATE TRIGGER nature_validate_seal BEFORE UPDATE ON version_snapshot WHEN OLD.is_issued=0 AND NEW.is_issued=1 BEGIN
 SELECT CASE WHEN EXISTS(SELECT 1 FROM nature_membership m WHERE m.artifact_id=NEW.artifact_id) AND NOT EXISTS(SELECT 1 FROM v_nature_expected_payload p WHERE p.version_id=NEW.version_id) THEN RAISE(ABORT,'NRA-METADATA') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_expected_payload p WHERE p.version_id=NEW.version_id) AND (NEW.payload_json IS NOT OLD.payload_json OR NEW.issued_at IS NOT json_extract(NEW.payload_json,'$.recorded_at') OR EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.version_id AND code<>'RECORDING')) THEN RAISE(ABORT,'NRA-SEAL') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM nature_snapshot WHERE version_id=NEW.version_id) AND (NOT EXISTS(SELECT 1 FROM nature_entry_link WHERE nature_version_id=NEW.version_id) OR EXISTS(SELECT 1 FROM nature_entry_link l JOIN version_snapshot v ON v.version_id=l.entry_version_id WHERE l.nature_version_id=NEW.version_id AND v.is_issued<>1)) THEN RAISE(ABORT,'NRA-RECORDING') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM nature_entry e WHERE e.version_id=NEW.version_id) AND (NOT EXISTS(SELECT 1 FROM nature_entry_link WHERE entry_version_id=NEW.version_id) OR EXISTS(SELECT 1 FROM nature_entry_link l JOIN nature_snapshot n ON n.version_id=l.nature_version_id JOIN nature_entry e ON e.version_id=l.entry_version_id JOIN register_entry r ON r.entry_id=e.entry_id WHERE l.entry_version_id=NEW.version_id AND r.case_id<>n.case_id)) THEN RAISE(ABORT,'NRA-RECORDING') END;
 END;

CREATE INDEX nature_by_case ON nature_snapshot(case_id,version_id);

CREATE INDEX nature_by_artifact ON nature_snapshot(artifact_id,version_id);

CREATE INDEX nature_children ON nature_correction(prior_version_id,corrected_version_id);

CREATE INDEX nature_recorders ON nature_entry_link(nature_version_id,entry_version_id);
