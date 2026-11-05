# External-definition source and publication checkpoint — 5 November 2026

PR #87 merged the reviewed source at `488db8a2336ffe963681e91144d7561e16bddded`. All 14 PR workflows and 14 main workflows succeeded. Four retired main publisher runs were skipped. Reader 0.4.8 deployed in run 42031546220. Model/OWL 0.3.1, SQL 0.9.0/schema 10 and immutable source release v0.3.8 remain separate.

## Documentary review

All 80 authored definitions have an individually recorded source-comparison disposition. The register uses nine primary-source identities and 39 selected term/section locators: 40 RELATED, 18 ANALOGY, 13 CONTRAST, six scoped NO_DIRECT_EQUIVALENT_REVIEWED and three NEEDS_LICENSED_SOURCE. No formal equivalence or independent rating is asserted. Normative adoption remains #78 and actual independent judgment remains #23.

## Delivery evidence and exact remaining gate

The actual GitHub Pages and Wiki build artifacts were downloaded through the authenticated artifact route. Their ZIP digests are, respectively, `c6ec26b95bad781dcd47568096997beeb824557729abc9a90d2e37791e397c42` and `bc52e433fcc920075f0799a1f046dc9d96200dd7af7b230ad2e0fffff88937e8`. All 404 public HTTP bodies match the authenticated deployment artifact byte for byte. The local CI audit also covers 226 HTML pages, 35,880 local links and four preserved snapshots. The separate channel readback records actual HTTP and native Wiki comparison outcomes. The hidden zero-byte `.nojekyll` build marker is omitted by the upload and is not an HTTP resource.

Native Wiki is NOT synchronized. Its freshly fetched HEAD remains `7ab60f85dd957d9c63d7bb9be0e512e0e7a18840`, with 105 Markdown files. The source-qualified CI output requires 106 files: 20 existing guide bodies match, 85 bodies differ and `External-Definitions.md` is missing. Thus 86 bodies remain to publish and read back. No Wiki save action was executed: the browser interaction service timed out during a read-only page navigation, then state recovery and runtime reset also timed out. This is a limitation of that interaction path, not a claim that GitHub or the user’s session is unavailable.

Issue #85 remains OPEN. This checkpoint is not a completion certificate. Resume by publishing the exact 86 changed/missing Markdown bodies from the same main CI output, fetch the native Wiki afresh, compare its complete 106-file inventory with the artifact, and execute the strict channel verifier without `--allow-wiki-pending`. Record the evidence before closing #85. No acceptance criterion is waived.

The conference article remains the author-held 7.2.4 candidate; no new article revision, independent validation, source release or submission is claimed by this documentation pass.
