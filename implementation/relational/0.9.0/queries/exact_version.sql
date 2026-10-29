SELECT n.*,
 t.artifact_id AS term_id, s.artifact_id AS scheme_id,s.version_id AS scheme_version_id,
 c.artifact_id AS context_id,
 (SELECT json_group_array(objective_version_id) FROM
   (SELECT objective_version_id FROM nature_objective WHERE context_version_id=n.context_version_id ORDER BY objective_version_id)) AS objective_version_ids,
 (SELECT json_group_array(entry_version_id) FROM
   (SELECT entry_version_id FROM nature_entry_link WHERE nature_version_id=n.version_id ORDER BY entry_version_id)) AS recording_entry_version_ids,
 CASE WHEN n.context_version_id IS NULL THEN 'NOT_READY_CONTEXT_UNRECORDED'
      WHEN NOT EXISTS(SELECT 1 FROM nature_objective WHERE context_version_id=n.context_version_id) THEN 'NOT_READY_OBJECTIVES_UNRECORDED'
      ELSE 'READY_FOR_DECLARED_RETRIEVAL' END AS readiness
FROM nature_snapshot n JOIN version_snapshot v ON v.version_id=n.version_id AND v.is_issued=1
JOIN nature_support t ON t.version_id=n.term_version_id
JOIN nature_support s ON s.version_id=t.scheme_version_id
LEFT JOIN nature_context c ON c.version_id=n.context_version_id
WHERE n.version_id=:version;
