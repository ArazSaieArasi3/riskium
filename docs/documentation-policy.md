# Documentation policy

The model defines semantics. Source-controlled explanations interpret and navigate that model. Generated reference pages project it. Published Wiki and Pages surfaces do not create independent definitions.

Public text is English. Reader-facing headings describe their subject, such as Scope, Requirements or Evaluation. Readers should not need internal execution vocabulary to understand the research. Stable semantic identifiers remain available in reference data and supporting traceability.

Explain the domain concept, its rationale and its consequences directly. Avoid interchangeable template prose and long ticket histories. A reference page and a tutorial may use different structures because they serve different tasks.

Editing must preserve supported meaning, uncertainty, limitations and version state. A claim-sensitive or definition-sensitive change is reviewed against its semantic or evidential source. Clearer prose must not imply stronger validation.

The repository is the source-controlled home of the artifacts. The shared guide registry names one source per explanation; Wiki Markdown and Pages guide HTML are generated projections of that source. Pages contains the equivalent explanations as well as the generated reference/explorer. Existing Wiki slugs are preserved. Each published view identifies its source version and is verified after publication.

The current route is mutable. Registered documentation snapshots bind an exact committed input tree and exact presentation/output hashes; existing registrations cannot be replaced or removed. The legacy rc.1 website is preserved as observed at commit `3f332ea56cb27263d2435fa0ae20afb7a5d5f432`, without pretending earlier guides had always been immutable. Model, documentation, implementation and evidence versions remain separate. Publish the exact main-branch source only after its documentation workflow succeeds; native Wiki publication requires its own readback.
