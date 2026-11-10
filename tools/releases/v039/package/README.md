# R2a package preparation

The builder reads committed Git objects and consumes the exact-source R1
qualification report. The separate verifier uses only the standard library and
the six downloaded assets; it does not import the builder, use the repository or
require the ontology toolchain. An independently supplied commit (and CI run for
CI-mode assets) anchors its source/provenance checks. A Git commit/tree hash is an
integrity binding, not a cryptographic author signature.

The existing branch-specific workflow qualifies the exact source first. A second
job, conditional on that qualification's success, downloads the first job's
artifact, runs the package guard tests, builds six CI-mode assets and verifies
them. The R2a artifact then retains those six assets and their separate test and
verification receipts. No release/tag, Wiki or Pages mutation is performed.

```sh
python tools/releases/v039/package/build_package.py \
  --qualification /absolute/path/qualification-report.json \
  --output /absolute/path/assets --mode local-preflight
python tools/releases/v039/package/verify_package.py \
  --assets /absolute/path/assets --expected-source-commit FULL_COMMIT_SHA \
  --report /absolute/path/verification.json
```

For actual CI assets pass their externally checked workflow run ID through
`--expected-run-id`. The unit tests deliberately use a synthetic adapter report;
they test packaging guards and never supply new ontology-engine evidence. The
actual package uses the fresh prerequisite CI report, not that fixture.

## R2b promotion checklist

1. Retain the qualified executable commit, actual CI artifact ID/digest and all
   six asset digests. Preserve any receipt-only descendant as separately identified
   delivery metadata. Rebuild/requalify if a selected input changes.
2. Prepare the coordinated release and maintained repository/Wiki/Pages projections
   from those bindings. Inspect the finite set of maintained pointers, generated
   pages and version roles before publishing. Source qualifications, archived
   components and live publication state remain separate.
3. Publish the verified six assets and download all six through their public
   release URLs; run the separate verifier with the pinned source/run IDs.
4. Publish the matching maintained entry points and read back their actual bodies,
   routes, version pointers and source/download links. Record individual channel
   outcomes, not a blanket success inferred from a local build.
5. Close #92/#93 only when their own last acceptance criteria pass. If any channel
   fails, keep that gate open and record the bounded repair. Roll back maintained
   pointers/deployment to the previous verified release if necessary; retain
   release history and original research receipts.

Full PostgreSQL migration, external term curation, independent semantic review,
production workloads and product development are separately scoped future work.
Manuscript 7.2.21 remains unchanged.
