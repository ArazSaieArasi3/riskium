# Maintained concept dictionary reader

Reader **0.4.6** publishes the model-derived 80-concept dictionary, eleven subdomain purposes and exact package/matrix relationship views. The source release stays **v0.3.7**, model/OWL **0.3.1**, relational profile **0.9.0/schema 10**. Guide content keeps its original 0.4.5 source binding. This is a presentation/documentation change, not a scientific release or independent semantic validation.

The builder reconstructs reader 0.4.5 on exact source `50f731aa5e065233c81fceeadaab8d87f5569de6`, preserving every frozen snapshot. New dossiers derive from `documentation/concepts/0.3.1/` and the exact conceptual catalog. Each keeps identity, dependency, relation endpoints, source IDs and explicit unassessed external-definition/alignment fields.

## Build and verify

```sh
python tools/publication/dictionary_documentation.py --output build/site --wiki-output build/wiki
python -m unittest discover -s tests -p test_dictionary_documentation.py -v
git clone https://github.com/ArazSaieArasi3/riskium.wiki.git build/actual-wiki
python tools/publication/dictionary_documentation.py --output build/site --verify-wiki build/actual-wiki --receipt build/live-dictionary.json
```

The new Pages publisher checks source-transition boundaries, model-derived sources and all local HTML routes/fragments before deployment. All older publishers retain their exact historical source guards, preventing competing deployment. A current-source/main check precedes deployment. Native Wiki is committed independently and read back; this workflow does not grant a repository token permission to write Wiki.

Acceptance requires every deployed byte to match the built site, every expected Wiki file to match its generated projection, and zero broken internal HTML links/fragments across current pages and frozen snapshots. External repository links must point to existing source paths; no term equivalence is fabricated.

The dictionary content source is pinned to `20b2983352d2a6491600fcdbd765259d3da456c2`, separately from subsequent audit-tool revisions. The builder rejects changes to that source's model, dossiers, dictionary generator or SVGs. This keeps the qualified Wiki projection and source links stable when only an audit tool changes. Updating dictionary content requires an explicit new content binding and renewed publication checks. HTTP verification checks all public artifacts; `.nojekyll` remains hash-bound in the build inventory but is an unserved deployment marker, not a reader route.
