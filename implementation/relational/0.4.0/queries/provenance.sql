SELECT k.version_id,k.source_record_id,s.original_json,k.source_locator,k.interpretation_origin,k.narrative
FROM knowledge_snapshot k JOIN version_snapshot v USING(version_id)
JOIN source_record s ON s.record_id=k.source_record_id
WHERE k.version_id=:version_id AND v.is_issued=1;
