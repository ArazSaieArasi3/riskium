# v0.3.9 coordinated delivery

This publication adapter exposes the qualified scientific model 0.3.2 through
reader 0.4.9. The six frozen package assets remain byte-identical to actual CI
42776380967 at source commit ce0baefa3495d1bc3b42f56ad578154d5bc4f178.

The adapter verifies all 1,213 selected bindings before rendering. It changes
publication labels and routes, not authored scientific definitions. It checks
current and versioned local links, preserves tracked historical release
snapshots, labels old model 0.3.1 visualizations, and emits canonical Wiki
bodies from the same inputs. Historical documentary comparisons retain their
0.3.1 population and interpretation boundary.

Build with the pinned `tools/publication/requirements.txt` dependencies:

```sh
python tools/releases/v039/delivery/build_reader.py --output build/site --wiki-output build/wiki
```

After publication, clone/fetch the actual native Wiki and independently compare
all served Pages files and all Wiki file hashes:

```sh
python tools/releases/v039/delivery/build_reader.py --output build/site --wiki-output /path/to/actual-wiki --verify-live --receipt live-channels.json
```

The delivery commit differs from the frozen scientific source commit. Public
download and live-channel observations are appended under
`evaluation/releases/v0.3.9/`; historical freeze receipts are not rewritten.
The author-held article remains 7.2.21 with its own source-bound results.
