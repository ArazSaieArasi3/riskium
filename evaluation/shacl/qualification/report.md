# Scheme-qualified vocabulary and role-qualified evidence — module 0.5.0

Source commit `3e34a5d446b788b71a97126246f0914e42b1efbc`. **2/2 scoped obligations PASS**. **47 actual SHACL validations**, 0 unexpected outcomes and 0 errors. [Policy](profile-review.md) and [full compressed receipt](report.json.gz) define the exact limits.

Every selected VocabularyConcept subtype receives a managed record with explicit scheme, edition, local code and descriptive label. Only ClassificationTerm descendants require the matching `belongsToScheme` pair. An EvidenceReference record identifies source, item, target and Support/Challenge/Context role; the explicit `pointsToEvidence` and role-appropriate support pair are checked. These are application metadata and graph checks. A source link and even a Support role never prove the target's truth.

Each case preserves raw/effective data, shapes and result graph snapshots, identity map, input digests and exact shape/component/focus oracle. Raw means staging only. Inference is none; no imports or truth repair. Selected endpoint and catalog cases are included, while full managed integration remains #5 and independent interpretation remains #7.

| Case | Constraint | Expected | Observed | Result |
| --- | --- | --- | --- | --- |
| `VOC-RKM-C006` | C-11 | CONFORMS | CONFORMS | PASS |
| `VOC-RKM-C017` | C-11 | CONFORMS | CONFORMS | PASS |
| `VOC-RKM-C019` | C-11 | CONFORMS | CONFORMS | PASS |
| `VOC-RKM-C027` | C-11 | CONFORMS | CONFORMS | PASS |
| `VOC-RKM-C028` | C-11 | CONFORMS | CONFORMS | PASS |
| `VOC-RKM-C029` | C-11 | CONFORMS | CONFORMS | PASS |
| `VOC-RKM-C038` | C-11 | CONFORMS | CONFORMS | PASS |
| `VOC-RKM-C039` | C-11 | CONFORMS | CONFORMS | PASS |
| `VOC-RKM-C040` | C-11 | CONFORMS | CONFORMS | PASS |
| `VOC-RKM-C042` | C-11 | CONFORMS | CONFORMS | PASS |
| `VOC-RKM-C046` | C-11 | CONFORMS | CONFORMS | PASS |
| `VOC-RKM-C059` | C-11 | CONFORMS | CONFORMS | PASS |
| `VOC-RKM-C060` | C-11 | CONFORMS | CONFORMS | PASS |
| `VOC-RKM-C061` | C-11 | CONFORMS | CONFORMS | PASS |
| `VOC-RAW-INCOMPLETE` | C-11 | CONFORMS | CONFORMS | PASS |
| `VOC-MISSING-SCHEME` | C-11 | VIOLATES | VIOLATES | PASS |
| `VOC-MISSING-EDITION` | C-11 | VIOLATES | VIOLATES | PASS |
| `VOC-MISSING-CODE` | C-11 | VIOLATES | VIOLATES | PASS |
| `VOC-MISSING-LABEL` | C-11 | VIOLATES | VIOLATES | PASS |
| `VOC-BLANK-CODE` | C-11 | VIOLATES | VIOLATES | PASS |
| `VOC-SCHEME-MISMATCH` | C-11 | VIOLATES | VIOLATES | PASS |
| `VOC-DELETED-AGREEMENT` | C-11 | CONFORMS | CONFORMS | PASS |
| `VOC-DUPLICATE-KEY` | C-11 | VIOLATES | VIOLATES | PASS |
| `VOC-DELETED-UNIQUENESS` | C-11 | CONFORMS | CONFORMS | PASS |
| `VOC-OTHER-SCHEME` | C-11 | CONFORMS | CONFORMS | PASS |
| `VOC-OTHER-EDITION` | C-11 | CONFORMS | CONFORMS | PASS |
| `VOC-ASSERTED-ALIAS` | C-11 | CONFORMS | CONFORMS | PASS |
| `VOC-WRONG-CANDIDATE` | C-11 | VIOLATES | VIOLATES | PASS |
| `EVIDENCE-SUPPORT` | C-12 | CONFORMS | CONFORMS | PASS |
| `EVIDENCE-CHALLENGE` | C-12 | CONFORMS | CONFORMS | PASS |
| `EVIDENCE-CONTEXT` | C-12 | CONFORMS | CONFORMS | PASS |
| `EVIDENCE-RAW` | C-12 | CONFORMS | CONFORMS | PASS |
| `EVIDENCE-MISSING-ROLE` | C-12 | VIOLATES | VIOLATES | PASS |
| `EVIDENCE-MISSING-SOURCE` | C-12 | VIOLATES | VIOLATES | PASS |
| `EVIDENCE-MISSING-ITEM` | C-12 | VIOLATES | VIOLATES | PASS |
| `EVIDENCE-MISSING-TARGET` | C-12 | VIOLATES | VIOLATES | PASS |
| `EVIDENCE-UNKNOWN-ROLE` | C-12 | VIOLATES | VIOLATES | PASS |
| `EVIDENCE-LITERAL-SOURCE` | C-12 | VIOLATES | VIOLATES | PASS |
| `EVIDENCE-MISSING-ITEM-PAIR` | C-12 | VIOLATES | VIOLATES | PASS |
| `EVIDENCE-DELETED-ITEM-RULE` | C-12 | CONFORMS | CONFORMS | PASS |
| `EVIDENCE-SUPPORT-WITHOUT-PAIR` | C-12 | VIOLATES | VIOLATES | PASS |
| `EVIDENCE-DELETED-ROLE-RULE` | C-12 | CONFORMS | CONFORMS | PASS |
| `EVIDENCE-CHALLENGE-WITH-SUPPORT-PAIR` | C-12 | VIOLATES | VIOLATES | PASS |
| `EVIDENCE-OTHER-ITEM` | C-12 | VIOLATES | VIOLATES | PASS |
| `EVIDENCE-OTHER-TARGET` | C-12 | VIOLATES | VIOLATES | PASS |
| `VOC-INTEGRATED` | C-11 | CONFORMS | CONFORMS | PASS |
| `EVIDENCE-INTEGRATED` | C-12 | CONFORMS | CONFORMS | PASS |

Reproduce with `tools/build_qualification_shapes.py`, `tools/run_qualification_shacl.py` and `tools/summarize_shacl.py` in the pinned SHACL environment.
