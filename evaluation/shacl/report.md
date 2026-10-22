# Riskium SHACL execution report — profile 0.1.0

Source commit: `9668e2bc2a3454ad14aae641b914c64d43cb993b`. This is a **scoped explicit-data validation** run, separate from the [HermiT receipt](../hermit/report.md). The [JSON receipt](report.json) retains each raw graph, normalized data graph, exact shapes graph, publication target list, hashes, validation output and expected source-shape oracle.

## Method and policy

The runner uses pySHACL 0.30.1, RDFLib 7.6.0 and OWL-RL package 7.6.2. OWL-RL is not enabled: inference is `none`, no imports are followed, and only the 66 source subclass triples are explicitly appended as class-check support. Each validation checks the shapes with meta-SHACL. The exact top-level source-shape and constraint-component pairs must match the expected set, so an unrelated violation cannot substitute for the intended negative result. The [profile review](profile-review.md) records policy decisions and source paths.

The source conceptual model is unchanged. Four versioned shape graphs separate raw (no managed-content admission), managed (the selected C-06/C-08/C-25 rules), published (plus C-09 for an externally declared publication target list), and task-ready (same scoped rules, with an explicit compatibility gate). This is not a complete raw/managed/task-ready schema. Publication is deliberately not asserted as a new domain class or inferred from a description's mere existence.

For managed/published/task-ready data, identity normalization uses only asserted `owl:sameAs` equivalence, chooses a stable canonical IRI, preserves combined types and links, and symmetrizes explicit `owl:differentFrom`. A conflict is rejected before SHACL. Raw staging keeps the original identity assertions, including conflicts. Different names alone do not supply actor-distinctness evidence. Both raw and normalized graphs are retained. External identity verification and grounding remain independent obligations.

## Results and coverage

- 77 actual SHACL validation runs.
- 78 matching case outcomes, including identity-policy rejection controls.
- 1 BLOCKED case(s), excluded from successful engine executions.
- 0 unexpected outcomes.

Of **359 predeclared SHACL obligations**, **3 PASS, 1 PARTIAL, 355 NOT_RUN**. Scoped PASS coverage is **0.84%**; exercised coverage including partial work is **1.11%**. The unimplemented 254 endpoint rules, 80 catalog-admission rules and other constraint routes remain in the denominator. More cases for four constraints do not increase this obligation count. Neither percentage measures the semantic correctness of the ontology.

| Constraint | Outcome | What was tested | Remaining boundary |
| --- | --- | --- | --- |
| C-06 | PASS, scoped profile | Named mediation participants, local counts/types, normalized identity and explicit difference evidence | Actual identity, mandate grounding and every other endpoint are separate claims. |
| C-08 | PARTIAL | Indicator-only, scale-only, structural dual anchor, no anchor, wrong types, excess count and deleted-rule mutation | No approved unit/scale compatibility schema; dual-anchor task-ready admission remains BLOCKED. |
| C-09 | PASS, scoped profile | Declared published focus, each alternative, multiple targets, absent/wrong target and deleted-minimum mutation | Publication membership is provided by the caller; meaning of multiple targets still needs domain review. |
| C-25 | PASS, scoped profile | All four version kinds, missing/wrong/multiple targets, alias normalization, direct-reference equality for Context/Method/Scale | The catalog has no direct criteria-reference property to compare; no such property was invented. |

## Full case register

| Case | Profile | Expected | Observed | Verdict | Reported source shapes |
| --- | --- | --- | --- | --- | --- |
| `S-C06-DISTINCT` | managed | CONFORMS | CONFORMS | PASS | — |
| `S-C06-SUBTYPE-BEARER` | managed | CONFORMS | CONFORMS | PASS | — |
| `S-C06-WRONG-BEARER-TYPE` | managed | VIOLATES | VIOLATES | PASS | C06Bearer |
| `S-C06-WRONG-AUTHORITY-TYPE` | managed | VIOLATES | VIOLATES | PASS | C06Authority |
| `S-C06-REVERSE-DIFFERENCE` | managed | CONFORMS | CONFORMS | PASS | — |
| `S-C06-UNRESOLVED-NAMES` | managed | VIOLATES | VIOLATES | PASS | C06Distinct |
| `S-C06-SAME-ACTOR` | managed | VIOLATES | VIOLATES | PASS | C06Distinct |
| `S-C06-ALIASED-SAME-ACTOR` | managed | VIOLATES | VIOLATES | PASS | C06Distinct |
| `S-C06-ALIAS-CHAIN` | managed | VIOLATES | VIOLATES | PASS | C06Distinct |
| `S-C06-IDENTITY-CONFLICT` | managed | IDENTITY_CONFLICT | IDENTITY_CONFLICT | PASS | — |
| `S-C06-RAW-IDENTITY-CONFLICT` | raw | CONFORMS | CONFORMS | PASS | — |
| `S-C06-MISSING-BEARER` | managed | VIOLATES | VIOLATES | PASS | C06Bearer |
| `S-C06-MISSING-AUTHORITY` | managed | VIOLATES | VIOLATES | PASS | C06Authority |
| `S-C06-EXCESS-BEARER` | managed | VIOLATES | VIOLATES | PASS | C06Bearer |
| `S-C06-EXCESS-AUTHORITY` | managed | VIOLATES | VIOLATES | PASS | C06Authority |
| `S-C06-INFORMATION-ONLY` | managed | CONFORMS | CONFORMS | PASS | — |
| `S-C06-RAW-INCOMPLETE` | raw | CONFORMS | CONFORMS | PASS | — |
| `S-C06-MANAGED-INCOMPLETE` | managed | VIOLATES | VIOLATES | PASS | C06Authority, C06Bearer |
| `S-C08-INDICATOR-ONLY` | managed | CONFORMS | CONFORMS | PASS | — |
| `S-C08-SCALE-ONLY` | managed | CONFORMS | CONFORMS | PASS | — |
| `S-C08-DUAL-STRUCTURAL` | managed | CONFORMS | CONFORMS | PASS | — |
| `S-C08-NO-ANCHOR` | managed | VIOLATES | VIOLATES | PASS | C08Anchor |
| `S-C08-RAW-NO-ANCHOR` | raw | CONFORMS | CONFORMS | PASS | — |
| `S-C08-WRONG-INDICATOR-TYPE` | managed | VIOLATES | VIOLATES | PASS | C08Indicator |
| `S-C08-WRONG-SCALE-TYPE` | managed | VIOLATES | VIOLATES | PASS | C08Scale |
| `S-C08-TWO-INDICATORS` | managed | VIOLATES | VIOLATES | PASS | C08Indicator |
| `S-C08-TWO-SCALES` | managed | VIOLATES | VIOLATES | PASS | C08Scale |
| `S-C08-TASK-DUAL-UNKNOWN` | task-ready | BLOCKED | BLOCKED | BLOCKED | — |
| `S-C08-DELETED-ANCHOR-RULE` | managed | CONFORMS | CONFORMS | PASS | — |
| `S-C09-CASE` | published | CONFORMS | CONFORMS | PASS | — |
| `S-C09-PATTERN` | published | CONFORMS | CONFORMS | PASS | — |
| `S-C09-WRONG-PATTERN-TYPE` | published | VIOLATES | VIOLATES | PASS | C09Pattern |
| `S-C09-SCENARIO` | published | CONFORMS | CONFORMS | PASS | — |
| `S-C09-WRONG-SCENARIO-TYPE` | published | VIOLATES | VIOLATES | PASS | C09Scenario |
| `S-C09-MULTIPLE-TARGETS` | published | CONFORMS | CONFORMS | PASS | — |
| `S-C09-PUBLISHED-NO-TARGET` | published | VIOLATES | VIOLATES | PASS | C09Aboutness |
| `S-C09-ORDINARY-NO-TARGET` | published | CONFORMS | CONFORMS | PASS | — |
| `S-C09-UNTYPED-PUBLISHED` | published | VIOLATES | VIOLATES | PASS | C09PublishedDescription |
| `S-C09-WRONG-TARGET-TYPE` | published | VIOLATES | VIOLATES | PASS | C09Case |
| `S-C09-DELETED-MINIMUM` | published | CONFORMS | CONFORMS | PASS | — |
| `S-C25-Context-VALID` | managed | CONFORMS | CONFORMS | PASS | — |
| `S-C25-Context-UNTYPED-VERSION` | managed | VIOLATES | VIOLATES | PASS | C25ContextLink |
| `S-C25-Context-UNTYPED-SOURCE` | managed | VIOLATES | VIOLATES | PASS | C25Context |
| `S-C25-Context-MISSING-TARGET` | managed | VIOLATES | VIOLATES | PASS | C25ContextLink |
| `S-C25-Context-WRONG-KIND` | managed | VIOLATES | VIOLATES | PASS | C25ContextLink |
| `S-C25-Context-TWO-TARGETS` | managed | VIOLATES | VIOLATES | PASS | C25ContextLink |
| `S-C25-Context-ALIASED-TARGET` | managed | CONFORMS | CONFORMS | PASS | — |
| `S-C25-Context-DIRECT-MATCH` | managed | CONFORMS | CONFORMS | PASS | — |
| `S-C25-Context-DIRECT-MISMATCH` | managed | VIOLATES | VIOLATES | PASS | C25ContextAgreement |
| `S-C25-Context-DIRECT-ALIAS` | managed | CONFORMS | CONFORMS | PASS | — |
| `S-C25-Method-VALID` | managed | CONFORMS | CONFORMS | PASS | — |
| `S-C25-Method-UNTYPED-VERSION` | managed | VIOLATES | VIOLATES | PASS | C25MethodLink |
| `S-C25-Method-UNTYPED-SOURCE` | managed | VIOLATES | VIOLATES | PASS | C25Method |
| `S-C25-Method-MISSING-TARGET` | managed | VIOLATES | VIOLATES | PASS | C25MethodLink |
| `S-C25-Method-WRONG-KIND` | managed | VIOLATES | VIOLATES | PASS | C25MethodLink |
| `S-C25-Method-TWO-TARGETS` | managed | VIOLATES | VIOLATES | PASS | C25MethodLink |
| `S-C25-Method-ALIASED-TARGET` | managed | CONFORMS | CONFORMS | PASS | — |
| `S-C25-Method-DIRECT-MATCH` | managed | CONFORMS | CONFORMS | PASS | — |
| `S-C25-Method-DIRECT-MISMATCH` | managed | VIOLATES | VIOLATES | PASS | C25MethodAgreement |
| `S-C25-Method-DIRECT-ALIAS` | managed | CONFORMS | CONFORMS | PASS | — |
| `S-C25-Scale-VALID` | managed | CONFORMS | CONFORMS | PASS | — |
| `S-C25-Scale-UNTYPED-VERSION` | managed | VIOLATES | VIOLATES | PASS | C25ScaleLink |
| `S-C25-Scale-UNTYPED-SOURCE` | managed | VIOLATES | VIOLATES | PASS | C25Scale |
| `S-C25-Scale-MISSING-TARGET` | managed | VIOLATES | VIOLATES | PASS | C25ScaleLink |
| `S-C25-Scale-WRONG-KIND` | managed | VIOLATES | VIOLATES | PASS | C25ScaleLink |
| `S-C25-Scale-TWO-TARGETS` | managed | VIOLATES | VIOLATES | PASS | C25ScaleLink |
| `S-C25-Scale-ALIASED-TARGET` | managed | CONFORMS | CONFORMS | PASS | — |
| `S-C25-Scale-DIRECT-MATCH` | managed | CONFORMS | CONFORMS | PASS | — |
| `S-C25-Scale-DIRECT-MISMATCH` | managed | VIOLATES | VIOLATES | PASS | C25ScaleAgreement |
| `S-C25-Scale-DIRECT-ALIAS` | managed | CONFORMS | CONFORMS | PASS | — |
| `S-C25-Criteria-VALID` | managed | CONFORMS | CONFORMS | PASS | — |
| `S-C25-Criteria-UNTYPED-VERSION` | managed | VIOLATES | VIOLATES | PASS | C25CriteriaLink |
| `S-C25-Criteria-UNTYPED-SOURCE` | managed | VIOLATES | VIOLATES | PASS | C25Criteria |
| `S-C25-Criteria-MISSING-TARGET` | managed | VIOLATES | VIOLATES | PASS | C25CriteriaLink |
| `S-C25-Criteria-WRONG-KIND` | managed | VIOLATES | VIOLATES | PASS | C25CriteriaLink |
| `S-C25-Criteria-TWO-TARGETS` | managed | VIOLATES | VIOLATES | PASS | C25CriteriaLink |
| `S-C25-Criteria-ALIASED-TARGET` | managed | CONFORMS | CONFORMS | PASS | — |
| `S-INTEGRATION-ALL-FOUR` | published | CONFORMS | CONFORMS | PASS | — |
| `S-INTEGRATION-C09-DEFECT` | published | VIOLATES | VIOLATES | PASS | C09Aboutness |

## Full baseline register

| Obligation | Source | Outcome |
| --- | --- | --- |
| `SHACL-0145` | `R-01:source` | NOT_RUN |
| `SHACL-0146` | `R-01:target` | NOT_RUN |
| `SHACL-0148` | `R-02:source` | NOT_RUN |
| `SHACL-0149` | `R-02:target` | NOT_RUN |
| `SHACL-0151` | `R-03:source` | NOT_RUN |
| `SHACL-0152` | `R-03:target` | NOT_RUN |
| `SHACL-0154` | `R-04:source` | NOT_RUN |
| `SHACL-0155` | `R-04:target` | NOT_RUN |
| `SHACL-0157` | `R-05:source` | NOT_RUN |
| `SHACL-0158` | `R-05:target` | NOT_RUN |
| `SHACL-0160` | `R-06:source` | NOT_RUN |
| `SHACL-0161` | `R-06:target` | NOT_RUN |
| `SHACL-0163` | `R-07:source` | NOT_RUN |
| `SHACL-0164` | `R-07:target` | NOT_RUN |
| `SHACL-0166` | `R-08:source` | NOT_RUN |
| `SHACL-0167` | `R-08:target` | NOT_RUN |
| `SHACL-0169` | `R-09:source` | NOT_RUN |
| `SHACL-0170` | `R-09:target` | NOT_RUN |
| `SHACL-0172` | `R-10:source` | NOT_RUN |
| `SHACL-0173` | `R-10:target` | NOT_RUN |
| `SHACL-0175` | `R-11:source` | NOT_RUN |
| `SHACL-0176` | `R-11:target` | NOT_RUN |
| `SHACL-0178` | `R-12:source` | NOT_RUN |
| `SHACL-0179` | `R-12:target` | NOT_RUN |
| `SHACL-0181` | `R-13:source` | NOT_RUN |
| `SHACL-0182` | `R-13:target` | NOT_RUN |
| `SHACL-0184` | `R-14:source` | NOT_RUN |
| `SHACL-0185` | `R-14:target` | NOT_RUN |
| `SHACL-0187` | `R-15:source` | NOT_RUN |
| `SHACL-0188` | `R-15:target` | NOT_RUN |
| `SHACL-0190` | `R-16:source` | NOT_RUN |
| `SHACL-0191` | `R-16:target` | NOT_RUN |
| `SHACL-0193` | `R-17:source` | NOT_RUN |
| `SHACL-0194` | `R-17:target` | NOT_RUN |
| `SHACL-0196` | `R-18:source` | NOT_RUN |
| `SHACL-0197` | `R-18:target` | NOT_RUN |
| `SHACL-0199` | `R-19:source` | NOT_RUN |
| `SHACL-0200` | `R-19:target` | NOT_RUN |
| `SHACL-0202` | `R-20:source` | NOT_RUN |
| `SHACL-0203` | `R-20:target` | NOT_RUN |
| `SHACL-0205` | `R-21:source` | NOT_RUN |
| `SHACL-0206` | `R-21:target` | NOT_RUN |
| `SHACL-0208` | `R-22:source` | NOT_RUN |
| `SHACL-0209` | `R-22:target` | NOT_RUN |
| `SHACL-0211` | `R-23:source` | NOT_RUN |
| `SHACL-0212` | `R-23:target` | NOT_RUN |
| `SHACL-0214` | `R-24:source` | NOT_RUN |
| `SHACL-0215` | `R-24:target` | NOT_RUN |
| `SHACL-0217` | `R-25:source` | NOT_RUN |
| `SHACL-0218` | `R-25:target` | NOT_RUN |
| `SHACL-0220` | `R-26:source` | NOT_RUN |
| `SHACL-0221` | `R-26:target` | NOT_RUN |
| `SHACL-0223` | `R-27:source` | NOT_RUN |
| `SHACL-0224` | `R-27:target` | NOT_RUN |
| `SHACL-0226` | `R-28:source` | NOT_RUN |
| `SHACL-0227` | `R-28:target` | NOT_RUN |
| `SHACL-0229` | `R-29:source` | NOT_RUN |
| `SHACL-0230` | `R-29:target` | NOT_RUN |
| `SHACL-0232` | `R-30:source` | NOT_RUN |
| `SHACL-0233` | `R-30:target` | NOT_RUN |
| `SHACL-0235` | `R-31:source` | NOT_RUN |
| `SHACL-0236` | `R-31:target` | NOT_RUN |
| `SHACL-0238` | `R-32:source` | NOT_RUN |
| `SHACL-0239` | `R-32:target` | NOT_RUN |
| `SHACL-0241` | `R-33:source` | NOT_RUN |
| `SHACL-0242` | `R-33:target` | NOT_RUN |
| `SHACL-0244` | `R-34:source` | NOT_RUN |
| `SHACL-0245` | `R-34:target` | NOT_RUN |
| `SHACL-0247` | `R-35:source` | NOT_RUN |
| `SHACL-0248` | `R-35:target` | NOT_RUN |
| `SHACL-0250` | `R-36:source` | NOT_RUN |
| `SHACL-0251` | `R-36:target` | NOT_RUN |
| `SHACL-0253` | `R-37:source` | NOT_RUN |
| `SHACL-0254` | `R-37:target` | NOT_RUN |
| `SHACL-0256` | `R-38:source` | NOT_RUN |
| `SHACL-0257` | `R-38:target` | NOT_RUN |
| `SHACL-0259` | `R-39:source` | NOT_RUN |
| `SHACL-0260` | `R-39:target` | NOT_RUN |
| `SHACL-0262` | `R-40:source` | NOT_RUN |
| `SHACL-0263` | `R-40:target` | NOT_RUN |
| `SHACL-0265` | `R-41:source` | NOT_RUN |
| `SHACL-0266` | `R-41:target` | NOT_RUN |
| `SHACL-0268` | `R-42:source` | NOT_RUN |
| `SHACL-0269` | `R-42:target` | NOT_RUN |
| `SHACL-0271` | `R-43:source` | NOT_RUN |
| `SHACL-0272` | `R-43:target` | NOT_RUN |
| `SHACL-0274` | `R-44:source` | NOT_RUN |
| `SHACL-0275` | `R-44:target` | NOT_RUN |
| `SHACL-0277` | `R-45:source` | NOT_RUN |
| `SHACL-0278` | `R-45:target` | NOT_RUN |
| `SHACL-0280` | `R-46:source` | NOT_RUN |
| `SHACL-0281` | `R-46:target` | NOT_RUN |
| `SHACL-0283` | `R-47:source` | NOT_RUN |
| `SHACL-0284` | `R-47:target` | NOT_RUN |
| `SHACL-0286` | `R-48:source` | NOT_RUN |
| `SHACL-0287` | `R-48:target` | NOT_RUN |
| `SHACL-0289` | `R-49:source` | NOT_RUN |
| `SHACL-0290` | `R-49:target` | NOT_RUN |
| `SHACL-0292` | `R-50:source` | NOT_RUN |
| `SHACL-0293` | `R-50:target` | NOT_RUN |
| `SHACL-0295` | `R-51:source` | NOT_RUN |
| `SHACL-0296` | `R-51:target` | NOT_RUN |
| `SHACL-0298` | `R-52:source` | NOT_RUN |
| `SHACL-0299` | `R-52:target` | NOT_RUN |
| `SHACL-0301` | `R-53:source` | NOT_RUN |
| `SHACL-0302` | `R-53:target` | NOT_RUN |
| `SHACL-0304` | `R-54:source` | NOT_RUN |
| `SHACL-0305` | `R-54:target` | NOT_RUN |
| `SHACL-0307` | `R-55:source` | NOT_RUN |
| `SHACL-0308` | `R-55:target` | NOT_RUN |
| `SHACL-0310` | `R-56:source` | NOT_RUN |
| `SHACL-0311` | `R-56:target` | NOT_RUN |
| `SHACL-0313` | `R-57:source` | NOT_RUN |
| `SHACL-0314` | `R-57:target` | NOT_RUN |
| `SHACL-0316` | `R-58:source` | NOT_RUN |
| `SHACL-0317` | `R-58:target` | NOT_RUN |
| `SHACL-0319` | `R-59:source` | NOT_RUN |
| `SHACL-0320` | `R-59:target` | NOT_RUN |
| `SHACL-0322` | `R-60:source` | NOT_RUN |
| `SHACL-0323` | `R-60:target` | NOT_RUN |
| `SHACL-0325` | `R-61:source` | NOT_RUN |
| `SHACL-0326` | `R-61:target` | NOT_RUN |
| `SHACL-0328` | `R-62:source` | NOT_RUN |
| `SHACL-0329` | `R-62:target` | NOT_RUN |
| `SHACL-0331` | `R-63:source` | NOT_RUN |
| `SHACL-0332` | `R-63:target` | NOT_RUN |
| `SHACL-0334` | `R-64:source` | NOT_RUN |
| `SHACL-0335` | `R-64:target` | NOT_RUN |
| `SHACL-0337` | `R-65:source` | NOT_RUN |
| `SHACL-0338` | `R-65:target` | NOT_RUN |
| `SHACL-0340` | `R-68:source` | NOT_RUN |
| `SHACL-0341` | `R-68:target` | NOT_RUN |
| `SHACL-0343` | `R-69:source` | NOT_RUN |
| `SHACL-0344` | `R-69:target` | NOT_RUN |
| `SHACL-0346` | `R-70:source` | NOT_RUN |
| `SHACL-0347` | `R-70:target` | NOT_RUN |
| `SHACL-0349` | `R-71:source` | NOT_RUN |
| `SHACL-0350` | `R-71:target` | NOT_RUN |
| `SHACL-0352` | `R-72:source` | NOT_RUN |
| `SHACL-0353` | `R-72:target` | NOT_RUN |
| `SHACL-0355` | `RX-001:source` | NOT_RUN |
| `SHACL-0356` | `RX-001:target` | NOT_RUN |
| `SHACL-0358` | `RX-002:source` | NOT_RUN |
| `SHACL-0359` | `RX-002:target` | NOT_RUN |
| `SHACL-0361` | `RX-003:source` | NOT_RUN |
| `SHACL-0362` | `RX-003:target` | NOT_RUN |
| `SHACL-0364` | `RX-004:source` | NOT_RUN |
| `SHACL-0365` | `RX-004:target` | NOT_RUN |
| `SHACL-0367` | `RX-006:source` | NOT_RUN |
| `SHACL-0368` | `RX-006:target` | NOT_RUN |
| `SHACL-0370` | `RX-007:source` | NOT_RUN |
| `SHACL-0371` | `RX-007:target` | NOT_RUN |
| `SHACL-0373` | `RX-008:source` | NOT_RUN |
| `SHACL-0374` | `RX-008:target` | NOT_RUN |
| `SHACL-0376` | `RX-009:source` | NOT_RUN |
| `SHACL-0377` | `RX-009:target` | NOT_RUN |
| `SHACL-0379` | `RX-011:source` | NOT_RUN |
| `SHACL-0380` | `RX-011:target` | NOT_RUN |
| `SHACL-0382` | `RX-012:source` | NOT_RUN |
| `SHACL-0383` | `RX-012:target` | NOT_RUN |
| `SHACL-0385` | `RX-013:source` | NOT_RUN |
| `SHACL-0386` | `RX-013:target` | NOT_RUN |
| `SHACL-0388` | `RX-014:source` | NOT_RUN |
| `SHACL-0389` | `RX-014:target` | NOT_RUN |
| `SHACL-0391` | `RX-015:source` | NOT_RUN |
| `SHACL-0392` | `RX-015:target` | NOT_RUN |
| `SHACL-0394` | `RX-016:source` | NOT_RUN |
| `SHACL-0395` | `RX-016:target` | NOT_RUN |
| `SHACL-0397` | `RX-017:source` | NOT_RUN |
| `SHACL-0398` | `RX-017:target` | NOT_RUN |
| `SHACL-0400` | `RX-018:source` | NOT_RUN |
| `SHACL-0401` | `RX-018:target` | NOT_RUN |
| `SHACL-0403` | `RX-019:source` | NOT_RUN |
| `SHACL-0404` | `RX-019:target` | NOT_RUN |
| `SHACL-0406` | `RX-021:source` | NOT_RUN |
| `SHACL-0407` | `RX-021:target` | NOT_RUN |
| `SHACL-0409` | `RX-022:source` | NOT_RUN |
| `SHACL-0410` | `RX-022:target` | NOT_RUN |
| `SHACL-0412` | `RX-023:source` | NOT_RUN |
| `SHACL-0413` | `RX-023:target` | NOT_RUN |
| `SHACL-0415` | `RX-024:source` | NOT_RUN |
| `SHACL-0416` | `RX-024:target` | NOT_RUN |
| `SHACL-0418` | `RX-025:source` | NOT_RUN |
| `SHACL-0419` | `RX-025:target` | NOT_RUN |
| `SHACL-0421` | `RX-026:source` | NOT_RUN |
| `SHACL-0422` | `RX-026:target` | NOT_RUN |
| `SHACL-0424` | `RX-027:source` | NOT_RUN |
| `SHACL-0425` | `RX-027:target` | NOT_RUN |
| `SHACL-0427` | `RX-028:source` | NOT_RUN |
| `SHACL-0428` | `RX-028:target` | NOT_RUN |
| `SHACL-0430` | `RX-029:source` | NOT_RUN |
| `SHACL-0431` | `RX-029:target` | NOT_RUN |
| `SHACL-0433` | `RX-030:source` | NOT_RUN |
| `SHACL-0434` | `RX-030:target` | NOT_RUN |
| `SHACL-0436` | `RX-031:source` | NOT_RUN |
| `SHACL-0437` | `RX-031:target` | NOT_RUN |
| `SHACL-0439` | `RX-032:source` | NOT_RUN |
| `SHACL-0440` | `RX-032:target` | NOT_RUN |
| `SHACL-0442` | `RK2-001:source` | NOT_RUN |
| `SHACL-0443` | `RK2-001:target` | NOT_RUN |
| `SHACL-0445` | `RK2-002:source` | NOT_RUN |
| `SHACL-0446` | `RK2-002:target` | NOT_RUN |
| `SHACL-0448` | `RK2-003:source` | NOT_RUN |
| `SHACL-0449` | `RK2-003:target` | NOT_RUN |
| `SHACL-0451` | `RK2-004:source` | NOT_RUN |
| `SHACL-0452` | `RK2-004:target` | NOT_RUN |
| `SHACL-0454` | `RK2-005:source` | NOT_RUN |
| `SHACL-0455` | `RK2-005:target` | NOT_RUN |
| `SHACL-0457` | `RK2-007:source` | NOT_RUN |
| `SHACL-0458` | `RK2-007:target` | NOT_RUN |
| `SHACL-0460` | `RK2-008:source` | NOT_RUN |
| `SHACL-0461` | `RK2-008:target` | NOT_RUN |
| `SHACL-0463` | `RK2-009:source` | NOT_RUN |
| `SHACL-0464` | `RK2-009:target` | NOT_RUN |
| `SHACL-0466` | `RK2-010:source` | NOT_RUN |
| `SHACL-0467` | `RK2-010:target` | NOT_RUN |
| `SHACL-0469` | `RK2-011:source` | NOT_RUN |
| `SHACL-0470` | `RK2-011:target` | NOT_RUN |
| `SHACL-0472` | `RK2-012:source` | NOT_RUN |
| `SHACL-0473` | `RK2-012:target` | NOT_RUN |
| `SHACL-0475` | `RK2-013:source` | NOT_RUN |
| `SHACL-0476` | `RK2-013:target` | NOT_RUN |
| `SHACL-0478` | `RK2-014:source` | NOT_RUN |
| `SHACL-0479` | `RK2-014:target` | NOT_RUN |
| `SHACL-0481` | `RK2-015:source` | NOT_RUN |
| `SHACL-0482` | `RK2-015:target` | NOT_RUN |
| `SHACL-0484` | `RK2-016:source` | NOT_RUN |
| `SHACL-0485` | `RK2-016:target` | NOT_RUN |
| `SHACL-0487` | `RK2-017:source` | NOT_RUN |
| `SHACL-0488` | `RK2-017:target` | NOT_RUN |
| `SHACL-0490` | `RK2-018:source` | NOT_RUN |
| `SHACL-0491` | `RK2-018:target` | NOT_RUN |
| `SHACL-0493` | `RK2-019:source` | NOT_RUN |
| `SHACL-0494` | `RK2-019:target` | NOT_RUN |
| `SHACL-0496` | `RK2-020:source` | NOT_RUN |
| `SHACL-0497` | `RK2-020:target` | NOT_RUN |
| `SHACL-0499` | `RK2-021:source` | NOT_RUN |
| `SHACL-0500` | `RK2-021:target` | NOT_RUN |
| `SHACL-0502` | `RK2-022:source` | NOT_RUN |
| `SHACL-0503` | `RK2-022:target` | NOT_RUN |
| `SHACL-0505` | `RK2-023:source` | NOT_RUN |
| `SHACL-0506` | `RK2-023:target` | NOT_RUN |
| `SHACL-0508` | `RK2-024:source` | NOT_RUN |
| `SHACL-0509` | `RK2-024:target` | NOT_RUN |
| `SHACL-0511` | `RK2-025:source` | NOT_RUN |
| `SHACL-0512` | `RK2-025:target` | NOT_RUN |
| `SHACL-0514` | `RK2-026:source` | NOT_RUN |
| `SHACL-0515` | `RK2-026:target` | NOT_RUN |
| `SHACL-0517` | `RK3-001:source` | NOT_RUN |
| `SHACL-0518` | `RK3-001:target` | NOT_RUN |
| `SHACL-0520` | `RK3-003:source` | NOT_RUN |
| `SHACL-0521` | `RK3-003:target` | NOT_RUN |
| `SHACL-0523` | `RK3-004:source` | NOT_RUN |
| `SHACL-0524` | `RK3-004:target` | NOT_RUN |
| `SHACL-0525` | `RKM-C001` | NOT_RUN |
| `SHACL-0526` | `RKM-C002` | NOT_RUN |
| `SHACL-0527` | `RKM-C003` | NOT_RUN |
| `SHACL-0528` | `RKM-C004` | NOT_RUN |
| `SHACL-0529` | `RKM-C005` | NOT_RUN |
| `SHACL-0530` | `RKM-C006` | NOT_RUN |
| `SHACL-0531` | `RKM-C007` | NOT_RUN |
| `SHACL-0532` | `RKM-C008` | NOT_RUN |
| `SHACL-0533` | `RKM-C009` | NOT_RUN |
| `SHACL-0534` | `RKM-C010` | NOT_RUN |
| `SHACL-0535` | `RKM-C011` | NOT_RUN |
| `SHACL-0536` | `RKM-C012` | NOT_RUN |
| `SHACL-0537` | `RKM-C013` | NOT_RUN |
| `SHACL-0538` | `RKM-C014` | NOT_RUN |
| `SHACL-0539` | `RKM-C015` | NOT_RUN |
| `SHACL-0540` | `RKM-C016` | NOT_RUN |
| `SHACL-0541` | `RKM-C017` | NOT_RUN |
| `SHACL-0542` | `RKM-C018` | NOT_RUN |
| `SHACL-0543` | `RKM-C019` | NOT_RUN |
| `SHACL-0544` | `RKM-C020` | NOT_RUN |
| `SHACL-0545` | `RKM-C021` | NOT_RUN |
| `SHACL-0546` | `RKM-C022` | NOT_RUN |
| `SHACL-0547` | `RKM-C023` | NOT_RUN |
| `SHACL-0548` | `RKM-C024` | NOT_RUN |
| `SHACL-0549` | `RKM-C025` | NOT_RUN |
| `SHACL-0550` | `RKM-C026` | NOT_RUN |
| `SHACL-0551` | `RKM-C027` | NOT_RUN |
| `SHACL-0552` | `RKM-C028` | NOT_RUN |
| `SHACL-0553` | `RKM-C029` | NOT_RUN |
| `SHACL-0554` | `RKM-C030` | NOT_RUN |
| `SHACL-0555` | `RKM-C031` | NOT_RUN |
| `SHACL-0556` | `RKM-C032` | NOT_RUN |
| `SHACL-0557` | `RKM-C033` | NOT_RUN |
| `SHACL-0558` | `RKM-C034` | NOT_RUN |
| `SHACL-0559` | `RKM-C035` | NOT_RUN |
| `SHACL-0560` | `RKM-C036` | NOT_RUN |
| `SHACL-0561` | `RKM-C037` | NOT_RUN |
| `SHACL-0562` | `RKM-C038` | NOT_RUN |
| `SHACL-0563` | `RKM-C039` | NOT_RUN |
| `SHACL-0564` | `RKM-C040` | NOT_RUN |
| `SHACL-0565` | `RKM-C041` | NOT_RUN |
| `SHACL-0566` | `RKM-C042` | NOT_RUN |
| `SHACL-0567` | `RKM-C043` | NOT_RUN |
| `SHACL-0568` | `RKM-C044` | NOT_RUN |
| `SHACL-0569` | `RKM-C045` | NOT_RUN |
| `SHACL-0570` | `RKM-C046` | NOT_RUN |
| `SHACL-0571` | `RKM-C047` | NOT_RUN |
| `SHACL-0572` | `RKM-C048` | NOT_RUN |
| `SHACL-0573` | `RKM-C049` | NOT_RUN |
| `SHACL-0574` | `RKM-C050` | NOT_RUN |
| `SHACL-0575` | `RKM-C051` | NOT_RUN |
| `SHACL-0576` | `RKM-C052` | NOT_RUN |
| `SHACL-0577` | `RKM-C053` | NOT_RUN |
| `SHACL-0578` | `RKM-C054` | NOT_RUN |
| `SHACL-0579` | `RKM-C055` | NOT_RUN |
| `SHACL-0580` | `RKM-C056` | NOT_RUN |
| `SHACL-0581` | `RKM-C057` | NOT_RUN |
| `SHACL-0582` | `RKM-C058` | NOT_RUN |
| `SHACL-0583` | `RKM-C059` | NOT_RUN |
| `SHACL-0584` | `RKM-C060` | NOT_RUN |
| `SHACL-0585` | `RKM-C061` | NOT_RUN |
| `SHACL-0586` | `RKM-C062` | NOT_RUN |
| `SHACL-0587` | `RKM-C063` | NOT_RUN |
| `SHACL-0588` | `RKM-C064` | NOT_RUN |
| `SHACL-0589` | `RKM-C065` | NOT_RUN |
| `SHACL-0590` | `RKM-C066` | NOT_RUN |
| `SHACL-0591` | `RKM-C067` | NOT_RUN |
| `SHACL-0592` | `RKM-C068` | NOT_RUN |
| `SHACL-0593` | `RKM-C069` | NOT_RUN |
| `SHACL-0594` | `RKM-C070` | NOT_RUN |
| `SHACL-0595` | `RKM-C071` | NOT_RUN |
| `SHACL-0596` | `RKM-C072` | NOT_RUN |
| `SHACL-0597` | `RKM-C073` | NOT_RUN |
| `SHACL-0598` | `RKM-C074` | NOT_RUN |
| `SHACL-0599` | `RKM-X01` | NOT_RUN |
| `SHACL-0600` | `RKM-X02` | NOT_RUN |
| `SHACL-0601` | `RKM-X03` | NOT_RUN |
| `SHACL-0602` | `RKM-X04` | NOT_RUN |
| `SHACL-0603` | `RKM-X05` | NOT_RUN |
| `SHACL-0604` | `RKM-X06` | NOT_RUN |
| `SHACL-0606` | `C-01` | NOT_RUN |
| `SHACL-0608` | `C-02` | NOT_RUN |
| `SHACL-0610` | `C-03` | NOT_RUN |
| `SHACL-0612` | `C-04` | NOT_RUN |
| `SHACL-0614` | `C-05` | NOT_RUN |
| `SHACL-0616` | `C-06` | PASS |
| `SHACL-0618` | `C-07` | NOT_RUN |
| `SHACL-0620` | `C-08` | PARTIAL |
| `SHACL-0622` | `C-09` | PASS |
| `SHACL-0624` | `C-10` | NOT_RUN |
| `SHACL-0626` | `C-11` | NOT_RUN |
| `SHACL-0628` | `C-12` | NOT_RUN |
| `SHACL-0630` | `C-13` | NOT_RUN |
| `SHACL-0632` | `C-14` | NOT_RUN |
| `SHACL-0634` | `C-15` | NOT_RUN |
| `SHACL-0636` | `C-16` | NOT_RUN |
| `SHACL-0638` | `C-17` | NOT_RUN |
| `SHACL-0640` | `C-18` | NOT_RUN |
| `SHACL-0642` | `C-19` | NOT_RUN |
| `SHACL-0644` | `C-20` | NOT_RUN |
| `SHACL-0646` | `C-21` | NOT_RUN |
| `SHACL-0648` | `C-22` | NOT_RUN |
| `SHACL-0650` | `C-23` | NOT_RUN |
| `SHACL-0652` | `C-24` | NOT_RUN |
| `SHACL-0654` | `C-25` | PASS |

## Reproduce and next work

```sh
python3 -m venv .venv-shacl
.venv-shacl/bin/pip install -r tools/requirements-shacl.txt
.venv-shacl/bin/python tools/build_shacl.py
.venv-shacl/bin/python tools/run_shacl.py
```

The JSON contains exact snapshots for this run, including effective targetNode additions and shape mutations. Base profiles are in `ontology/shacl/0.1.0/`. Next implement the 254 ordered endpoint obligations with deliberate inverse-path controls, then catalog admission and remaining constraint routes. Resolve C-08 compatibility through an approved scalar/unit/scale schema before turning its partial outcome into a pass. Requirements, competency questions, independent semantic review, application history and case adequacy retain separate evidence registers.
