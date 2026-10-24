-- Generated guards and selected named-graph projections; no native ontology changes.

CREATE VIEW v_profile_artifact_type AS SELECT artifact_id,kind AS native_class FROM information_artifact UNION SELECT artifact_id,native_class FROM artifact_typing;

CREATE TRIGGER a_typing_insert BEFORE INSERT ON artifact_typing
BEGIN
SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM information_artifact WHERE artifact_id=NEW.artifact_id AND kind='RKM-C014') THEN RAISE(ABORT,'R-TYPE-BASE-KIND') END;SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE artifact_id=NEW.artifact_id AND is_issued=1) THEN RAISE(ABORT,'R-TYPE-ALREADY-ISSUED') END;SELECT CASE WHEN EXISTS(SELECT 1 FROM artifact_typing WHERE artifact_id=NEW.artifact_id) THEN RAISE(ABORT,'R-METADATA-DUPLICATE') END;
END;

CREATE TRIGGER a_typing_update BEFORE UPDATE ON artifact_typing
BEGIN
SELECT CASE WHEN 1 THEN RAISE(ABORT,'R-CATALOG-IMMUTABLE') END;
END;

CREATE TRIGGER a_typing_delete BEFORE DELETE ON artifact_typing
BEGIN
SELECT CASE WHEN 1 THEN RAISE(ABORT,'R-CATALOG-IMMUTABLE') END;
END;

CREATE TRIGGER a_scale_snapshot_insert BEFORE INSERT ON scale_snapshot
BEGIN
SELECT CASE WHEN EXISTS(SELECT 1 FROM scale_snapshot WHERE scale_version_id=NEW.scale_version_id) THEN RAISE(ABORT,'R-METADATA-DUPLICATE') END;SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.scale_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ISSUED-METADATA') END;SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM version_snapshot v JOIN information_artifact a ON a.artifact_id=v.artifact_id WHERE v.version_id=NEW.scale_version_id AND v.artifact_id=NEW.scale_id AND a.kind='RKM-C036') THEN RAISE(ABORT,'R-SCALE-VERSION-TARGET') END;SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM v_profile_artifact_type WHERE artifact_id=NEW.dimension_id AND native_class='RKM-C039') THEN RAISE(ABORT,'R-DIMENSION-KIND') END;
END;

CREATE TRIGGER a_scale_snapshot_update BEFORE UPDATE ON scale_snapshot
BEGIN
SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=OLD.scale_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ISSUED-METADATA') END;SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.scale_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ISSUED-METADATA') END;SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM version_snapshot v JOIN information_artifact a ON a.artifact_id=v.artifact_id WHERE v.version_id=NEW.scale_version_id AND v.artifact_id=NEW.scale_id AND a.kind='RKM-C036') THEN RAISE(ABORT,'R-SCALE-VERSION-TARGET') END;SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM v_profile_artifact_type WHERE artifact_id=NEW.dimension_id AND native_class='RKM-C039') THEN RAISE(ABORT,'R-DIMENSION-KIND') END;
END;

CREATE TRIGGER a_scale_snapshot_delete BEFORE DELETE ON scale_snapshot
BEGIN
SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=OLD.scale_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ISSUED-METADATA') END;
END;

CREATE TRIGGER a_scale_level_insert BEFORE INSERT ON scale_level
BEGIN
SELECT CASE WHEN EXISTS(SELECT 1 FROM scale_level WHERE level_id=NEW.level_id) THEN RAISE(ABORT,'R-METADATA-DUPLICATE') END;SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.scale_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ISSUED-METADATA') END;SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM v_profile_artifact_type WHERE artifact_id=NEW.level_id AND native_class='RKM-C038') THEN RAISE(ABORT,'R-LEVEL-KIND') END;
END;

CREATE TRIGGER a_scale_level_update BEFORE UPDATE ON scale_level
BEGIN
SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=OLD.scale_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ISSUED-METADATA') END;SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.scale_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ISSUED-METADATA') END;SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM v_profile_artifact_type WHERE artifact_id=NEW.level_id AND native_class='RKM-C038') THEN RAISE(ABORT,'R-LEVEL-KIND') END;
END;

CREATE TRIGGER a_scale_level_delete BEFORE DELETE ON scale_level
BEGIN
SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=OLD.scale_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ISSUED-METADATA') END;
END;

CREATE TRIGGER a_method_scope_insert BEFORE INSERT ON method_scope
BEGIN
SELECT CASE WHEN EXISTS(SELECT 1 FROM method_scope WHERE method_version_id=NEW.method_version_id AND scale_id=NEW.scale_id AND dimension_id=NEW.dimension_id) THEN RAISE(ABORT,'R-METADATA-DUPLICATE') END;SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.method_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ISSUED-METADATA') END;SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM version_snapshot v JOIN information_artifact a ON a.artifact_id=v.artifact_id WHERE v.version_id=NEW.method_version_id AND a.kind='RKM-C035') THEN RAISE(ABORT,'R-METHOD-VERSION-KIND') END;SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM v_profile_artifact_type WHERE artifact_id=NEW.scale_id AND native_class='RKM-C036') OR NOT EXISTS(SELECT 1 FROM v_profile_artifact_type WHERE artifact_id=NEW.dimension_id AND native_class='RKM-C039') THEN RAISE(ABORT,'R-SCOPE-KIND') END;
END;

CREATE TRIGGER a_method_scope_update BEFORE UPDATE ON method_scope
BEGIN
SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=OLD.method_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ISSUED-METADATA') END;SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.method_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ISSUED-METADATA') END;SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM version_snapshot v JOIN information_artifact a ON a.artifact_id=v.artifact_id WHERE v.version_id=NEW.method_version_id AND a.kind='RKM-C035') THEN RAISE(ABORT,'R-METHOD-VERSION-KIND') END;SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM v_profile_artifact_type WHERE artifact_id=NEW.scale_id AND native_class='RKM-C036') OR NOT EXISTS(SELECT 1 FROM v_profile_artifact_type WHERE artifact_id=NEW.dimension_id AND native_class='RKM-C039') THEN RAISE(ABORT,'R-SCOPE-KIND') END;
END;

CREATE TRIGGER a_method_scope_delete BEFORE DELETE ON method_scope
BEGIN
SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=OLD.method_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ISSUED-METADATA') END;
END;

CREATE TRIGGER a_assessment_snapshot_insert BEFORE INSERT ON assessment_snapshot
BEGIN
SELECT CASE WHEN EXISTS(SELECT 1 FROM assessment_snapshot WHERE assessment_version_id=NEW.assessment_version_id) THEN RAISE(ABORT,'R-METADATA-DUPLICATE') END;SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.assessment_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ISSUED-METADATA') END;SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM v_profile_artifact_type WHERE artifact_id=NEW.assessment_id AND native_class='RKM-C032') OR NOT EXISTS(SELECT 1 FROM v_profile_artifact_type WHERE artifact_id=NEW.basis_id AND native_class='RKM-C033') THEN RAISE(ABORT,'R-ASSESSMENT-KIND') END;SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.assessment_version_id AND artifact_id=NEW.assessment_id) THEN RAISE(ABORT,'R-OWNER-VERSION-TARGET') END;SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.context_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ROLE-ISSUED') END;SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM version_snapshot v JOIN v_profile_artifact_type t ON t.artifact_id=v.artifact_id WHERE v.version_id=NEW.context_version_id AND t.native_class='RKM-C002') THEN RAISE(ABORT,'R-ROLE-KIND') END;SELECT CASE WHEN NEW.context_version_id IS NOT NULL AND NEW.context_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.context_version_id AND artifact_id=NEW.context_id) THEN RAISE(ABORT,'R-ROLE-TARGET') END;SELECT CASE WHEN NEW.context_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM v_profile_artifact_type WHERE artifact_id=NEW.context_id AND native_class='RKM-C002') THEN RAISE(ABORT,'R-ROLE-KIND') END;SELECT CASE WHEN NEW.method_version_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.method_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ROLE-ISSUED') END;SELECT CASE WHEN NEW.method_version_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM version_snapshot v JOIN v_profile_artifact_type t ON t.artifact_id=v.artifact_id WHERE v.version_id=NEW.method_version_id AND t.native_class='RKM-C035') THEN RAISE(ABORT,'R-ROLE-KIND') END;SELECT CASE WHEN NEW.method_version_id IS NOT NULL AND NEW.method_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.method_version_id AND artifact_id=NEW.method_id) THEN RAISE(ABORT,'R-ROLE-TARGET') END;SELECT CASE WHEN NEW.method_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM v_profile_artifact_type WHERE artifact_id=NEW.method_id AND native_class='RKM-C035') THEN RAISE(ABORT,'R-ROLE-KIND') END;SELECT CASE WHEN NEW.basis_version_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.basis_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ROLE-ISSUED') END;SELECT CASE WHEN NEW.basis_version_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM version_snapshot v JOIN v_profile_artifact_type t ON t.artifact_id=v.artifact_id WHERE v.version_id=NEW.basis_version_id AND t.native_class='RKM-C033') THEN RAISE(ABORT,'R-ROLE-KIND') END;SELECT CASE WHEN NEW.basis_version_id IS NOT NULL AND NEW.basis_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.basis_version_id AND artifact_id=NEW.basis_id) THEN RAISE(ABORT,'R-ROLE-TARGET') END;SELECT CASE WHEN NEW.basis_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM v_profile_artifact_type WHERE artifact_id=NEW.basis_id AND native_class='RKM-C033') THEN RAISE(ABORT,'R-ROLE-KIND') END;SELECT CASE WHEN NEW.recorded_at IS NOT NULL AND (length(NEW.recorded_at)<>20 OR NEW.recorded_at NOT GLOB '????-??-??T??:??:??Z' OR substr(NEW.recorded_at,1,4)<'0001' OR COALESCE(strftime('%Y-%m-%dT%H:%M:%SZ',NEW.recorded_at,'+0 seconds'),'')<>NEW.recorded_at) THEN RAISE(ABORT,'R-TIME-LEXICAL') END;SELECT CASE WHEN NEW.reference_at IS NOT NULL AND (length(NEW.reference_at)<>20 OR NEW.reference_at NOT GLOB '????-??-??T??:??:??Z' OR substr(NEW.reference_at,1,4)<'0001' OR COALESCE(strftime('%Y-%m-%dT%H:%M:%SZ',NEW.reference_at,'+0 seconds'),'')<>NEW.reference_at) THEN RAISE(ABORT,'R-TIME-LEXICAL') END;SELECT CASE WHEN NEW.valid_from IS NOT NULL AND (length(NEW.valid_from)<>20 OR NEW.valid_from NOT GLOB '????-??-??T??:??:??Z' OR substr(NEW.valid_from,1,4)<'0001' OR COALESCE(strftime('%Y-%m-%dT%H:%M:%SZ',NEW.valid_from,'+0 seconds'),'')<>NEW.valid_from) THEN RAISE(ABORT,'R-TIME-LEXICAL') END;SELECT CASE WHEN NEW.valid_to IS NOT NULL AND (length(NEW.valid_to)<>20 OR NEW.valid_to NOT GLOB '????-??-??T??:??:??Z' OR substr(NEW.valid_to,1,4)<'0001' OR COALESCE(strftime('%Y-%m-%dT%H:%M:%SZ',NEW.valid_to,'+0 seconds'),'')<>NEW.valid_to) THEN RAISE(ABORT,'R-TIME-LEXICAL') END;SELECT CASE WHEN NEW.valid_from IS NOT NULL AND NEW.valid_to IS NOT NULL AND NEW.valid_to<NEW.valid_from THEN RAISE(ABORT,'R-TIME-ORDER') END;
END;

CREATE TRIGGER a_assessment_snapshot_update BEFORE UPDATE ON assessment_snapshot
BEGIN
SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=OLD.assessment_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ISSUED-METADATA') END;SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.assessment_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ISSUED-METADATA') END;SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM v_profile_artifact_type WHERE artifact_id=NEW.assessment_id AND native_class='RKM-C032') OR NOT EXISTS(SELECT 1 FROM v_profile_artifact_type WHERE artifact_id=NEW.basis_id AND native_class='RKM-C033') THEN RAISE(ABORT,'R-ASSESSMENT-KIND') END;SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.assessment_version_id AND artifact_id=NEW.assessment_id) THEN RAISE(ABORT,'R-OWNER-VERSION-TARGET') END;SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.context_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ROLE-ISSUED') END;SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM version_snapshot v JOIN v_profile_artifact_type t ON t.artifact_id=v.artifact_id WHERE v.version_id=NEW.context_version_id AND t.native_class='RKM-C002') THEN RAISE(ABORT,'R-ROLE-KIND') END;SELECT CASE WHEN NEW.context_version_id IS NOT NULL AND NEW.context_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.context_version_id AND artifact_id=NEW.context_id) THEN RAISE(ABORT,'R-ROLE-TARGET') END;SELECT CASE WHEN NEW.context_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM v_profile_artifact_type WHERE artifact_id=NEW.context_id AND native_class='RKM-C002') THEN RAISE(ABORT,'R-ROLE-KIND') END;SELECT CASE WHEN NEW.method_version_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.method_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ROLE-ISSUED') END;SELECT CASE WHEN NEW.method_version_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM version_snapshot v JOIN v_profile_artifact_type t ON t.artifact_id=v.artifact_id WHERE v.version_id=NEW.method_version_id AND t.native_class='RKM-C035') THEN RAISE(ABORT,'R-ROLE-KIND') END;SELECT CASE WHEN NEW.method_version_id IS NOT NULL AND NEW.method_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.method_version_id AND artifact_id=NEW.method_id) THEN RAISE(ABORT,'R-ROLE-TARGET') END;SELECT CASE WHEN NEW.method_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM v_profile_artifact_type WHERE artifact_id=NEW.method_id AND native_class='RKM-C035') THEN RAISE(ABORT,'R-ROLE-KIND') END;SELECT CASE WHEN NEW.basis_version_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.basis_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ROLE-ISSUED') END;SELECT CASE WHEN NEW.basis_version_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM version_snapshot v JOIN v_profile_artifact_type t ON t.artifact_id=v.artifact_id WHERE v.version_id=NEW.basis_version_id AND t.native_class='RKM-C033') THEN RAISE(ABORT,'R-ROLE-KIND') END;SELECT CASE WHEN NEW.basis_version_id IS NOT NULL AND NEW.basis_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.basis_version_id AND artifact_id=NEW.basis_id) THEN RAISE(ABORT,'R-ROLE-TARGET') END;SELECT CASE WHEN NEW.basis_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM v_profile_artifact_type WHERE artifact_id=NEW.basis_id AND native_class='RKM-C033') THEN RAISE(ABORT,'R-ROLE-KIND') END;SELECT CASE WHEN NEW.recorded_at IS NOT NULL AND (length(NEW.recorded_at)<>20 OR NEW.recorded_at NOT GLOB '????-??-??T??:??:??Z' OR substr(NEW.recorded_at,1,4)<'0001' OR COALESCE(strftime('%Y-%m-%dT%H:%M:%SZ',NEW.recorded_at,'+0 seconds'),'')<>NEW.recorded_at) THEN RAISE(ABORT,'R-TIME-LEXICAL') END;SELECT CASE WHEN NEW.reference_at IS NOT NULL AND (length(NEW.reference_at)<>20 OR NEW.reference_at NOT GLOB '????-??-??T??:??:??Z' OR substr(NEW.reference_at,1,4)<'0001' OR COALESCE(strftime('%Y-%m-%dT%H:%M:%SZ',NEW.reference_at,'+0 seconds'),'')<>NEW.reference_at) THEN RAISE(ABORT,'R-TIME-LEXICAL') END;SELECT CASE WHEN NEW.valid_from IS NOT NULL AND (length(NEW.valid_from)<>20 OR NEW.valid_from NOT GLOB '????-??-??T??:??:??Z' OR substr(NEW.valid_from,1,4)<'0001' OR COALESCE(strftime('%Y-%m-%dT%H:%M:%SZ',NEW.valid_from,'+0 seconds'),'')<>NEW.valid_from) THEN RAISE(ABORT,'R-TIME-LEXICAL') END;SELECT CASE WHEN NEW.valid_to IS NOT NULL AND (length(NEW.valid_to)<>20 OR NEW.valid_to NOT GLOB '????-??-??T??:??:??Z' OR substr(NEW.valid_to,1,4)<'0001' OR COALESCE(strftime('%Y-%m-%dT%H:%M:%SZ',NEW.valid_to,'+0 seconds'),'')<>NEW.valid_to) THEN RAISE(ABORT,'R-TIME-LEXICAL') END;SELECT CASE WHEN NEW.valid_from IS NOT NULL AND NEW.valid_to IS NOT NULL AND NEW.valid_to<NEW.valid_from THEN RAISE(ABORT,'R-TIME-ORDER') END;
END;

CREATE TRIGGER a_assessment_snapshot_delete BEFORE DELETE ON assessment_snapshot
BEGIN
SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=OLD.assessment_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ISSUED-METADATA') END;
END;

CREATE TRIGGER a_result_snapshot_insert BEFORE INSERT ON result_snapshot
BEGIN
SELECT CASE WHEN EXISTS(SELECT 1 FROM result_snapshot WHERE result_version_id=NEW.result_version_id) THEN RAISE(ABORT,'R-METADATA-DUPLICATE') END;SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.result_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ISSUED-METADATA') END;SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.assessment_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ASSESSMENT-FROZEN') END;SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM v_profile_artifact_type WHERE artifact_id=NEW.result_id AND native_class='RKM-C034') THEN RAISE(ABORT,'R-RESULT-KIND') END;SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.result_version_id AND artifact_id=NEW.result_id) THEN RAISE(ABORT,'R-OWNER-VERSION-TARGET') END;SELECT CASE WHEN NEW.dimension_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM v_profile_artifact_type WHERE artifact_id=NEW.dimension_id AND native_class='RKM-C039') THEN RAISE(ABORT,'R-DIMENSION-KIND') END;SELECT CASE WHEN NEW.scale_version_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.scale_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ROLE-ISSUED') END;SELECT CASE WHEN NEW.scale_version_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM version_snapshot v JOIN v_profile_artifact_type t ON t.artifact_id=v.artifact_id WHERE v.version_id=NEW.scale_version_id AND t.native_class='RKM-C036') THEN RAISE(ABORT,'R-ROLE-KIND') END;SELECT CASE WHEN NEW.scale_version_id IS NOT NULL AND NEW.scale_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.scale_version_id AND artifact_id=NEW.scale_id) THEN RAISE(ABORT,'R-ROLE-TARGET') END;SELECT CASE WHEN NEW.scale_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM v_profile_artifact_type WHERE artifact_id=NEW.scale_id AND native_class='RKM-C036') THEN RAISE(ABORT,'R-ROLE-KIND') END;SELECT CASE WHEN NEW.dimension_id IS NOT NULL AND NEW.scale_version_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM scale_snapshot WHERE scale_version_id=NEW.scale_version_id AND dimension_id=NEW.dimension_id) THEN RAISE(ABORT,'R-SCALE-DIMENSION') END;SELECT CASE WHEN NEW.level_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM scale_level WHERE level_id=NEW.level_id AND scale_version_id=NEW.scale_version_id) THEN RAISE(ABORT,'R-LEVEL-VERSION') END;SELECT CASE WHEN EXISTS(SELECT 1 FROM result_snapshot old JOIN assessment_snapshot a ON a.assessment_version_id=old.assessment_version_id JOIN assessment_snapshot n ON n.assessment_version_id=NEW.assessment_version_id WHERE old.result_id=NEW.result_id AND a.assessment_id<>n.assessment_id) THEN RAISE(ABORT,'R-RESULT-PARENT-IDENTITY') END;SELECT CASE WHEN NEW.score_kind='COMPUTED' THEN RAISE(ABORT,'R-COMPUTATION-UNSUPPORTED') END;SELECT CASE WHEN NEW.score_kind NOT IN ('REPORTED','UNKNOWN','COMPUTED') THEN RAISE(ABORT,'R-SCORE-KIND') END;SELECT CASE WHEN NEW.score_kind='REPORTED' AND (NEW.reported_value IS NULL OR length(trim(NEW.reported_value))=0) THEN RAISE(ABORT,'R-REPORTED-VALUE') END;SELECT CASE WHEN NEW.score_kind='UNKNOWN' AND NEW.reported_value IS NOT NULL THEN RAISE(ABORT,'R-UNKNOWN-VALUE') END;SELECT CASE WHEN length(trim(NEW.source_locator))=0 OR length(trim(NEW.interpretation_origin))=0 THEN RAISE(ABORT,'R-SOURCE-QUALIFIER') END;
END;

CREATE TRIGGER a_result_snapshot_update BEFORE UPDATE ON result_snapshot
BEGIN
SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=OLD.result_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ISSUED-METADATA') END;SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.result_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ISSUED-METADATA') END;SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=OLD.assessment_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ASSESSMENT-FROZEN') END;SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.assessment_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ASSESSMENT-FROZEN') END;SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM v_profile_artifact_type WHERE artifact_id=NEW.result_id AND native_class='RKM-C034') THEN RAISE(ABORT,'R-RESULT-KIND') END;SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.result_version_id AND artifact_id=NEW.result_id) THEN RAISE(ABORT,'R-OWNER-VERSION-TARGET') END;SELECT CASE WHEN NEW.dimension_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM v_profile_artifact_type WHERE artifact_id=NEW.dimension_id AND native_class='RKM-C039') THEN RAISE(ABORT,'R-DIMENSION-KIND') END;SELECT CASE WHEN NEW.scale_version_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.scale_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ROLE-ISSUED') END;SELECT CASE WHEN NEW.scale_version_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM version_snapshot v JOIN v_profile_artifact_type t ON t.artifact_id=v.artifact_id WHERE v.version_id=NEW.scale_version_id AND t.native_class='RKM-C036') THEN RAISE(ABORT,'R-ROLE-KIND') END;SELECT CASE WHEN NEW.scale_version_id IS NOT NULL AND NEW.scale_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.scale_version_id AND artifact_id=NEW.scale_id) THEN RAISE(ABORT,'R-ROLE-TARGET') END;SELECT CASE WHEN NEW.scale_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM v_profile_artifact_type WHERE artifact_id=NEW.scale_id AND native_class='RKM-C036') THEN RAISE(ABORT,'R-ROLE-KIND') END;SELECT CASE WHEN NEW.dimension_id IS NOT NULL AND NEW.scale_version_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM scale_snapshot WHERE scale_version_id=NEW.scale_version_id AND dimension_id=NEW.dimension_id) THEN RAISE(ABORT,'R-SCALE-DIMENSION') END;SELECT CASE WHEN NEW.level_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM scale_level WHERE level_id=NEW.level_id AND scale_version_id=NEW.scale_version_id) THEN RAISE(ABORT,'R-LEVEL-VERSION') END;SELECT CASE WHEN EXISTS(SELECT 1 FROM result_snapshot old JOIN assessment_snapshot a ON a.assessment_version_id=old.assessment_version_id JOIN assessment_snapshot n ON n.assessment_version_id=NEW.assessment_version_id WHERE old.result_id=NEW.result_id AND a.assessment_id<>n.assessment_id) THEN RAISE(ABORT,'R-RESULT-PARENT-IDENTITY') END;SELECT CASE WHEN NEW.score_kind='COMPUTED' THEN RAISE(ABORT,'R-COMPUTATION-UNSUPPORTED') END;SELECT CASE WHEN NEW.score_kind NOT IN ('REPORTED','UNKNOWN','COMPUTED') THEN RAISE(ABORT,'R-SCORE-KIND') END;SELECT CASE WHEN NEW.score_kind='REPORTED' AND (NEW.reported_value IS NULL OR length(trim(NEW.reported_value))=0) THEN RAISE(ABORT,'R-REPORTED-VALUE') END;SELECT CASE WHEN NEW.score_kind='UNKNOWN' AND NEW.reported_value IS NOT NULL THEN RAISE(ABORT,'R-UNKNOWN-VALUE') END;SELECT CASE WHEN length(trim(NEW.source_locator))=0 OR length(trim(NEW.interpretation_origin))=0 THEN RAISE(ABORT,'R-SOURCE-QUALIFIER') END;
END;

CREATE TRIGGER a_result_snapshot_delete BEFORE DELETE ON result_snapshot
BEGIN
SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=OLD.result_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ISSUED-METADATA') END;SELECT CASE WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=OLD.assessment_version_id AND is_issued=1) THEN RAISE(ABORT,'R-ASSESSMENT-FROZEN') END;
END;

CREATE TRIGGER a_snapshot_seal BEFORE UPDATE ON version_snapshot WHEN OLD.is_issued=0 AND NEW.is_issued=1
BEGIN
SELECT CASE WHEN NEW.issued_at IS NOT NULL AND (length(NEW.issued_at)<>20 OR substr(NEW.issued_at,1,4)<'0001' OR NEW.issued_at NOT GLOB '????-??-??T??:??:??Z' OR COALESCE(strftime('%Y-%m-%dT%H:%M:%SZ',NEW.issued_at,'+0 seconds'),'')<>NEW.issued_at) THEN RAISE(ABORT,'R-TIME-LEXICAL') END;SELECT CASE WHEN EXISTS(SELECT 1 FROM v_profile_artifact_type WHERE artifact_id=NEW.artifact_id AND native_class='RKM-C032') AND NOT EXISTS(SELECT 1 FROM assessment_snapshot WHERE assessment_version_id=NEW.version_id) THEN RAISE(ABORT,'R-ISSUE-METADATA-REQUIRED') END;SELECT CASE WHEN EXISTS(SELECT 1 FROM v_profile_artifact_type WHERE artifact_id=NEW.artifact_id AND native_class='RKM-C034') AND NOT EXISTS(SELECT 1 FROM result_snapshot WHERE result_version_id=NEW.version_id) THEN RAISE(ABORT,'R-ISSUE-METADATA-REQUIRED') END;SELECT CASE WHEN EXISTS(SELECT 1 FROM assessment_snapshot a JOIN result_snapshot r ON r.assessment_version_id=a.assessment_version_id JOIN version_snapshot v ON v.version_id=r.result_version_id WHERE a.assessment_version_id=NEW.version_id AND v.is_issued<>1) THEN RAISE(ABORT,'R-UNSEALED-RESULT') END;SELECT CASE WHEN EXISTS(SELECT 1 FROM assessment_snapshot WHERE assessment_version_id=NEW.version_id AND assessment_id<>NEW.artifact_id) THEN RAISE(ABORT,'R-OWNER-VERSION-TARGET') END;SELECT CASE WHEN EXISTS(SELECT 1 FROM result_snapshot WHERE result_version_id=NEW.version_id AND result_id<>NEW.artifact_id) THEN RAISE(ABORT,'R-OWNER-VERSION-TARGET') END;SELECT CASE WHEN EXISTS(SELECT 1 FROM scale_snapshot WHERE scale_version_id=NEW.version_id AND scale_id<>NEW.artifact_id) THEN RAISE(ABORT,'R-OWNER-VERSION-TARGET') END;SELECT CASE WHEN EXISTS(SELECT 1 FROM assessment_snapshot m WHERE m.assessment_version_id=NEW.version_id AND (json_type(NEW.payload_json,'$.assessment_version_id') IS NULL OR json_extract(NEW.payload_json,'$.assessment_version_id') IS NOT m.assessment_version_id OR json_type(NEW.payload_json,'$.assessment_id') IS NULL OR json_extract(NEW.payload_json,'$.assessment_id') IS NOT m.assessment_id OR json_type(NEW.payload_json,'$.basis_id') IS NULL OR json_extract(NEW.payload_json,'$.basis_id') IS NOT m.basis_id OR json_type(NEW.payload_json,'$.basis_version_id') IS NULL OR json_extract(NEW.payload_json,'$.basis_version_id') IS NOT m.basis_version_id OR json_type(NEW.payload_json,'$.context_id') IS NULL OR json_extract(NEW.payload_json,'$.context_id') IS NOT m.context_id OR json_type(NEW.payload_json,'$.context_version_id') IS NULL OR json_extract(NEW.payload_json,'$.context_version_id') IS NOT m.context_version_id OR json_type(NEW.payload_json,'$.method_id') IS NULL OR json_extract(NEW.payload_json,'$.method_id') IS NOT m.method_id OR json_type(NEW.payload_json,'$.method_version_id') IS NULL OR json_extract(NEW.payload_json,'$.method_version_id') IS NOT m.method_version_id OR json_type(NEW.payload_json,'$.temporal_context_id') IS NULL OR json_extract(NEW.payload_json,'$.temporal_context_id') IS NOT m.temporal_context_id OR json_type(NEW.payload_json,'$.recorded_at') IS NULL OR json_extract(NEW.payload_json,'$.recorded_at') IS NOT m.recorded_at OR json_type(NEW.payload_json,'$.reference_at') IS NULL OR json_extract(NEW.payload_json,'$.reference_at') IS NOT m.reference_at OR json_type(NEW.payload_json,'$.valid_from') IS NULL OR json_extract(NEW.payload_json,'$.valid_from') IS NOT m.valid_from OR json_type(NEW.payload_json,'$.valid_to') IS NULL OR json_extract(NEW.payload_json,'$.valid_to') IS NOT m.valid_to OR json_type(NEW.payload_json,'$.source_record_id') IS NULL OR json_extract(NEW.payload_json,'$.source_record_id') IS NOT m.source_record_id)) THEN RAISE(ABORT,'R-PAYLOAD-METADATA-MISMATCH') END;SELECT CASE WHEN EXISTS(SELECT 1 FROM result_snapshot m WHERE m.result_version_id=NEW.version_id AND (json_type(NEW.payload_json,'$.result_version_id') IS NULL OR json_extract(NEW.payload_json,'$.result_version_id') IS NOT m.result_version_id OR json_type(NEW.payload_json,'$.result_id') IS NULL OR json_extract(NEW.payload_json,'$.result_id') IS NOT m.result_id OR json_type(NEW.payload_json,'$.assessment_version_id') IS NULL OR json_extract(NEW.payload_json,'$.assessment_version_id') IS NOT m.assessment_version_id OR json_type(NEW.payload_json,'$.dimension_id') IS NULL OR json_extract(NEW.payload_json,'$.dimension_id') IS NOT m.dimension_id OR json_type(NEW.payload_json,'$.scale_id') IS NULL OR json_extract(NEW.payload_json,'$.scale_id') IS NOT m.scale_id OR json_type(NEW.payload_json,'$.scale_version_id') IS NULL OR json_extract(NEW.payload_json,'$.scale_version_id') IS NOT m.scale_version_id OR json_type(NEW.payload_json,'$.level_id') IS NULL OR json_extract(NEW.payload_json,'$.level_id') IS NOT m.level_id OR json_type(NEW.payload_json,'$.score_kind') IS NULL OR json_extract(NEW.payload_json,'$.score_kind') IS NOT m.score_kind OR json_type(NEW.payload_json,'$.reported_value') IS NULL OR json_extract(NEW.payload_json,'$.reported_value') IS NOT m.reported_value OR json_type(NEW.payload_json,'$.source_record_id') IS NULL OR json_extract(NEW.payload_json,'$.source_record_id') IS NOT m.source_record_id OR json_type(NEW.payload_json,'$.source_locator') IS NULL OR json_extract(NEW.payload_json,'$.source_locator') IS NOT m.source_locator OR json_type(NEW.payload_json,'$.interpretation_origin') IS NULL OR json_extract(NEW.payload_json,'$.interpretation_origin') IS NOT m.interpretation_origin)) THEN RAISE(ABORT,'R-PAYLOAD-METADATA-MISMATCH') END;
END;

CREATE VIEW v_assessment_frame AS SELECT r.result_version_id,r.result_id,r.assessment_version_id,a.assessment_id,
      a.context_id,a.context_version_id,a.method_id,a.method_version_id,a.basis_id,a.basis_version_id,a.temporal_context_id,
      a.recorded_at,a.reference_at,a.valid_from,a.valid_to,r.dimension_id,r.scale_id,r.scale_version_id,r.level_id,
      r.score_kind,r.reported_value,r.source_record_id,a.source_record_id AS assessment_source_record_id,r.source_locator,r.interpretation_origin
      FROM result_snapshot r JOIN assessment_snapshot a USING(assessment_version_id)
      JOIN version_snapshot av ON av.version_id=a.assessment_version_id AND av.is_issued=1
      JOIN version_snapshot rv ON rv.version_id=r.result_version_id AND rv.is_issued=1;

CREATE VIEW v_assessment_quads AS
SELECT f.assessment_version_id AS graph_id,f.assessment_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C032' AS object FROM v_assessment_frame f  WHERE 1 AND f.assessment_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C032' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.assessment_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' AS object FROM v_assessment_frame f  WHERE 1 AND f.assessment_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.result_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C034' AS object FROM v_assessment_frame f  WHERE 1 AND f.result_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C034' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.result_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' AS object FROM v_assessment_frame f  WHERE 1 AND f.result_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.basis_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C033' AS object FROM v_assessment_frame f  WHERE 1 AND f.basis_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C033' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.basis_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' AS object FROM v_assessment_frame f  WHERE 1 AND f.basis_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.dimension_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C039' AS object FROM v_assessment_frame f  WHERE 1 AND f.dimension_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C039' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.dimension_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' AS object FROM v_assessment_frame f  WHERE 1 AND f.dimension_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.level_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C038' AS object FROM v_assessment_frame f  WHERE 1 AND f.level_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C038' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.level_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' AS object FROM v_assessment_frame f  WHERE 1 AND f.level_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.context_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C002' AS object FROM v_assessment_frame f  WHERE 1 AND f.context_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C002' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.context_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' AS object FROM v_assessment_frame f  WHERE 1 AND f.context_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.method_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C035' AS object FROM v_assessment_frame f  WHERE 1 AND f.method_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C035' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.method_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' AS object FROM v_assessment_frame f  WHERE 1 AND f.method_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.scale_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C036' AS object FROM v_assessment_frame f  WHERE 1 AND f.scale_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C036' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.scale_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' AS object FROM v_assessment_frame f  WHERE 1 AND f.scale_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.assessment_id AS subject,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#R-12' AS predicate,f.basis_id AS object FROM v_assessment_frame f  WHERE 1 AND f.assessment_id IS NOT NULL AND f.basis_id IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.assessment_id AS subject,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#R-13' AS predicate,f.result_id AS object FROM v_assessment_frame f  WHERE 1 AND f.assessment_id IS NOT NULL AND f.result_id IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.assessment_id AS subject,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#R-45' AS predicate,f.context_id AS object FROM v_assessment_frame f  WHERE 1 AND f.assessment_id IS NOT NULL AND f.context_id IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.assessment_id AS subject,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#R-46' AS predicate,f.method_id AS object FROM v_assessment_frame f  WHERE 1 AND f.assessment_id IS NOT NULL AND f.method_id IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.assessment_id AS subject,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RX-014' AS predicate,f.context_version_id AS object FROM v_assessment_frame f  WHERE 1 AND f.assessment_id IS NOT NULL AND f.context_version_id IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.assessment_id AS subject,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RX-015' AS predicate,f.method_version_id AS object FROM v_assessment_frame f  WHERE 1 AND f.assessment_id IS NOT NULL AND f.method_version_id IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.result_id AS subject,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#R-14' AS predicate,f.scale_id AS object FROM v_assessment_frame f  WHERE 1 AND f.result_id IS NOT NULL AND f.scale_id IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.result_id AS subject,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#R-15' AS predicate,f.level_id AS object FROM v_assessment_frame f  WHERE 1 AND f.result_id IS NOT NULL AND f.level_id IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.result_id AS subject,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#R-48' AS predicate,f.dimension_id AS object FROM v_assessment_frame f  WHERE 1 AND f.result_id IS NOT NULL AND f.dimension_id IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.result_id AS subject,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RX-016' AS predicate,f.scale_version_id AS object FROM v_assessment_frame f  WHERE 1 AND f.result_id IS NOT NULL AND f.scale_version_id IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.assessment_version_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C015' AS object FROM v_assessment_frame f  WHERE 1 AND f.assessment_version_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C015' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.assessment_version_id AS subject,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RX-006' AS predicate,v.artifact_id AS object FROM v_assessment_frame f JOIN version_snapshot v ON v.version_id=f.assessment_version_id WHERE 1 AND f.assessment_version_id IS NOT NULL AND v.artifact_id IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,v.artifact_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'||t.native_class AS object FROM v_assessment_frame f JOIN version_snapshot v ON v.version_id=f.assessment_version_id JOIN v_profile_artifact_type t ON t.artifact_id=v.artifact_id WHERE 1 AND v.artifact_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'||t.native_class IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,v.artifact_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' AS object FROM v_assessment_frame f JOIN version_snapshot v ON v.version_id=f.assessment_version_id JOIN v_profile_artifact_type t ON t.artifact_id=v.artifact_id WHERE 1 AND v.artifact_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.result_version_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C015' AS object FROM v_assessment_frame f  WHERE 1 AND f.result_version_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C015' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.result_version_id AS subject,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RX-006' AS predicate,v.artifact_id AS object FROM v_assessment_frame f JOIN version_snapshot v ON v.version_id=f.result_version_id WHERE 1 AND f.result_version_id IS NOT NULL AND v.artifact_id IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,v.artifact_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'||t.native_class AS object FROM v_assessment_frame f JOIN version_snapshot v ON v.version_id=f.result_version_id JOIN v_profile_artifact_type t ON t.artifact_id=v.artifact_id WHERE 1 AND v.artifact_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'||t.native_class IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,v.artifact_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' AS object FROM v_assessment_frame f JOIN version_snapshot v ON v.version_id=f.result_version_id JOIN v_profile_artifact_type t ON t.artifact_id=v.artifact_id WHERE 1 AND v.artifact_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.context_version_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C015' AS object FROM v_assessment_frame f  WHERE 1 AND f.context_version_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C015' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.context_version_id AS subject,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RX-006' AS predicate,v.artifact_id AS object FROM v_assessment_frame f JOIN version_snapshot v ON v.version_id=f.context_version_id WHERE 1 AND f.context_version_id IS NOT NULL AND v.artifact_id IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,v.artifact_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'||t.native_class AS object FROM v_assessment_frame f JOIN version_snapshot v ON v.version_id=f.context_version_id JOIN v_profile_artifact_type t ON t.artifact_id=v.artifact_id WHERE 1 AND v.artifact_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'||t.native_class IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,v.artifact_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' AS object FROM v_assessment_frame f JOIN version_snapshot v ON v.version_id=f.context_version_id JOIN v_profile_artifact_type t ON t.artifact_id=v.artifact_id WHERE 1 AND v.artifact_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.method_version_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C015' AS object FROM v_assessment_frame f  WHERE 1 AND f.method_version_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C015' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.method_version_id AS subject,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RX-006' AS predicate,v.artifact_id AS object FROM v_assessment_frame f JOIN version_snapshot v ON v.version_id=f.method_version_id WHERE 1 AND f.method_version_id IS NOT NULL AND v.artifact_id IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,v.artifact_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'||t.native_class AS object FROM v_assessment_frame f JOIN version_snapshot v ON v.version_id=f.method_version_id JOIN v_profile_artifact_type t ON t.artifact_id=v.artifact_id WHERE 1 AND v.artifact_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'||t.native_class IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,v.artifact_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' AS object FROM v_assessment_frame f JOIN version_snapshot v ON v.version_id=f.method_version_id JOIN v_profile_artifact_type t ON t.artifact_id=v.artifact_id WHERE 1 AND v.artifact_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.basis_version_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C015' AS object FROM v_assessment_frame f  WHERE 1 AND f.basis_version_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C015' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.basis_version_id AS subject,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RX-006' AS predicate,v.artifact_id AS object FROM v_assessment_frame f JOIN version_snapshot v ON v.version_id=f.basis_version_id WHERE 1 AND f.basis_version_id IS NOT NULL AND v.artifact_id IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,v.artifact_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'||t.native_class AS object FROM v_assessment_frame f JOIN version_snapshot v ON v.version_id=f.basis_version_id JOIN v_profile_artifact_type t ON t.artifact_id=v.artifact_id WHERE 1 AND v.artifact_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'||t.native_class IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,v.artifact_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' AS object FROM v_assessment_frame f JOIN version_snapshot v ON v.version_id=f.basis_version_id JOIN v_profile_artifact_type t ON t.artifact_id=v.artifact_id WHERE 1 AND v.artifact_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.scale_version_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C015' AS object FROM v_assessment_frame f  WHERE 1 AND f.scale_version_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C015' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.scale_version_id AS subject,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RX-006' AS predicate,v.artifact_id AS object FROM v_assessment_frame f JOIN version_snapshot v ON v.version_id=f.scale_version_id WHERE 1 AND f.scale_version_id IS NOT NULL AND v.artifact_id IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,v.artifact_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'||t.native_class AS object FROM v_assessment_frame f JOIN version_snapshot v ON v.version_id=f.scale_version_id JOIN v_profile_artifact_type t ON t.artifact_id=v.artifact_id WHERE 1 AND v.artifact_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'||t.native_class IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,v.artifact_id AS subject,'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' AS predicate,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' AS object FROM v_assessment_frame f JOIN version_snapshot v ON v.version_id=f.scale_version_id JOIN v_profile_artifact_type t ON t.artifact_id=v.artifact_id WHERE 1 AND v.artifact_id IS NOT NULL AND 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RKM-C014' IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.level_id AS subject,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#R-16' AS predicate,s.scale_id AS object FROM v_assessment_frame f JOIN scale_level l ON l.level_id=f.level_id JOIN scale_snapshot s ON s.scale_version_id=l.scale_version_id WHERE 1 AND f.level_id IS NOT NULL AND s.scale_id IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.scale_id AS subject,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RK2-019' AS predicate,s.dimension_id AS object FROM v_assessment_frame f JOIN scale_snapshot s ON s.scale_version_id=f.scale_version_id WHERE 1 AND f.scale_id IS NOT NULL AND s.dimension_id IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.method_id AS subject,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#R-49' AS predicate,m.scale_id AS object FROM v_assessment_frame f JOIN method_scope m ON m.method_version_id=f.method_version_id WHERE 1 AND f.method_id IS NOT NULL AND m.scale_id IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.method_id AS subject,'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#RK2-018' AS predicate,m.dimension_id AS object FROM v_assessment_frame f JOIN method_scope m ON m.method_version_id=f.method_version_id WHERE 1 AND f.method_id IS NOT NULL AND m.dimension_id IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.assessment_id AS subject,'https://github.com/ArazSaieArasi3/riskium/profiles/comparison/0.7.0#basisVersion' AS predicate,f.basis_version_id AS object FROM v_assessment_frame f  WHERE 1 AND f.assessment_id IS NOT NULL AND f.basis_version_id IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.assessment_id AS subject,'https://github.com/ArazSaieArasi3/riskium/profiles/comparison/0.7.0#temporalContext' AS predicate,f.temporal_context_id AS object FROM v_assessment_frame f  WHERE 1 AND f.assessment_id IS NOT NULL AND f.temporal_context_id IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.assessment_id AS subject,'https://github.com/ArazSaieArasi3/riskium/profiles/comparison/0.7.0#source' AS predicate,f.assessment_source_record_id AS object FROM v_assessment_frame f  WHERE 1 AND f.assessment_id IS NOT NULL AND f.assessment_source_record_id IS NOT NULL
UNION
SELECT f.assessment_version_id AS graph_id,f.level_id AS subject,'https://github.com/ArazSaieArasi3/riskium/profiles/comparison/0.7.0#levelScaleVersion' AS predicate,f.scale_version_id AS object FROM v_assessment_frame f  WHERE 1 AND f.level_id IS NOT NULL AND f.scale_version_id IS NOT NULL;

CREATE INDEX a_fk_artifact_typing_source_record_id ON artifact_typing(source_record_id);

CREATE INDEX a_fk_assessment_snapshot_source_record_id ON assessment_snapshot(source_record_id);

CREATE INDEX a_fk_assessment_snapshot_method_version_id ON assessment_snapshot(method_version_id);

CREATE INDEX a_fk_assessment_snapshot_method_id ON assessment_snapshot(method_id);

CREATE INDEX a_fk_assessment_snapshot_context_version_id ON assessment_snapshot(context_version_id);

CREATE INDEX a_fk_assessment_snapshot_context_id ON assessment_snapshot(context_id);

CREATE INDEX a_fk_assessment_snapshot_basis_version_id ON assessment_snapshot(basis_version_id);

CREATE INDEX a_fk_assessment_snapshot_basis_id ON assessment_snapshot(basis_id);

CREATE INDEX a_fk_assessment_snapshot_assessment_id ON assessment_snapshot(assessment_id);

CREATE INDEX a_fk_draft_dependency_direct_artifact_id ON draft_dependency(direct_artifact_id);

CREATE INDEX a_fk_draft_dependency_target_version_id ON draft_dependency(target_version_id);

CREATE INDEX a_fk_information_artifact_source_record_id ON information_artifact(source_record_id);

CREATE INDEX a_fk_method_scope_source_record_id ON method_scope(source_record_id);

CREATE INDEX a_fk_method_scope_dimension_id ON method_scope(dimension_id);

CREATE INDEX a_fk_method_scope_scale_id ON method_scope(scale_id);

CREATE INDEX a_fk_register_entry_register_id_register_kind ON register_entry(register_id,register_kind);

CREATE INDEX a_fk_register_entry_case_id ON register_entry(case_id);

CREATE INDEX a_fk_result_snapshot_source_record_id ON result_snapshot(source_record_id);

CREATE INDEX a_fk_result_snapshot_level_id ON result_snapshot(level_id);

CREATE INDEX a_fk_result_snapshot_scale_version_id ON result_snapshot(scale_version_id);

CREATE INDEX a_fk_result_snapshot_scale_id ON result_snapshot(scale_id);

CREATE INDEX a_fk_result_snapshot_dimension_id ON result_snapshot(dimension_id);

CREATE INDEX a_fk_result_snapshot_assessment_version_id ON result_snapshot(assessment_version_id);

CREATE INDEX a_fk_result_snapshot_result_id ON result_snapshot(result_id);

CREATE INDEX a_fk_risk_case_source_record_id ON risk_case(source_record_id);

CREATE INDEX a_fk_scale_level_source_record_id ON scale_level(source_record_id);

CREATE INDEX a_fk_scale_level_scale_version_id ON scale_level(scale_version_id);

CREATE INDEX a_fk_scale_snapshot_source_record_id ON scale_snapshot(source_record_id);

CREATE INDEX a_fk_scale_snapshot_dimension_id ON scale_snapshot(dimension_id);

CREATE INDEX a_fk_scale_snapshot_scale_id ON scale_snapshot(scale_id);

CREATE INDEX a_fk_version_dependency_direct_artifact_id ON version_dependency(direct_artifact_id);

CREATE INDEX a_fk_version_snapshot_source_record_id ON version_snapshot(source_record_id);

CREATE INDEX a_fk_working_draft_source_record_id ON working_draft(source_record_id);

CREATE INDEX a_fk_working_draft_previous_version_id ON working_draft(previous_version_id);

CREATE INDEX a_fk_working_draft_entry_id ON working_draft(entry_id);

CREATE INDEX a_fk_working_draft_artifact_id ON working_draft(artifact_id);
