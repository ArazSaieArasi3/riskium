-- Additive SQLite migration 5. Existing schema, native views and receipts unchanged.
CREATE TABLE knowledge_type (
 artifact_id TEXT PRIMARY KEY NOT NULL REFERENCES information_artifact(artifact_id),
 native_class TEXT NOT NULL CHECK(native_class IN ('RKM-C003','RKM-X06'))
) STRICT;
CREATE TABLE knowledge_snapshot (
 version_id TEXT PRIMARY KEY NOT NULL REFERENCES version_snapshot(version_id),
 artifact_id TEXT NOT NULL REFERENCES knowledge_type(artifact_id),
 narrative TEXT NOT NULL CHECK(length(trim(narrative))>0),
 source_record_id TEXT NOT NULL REFERENCES source_record(record_id),
 source_locator TEXT NOT NULL CHECK(length(trim(source_locator))>0),
 interpretation_origin TEXT NOT NULL CHECK(length(trim(interpretation_origin))>0),
 recorded_at TEXT NOT NULL
) STRICT;
CREATE TABLE knowledge_case (
 version_id TEXT NOT NULL REFERENCES knowledge_snapshot(version_id),
 case_id TEXT NOT NULL REFERENCES risk_case(case_id),
 PRIMARY KEY(version_id,case_id)
) STRICT;
CREATE TABLE knowledge_context (
 version_id TEXT NOT NULL REFERENCES knowledge_snapshot(version_id),
 context_id TEXT NOT NULL REFERENCES information_artifact(artifact_id),
 context_version_id TEXT NOT NULL REFERENCES version_snapshot(version_id),
 PRIMARY KEY(version_id,context_id),
 UNIQUE(version_id,context_version_id)
) STRICT;
CREATE INDEX knowledge_case_lookup ON knowledge_case(case_id,version_id);
CREATE INDEX knowledge_history ON knowledge_snapshot(artifact_id,version_id);
CREATE INDEX knowledge_provenance ON knowledge_snapshot(source_record_id,version_id);
CREATE INDEX knowledge_context_version ON knowledge_context(context_version_id);
CREATE TRIGGER knowledge_type_insert BEFORE INSERT ON knowledge_type BEGIN
 SELECT CASE WHEN EXISTS(SELECT 1 FROM knowledge_type WHERE artifact_id=NEW.artifact_id)
 THEN RAISE(ABORT,'R-KNOWLEDGE-DUPLICATE') END;
 SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM information_artifact a WHERE a.artifact_id=NEW.artifact_id AND a.kind='RKM-C014')
 OR EXISTS(SELECT 1 FROM artifact_typing WHERE artifact_id=NEW.artifact_id)
 THEN RAISE(ABORT,'R-KNOWLEDGE-TYPE') END;
END;
CREATE TRIGGER knowledge_no_conflicting_type BEFORE INSERT ON artifact_typing
 WHEN EXISTS(SELECT 1 FROM knowledge_type WHERE artifact_id=NEW.artifact_id) BEGIN
 SELECT RAISE(ABORT,'R-KNOWLEDGE-TYPE');
END;
CREATE TRIGGER knowledge_snapshot_insert BEFORE INSERT ON knowledge_snapshot BEGIN
 SELECT CASE WHEN EXISTS(SELECT 1 FROM knowledge_snapshot WHERE version_id=NEW.version_id)
 THEN RAISE(ABORT,'R-KNOWLEDGE-DUPLICATE') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.version_id AND is_issued=1)
 THEN RAISE(ABORT,'R-KNOWLEDGE-FROZEN') END;
 SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM version_snapshot v WHERE v.version_id=NEW.version_id AND v.artifact_id=NEW.artifact_id AND v.source_record_id=NEW.source_record_id)
 THEN RAISE(ABORT,'R-KNOWLEDGE-OWNER-SOURCE') END;
 SELECT CASE WHEN length(trim(NEW.narrative))=0 OR length(trim(NEW.source_locator))=0 OR length(trim(NEW.interpretation_origin))=0
 THEN RAISE(ABORT,'R-KNOWLEDGE-PROVENANCE') END;
 SELECT CASE WHEN length(NEW.recorded_at)<>20 OR NEW.recorded_at NOT GLOB '????-??-??T??:??:??Z'
 OR substr(NEW.recorded_at,1,4)<'0001' OR strftime('%Y-%m-%dT%H:%M:%SZ',NEW.recorded_at) IS NOT NEW.recorded_at
 OR date(NEW.recorded_at,'+0 days') IS NOT substr(NEW.recorded_at,1,10)
 THEN RAISE(ABORT,'R-KNOWLEDGE-TIME') END;
END;
CREATE TRIGGER knowledge_case_insert BEFORE INSERT ON knowledge_case BEGIN
 SELECT CASE WHEN EXISTS(SELECT 1 FROM knowledge_case WHERE version_id=NEW.version_id AND case_id=NEW.case_id)
 THEN RAISE(ABORT,'R-KNOWLEDGE-DUPLICATE') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.version_id AND is_issued=1)
 THEN RAISE(ABORT,'R-KNOWLEDGE-FROZEN') END;
 SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM risk_case WHERE case_id=NEW.case_id)
 THEN RAISE(ABORT,'R-KNOWLEDGE-CASE') END;
END;
CREATE TRIGGER knowledge_context_insert BEFORE INSERT ON knowledge_context BEGIN
 SELECT CASE WHEN EXISTS(SELECT 1 FROM knowledge_context WHERE version_id=NEW.version_id AND (context_id=NEW.context_id OR context_version_id=NEW.context_version_id))
 THEN RAISE(ABORT,'R-KNOWLEDGE-DUPLICATE') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.version_id AND is_issued=1)
 THEN RAISE(ABORT,'R-KNOWLEDGE-FROZEN') END;
 SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM version_snapshot v JOIN information_artifact a ON a.artifact_id=v.artifact_id
 WHERE v.version_id=NEW.context_version_id AND v.artifact_id=NEW.context_id AND v.is_issued=1 AND a.kind='RKM-C002')
 THEN RAISE(ABORT,'R-KNOWLEDGE-CONTEXT') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM knowledge_context WHERE version_id=NEW.version_id)
 AND EXISTS(SELECT 1 FROM knowledge_snapshot k JOIN knowledge_type t USING(artifact_id) WHERE k.version_id=NEW.version_id AND t.native_class='RKM-X06')
 THEN RAISE(ABORT,'R-KNOWLEDGE-CONTEXT-CARDINALITY') END;
END;
CREATE VIEW v_knowledge_invalid AS
 SELECT t.artifact_id AS version_id,'TYPE' AS code FROM knowledge_type t JOIN information_artifact a USING(artifact_id)
 WHERE a.kind<>'RKM-C014' OR t.native_class NOT IN ('RKM-C003','RKM-X06') OR EXISTS(SELECT 1 FROM artifact_typing z WHERE z.artifact_id=t.artifact_id)
 UNION ALL
 SELECT k.version_id,'PROVENANCE' FROM knowledge_snapshot k
 WHERE length(trim(k.narrative))=0 OR length(trim(k.source_locator))=0 OR length(trim(k.interpretation_origin))=0
 UNION ALL
 SELECT k.version_id,'OWNER-SOURCE' FROM knowledge_snapshot k JOIN version_snapshot v USING(version_id)
 WHERE k.artifact_id<>v.artifact_id OR k.source_record_id<>v.source_record_id OR (v.is_issued=1 AND v.issued_at<>k.recorded_at)
 UNION ALL
 SELECT k.version_id,'CARDINALITY' FROM knowledge_snapshot k JOIN knowledge_type t USING(artifact_id)
 WHERE (t.native_class='RKM-C003' AND NOT EXISTS(SELECT 1 FROM knowledge_case c WHERE c.version_id=k.version_id))
 OR (t.native_class='RKM-X06' AND (SELECT count(*) FROM knowledge_context c WHERE c.version_id=k.version_id)>1)
 UNION ALL
 SELECT c.version_id,'CONTEXT' FROM knowledge_context c JOIN version_snapshot v ON v.version_id=c.context_version_id
 JOIN information_artifact a ON a.artifact_id=v.artifact_id
 WHERE c.context_id<>v.artifact_id OR a.kind<>'RKM-C002' OR v.is_issued<>1
 UNION ALL
 SELECT k.version_id,'TIME' FROM knowledge_snapshot k
 WHERE length(k.recorded_at)<>20 OR k.recorded_at NOT GLOB '????-??-??T??:??:??Z'
 OR substr(k.recorded_at,1,4)<'0001' OR strftime('%Y-%m-%dT%H:%M:%SZ',k.recorded_at) IS NOT k.recorded_at
 OR date(k.recorded_at,'+0 days') IS NOT substr(k.recorded_at,1,10)
 UNION ALL
 SELECT k.version_id,'PAYLOAD' FROM knowledge_snapshot k JOIN version_snapshot v USING(version_id) JOIN knowledge_type t ON t.artifact_id=k.artifact_id
 WHERE (SELECT count(*) FROM json_each(v.payload_json))<>10
 OR json_extract(v.payload_json,'$.version_id') IS NOT k.version_id
 OR json_extract(v.payload_json,'$.artifact_id') IS NOT k.artifact_id
 OR json_extract(v.payload_json,'$.native_class') IS NOT t.native_class
 OR json_extract(v.payload_json,'$.narrative') IS NOT k.narrative
 OR json_extract(v.payload_json,'$.source_record_id') IS NOT k.source_record_id
 OR json_extract(v.payload_json,'$.source_locator') IS NOT k.source_locator
 OR json_extract(v.payload_json,'$.interpretation_origin') IS NOT k.interpretation_origin
 OR json_extract(v.payload_json,'$.recorded_at') IS NOT k.recorded_at
 OR json_type(v.payload_json,'$.case_ids') IS NOT 'array'
 OR json_type(v.payload_json,'$.context_version_ids') IS NOT 'array'
 OR json(json_extract(v.payload_json,'$.case_ids')) IS NOT (SELECT json_group_array(case_id) FROM (SELECT case_id FROM knowledge_case c WHERE c.version_id=k.version_id ORDER BY case_id))
 OR json(json_extract(v.payload_json,'$.context_version_ids')) IS NOT (SELECT json_group_array(context_version_id) FROM (SELECT context_version_id FROM knowledge_context c WHERE c.version_id=k.version_id ORDER BY context_version_id));
CREATE TRIGGER knowledge_seal BEFORE UPDATE ON version_snapshot
 WHEN OLD.is_issued=0 AND NEW.is_issued=1 AND EXISTS(SELECT 1 FROM knowledge_type t WHERE t.artifact_id=NEW.artifact_id) BEGIN
 SELECT CASE WHEN NEW.payload_json IS NOT OLD.payload_json
 THEN RAISE(ABORT,'R-KNOWLEDGE-PAYLOAD') END;
 SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM knowledge_snapshot k WHERE k.version_id=NEW.version_id AND k.artifact_id=NEW.artifact_id AND k.source_record_id=NEW.source_record_id)
 THEN RAISE(ABORT,'R-KNOWLEDGE-OWNER-SOURCE') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_knowledge_invalid WHERE version_id=NEW.version_id AND code='CARDINALITY')
 THEN RAISE(ABORT,'R-KNOWLEDGE-CARDINALITY') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_knowledge_invalid WHERE version_id=NEW.version_id AND code='PAYLOAD')
 THEN RAISE(ABORT,'R-KNOWLEDGE-PAYLOAD') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_knowledge_invalid WHERE version_id=NEW.version_id AND code='OWNER-SOURCE') OR NEW.issued_at IS NOT (SELECT recorded_at FROM knowledge_snapshot WHERE version_id=NEW.version_id)
 THEN RAISE(ABORT,'R-KNOWLEDGE-OWNER-SOURCE') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_knowledge_invalid WHERE version_id=NEW.version_id)
 THEN RAISE(ABORT,'R-KNOWLEDGE-DATA') END;
END;
CREATE TRIGGER knowledge_type_update BEFORE UPDATE ON knowledge_type BEGIN
 SELECT RAISE(ABORT,'R-KNOWLEDGE-IMMUTABLE');
END;
CREATE TRIGGER knowledge_type_delete BEFORE DELETE ON knowledge_type BEGIN
 SELECT RAISE(ABORT,'R-KNOWLEDGE-IMMUTABLE');
END;
CREATE TRIGGER knowledge_snapshot_update BEFORE UPDATE ON knowledge_snapshot BEGIN
 SELECT RAISE(ABORT,'R-KNOWLEDGE-IMMUTABLE');
END;
CREATE TRIGGER knowledge_snapshot_delete BEFORE DELETE ON knowledge_snapshot BEGIN
 SELECT RAISE(ABORT,'R-KNOWLEDGE-IMMUTABLE');
END;
CREATE TRIGGER knowledge_case_update BEFORE UPDATE ON knowledge_case BEGIN
 SELECT RAISE(ABORT,'R-KNOWLEDGE-IMMUTABLE');
END;
CREATE TRIGGER knowledge_case_delete BEFORE DELETE ON knowledge_case BEGIN
 SELECT RAISE(ABORT,'R-KNOWLEDGE-IMMUTABLE');
END;
CREATE TRIGGER knowledge_context_update BEFORE UPDATE ON knowledge_context BEGIN
 SELECT RAISE(ABORT,'R-KNOWLEDGE-IMMUTABLE');
END;
CREATE TRIGGER knowledge_context_delete BEFORE DELETE ON knowledge_context BEGIN
 SELECT RAISE(ABORT,'R-KNOWLEDGE-IMMUTABLE');
END;
CREATE VIEW v_knowledge_quads AS
 SELECT k.version_id AS graph_id,k.artifact_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,
 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'||t.native_class AS object
 FROM knowledge_snapshot k JOIN knowledge_type t USING(artifact_id) JOIN version_snapshot v USING(version_id) WHERE v.is_issued=1
 UNION SELECT k.version_id,k.artifact_id,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014'
 FROM knowledge_snapshot k JOIN version_snapshot v USING(version_id) WHERE v.is_issued=1
 UNION SELECT k.version_id,k.version_id,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C015'
 FROM knowledge_snapshot k JOIN version_snapshot v USING(version_id) WHERE v.is_issued=1
 UNION SELECT k.version_id,k.version_id,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RX-006',k.artifact_id
 FROM knowledge_snapshot k JOIN version_snapshot v USING(version_id) WHERE v.is_issued=1
 UNION SELECT c.version_id,c.case_id,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-X01'
 FROM knowledge_case c JOIN version_snapshot v USING(version_id) WHERE v.is_issued=1
 UNION SELECT c.version_id,CASE t.native_class WHEN 'RKM-C003' THEN k.artifact_id ELSE c.case_id END,
 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'||CASE t.native_class WHEN 'RKM-C003' THEN 'R-36' ELSE 'RK3-001' END,
 CASE t.native_class WHEN 'RKM-C003' THEN c.case_id ELSE k.artifact_id END
 FROM knowledge_case c JOIN knowledge_snapshot k USING(version_id) JOIN knowledge_type t USING(artifact_id) JOIN version_snapshot v USING(version_id) WHERE v.is_issued=1
 UNION SELECT c.version_id,k.artifact_id,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'||CASE t.native_class WHEN 'RKM-C003' THEN 'RK2-010' ELSE 'RK3-003' END,c.context_id
 FROM knowledge_context c JOIN knowledge_snapshot k USING(version_id) JOIN knowledge_type t USING(artifact_id) JOIN version_snapshot v USING(version_id) WHERE v.is_issued=1
 UNION SELECT c.version_id,c.context_id,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C002'
 FROM knowledge_context c JOIN version_snapshot v USING(version_id) WHERE v.is_issued=1
 UNION SELECT c.version_id,c.context_id,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014'
 FROM knowledge_context c JOIN version_snapshot v USING(version_id) WHERE v.is_issued=1
 UNION SELECT c.version_id,c.context_version_id,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C015'
 FROM knowledge_context c JOIN version_snapshot v USING(version_id) WHERE v.is_issued=1
 UNION SELECT c.version_id,c.context_version_id,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RX-006',c.context_id
 FROM knowledge_context c JOIN version_snapshot v USING(version_id) WHERE v.is_issued=1;
