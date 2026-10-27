SELECT k.version_id,t.native_class,k.artifact_id,k.source_record_id,k.source_locator
FROM knowledge_case c JOIN knowledge_snapshot k USING(version_id)
JOIN knowledge_type t ON t.artifact_id=k.artifact_id
JOIN version_snapshot v USING(version_id)
WHERE c.case_id=:case_id AND v.is_issued=1 ORDER BY k.version_id;
