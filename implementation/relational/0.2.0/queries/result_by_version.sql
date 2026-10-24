SELECT result_id,reported_value,context_version_id,method_version_id,
       basis_version_id,scale_version_id,dimension_id
FROM v_assessment_frame WHERE result_version_id=:result_version;
