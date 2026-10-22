# Documentation publication

The Riskium portal follows the reading structure selected for OntoSPK: overview, sidebar guide, conceptual reference, WIDOCO OWL reference, evaluation, explorer and downloads. Original portal code is licensed under MIT; generated original scientific content uses CC BY 4.0. Bundled WIDOCO template resources retain the notices in `docs/THIRD-PARTY-DOCUMENTATION.txt` and the Apache license distributed beside it.

All semantic inputs are read with `git show` from `cfb85905ab37549c7090f00a41ca62cdd3364ab5`, verified against tag `v0.3.1-rc.1`. Current guide sources are hashed separately. This is post-release documentation; neither the historical archive nor the published tag changes. A future semantic version needs a deliberately separate route and source decision.

```sh
python3 -m venv .venv-docs
.venv-docs/bin/pip install -r tools/publication/requirements.txt
.venv-docs/bin/python tools/build_reference.py
.venv-docs/bin/python tools/build_reference.py --check
.venv-docs/bin/python tools/publication/audit_portal.py --write
```

WIDOCO is a separate, optional generation step. Use Java 17 and the official [WIDOCO 1.4.25 jar](https://github.com/dgarijo/Widoco/releases/download/v1.4.25/widoco-1.4.25-jar-with-dependencies_JDK-17.jar), SHA-256 `be57a270fffb91e55810fa308717e704a44e2e7c027a3d68125a49da6c8b4e2b`:

```sh
.venv-docs/bin/python tools/publication/run_widoco.py --jar /path/to/widoco-1.4.25-jar-with-dependencies_JDK-17.jar
.venv-docs/bin/python tools/publication/audit_portal.py --write
```

The postprocessor removes remote badges and runtime scripts, generates static Markdown and contents, corrects display metadata and the upstream duplicate section ID, retains generator credits and adds navigation. It copies the exact Turtle and exports graph-isomorphic RDF/XML, JSON-LD and N-Triples from the original graph, rather than distributing a WIDOCO/OWL API rewrite as the original ontology. The tool receipt pins the configuration, postprocessor, jar and published WIDOCO file hashes. The jar is not checked in.

The local explorer follows asserted named class parents/children and object-property domain/range links. Its full inventory remains usable without JavaScript; a small original script filters visible text locally. There is no upload, network query, analytics, storage, or inferred closure. WIDOCO itself has no runtime script after post-processing. External source and citation hyperlinks are intentional user navigation.

The audit checks every local HTML target and fragment, input/output hashes, exact conceptual inventory, actual OWL neighborhoods, download hashes, all four RDF serializations, notices and runtime asset policy. These are documentation and serialization checks, not HermiT/SHACL execution or independent semantic validation. Browser filtering, keyboard, responsive rendering and deployed readback need separate evidence.
