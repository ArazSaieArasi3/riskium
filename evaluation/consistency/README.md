# Cross-document consistency audit

Audit date: 26 October 2026. This closes the bounded review in #39 after formal-reference delivery #33 and assessment-correction packet #40. It joins the source ledgers, corrects current reading routes and verifies the actual publication channels. The exact corrected source, hosted checks and publication readback are bound in `completion.json`; the audit is not a new stable release. #41 owns the final component selection, release freeze, assets and independent download verification.

## What was reconciled

The [JSON trace table](traceability.json) and [CSV equivalent](traceability.csv) contain 423 unique rows: 28 original requirement/scope/CQ rows, 306 native model elements, 65 historical manuscript claims, seven approved article amendments, twelve retained release claims and five SQL correction requirements. Each row retains source digests, implementation or exclusion, oracle/evidence routes, outcome, permitted claim and limit, article location, documentation routes and follow-up issues. A common documentation route does not imply an element-specific article paragraph.

The [input inventory](inventory.json) covers tracked sources and their digests, including requirements/DRSD/CQs, model/native/OWL, reference corpus, implementations, evidence, release records, tools and checks. Generated outputs are accounted for separately by the publication registries and actual Wiki/Pages readbacks. Frozen snapshots and old assets are preserved. This is a complete join of the declared ledgers, not a new scientific completeness or correctness score.

The ontology remains 0.3.1, ORSD 0.4.3 and approved manuscript 7.0.8. The latest published source distribution remains v0.3.2. SQL assessment-correction 0.3.0/migration 4 and current documentation are identified development components. The original HermiT ledger remains 281 PASS / 14 NOT_RUN of 295 obligations; historical SHACL remains 341 scoped PASS / one PARTIAL / 17 NOT_RUN of 359. Three withdrawn manuscript claims, 250 incomplete SQL core mappings, eleven external elements and zero independent ratings remain visible.

## Findings and corrections

The [six-entry findings ledger](findings.json) records severity, affected locations, correction and verification. Current README navigation still selected closed #33, fourteen live Wiki pages lagged their shared projections, the manuscript checklist omitted its approved successor, the ledgers lacked one joined route, the formal introduction omitted correction 0.3.0 and WebVOWL links retained an older cache token. These are corrected without changing model identities, historical outcomes or accepted scope. Two additional Wiki projections changed during the audit, so sixteen distinct reader pages were updated; all twenty-one guides and two navigation files were then compared.

The review uses existing model/native/OWL builders for identity, direction and cardinality; source-bound formal/CQ/SQL ledgers for examples and original denominators; reference and release checks for citations, chronology and version compatibility; and documentation checks for commands, links, route consistency and frozen/current labels. No new interpretation of a standard, formula, application policy or independent judgment is inferred from those checks. Wider adequacy and policy work stays in #37/#13/#4/#5.

## Actual external artifacts and channels

The [manuscript readback](manuscript-readback.json) records fresh checks of the actual delivered Word and PDF bytes against the approved 7.0.8 SHA-256 values. All seven changed DOCX paragraphs match the approved text at their recorded body indices. The unchanged PDF retains its earlier nine-page rendering QA; no new render or article revision is claimed. The thirteen historical private SQLite-companion claim rows remain explicitly historical and were not freshly replayed here. Private article binaries and database archives are not included in this repository.

The [Wiki readback](wiki-readback.json) binds a fresh independent Wiki Git fetch and byte comparison for all 23 files. The browser also confirmed the rendered traceability, formal-method and work-plan pages. The [Pages readback](pages-readback.json) binds the deployment's source commit and actual HTTP response bodies, including current and frozen outputs. Generated-source equality and deployed equality are separate checks; a historical readback never proves a later publication.

The [release readback](release-readback.json) records fresh independent downloads of all six v0.3.2 assets and verifies all 586 archived source files. The eight earlier releases retain their registered asset IDs, digests, sizes and status, and all nine remote tags still identify their recorded source commits. Those older assets have fresh metadata/tag comparisons, not another full historical download. Fourteen protected source/evidence/frozen roots have no changes from the declared pre-audit baseline.

## Reproduce and use the gate

Run `python tools/audit_consistency.py --check`, `python tools/build_reference.py --check`, `python tools/publication/build_wiki.py --check` and `python tools/publication/build_versioned_site.py --check --previous-ref HEAD^` in the pinned Python environment. The audit rejects missing/duplicate rows, stale source hashes and changed historical acceptance states. Five regression tests include deliberately removed native/claim rows, a stale binding and an attempted independent-acceptance promotion. The current aggregate candidate preparation includes this audit as its twenty-eighth gate.

After any further source or documentation change, regenerate and recheck affected rows. Before #41 publishes, bind the final selection to its exact source, rerun all aggregate gates and verify the newly published assets and channels independently. Existing release-download receipts remain historical evidence until that new publication is checked.
