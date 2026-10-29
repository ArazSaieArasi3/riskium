SELECT n.version_id FROM nature_snapshot n JOIN version_snapshot v USING(version_id)
WHERE n.case_id=:case AND v.is_issued=1 ORDER BY n.version_id;
