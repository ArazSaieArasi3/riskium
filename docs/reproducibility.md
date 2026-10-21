# Reproduce the current checks

Use Python 3.12 or a compatible Python 3 installation. The current validation and reference build use the standard library.

From the repository root:

```sh
python3 tools/validate_model.py
python3 -m unittest discover -s tests -v
python3 tools/build_reference.py
```

To browse the generated reference locally:

```sh
python3 -m http.server 8000
```

Open `http://localhost:8000/docs/site/`. The generated reference links to the model and conceptual views. Local browsing does not establish a live Pages deployment.

The formal HermiT and SHACL suites are not implemented in this snapshot. Their dependency versions and clean-environment reproduction commands will be recorded when the formal encodings and fixtures exist.
