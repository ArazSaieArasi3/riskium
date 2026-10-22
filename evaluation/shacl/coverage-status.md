# SHACL module execution coverage

This is the current source-bound execution ledger for conceptual model 0.3.1. It combines the [conditional profile batch](report.md) and [ordered endpoint batch](endpoints/report.md). The [JSON ledger](coverage-status.json) pins their exact digests and each obligation's case references. Both receipts use the same conceptual source and 359-row coverage contract; no historical pass from another model is imported.

| Measure | Result |
| --- | ---: |
| Baseline obligations | 359 |
| PASS within declared module scope | 257 |
| PARTIAL | 1 |
| NOT_RUN | 101 |
| PASS coverage | 71.59% |
| Exercised including partial | 71.87% |

| Family | PASS | PARTIAL | NOT_RUN |
| --- | ---: | ---: | ---: |
| Admission and class profile | 0 | 0 | 80 |
| Constraint encoding disposition | 3 | 1 | 21 |
| Managed-profile endpoint cardinality | 254 | 0 | 0 |

The endpoint batch executes all 254 ordered ends with isolated cardinality controls and paired-end integration for all 127 typed relations. The earlier conditional profiles retain three scoped passes and C-08's partial result. Their fixture populations differ; this ledger reports obligation coverage, not full-profile acceptance of arbitrary records. The 80 catalog-admission rows and 21 other constraint rows are NOT_RUN. Global integration across relations and conditional profiles still needs separate fixtures.

The next batch implements catalog admission, then remaining constraint routes and full managed-profile integration. Unit/scale compatibility needs an approved schema. Requirement/CQ outcomes, independent semantic judgments and real-world case adequacy are governed by the [semantic assurance plan](../semantic-assurance-plan.md).

Reproduce after running the respective suites:

```sh
python3 tools/summarize_shacl.py
```

## Complete 359-row ledger

| Obligation | Source | Outcome | Evidence |
| --- | --- | --- | --- |
| `SHACL-0145` | `R-01:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0146` | `R-01:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0148` | `R-02:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0149` | `R-02:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0151` | `R-03:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0152` | `R-03:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0154` | `R-04:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0155` | `R-04:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0157` | `R-05:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0158` | `R-05:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0160` | `R-06:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0161` | `R-06:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0163` | `R-07:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0164` | `R-07:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0166` | `R-08:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0167` | `R-08:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0169` | `R-09:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0170` | `R-09:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0172` | `R-10:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0173` | `R-10:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0175` | `R-11:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0176` | `R-11:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0178` | `R-12:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0179` | `R-12:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0181` | `R-13:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0182` | `R-13:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0184` | `R-14:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0185` | `R-14:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0187` | `R-15:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0188` | `R-15:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0190` | `R-16:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0191` | `R-16:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0193` | `R-17:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0194` | `R-17:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0196` | `R-18:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0197` | `R-18:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0199` | `R-19:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0200` | `R-19:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0202` | `R-20:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0203` | `R-20:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0205` | `R-21:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0206` | `R-21:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0208` | `R-22:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0209` | `R-22:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0211` | `R-23:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0212` | `R-23:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0214` | `R-24:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0215` | `R-24:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0217` | `R-25:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0218` | `R-25:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0220` | `R-26:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0221` | `R-26:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0223` | `R-27:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0224` | `R-27:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0226` | `R-28:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0227` | `R-28:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0229` | `R-29:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0230` | `R-29:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0232` | `R-30:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0233` | `R-30:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0235` | `R-31:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0236` | `R-31:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0238` | `R-32:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0239` | `R-32:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0241` | `R-33:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0242` | `R-33:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0244` | `R-34:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0245` | `R-34:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0247` | `R-35:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0248` | `R-35:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0250` | `R-36:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0251` | `R-36:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0253` | `R-37:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0254` | `R-37:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0256` | `R-38:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0257` | `R-38:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0259` | `R-39:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0260` | `R-39:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0262` | `R-40:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0263` | `R-40:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0265` | `R-41:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0266` | `R-41:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0268` | `R-42:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0269` | `R-42:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0271` | `R-43:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0272` | `R-43:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0274` | `R-44:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0275` | `R-44:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0277` | `R-45:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0278` | `R-45:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0280` | `R-46:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0281` | `R-46:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0283` | `R-47:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0284` | `R-47:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0286` | `R-48:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0287` | `R-48:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0289` | `R-49:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0290` | `R-49:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0292` | `R-50:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0293` | `R-50:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0295` | `R-51:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0296` | `R-51:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0298` | `R-52:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0299` | `R-52:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0301` | `R-53:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0302` | `R-53:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0304` | `R-54:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0305` | `R-54:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0307` | `R-55:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0308` | `R-55:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0310` | `R-56:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0311` | `R-56:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0313` | `R-57:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0314` | `R-57:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0316` | `R-58:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0317` | `R-58:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0319` | `R-59:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0320` | `R-59:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0322` | `R-60:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0323` | `R-60:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0325` | `R-61:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0326` | `R-61:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0328` | `R-62:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0329` | `R-62:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0331` | `R-63:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0332` | `R-63:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0334` | `R-64:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0335` | `R-64:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0337` | `R-65:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0338` | `R-65:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0340` | `R-68:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0341` | `R-68:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0343` | `R-69:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0344` | `R-69:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0346` | `R-70:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0347` | `R-70:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0349` | `R-71:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0350` | `R-71:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0352` | `R-72:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0353` | `R-72:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0355` | `RX-001:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0356` | `RX-001:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0358` | `RX-002:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0359` | `RX-002:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0361` | `RX-003:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0362` | `RX-003:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0364` | `RX-004:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0365` | `RX-004:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0367` | `RX-006:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0368` | `RX-006:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0370` | `RX-007:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0371` | `RX-007:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0373` | `RX-008:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0374` | `RX-008:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0376` | `RX-009:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0377` | `RX-009:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0379` | `RX-011:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0380` | `RX-011:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0382` | `RX-012:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0383` | `RX-012:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0385` | `RX-013:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0386` | `RX-013:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0388` | `RX-014:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0389` | `RX-014:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0391` | `RX-015:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0392` | `RX-015:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0394` | `RX-016:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0395` | `RX-016:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0397` | `RX-017:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0398` | `RX-017:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0400` | `RX-018:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0401` | `RX-018:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0403` | `RX-019:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0404` | `RX-019:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0406` | `RX-021:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0407` | `RX-021:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0409` | `RX-022:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0410` | `RX-022:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0412` | `RX-023:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0413` | `RX-023:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0415` | `RX-024:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0416` | `RX-024:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0418` | `RX-025:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0419` | `RX-025:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0421` | `RX-026:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0422` | `RX-026:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0424` | `RX-027:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0425` | `RX-027:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0427` | `RX-028:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0428` | `RX-028:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0430` | `RX-029:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0431` | `RX-029:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0433` | `RX-030:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0434` | `RX-030:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0436` | `RX-031:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0437` | `RX-031:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0439` | `RX-032:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0440` | `RX-032:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0442` | `RK2-001:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0443` | `RK2-001:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0445` | `RK2-002:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0446` | `RK2-002:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0448` | `RK2-003:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0449` | `RK2-003:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0451` | `RK2-004:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0452` | `RK2-004:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0454` | `RK2-005:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0455` | `RK2-005:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0457` | `RK2-007:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0458` | `RK2-007:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0460` | `RK2-008:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0461` | `RK2-008:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0463` | `RK2-009:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0464` | `RK2-009:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0466` | `RK2-010:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0467` | `RK2-010:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0469` | `RK2-011:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0470` | `RK2-011:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0472` | `RK2-012:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0473` | `RK2-012:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0475` | `RK2-013:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0476` | `RK2-013:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0478` | `RK2-014:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0479` | `RK2-014:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0481` | `RK2-015:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0482` | `RK2-015:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0484` | `RK2-016:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0485` | `RK2-016:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0487` | `RK2-017:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0488` | `RK2-017:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0490` | `RK2-018:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0491` | `RK2-018:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0493` | `RK2-019:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0494` | `RK2-019:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0496` | `RK2-020:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0497` | `RK2-020:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0499` | `RK2-021:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0500` | `RK2-021:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0502` | `RK2-022:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0503` | `RK2-022:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0505` | `RK2-023:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0506` | `RK2-023:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0508` | `RK2-024:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0509` | `RK2-024:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0511` | `RK2-025:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0512` | `RK2-025:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0514` | `RK2-026:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0515` | `RK2-026:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0517` | `RK3-001:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0518` | `RK3-001:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0520` | `RK3-003:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0521` | `RK3-003:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0523` | `RK3-004:source` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0524` | `RK3-004:target` | PASS | [endpoint receipt](endpoints/report.md) |
| `SHACL-0525` | `RKM-C001` | NOT_RUN | — |
| `SHACL-0526` | `RKM-C002` | NOT_RUN | — |
| `SHACL-0527` | `RKM-C003` | NOT_RUN | — |
| `SHACL-0528` | `RKM-C004` | NOT_RUN | — |
| `SHACL-0529` | `RKM-C005` | NOT_RUN | — |
| `SHACL-0530` | `RKM-C006` | NOT_RUN | — |
| `SHACL-0531` | `RKM-C007` | NOT_RUN | — |
| `SHACL-0532` | `RKM-C008` | NOT_RUN | — |
| `SHACL-0533` | `RKM-C009` | NOT_RUN | — |
| `SHACL-0534` | `RKM-C010` | NOT_RUN | — |
| `SHACL-0535` | `RKM-C011` | NOT_RUN | — |
| `SHACL-0536` | `RKM-C012` | NOT_RUN | — |
| `SHACL-0537` | `RKM-C013` | NOT_RUN | — |
| `SHACL-0538` | `RKM-C014` | NOT_RUN | — |
| `SHACL-0539` | `RKM-C015` | NOT_RUN | — |
| `SHACL-0540` | `RKM-C016` | NOT_RUN | — |
| `SHACL-0541` | `RKM-C017` | NOT_RUN | — |
| `SHACL-0542` | `RKM-C018` | NOT_RUN | — |
| `SHACL-0543` | `RKM-C019` | NOT_RUN | — |
| `SHACL-0544` | `RKM-C020` | NOT_RUN | — |
| `SHACL-0545` | `RKM-C021` | NOT_RUN | — |
| `SHACL-0546` | `RKM-C022` | NOT_RUN | — |
| `SHACL-0547` | `RKM-C023` | NOT_RUN | — |
| `SHACL-0548` | `RKM-C024` | NOT_RUN | — |
| `SHACL-0549` | `RKM-C025` | NOT_RUN | — |
| `SHACL-0550` | `RKM-C026` | NOT_RUN | — |
| `SHACL-0551` | `RKM-C027` | NOT_RUN | — |
| `SHACL-0552` | `RKM-C028` | NOT_RUN | — |
| `SHACL-0553` | `RKM-C029` | NOT_RUN | — |
| `SHACL-0554` | `RKM-C030` | NOT_RUN | — |
| `SHACL-0555` | `RKM-C031` | NOT_RUN | — |
| `SHACL-0556` | `RKM-C032` | NOT_RUN | — |
| `SHACL-0557` | `RKM-C033` | NOT_RUN | — |
| `SHACL-0558` | `RKM-C034` | NOT_RUN | — |
| `SHACL-0559` | `RKM-C035` | NOT_RUN | — |
| `SHACL-0560` | `RKM-C036` | NOT_RUN | — |
| `SHACL-0561` | `RKM-C037` | NOT_RUN | — |
| `SHACL-0562` | `RKM-C038` | NOT_RUN | — |
| `SHACL-0563` | `RKM-C039` | NOT_RUN | — |
| `SHACL-0564` | `RKM-C040` | NOT_RUN | — |
| `SHACL-0565` | `RKM-C041` | NOT_RUN | — |
| `SHACL-0566` | `RKM-C042` | NOT_RUN | — |
| `SHACL-0567` | `RKM-C043` | NOT_RUN | — |
| `SHACL-0568` | `RKM-C044` | NOT_RUN | — |
| `SHACL-0569` | `RKM-C045` | NOT_RUN | — |
| `SHACL-0570` | `RKM-C046` | NOT_RUN | — |
| `SHACL-0571` | `RKM-C047` | NOT_RUN | — |
| `SHACL-0572` | `RKM-C048` | NOT_RUN | — |
| `SHACL-0573` | `RKM-C049` | NOT_RUN | — |
| `SHACL-0574` | `RKM-C050` | NOT_RUN | — |
| `SHACL-0575` | `RKM-C051` | NOT_RUN | — |
| `SHACL-0576` | `RKM-C052` | NOT_RUN | — |
| `SHACL-0577` | `RKM-C053` | NOT_RUN | — |
| `SHACL-0578` | `RKM-C054` | NOT_RUN | — |
| `SHACL-0579` | `RKM-C055` | NOT_RUN | — |
| `SHACL-0580` | `RKM-C056` | NOT_RUN | — |
| `SHACL-0581` | `RKM-C057` | NOT_RUN | — |
| `SHACL-0582` | `RKM-C058` | NOT_RUN | — |
| `SHACL-0583` | `RKM-C059` | NOT_RUN | — |
| `SHACL-0584` | `RKM-C060` | NOT_RUN | — |
| `SHACL-0585` | `RKM-C061` | NOT_RUN | — |
| `SHACL-0586` | `RKM-C062` | NOT_RUN | — |
| `SHACL-0587` | `RKM-C063` | NOT_RUN | — |
| `SHACL-0588` | `RKM-C064` | NOT_RUN | — |
| `SHACL-0589` | `RKM-C065` | NOT_RUN | — |
| `SHACL-0590` | `RKM-C066` | NOT_RUN | — |
| `SHACL-0591` | `RKM-C067` | NOT_RUN | — |
| `SHACL-0592` | `RKM-C068` | NOT_RUN | — |
| `SHACL-0593` | `RKM-C069` | NOT_RUN | — |
| `SHACL-0594` | `RKM-C070` | NOT_RUN | — |
| `SHACL-0595` | `RKM-C071` | NOT_RUN | — |
| `SHACL-0596` | `RKM-C072` | NOT_RUN | — |
| `SHACL-0597` | `RKM-C073` | NOT_RUN | — |
| `SHACL-0598` | `RKM-C074` | NOT_RUN | — |
| `SHACL-0599` | `RKM-X01` | NOT_RUN | — |
| `SHACL-0600` | `RKM-X02` | NOT_RUN | — |
| `SHACL-0601` | `RKM-X03` | NOT_RUN | — |
| `SHACL-0602` | `RKM-X04` | NOT_RUN | — |
| `SHACL-0603` | `RKM-X05` | NOT_RUN | — |
| `SHACL-0604` | `RKM-X06` | NOT_RUN | — |
| `SHACL-0606` | `C-01` | NOT_RUN | — |
| `SHACL-0608` | `C-02` | NOT_RUN | — |
| `SHACL-0610` | `C-03` | NOT_RUN | — |
| `SHACL-0612` | `C-04` | NOT_RUN | — |
| `SHACL-0614` | `C-05` | NOT_RUN | — |
| `SHACL-0616` | `C-06` | PASS | [conditional receipt](report.md) |
| `SHACL-0618` | `C-07` | NOT_RUN | — |
| `SHACL-0620` | `C-08` | PARTIAL | [conditional receipt](report.md) |
| `SHACL-0622` | `C-09` | PASS | [conditional receipt](report.md) |
| `SHACL-0624` | `C-10` | NOT_RUN | — |
| `SHACL-0626` | `C-11` | NOT_RUN | — |
| `SHACL-0628` | `C-12` | NOT_RUN | — |
| `SHACL-0630` | `C-13` | NOT_RUN | — |
| `SHACL-0632` | `C-14` | NOT_RUN | — |
| `SHACL-0634` | `C-15` | NOT_RUN | — |
| `SHACL-0636` | `C-16` | NOT_RUN | — |
| `SHACL-0638` | `C-17` | NOT_RUN | — |
| `SHACL-0640` | `C-18` | NOT_RUN | — |
| `SHACL-0642` | `C-19` | NOT_RUN | — |
| `SHACL-0644` | `C-20` | NOT_RUN | — |
| `SHACL-0646` | `C-21` | NOT_RUN | — |
| `SHACL-0648` | `C-22` | NOT_RUN | — |
| `SHACL-0650` | `C-23` | NOT_RUN | — |
| `SHACL-0652` | `C-24` | NOT_RUN | — |
| `SHACL-0654` | `C-25` | PASS | [conditional receipt](report.md) |
