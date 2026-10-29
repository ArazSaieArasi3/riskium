# v0.3.7 integration evidence

R3 checkpoint, 30 October 2026. The completed runtime was executed at **`7f3f8440b22690d28cea750bd441dde78b1e0337`**, following the immutable R1 declaration at `805b1edecff254f1e21131aa6fd098344affb398`. This directory adds evidence reconciliation; it does not relabel that runtime source or edit its original expectations.

[inputs/r2-completion.json](inputs/r2-completion.json) is the complete, lossless JSON decoded from the actually published [#65 body](https://github.com/ArazSaieArasi3/riskium/issues/65). Expected size: **317,022 bytes**. SHA-256: **`cb01769bcf4d2e5f9d4bf7baeeb5ad0fe5313ac987c8c215ce086766ea02b268`**. This preserves evidence independently of Actions artifact expiry.

It contains the actual hosted receipt, independent hosted ZIP readback, local full query/source/dependency vectors and every exact-version native triple. Hosted [run 40971993707](https://github.com/ArazSaieArasi3/riskium/actions/runs/40971993707) succeeded with 550 current software tests plus 12 historical reader tests. The independently downloaded artifact `12941506372` has 13,243 bytes and SHA-256 `60fb7b592bbfbb6025f24c833e0708e43ffccab65585ed49aa2cabff13236c54`. All 60 fixed controls and 51 malformed-request variants completed. The original declaration still records NOT_RUN expectations.

| Evidence | Actual environment or scope |
| --- | --- |
| Hosted R2 | Python 3.12.15, SQLite 3.45.1; foreign keys and recursive triggers enabled |
| Local full vectors | Python 3.12.14, SQLite 3.53.1; clean exact R2 source |
| Exact queries | Eight complete row/source/dependency answers compared with fixed source records and pins |
| Native projection | Eight separate named graphs, 306 literal quads and nine exact query rows |
| External readback | F60 was completed only after the actual hosted ZIP download; the pre-download run honestly retained a pending control |

The [0.5.0 consistency overlay](../../consistency/current-0.5.0/README.md) independently resolves R1 literals, checks all observations and preserves all original populations. Reproduce with:

```sh
python tools/audit_risk_nature_alignment.py --check
python -m unittest discover -s tests -p 'test_risk_nature_alignment.py'
```

This is synthetic engineering evidence. It does not add an independent semantic rating, validate source truth, admit an organizational case or establish production performance. Historical scientific results and manuscript 7.0.8 remain unchanged. [Next gates](next-steps.md) are R4 reader delivery and R5 exact-source distribution.
