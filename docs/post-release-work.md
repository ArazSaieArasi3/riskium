# Work after the first stable release

The published **v0.3.1** remains the first owner-reviewed bounded research artifact. Its tag, six assets, 371-file source archive, accepted component matrix and earlier prereleases remain immutable. The new work below is development on main after that release; it is not a newly published release or a new owner/independent scientific judgment.

| Workstream | Completed development | Remaining acceptance |
| --- | --- | --- |
| Explicit-data/application integration (#4/#5) | [Shared-graph validator 0.1.0](../implementation/validation/0.1.0/README.md), 31 fixed matching scenarios across seven module families and 29 selected relation pairs; two explicit cross-module scale/version joins | Full native/profile coverage, temporal semantics, multi-value assertion policies, workflow transitions and calculations remain open; historical HermiT/SHACL rows unchanged |
| Relational reconciliation (#12) | [Exhaustive 306-element inventory](../evaluation/relational/coverage/README.md); explicit 10-class/five-predicate support and four partially supported constraints, with every other source element accounted for | Broader schema/assessment-role mapping, private migration, formulas, workloads/concurrency and PostgreSQL remain unexecuted |
| Literature/source evidence (#13) | [Publication-boundary review](../evaluation/sources/publication-review.json) reconciles four previously inspected source notices, machine assistance, unchanged finite populations and binary/source exclusions | Independently prepared broader cases, actual case/meaning accuracy and complete source/correction coverage remain unestablished |
| External/domain boundaries (#16) | [17-record ownership/adoption register](extensions-and-bridges.md), exact three-boundary/seven-bridge coverage, explicit domain proposals and pre-adoption CQ/evidence rules | Boundary-policy objective complete; no extension or alignment is implemented by that completion |
| Independent review (#23) | [Frozen 40-group initial protocol and empty responses](../evaluation/independent-review/README.md), eligibility, source/counterexample packets and rating/adjudication rules | Actual distinct eligible reviewers, independent initial responses and reasoned adjudication |

The [development component overlay](../releases/development-components.json) independently versions five supplements as 0.1.0, compatible with model 0.3.1. It pins exact hashes and the unchanged accepted matrix. Model 0.3.1, ORSD 0.4.3, article 7.0.8, public SQL 0.1.0 and all original MUST/SHOULD priorities remain unchanged. No article edit is needed to claim these as post-release engineering progress; a future paper claim about the additions needs its own editorial revision.

The integration oracle graph and 31 exact findings/decisions were committed before the validator at `6243411579029120459cdd914a17b6006c7cdbbf`. The full receipt stores raw/effective/shapes/result snapshots, expected findings, input hashes, runtime and actual engine outputs. It separates 21 real SHACL runs, nine preflight rejections, one raw preservation case and four deliberately weakened-rule controls included within the 21 runs. A bad graph accepted by a deliberately deleted rule demonstrates sensitivity, not domain acceptance.

The [post-release workflow](../.github/workflows/post-release-validation.yml) replays the integration receipt, checks the source/ownership/protocol/mapping and component bindings, tests trust boundaries, and freshly replays the unchanged 67-case SQL and 35/59-case source suites. The ordinary candidate workflow also runs all software regressions. These commands do not re-inspect the original PDFs, perform new HermiT execution, adjudicate independent judgments or publish a new release.

```sh
python tools/run_integrated_validation.py --check
python tools/check_research_backlog.py --check
python -m unittest discover -s tests -q
```

Next implement a small, explicitly versioned relational assessment/result slice with native context/method/scale-version joins and source-preserving expected query/migration outcomes. Add missing time/workflow/calculation rules only under a declared application policy with independently fixed expected cases; a source-preserving reported value is never relabeled a computed value. Obtain real independent judgments under #23 when available. A later corrective/enhancement release uses a new immutable tag and a reviewed component set; there is no need to wait for every broad research issue to finish.
