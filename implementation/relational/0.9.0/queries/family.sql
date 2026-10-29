WITH RECURSIVE family(version_id,depth) AS (
 SELECT :root,0 UNION ALL
 SELECT c.corrected_version_id,f.depth+1 FROM nature_correction c JOIN family f ON c.prior_version_id=f.version_id
) SELECT f.version_id,f.depth,c.prior_version_id FROM family f
LEFT JOIN nature_correction c ON c.corrected_version_id=f.version_id ORDER BY f.depth,f.version_id;
