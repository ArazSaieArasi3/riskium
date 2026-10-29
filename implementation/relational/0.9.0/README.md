# Risk-nature assertion 0.9.0: declaration

A reviewer needs to recover what a particular report said about the nature of a risk, including the source, local vocabulary, context and objective references used at that time. Another source may disagree, and two corrections may branch from the same original report. This packet declares that finite retrieval task for the proposed source distribution **v0.3.7**.

For example, A-v1 reports an unfavorable effect using context-v1 and objective-v1. A-v2 corrects it with a favorable report using context-v2 and objective-v2. A-v3 is an alternative mixed correction using the original context. B-v1 retains another source's report with a separate scheme-qualified term. Retrieving A-v1 must still return its original pins. The family of A-v1 contains A-v1, A-v2 and A-v3. A later A-v4 without a correction declaration stays outside that family.

**This is a preimplementation declaration under [#64](https://github.com/ArazSaieArasi3/riskium/issues/64).** The published source remains [v0.3.6](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.6); SQL 0.8.0/schema 9 and documentation 0.4.3 retain their existing meanings. The prospective runtime is SQL 0.9.0/schema 10 under [#65](https://github.com/ArazSaieArasi3/riskium/issues/65). Final integration and publication are [#66](https://github.com/ArazSaieArasi3/riskium/issues/66).

## Inspect the declaration

| File | Purpose |
| --- | --- |
| [Contract](contract.json) | Ten derived requirements, 31 exact native source routes, ownership, error/readiness policy and release gates |
| [Concrete inputs](execution-fixture.json) | Ten original source records; governed case/register/entry identities; eleven support versions; three contexts; seven initial assertions and one later issue; explicit correction and recording bindings |
| [Literal query answers](query-oracles.json) | Eight exact-version answer rows, case/family results, the non-endorsement envelope and nine literal native query rows |
| [Literal named graphs](native-oracles.trig) | Eight separately authored native expectations, including missing context/objectives and both original recording revisions |
| [Native query](native-query.rq) | SPARQL projection with an explicit graph binding, used to check the literal RDF expectations |
| [60 fixed controls](fixtures.json) | Positive, negative, incomplete, competing-source, history, populated migration, transaction, recovery and sensitivity controls; every actual result remains null/NOT_RUN |
| [Concrete negative requests](negative-inputs.json) | Fixed record copies, literal replacement values and preparation for malformed inputs; bind each variant to its control and expected rejection |
| [Prior population](prior-population.json) | Actual execution of the unchanged schema-9 fixture and six selection events; a dated preservation reference for the later upgrade |
| [Proposed storage and gates](proposed-design.md) | Ownership, keys, dependencies, issue ordering, recovery and reader/publication criteria for implementation |
| [Declaration manifest](declaration-manifest.json) | Exact byte bindings for the declaration and its checking tools |

The expected answers are synthetic agent-authored values, independent of any prospective risk-nature runtime output. They are available for review and mutation checks. They do not constitute an independent semantic review, a real organizational case or a source-truth judgment.

## Identity and missing information

RiskNatureAssertion is an InformationArtifact under G-07. Its issued version has a separate ArtifactVersion identity. NatureTerm inherits ClassificationTerm, VocabularyConcept and InformationArtifact; its stable scheme identity and code qualify its identity. Repeated labels are deliberately present in the fixture.

The native route to objectives is `C005 --R-43--> C002 --RK2-011--> X02`. Exact context and objective version pins are supplementary immutable bindings. Every assertion version must also have at least one recording EntryRevision through the existing R-44 route. Those entry bindings are captured before the recording revision issues.

Missing mandatory case, term or provenance keeps a received statement in raw staging. Native R-43 permits an absent context: U-v1 is managed but returns `NOT_READY_CONTEXT_UNRECORDED`. Z-v1 has an explicit context with no recorded objective references and returns `NOT_READY_OBJECTIVES_UNRECORDED`. Readiness means complete pins for this documentary retrieval task. Factual correctness, an actual occurrence and organizational authority each require their own evidence.

## Validate this packet

Use the repository's pinned RDF dependencies:

```sh
python -m pip install -r tools/requirements-shacl.txt
python tools/check_risk_nature_declaration.py --require-no-runtime
python -m unittest discover -s tests -p test_risk_nature_declaration.py -v
```

The checker validates source hashes, native directions and cardinalities, requirement/control coverage, input/expected-answer coherence, literal RDF/query agreement and the prior source preservation boundary. It executes no migration 10, new SQL/API, HermiT or SHACL obligation. Later runtime evidence must be saved separately while these original declarations remain unchanged. The exact independent source readback and accepted R1 scope are recorded in #64.

The native model remains 0.3.1, ORSD 0.4.3, original DRSD 0.1.0 and manuscript 7.0.8. Eleven organizational admissions remain WITHHELD and independent ratings remain zero. ClassificationAssertion, RecordStateAssertion, automatic selected truth, formulas, workflows, authorization, PostgreSQL/private migration and actual deployment acceptance retain their separate workstreams.
