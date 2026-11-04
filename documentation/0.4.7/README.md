# Current article-companion reader 0.4.7

This maintained reader accompanies the selected v0.3.8 source package. It uses the qualified dictionary content from reader 0.4.6, updates publication/artifact/article/work-plan routes, and preserves every frozen snapshot. Current article 7.2.3 remains author-held; model/OWL 0.3.1 and SQL 0.9.0/schema 10 are unchanged.

The publication JSON is a later observation, not part of the prepublication freeze. Without a verified publication record the builder emits a prepared-state preview, which must not be deployed as a published release. Actual publication promotes the separate root landing and triggers the maintained reader workflow. Native Wiki is committed and independently cloned/read back separately. Original technical guide bodies are explicitly marked as retained historical material rather than relabelled with new outcomes.

Build: `python tools/publication/v038_documentation.py --output build/site --wiki-output build/wiki`. Readback: add `--verify-wiki PATH_TO_FRESH_WIKI --receipt build/channels.json`. All public HTTP bodies and expected Wiki bodies must match; `.nojekyll` remains an unserved build marker. The prior 80 concept Wiki pages retain exact dictionary bytes; 21 guide pages and two navigation files carry the updated reader context.
