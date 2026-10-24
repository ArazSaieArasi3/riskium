# Preparation verification

Evidence accounting only; source checkpoint `7968d7ef5662d05f171568278f27df204f50cbd9`. No new HermiT/SHACL scientific execution, owner judgment or article modification is implied by these preparation checks.

- `python tools/build_final_review.py --write` followed by `--check`: eight deterministic outputs matched; 25 clauses, 31 historical NOT_RUN routes, 28 traces, 11 pending prompts, 65 baseline manuscript claims and seven exact prose proposals bound.
- Three isolated negative probes were rejected: omitted clause, fabricated owner rating and nonexistent evidence key. No probe changed the source checkout or live owner register.
- `python tools/build_quality_report.py --check`: existing 14-metric/25-clause/28-trace historical synthesis matched unchanged inputs.
- `python tools/build_traceability.py --check`: all 28 original traces matched, with no full requirement acceptance claim.
- `python tools/publication/audit_portal.py`: 21 pages / 3,634 local links and four graph-isomorphic serializations passed structural audit. This is not fresh deployed browser QA.
- `python -m unittest discover -s tests -v`: all 137 software regressions passed locally.
- The exact local Word/PDF hashes were checked against the existing manuscript ledger; each of the seven source paragraph hashes was checked before preparing full original/replacement text. The article files were not edited or rendered again.
- The candidate workflow now adds the preparation check as gate 17. Main push does not request another prerelease: `releases/development-request.json` remains unchanged. Hosted result is recorded with completion of preparation issue #27.

The final target remains v0.3.1. Actual judgments (#7), accepted necessary manuscript edits/QA, critical-finding resolution and the reviewed final publication/freeze/readback remain pending; see [freeze-checklist.md](freeze-checklist.md).
