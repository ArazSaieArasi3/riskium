# Manuscript and source-release roadmap after Riskium v0.3.7

**Planning checkpoint: 3 November 2026.** This is a prospective work plan, not a release receipt or a submission claim. [v0.3.7](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.7) is the published source distribution. Its model and OWL are 0.3.1; its frozen manuscript component is 7.0.8. The author-held, separately rendered manuscript 7.1.0 is recorded in [its intake](../evaluation/manuscript-review/v7.1.0/README.md). That intake does not put the Word/PDF or supplementary code into a public source release.

## Objective and order

**Immediate objective:** produce a better, source-bound ten-page CSICC 2026 manuscript 7.2.0 from 7.1.0. Reconcile its actual claims and artifacts, settle the remaining paper-sensitive wording and bounded evidence, then render and inspect the final Word/PDF. Independent semantic judgment, complete native/SQL mapping, production deployment, a concept-per-page website and all-context organizational validation are separate undertakings unless the manuscript claims their results.

| Order | Work and evidence | Owner issue | Exit and dependency |
| --- | --- | --- | --- |
| 0 — intake, now | Register the actual 7.1.0 Word/PDF/SVG/supplement hashes, model source and explicit limits; inventory every article claim, number, table, figure and citation. Inspect modifier-function wording and current venue format. | [#67](https://github.com/ArazSaieArasi3/riskium/issues/67) | A reviewed claim-to-evidence table and reproducible article baseline. The present intake is a first record, not that complete audit. |
| 1 — article evidence | Answer finite related-work and standards questions; reconcile 30 papers plus one correction, the withheld cases and exact source locators; adjudicate the selected pattern candidates and define any design metrics actually used. | [#37](https://github.com/ArazSaieArasi3/riskium/issues/37), [#13](https://github.com/ArazSaieArasi3/riskium/issues/13), [#68](https://github.com/ArazSaieArasi3/riskium/issues/68) | Paper reports actual observations and justified limits. Full catalogue screening and semantic COH/COP are included only after real execution, not required to preserve a bounded article. |
| 2 — next paper | Revise the manuscript and render/test exact Word/PDF within ten pages; verify six author citations, figures, evidence/claim agreement, references, abbreviations and submission policy. | [#67](https://github.com/ArazSaieArasi3/riskium/issues/67) | Candidate **manuscript 7.2.0** with own digest and receipt. Coauthor approval and submission are later explicit gates. This is the first point at which a new paper version can exist. |
| 3 — next source package | Select and qualify a compatible source/documentation/evidence component set, reconcile current repo/Wiki/Pages and source release, freeze, publish and read back actual assets. | [#76](https://github.com/ArazSaieArasi3/riskium/issues/76), supported by #67/#69/#70 | **Proposed v0.3.8**, not frozen or released. Its exact scope and component versions must be declared before a release request. No implicit model 0.3.2 or SQL migration. The paper may precede it if all cited inputs are accessible and pinned. |
| 4 — expanded research and reader experience | Complete the concept dictionary and site UX, broader case transformation, remaining pattern/metric work, synthetic and independent cross-context tasks. | [#69](https://github.com/ArazSaieArasi3/riskium/issues/69), [#70](https://github.com/ArazSaieArasi3/riskium/issues/70), [#71](https://github.com/ArazSaieArasi3/riskium/issues/71), [#72](https://github.com/ArazSaieArasi3/riskium/issues/72), plus #12/#35 | Later bounded package(s); **v0.3.9 is a tentative slot, not an allocated release**. Evidence may inform a later journal paper. |
| 5 — broader acceptance | Obtain independent semantic judgments and adjudication, remaining justified formal/SHACL and mapping routes, and a tested organizational use context. Separate deployment acceptance where actually in scope. | [#23](https://github.com/ArazSaieArasi3/riskium/issues/23), [#4](https://github.com/ArazSaieArasi3/riskium/issues/4), [#5](https://github.com/ArazSaieArasi3/riskium/issues/5), [#12](https://github.com/ArazSaieArasi3/riskium/issues/12), [#36](https://github.com/ArazSaieArasi3/riskium/issues/36), [#72](https://github.com/ArazSaieArasi3/riskium/issues/72) | A future first major release **v1.0.0 is a goal, not a promised date or already satisfied gate**. Publish only after a concrete accepted claim set and exact freeze/readback; it need not assert production readiness if production is excluded. |
| Future product | Define a risk-knowledge product, service boundaries and interoperability, then test a smallest service slice. Maintain the internal editorial/research-assistance policy separately. | [#73](https://github.com/ArazSaieArasi3/riskium/issues/73), [#74](https://github.com/ArazSaieArasi3/riskium/issues/74) | No source-release number or implementation claim has been assigned. |

## Comment ownership

Editorial changes already implemented in author-held 7.1.0 — title, two email addresses, abstract, scope, related-work themes, six author citations, section order, VVEAA introduction, separate quality/discussion headings and ten-page layout — are recorded in its [intake](../evaluation/manuscript-review/v7.1.0/README.md). They do not need a new open engineering issue individually; #67 owns their source-bound verification and any carry-forward correction.

| Outstanding comment family | Exact open owner(s) | Boundary |
| --- | --- | --- |
| Literature and standards source adequacy, diplomatic comparison | #37 | Finite inspected sources, not exhaustive novelty or equivalence. |
| Case study population, source-to-dataset rewrite and admission | #13, #71; mapping #12/#35 | A documented article source is not by itself an admitted enterprise RiskCase. |
| Pattern and anti-pattern review; subdomain design measures | #68 | Eight selected structural screens and graph counts already exist; semantic verdicts and COH/COP do not. |
| Independent expert judgment and organizational applicability | #23, #72 | Prepared protocol and illustrative contexts are not observed ratings or success at three scales. |
| Subdomain SVG, concept pages, documentation navigation | #69 | Reuse one authoritative catalog source and verify actual Wiki/Pages publication. |
| Experiment and workflow inventory, landing UX and cross-channel checks | #70 | Release-time checks must run on the exact candidate and actual public bodies. |
| Manuscript version/claim/format reconciliation and next paper | #67 | 7.1.0 is author-held; the repo's 7.0.8 historical component remains unchanged. |
| Product, microservices, dynamic risk and editorial policy | #73, #74 | Future work; private policy text stays out of the public repository. |

The existing open parents #4, #5, #12, #13, #23, #35, #36 and #37 retain their original acceptance criteria. The new issues assign owners to previously untracked comments; this plan does not close those parents, reclassify historical NOT_RUN results, alter the model, or revise frozen release documents.

## Manuscript 7.2.0 stop/go

1. A finite claim ledger links every retained result and number to exact input, method, observed report and version; the new SQL–SPARQL suite is separately replayed or explicitly source-bound, not folded into old engine counts.
2. Any changed literature interpretation is justified from inspected material. Six requested author papers have a relevant citation context. Real expert review is reported only if #23 has actual responses.
3. The SVG and selected OntoUML view are legible in the conference template. All scientific tables have borders, all citations resolve, and the PDF is at most ten pages after final rendering.
4. The paper names its bounded enterprise/ecosystem intent and pharmaceutical case context without asserting tested usefulness at every organizational level.
5. An exact final manuscript receipt and author decision exist. Submission and a new source-distribution release have separate gates.
