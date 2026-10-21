# Formal validation plan

The [coverage contract](coverage-contract.md) is the current design baseline. Its JSON register owns constraint routes and execution acceptance; the generated row review owns source allocation. The following sections explain the intended formal work.

## What comprehensive coverage means

Coverage is defined from the model and declared claims, not from an arbitrary test count. The starting inventory includes every typed class, generalization, typed relation, endpoint obligation, interpretation constraint, current requirement and selected competency question. Cross-domain combinations and inference boundaries extend that inventory.

The current catalog has 674 baseline coverage obligations: 295 for HermiT-related work, 359 for SHACL-related work and 20 for combined requirement/query tasks. An obligation may require several positive, negative, boundary and regression fixtures. These are not 674 implemented tests. The later [HermiT report](hermit/report.md) records the executed subset of its 295 obligations; SHACL and combined requirement/query execution remain separate work.

## HermiT

Use the reviewed OWL mapping and exact import closure. The HermiT report tests ontology consistency, satisfiability of all 77 typed classes, all 66 declared generalizations and the supported semantics of 127 typed relations, with additional inference and boundary probes. It declares intended and forbidden inferences; the remaining constraints are recorded separately rather than counted as passes.

Resolve identity, overlap, disjointness, relator dependence, role participation and generalization-set assumptions before asserting their expected outcomes. Do not treat an abstract conceptual class as automatically unsatisfiable in OWL. Do not encode immutable database payloads or temporal authorization as OWL capabilities without a justified mapping.

## SHACL

Define raw, managed and task-ready profiles separately. Start with 254 endpoint-cardinality obligations for the typed relations, plus class admission and 25 constraint-encoding decisions. Add datatype, unit/scale, version coherence, temporal boundaries, provenance, duplicate/cycle and conflicting-value fixtures.

A source-end cardinality counts sources per target and therefore normally uses an inverse property path with the target as focus. A target-end cardinality counts targets per source and normally uses the direct path. Fixture design must verify this direction instead of copying a diagram label mechanically.

## Acceptance

Each obligation needs an exact source element, encoding disposition, fixture population, expected result, engine/version and execution receipt. Include valid fixtures, prohibited cases, boundary values and mutations. Record unsupported or not-applicable cases with reasons. Verify that negative fixtures fail for the intended rule.

Class coverage, relation coverage, constraint encoding, fixture coverage and actual execution coverage are separate denominators. Additional examples do not prove universal correctness. A green subset must not hide an unencoded constraint or an unexecuted task.
