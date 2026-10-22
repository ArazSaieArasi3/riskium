# Explicit context and revision coherence — module 0.4.0

Source commit `7330a0b4382a95c1e27c46c9452e2bb1eea28f50`. **2/2 obligations PASS**, **48 actual SHACL validations**, 0 unexpected outcomes and 0 errors. [Full JSON receipt](report.json) and [profile decisions](profile-review.md) preserve the scope and evidence.

C-23 requires the same explicit hasContext pair for every analyzedInContext pair, without inferring the reverse or repairing missing values. C-24 checks matching singleton entry targets, optional single predecessors, arbitrary recorded transitive cycles and same-entry lineage. Branches remain allowed. Cycles of 1, 2, 3, 8 and 17 nodes, alias collapse, raw conflicts, type/target errors and removed/reversed/weakened rules have separate outcomes. Four cases integrate selected endpoint shapes and application metadata admission for all participants. No whole-profile admission is claimed.

The JSON retains exact raw/data/shapes/result snapshots, normalized identity maps, expectations and code/input digests. Reconstruct data and shapes with `run_admission_shacl.reconstruct_pair()` and its shared blank-node context. Engine inference is none, imports disabled, only pinned source taxonomy appended. Instance schema/import assertions and reserved-vocabulary aliases reject before SHACL; raw retains them. The conceptual model, OWL and coverage contract are unchanged. Static graph checks do not prove historical immutability or independent semantic correctness.

| Case | Constraint | Profile | Mutation | Expected | Observed | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `C23-MATCH` | C-23 | managed | — | CONFORMS | CONFORMS | PASS |
| `C23-GENERAL-ONLY` | C-23 | managed | — | CONFORMS | CONFORMS | PASS |
| `C23-UNSPECIFIED` | C-23 | managed | — | CONFORMS | CONFORMS | PASS |
| `C23-MISSING-GENERAL` | C-23 | managed | — | VIOLATES | VIOLATES | PASS |
| `C23-DIFFERENT-GENERAL` | C-23 | managed | — | VIOLATES | VIOLATES | PASS |
| `C23-MULTIPLE` | C-23 | managed | — | CONFORMS | CONFORMS | PASS |
| `C23-MISSING-ONE` | C-23 | managed | — | VIOLATES | VIOLATES | PASS |
| `C23-UNTYPED-SUBJECT` | C-23 | managed | — | VIOLATES | VIOLATES | PASS |
| `C23-WRONG-CONTEXT-TYPE` | C-23 | managed | — | VIOLATES | VIOLATES | PASS |
| `C23-CONTEXT-ALIASES` | C-23 | managed | — | CONFORMS | CONFORMS | PASS |
| `C23-LABELS-NOT-IDENTITY` | C-23 | managed | — | VIOLATES | VIOLATES | PASS |
| `C23-RAW-INCOMPLETE` | C-23 | raw | — | CONFORMS | CONFORMS | PASS |
| `C23-DELETED-RULE` | C-23 | managed | delete-context-inclusion | CONFORMS | CONFORMS | PASS |
| `C23-REVERSED-RULE` | C-23 | managed | reverse-context-inclusion | VIOLATES | VIOLATES | PASS |
| `C24-CHAIN-1` | C-24 | managed | — | CONFORMS | CONFORMS | PASS |
| `C24-CHAIN-2` | C-24 | managed | — | CONFORMS | CONFORMS | PASS |
| `C24-CHAIN-3` | C-24 | managed | — | CONFORMS | CONFORMS | PASS |
| `C24-CHAIN-6` | C-24 | managed | — | CONFORMS | CONFORMS | PASS |
| `C24-CHAIN-12` | C-24 | managed | — | CONFORMS | CONFORMS | PASS |
| `C24-BRANCH` | C-24 | managed | — | CONFORMS | CONFORMS | PASS |
| `C24-SKIPPED-PREDECESSOR` | C-24 | managed | — | CONFORMS | CONFORMS | PASS |
| `C24-BLANK-NODES` | C-24 | managed | — | CONFORMS | CONFORMS | PASS |
| `C24-MISSING-REVISION-OF` | C-24 | managed | — | VIOLATES | VIOLATES | PASS |
| `C24-MISSING-VERSION-OF` | C-24 | managed | — | VIOLATES | VIOLATES | PASS |
| `C24-DIFFERENT-ENTRY-TARGETS` | C-24 | managed | — | VIOLATES | VIOLATES | PASS |
| `C24-DELETED-EQUALITY` | C-24 | managed | delete-entry-equality | CONFORMS | CONFORMS | PASS |
| `C24-WRONG-ENTRY-TYPE` | C-24 | managed | — | VIOLATES | VIOLATES | PASS |
| `C24-UNTYPED-REVISION` | C-24 | managed | — | VIOLATES | VIOLATES | PASS |
| `C24-MULTIPLE-ENTRY-TARGETS` | C-24 | managed | — | VIOLATES | VIOLATES | PASS |
| `C24-CYCLE-1` | C-24 | managed | — | VIOLATES | VIOLATES | PASS |
| `C24-CYCLE-2` | C-24 | managed | — | VIOLATES | VIOLATES | PASS |
| `C24-CYCLE-3` | C-24 | managed | — | VIOLATES | VIOLATES | PASS |
| `C24-CYCLE-8` | C-24 | managed | — | VIOLATES | VIOLATES | PASS |
| `C24-CYCLE-17` | C-24 | managed | — | VIOLATES | VIOLATES | PASS |
| `C24-DELETED-CYCLE` | C-24 | managed | delete-cycle | CONFORMS | CONFORMS | PASS |
| `C24-WEAKENED-CYCLE` | C-24 | managed | self-loop-only | CONFORMS | CONFORMS | PASS |
| `C24-CROSS-ENTRY` | C-24 | managed | — | VIOLATES | VIOLATES | PASS |
| `C24-DELETED-LINEAGE` | C-24 | managed | delete-same-entry | CONFORMS | CONFORMS | PASS |
| `C24-TWO-PREDECESSORS` | C-24 | managed | — | VIOLATES | VIOLATES | PASS |
| `C24-RELAXED-PREDECESSORS` | C-24 | managed | relax-predecessor-count | CONFORMS | CONFORMS | PASS |
| `C24-ENTRY-ALIASES` | C-24 | managed | — | CONFORMS | CONFORMS | PASS |
| `C24-ALIASED-SELF-LOOP` | C-24 | managed | — | VIOLATES | VIOLATES | PASS |
| `C24-LABELS-NOT-IDENTITY` | C-24 | managed | — | VIOLATES | VIOLATES | PASS |
| `C24-RAW-CONFLICT` | C-24 | raw | — | CONFORMS | CONFORMS | PASS |
| `C23-INTEGRATED-VALID` | C-23 | managed | — | CONFORMS | CONFORMS | PASS |
| `C23-INTEGRATED-MISSING` | C-23 | managed | — | VIOLATES | VIOLATES | PASS |
| `C24-INTEGRATED-VALID` | C-24 | managed | — | CONFORMS | CONFORMS | PASS |
| `C24-INTEGRATED-CROSS-ENTRY` | C-24 | managed | — | VIOLATES | VIOLATES | PASS |

Reproduce with `tools/build_coherence_shapes.py`, `tools/run_coherence_shacl.py` and `tools/summarize_shacl.py` in the pinned SHACL environment. Parent #5 retains C-08 compatibility, other constraint routes and complete integration.
