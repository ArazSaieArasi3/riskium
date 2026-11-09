# Issue 93 candidate CI and publication staging

This additive packet qualifies `candidate/issue93-evidence-use`. It does not deploy Pages, upload Wiki pages, change a default ontology, or supply independent semantic acceptance.

## Execution

The branch-scoped workflow installs the recorded engine versions and replays B0-1 through B0-6 in a disposable detached worktree. The original checkout and the four frozen scientific inputs must remain unchanged. Each phase retains its fresh receipt and logs. The B0-3 SHACL serialization is saved with its actual receipt; the byte-pinned B0-4 input is selected separately after RDF graph-isomorphism checking. Historical receipts are never rewritten in the source checkout.

`run_ci.py` accepts `--root`, `--output`, `--schema`, `--robot`, `--sdk`, and `--node`. The schema and ROBOT hashes must match the existing candidate contracts. Output is an execution artifact, not committed research source.

## Publication staging

`build_projection.py` generates 89 standalone HTML pages and 89 prefixed Wiki Markdown pages from the complete B0-6 dictionary. All 82 catalog concepts and the external anchor retain their source-bound dossiers. HTML lives below `site/candidate/issue93/0.3.2-structural.2/`; Wiki page names begin `Issue93-Candidate-`. The generation is separate from the live reader, and no global Wiki Home page is overwritten. Every output is hashed, internal HTML anchors and Wiki routes are checked, and source links use the execution commit. External HTTP availability is not asserted.

## Integration gate

A successful run establishes reproducible candidate tooling and internally consistent staged reader projections. Default promotion still requires a separately qualified current-source release, a decision on the RiskCase core/profile boundary tracked in #92, and live-channel consistency checks. The synthetic SQLite sidecar remains separate from production PostgreSQL/data migration. Issue #93 stays open until the final affected-public-documentation and release-evidence criterion is actually fulfilled. No failed historical run is hidden, relabelled or repeatedly retriggered.
