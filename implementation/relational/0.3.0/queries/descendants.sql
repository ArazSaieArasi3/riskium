WITH RECURSIVE family(id,depth) AS (
 SELECT a.assessment_version_id,0 FROM assessment_snapshot a JOIN version_snapshot v ON v.version_id=a.assessment_version_id WHERE a.assessment_version_id=:root AND v.is_issued=1
 UNION ALL SELECT c.corrected_version_id,f.depth+1 FROM assessment_correction c JOIN family f ON c.prior_version_id=f.id
)
SELECT id,depth FROM family ORDER BY depth,id;
