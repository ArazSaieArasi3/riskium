# Maintained reader documentation 0.4.1

This namespace explains published source v0.3.5 and unchanged model 0.3.1. It is an additive editorial/status maintenance view after publication, not a new source release or semantic component selection.

The same 21 guide sources generate current Pages guides and 23 native Wiki files, including sidebar/footer. `.github/README.md` is the active GitHub repository landing page and must exactly match `Repository.md`. GitHub gives that location precedence over a root README. The released root README, documentation 0.4.0 and the 687 selected input files remain byte-preserved; they are historical source inputs rather than the active landing explanation.

`publication.json` preserves the independently executed six-public-download record from #59. Its historical results are not relabeled as fresh documentation execution. The deployment checks actual Latest/tag/asset identities again. `review-plan.json` fixes the audience paths and qualitative criteria adapted from the owner's OGCM-RF and Portfolio methods before the final assessment. It does not claim full framework conformance, a numeric usability score or independent expert review.

Build and check with:

```bash
python tools/publication/published_documentation.py --check
python tools/publication/published_documentation.py --output build/published-site --wiki-output build/published-wiki
```

The maintained projection preserves all four frozen snapshots, original semantic/engine data and release assets. Actual deployed bodies, native Wiki Git bytes and rendered journeys require separate postdeployment checks. Evidence is recorded under `evaluation/documentation/published-v0.3.5/` and issue #60.
