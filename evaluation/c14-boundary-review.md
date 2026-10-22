# C-14 boundary reconciliation

The [machine-readable review](c14-boundary-review.json) pins the conceptual source, typed projection, native exchange, OWL export, fixed coverage contract and earlier compressed admission receipt by SHA-256. Reproduce with `.venv-shacl/bin/python tools/review_c14_boundary.py` from the repository root.

| Catalog boundary | Documentary representation in the typed core | Optional external bridges |
| --- | --- | --- |
| `RKM-C007` RiskSource | `RKM-X06` RiskSourceReference | `RX-005`, `RK3-002` |
| `RKM-C010` Consequence | `RKM-C025` ConsequenceStatement | `RX-010`, `RK2-006` |
| `RKM-C045` RiskControl | `RKM-X05` ControlReference | `R-66`, `R-67`, `RX-020` |

All three broad boundaries are catalog concepts and native notes, absent from the 77-class typed projection and OWL class export. Their seven bridges remain native notes and absent from the 127-property typed/OWL exports. Each documentary representation is a typed native and OWL class. The earlier admission receipt independently executed raw preservation, managed exclusion and promotion rejection for each boundary, plus managed catalog acceptance for each documentary representation: **12 previously executed cases**, with matching exact oracles. This review adds **zero** SHACL or HermiT executions.

The constraint is an interpretation boundary: describing a possible source or consequence, or recording a claimed control, does not establish a real-world bearer, outcome, implementation or effectiveness. External resolution/import would need an explicit bridge and separate source, identity and authority review. The fixed `SHACL-0632` and `HERMIT-0631` rows remain **NOT_RUN** as engine-specific C-14 obligations. The earlier three catalog-admission boundary rows retain their scoped PASS; they are not counted again here. Independent semantic acceptance remains open.
