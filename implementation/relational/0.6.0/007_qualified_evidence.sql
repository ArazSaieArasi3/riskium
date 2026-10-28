-- Additive application profile; EvidenceItem role is NOT a global artifact type.
CREATE TABLE evidence_reference_type (
 artifact_id TEXT PRIMARY KEY NOT NULL REFERENCES information_artifact(artifact_id)
) STRICT;
CREATE TABLE evidence_snapshot (
 version_id TEXT PRIMARY KEY NOT NULL REFERENCES version_snapshot(version_id),
 artifact_id TEXT NOT NULL REFERENCES evidence_reference_type(artifact_id),
 item_id TEXT NOT NULL REFERENCES information_artifact(artifact_id),
 item_version_id TEXT NOT NULL REFERENCES version_snapshot(version_id),
 statement TEXT NOT NULL CHECK(length(trim(statement))>0),
 evidential_role TEXT NOT NULL CHECK(evidential_role IN ('support','challenge','context')),
 source_record_id TEXT NOT NULL REFERENCES source_record(record_id),
 source_locator TEXT NOT NULL CHECK(length(trim(source_locator))>0),
 interpretation_origin TEXT NOT NULL CHECK(length(trim(interpretation_origin))>0),
 recorded_at TEXT NOT NULL
) STRICT;
CREATE TABLE evidence_target (
 version_id TEXT NOT NULL REFERENCES evidence_snapshot(version_id),
 artifact_id TEXT NOT NULL REFERENCES information_artifact(artifact_id),
 target_version_id TEXT NOT NULL REFERENCES version_snapshot(version_id),
 PRIMARY KEY(version_id,artifact_id), UNIQUE(version_id,target_version_id)
) STRICT;
CREATE INDEX evidence_by_artifact ON evidence_snapshot(artifact_id,version_id);
CREATE INDEX evidence_by_source ON evidence_snapshot(source_record_id,version_id);
CREATE INDEX evidence_by_item ON evidence_snapshot(item_version_id,version_id);
CREATE INDEX evidence_by_target ON evidence_target(target_version_id,version_id);
CREATE TRIGGER evidence_type_insert BEFORE INSERT ON evidence_reference_type BEGIN
 SELECT CASE WHEN EXISTS(SELECT 1 FROM evidence_reference_type WHERE artifact_id=NEW.artifact_id) THEN RAISE(ABORT,'R-EVIDENCE-DUPLICATE') END;
 SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM information_artifact WHERE artifact_id=NEW.artifact_id AND kind='RKM-C014')
 OR EXISTS(SELECT 1 FROM artifact_typing WHERE artifact_id=NEW.artifact_id)
 OR EXISTS(SELECT 1 FROM knowledge_type WHERE artifact_id=NEW.artifact_id) THEN RAISE(ABORT,'R-EVIDENCE-TYPE') END;
END;
CREATE TRIGGER evidence_no_assessment_typing BEFORE INSERT ON artifact_typing
 WHEN EXISTS(SELECT 1 FROM evidence_reference_type WHERE artifact_id=NEW.artifact_id) BEGIN
 SELECT RAISE(ABORT,'R-EVIDENCE-TYPE');
END;
CREATE TRIGGER evidence_no_knowledge_typing BEFORE INSERT ON knowledge_type
 WHEN EXISTS(SELECT 1 FROM evidence_reference_type WHERE artifact_id=NEW.artifact_id) BEGIN
 SELECT RAISE(ABORT,'R-EVIDENCE-TYPE');
END;
CREATE TRIGGER evidence_snapshot_insert BEFORE INSERT ON evidence_snapshot BEGIN
 SELECT CASE WHEN EXISTS(SELECT 1 FROM evidence_snapshot WHERE version_id=NEW.version_id) THEN RAISE(ABORT,'R-EVIDENCE-DUPLICATE') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.version_id AND is_issued=1) THEN RAISE(ABORT,'R-EVIDENCE-FROZEN') END;
 SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.version_id AND artifact_id=NEW.artifact_id AND source_record_id=NEW.source_record_id)
 THEN RAISE(ABORT,'R-EVIDENCE-OWNER-SOURCE') END;
 SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.item_version_id AND artifact_id=NEW.item_id AND is_issued=1)
 THEN RAISE(ABORT,'R-EVIDENCE-ITEM') END;
 SELECT CASE WHEN length(trim(NEW.statement))=0 OR length(trim(NEW.source_locator))=0 OR length(trim(NEW.interpretation_origin))=0
 THEN RAISE(ABORT,'R-EVIDENCE-PROVENANCE') END;
 SELECT CASE WHEN NEW.evidential_role NOT IN ('support','challenge','context') THEN RAISE(ABORT,'R-EVIDENCE-ROLE') END;
 SELECT CASE WHEN length(NEW.recorded_at)<>20 OR NEW.recorded_at NOT GLOB '????-??-??T??:??:??Z' OR substr(NEW.recorded_at,1,4)<'0001'
 OR strftime('%Y-%m-%dT%H:%M:%SZ',NEW.recorded_at) IS NOT NEW.recorded_at
 OR date(NEW.recorded_at,'+0 days') IS NOT substr(NEW.recorded_at,1,10) THEN RAISE(ABORT,'R-EVIDENCE-TIME') END;
END;
CREATE TRIGGER evidence_target_insert BEFORE INSERT ON evidence_target BEGIN
 SELECT CASE WHEN EXISTS(SELECT 1 FROM evidence_target WHERE version_id=NEW.version_id AND (artifact_id=NEW.artifact_id OR target_version_id=NEW.target_version_id))
 THEN RAISE(ABORT,'R-EVIDENCE-DUPLICATE') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.version_id AND is_issued=1) THEN RAISE(ABORT,'R-EVIDENCE-FROZEN') END;
 SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.target_version_id AND artifact_id=NEW.artifact_id AND is_issued=1)
 THEN RAISE(ABORT,'R-EVIDENCE-TARGET') END;
END;
CREATE VIEW v_evidence_invalid AS
 SELECT t.artifact_id AS version_id,'TYPE' AS code FROM evidence_reference_type t JOIN information_artifact a USING(artifact_id)
 WHERE a.kind<>'RKM-C014' OR EXISTS(SELECT 1 FROM artifact_typing z WHERE z.artifact_id=t.artifact_id)
 OR EXISTS(SELECT 1 FROM knowledge_type z WHERE z.artifact_id=t.artifact_id)
 UNION ALL SELECT e.version_id,'OWNER-SOURCE' FROM evidence_snapshot e JOIN version_snapshot v USING(version_id)
 WHERE e.artifact_id<>v.artifact_id OR e.source_record_id<>v.source_record_id OR (v.is_issued=1 AND v.issued_at IS NOT e.recorded_at)
 UNION ALL SELECT e.version_id,'ITEM' FROM evidence_snapshot e JOIN version_snapshot v ON v.version_id=e.item_version_id
 WHERE e.item_id<>v.artifact_id OR v.is_issued<>1
 UNION ALL SELECT e.version_id,'PROVENANCE' FROM evidence_snapshot e
 WHERE length(trim(e.statement))=0 OR length(trim(e.source_locator))=0 OR length(trim(e.interpretation_origin))=0
 UNION ALL SELECT e.version_id,'ROLE' FROM evidence_snapshot e WHERE e.evidential_role NOT IN ('support','challenge','context')
 UNION ALL SELECT e.version_id,'CARDINALITY' FROM evidence_snapshot e WHERE NOT EXISTS(SELECT 1 FROM evidence_target t WHERE t.version_id=e.version_id)
 UNION ALL SELECT t.version_id,'TARGET' FROM evidence_target t JOIN version_snapshot v ON v.version_id=t.target_version_id
 WHERE t.artifact_id<>v.artifact_id OR v.is_issued<>1
 UNION ALL SELECT e.version_id,'TIME' FROM evidence_snapshot e
 WHERE length(e.recorded_at)<>20 OR e.recorded_at NOT GLOB '????-??-??T??:??:??Z' OR substr(e.recorded_at,1,4)<'0001'
 OR strftime('%Y-%m-%dT%H:%M:%SZ',e.recorded_at) IS NOT e.recorded_at
 OR date(e.recorded_at,'+0 days') IS NOT substr(e.recorded_at,1,10)
 UNION ALL SELECT e.version_id,'PAYLOAD' FROM evidence_snapshot e JOIN version_snapshot v USING(version_id)
 WHERE (SELECT count(*) FROM json_each(v.payload_json))<>10
 OR json_extract(v.payload_json,'$.version_id') IS NOT e.version_id
 OR json_extract(v.payload_json,'$.artifact_id') IS NOT e.artifact_id
 OR json_extract(v.payload_json,'$.statement') IS NOT e.statement
 OR json_extract(v.payload_json,'$.item_version_id') IS NOT e.item_version_id
 OR json_extract(v.payload_json,'$.evidential_role') IS NOT e.evidential_role
 OR json_extract(v.payload_json,'$.source_record_id') IS NOT e.source_record_id
 OR json_extract(v.payload_json,'$.source_locator') IS NOT e.source_locator
 OR json_extract(v.payload_json,'$.interpretation_origin') IS NOT e.interpretation_origin
 OR json_extract(v.payload_json,'$.recorded_at') IS NOT e.recorded_at
 OR json_type(v.payload_json,'$.target_version_ids') IS NOT 'array'
 OR json(json_extract(v.payload_json,'$.target_version_ids')) IS NOT (SELECT json_group_array(target_version_id) FROM (SELECT target_version_id FROM evidence_target t WHERE t.version_id=e.version_id ORDER BY target_version_id));
CREATE TRIGGER evidence_seal BEFORE UPDATE ON version_snapshot
 WHEN OLD.is_issued=0 AND NEW.is_issued=1 AND EXISTS(SELECT 1 FROM evidence_reference_type WHERE artifact_id=NEW.artifact_id) BEGIN
 SELECT CASE WHEN NEW.payload_json IS NOT OLD.payload_json THEN RAISE(ABORT,'R-EVIDENCE-PAYLOAD') END;
 SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM evidence_snapshot WHERE version_id=NEW.version_id AND artifact_id=NEW.artifact_id AND source_record_id=NEW.source_record_id)
 OR NEW.issued_at IS NOT (SELECT recorded_at FROM evidence_snapshot WHERE version_id=NEW.version_id)
 THEN RAISE(ABORT,'R-EVIDENCE-OWNER-SOURCE') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_evidence_invalid WHERE version_id=NEW.version_id AND code='CARDINALITY') THEN RAISE(ABORT,'R-EVIDENCE-CARDINALITY') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_evidence_invalid WHERE version_id=NEW.version_id AND code='PAYLOAD') THEN RAISE(ABORT,'R-EVIDENCE-PAYLOAD') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_evidence_invalid WHERE version_id=NEW.version_id) THEN RAISE(ABORT,'R-EVIDENCE-DATA') END;
END;
CREATE TRIGGER evidence_type_update BEFORE UPDATE ON evidence_reference_type BEGIN SELECT RAISE(ABORT,'R-EVIDENCE-IMMUTABLE'); END;
CREATE TRIGGER evidence_type_delete BEFORE DELETE ON evidence_reference_type BEGIN SELECT RAISE(ABORT,'R-EVIDENCE-IMMUTABLE'); END;
CREATE TRIGGER evidence_snapshot_update BEFORE UPDATE ON evidence_snapshot BEGIN SELECT RAISE(ABORT,'R-EVIDENCE-IMMUTABLE'); END;
CREATE TRIGGER evidence_snapshot_delete BEFORE DELETE ON evidence_snapshot BEGIN SELECT RAISE(ABORT,'R-EVIDENCE-IMMUTABLE'); END;
CREATE TRIGGER evidence_target_update BEFORE UPDATE ON evidence_target BEGIN SELECT RAISE(ABORT,'R-EVIDENCE-IMMUTABLE'); END;
CREATE TRIGGER evidence_target_delete BEFORE DELETE ON evidence_target BEGIN SELECT RAISE(ABORT,'R-EVIDENCE-IMMUTABLE'); END;
CREATE VIEW v_evidence_quads AS
 SELECT e.version_id AS graph_id,e.artifact_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,
 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C065' AS object FROM evidence_snapshot e JOIN version_snapshot v USING(version_id) WHERE v.is_issued=1
 UNION SELECT e.version_id,e.artifact_id,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' FROM evidence_snapshot e JOIN version_snapshot v USING(version_id) WHERE v.is_issued=1
 UNION SELECT e.version_id,e.version_id,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C015' FROM evidence_snapshot e JOIN version_snapshot v USING(version_id) WHERE v.is_issued=1
 UNION SELECT e.version_id,e.version_id,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RX-006',e.artifact_id FROM evidence_snapshot e JOIN version_snapshot v USING(version_id) WHERE v.is_issued=1
 UNION SELECT e.version_id,e.item_id,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C066' FROM evidence_snapshot e JOIN version_snapshot v USING(version_id) WHERE v.is_issued=1
 UNION SELECT e.version_id,e.item_id,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' FROM evidence_snapshot e JOIN version_snapshot v USING(version_id) WHERE v.is_issued=1
 UNION SELECT e.version_id,e.item_version_id,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C015' FROM evidence_snapshot e JOIN version_snapshot v USING(version_id) WHERE v.is_issued=1
 UNION SELECT e.version_id,e.item_version_id,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RX-006',e.item_id FROM evidence_snapshot e JOIN version_snapshot v USING(version_id) WHERE v.is_issued=1
 UNION SELECT e.version_id,e.artifact_id,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RX-021',e.item_id FROM evidence_snapshot e JOIN version_snapshot v USING(version_id) WHERE v.is_issued=1
 UNION SELECT t.version_id,t.artifact_id,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' FROM evidence_target t JOIN version_snapshot v ON v.version_id=t.version_id WHERE v.is_issued=1
 UNION SELECT t.version_id,t.target_version_id,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C015' FROM evidence_target t JOIN version_snapshot v ON v.version_id=t.version_id WHERE v.is_issued=1
 UNION SELECT t.version_id,t.target_version_id,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RX-006',t.artifact_id FROM evidence_target t JOIN version_snapshot v ON v.version_id=t.version_id WHERE v.is_issued=1
 UNION SELECT t.version_id,e.artifact_id,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#R-68',t.artifact_id FROM evidence_target t JOIN evidence_snapshot e USING(version_id) JOIN version_snapshot v ON v.version_id=t.version_id WHERE v.is_issued=1;
