# Formal-method reading coverage

Task [#33](https://github.com/ArazSaieArasi3/riskium/issues/33) connects the existing formal and application evidence to a readable explanation. The source is [the method guide](../../docs/formal-method.md), projected to the existing Formalization route on Pages and to the shared Wiki Markdown. The [register](register.json) preserves exact source hashes, 25 clause statements, OWL encoding boundaries, historical engine obligation/case identities, owner-accepted exclusions and the later SQL assessment overlay.

## What changed

The former Formalization route explained the bounded OWL export and listed the 25 OWL dispositions. Readers still had to assemble the engine, task-profile, application/history and acceptance story from separate repository reports. The maintained guide now explains those languages and assumptions together, illustrates open-world and identity boundaries, provides exact reproduction commands and separates expected outcomes from recorded evidence. A 25-row index leads to a dedicated section for each constraint. Conceptual clauses and search results each have 25 direct method/evidence links.

Each clause retains its original statement, historical HermiT/SHACL state, encoding boundary, bounded accepted claim, remaining exclusions and receipt links. Expandable fixture sections expose original case IDs and clickable source routes. The SQL assessment overlay explicitly covers selected subclauses of eleven constraints; it does not expand the original owner decision or complete those constraints.

The source builder rejects missing clause/owner rows, changed conceptual statements, stale evidence digests and mismatched engine/source bindings. The portal builder rejects a stale formal explanation before projecting the shared sources. Browser inspection found raw Markdown in the first fixture disclosure; the final implementation renders it properly and a regression checks the actual links.

## Evidence and interpretation

[Verification](verification.json) records the exact tested source, software checks, selected current replays and unchanged scientific inputs. [HTTPS readback](http-readback.json) binds the deployed source and file bodies. [CI readback](ci-readback.json) records hosted outcomes. [Browser readback](browser-readback.json) records actual navigation, disclosures and responsive dimensions; screenshots are saved alongside it.

The original HermiT obligations remain 281 PASS / 14 NOT_RUN of 295. The historical SHACL obligations remain 341 scoped PASS / one PARTIAL / 17 NOT_RUN of 359. C-08 stays globally PARTIAL. Model 0.3.1, ORSD 0.4.3, manuscript 7.0.8, frozen documentation and v0.3.2 source assets remain unchanged. This delivery creates no full FOL/TPTP package, independent rating, complete assessment admission or new stable source release. Source parity for 21 Wiki guides is checked; a new native Wiki publication is not claimed.

Coverage improved from OWL-only clause explanations to 25 joined source/encoding/historical-outcome/accepted-scope/remaining-evidence routes. This is a verifiable documentation improvement. No reader-comprehension percentage or overall ontology-correctness score is inferred.

The final recorded population is 216 software regressions with no failures/errors/skips, 25 passed hosted candidate checks, 175 matching public file bodies plus the root source manifest, and two actual responsive frame widths with no document overflow. Both registered frozen snapshots remain unchanged.

## Next checkpoint

[#39](https://github.com/ArazSaieArasi3/riskium/issues/39) organizes the requested full cross-document audit before the next stable freeze. Run it after the next selected SQL packet stabilizes and CI is green, or for an earlier documentation-only stable candidate if that comes first. Bind the audit to one commit, extend existing requirement/CQ/clause/manuscript/SQL ledgers into one trace table, resolve critical contradictions and verify the deployed channels after publication. This release gate does not wait for every research issue or independent reviewer.

## Reproduce the reading checks

```sh
python tools/build_formal_reference.py --check
python tools/build_reference.py --check
python tools/publication/audit_portal.py
python tools/publication/build_wiki.py --check
python tools/publication/build_versioned_site.py --check
python -m unittest discover -s tests -p test_formal_reference.py -v
```

Use the pinned documentation dependencies and the complete suite for the recorded software population. Replaying scientific/application receipts remains a separate operation with the commands and limits in the guide.
