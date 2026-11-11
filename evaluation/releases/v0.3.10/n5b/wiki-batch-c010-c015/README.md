# W1: native Wiki C010–C015

Date: 11 November 2026. This is a completed six-page documentary publication batch within the remaining v0.3.10 coordinated-publication gate (#85), not a new release or ontology-engine evaluation.

## Result and independent verification

| Check | Observed result |
|---|---|
| Frozen inputs | Public release ID 440894153 selects source `4ae0cdc72a1008e8107be320694d90324890b696`. The deployed reader artifact from run 42899912762 is artifact 13802387546, associated with documentary adapter commit `fb751343d19007c9fa8c43376181d8d1c5c2cb4f`. Its downloaded ZIP SHA-256 is `22fcee8b647917d0235ca0af44ac35f565fca60a31ef4c533ede71db0b8b88dd`. |
| Batch publication | RKM-C010.md through RKM-C015.md were saved through the native Wiki editor using the already qualified published Wiki bodies. A stale C014 browser view was reloaded; the underlying save was not repeated. |
| Independent Git readback | All six actual saved bodies match their deployed-artifact SHA-256 hashes byte for byte. The Wiki advanced from `397aac3a9ee850f05838fa5d340bf2c7df12a156` to `978635fd738eae944828673170a8e35235b25078`; its changed-path set is exactly these six files. |
| Preservation | All ten previously matching bodies still match. No unexpected path was introduced. The historical References body retains its expected bytes. |
| Complete current inventory | The [114-file readback](readback.json) records 16 matching files: fifteen updated concepts and one preserved historical reference. The remaining 98 files stay explicitly incomplete. |
| Boundaries | This execution did not rerun release downloads, HTTP Pages readback, ontology engines or database tests. Earlier successful release/Pages observations remain in their original receipts. Scientific definitions, selected release inputs, article files, public tag and release assets were not changed. |

The batch is **6/6 complete**; cumulative documentary synchronization is **16/114 (14.0%)**, not an ontology-correctness percentage. #85 remains open. Native Home and navigation still select the predecessor until the final guide/navigation batch.

## Next bounded execution and closure

Publish C016–C021 with at most two or three saves per browser call, then obtain a new independent Wiki Git readback before counting the batch complete. After an interrupted save, inspect actual stored content before retrying. Finish all remaining concepts, aggregate/structural bodies and guides; publish Home/sidebar/footer last. Close #85 only after all 114 expected bytes, cross-channel current pointers and navigation have passed their declared checks. Retain the separate #78 and #23 scopes and the paused H1–H3 scopes.

The [initial N5b receipt](../wiki-readback.json) remains unchanged as dated history. The [current progress record](../progress.json) points to this later checkpoint.
