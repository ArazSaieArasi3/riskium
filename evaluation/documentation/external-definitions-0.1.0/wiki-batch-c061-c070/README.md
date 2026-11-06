# Native Wiki publication batch C061–C070

Accepted on 6 November 2026 for issue #89, the next bounded publication package of #85 after completed #88.

All ten dossiers `RKM-C061.md` through `RKM-C070.md` were published through the native Wiki editor. Fresh independent Git readback at `33de1cbe1bbd11ffa7dff4bc781a33e21866064b` confirms exact byte equality with the authenticated CI Wiki projection for source `488db8a2336ffe963681e91144d7561e16bddded`, reader 0.4.8, documentary review 0.1.0. The expected projection's 106 hashes were also checked against the CI `published-status.json` manifest.

The diff from the accepted #88 Wiki checkpoint `9858df83390cafa07249ad8ac6469d9d3b6df440` contains exactly these ten files. All 80 previously equal bodies (60 concept dossiers and 20 guides) retain their expected bytes. The receipt records lengths and SHA-256 digests for the 90 equal bodies, plus expected/actual hashes for the remaining files.

## Acceptance boundary

The current Wiki still has 105 Markdown files; the complete expected projection has 106. There are now 70 matching concept dossiers and 20 matching guides, leaving 16 bodies to synchronize. **This receipt accepts the ten-body batch, not the complete channel.** #85 remains open until full native Wiki and actual HTTP channel readbacks pass. The earlier [C001–C060 acceptance](https://github.com/ArazSaieArasi3/riskium/blob/2b188cefd5212ada6b45bdb995d4ddd94e6d3e1e/evaluation/documentation/external-definitions-0.1.0/wiki-batch-c001-c060/README.md) is retained as dated history.

| Next bounded package | Bodies | Acceptance |
| --- | ---: | --- |
| C071–C074 and X01–X06 | 10 | Publish, independently fetch and compare all ten bodies exactly. |
| External-Definitions, Concept-Index, Subdomains, Home, _Sidebar, _Footer | 6 | Publish, match the full 106-file projection and rerun the complete actual channel verifier before closing #85. |

No authored ontology definition, model relation, source release or manuscript was changed. This publication does not introduce equivalence axioms, resolve normative source adoption in #78, or supply independent semantic ratings in #23. The HTTP/Pages checkpoint was not rerun for this ten-body Wiki-only package.

## Reproduce

Fetch the native Wiki repository. Supply the Wiki directory, the actual CI Wiki projection for source 488db8a, and its corresponding `published-status.json`:

```bash
git -C /path/to/riskium.wiki fetch origin
python verify_wiki_batch.py --wiki /path/to/riskium.wiki --expected /path/to/ci-wiki/wiki --published-status /path/to/ci-pages/current/published-status.json --output wiki-batch-readback.json
```

The verifier reads `FETCH_HEAD`, compares the exact body bytes and the ten-path diff against the previous accepted Wiki checkpoint, and reports whole-channel acceptance separately. It does not reset a working tree or publish changes. Later Wiki updates can legitimately exceed the ten-path diff and should be accepted in their own dated receipt.
