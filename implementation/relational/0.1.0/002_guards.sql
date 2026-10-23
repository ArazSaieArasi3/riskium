-- Generated history guards; apply with the transactional migration runner.

CREATE TRIGGER source_record_no_replace BEFORE INSERT ON source_record WHEN EXISTS(SELECT 1 FROM source_record WHERE record_id=NEW.record_id)
BEGIN
SELECT RAISE(ABORT, 'R-CATALOG-DUPLICATE');
END;

CREATE TRIGGER source_record_no_update BEFORE UPDATE ON source_record
BEGIN
SELECT RAISE(ABORT, 'R-CATALOG-IMMUTABLE');
END;

CREATE TRIGGER source_record_no_delete BEFORE DELETE ON source_record
BEGIN
SELECT RAISE(ABORT, 'R-CATALOG-IMMUTABLE');
END;

CREATE TRIGGER identity_registry_no_replace BEFORE INSERT ON identity_registry WHEN EXISTS(SELECT 1 FROM identity_registry WHERE resource_id=NEW.resource_id)
BEGIN
SELECT RAISE(ABORT, 'R-CATALOG-DUPLICATE');
END;

CREATE TRIGGER identity_registry_no_update BEFORE UPDATE ON identity_registry
BEGIN
SELECT RAISE(ABORT, 'R-CATALOG-IMMUTABLE');
END;

CREATE TRIGGER identity_registry_no_delete BEFORE DELETE ON identity_registry
BEGIN
SELECT RAISE(ABORT, 'R-CATALOG-IMMUTABLE');
END;

CREATE TRIGGER risk_case_no_replace BEFORE INSERT ON risk_case WHEN EXISTS(SELECT 1 FROM risk_case WHERE case_id=NEW.case_id)
BEGIN
SELECT RAISE(ABORT, 'R-CATALOG-DUPLICATE');
END;

CREATE TRIGGER risk_case_no_update BEFORE UPDATE ON risk_case
BEGIN
SELECT RAISE(ABORT, 'R-CATALOG-IMMUTABLE');
END;

CREATE TRIGGER risk_case_no_delete BEFORE DELETE ON risk_case
BEGIN
SELECT RAISE(ABORT, 'R-CATALOG-IMMUTABLE');
END;

CREATE TRIGGER information_artifact_no_replace BEFORE INSERT ON information_artifact WHEN EXISTS(SELECT 1 FROM information_artifact WHERE artifact_id=NEW.artifact_id)
BEGIN
SELECT RAISE(ABORT, 'R-CATALOG-DUPLICATE');
END;

CREATE TRIGGER information_artifact_no_update BEFORE UPDATE ON information_artifact
BEGIN
SELECT RAISE(ABORT, 'R-CATALOG-IMMUTABLE');
END;

CREATE TRIGGER information_artifact_no_delete BEFORE DELETE ON information_artifact
BEGIN
SELECT RAISE(ABORT, 'R-CATALOG-IMMUTABLE');
END;

CREATE TRIGGER register_entry_no_replace BEFORE INSERT ON register_entry WHEN EXISTS(SELECT 1 FROM register_entry WHERE entry_id=NEW.entry_id)
BEGIN
SELECT RAISE(ABORT, 'R-CATALOG-DUPLICATE');
END;

CREATE TRIGGER register_entry_no_update BEFORE UPDATE ON register_entry
BEGIN
SELECT RAISE(ABORT, 'R-CATALOG-IMMUTABLE');
END;

CREATE TRIGGER register_entry_no_delete BEFORE DELETE ON register_entry
BEGIN
SELECT RAISE(ABORT, 'R-CATALOG-IMMUTABLE');
END;

CREATE TRIGGER snapshot_no_replace BEFORE INSERT ON version_snapshot WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.version_id)
BEGIN
SELECT RAISE(ABORT, 'R-VERSION-DUPLICATE');
END;

CREATE TRIGGER snapshot_insert_unissued BEFORE INSERT ON version_snapshot WHEN NEW.is_issued<>0
BEGIN
SELECT RAISE(ABORT, 'R-ISSUE-VIA-SEAL');
END;

CREATE TRIGGER snapshot_immutable_update BEFORE UPDATE ON version_snapshot WHEN OLD.is_issued=1
BEGIN
SELECT RAISE(ABORT, 'R-ISSUED-IMMUTABLE');
END;

CREATE TRIGGER snapshot_immutable_delete BEFORE DELETE ON version_snapshot WHEN OLD.is_issued=1
BEGIN
SELECT RAISE(ABORT, 'R-ISSUED-IMMUTABLE');
END;

CREATE TRIGGER snapshot_lineage_insert BEFORE INSERT ON version_snapshot
BEGIN
SELECT CASE WHEN NEW.previous_version_id IS NOT NULL AND NOT EXISTS(
      SELECT 1 FROM version_snapshot p WHERE p.version_id=NEW.previous_version_id
      AND p.entry_id=NEW.entry_id AND p.is_issued=1) THEN RAISE(ABORT,'R-PREDECESSOR-SAME-ISSUED-ENTRY') END;
END;

CREATE TRIGGER snapshot_cycle_insert BEFORE INSERT ON version_snapshot
BEGIN
SELECT CASE WHEN NEW.previous_version_id IS NOT NULL AND EXISTS(
      WITH RECURSIVE prior(id) AS (SELECT NEW.previous_version_id UNION
        SELECT v.previous_version_id FROM version_snapshot v JOIN prior p ON v.version_id=p.id
        WHERE v.previous_version_id IS NOT NULL) SELECT 1 FROM prior WHERE id=NEW.version_id)
      THEN RAISE(ABORT,'R-PREDECESSOR-CYCLE') END;
END;

CREATE TRIGGER snapshot_lineage_update BEFORE UPDATE ON version_snapshot
BEGIN
SELECT CASE WHEN NEW.previous_version_id IS NOT NULL AND NOT EXISTS(
      SELECT 1 FROM version_snapshot p WHERE p.version_id=NEW.previous_version_id
      AND p.entry_id=NEW.entry_id AND p.is_issued=1) THEN RAISE(ABORT,'R-PREDECESSOR-SAME-ISSUED-ENTRY') END;
END;

CREATE TRIGGER snapshot_cycle_update BEFORE UPDATE ON version_snapshot
BEGIN
SELECT CASE WHEN NEW.previous_version_id IS NOT NULL AND EXISTS(
      WITH RECURSIVE prior(id) AS (SELECT NEW.previous_version_id UNION
        SELECT v.previous_version_id FROM version_snapshot v JOIN prior p ON v.version_id=p.id
        WHERE v.previous_version_id IS NOT NULL) SELECT 1 FROM prior WHERE id=NEW.version_id)
      THEN RAISE(ABORT,'R-PREDECESSOR-CYCLE') END;
END;

CREATE TRIGGER snapshot_seal BEFORE UPDATE ON version_snapshot WHEN OLD.is_issued=0 AND NEW.is_issued=1
BEGIN
SELECT CASE WHEN NEW.issued_at IS NULL THEN RAISE(ABORT,'R-ISSUE-TIME-REQUIRED') END;
      SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM json_each(NEW.payload_json)) THEN RAISE(ABORT,'R-ISSUE-CONTENT-REQUIRED') END;
      SELECT CASE WHEN EXISTS(SELECT 1 FROM information_artifact a WHERE a.artifact_id=NEW.artifact_id
        AND ((a.kind='RKM-C022' AND (NEW.entry_id IS NULL OR NEW.entry_id<>a.artifact_id))
          OR (a.kind<>'RKM-C022' AND NEW.entry_id IS NOT NULL))) THEN RAISE(ABORT,'R-REVISION-TARGET-KIND') END;
END;

CREATE TRIGGER dependency_frozen_insert BEFORE INSERT ON version_dependency WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.owner_version_id AND is_issued=1)
BEGIN
SELECT RAISE(ABORT, 'R-DEPENDENCY-FROZEN');
END;

CREATE TRIGGER dependency_frozen_update BEFORE UPDATE ON version_dependency WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=OLD.owner_version_id AND is_issued=1) OR EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.owner_version_id AND is_issued=1)
BEGIN
SELECT RAISE(ABORT, 'R-DEPENDENCY-FROZEN');
END;

CREATE TRIGGER dependency_frozen_delete BEFORE DELETE ON version_dependency WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=OLD.owner_version_id AND is_issued=1)
BEGIN
SELECT RAISE(ABORT, 'R-DEPENDENCY-FROZEN');
END;

CREATE TRIGGER dependency_no_replace BEFORE INSERT ON version_dependency WHEN EXISTS(SELECT 1 FROM version_dependency WHERE owner_version_id=NEW.owner_version_id AND slot=NEW.slot)
BEGIN
SELECT RAISE(ABORT, 'R-DEPENDENCY-DUPLICATE');
END;

CREATE TRIGGER dependency_target_insert BEFORE INSERT ON version_dependency
BEGIN
SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM version_snapshot t WHERE t.version_id=NEW.target_version_id AND t.is_issued=1)
       THEN RAISE(ABORT,'R-DEPENDENCY-TARGET-NOT-ISSUED') END;
      SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM version_snapshot t JOIN information_artifact a ON a.artifact_id=t.artifact_id
        WHERE t.version_id=NEW.target_version_id AND a.kind=CASE NEW.slot WHEN 'Context' THEN 'RKM-C002' WHEN 'Method' THEN 'RKM-C035' WHEN 'Scale' THEN 'RKM-C036' WHEN 'Criteria' THEN 'RKM-C072' END) THEN RAISE(ABORT,'R-DEPENDENCY-TARGET-KIND') END;
      SELECT CASE WHEN NEW.direct_artifact_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM version_snapshot t
        WHERE t.version_id=NEW.target_version_id AND t.artifact_id=NEW.direct_artifact_id)
        THEN RAISE(ABORT,'R-DEPENDENCY-DIRECT-TARGET') END;
END;

CREATE TRIGGER dependency_target_update BEFORE UPDATE ON version_dependency
BEGIN
SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM version_snapshot t WHERE t.version_id=NEW.target_version_id AND t.is_issued=1)
       THEN RAISE(ABORT,'R-DEPENDENCY-TARGET-NOT-ISSUED') END;
      SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM version_snapshot t JOIN information_artifact a ON a.artifact_id=t.artifact_id
        WHERE t.version_id=NEW.target_version_id AND a.kind=CASE NEW.slot WHEN 'Context' THEN 'RKM-C002' WHEN 'Method' THEN 'RKM-C035' WHEN 'Scale' THEN 'RKM-C036' WHEN 'Criteria' THEN 'RKM-C072' END) THEN RAISE(ABORT,'R-DEPENDENCY-TARGET-KIND') END;
      SELECT CASE WHEN NEW.direct_artifact_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM version_snapshot t
        WHERE t.version_id=NEW.target_version_id AND t.artifact_id=NEW.direct_artifact_id)
        THEN RAISE(ABORT,'R-DEPENDENCY-DIRECT-TARGET') END;
END;

CREATE INDEX version_by_artifact ON version_snapshot(artifact_id,is_issued);

CREATE INDEX version_by_entry ON version_snapshot(entry_id,is_issued);

CREATE INDEX version_by_predecessor ON version_snapshot(previous_version_id);

CREATE INDEX dependency_by_target ON version_dependency(target_version_id);

CREATE VIEW v_issued_history AS SELECT v.version_id,v.artifact_id,v.entry_id,e.case_id,e.register_id,
          v.previous_version_id,v.payload_json,v.source_record_id,v.issued_at FROM version_snapshot v
          LEFT JOIN register_entry e ON e.entry_id=v.entry_id WHERE v.is_issued=1;

CREATE VIEW v_native_facts AS SELECT case_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-X01' AS object FROM risk_case
UNION
SELECT artifact_id,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'||kind FROM information_artifact
UNION
SELECT artifact_id,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' FROM information_artifact
UNION
SELECT version_id,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C015' FROM version_snapshot WHERE is_issued=1
UNION
SELECT version_id,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type','https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C023' FROM version_snapshot WHERE is_issued=1 AND entry_id IS NOT NULL
UNION
SELECT entry_id,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#R-01',case_id FROM register_entry
UNION
SELECT entry_id,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RX-008',register_id FROM register_entry
UNION
SELECT version_id,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RX-006',artifact_id FROM version_snapshot WHERE is_issued=1
UNION
SELECT version_id,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#R-33',entry_id FROM version_snapshot WHERE is_issued=1 AND entry_id IS NOT NULL
UNION
SELECT version_id,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#R-34',previous_version_id FROM version_snapshot WHERE is_issued=1 AND previous_version_id IS NOT NULL;
