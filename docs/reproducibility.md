# Reproduce the current checks

Use Python 3.12 or a compatible Python 3 installation. The conceptual-model, coverage and reference builders use the standard library. The OWL syntax and mapping regression tests require the pinned RDFLib package.

From the repository root:

```sh
python3 tools/validate_model.py
python3 tools/review_coverage.py
python3 tools/build_reference.py
```

To reproduce the OWL export and the complete regression suite in an isolated environment:

```sh
python3 -m venv .venv-owl
.venv-owl/bin/pip install -r tools/requirements-owl.txt
python3 tools/build_owl.py --check
.venv-owl/bin/python -m unittest discover -s tests -v
```

The [OWL review](../evaluation/owl-mapping-review.md) describes the mapping and its limits. Parsing the RDF and checking source allocation do not execute HermiT or SHACL.

To browse the generated reference locally:

```sh
python3 -m http.server 8000
```

Open `http://localhost:8000/docs/site/`. The generated reference links to the model and conceptual views. Local browsing does not establish a live Pages deployment.

The coverage review verifies source allocation, planned constraint routes and expected fixture contracts. It detects a stale or missing stored review; regeneration with `python3 tools/review_coverage.py --write` is appropriate only after reviewing an intentional contract change.

The optional [native-exchange checks](../evaluation/native-model-review.md) use a pinned schema, Python validation environment and official SDK versions. Their dependency installation and reproduction commands are documented separately; the standard-library checks above remain available without those dependencies.

The [HermiT execution report](../evaluation/hermit/report.md) and exact [premise](../evaluation/hermit/premise.rdf) record the scoped reasoner run. To rerun the mapped ontology and regenerate the JSON and Markdown evidence:

```sh
python3 -m venv .venv-hermit
.venv-hermit/bin/pip install -r tools/requirements-hermit.txt
.venv-hermit/bin/python tools/run_hermit.py
```

The installed Owlready2 package supplies the pinned HermiT jar; the jar itself is not copied into this repository. The script verifies its version and records its SHA-256 digest. Its baseline percentage uses the 295 predeclared HermiT-related obligations; supplemental inference and mutation cases have their own counts. SHACL profiles and explicit-data fixtures remain open in issue #5.
