-- Exact root plus explicit descendants. No latest/authority selection or graph union.
WITH RECURSIVE family(id) AS (
 SELECT k.version_id FROM knowledge_snapshot k JOIN version_snapshot v USING(version_id)
 WHERE k.version_id=:root AND v.is_issued=1
 UNION SELECT c.corrected_version_id FROM knowledge_correction c JOIN family f ON c.prior_version_id=f.id
)
SELECT k.version_id,k.artifact_id,t.native_class,k.narrative,k.source_record_id,s.original_json,
 k.source_locator,k.interpretation_origin,k.recorded_at,
 (SELECT json_group_array(case_id) FROM (SELECT case_id FROM knowledge_case WHERE version_id=k.version_id ORDER BY case_id)),
 (SELECT json_group_array(context_version_id) FROM (SELECT context_version_id FROM knowledge_context WHERE version_id=k.version_id ORDER BY context_version_id)),
 c.prior_version_id,c.reason,c.recorded_at,c.source_record_id,ds.original_json,c.source_locator,c.interpretation_origin
FROM family f JOIN knowledge_snapshot k ON k.version_id=f.id
JOIN knowledge_type t ON t.artifact_id=k.artifact_id
JOIN source_record s ON s.record_id=k.source_record_id
LEFT JOIN knowledge_correction c ON c.corrected_version_id=k.version_id
LEFT JOIN source_record ds ON ds.record_id=c.source_record_id
ORDER BY k.version_id;
