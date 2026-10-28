# Evidence-reference lifecycle 0.7.0 — executed development component

Implementation [#53](https://github.com/ArazSaieArasi3/riskium/issues/53) executes the frozen [#52](https://github.com/ArazSaieArasi3/riskium/issues/52) declaration under release #51 and broader #35/#12. It supplies additive migration 8, an audited internal Python API and actual SQLite evidence. Source distribution v0.3.5 is not frozen or published.

An existing issued C065 EvidenceReference can have explicit same-artifact correction branches and documentary, context-specific SELECT/WITHDRAW/CLEAR events. Selection requires an exact artifact/context/as-of ledger bound. WITHDRAWN returns a null selected pointer with its former version/history retained; another context and earlier as-of retrieval remain separate. Native item/target/version pins and all four literal v7 graph oracles are preserved.

The original nine-requirement [contract](contract.json) and [43 prospective expectations](fixtures.json) remain unchanged declaration-time files, including their historical NOT_RUN fields. [Current actual results](../../../evaluation/relational/evidence-lifecycle/report.json) record execution. [Design](design.json) and [concrete synthetic inputs](execution-fixture.json) precede implementation in Git history.

## Internal Python API

| Entry point | Result and reason |
| --- | --- |
| migrate / connect / health | Upgrade a populated valid v7 database or audit v8, retaining old rows/schema/semantic checks. |
| append | Atomically record a complete attributed CORRECT/SELECT/WITHDRAW/CLEAR event; return its database-assigned sequence. |
| issue / issue_corrected | Seal a plain version, or atomically seal it with an explicit correction; preserve caller transactions on failure. |
| selection | Return NO_SELECTION, SELECTED or WITHDRAWN for an explicit context and ledger bound. |
| family / ledger | Retrieve every declared branch and immutable event with separate source provenance. |
| native_graph / by_target | Read unchanged exact version graphs and target pins. |
| restore_dump | Restore then audit all current/prior schema/data/allocator invariants before committing. |

This API is a local Python function interface over SQLite. Callers provide every required source/identity/context field; fixtures expand common test inputs explicitly, while the runtime supplies no missing-source/context repair. Actor attribution is documentary metadata, not a native authority or verified access-control decision.

[Schema dictionary and index/transaction review](schema-dictionary.md) explains all columns/keys and recovery. [Execution and trace](../../../evaluation/relational/evidence-lifecycle/README.md) retain actual expected/observed results and limits. No full arbitrary assertion mapping, reinstatement, R-69..R-72, production deployment, independent semantic acceptance or new organizational admission is claimed.

Native model 0.3.1, ORSD 0.4.3, original DRSD 0.1.0, manuscript 7.0.8, old component bytes and all eleven WITHHELD/zero independent-rating decisions remain unchanged.
