# Explicit context and revision coherence profile 0.4.0

This child of #5 implements exactly SHACL-0650 / C-23 and SHACL-0652 / C-24 from the unchanged conceptual model 0.3.1 and 359-row contract. Its source-field allocation is pinned and checked by the builder. No conceptual class, property, definition or OWL axiom is added. This is an explicit graph profile, not independent domain adjudication.

## C-23: direction and explicit completeness

`R-35 analyzedInContext` must be accompanied by `RX-001 hasContext` for the same pair. The reverse is not required. The source case and context types must be explicitly supported by the pinned source taxonomy. Missing data are reported, never silently materialized. The C-23 module alone does not impose the separate hasContext endpoint minimum on every case; endpoint admission remains a distinct rule, included in selected integration cases.

## C-24: entry targets and predecessor graph

Every selected EntryRevision has exactly one `R-33 revisionOf` and exactly one inherited `RX-006 versionOf`; both identify the same explicitly typed RiskRegisterEntry after asserted instance-alias normalization. An optional `R-34 previousRevision` has at most one target, which is an explicitly supported EntryRevision for the same entry. Zero predecessors is valid. Several later revisions may share a predecessor; this branch is allowed and is not an inverse-functional identity key. A recorded predecessor may skip an intermediate revision; no chronological or consecutive-number rule is invented.

`previousRevision+` detects a node returning to itself at any positive recorded path length. The query is not a fixed-depth expansion; fixtures exercise 1, 2, 3, 8 and 17-node cycles. Acyclicity is about the supplied graph, not unseen history. Cycle and same-entry queries have distinct source NodeShapes so the exact shape/component/focus oracle cannot confuse two SPARQL violations. Missing/equal/extra entry targets and endpoint types have separate property shapes.

## Focus, inference and identity

The managed graph selects C-23 cases through their class and both relevant subject predicates. C-24 selects revisions through class, revisionOf subjects, and both subjects and objects of previousRevision. Thus an untyped subject or predecessor cannot disappear from validation by losing its class assertion. Ordinary ArtifactVersions that are not revisions remain outside C-24. Empty/out-of-scope graph populations are not evidence of whole-profile acceptance; each obligation has nonempty declared fixtures and exact expected results.

Only the 66 source subclass triples are appended. Inference is none; no subproperty materialization, anonymous OWL fillers or imports supplies missing links. Asserted named instance sameAs aliases normalize; equal labels do not. Schema/import assertions and reserved-vocabulary aliases reject before engine execution. SameAs/differentFrom conflicts reject under the existing identity policy. Raw mode preserves the supplied graph with no normalization or managed conformance claim. Blank revision resources may pass these structural checks; the separate catalog metadata policy still requires named managed record/candidate identities.

## Evidence and integration limits

Positive, negative, raw, alias, wrong-type, branching and multi-step cases have independent expected shape/component/focus sets. Removing a required rule, reversing inclusion or weakening transitive cycles to self-loops has explicit mutation controls. Four cases combine all active C-23/C-24 shapes with selected original endpoint shapes and catalog metadata admission for each participant. This is selected integration, not complete multi-relation/conditional-profile admission.

Every raw/effective data, shapes and result graph is stored with a content hash; requests and identity maps are retained. Replay with the shared blank-node context of `run_admission_shacl.reconstruct_pair()`. Source/input/runtime digests bind the actual receipt. Engineering regressions and pre-validation errors remain separate from actual SHACL case counts.

C-03 issued-content immutability still requires application/transaction history tests in #12. Temporal correctness, real-world case identity, source truth, scale/unit compatibility, independent expert review and CQ execution are not established by this module. Both PASS rows are scoped graph-conformance results; the HermiT denominator and overall semantic-correctness status are unchanged.
