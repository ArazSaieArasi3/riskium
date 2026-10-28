# Evidence-reference lifecycle 0.7.0 — declaration only

**DECLARED_NOT_IMPLEMENTED.** Release parent [#51](https://github.com/ArazSaieArasi3/riskium/issues/51), declaration [#52](https://github.com/ArazSaieArasi3/riskium/issues/52), broader parents #35/#12. No migration 8, API, query execution, result receipt or native mapping completion is supplied by this declaration.

The [contract](contract.json) freezes nine derived ELC requirements and the [43 literal engineering expectations](fixtures.json) before implementation. They address only existing issued C065 EvidenceReference versions: explicit same-artifact correction branches, documentary context-specific withdrawal/selection, an explicit as-of ledger boundary, immutable provenance and unchanged named native graphs. Context/decision fields are application supplements and do not establish authority or truth.

A populated validated v7 database must upgrade additively, preserving migrations 1–7, original payloads/item/target pins, old graphs and all prior audits. Selection requires an explicit artifact/context/as-of sequence; no implicit newest branch or fallback. A withdrawn selected version yields WITHDRAWN and a null selected pointer in that context; earlier historical retrieval remains available. Reinstatement and notice-level correction remain deferred.

The original four EQR 0.6.0 literal graph oracles are reused by exact file hash. ref-A@3/@4 are lineage/selection fixtures with no invented native graph identity. The declared engine interface and diagnostics may only be amended with reasons in a separate prior commit, never by substituting observed output.

All expected outcomes are **NOT_RUN**. Future implementation must record actual input/code/runtime hashes, expected versus observed SQL/native results, populated migration/rollback/recovery and real weakened-rule controls. Passing JSON/source checks of this declaration does not execute any lifecycle behavior.

[Release definition](../../../plans/v0.3.5.md) and [conference-readiness gates](../../../docs/conference-readiness.md) keep mechanical trace accounting, scoped implementation and independent scientific adequacy separate. Native model 0.3.1, ORSD 0.4.3, original DRSD 0.1.0, manuscript 7.0.8, all eleven WITHHELD admissions and zero independent ratings remain unchanged.
