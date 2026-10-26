-- All declared descendants, including branches; never a latest-wins selection.
WITH RECURSIVE family(id) AS (
 SELECT a.assessment_version_id FROM assessment_snapshot a JOIN version_snapshot v ON v.version_id=a.assessment_version_id WHERE a.assessment_version_id=:root AND v.is_issued=1
 UNION SELECT c.corrected_version_id FROM assessment_correction c JOIN family f ON c.prior_version_id=f.id
)
SELECT r.assessment_version_id,r.result_version_id,r.score_kind,r.reported_value,r.source_record_id
FROM result_snapshot r JOIN family f ON f.id=r.assessment_version_id
JOIN version_snapshot v ON v.version_id=r.result_version_id AND v.is_issued=1
ORDER BY r.assessment_version_id,r.result_version_id;
