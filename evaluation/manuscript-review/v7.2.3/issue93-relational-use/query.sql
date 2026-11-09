SELECT u.id,rv.artifact_id,u.reference_version,iv.artifact_id,u.item_version,cv.artifact_id,u.context_version,g.artifact_id,u.grounding_version,u.purpose
FROM evidence_use u
JOIN artifact_version rv ON rv.id=u.reference_version
JOIN artifact_version iv ON iv.id=u.item_version
JOIN artifact_version cv ON cv.id=u.context_version
JOIN grounding_record g ON g.version_id=u.grounding_version
ORDER BY u.id;
