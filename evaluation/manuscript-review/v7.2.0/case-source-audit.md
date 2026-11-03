# Case-source denominator and admission audit for manuscript 7.2.0

This finite #80 audit reads the original author-held SQLite archive and the eleven-row adjudication CSV at the SHA-256 digests in [the machine-readable receipt](case-source-audit.json). It reruns aggregate read-only SQL, foreign-key and source-coherence checks. It does not publish the database, PDF passages, source rows or a fresh manuscript.

| Count | Observed | Interpretation |
| --- | ---: | --- |
| All catalogued works | 55 | Includes parked, reference, supplement and unextracted works; **not** the article denominator. |
| In-scope journal articles | 30 | All have source records with an active role. Seven other catalogued journal articles are outside this stage. |
| In-scope correction | 1 | Explicitly links to its original study; not an independent 31st journal study. |
| All source records | 1,023 | 1,011 active plus 12 historical supplement records outside this stage. Do not call all 1,023 the 30+1 active extraction. |
| Catalog items / item-record links / reported values | 883 / 1,011 / 1,695 | Structural aggregate counts over the archived relational database. |
| Scenario components / withheld decisions / accepted organizational cases | 84 / 11 / 0 | The eleven source-local candidates are withheld; no actual occurrence or RiskCase follows from the article corpus. |

The source/evidence join, item-link targets, value-to-record and value-to-evidence source identities, and scenario-to-evidence source identities have **zero mismatches** in this frozen database. `PRAGMA integrity_check` returns `ok`, with zero foreign-key violations. These checks establish internal structural consistency, not the truth of every extracted assertion. The correction is `MAT-018`, related to `NEW-PH-015`; it must not be counted as independent corroboration. The twelve outside-stage source records belong to the older conference supplement `PH-IEOM-2017`.

To replay locally with authorized copies of the pinned private inputs:

```sh
python evaluation/manuscript-review/v7.2.0/case-source-audit.py \
  --db /path/to/source_pharma.sqlite \
  --archive /path/to/Riskium_SQLite_v0.3.0-rc.1_integrated_review.zip
```

The script stops on an input hash, denominator, correction-link, withheld-decision or relational consistency mismatch. The article's Table VII **30 journal articles plus one corrigendum** and the 883/1,011/1,695/84/11/0 figures are supported by this exact archived input. If the article describes 1,023 rows as all belonging to the active 30+1 sources, revise that sentence; the correct split is 1,011 active and 12 outside-stage rows. The active journal-article count is not a count of independent organizational case validations. No case-accuracy percentage can be computed from these observations.

Parent [#13](https://github.com/ArazSaieArasi3/riskium/issues/13) stays open: independently prepared CQ06–CQ08 populations, source-truth judgments and case admission are separate scientific tasks. Independent semantic judgments are tracked in [#23](https://github.com/ArazSaieArasi3/riskium/issues/23). The next manuscript edit [#79](https://github.com/ArazSaieArasi3/riskium/issues/79) can use this denominator note without asserting the unfinished criteria.
