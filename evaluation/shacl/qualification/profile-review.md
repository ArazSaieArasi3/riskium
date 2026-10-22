# Vocabulary and evidence qualification profile 0.5.0

This bounded application policy covers SHACL-0626/C-11 and SHACL-0628/C-12 in conceptual model 0.3.1. It adds no conceptual property, class or OWL axiom. The source and fixed coverage contract are pinned by hashes in the generated receipt. The policy is an author decision awaiting independent interpretation review in #7.

## C-11: operational vocabulary identity

The externally selected managed record and candidate have named IRIs. `q:scheme` names its governing resource, `q:edition` names the edition context, `q:localCode` is a nonblank string and `dct:title` is a descriptive label. The application key is `(scheme IRI, edition IRI, code literal)` within the submitted graph: two different candidate resources cannot share it. The same code in different schemes or editions is allowed; equal labels do not merge resources. Asserted instance aliases normalize before checking. This key does not prove real-world identity, scheme governance or the validity of a cross-scheme correspondence.

All 14 source-declared `VocabularyConcept` descendants, including the class itself, receive the record profile. For `ClassificationTerm` and its descendants, the record's scheme must also equal the explicit `R-05 belongsToScheme` target of the candidate. Other vocabulary subclasses lack this relation in the current core; their scheme is application metadata and no new core relation is inferred. The selected existing endpoint and catalog metadata shapes are combined in one fixture, not treated as universal record acceptance. Labels never become OWL classes.

## C-12: qualified use of evidence

An externally selected `EvidenceReference` record declares exactly one of `q:Support`, `q:Challenge` or `q:Context`, one named source locator, an explicitly typed EvidenceItem and an explicitly typed InformationArtifact target. Its candidate must have the explicit `RX-021 pointsToEvidence` pair for the item. `q:Support` requires the candidate's `R-68 supportsRecordedArtifact` pair for that target. `q:Challenge` and `q:Context` reject that support pair **to the same target**; a record concerning another target is assessed separately. This resolves the otherwise ambiguous reading of the support-named core relation without renaming or expanding it.

The source locator is a pointer, not proof of existence, authority, accuracy or publication rights. `Support` is a claimed evidential role, not a truth entailment or endorsement by Riskium. Independent assessment of adequacy, source interpretation and claim truth remains in #7/#8/#13. There is deliberately no `trueClaim` or `endorsedClaim` assertion in these shapes.

## Execution boundary

`q:` denotes `https://github.com/ArazSaieArasi3/riskium/profiles/qualification/0.5.0#`; these are application record fields. A caller supplies a nonempty list of record and expected core class pairs, independently of data declarations. Managed mode checks those records and the submitted graph; raw mode preserves incomplete material and does not assert managed acceptance. Only asserted named `owl:sameAs` instance aliases normalize; equal labels do not. Managed input cannot supply schema/import axioms or aliases of reserved vocabulary. The 66 pinned source subclass links are appended, with SHACL inference `none` and imports off.

Positive, negative, raw, alias, duplicate, wrong type and omitted-rule mutation cases have exact shape, component and focus oracles. Every engine run stores raw and effective data, shapes, results, input digests and runtime versions. Selected endpoint/catalog interaction does not close full conditional and multi-relation integration in #5; C-08 also remains partial. The two scoped PASS rows measure graph and application metadata conformance, not overall semantic correctness.
