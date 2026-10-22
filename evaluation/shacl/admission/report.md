# Catalog metadata admission SHACL report — module 0.3.0

Source commit `de6194955c598c509b38acd1312e2012b7d4cd06`. **80/80** catalog-admission obligations passed within the declared [policy](profile-review.md): 77 managed catalog class profiles and three explicit boundary exclusions. **2012 actual SHACL validations**, 0 unexpected results, 0 errors. These are application metadata/task-inspection results, not complete risk-record or semantic validation.

The [lossless full JSON archive](report.json.gz) and [readable index](report-index.json) retains complete raw, effective data, shapes and result graph snapshots, external focus/class requests, identity maps, exact input/code hashes, runtime versions, expected/observed shape-component-focus sets and individual case outcomes. Use `reconstruct_pair()` to parse the `data_graph` and `shapes_graph` snapshots with a shared blank-node context, preserving cross-graph target identities. Snapshot hashes identify serialized content within this receipt, not canonical RDF graph identities. No source model or OWL axiom is changed. Policy is an author implementation decision, not an independent domain review.

Each of 77 core concepts is exercised with complete managed metadata, the sole supported catalog-inspection task, incomplete raw staging, missing metadata, wrong text/source types, missing candidate type, unsupported/missing task, wrong class declaration, blank identities, aliases and equal-label distinct records. Omitted source/type rule mutations must change rejection to conformance. Source generalizations have subtype and forbidden reverse controls. All 127 relations combine both endpoint shapes with admission envelopes for both participants, including an untyped filler. No result here discharges the remaining 21 constraints or C-08 compatibility.

## Fixture families

| Family | Matched / total |
| --- | ---: |
| Asserted alias normalization | 77/77 |
| Boundary promotion attempt | 3/3 |
| Catalog task complete | 77/77 |
| Endpoint filler type | 127/127 |
| Endpoint plus admission integration | 127/127 |
| Equal labels retain distinct records | 77/77 |
| Explicit candidate type | 77/77 |
| External class request | 77/77 |
| Incomplete raw staging | 77/77 |
| Managed candidate identity | 77/77 |
| Managed complete | 77/77 |
| Managed record identity | 77/77 |
| No reverse inheritance | 66/66 |
| Normalized external focus | 77/77 |
| Omitted-rule mutation | 154/154 |
| Optional boundary rejection | 3/3 |
| Optional boundary staging | 3/3 |
| Required metadata | 308/308 |
| Source locator type | 77/77 |
| Source subtype admission | 66/66 |
| Task input missing | 77/77 |
| Text boundary | 77/77 |
| Text datatype | 77/77 |
| Unsupported readiness | 77/77 |

## All 80 source-bound obligations

| Obligation | Concept | Disposition | Outcome | Cases |
| --- | --- | --- | --- | ---: |
| `SHACL-0525` | `RKM-C001` | MANAGED_CATALOG_METADATA | PASS | 27 |
| `SHACL-0526` | `RKM-C002` | MANAGED_CATALOG_METADATA | PASS | 55 |
| `SHACL-0527` | `RKM-C003` | MANAGED_CATALOG_METADATA | PASS | 33 |
| `SHACL-0528` | `RKM-C004` | MANAGED_CATALOG_METADATA | PASS | 29 |
| `SHACL-0529` | `RKM-C005` | MANAGED_CATALOG_METADATA | PASS | 31 |
| `SHACL-0530` | `RKM-C006` | MANAGED_CATALOG_METADATA | PASS | 25 |
| `SHACL-0531` | `RKM-C007` | OPTIONAL_CORE_EXCLUSION | PASS | 3 |
| `SHACL-0532` | `RKM-C008` | MANAGED_CATALOG_METADATA | PASS | 23 |
| `SHACL-0533` | `RKM-C009` | MANAGED_CATALOG_METADATA | PASS | 25 |
| `SHACL-0534` | `RKM-C010` | OPTIONAL_CORE_EXCLUSION | PASS | 3 |
| `SHACL-0535` | `RKM-C011` | MANAGED_CATALOG_METADATA | PASS | 25 |
| `SHACL-0536` | `RKM-C012` | MANAGED_CATALOG_METADATA | PASS | 23 |
| `SHACL-0537` | `RKM-C013` | MANAGED_CATALOG_METADATA | PASS | 23 |
| `SHACL-0538` | `RKM-C014` | MANAGED_CATALOG_METADATA | PASS | 101 |
| `SHACL-0539` | `RKM-C015` | MANAGED_CATALOG_METADATA | PASS | 37 |
| `SHACL-0540` | `RKM-C016` | MANAGED_CATALOG_METADATA | PASS | 23 |
| `SHACL-0541` | `RKM-C017` | MANAGED_CATALOG_METADATA | PASS | 29 |
| `SHACL-0542` | `RKM-C018` | MANAGED_CATALOG_METADATA | PASS | 25 |
| `SHACL-0543` | `RKM-C019` | MANAGED_CATALOG_METADATA | PASS | 49 |
| `SHACL-0544` | `RKM-C020` | MANAGED_CATALOG_METADATA | PASS | 29 |
| `SHACL-0545` | `RKM-C021` | MANAGED_CATALOG_METADATA | PASS | 25 |
| `SHACL-0546` | `RKM-C022` | MANAGED_CATALOG_METADATA | PASS | 29 |
| `SHACL-0547` | `RKM-C023` | MANAGED_CATALOG_METADATA | PASS | 55 |
| `SHACL-0548` | `RKM-C024` | MANAGED_CATALOG_METADATA | PASS | 35 |
| `SHACL-0549` | `RKM-C025` | MANAGED_CATALOG_METADATA | PASS | 31 |
| `SHACL-0550` | `RKM-C026` | MANAGED_CATALOG_METADATA | PASS | 31 |
| `SHACL-0551` | `RKM-C027` | MANAGED_CATALOG_METADATA | PASS | 25 |
| `SHACL-0552` | `RKM-C028` | MANAGED_CATALOG_METADATA | PASS | 25 |
| `SHACL-0553` | `RKM-C029` | MANAGED_CATALOG_METADATA | PASS | 25 |
| `SHACL-0554` | `RKM-C030` | MANAGED_CATALOG_METADATA | PASS | 25 |
| `SHACL-0555` | `RKM-C031` | MANAGED_CATALOG_METADATA | PASS | 27 |
| `SHACL-0556` | `RKM-C032` | MANAGED_CATALOG_METADATA | PASS | 51 |
| `SHACL-0557` | `RKM-C033` | MANAGED_CATALOG_METADATA | PASS | 27 |
| `SHACL-0558` | `RKM-C034` | MANAGED_CATALOG_METADATA | PASS | 35 |
| `SHACL-0559` | `RKM-C035` | MANAGED_CATALOG_METADATA | PASS | 31 |
| `SHACL-0560` | `RKM-C036` | MANAGED_CATALOG_METADATA | PASS | 33 |
| `SHACL-0561` | `RKM-C037` | MANAGED_CATALOG_METADATA | PASS | 29 |
| `SHACL-0562` | `RKM-C038` | MANAGED_CATALOG_METADATA | PASS | 27 |
| `SHACL-0563` | `RKM-C039` | MANAGED_CATALOG_METADATA | PASS | 29 |
| `SHACL-0564` | `RKM-C040` | MANAGED_CATALOG_METADATA | PASS | 25 |
| `SHACL-0565` | `RKM-C041` | MANAGED_CATALOG_METADATA | PASS | 35 |
| `SHACL-0566` | `RKM-C042` | MANAGED_CATALOG_METADATA | PASS | 25 |
| `SHACL-0567` | `RKM-C043` | MANAGED_CATALOG_METADATA | PASS | 33 |
| `SHACL-0568` | `RKM-C044` | MANAGED_CATALOG_METADATA | PASS | 27 |
| `SHACL-0569` | `RKM-C045` | OPTIONAL_CORE_EXCLUSION | PASS | 3 |
| `SHACL-0570` | `RKM-C046` | MANAGED_CATALOG_METADATA | PASS | 25 |
| `SHACL-0571` | `RKM-C047` | MANAGED_CATALOG_METADATA | PASS | 37 |
| `SHACL-0572` | `RKM-C048` | MANAGED_CATALOG_METADATA | PASS | 27 |
| `SHACL-0573` | `RKM-C049` | MANAGED_CATALOG_METADATA | PASS | 27 |
| `SHACL-0574` | `RKM-C050` | MANAGED_CATALOG_METADATA | PASS | 31 |
| `SHACL-0575` | `RKM-C051` | MANAGED_CATALOG_METADATA | PASS | 35 |
| `SHACL-0576` | `RKM-C052` | MANAGED_CATALOG_METADATA | PASS | 31 |
| `SHACL-0577` | `RKM-C053` | MANAGED_CATALOG_METADATA | PASS | 29 |
| `SHACL-0578` | `RKM-C054` | MANAGED_CATALOG_METADATA | PASS | 29 |
| `SHACL-0579` | `RKM-C055` | MANAGED_CATALOG_METADATA | PASS | 25 |
| `SHACL-0580` | `RKM-C056` | MANAGED_CATALOG_METADATA | PASS | 25 |
| `SHACL-0581` | `RKM-C057` | MANAGED_CATALOG_METADATA | PASS | 25 |
| `SHACL-0582` | `RKM-C058` | MANAGED_CATALOG_METADATA | PASS | 25 |
| `SHACL-0583` | `RKM-C059` | MANAGED_CATALOG_METADATA | PASS | 27 |
| `SHACL-0584` | `RKM-C060` | MANAGED_CATALOG_METADATA | PASS | 25 |
| `SHACL-0585` | `RKM-C061` | MANAGED_CATALOG_METADATA | PASS | 29 |
| `SHACL-0586` | `RKM-C062` | MANAGED_CATALOG_METADATA | PASS | 31 |
| `SHACL-0587` | `RKM-C063` | MANAGED_CATALOG_METADATA | PASS | 27 |
| `SHACL-0588` | `RKM-C064` | MANAGED_CATALOG_METADATA | PASS | 29 |
| `SHACL-0589` | `RKM-C065` | MANAGED_CATALOG_METADATA | PASS | 35 |
| `SHACL-0590` | `RKM-C066` | MANAGED_CATALOG_METADATA | PASS | 25 |
| `SHACL-0591` | `RKM-C067` | MANAGED_CATALOG_METADATA | PASS | 23 |
| `SHACL-0592` | `RKM-C068` | MANAGED_CATALOG_METADATA | PASS | 35 |
| `SHACL-0593` | `RKM-C069` | MANAGED_CATALOG_METADATA | PASS | 27 |
| `SHACL-0594` | `RKM-C070` | MANAGED_CATALOG_METADATA | PASS | 29 |
| `SHACL-0595` | `RKM-C071` | MANAGED_CATALOG_METADATA | PASS | 29 |
| `SHACL-0596` | `RKM-C072` | MANAGED_CATALOG_METADATA | PASS | 29 |
| `SHACL-0597` | `RKM-C073` | MANAGED_CATALOG_METADATA | PASS | 27 |
| `SHACL-0598` | `RKM-C074` | MANAGED_CATALOG_METADATA | PASS | 27 |
| `SHACL-0599` | `RKM-X01` | MANAGED_CATALOG_METADATA | PASS | 65 |
| `SHACL-0600` | `RKM-X02` | MANAGED_CATALOG_METADATA | PASS | 27 |
| `SHACL-0601` | `RKM-X03` | MANAGED_CATALOG_METADATA | PASS | 29 |
| `SHACL-0602` | `RKM-X04` | MANAGED_CATALOG_METADATA | PASS | 31 |
| `SHACL-0603` | `RKM-X05` | MANAGED_CATALOG_METADATA | PASS | 27 |
| `SHACL-0604` | `RKM-X06` | MANAGED_CATALOG_METADATA | PASS | 27 |

## Reproduce

```sh
.venv-shacl/bin/python tools/build_admission_shapes.py
.venv-shacl/bin/python tools/run_admission_shacl.py
.venv-shacl/bin/python tools/package_admission_receipt.py
.venv-shacl/bin/python tools/summarize_shacl.py
```

Continue parent #5 with constraint routes, C-08 compatibility and full-profile integration. Close child #17 only after regression checks and published readback.
