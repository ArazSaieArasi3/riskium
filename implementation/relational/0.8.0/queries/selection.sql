WITH latest AS (
 SELECT * FROM assessment_selection_event
 WHERE assessment_id=:assessment AND decision_context_id=:context
 AND ordinal<=:as_of AND kind IN ('SELECT','CLEAR')
 ORDER BY ordinal DESC LIMIT 1
), answer AS (
 SELECT CASE WHEN l.kind IS NULL OR l.kind='CLEAR' THEN 'NO_SELECTION'
 WHEN EXISTS(SELECT 1 FROM assessment_selection_event w WHERE w.assessment_id=:assessment
 AND w.decision_context_id=:context AND w.kind='WITHDRAW' AND w.target_version=l.target_version
 AND w.ordinal<=:as_of) THEN 'WITHDRAWN' ELSE 'SELECTED' END AS state,
 l.target_version AS last_selected_version
 FROM (SELECT 1) anchor LEFT JOIN latest l ON 1=1
)
SELECT state,CASE WHEN state='SELECTED' THEN last_selected_version END AS assessment_version,
 last_selected_version FROM answer;
