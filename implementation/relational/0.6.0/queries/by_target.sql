-- An exact target-version pin; all explicitly qualified reference versions.
SELECT e.version_id,e.artifact_id,e.evidential_role,e.item_id,e.item_version_id,e.statement,
 e.source_record_id,s.original_json,e.source_locator,e.interpretation_origin,e.recorded_at,
 iv.source_record_id,items.original_json,
 (SELECT json_group_array(target_version_id) FROM (SELECT target_version_id FROM evidence_target WHERE version_id=e.version_id ORDER BY target_version_id))
FROM evidence_snapshot e JOIN version_snapshot v USING(version_id)
JOIN source_record s ON s.record_id=e.source_record_id
JOIN version_snapshot iv ON iv.version_id=e.item_version_id
JOIN source_record items ON items.record_id=iv.source_record_id
WHERE v.is_issued=1 AND EXISTS(SELECT 1 FROM evidence_target t WHERE t.version_id=e.version_id AND t.target_version_id=:target)
ORDER BY e.version_id;
