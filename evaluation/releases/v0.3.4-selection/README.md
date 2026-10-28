# v0.3.4 component selection

Bounded child #47 under #45 prepares the component set only. Stable remains **v0.3.3**; v0.3.4 has no new snapshot, stable publication profile, freeze, tag or release assets from this task.

[The declared policy](../../../releases/selection-policy-v0.3.4.json), [provisional selection](../../../releases/selection-v0.3.4.json), [separate development overlay](../../../releases/development-components-v0.3.4.json) and [readable component/dependency table](components.md) bind **27 components, 59 declared prerequisite edges and 286 unique selected files**. Shared paths record every component owner and must bind identical bytes. These counts describe selection, not correctness or complete runtime/code dependencies.

Twenty-two original v0.3.3 rows are retained without rehashing/relabeling their components. Three separately completed SQL components are added: source/scenario 0.4.0, lineage 0.5.0 and qualified evidence 0.6.0. DOCUMENTATION advances from frozen 0.2.0 to completed current 0.3.0. CONSISTENCY advances from 0.1.0 to 0.2.0 because current routing/input-binding metadata changed in #46; its [source comparison](../../consistency/current-0.2.0/source-comparison.json) preserves the exact 423 historical JSON rows and CSV bytes and names only the four changed top-level metadata keys. All original matrices, component files and accepted scientific inputs remain unchanged.

The declared SQLite chain pins schemas 2→3→4→5→6→7, exact reader/SQL files and existing migration ledger digests. Original source-bound completion/software/hosted receipts accompany the new components. The #42 receipt's historical format is preserved rather than inventing per-workflow head fields. Documentation #46's Wiki/HTTP receipts are retained evidence of that source; they do not establish freshness for a later final freeze. All ten preceding releases remain in the preservation contract; actual final tag/asset checks are future publication work.

Reproduce with:

```bash
python tools/build_release_selection.py --check
python -m unittest discover -s tests -p test_release_selection.py -v
```

The validator rejects missing/duplicate/wrong component versions, incompatible models, missing/wrong/duplicate/cyclic/out-of-order dependencies, undeclared graph changes, unsafe/duplicate/missing or conflicting file bindings, lost descriptor/receipt closure, changed historical rows/CSV/summary, old register changes, incorrect migration chains, omitted tooling, fabricated source/acceptance/freeze state and missing future/prior-release gates. These software controls do not certify domain semantics.

Next under #45: review/register the v0.3.4/documentation-0.3.0 snapshot compatibility and freeze an exact reviewed documentation source, then explicitly refresh the provisional selection after snapshot/source changes. Run final-source checks and fresh channel evidence before registering/freezing/publishing the final distribution and independently verifying actual assets/Latest and prior preservation. Model 0.3.1, ORSD 0.4.3, original DRSD 0.1.0, manuscript 7.0.8, all eleven WITHHELD admissions and zero independent ratings remain unchanged.
