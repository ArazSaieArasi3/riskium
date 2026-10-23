# Small continuous development releases

The first development prerelease, v0.3.1-rc.1, remains unchanged. [v0.3.1-rc.2](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.1-rc.2) was published on 23 October 2026 at `5f10ad103af5818cb99331a9d71e8b5f518e93de`, consolidating the public source/query/quality and manuscript 7.0.7 review work. The [publication receipt](../evaluation/releases/v0.3.1-rc.2-publication.json) records the successful candidate and publication jobs, all five downloaded/verified assets and 263 verified source files. The next bounded release target is **v0.3.1-rc.3**, with its [precise C-08 packet](next-release-v0.3.1-rc.3.md). Full application integration and independent semantic acceptance remain unclaimed.

## Delivery rule

Release one completed, reviewable improvement at a time: finish a scoped batch, reconcile its evidence/claims, pass relevant checks, freeze a new commit and publish a new development tag. A parent issue may remain open across several releases. Do not wait for a large issue to be entirely complete, and do not equate frequent releases with growing scientific validity.

Every push to main now prepares a checked candidate through [the incremental workflow](../.github/workflows/incremental-release.yml). It checks structural/native/OWL generation, source and quality accounting, actual synthetic query answers, traces, documentation and regressions. It uploads the exact source archive, inventory, candidate receipt, release notes and checksums as an Actions artifact retained for 30 days. Candidate preparation is automatic; it is not a published GitHub Release.

To publish, run the same workflow from main with an explicit unused `v0.3.1-rc.N` tag and `publish=true`. The default is `publish=false`. The publication job checks all candidate gates, refuses an existing tag/release, creates a draft prerelease at the checked commit, uploads and byte-verifies its assets, then publishes it as a prerelease. No stable release or `latest` promotion is automated. A failed upload/verification leaves an inspectable draft; it never replaces a published version.

An equivalent reviewed request can be committed in `releases/development-request.json` with an explicit unused development tag, `profile=development-prerelease` and `publish=true`, alongside `docs/prerelease-TAG.md`. Only a change to that request in the triggering main push enables publication. An unchanged retained request does not publish again on later ordinary pushes. The exact tagged commit supplies the request, release notes and packaged source. This path supports publication through repository changes when a client cannot call workflow_dispatch directly.

New model, mapping or shape semantics require their affected scientific engines and reports to be rerun and reviewed before release; the candidate checks do not turn old receipts into new engine runs. Evidence is bound to its actual source hashes. Documentation-only packages can retain unchanged verified scientific receipts. The candidate workflow does not publish private manuscript/database files that are outside the public tracked tree.

## Current work mapped to small releases

The numbers below are proposed cut order, not promises that a whole parent issue is completed in one batch. Skip or subdivide a packet when its evidence or domain decision is not ready. Package numbers and scientific maturity are separate. A changed conceptual baseline requires its own reviewed model version and package series.

| Proposed package | Focus and linked work | Small completion boundary | Broader work retained |
| --- | --- | --- | --- |
| v0.3.1-rc.2 — published | Consolidate completed #6/#8/#11/#14 and the continuous candidate path; publication #20 | Current public source/evidence, manuscript 7.0.7 review ledger, 11 passed gates and five verified assets | Author-facing manuscript binaries and private SQL companions remain separate from the public source assets |
| v0.3.1-rc.3 | #5: C-08 unit/scale policy and a selected integration batch | Approved explicit compatibility/missing-data policy plus positive, invalid, incomplete and mutation fixtures; publish exactly its scope | Remaining 17 NOT_RUN routes and full multi-relation acceptance can require more packets |
| v0.3.1-rc.4 | #4: reconcile one cluster of remaining formal/alternative routes | Source-bound disposition and supported alternative evidence; preserve all HermiT NOT_RUN outcomes unless actually executed | All 14 routes need eventual explicit disposition; no artificial reasoner passes |
| v0.3.1-rc.5 | #12: first current relational reconciliation batch | Identity/version/provenance mapping plus actual preservation/history tests for a selected population | Full migration, formula, workload and readiness claims remain separate |
| v0.3.1-rc.6 | #13: first independently prepared source/CQ population | Start with CQ06 and its independently specified expected joins; retain the 11 withheld case admissions | CQ07/08 and further case work can ship as subsequent packets |
| v0.3.1-rc.7 or later | #7: actual independent semantic review | Predeclared first identity cluster, actual eligible reviewer responses and reasoned dispositions | Timing depends on real reviewers; no simulated judgments or automatic stable designation |
| Later separately scoped release | #16: extensions/interoperability | Only an approved extension with its own requirements, ownership and evidence | Non-blocking future scope; no reserved release date |

Use a completed packet as the release trigger; aim for one focused packet per work cycle. A weekly review of completed packets is useful but no calendar-based publication is enabled. No time-to-stable or global readiness percentage is inferred from issue count. Before the rc.2 publication task, 13 of 19 issues were closed (68.4% by count), six research issues remained open and one prerelease was public. The focused rc.2 publication task is tracked separately in [#20](https://github.com/ArazSaieArasi3/riskium/issues/20); its actual workflow and release state determine completion.

## Local preparation

Use a clean checkout and the pinned SHACL/documentation dependencies, then run:

```sh
python tools/prepare_incremental_release.py --run-checks --tag v0.3.1-rc.2 --output /tmp/riskium-rc2-candidate
```

The output directory must be empty and outside the source checkout. `--run-checks` requires HEAD to be the target commit and refuses uncommitted changes. Source archives include only regular tracked blobs from that commit; untracked local/private files cannot enter. Existing output and published versions are never silently overwritten.

GitHub supports explicit manual workflow inputs and CLI draft/prerelease publication. Primary references: [workflow triggers](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow) and [gh release create](https://cli.github.com/manual/gh_release_create). Automatic candidate delivery is verified by a successful hosted run and its uploaded artifacts; publication itself is verified only after an actual publish run. An implemented publication job is not evidence that a new release was published.
