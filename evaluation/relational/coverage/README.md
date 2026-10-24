# Full relational mapping inventory

This static audit accounts for all 306 source elements, including optional boundaries and the imported anchor. It identifies missing implementation; it does not close #12 or convert exclusions into support. No new SQL migration or scientific validation is performed by this report.

The public SQLite 0.1.0 profile explicitly represents 10 classes and exports five native predicates. Four constraints have supported subclauses, with C-25 application bindings kept distinct from native assessment roles. All other rows retain their explicit unimplemented/external disposition.

Summary: {"total_source_elements": 306, "families": {"Concept": 80, "Imported anchor": 1, "Relation": 134, "Generalization": 66, "Constraint": 25}, "dispositions": {"DEFERRED_NO_COMPLETE_SQL_MAPPING": 276, "SELECTED_STORAGE_REPRESENTATION": 10, "EXTERNAL_BOUNDARY_NOT_STORED": 11, "SELECTED_NATIVE_EXPORT": 5, "SELECTED_SUBCLAUSES_ONLY": 4}}.

[Exact per-element JSON and source hashes](report.json). Reproduce: `python tools/check_research_backlog.py --check`.

| Family | Element | Disposition | Representation or remaining scope |
| --- | --- | --- | --- |
| Concept | RKM-C001 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C002 | SELECTED_STORAGE_REPRESENTATION | Context artifact kind |
| Concept | RKM-C003 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C004 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C005 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C006 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C007 | EXTERNAL_BOUNDARY_NOT_STORED | External bearer/bridge ownership remains outside the public SQLite slice; documentary references do not establish referent truth. |
| Concept | RKM-C008 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C009 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C010 | EXTERNAL_BOUNDARY_NOT_STORED | External bearer/bridge ownership remains outside the public SQLite slice; documentary references do not establish referent truth. |
| Concept | RKM-C011 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C012 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C013 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C014 | SELECTED_STORAGE_REPRESENTATION | information_artifact |
| Concept | RKM-C015 | SELECTED_STORAGE_REPRESENTATION | version_snapshot WHERE is_issued=1 |
| Concept | RKM-C016 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C017 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C018 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C019 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C020 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C021 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C022 | SELECTED_STORAGE_REPRESENTATION | register_entry + information_artifact |
| Concept | RKM-C023 | SELECTED_STORAGE_REPRESENTATION | issued version_snapshot with entry_id |
| Concept | RKM-C024 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C025 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C026 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C027 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C028 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C029 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C030 | SELECTED_STORAGE_REPRESENTATION | register artifact kind |
| Concept | RKM-C031 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C032 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C033 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C034 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C035 | SELECTED_STORAGE_REPRESENTATION | Method artifact kind |
| Concept | RKM-C036 | SELECTED_STORAGE_REPRESENTATION | Scale artifact kind |
| Concept | RKM-C037 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C038 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C039 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C040 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C041 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C042 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C043 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C044 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C045 | EXTERNAL_BOUNDARY_NOT_STORED | External bearer/bridge ownership remains outside the public SQLite slice; documentary references do not establish referent truth. |
| Concept | RKM-C046 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C047 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C048 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C049 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C050 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C051 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C052 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C053 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C054 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C055 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C056 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C057 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C058 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C059 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C060 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C061 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C062 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C063 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C064 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C065 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C066 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C067 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C068 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C069 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C070 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C071 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C072 | SELECTED_STORAGE_REPRESENTATION | Criteria artifact kind |
| Concept | RKM-C073 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-C074 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-X01 | SELECTED_STORAGE_REPRESENTATION | risk_case |
| Concept | RKM-X02 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-X03 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-X04 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-X05 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Concept | RKM-X06 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Imported anchor | EXT-OBJECT | EXTERNAL_BOUNDARY_NOT_STORED | External bearer/bridge ownership remains outside the public SQLite slice; documentary references do not establish referent truth. |
| Relation | R-01 | SELECTED_NATIVE_EXPORT | v_native_facts: R-01 |
| Relation | R-02 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-03 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-04 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-05 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-06 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-07 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-08 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-09 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-10 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-11 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-12 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-13 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-14 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-15 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-16 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-17 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-18 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-19 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-20 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-21 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-22 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-23 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-24 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-25 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-26 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-27 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-28 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-29 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-30 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-31 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-32 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-33 | SELECTED_NATIVE_EXPORT | v_native_facts: R-33 |
| Relation | R-34 | SELECTED_NATIVE_EXPORT | v_native_facts: R-34 |
| Relation | R-35 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-36 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-37 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-38 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-39 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-40 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-41 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-42 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-43 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-44 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-45 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-46 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-47 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-48 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-49 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-50 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-51 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-52 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-53 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-54 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-55 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-56 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-57 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-58 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-59 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-60 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-61 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-62 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-63 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-64 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-65 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-66 | EXTERNAL_BOUNDARY_NOT_STORED | External bearer/bridge ownership remains outside the public SQLite slice; documentary references do not establish referent truth. |
| Relation | R-67 | EXTERNAL_BOUNDARY_NOT_STORED | External bearer/bridge ownership remains outside the public SQLite slice; documentary references do not establish referent truth. |
| Relation | R-68 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-69 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-70 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-71 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | R-72 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RX-001 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RX-002 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RX-003 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RX-004 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RX-005 | EXTERNAL_BOUNDARY_NOT_STORED | External bearer/bridge ownership remains outside the public SQLite slice; documentary references do not establish referent truth. |
| Relation | RX-006 | SELECTED_NATIVE_EXPORT | v_native_facts: RX-006 |
| Relation | RX-007 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RX-008 | SELECTED_NATIVE_EXPORT | v_native_facts: RX-008 |
| Relation | RX-009 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RX-010 | EXTERNAL_BOUNDARY_NOT_STORED | External bearer/bridge ownership remains outside the public SQLite slice; documentary references do not establish referent truth. |
| Relation | RX-011 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RX-012 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RX-013 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RX-014 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RX-015 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RX-016 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RX-017 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RX-018 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RX-019 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RX-020 | EXTERNAL_BOUNDARY_NOT_STORED | External bearer/bridge ownership remains outside the public SQLite slice; documentary references do not establish referent truth. |
| Relation | RX-021 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RX-022 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RX-023 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RX-024 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RX-025 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RX-026 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RX-027 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RX-028 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RX-029 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RX-030 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RX-031 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RX-032 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK2-001 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK2-002 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK2-003 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK2-004 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK2-005 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK2-006 | EXTERNAL_BOUNDARY_NOT_STORED | External bearer/bridge ownership remains outside the public SQLite slice; documentary references do not establish referent truth. |
| Relation | RK2-007 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK2-008 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK2-009 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK2-010 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK2-011 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK2-012 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK2-013 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK2-014 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK2-015 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK2-016 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK2-017 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK2-018 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK2-019 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK2-020 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK2-021 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK2-022 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK2-023 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK2-024 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK2-025 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK2-026 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK3-001 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK3-002 | EXTERNAL_BOUNDARY_NOT_STORED | External bearer/bridge ownership remains outside the public SQLite slice; documentary references do not establish referent truth. |
| Relation | RK3-003 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Relation | RK3-004 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-01 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-02 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-03 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-04 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-05 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-06 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-07 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-08 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-09 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-10 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-11 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-12 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-13 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-14 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-15 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-16 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-17 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-18 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-19 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-20 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-21 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-22 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-23 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-24 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-25 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-26 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-27 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-28 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-29 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-30 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G-31 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | GX-046 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | GX-047 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | GX-048 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | GX-049 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | GX-050 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | GX-051 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | GX-053 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | GX-054 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | GX-055 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | GX-056 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | GX-057 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | GX-058 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | GX-059 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | GX-060 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | GX-061 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | GX-062 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | GX-063 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | GX-064 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G2-050 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G2-051 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G2-052 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G2-053 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G2-054 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G2-055 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G2-056 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G2-057 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G2-058 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G2-059 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G2-060 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G2-061 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G2-062 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G2-063 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G2-064 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G2-065 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Generalization | G3-001 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Constraint | C-01 | SELECTED_SUBCLAUSES_ONLY | Exact case identifiers and selected entry joins; no complete real-world identity adjudication. |
| Constraint | C-02 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Constraint | C-03 | SELECTED_SUBCLAUSES_ONLY | Issued serialized payload/provenance/dependency guards; not full InformationContent or every ontology relation. |
| Constraint | C-04 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Constraint | C-05 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Constraint | C-06 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Constraint | C-07 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Constraint | C-08 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Constraint | C-09 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Constraint | C-10 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Constraint | C-11 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Constraint | C-12 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Constraint | C-13 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Constraint | C-14 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Constraint | C-15 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Constraint | C-16 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Constraint | C-17 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Constraint | C-18 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Constraint | C-19 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Constraint | C-20 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Constraint | C-21 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Constraint | C-22 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Constraint | C-23 | DEFERRED_NO_COMPLETE_SQL_MAPPING | Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema. |
| Constraint | C-24 | SELECTED_SUBCLAUSES_ONLY | Static and stored same-entry predecessor lineage; no full chronology semantics. |
| Constraint | C-25 | SELECTED_SUBCLAUSES_ONLY | Supplementary version-owned dependency kind/coherence checks, not native assessment-subject role admission. |
