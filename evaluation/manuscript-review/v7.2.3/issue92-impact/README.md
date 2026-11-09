# RiskCase impact inventory and bounded migration contract

B1 / issue #92. Inspection baseline: candidate commit `aafc9b77ea320d726fcd0ae3d78449d03c061a26`. This packet completes the impact analysis and predeclares the next implementation. It does not apply a source migration, publish a release, or close #92/#93.

## Decision

Use the adopted [analytical-item definition](../../../../docs/design/semantic-core-and-application-profiles.md): a RiskCase is an identifiable risk item for analysis and tracking relative to objectives and context; it may represent a threat or opportunity from a specified perspective. Formal organizational register acceptance is local. Preserve the existing kind commitment, identity supplier, identifiers, associations, cardinalities, subtype links and explicit set policy.

The main finding is a wording/profile-boundary problem. In the inspected source, R-01 requires exactly one case per entry and permits zero or more entries per case. RiskCase has context/objective minima RX-001/RX-003; no case-side minimum requires a register, owner or committee. The old catalog admission module explicitly checks documentary metadata for a caller-selected request; it does not implement full risk readiness. Its output must not be interpreted as universal case admission.

[The actual SQLite probe](sqlite-probe.json) created one disposable synthetic analytical case, with zero register entries, and obtained its RiskCase type from the existing `v_native_facts` view. Integrity was `ok`, foreign-key violations were zero and schema bytes were unchanged. The probe uses the frozen identity/history slice (schema user_version 2), not the latest full SQL component, real source data or PostgreSQL. No fresh HermiT/SHACL result is claimed by B1.

## Three boundaries for B2

| Boundary | Meaning and selected behavior |
|---|---|
| Analytical identity | A justified scoped analytical item can exist without approval or registration. Labels/scores do not merge identities. Entries, scenarios, assessments and occurrences retain their distinct roles. |
| Explicit task readiness | A declared analytical task may require explicit context, objective or other inputs. An incomplete task report is not an assertion that the case does not exist. OWL anonymous witnesses do not provide missing observed data. |
| Local operational eligibility | A separately selected example operational-register profile may require a linked entry and supported approval. Missing approval remains unknown; explicit denial remains distinct. The input cannot choose its own permissive profile. |

No global threat/opportunity partition, blanket class disjointness, extra institutional prerequisite or removal of context/objective minima is selected. A broad rewrite of every occurrence of “instituted” would alter documentary identity meanings and is rejected.

## Inspectable outputs

- [decisions.json](decisions.json): 18 decisions — six prose corrections, five profile-boundary actions, seven explicit non-changes. Zero formal structural changes selected.
- [proposed-source-delta.json](proposed-source-delta.json): 12 exact proposed field changes, with old/new text and reasons; not applied. The successor also needs its own version/date/publication metadata and fresh bindings.
- [inventory.json](inventory.json): 1,855 pinned tracked files were enumerated; 1,811 are UTF-8 text. There are 440 direct case-match files and 564 admission-terminology files, with overlap. Their union plus reviewed generic dependencies contains 756 files. Each has source hash, line locators and disposition. A hit is not a defect or an instruction to edit an archive. Non-UTF-8 and untracked/private content are outside the lexical scan.
- [input-bindings.json](input-bindings.json): selected original source, generator, profile, SQL and cohort hashes.
- [acceptance-oracles.json](acceptance-oracles.json): 20 planned cases with exact expected behavior and named mechanisms. **All 20 remain unrun in B1.**
- [verification-report.json](verification-report.json): reproducible inventory/input and proposed-delta audit. The simulated source delta preserves the full structural signature; this is not successor-model qualification.

The B0 candidate's machine inventory is already 82 concepts / 137 association entries, but its inherited counting narrative still says 80 / 134. Correct that narrative only in the successor; preserve the B0 source hash and historical report. Four other kind rationales also carry a boilerplate reference to instituted case identity; replace those rationales specifically without changing their stereotypes or owning-domain identity commitments.

## Exact next execution — B2

1. Copy the accepted combined B0 scientific candidate into a new `issue92-riskcase` packet. Apply only the declared semantic prose/scope delta plus successor metadata (`0.3.2-case.1` is a candidate design version, not a release tag).
2. Bind a new source/export contract and regenerate native/OWL through the explicit-set-policy pure route. Do not call older builders that overwrite B0 outputs. Preserve the B0 evidence repair and compare logical OWL graphs after removing documentary annotations/version metadata.
3. Add caller-selected analytical and local operational checks, then execute the 20 predeclared cases. Each mechanism reports its own actual result. Selected SQLite identity/entry and RDF query checks do not establish full context/approval persistence.
4. Regenerate the successor dictionary and selected reader bindings. Keep old source paths, cohorts, withheld judgments and engine receipts unchanged. Exercise a candidate CI route on the exact resulting commit.

If one mechanism exposes a genuine design ambiguity, report its exact failed expectation rather than weakening an oracle or claiming the whole migration is complete.

## Finite coordinated release target

The published predecessor is **v0.3.8** (2026-11-04). The existing `plans/v0.3.8.md` already names v0.3.9 as a possible planning slot; it is not a reserved or published tag. The next package's goal is:

> Publish one source-qualified Riskium distribution that contains the EvidenceItem/set-policy repairs and the adopted analytical RiskCase interpretation, with matching native, OWL, selected validation profiles, complete source-derived concept reader and consistent maintained repository/Wiki/Pages version pointers, while retaining the original scientific baselines and receipts.

After B2, qualify the selected next scientific source and its component closure, then package/verify assets, publish and read back actual maintained channels. Prefer a separately versioned current-source selection; do not overwrite 0.3.1 scientific paths or remove their hash guards. The precise package selection/tag is frozen at the qualification gate, independently of model/profile/SQL/manuscript versions.

The selected release does **not** wait for complete external-definition curation (#85), semantic COH/COP (#77), larger independent expert review (#23), reconstruction of all pharmaceutical case data (#71), PostgreSQL deployment (#36), or a software product (#73). Only portions needed for the selected source/reader contract are release gates. Those wider objectives remain explicit follow-ups. A new candidate does not change the author-held manuscript 7.2.21 or make its archived 0.3.1 results executions of the repaired source.

## Reproduction

Run `python build_inventory.py`, `python probe_sqlite.py` (redirect stdout to a new receipt when intentionally recording a new probe), then `python audit_impact.py` from this packet or by repository-relative path. The inventory is pinned to the inspection commit. Audit regenerates its own report; it applies the proposed delta only to an in-memory copy. No original scientific or historical report file is written.
