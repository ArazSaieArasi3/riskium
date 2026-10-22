# Riskium v0.3.1-rc.1: development prerelease specification

This document specifies the first development prerelease of conceptual design **0.3.1**. Its publication status is determined by the [GitHub Releases page](https://github.com/ArazSaieArasi3/riskium/releases), not by the presence of this file. It is not a stable scientific release or independent semantic certification.

## Package

The exact tagged source tree includes the structured conceptual source, native OntoUML exchange, bounded typed-core OWL mapping, selected/complete SVG views, requirements, scoped evaluation receipts, generated reference and reproduction tools. Use the source archive for an immutable snapshot. Pages follows `main` and the Wiki has its own Git history; neither moving public route substitutes for the tagged source. The release description must state the source commit, Wiki commit and checksum inventory.

## Authors and licensing

Araz Saie Arasi, Hassan Haghighi and Hossein Azgomi, in manuscript order. [AUTHORS.md](../AUTHORS.md) records the affiliations matched to manuscript 7.0.6. The artifact title is **Riskium: An Ontology for Modeling Enterprise Risk Knowledge**. Original scientific artifacts use **CC BY 4.0**, original software uses **MIT**, with distinct scopes in [RIGHTS.md](../RIGHTS.md). Third-party works retain their own terms. [CITATION.cff](../CITATION.cff) identifies the artifact; no DOI or article publication is invented.

## Executed evidence and limits

| Evidence | Scope |
| --- | --- |
| Conceptual inventory | 80 catalog concepts, including 77 typed core concepts and three optional boundaries; one imported anchor is separately recorded |
| Bounded OWL mapping | 77 typed classes and 127 object properties; not a complete representation of every interpretation constraint |
| HermiT | 693 cases passed in the complete candidate rehearsal; 281/295 baseline obligations covered, 14 NOT_RUN |
| SHACL | Five scoped modules; 341 PASS, 1 PARTIAL and 17 NOT_RUN out of 359 obligations |
| Regressions | 79 engineering tests passed in the clean candidate rehearsal |

The final freeze checks and any engine reruns must be recorded outside the tagged source, with hashes for their exact evidence. Historical receipts retain their actual source commits and are not relabeled as final runs. See [claim inventory](../evaluation/release-claims.md), [release gates](first-release-profile.md) and issue #15 for exact provenance.

C-08 unit/scale compatibility remains partial. The 14 HermiT and 17 SHACL unrun routes, full conditional/multi-relation integration, independent semantic review, requirement/CQ acceptance, standards interpretation, literature case acceptance, relational implementation and final manuscript review remain open. This package does not establish risk-assessment readiness, complete managed-record admission, an ontology explorer, a working database, regulatory compliance or an overall semantic-correctness percentage.

## Corrections and deprecation

Published tags and release evidence are immutable. Corrections use a new prerelease tag and identify the superseded version; a published tag is not moved to hide a correction. Preserve archived receipts with their original provenance. Model, mapping, constraint or engine-input changes require regenerated relevant outputs and new checks. Identifier changes require an explicit mapping/deprecation decision. A later stable scientific release needs a separate review and stronger evidence.
