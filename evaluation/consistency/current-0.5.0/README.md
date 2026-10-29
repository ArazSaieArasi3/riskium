# Risk-nature integration alignment 0.5.0

This development overlay reconciles the completed R2 evidence for proposed source distribution **v0.3.7** under [#66](https://github.com/ArazSaieArasi3/riskium/issues/66). It extends the unchanged [0.4.0 overlay](../current-0.4.0/README.md) with ten nature-task routes. The published package remains v0.3.6. Model/OWL remain 0.3.1.

Run `python tools/audit_risk_nature_alignment.py --check` from the repository root. Generation without `--check` is deterministic. The validator does not import the nature runtime or runner to produce expected answers. It reads the R1 literal oracles, the losslessly preserved actual R2 receipt and original source definitions separately.

| Output | Meaning |
| --- | --- |
| [report.json](report.json) | R3 gate, exact executed-source role, input hashes, counts and pending gates |
| [traceability.json](traceability.json) and [CSV](traceability.csv) | All 460 predecessor routes unchanged plus ten NRA routes, queries, original requirements, controls and actual-receipt locations |
| [native-accounting.json](native-accounting.json) | Every one of 306 source identities, unchanged historical disposition and explicit witnesses for 31 selected routes |
| [database-requirements.json](database-requirements.json) | All 28 original DRSD definitions: 22 affected only within this task, two inherited and four deferred |
| [manuscript-dispositions.json](manuscript-dispositions.json) | All 65 approved paper dispositions retained; ten supported engineering statements explicitly outside manuscript 7.0.8 |
| [component.json](component.json) | Versioned consistency component and output/source bindings; not yet selected into a release |

The historical **236 deferred mappings remain 236**. Some of those native identities now have finite nature-task projection witnesses. Their original incomplete mapping disposition is preserved inside each row, with a separate `current_task` field. Paired explicit RDF types witness only the selected inheritance projection; they do not validate OntoUML identity, rigidity, all instances or all generalization constraints. The 306 RDF quads are distinct from the 306 model identifiers.

The complete [integration evidence](../../integration/v0.3.7/README.md) retains the original hosted and local engine identities. The existing [R1 contract](../../../implementation/relational/0.9.0/contract.json), historical fixtures and execution trace remain unchanged. `NRA-10` is explicitly partial pending R4/R5; a passed engineering control cannot substitute for reader or publication acceptance.
