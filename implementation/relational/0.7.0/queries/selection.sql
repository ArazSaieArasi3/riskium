WITH latest AS (
 SELECT sequence,kind,version_id FROM v_evidence_lifecycle_ledger
 WHERE context_id=:context AND artifact_id=:artifact
 AND kind IN ('SELECT','CLEAR') AND sequence<=:as_of_sequence
 ORDER BY sequence DESC LIMIT 1
), state AS (
 SELECT CASE WHEN l.kind IS NULL OR l.kind='CLEAR' THEN 'NO_SELECTION'
 WHEN EXISTS(SELECT 1 FROM v_evidence_lifecycle_ledger w WHERE w.kind='WITHDRAW'
 AND w.context_id=:context AND w.artifact_id=:artifact AND w.version_id=l.version_id
 AND w.sequence<=:as_of_sequence) THEN 'WITHDRAWN' ELSE 'SELECTED' END AS status,
 CASE WHEN l.kind='SELECT' THEN l.version_id END AS last_selected_version
 FROM (SELECT 1) anchor LEFT JOIN latest l ON 1=1
)
SELECT status,CASE WHEN status='SELECTED' THEN last_selected_version END AS selected_version,
 last_selected_version FROM state;
