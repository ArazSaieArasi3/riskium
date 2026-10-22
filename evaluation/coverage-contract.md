# Validation coverage contract

This contract defines what the formal evaluation must cover and how its results will be accepted. It is the planning baseline. The subsequent [HermiT execution report](hermit/report.md) and first [scoped SHACL report](shacl/report.md) record actual runs against this baseline; their outstanding rows remain visible.

The [machine-readable contract](coverage-contract.json) assigns a planned route to all 25 interpretation constraints. The [row review](coverage-review.json) binds each baseline obligation to its exact source element, source-file digest and expected fixture behavior. Neither file is an execution report from a formal engine.

## The baseline and its limits

| Coverage family | Baseline obligations | What each row establishes at this stage |
| --- | ---: | --- |
| Typed-class satisfiability | 77 | The class to test and the expected satisfiability probe |
| Declared generalizations | 66 | The specific/general pair and required entailment |
| Typed associations | 127 | Endpoint identities, semantic reading and mapping review obligation |
| Managed endpoint cardinalities | 254 | Focus class, path direction, bounds and valid or invalid counts |
| Catalog admission | 80 | Typed admission or explicit exclusion of an optional boundary |
| Constraint routing | 50 | One OWL-related and one SHACL-related disposition for each of 25 constraints |
| Requirement acceptance | 12 | The current acceptance criterion and prohibited behavior |
| Competency questions | 8 | The expected answer contract, rejection and required population |
| **Baseline total** | **674** | **Allocated obligations at contract review; execution status is reported separately** |

An obligation can require several fixtures. Conversely, an endpoint with multiplicity `0..*` has no invalid non-negative count: neither a below-minimum nor an above-maximum count test applies. That exclusion needs a reason; it is not a successful negative test.

Ten supplementary families cover imports and the foundational anchor; generalization sets, identity and role dependence; seven optional bridges; eight scope requirements; cross-domain integration; datatypes and units; unknown and conflicting content; temporal history; duplicates and blank nodes; and mutation plus clean reruns. They remain separate from the 674-row baseline. A fixed count cannot establish completeness.

## What the engines may establish

HermiT tests must use a reviewed OWL mapping with pinned imports. A missing explicit value is not automatically a contradiction, and two names are not automatically two different individuals. A non-entailment result must be supported by a reasoner test against the negated conclusion or an independently checked countermodel. It does not mean that the conclusion is false in every interpretation.

SHACL tests must name the data graph, shapes graph, profile, focus population and inference policy. Source-end multiplicity counts sources for each target and uses an inverse path. Target-end multiplicity counts targets for each source and uses the direct path. Negative fixtures must trigger the intended constraint rather than pass because a different defect was detected.

The contract uses the [OWL 2 Primer, 11 December 2012](https://www.w3.org/TR/2012/REC-owl2-primer-20121211/) and the [SHACL Recommendation, 20 July 2017](https://www.w3.org/TR/2017/REC-shacl-20170720/) as its technical basis. A later draft is not adopted implicitly.

## Constraints that need more than an engine

Several constraints combine graph structure with meaning or application behavior. The routing register retains these obligations explicitly. In particular:

- An issued version's immutability needs a history and transaction test, beyond checking a static graph.
- Evidence adequacy, actual occurrence and responsibility grounding need source and semantic review.
- Computed scores require a reproducible calculation with justified inputs.
- Mandate identity needs grounding, scope and validity; equal participants alone are not a key.
- Workflow permission and unknown transitions need application-level behavior tests.

Planning routes alone are not implemented encodings. The later OWL mapping and HermiT receipt identify which routes became executable. Where the scalar vocabulary, external identity policy or task profile is unresolved, implementation remains blocked until the decision is recorded. An engine-specific limitation does not remove the underlying constraint from coverage.

## What every execution must record

Each executed case must identify its obligations, source commit and digests, formal encoding, fixture, expected and observed outcomes, engine and runtime versions, import closure, inference policy, command, exit code, report and limitations. The required fields are listed in the JSON contract.

`PASS` is reserved for a reviewed implemented oracle whose observed result matches the expectation. `FAIL`, `ERROR`, `TIMEOUT`, `BLOCKED` and `NOT_RUN` remain separate outcomes. `NOT_APPLICABLE` requires a reason, a reviewer and replacement evidence when the claim remains in scope. None of these states may be counted as a pass.

Report source allocation, encoding, fixture, execution, requirement, query and independent adequacy coverage separately. The allocation review is complete for the declared baseline. HermiT and SHACL execution reports give their separate fractions and remaining obligations; requirement/CQ execution and independent adequacy retain their separate statuses.

## Reproduce the design review

```sh
python3 tools/review_coverage.py
python3 -m unittest discover -s tests -v
```

The first command verifies that the stored review matches the current sources and contract. After an intentional source or contract revision, review the changes before regenerating with `--write`. Regeneration produces planning evidence, never a formal pass.

The review checker has twelve focused regressions, including lost obligations, reversed endpoint direction, stale source binding, missing constraint routes, changed requirement expectations, excluded-boundary promotion and false pass claims. Other suites exercise native export, OWL mapping and HermiT fixture construction. Their engineering results, executed reasoning and independent adequacy are distinct evidence categories.
