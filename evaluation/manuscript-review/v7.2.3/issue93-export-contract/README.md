# Candidate native and OWL export contract

Date: 2026-11-08. Scope: **B0-4 / P1**, continuing [issue #93](https://github.com/ArazSaieArasi3/riskium/issues/93) after the combined B0-3 audit. The native/OWL contract route is complete in this candidate packet. **Production promotion is not complete; #93 remains open.**

## Decision and implementation

[input-contract.json](input-contract.json) binds the source version, term and version namespaces, source/policy hashes, inventory, generator dependencies, frozen production inputs, combined SHACL profile and six selected candidate definitions. It supersedes the private preliminary four-check input-gate checkpoint as the executable native/OWL route. The checkpoint did not itself implement generation.

[export_candidate.py](export_candidate.py) validates those inputs before generation and writes only its own ignored `generated/` directory. It calls the existing explicit-policy native serializer as a pure function, without invoking the earlier builders' file-writing entry points. [candidate_owl.py](candidate_owl.py) is an additive source-driven adaptation of the baseline mapping, with the candidate coverage and C-26 mappings explicitly selected. It does not patch the previous OWL graph or bypass the historical generator guards.

The term namespace deliberately remains `.../ontologies/riskium/0.3.1#` for compatibility with the current candidate SHACL/data signatures; the candidate source version is `0.3.2-structural.2` and its separate `owl:versionIRI` is `https://github.com/ArazSaieArasi3/riskium/candidates/issue93/generalization-sets`. Reusing term IRIs does not assert equivalence of ontology versions or publication of the candidate. Choosing a future public namespace/version scheme remains a release decision.

The inventory is 82 catalog concepts, one imported local anchor, 137 catalog associations, 67 generalizations and 26 source constraints. The native/OWL formal surface contains 79 source classes plus the local anchor, 130 typed source relations and eight explicit generalization sets. The two auxiliary evidence context/purpose vocabulary terms are reported separately. These populations must not be interchanged.

The contract is a reviewable Git-bound declaration, not a digital signature or independent semantic approval. Editing a contract and its matching sources requires a new review/receipt. Bindings to six selected definition pages do not establish completion of the 82-concept dictionary, Pages or Wiki.

## Actual verification

The [verification receipt](verification-report.json) contains the commands, output hashes, per-case outcomes and test logs.

| Check | Observation and supported interpretation |
|---|---|
| Contract and output tests | All 14 unit tests pass. They exercise deterministic generation, selected source fidelity and rejection of wrong versions, hashes, inventory, namespaces, ontology identity, missing bindings, promotion flags, escaping paths, legacy native sets and changed relation cardinality. |
| Frozen baseline | 11 native exchange, seven OWL mapping and five source-transition tests pass: 23/23. Original production exporters, guards and reviewed inputs remain unchanged. |
| Native representation | The generated native file is byte-identical to the B0-2 combined candidate, has 596 elements and 67 generalizations, and omits both mixed sets while preserving the eight explicit sets. Pinned schema validation has zero errors; ontouml-js 1.0.0 preserves checked round-trip invariants. |
| OWL mapping comparison | After removing documentary annotations and version metadata, the generated OWL graph is isomorphic to the prior combined candidate's logical graph. Class descriptions are emitted directly from the candidate source rather than copied from the old OWL graph. This is a projection comparison, not a proof of complete semantic preservation. |
| Fresh engine checks | One whole-candidate HermiT consistency invocation succeeds and ROBOT reports OWL 2 DL profile conformance. These results belong to the new output; no historical receipt or manuscript denominator is rewritten. |
| Combined data profile | All 20 SHACL cases match expected outcomes, including 14 negative cases and direct/chain sameAs aliases. The newly generated OWL is the ontology graph; inference/imports are disabled. |

The new OWL file differs in documentary annotations, provenance and deterministic serialization from the older candidate file. Equal logical projections are checked by graph isomorphism rather than byte hashes or blank-node labels. Output hashes refer to the actual files generated in this run.

## Replay

Use the pinned Python/schema/ROBOT dependencies from the [B0-1 instructions](../issue93-evidence-use/README.md#replay), together with ontouml-js 1.0.0. On a fresh checkout first materialize the deterministic candidate source/policy and comparison outputs:

```sh
python evaluation/manuscript-review/v7.2.3/issue93-generalization-sets/build_candidate.py
python evaluation/manuscript-review/v7.2.3/issue93-export-contract/export_candidate.py
python evaluation/manuscript-review/v7.2.3/issue93-export-contract/export_candidate.py --check
python evaluation/manuscript-review/v7.2.3/issue93-export-contract/verify_export.py --schema /tmp/ontouml-schema.json --robot /path/to/robot-1.9.11.jar --sdk /path/to/node_modules/ontouml-js --node /path/to/node
```

The prerequisites rebuild ignored comparison files; historical receipt files are not rewritten. Do not regenerate the committed B0-3 SHACL profile merely to obtain a different hash: the contract binds that exact reviewed file. The native SDK check retains the previously disclosed generated-ID seed adjustment for this execution environment; explicit source IDs and serializer rules are unchanged.

## Remaining work

**P2 is next:** specify and implement one small SQLite/RDF slice for justified evidential use, its reference participation, evidence artifact, grounding record, context and purpose. Preserve information-only references rather than inventing actual use from a citation. The prior four-projection mismatch has not been repaired by this exporter.

**P3 follows:** generate and reconcile the full candidate dictionary/structural bindings and affected readers/diagrams, then exercise candidate CI and decide promotion readiness. Only selected definition/SHACL inputs are bound here. No new GitHub Actions success, public release, production migration, real-case population or full independent semantic acceptance is claimed. Main, historical inputs and manuscript 7.2.21 remain unchanged.
