# Extension ownership and adoption boundaries

The [versioned register](../requirements/extensions.json) completes the boundary-policy work in #16. It contains 17 records: three optional phenomenon boundaries, seven proposed bridges, one local foundational anchor, three domain proposals and three unassessed alignment candidates. It adopts no external class, property, equivalence or import. Existing Riskium authors remain the maintainers identified in `CITATION.cff`; no external author is assigned work or represented as endorsing a mapping.

| Referent | Current Riskium representation | Optional bridges | Authority and applicability |
| --- | --- | --- | --- |
| RiskSource (`RKM-C007`) | RiskSourceReference (`RKM-X06`) | `RX-005`, `RK3-002` | Riskium owns the documentary reference; any resolved bearer needs an explicitly selected external identity/category authority. A possible source does not establish an occurrence. |
| Consequence (`RKM-C010`) | ConsequenceStatement (`RKM-C025`) | `RX-010`, `RK2-006` | An actual outcome requires source and referent evidence distinct from a statement; a bridge alone does not prove causation. |
| RiskControl (`RKM-C045`) | ControlReference (`RKM-X05`) | `R-66`, `R-67`, `RX-020` | Control bearer, implementation and measured effectiveness need separate evidence and authority. |
| External Object (`EXT-OBJECT`) | Local abstract bearer proxy | No external import closure | Riskium maintains the proxy; external kinds supply bearer identity. UFO/gUFO citation is not an adopted external distribution or a new Riskium kind. |

All seven bridge records preserve their exact source/target signatures. The three optional referents and seven bridge predicates remain outside the native/OWL typed core. Their existing [C-14 evidence](../evaluation/c14-boundary-review.md) remains unchanged.

| Proposal | Intended future task | Current state |
| --- | --- | --- |
| Business-domain profile | Independently sourced case/objective/context and method-version queries | Deferred; separate adapter and evidence population required |
| Health-domain profile | Source claims, temporal context and scenario/occurrence distinction | Deferred; no clinical validity or decision capability claimed |
| Risk-intelligence profile | Signal provenance, correction, uncertainty and unresolved identity | Deferred; no automatic RiskCase or occurrence promotion |
| COVER, ROSE and WATCHDOG alignment candidates | Reviewed directional mappings from exact external editions to named Riskium elements | Unassessed; the [prior-art register](../references/README.md) provides bounded citations, not implemented alignment |

Before adoption, name the proposed profile maintainer and external authority, pin exact source editions and terms, review identity/category/dependence and mapping direction, preserve missing/conflicting provenance, predeclare CQ answers and positive/negative/incomplete/mutation cases, and review affected model/ORSD/SQL/manuscript components. Original external work retains its own rights. A name or shared label never establishes equivalence. The register includes a specific CQ and evidence checklist for every proposal and bridge.

These proposals are nonblocking for the already published v0.3.1 research artifact. Actual implementation requires its own evidence and component revision; completion of this policy does not mean the proposals are implemented. `python tools/check_research_backlog.py --check` checks exhaustive boundary coverage and exact bindings.
