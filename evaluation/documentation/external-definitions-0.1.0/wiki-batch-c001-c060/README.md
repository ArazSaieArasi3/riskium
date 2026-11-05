# Native Wiki publication batch C001–C060

Accepted on 5 November 2026 for issue #88, a bounded publication work package of #85.

All 60 dossiers `RKM-C001.md` through `RKM-C060.md` were saved through the native GitHub Wiki editor. A fresh independent Git fetch at Wiki commit `9858df83390cafa07249ad8ac6469d9d3b6df440` confirms exact byte equality with the authenticated CI Wiki projection for source `488db8a2336ffe963681e91144d7561e16bddded`, reader 0.4.8, documentary review 0.1.0. The 20 unchanged guide bodies also match. The receipt includes lengths and SHA-256 digests for all 80 equal bodies and expected/actual hashes for the remaining files.

## Acceptance boundary

The current Wiki has 105 Markdown files; the complete expected projection has 106. **This is a batch acceptance, not full native Wiki acceptance.** Issue #85 remains open. Browser transport/runtime timeouts interrupted subsequent editor access; independent Git readback determined which saves actually completed, avoiding repeated saves or a claim of whole-channel completion. No site bot block or authentication failure was observed.

| Next bounded package | Bodies | Acceptance |
| --- | ---: | --- |
| C061–C070 | 10 | Publish and fetch; compare all ten bodies exactly. |
| C071–C074 and X01–X06 | 10 | Publish and fetch; compare all ten bodies exactly. |
| External-Definitions, Concept-Index, Subdomains, Home, _Sidebar, _Footer | 6 | Publish all six, then match the full 106-file projection and rerun the complete channel verifier before closing #85. |

The parent review accounts for all 80 concepts in source and Pages. Its earlier [Pages/CI evidence](https://github.com/ArazSaieArasi3/riskium/blob/0043b8159c3638b0bbef0dfb58d03e46985232cf/evaluation/documentation/external-definitions-0.1.0/channels/README.md) remains a dated checkpoint. The present receipt updates only native Wiki publication observations. It does not replace the ontology's authored definitions, introduce formal equivalence, resolve normative mappings in #78, or supply independent ratings in #23. The model, source release and manuscript are unchanged.

## Reproduce

Fetch the native Wiki repository. Supply the actual Wiki directory and the CI Wiki projection extracted for source 488db8a to the accompanying verifier:

```bash
git -C /path/to/riskium.wiki fetch origin
python verify_wiki_batch.py --wiki /path/to/riskium.wiki --expected /path/to/ci-wiki/wiki --output wiki-batch-readback.json
```

The verifier reads `FETCH_HEAD`; it does not reset a working tree or publish changes. For whole-channel acceptance, use the complete channel verifier from the earlier checkpoint with the complete fresh Wiki snapshot, without its pending-Wiki option.
