# Reader and publication consistency — observed 2026-11-03 UTC

This is a dated pre-release decision sheet for [#70](https://github.com/ArazSaieArasi3/riskium/issues/70). A source-side edit in [draft PR #75](https://github.com/ArazSaieArasi3/riskium/pull/75) is not a claim that the public `main` landing or frozen release already changed. Repeat the live checks after merge and at the next actual candidate. Preserve historical reports and tags.

| Channel | Observed state and evidence route | Next candidate decision |
| --- | --- | --- |
| Repository root | Public `main` README still led with v0.3.4 and v0.3.5 on this date; draft PR #75 rewrites the landing for published v0.3.7. | Merge and fetch public root before calling it synchronized. Check all local targets and the four audience journeys. |
| Native Wiki | Live `riskium.wiki.git` Home and sidebar head `f20f12d6ad0c32125461b20e58a10d3b631ff79d` describe published v0.3.7 and reader 0.4.5; Home links repository, Pages, WebVOWL and releases. | Reclone/re-fetch native Wiki and check both directions, not just generated source pages. |
| Live Pages | HTTP 200 readback of `current/index.html`, `current/guide/Home.html`, `current/reference/native/index.html`, `current/widoco/index-en.html`, `current/webvowl/index.html`, `current/explore/index.html`, `versions/index.html`, `current/guide/Publication.html`; sampled HTML identifies reader 0.4.5/source v0.3.7. | Fetch again after deployment; check the reader's menu, home links and external navigation behavior in a browser. `docs/current/` in this checkout is an older 0.3.0 projection, not proof that live Pages is stale. |
| Source release | GitHub latest-release API gave tag v0.3.7, publication `2026-10-30T12:58:55Z` and six assets. | Verify tag/selection, six asset names, independent downloads, SHA-256 and release history; never use a draft qualification receipt as a publication receipt. |
| Manuscript | [7.2.1 author-held receipt](../evaluation/manuscript-review/v7.2.1/README.md) pins separate Word/PDF hashes and ten A4 pages. | Check exact author-approved file, six own references, page cap, counts, rights and bibliography. Do not describe the binaries as v0.3.7 assets. |

## Candidate gates, in execution order

- [x] **Source landing check at this draft:** [run the local audit](../tools/audit_reader_consistency.py) against the proposed README and verify relative links, version roles, licensing and manuscript receipt. Re-run on the exact candidate commit.
- [ ] **Model and quality evidence:** diff source catalog/hash, verify 11 subdomains and only source-bound concept/relation counts; compare requirements/CQ, 281/295 HermiT and 341/359 SHACL with their recorded PASS/PARTIAL/NOT_RUN units. Check selected pattern and query-parity receipt hashes. Avoid an aggregate semantic score.
- [ ] **Source corpus:** verify 30 active articles plus one corrigendum, 1,011 active source records, 12 out of scope and 11 WITHHELD decisions in [the audit](../evaluation/manuscript-review/v7.2.0/case-source-audit.md); no source record silently becomes an admitted RiskCase.
- [ ] **Paper:** render exact candidate Word and PDF; inspect pages/tables/figures/first-use abbreviations, six author citations, bibliography, claim-to-evidence mapping, ten-page cap and SHA-256. Record any new paper version separately from the model/release.
- [ ] **Licenses and attribution:** inspect [RIGHTS](../RIGHTS.md), [NOTICE](../NOTICE.md), [citation](../CITATION.cff), and excluded/private source rules in source and in each packaged distribution.
- [ ] **Candidate workflows:** execute affected requirements, references, quality, documentation, versioned software and release gates on one exact commit; link run ID, artifact ID, inputs, raw result and remaining NOT_RUN/PARTIAL rows. Defined YAML alone is not evidence of execution.
- [ ] **Public readback after deployment:** fetch `main` README, native Wiki Home/sidebar, Pages Home/guide/reference/WIDOCO/WebVOWL/versions, latest release/tag and six assets. Verify reciprocal paths from each home, active version labels and external-link expectations. Browser-test the menu; an HTTP 200 alone does not establish UX.
- [ ] **Closure:** write a dated matrix of source commit, URL, digest, observed result, exception and owner disposition; only then declare synchronized public channels. Track larger concept-page/navigation redesign in [#69](https://github.com/ArazSaieArasi3/riskium/issues/69) and full release qualification separately.

The current `main` README discrepancy is intentionally open in the live-readback gate until PR #75 lands. The live Pages and Wiki checks above are observations from this date, not promises about a future stable release.
