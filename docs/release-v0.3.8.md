# Riskium v0.3.8 — manuscript evidence and current reader

This source package collects the maintained concept dictionary and public review evidence for author-held manuscript 7.2.3 in a reproducible distribution. It selects 32 component families: 30 retained, DOCUMENTATION replaced by reader 0.4.7 and MANUSCRIPT_REVIEW added. Model/OWL remain 0.3.1, ORSD 0.4.3, original DRSD 0.1.0 and SQLite SQL 0.9.0/schema 10.

The historical manuscript component stays 7.0.8. The new article-evidence component carries public source/report/receipt bindings for the ten-page 7.2.3 candidate, 36 references and six requested author papers; private Word/PDF and pharmaceutical source archives are excluded. Authored concept definitions do not establish external term equivalence. Independent ratings, all eleven organizational admissions and broader mapping/research limitations retain their original states.

## Downloads and verification

Use all six uploaded assets together. Verify `SHA256SUMS.txt`, extract `riskium-v0.3.8-source.tar.gz`, and run `python -S v0.3.8/tools/releases/v038/release.py verify --folder . --source EXACT_RELEASE_SOURCE_SHA`. The exact source is supplied by the actual tag/publication. Verification requires only standard-library Python and no Git or network. Internal agreement does not establish authenticity: check the archive digest/source against an independent trusted publication.

The manifest binds every tracked source body. All 904 predecessor-selected bodies are retained; fifteen delivery bodies use explicit archival aliases, while current delivery has separate source/qualification identities. Four frozen site snapshots and all fourteen earlier releases/tags/assets remain unchanged. The freeze receipt preserves FROZEN_NOT_PUBLISHED; actual draft verification, publication, public downloads and current channel reconciliation are later records.

## Scope and next steps

Reader 0.4.7 updates article/version/publication/work-plan routes while retaining the model-derived 80-concept dictionary and exact subdomain SVGs. The package adds no model semantics, SQL schema, PostgreSQL execution, independent semantic rating, dataset admission or article submission. External definitions #85, normative mappings #78, modules/COH/COP #77, independent review #23, dataset/pilot #13/#71 and context validation #72 retain separate gates. A possible v0.3.9 and first major v1.0.0 are future planning targets with finite acceptance criteria, not claims of completion.
