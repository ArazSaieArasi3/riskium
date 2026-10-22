# Ordered endpoint SHACL report — module 0.2.0

Source commit `f8aede601232c3afd1068eaa93e336b89eb30ad5`. All **254/254 (100.0%)** declared endpoint obligations passed. There were **1878 actual SHACL runs**, **0 unexpected results** and **0 errors. These are cardinality-coverage results, not an ontology semantic-correctness score.

## Inputs, method and interpretation

The [JSON receipt](report.json) retains every raw/normalized graph, effective shapes graph, result graph, identity map, expected/observed source-shape and component, input hashes, engine/runtime versions and elapsed time. Graph snapshots are content-addressed canonical N-Triples. To reconstruct a validation data graph, union the case's normalized snapshot with the shared taxonomy snapshot. Base shapes are `ontology/shacl/0.2.0/endpoints.ttl`.

The generator reads the reviewed model; an independent predeclared 254-row contract supplies fixture bounds, focus classes and expected path direction. The two representations are checked for agreement before execution. A **source-end** label counts sources per target through an inverse path; a **target-end** label counts targets per source through a direct path. Counts include all distinct RDF value nodes on that path after asserted sameAs normalization. Filler type admission is a separate obligation and cannot hide an excessive count.

Local controls activate exactly one endpoint for an explicit focus node, then test valid counts and every applicable below/above-bound case. Every applicable bound is relaxed in a mutation: the previously rejected graph must become conforming. Every one of 254 paths has a supplementary hasValue witness and a reversed-path mutation. Both directions have one node, so cardinality alone cannot mask the reversal; the reversed path must fail specifically for the missing witness. These hasValue constraints are controls in fixture snapshots, not added domain rules. Unbounded or zero-minimum exclusions are retained below and never counted as negative-test passes.

Each of 127 relations also runs with both original targetClass populations and both endpoint shapes together, including valid, missing-link and applicable excessive-count cases. This establishes paired integration within the endpoint module. It does not yet establish full-profile admission across all relations plus the conditional 0.1.0 shapes. The original [conditional-profile receipt](../report.md) remains separately inspectable.

SHACL inference is `none`, no imports are followed, only the 66 source subclass triples are explicitly supplied, and each case runs meta-SHACL. The result must match the exact source-shape/component/focus-node set, including each focus in paired integration. All finite upper bounds also receive alias-normalization and one/two blank-node boundary probes.

## Fixture families

| Family | Passed / total |
| --- | ---: |
| Blank-node boundary | 130/130 |
| Bound mutation | 133/133 |
| Identity boundary | 65/65 |
| Invalid cardinality | 133/133 |
| Paired-end integration | 257/257 |
| Path mutation | 254/254 |
| Path witness | 254/254 |
| Valid cardinality | 652/652 |

## All 254 endpoint obligations

| Obligation | Source | Outcome | Cases | Bounds | Excluded negative cases and reasons |
| --- | --- | --- | ---: | --- | --- |
| `SHACL-0145` | `R-01:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0146` | `R-01:target` | PASS | 13 | 1..1 | — |
| `SHACL-0148` | `R-02:source` | PASS | 13 | 1..1 | — |
| `SHACL-0149` | `R-02:target` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0151` | `R-03:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0152` | `R-03:target` | PASS | 13 | 1..1 | — |
| `SHACL-0154` | `R-04:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0155` | `R-04:target` | PASS | 13 | 1..1 | — |
| `SHACL-0157` | `R-05:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0158` | `R-05:target` | PASS | 13 | 1..1 | — |
| `SHACL-0160` | `R-06:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0161` | `R-06:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0163` | `R-07:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0164` | `R-07:target` | PASS | 13 | 1..1 | — |
| `SHACL-0166` | `R-08:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0167` | `R-08:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0169` | `R-09:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0170` | `R-09:target` | PASS | 13 | 1..1 | — |
| `SHACL-0172` | `R-10:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0173` | `R-10:target` | PASS | 13 | 1..1 | — |
| `SHACL-0175` | `R-11:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0176` | `R-11:target` | PASS | 13 | 1..1 | — |
| `SHACL-0178` | `R-12:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0179` | `R-12:target` | PASS | 13 | 1..1 | — |
| `SHACL-0181` | `R-13:source` | PASS | 13 | 1..1 | — |
| `SHACL-0182` | `R-13:target` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0184` | `R-14:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0185` | `R-14:target` | PASS | 11 | 0..1 | below_minimum: Zero is allowed; a negative node count cannot be constructed. |
| `SHACL-0187` | `R-15:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0188` | `R-15:target` | PASS | 11 | 0..1 | below_minimum: Zero is allowed; a negative node count cannot be constructed. |
| `SHACL-0190` | `R-16:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0191` | `R-16:target` | PASS | 13 | 1..1 | — |
| `SHACL-0193` | `R-17:source` | PASS | 13 | 1..1 | — |
| `SHACL-0194` | `R-17:target` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0196` | `R-18:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0197` | `R-18:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0199` | `R-19:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0200` | `R-19:target` | PASS | 13 | 1..1 | — |
| `SHACL-0202` | `R-20:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0203` | `R-20:target` | PASS | 13 | 1..1 | — |
| `SHACL-0205` | `R-21:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0206` | `R-21:target` | PASS | 9 | 1..* | above_maximum: The upper bound is unbounded. |
| `SHACL-0208` | `R-22:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0209` | `R-22:target` | PASS | 13 | 1..1 | — |
| `SHACL-0211` | `R-23:source` | PASS | 13 | 1..1 | — |
| `SHACL-0212` | `R-23:target` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0214` | `R-24:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0215` | `R-24:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0217` | `R-25:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0218` | `R-25:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0220` | `R-26:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0221` | `R-26:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0223` | `R-27:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0224` | `R-27:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0226` | `R-28:source` | PASS | 9 | 1..* | above_maximum: The upper bound is unbounded. |
| `SHACL-0227` | `R-28:target` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0229` | `R-29:source` | PASS | 9 | 1..* | above_maximum: The upper bound is unbounded. |
| `SHACL-0230` | `R-29:target` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0232` | `R-30:source` | PASS | 9 | 1..* | above_maximum: The upper bound is unbounded. |
| `SHACL-0233` | `R-30:target` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0235` | `R-31:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0236` | `R-31:target` | PASS | 11 | 0..1 | below_minimum: Zero is allowed; a negative node count cannot be constructed. |
| `SHACL-0238` | `R-32:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0239` | `R-32:target` | PASS | 11 | 0..1 | below_minimum: Zero is allowed; a negative node count cannot be constructed. |
| `SHACL-0241` | `R-33:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0242` | `R-33:target` | PASS | 13 | 1..1 | — |
| `SHACL-0244` | `R-34:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0245` | `R-34:target` | PASS | 11 | 0..1 | below_minimum: Zero is allowed; a negative node count cannot be constructed. |
| `SHACL-0247` | `R-35:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0248` | `R-35:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0250` | `R-36:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0251` | `R-36:target` | PASS | 9 | 1..* | above_maximum: The upper bound is unbounded. |
| `SHACL-0253` | `R-37:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0254` | `R-37:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0256` | `R-38:source` | PASS | 13 | 1..1 | — |
| `SHACL-0257` | `R-38:target` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0259` | `R-39:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0260` | `R-39:target` | PASS | 13 | 1..1 | — |
| `SHACL-0262` | `R-40:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0263` | `R-40:target` | PASS | 13 | 1..1 | — |
| `SHACL-0265` | `R-41:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0266` | `R-41:target` | PASS | 13 | 1..1 | — |
| `SHACL-0268` | `R-42:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0269` | `R-42:target` | PASS | 13 | 1..1 | — |
| `SHACL-0271` | `R-43:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0272` | `R-43:target` | PASS | 11 | 0..1 | below_minimum: Zero is allowed; a negative node count cannot be constructed. |
| `SHACL-0274` | `R-44:source` | PASS | 9 | 1..* | above_maximum: The upper bound is unbounded. |
| `SHACL-0275` | `R-44:target` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0277` | `R-45:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0278` | `R-45:target` | PASS | 11 | 0..1 | below_minimum: Zero is allowed; a negative node count cannot be constructed. |
| `SHACL-0280` | `R-46:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0281` | `R-46:target` | PASS | 11 | 0..1 | below_minimum: Zero is allowed; a negative node count cannot be constructed. |
| `SHACL-0283` | `R-47:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0284` | `R-47:target` | PASS | 11 | 0..1 | below_minimum: Zero is allowed; a negative node count cannot be constructed. |
| `SHACL-0286` | `R-48:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0287` | `R-48:target` | PASS | 13 | 1..1 | — |
| `SHACL-0289` | `R-49:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0290` | `R-49:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0292` | `R-50:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0293` | `R-50:target` | PASS | 13 | 1..1 | — |
| `SHACL-0295` | `R-51:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0296` | `R-51:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0298` | `R-52:source` | PASS | 9 | 1..* | above_maximum: The upper bound is unbounded. |
| `SHACL-0299` | `R-52:target` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0301` | `R-53:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0302` | `R-53:target` | PASS | 11 | 0..1 | below_minimum: Zero is allowed; a negative node count cannot be constructed. |
| `SHACL-0304` | `R-54:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0305` | `R-54:target` | PASS | 13 | 1..1 | — |
| `SHACL-0307` | `R-55:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0308` | `R-55:target` | PASS | 11 | 0..1 | below_minimum: Zero is allowed; a negative node count cannot be constructed. |
| `SHACL-0310` | `R-56:source` | PASS | 10 | 1..* | above_maximum: The upper bound is unbounded. |
| `SHACL-0311` | `R-56:target` | PASS | 13 | 1..1 | — |
| `SHACL-0313` | `R-57:source` | PASS | 10 | 1..* | above_maximum: The upper bound is unbounded. |
| `SHACL-0314` | `R-57:target` | PASS | 13 | 1..1 | — |
| `SHACL-0316` | `R-58:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0317` | `R-58:target` | PASS | 9 | 1..* | above_maximum: The upper bound is unbounded. |
| `SHACL-0319` | `R-59:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0320` | `R-59:target` | PASS | 13 | 1..1 | — |
| `SHACL-0322` | `R-60:source` | PASS | 9 | 1..* | above_maximum: The upper bound is unbounded. |
| `SHACL-0323` | `R-60:target` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0325` | `R-61:source` | PASS | 9 | 1..* | above_maximum: The upper bound is unbounded. |
| `SHACL-0326` | `R-61:target` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0328` | `R-62:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0329` | `R-62:target` | PASS | 13 | 1..1 | — |
| `SHACL-0331` | `R-63:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0332` | `R-63:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0334` | `R-64:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0335` | `R-64:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0337` | `R-65:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0338` | `R-65:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0340` | `R-68:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0341` | `R-68:target` | PASS | 9 | 1..* | above_maximum: The upper bound is unbounded. |
| `SHACL-0343` | `R-69:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0344` | `R-69:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0346` | `R-70:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0347` | `R-70:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0349` | `R-71:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0350` | `R-71:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0352` | `R-72:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0353` | `R-72:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0355` | `RX-001:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0356` | `RX-001:target` | PASS | 9 | 1..* | above_maximum: The upper bound is unbounded. |
| `SHACL-0358` | `RX-002:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0359` | `RX-002:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0361` | `RX-003:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0362` | `RX-003:target` | PASS | 9 | 1..* | above_maximum: The upper bound is unbounded. |
| `SHACL-0364` | `RX-004:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0365` | `RX-004:target` | PASS | 13 | 1..1 | — |
| `SHACL-0367` | `RX-006:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0368` | `RX-006:target` | PASS | 13 | 1..1 | — |
| `SHACL-0370` | `RX-007:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0371` | `RX-007:target` | PASS | 9 | 1..* | above_maximum: The upper bound is unbounded. |
| `SHACL-0373` | `RX-008:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0374` | `RX-008:target` | PASS | 13 | 1..1 | — |
| `SHACL-0376` | `RX-009:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0377` | `RX-009:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0379` | `RX-011:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0380` | `RX-011:target` | PASS | 13 | 1..1 | — |
| `SHACL-0382` | `RX-012:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0383` | `RX-012:target` | PASS | 9 | 1..* | above_maximum: The upper bound is unbounded. |
| `SHACL-0385` | `RX-013:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0386` | `RX-013:target` | PASS | 13 | 1..1 | — |
| `SHACL-0388` | `RX-014:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0389` | `RX-014:target` | PASS | 13 | 1..1 | — |
| `SHACL-0391` | `RX-015:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0392` | `RX-015:target` | PASS | 11 | 0..1 | below_minimum: Zero is allowed; a negative node count cannot be constructed. |
| `SHACL-0394` | `RX-016:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0395` | `RX-016:target` | PASS | 11 | 0..1 | below_minimum: Zero is allowed; a negative node count cannot be constructed. |
| `SHACL-0397` | `RX-017:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0398` | `RX-017:target` | PASS | 9 | 1..* | above_maximum: The upper bound is unbounded. |
| `SHACL-0400` | `RX-018:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0401` | `RX-018:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0403` | `RX-019:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0404` | `RX-019:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0406` | `RX-021:source` | PASS | 10 | 1..* | above_maximum: The upper bound is unbounded. |
| `SHACL-0407` | `RX-021:target` | PASS | 13 | 1..1 | — |
| `SHACL-0409` | `RX-022:source` | PASS | 13 | 1..1 | — |
| `SHACL-0410` | `RX-022:target` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0412` | `RX-023:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0413` | `RX-023:target` | PASS | 13 | 1..1 | — |
| `SHACL-0415` | `RX-024:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0416` | `RX-024:target` | PASS | 13 | 1..1 | — |
| `SHACL-0418` | `RX-025:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0419` | `RX-025:target` | PASS | 11 | 0..1 | below_minimum: Zero is allowed; a negative node count cannot be constructed. |
| `SHACL-0421` | `RX-026:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0422` | `RX-026:target` | PASS | 9 | 1..* | above_maximum: The upper bound is unbounded. |
| `SHACL-0424` | `RX-027:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0425` | `RX-027:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0427` | `RX-028:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0428` | `RX-028:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0430` | `RX-029:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0431` | `RX-029:target` | PASS | 13 | 1..1 | — |
| `SHACL-0433` | `RX-030:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0434` | `RX-030:target` | PASS | 13 | 1..1 | — |
| `SHACL-0436` | `RX-031:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0437` | `RX-031:target` | PASS | 13 | 1..1 | — |
| `SHACL-0439` | `RX-032:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0440` | `RX-032:target` | PASS | 11 | 0..1 | below_minimum: Zero is allowed; a negative node count cannot be constructed. |
| `SHACL-0442` | `RK2-001:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0443` | `RK2-001:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0445` | `RK2-002:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0446` | `RK2-002:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0448` | `RK2-003:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0449` | `RK2-003:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0451` | `RK2-004:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0452` | `RK2-004:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0454` | `RK2-005:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0455` | `RK2-005:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0457` | `RK2-007:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0458` | `RK2-007:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0460` | `RK2-008:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0461` | `RK2-008:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0463` | `RK2-009:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0464` | `RK2-009:target` | PASS | 11 | 0..1 | below_minimum: Zero is allowed; a negative node count cannot be constructed. |
| `SHACL-0466` | `RK2-010:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0467` | `RK2-010:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0469` | `RK2-011:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0470` | `RK2-011:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0472` | `RK2-012:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0473` | `RK2-012:target` | PASS | 11 | 0..1 | below_minimum: Zero is allowed; a negative node count cannot be constructed. |
| `SHACL-0475` | `RK2-013:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0476` | `RK2-013:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0478` | `RK2-014:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0479` | `RK2-014:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0481` | `RK2-015:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0482` | `RK2-015:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0484` | `RK2-016:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0485` | `RK2-016:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0487` | `RK2-017:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0488` | `RK2-017:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0490` | `RK2-018:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0491` | `RK2-018:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0493` | `RK2-019:source` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0494` | `RK2-019:target` | PASS | 13 | 1..1 | — |
| `SHACL-0496` | `RK2-020:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0497` | `RK2-020:target` | PASS | 11 | 0..1 | below_minimum: Zero is allowed; a negative node count cannot be constructed. |
| `SHACL-0499` | `RK2-021:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0500` | `RK2-021:target` | PASS | 9 | 1..* | above_maximum: The upper bound is unbounded. |
| `SHACL-0502` | `RK2-022:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0503` | `RK2-022:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0505` | `RK2-023:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0506` | `RK2-023:target` | PASS | 9 | 1..* | above_maximum: The upper bound is unbounded. |
| `SHACL-0508` | `RK2-024:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0509` | `RK2-024:target` | PASS | 9 | 1..* | above_maximum: The upper bound is unbounded. |
| `SHACL-0511` | `RK2-025:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0512` | `RK2-025:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0514` | `RK2-026:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0515` | `RK2-026:target` | PASS | 11 | 0..1 | below_minimum: Zero is allowed; a negative node count cannot be constructed. |
| `SHACL-0517` | `RK3-001:source` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0518` | `RK3-001:target` | PASS | 6 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0520` | `RK3-003:source` | PASS | 7 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |
| `SHACL-0521` | `RK3-003:target` | PASS | 11 | 0..1 | below_minimum: Zero is allowed; a negative node count cannot be constructed. |
| `SHACL-0523` | `RK3-004:source` | PASS | 13 | 1..1 | — |
| `SHACL-0524` | `RK3-004:target` | PASS | 8 | 0..* | below_minimum: Zero is allowed; a negative node count cannot be constructed.; above_maximum: The upper bound is unbounded. |

## All executed cases

| Case | Family | Expected | Observed | Verdict |
| --- | --- | --- | --- | --- |
| `EP-R-01:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-01:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-01:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-01:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-01:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-01:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-01:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-01:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-01:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-01:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-01:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-01:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-01:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-01:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-01:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-02:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-02:source-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-02:source-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-02:source-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-02:source-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-02:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-02:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-02:source-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-02:source-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-02:source-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-02:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-02:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-02:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-02:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-02:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-03:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-03:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-03:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-03:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-03:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-03:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-03:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-03:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-03:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-03:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-03:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-03:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-03:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-03:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-03:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-04:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-04:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-04:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-04:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-04:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-04:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-04:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-04:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-04:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-04:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-04:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-04:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-04:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-04:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-04:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-05:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-05:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-05:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-05:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-05:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-05:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-05:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-05:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-05:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-05:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-05:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-05:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-05:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-05:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-05:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-06:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-06:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-06:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-06:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-06:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-06:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-06:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-06:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-06:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-06:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-07:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-07:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-07:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-07:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-07:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-07:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-07:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-07:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-07:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-07:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-07:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-07:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-07:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-07:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-07:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-08:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-08:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-08:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-08:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-08:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-08:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-08:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-08:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-08:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-08:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-09:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-09:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-09:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-09:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-09:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-09:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-09:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-09:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-09:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-09:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-09:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-09:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-09:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-09:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-09:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-10:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-10:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-10:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-10:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-10:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-10:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-10:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-10:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-10:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-10:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-10:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-10:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-10:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-10:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-10:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-11:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-11:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-11:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-11:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-11:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-11:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-11:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-11:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-11:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-11:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-11:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-11:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-11:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-11:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-11:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-12:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-12:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-12:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-12:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-12:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-12:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-12:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-12:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-12:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-12:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-12:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-12:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-12:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-12:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-12:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-13:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-13:source-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-13:source-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-13:source-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-13:source-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-13:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-13:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-13:source-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-13:source-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-13:source-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-13:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-13:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-13:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-13:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-13:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-14:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-14:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-14:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-14:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-14:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-14:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-14:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-14:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-14:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-14:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-14:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-14:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-14:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-14:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-15:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-15:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-15:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-15:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-15:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-15:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-15:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-15:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-15:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-15:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-15:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-15:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-15:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-15:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-16:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-16:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-16:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-16:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-16:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-16:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-16:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-16:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-16:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-16:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-16:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-16:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-16:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-16:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-16:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-17:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-17:source-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-17:source-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-17:source-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-17:source-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-17:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-17:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-17:source-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-17:source-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-17:source-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-17:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-17:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-17:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-17:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-17:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-18:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-18:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-18:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-18:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-18:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-18:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-18:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-18:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-18:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-18:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-19:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-19:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-19:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-19:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-19:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-19:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-19:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-19:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-19:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-19:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-19:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-19:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-19:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-19:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-19:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-20:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-20:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-20:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-20:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-20:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-20:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-20:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-20:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-20:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-20:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-20:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-20:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-20:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-20:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-20:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-21:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-21:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-21:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-21:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-21:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-21:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-21:target-VALID-2` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-21:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-21:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-21:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-21:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-21:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-22:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-22:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-22:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-22:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-22:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-22:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-22:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-22:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-22:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-22:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-22:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-22:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-22:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-22:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-22:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-23:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-23:source-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-23:source-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-23:source-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-23:source-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-23:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-23:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-23:source-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-23:source-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-23:source-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-23:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-23:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-23:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-23:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-23:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-24:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-24:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-24:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-24:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-24:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-24:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-24:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-24:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-24:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-24:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-25:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-25:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-25:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-25:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-25:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-25:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-25:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-25:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-25:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-25:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-26:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-26:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-26:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-26:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-26:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-26:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-26:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-26:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-26:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-26:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-27:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-27:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-27:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-27:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-27:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-27:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-27:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-27:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-27:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-27:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-28:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-28:source-VALID-2` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-28:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-28:source-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-28:source-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-28:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-28:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-28:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-28:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-28:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-28:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-28:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-29:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-29:source-VALID-2` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-29:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-29:source-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-29:source-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-29:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-29:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-29:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-29:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-29:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-29:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-29:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-30:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-30:source-VALID-2` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-30:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-30:source-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-30:source-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-30:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-30:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-30:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-30:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-30:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-30:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-30:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-31:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-31:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-31:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-31:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-31:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-31:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-31:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-31:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-31:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-31:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-31:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-31:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-31:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-31:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-32:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-32:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-32:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-32:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-32:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-32:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-32:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-32:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-32:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-32:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-32:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-32:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-32:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-32:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-33:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-33:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-33:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-33:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-33:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-33:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-33:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-33:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-33:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-33:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-33:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-33:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-33:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-33:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-33:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-34:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-34:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-34:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-34:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-34:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-34:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-34:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-34:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-34:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-34:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-34:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-34:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-34:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-34:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-35:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-35:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-35:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-35:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-35:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-35:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-35:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-35:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-35:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-35:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-36:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-36:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-36:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-36:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-36:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-36:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-36:target-VALID-2` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-36:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-36:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-36:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-36:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-36:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-37:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-37:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-37:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-37:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-37:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-37:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-37:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-37:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-37:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-37:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-38:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-38:source-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-38:source-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-38:source-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-38:source-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-38:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-38:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-38:source-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-38:source-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-38:source-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-38:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-38:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-38:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-38:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-38:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-39:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-39:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-39:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-39:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-39:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-39:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-39:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-39:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-39:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-39:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-39:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-39:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-39:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-39:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-39:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-40:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-40:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-40:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-40:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-40:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-40:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-40:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-40:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-40:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-40:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-40:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-40:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-40:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-40:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-40:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-41:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-41:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-41:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-41:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-41:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-41:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-41:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-41:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-41:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-41:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-41:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-41:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-41:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-41:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-41:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-42:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-42:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-42:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-42:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-42:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-42:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-42:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-42:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-42:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-42:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-42:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-42:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-42:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-42:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-42:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-43:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-43:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-43:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-43:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-43:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-43:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-43:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-43:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-43:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-43:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-43:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-43:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-43:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-43:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-44:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-44:source-VALID-2` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-44:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-44:source-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-44:source-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-44:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-44:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-44:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-44:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-44:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-44:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-44:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-45:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-45:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-45:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-45:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-45:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-45:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-45:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-45:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-45:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-45:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-45:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-45:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-45:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-45:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-46:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-46:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-46:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-46:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-46:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-46:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-46:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-46:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-46:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-46:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-46:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-46:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-46:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-46:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-47:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-47:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-47:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-47:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-47:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-47:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-47:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-47:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-47:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-47:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-47:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-47:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-47:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-47:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-48:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-48:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-48:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-48:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-48:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-48:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-48:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-48:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-48:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-48:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-48:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-48:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-48:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-48:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-48:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-49:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-49:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-49:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-49:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-49:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-49:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-49:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-49:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-49:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-49:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-50:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-50:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-50:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-50:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-50:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-50:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-50:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-50:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-50:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-50:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-50:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-50:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-50:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-50:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-50:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-51:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-51:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-51:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-51:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-51:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-51:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-51:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-51:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-51:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-51:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-52:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-52:source-VALID-2` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-52:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-52:source-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-52:source-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-52:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-52:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-52:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-52:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-52:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-52:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-52:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-53:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-53:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-53:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-53:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-53:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-53:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-53:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-53:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-53:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-53:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-53:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-53:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-53:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-53:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-54:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-54:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-54:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-54:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-54:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-54:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-54:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-54:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-54:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-54:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-54:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-54:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-54:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-54:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-54:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-55:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-55:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-55:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-55:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-55:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-55:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-55:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-55:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-55:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-55:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-55:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-55:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-55:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-55:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-56:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-56:source-VALID-2` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-56:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-56:source-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-56:source-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-56:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-56:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-56:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-56:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-56:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-56:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-56:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-56:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-56:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-56:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-56:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-56:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-57:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-57:source-VALID-2` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-57:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-57:source-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-57:source-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-57:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-57:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-57:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-57:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-57:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-57:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-57:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-57:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-57:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-57:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-57:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-57:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-58:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-58:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-58:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-58:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-58:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-58:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-58:target-VALID-2` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-58:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-58:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-58:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-58:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-58:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-59:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-59:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-59:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-59:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-59:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-59:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-59:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-59:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-59:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-59:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-59:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-59:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-59:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-59:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-59:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-60:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-60:source-VALID-2` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-60:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-60:source-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-60:source-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-60:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-60:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-60:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-60:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-60:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-60:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-60:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-61:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-61:source-VALID-2` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-61:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-61:source-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-61:source-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-61:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-61:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-61:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-61:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-61:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-61:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-61:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-62:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-62:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-62:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-62:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-62:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-62:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-62:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-62:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-62:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-62:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-62:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-62:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-62:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-62:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-R-62:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-R-63:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-63:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-63:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-63:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-63:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-63:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-63:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-63:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-63:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-63:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-64:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-64:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-64:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-64:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-64:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-64:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-64:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-64:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-64:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-64:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-65:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-65:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-65:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-65:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-65:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-65:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-65:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-65:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-65:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-65:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-68:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-68:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-68:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-68:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-68:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-68:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-68:target-VALID-2` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-68:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-68:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-R-68:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-R-68:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-68:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-69:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-69:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-69:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-69:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-69:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-69:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-69:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-69:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-69:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-69:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-70:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-70:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-70:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-70:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-70:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-70:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-70:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-70:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-70:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-70:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-71:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-71:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-71:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-71:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-71:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-71:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-71:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-71:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-71:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-71:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-72:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-72:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-72:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-72:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-72:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-R-72:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-72:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-72:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-R-72:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-R-72:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-001:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-001:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-001:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-001:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-001:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-001:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-001:target-VALID-2` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-001:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-001:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-001:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-001:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-001:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-002:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-002:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-002:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-002:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-002:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-002:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-002:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-002:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-002:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-002:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-003:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-003:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-003:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-003:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-003:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-003:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-003:target-VALID-2` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-003:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-003:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-003:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-003:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-003:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-004:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-004:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-004:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-004:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-004:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-004:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-004:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-004:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-004:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-004:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-004:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-004:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-004:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-004:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-004:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-RX-006:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-006:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-006:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-006:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-006:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-006:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-006:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-006:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-006:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-006:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-006:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-006:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-006:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-006:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-006:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-RX-007:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-007:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-007:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-007:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-007:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-007:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-007:target-VALID-2` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-007:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-007:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-007:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-007:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-007:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-008:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-008:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-008:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-008:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-008:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-008:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-008:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-008:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-008:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-008:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-008:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-008:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-008:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-008:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-008:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-RX-009:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-009:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-009:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-009:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-009:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-009:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-009:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-009:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-009:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-009:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-011:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-011:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-011:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-011:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-011:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-011:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-011:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-011:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-011:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-011:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-011:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-011:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-011:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-011:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-011:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-RX-012:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-012:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-012:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-012:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-012:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-012:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-012:target-VALID-2` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-012:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-012:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-012:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-012:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-012:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-013:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-013:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-013:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-013:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-013:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-013:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-013:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-013:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-013:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-013:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-013:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-013:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-013:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-013:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-013:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-RX-014:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-014:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-014:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-014:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-014:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-014:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-014:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-014:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-014:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-014:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-014:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-014:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-014:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-014:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-014:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-RX-015:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-015:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-015:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-015:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-015:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-015:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-015:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-015:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-015:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-015:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-015:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-015:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-015:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-015:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-RX-016:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-016:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-016:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-016:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-016:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-016:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-016:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-016:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-016:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-016:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-016:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-016:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-016:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-016:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-RX-017:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-017:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-017:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-017:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-017:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-017:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-017:target-VALID-2` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-017:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-017:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-017:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-017:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-017:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-018:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-018:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-018:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-018:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-018:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-018:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-018:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-018:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-018:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-018:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-019:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-019:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-019:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-019:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-019:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-019:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-019:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-019:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-019:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-019:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-021:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-021:source-VALID-2` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-021:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-021:source-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-021:source-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-021:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-021:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-021:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-021:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-021:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-021:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-021:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-021:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-021:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-021:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-021:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-021:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-RX-022:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-022:source-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-022:source-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-022:source-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-022:source-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-022:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-022:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-022:source-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-022:source-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-022:source-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-RX-022:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-022:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-022:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-022:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-022:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-023:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-023:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-023:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-023:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-023:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-023:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-023:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-023:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-023:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-023:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-023:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-023:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-023:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-023:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-023:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-RX-024:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-024:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-024:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-024:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-024:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-024:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-024:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-024:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-024:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-024:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-024:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-024:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-024:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-024:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-024:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-RX-025:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-025:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-025:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-025:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-025:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-025:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-025:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-025:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-025:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-025:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-025:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-025:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-025:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-025:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-RX-026:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-026:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-026:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-026:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-026:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-026:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-026:target-VALID-2` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-026:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-026:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-026:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-026:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-026:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-027:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-027:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-027:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-027:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-027:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-027:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-027:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-027:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-027:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-027:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-028:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-028:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-028:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-028:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-028:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-028:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-028:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-028:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-028:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-028:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-029:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-029:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-029:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-029:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-029:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-029:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-029:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-029:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-029:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-029:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-029:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-029:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-029:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-029:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-029:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-RX-030:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-030:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-030:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-030:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-030:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-030:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-030:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-030:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-030:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-030:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-030:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-030:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-030:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-030:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-030:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-RX-031:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-031:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-031:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-031:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-031:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-031:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-031:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-031:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-031:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-031:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-031:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-031:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-031:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-031:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-031:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-RX-032:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-032:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-032:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-032:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-032:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-032:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-032:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RX-032:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RX-032:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RX-032:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RX-032:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RX-032:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-032:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-RX-032:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-RK2-001:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-001:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-001:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-001:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-001:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-001:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-001:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-001:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-001:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-001:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-002:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-002:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-002:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-002:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-002:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-002:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-002:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-002:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-002:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-002:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-003:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-003:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-003:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-003:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-003:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-003:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-003:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-003:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-003:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-003:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-004:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-004:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-004:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-004:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-004:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-004:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-004:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-004:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-004:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-004:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-005:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-005:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-005:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-005:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-005:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-005:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-005:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-005:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-005:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-005:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-007:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-007:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-007:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-007:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-007:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-007:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-007:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-007:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-007:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-007:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-008:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-008:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-008:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-008:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-008:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-008:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-008:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-008:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-008:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-008:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-009:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-009:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-009:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-009:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-009:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-009:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-009:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-009:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RK2-009:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RK2-009:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-009:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-009:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-RK2-009:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-RK2-009:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-RK2-010:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-010:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-010:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-010:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-010:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-010:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-010:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-010:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-010:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-010:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-011:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-011:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-011:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-011:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-011:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-011:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-011:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-011:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-011:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-011:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-012:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-012:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-012:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-012:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-012:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-012:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-012:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-012:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RK2-012:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RK2-012:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-012:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-012:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-RK2-012:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-RK2-012:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-RK2-013:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-013:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-013:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-013:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-013:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-013:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-013:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-013:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-013:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-013:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-014:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-014:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-014:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-014:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-014:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-014:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-014:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-014:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-014:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-014:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-015:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-015:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-015:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-015:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-015:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-015:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-015:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-015:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-015:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-015:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-016:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-016:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-016:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-016:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-016:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-016:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-016:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-016:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-016:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-016:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-017:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-017:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-017:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-017:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-017:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-017:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-017:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-017:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-017:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-017:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-018:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-018:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-018:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-018:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-018:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-018:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-018:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-018:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-018:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-018:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-019:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-019:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-019:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-019:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-019:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-019:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-019:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RK2-019:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RK2-019:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RK2-019:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RK2-019:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-019:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-019:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-RK2-019:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-RK2-019:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-RK2-020:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-020:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-020:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-020:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-020:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-020:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-020:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-020:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RK2-020:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RK2-020:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-020:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-020:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-RK2-020:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-RK2-020:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-RK2-021:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-021:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-021:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-021:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-021:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-021:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-021:target-VALID-2` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-021:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-021:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RK2-021:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RK2-021:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-021:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-022:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-022:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-022:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-022:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-022:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-022:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-022:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-022:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-022:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-022:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-023:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-023:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-023:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-023:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-023:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-023:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-023:target-VALID-2` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-023:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-023:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RK2-023:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RK2-023:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-023:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-024:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-024:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-024:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-024:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-024:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-024:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-024:target-VALID-2` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-024:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-024:target-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RK2-024:target-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RK2-024:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-024:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-025:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-025:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-025:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-025:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-025:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-025:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-025:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-025:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-025:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-025:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-026:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-026:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-026:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-026:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-026:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-026:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-026:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK2-026:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RK2-026:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RK2-026:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK2-026:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK2-026:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-RK2-026:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-RK2-026:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-RK3-001:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK3-001:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK3-001:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK3-001:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK3-001:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK3-001:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK3-001:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK3-001:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK3-001:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK3-001:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK3-003:source-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK3-003:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK3-003:source-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK3-003:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK3-003:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK3-003:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK3-003:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK3-003:target-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RK3-003:target-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RK3-003:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK3-003:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK3-003:target-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-RK3-003:target-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-RK3-003:target-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-RK3-004:source-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK3-004:source-BELOW-MIN` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RK3-004:source-RELAXED-MIN` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RK3-004:source-ABOVE-MAX` | Invalid cardinality | VIOLATES | VIOLATES | PASS |
| `EP-RK3-004:source-RELAXED-MAX` | Bound mutation | CONFORMS | CONFORMS | PASS |
| `EP-RK3-004:source-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK3-004:source-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `EP-RK3-004:source-ALIASED-VALUES` | Identity boundary | CONFORMS | CONFORMS | PASS |
| `EP-RK3-004:source-ONE-BLANK` | Blank-node boundary | CONFORMS | CONFORMS | PASS |
| `EP-RK3-004:source-TWO-BLANKS` | Blank-node boundary | VIOLATES | VIOLATES | PASS |
| `EP-RK3-004:target-VALID-0` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK3-004:target-VALID-1` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK3-004:target-VALID-5` | Valid cardinality | CONFORMS | CONFORMS | PASS |
| `EP-RK3-004:target-PATH-WITNESS` | Path witness | CONFORMS | CONFORMS | PASS |
| `EP-RK3-004:target-REVERSED-PATH` | Path mutation | VIOLATES | VIOLATES | PASS |
| `PAIR-R-01-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-01-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-01-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-02-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-02-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-02-EXCESS-source` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-03-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-03-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-03-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-04-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-04-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-04-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-05-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-05-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-05-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-06-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-07-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-07-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-07-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-08-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-09-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-09-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-09-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-10-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-10-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-10-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-11-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-11-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-11-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-12-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-12-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-12-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-13-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-13-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-13-EXCESS-source` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-14-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-14-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-15-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-15-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-16-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-16-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-16-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-17-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-17-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-17-EXCESS-source` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-18-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-19-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-19-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-19-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-20-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-20-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-20-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-21-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-21-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-22-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-22-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-22-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-23-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-23-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-23-EXCESS-source` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-24-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-25-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-26-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-27-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-28-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-28-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-29-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-29-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-30-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-30-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-31-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-31-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-32-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-32-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-33-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-33-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-33-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-34-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-34-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-35-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-36-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-36-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-37-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-38-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-38-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-38-EXCESS-source` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-39-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-39-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-39-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-40-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-40-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-40-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-41-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-41-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-41-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-42-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-42-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-42-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-43-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-43-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-44-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-44-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-45-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-45-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-46-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-46-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-47-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-47-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-48-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-48-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-48-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-49-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-50-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-50-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-50-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-51-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-52-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-52-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-53-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-53-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-54-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-54-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-54-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-55-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-55-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-56-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-56-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-56-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-57-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-57-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-57-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-58-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-58-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-59-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-59-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-59-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-60-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-60-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-61-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-61-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-62-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-62-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-62-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-63-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-64-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-65-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-68-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-68-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-R-69-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-70-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-71-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-R-72-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK2-001-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK2-002-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK2-003-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK2-004-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK2-005-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK2-007-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK2-008-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK2-009-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK2-009-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RK2-010-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK2-011-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK2-012-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK2-012-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RK2-013-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK2-014-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK2-015-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK2-016-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK2-017-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK2-018-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK2-019-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK2-019-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RK2-019-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RK2-020-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK2-020-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RK2-021-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK2-021-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RK2-022-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK2-023-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK2-023-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RK2-024-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK2-024-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RK2-025-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK2-026-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK2-026-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RK3-001-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK3-003-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK3-003-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RK3-004-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RK3-004-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RK3-004-EXCESS-source` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-001-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-001-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-002-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-003-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-003-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-004-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-004-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-004-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-006-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-006-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-006-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-007-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-007-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-008-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-008-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-008-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-009-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-011-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-011-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-011-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-012-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-012-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-013-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-013-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-013-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-014-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-014-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-014-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-015-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-015-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-016-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-016-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-017-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-017-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-018-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-019-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-021-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-021-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-021-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-022-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-022-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-022-EXCESS-source` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-023-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-023-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-023-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-024-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-024-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-024-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-025-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-025-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-026-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-026-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-027-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-028-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-029-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-029-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-029-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-030-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-030-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-030-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-031-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-031-MISSING` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-031-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |
| `PAIR-RX-032-VALID` | Paired-end integration | CONFORMS | CONFORMS | PASS |
| `PAIR-RX-032-EXCESS-target` | Paired-end integration | VIOLATES | VIOLATES | PASS |

## Reproduce and next step

```sh
.venv-shacl/bin/python tools/build_endpoint_shapes.py
.venv-shacl/bin/python tools/run_endpoint_shacl.py
```

Pinned environment setup is in `docs/reproducibility.md`. Next implement the 80 catalog-admission obligations, then remaining constraint routes and full managed-profile integration. C-08 compatibility remains partial; requirement/CQ execution and independent semantic review retain separate evidence.
