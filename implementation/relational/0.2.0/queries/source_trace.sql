SELECT result_version_id,source_locator FROM result_snapshot
WHERE source_record_id=:source_record ORDER BY result_version_id;
