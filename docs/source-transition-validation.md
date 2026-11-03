# Source transition validation

The manuscript and reader changes in PR #75 preserve the published research
implementation. Historical release qualification must use the source to which
its profile, selected files and receipts were bound. Replacing those receipts
with hashes of a new README would change the meaning of the old release.

## Execution boundary

`tools/check_source_transition.py` binds this transition to reviewed source
`50f731aa5e065233c81fceeadaab8d87f5569de6`. It compares every pre-existing tracked
file against that Git tree. The only permitted replacements are the two
declared current README/inventory files and the explicitly listed CI schedulers.
All ontology, SQL, runtime code, scientific tests, selected components and
published receipts must remain byte-identical. Added material is restricted to
the declared manuscript supplements, concept dictionary, diagrams and their
validation tools. An added scientific implementation requires a new component
qualification; the old replay cannot approve it.

The validation workflows and source-bound alignment/documentation checkpoints, v0.3.5 support/selection
and v0.3.6/v0.3.7 suite workflows first enforce this
boundary on the candidate, then create a detached worktree at the applicable reviewed source. The earlier v0.3.6 runner uses pre-publication source `86accc6695e4738dd1337d5b9addd73b82c73c3d`; the maintained v0.3.7 runner uses `50f731aa5e065233c81fceeadaab8d87f5569de6`, whose reader split also covers the later published reader. Each source has its own unchanged suite
and execute their source-bound commands there. The v0.3.7 routing policy already declares that the original full-source inventory is historical: putting the successor selection into the inventory it hashes would create a hash cycle. Historical jobs therefore use its existing `routing.py --inventory-receipt` check, which verifies every retained consistency output and emits the actual inventory as a runtime receipt. The candidate workflow still requires its complete current inventory to match. The full suites still execute their
tests, including mutation and restoration checks; no failure is ignored or
converted to an expected success. Their receipts identify the historical source.
The separate **Current manuscript and reader source transition** workflow checks
the current README, all tracked source inventory, source-derived diagram/dictionary and the new manuscript experiment replays.
Its receipt identifies the actual candidate source and every file digest. The new experiment scripts are copied unchanged into an isolated reviewed-source worktree, where their frozen runtime contracts resolve. The candidate gate proves that those scientific inputs and implementations are unchanged; the replay receipts retain the reviewed source identity.

## Scheduling and integration

The historical validation workflows cancel superseded attempts for the
same branch. Release packaging is triggered by its explicit release request or
selected version paths, instead of every documentation push. Completed reader
publishers are limited to their reviewed source, so a later README change cannot
silently republish an old reader or freeze the same source release again.

Tracked issue #81 records the repair and exact CI run links. PR #75 may be integrated after all applicable candidate checks and the source
qualified historical runs pass on the same head. This source integration does
not publish v0.3.8, change the ontology version, update live concept pages, or
submit an article. Issue #69 owns the next maintained site/Wiki publication and
actual route readbacks. Issue #76 owns selection, freeze and publication of the
next source package, with a newly declared component set.

## Failure policy

A scientific file change, deleted historical file, unexpected added code,
failing historical replay, current inventory mismatch or differing manuscript
oracle stops integration. A future implementation update must replace this
bounded documentation transition with its own reviewed version-aware policy.
Historical notification emails remain records of previous failed commits; the
current head and its run URLs establish the state after the repair.
