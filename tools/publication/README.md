# Documentation publication

The Riskium portal follows the reading structure selected for OntoSPK: overview, sidebar guide, conceptual reference, WIDOCO OWL reference, evaluation, explorer and downloads. Original portal code is licensed under MIT; generated original scientific content uses CC BY 4.0. Bundled WIDOCO template resources retain the notices in `docs/THIRD-PARTY-DOCUMENTATION.txt` and the Apache license distributed beside it.

Current semantic inputs are read with `git show` from `8afe169968b5c1396c02834dbc499af691b894b4`, verified against published tag `v0.3.1`. Explanations are listed once in `guide-registry.json` and projected to both `docs/current/guide/` and `docs/wiki/`. Source hashes are separate from model identity. The original rc.1 website stays byte-identical to the dated source in `pages-registry.json`.

`current/` is mutable; `versions/index.html` lists separately registered frozen snapshots. A documentation snapshot can describe model 0.3.1 without creating another ontology/source release. Registration pins an exact source tree and output file hashes. The old entry/bytes cannot be removed or replaced; a changed presentation renderer requires a new explicit policy/version rather than rewriting an existing snapshot. A changed existing source file links to current source, not an older commit merely because the path existed there.

```sh
python3 -m venv .venv-docs
.venv-docs/bin/pip install -r tools/publication/requirements.txt
.venv-docs/bin/python tools/build_reference.py
.venv-docs/bin/python tools/build_reference.py --check
.venv-docs/bin/python tools/publication/audit_portal.py --write
.venv-docs/bin/python tools/publication/build_versioned_site.py --output build/site --previous-ref HEAD^
.venv-docs/bin/python -m unittest discover -s tests -p test_documentation_routes.py -v
```

WIDOCO is a separate, optional generation step. Use Java 17 and the official [WIDOCO 1.4.25 jar](https://github.com/dgarijo/Widoco/releases/download/v1.4.25/widoco-1.4.25-jar-with-dependencies_JDK-17.jar), SHA-256 `be57a270fffb91e55810fa308717e704a44e2e7c027a3d68125a49da6c8b4e2b`:

```sh
.venv-docs/bin/python tools/publication/run_widoco.py --jar /path/to/widoco-1.4.25-jar-with-dependencies_JDK-17.jar
.venv-docs/bin/python tools/publication/audit_portal.py --write
```

The postprocessor removes remote badges and runtime scripts, generates static Markdown and contents, corrects display metadata and the upstream duplicate section ID, retains generator credits and adds navigation. It copies the exact Turtle and exports graph-isomorphic RDF/XML, JSON-LD and N-Triples from the original graph, rather than distributing a WIDOCO/OWL API rewrite as the original ontology. The tool receipt pins the configuration, postprocessor, jar and published WIDOCO file hashes. The jar is not checked in.

The local explorer follows asserted named class parents/children and object-property domain/range links. Its full inventory remains usable without JavaScript; a small original script filters visible text locally. There is no upload, network query, analytics, storage, or inferred closure. WIDOCO itself has no runtime script after post-processing. External source and citation hyperlinks are intentional user navigation.

The audit checks every local HTML target and fragment, input/output hashes, exact conceptual inventory, actual OWL neighborhoods, download hashes, all four RDF serializations, notices and runtime asset policy. These are documentation and serialization checks, not HermiT/SHACL execution or independent semantic validation. Browser filtering, keyboard, responsive rendering and deployed readback need separate evidence.

Only after the current source is committed, register a new snapshot with `python tools/publication/freeze_documentation.py --label v0.3.1 --source EXACT_SOURCE_SHA --documentation-version 0.1.0`, then rebuild/index/check. Repeating an existing label is rejected. This is an explicit first documentation registration, not permission to replace old snapshots or publish a new source tag.

The Pages workflow is triggered only by successful main-repository, main-branch documentation CI and checks out its exact `head_sha`. It builds the complete site and root source/file manifest before deploying. Configure repository Pages source as GitHub Actions, rather than branch deployment. Publishing Wiki requires a separate actual Git push and fresh read-only clone; files matching the generated projection are necessary, and rendered navigation/reading is checked separately. New documentation versions must not imply independent semantic acceptance or rewrite historical science.
