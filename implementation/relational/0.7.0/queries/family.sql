WITH RECURSIVE family(version_id) AS (
 SELECT v.version_id FROM evidence_snapshot e JOIN version_snapshot v USING(version_id)
 WHERE v.version_id=:root AND v.is_issued=1
 UNION SELECT e.version_id FROM evidence_lifecycle_event e JOIN family f ON e.prior_version_id=f.version_id
 WHERE e.kind='CORRECT'
)
SELECT r.version_id,r.artifact_id,r.statement,r.source_record_id,s.original_json,r.item_version_id,
 c.prior_version_id,c.event_id,c.source_record_id,cs.original_json,c.actor_id,c.reason,
 c.recorded_at,c.source_locator,c.interpretation_origin
FROM family f JOIN evidence_snapshot r ON r.version_id=f.version_id
JOIN source_record s ON s.record_id=r.source_record_id
LEFT JOIN evidence_lifecycle_event c ON c.version_id=r.version_id AND c.kind='CORRECT'
LEFT JOIN source_record cs ON cs.record_id=c.source_record_id ORDER BY r.version_id;
