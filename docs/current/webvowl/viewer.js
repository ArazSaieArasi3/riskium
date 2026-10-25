/* Original Riskium shell, MIT. Fixed local data only; no editor/upload/converter. */
(() => {
  "use strict";
  const $ = (id) => document.getElementById(id);
  let graph, source, terms = [], selected;
  let valid = false, ready = false, initializing = true;
  const noop = () => {};
  function fail(error) {
    valid = false;
    $("status").textContent = "The graph could not be loaded. Use the text explorer; details are available in the browser console.";
    $("status").classList.add("error");
    console.error("Riskium WebVOWL:", error);
  }
  function markReady() {
    if (ready || !valid) return;
    const ids = [...document.querySelectorAll("#graph .node")].map(n => n.id).sort();
    const expected = source.class.map(n => n.id).sort();
    if (JSON.stringify(ids) !== JSON.stringify(expected)) { fail("Rendered class inventory differs from source"); return; }
    ready = true;
    document.body.dataset.graphReady = "true";
    $("status").textContent = `${source.metrics.classCount} classes · ${source.metrics.objectPropertyCount} object properties · ${source.metrics.propertyCount-source.metrics.objectPropertyCount} subclass links`;
    document.querySelectorAll(".toolbar button, #search").forEach(n => { n.disabled = false; });
    renderResults();
  }
  function selectTerm(term, move = true) {
    if (!term) return;
    selected = term.id;
    const box = $("details"); box.replaceChildren();
    const kind = document.createElement("p"); kind.className = "kind"; kind.textContent = term.kind;
    const title = document.createElement("h2"); title.textContent = term.label;
    const id = document.createElement("code"); id.textContent = term.id;
    const definition = document.createElement("p"); definition.textContent = term.comment || "Read the full conceptual and OWL references for this declaration.";
    box.append(kind, title, id, definition);
    if (term.domain) {
      const endpoints = document.createElement("p"); endpoints.textContent = `Asserted endpoints: ${term.domain} → ${term.range}`; box.append(endpoints);
    }
    const links = document.createElement("div"); links.className = "term-links";
    for (const [name, path] of [["Text neighborhood", "../explore/index.html"], ["Conceptual definition", "../reference/native/index.html"], ["WIDOCO term", "../widoco/index-en.html"]]) {
      const a = document.createElement("a"); a.textContent = name; a.href = path + "#" + encodeURIComponent(term.native_anchor); links.append(a);
    }
    box.append(links);
    document.querySelectorAll("#graph .selected").forEach(n => n.classList.remove("selected"));
    const node = document.getElementById(term.id); if (node && $("graph").contains(node)) node.classList.add("selected");
    if (move) {
      const target = graph.graphNodeElements().data().find(n => n.id() === term.id) || graph.graphLabelElements().find(n => n.property().id() === term.id);
      if (target && Number.isFinite(target.x) && Number.isFinite(target.y)) graph.zoomToElementInGraph(target);
    }
    renderResults();
  }
  function renderResults() {
    const query = $("search").value.trim().toLowerCase();
    const matches = terms.filter(t => `${t.id} ${t.label} ${t.comment}`.toLowerCase().includes(query));
    const shown = matches.slice(0, 30);
    $("results-status").textContent = `${matches.length} matching terms${matches.length > 30 ? "; showing first 30 — refine search" : ""}`;
    $("results").replaceChildren();
    for (const term of shown) {
      const b = document.createElement("button"); b.textContent = term.label; b.title = `${term.kind} · ${term.id}`;
      b.setAttribute("aria-pressed", String(selected === term.id)); b.addEventListener("click", () => selectTerm(term)); $("results").append(b);
    }
  }
  function resize() {
    if (!graph) return;
    const box = $("graph").getBoundingClientRect(); graph.options().width(box.width).height(box.height); graph.updateCanvasContainerSize();
  }
  async function start() {
    const response = await fetch("data/riskium.json", {credentials: "omit", cache: "no-cache"});
    if (!response.ok) throw new Error("Local graph request failed");
    source = await response.json();
    if (!source.class?.length || source.class.length !== source.metrics?.classCount || !source.property?.length || source.property.length !== source.metrics?.propertyCount) throw new Error("Empty/inconsistent graph inventory");
    const nodeIds = new Set(source.class.map(n => n.id));
    if (nodeIds.size !== source.class.length || source.propertyAttribute.some(p => !nodeIds.has(p.domain) || !nodeIds.has(p.range))) throw new Error("Unresolved or duplicate graph identifier");
    terms = source.riskiumSource.terms.slice().sort((a,b) => a.label.localeCompare(b.label));
    graph = webvowl.graph("#graph");
    const options = graph.options();
    // Core UI callbacks are explicitly adapted; the upstream application, editor,
    // ontology loader/converter and export modules are never bundled or started.
    options.loadingModule({successfullyLoadedOntology: () => valid, missingImportsWarning: () => false,
      setPercentValue: noop, setPercentMode: noop, setSuccessful: markReady, hideLoadingIndicator: noop,
      collapseDetails: noop, showWarningDetailsMessage: noop, setErrorMode: () => { if (!initializing) fail("Core parser/layout error"); },
      showErrorDetailsMessage: () => fail("Core parser/layout error")});
    options.ontologyMenu({append_bulletPoint: noop, append_message_toLastBulletPoint: noop});
    options.warningModule({closeFilterHint: noop, showFilterHint: noop, showEditorHint: noop});
    options.sidebar({clearOntologyInformation: noop, updateShowedInformation: noop});
    options.editSidebar({clearMetaObjectValue: noop, updateGeneralOntologyInfo: noop, updatePrefixUi: noop, updateElementWidth: noop, updateSelectionInformation: noop});
    options.searchMenu({requestDictionaryUpdate: noop, getSearchString: () => $("search").value});
    options.zoomSlider({updateZoomSliderValue: (v) => { $("zoom-value").textContent = `${Math.round(v*100)}%`; }});
    options.focuserModule({handle: noop}); options.pickAndPinModule({enabled: () => false});
    const literals = webvowl.modules.emptyLiteralFilter(); literals.enabled(true); options.literalFilter(literals);
    options.filterModules([literals]);
    options.selectionModules([{handle: element => { const term = terms.find(t => t.id === element.id()); if (term) selectTerm(term, false); }}]);
    options.drawPropertyDraggerOnHover(false); options.useAccuracyHelper(false);
    options.classDistance(190); options.charge(-750); options.gravity(0.035);
    resize(); options.data(source); graph.start(); initializing = false; valid = true; graph.load(); graph.setDefaultZoom(0.55);
    $("search").addEventListener("input", renderResults);
    $("search").addEventListener("keydown", event => { if (event.key === "Enter") { const match = $("results").querySelector("button"); if (match) match.click(); } });
    $("pause").addEventListener("click", () => { const paused = !graph.paused(); graph.paused(paused); $("pause").setAttribute("aria-pressed", String(paused)); $("pause").textContent = paused ? "Resume layout" : "Pause layout"; });
    $("zoom-in").addEventListener("click", () => graph.zoomIn());
    $("zoom-out").addEventListener("click", () => graph.zoomOut());
    $("reset").addEventListener("click", () => { graph.setDefaultZoom(0.55); graph.updateCanvasContainerSize(); });
    new ResizeObserver(resize).observe($("graph"));
    // The core marks layout completion asynchronously. This fallback also checks
    // actual SVG class identities; a successful fetch cannot certify an empty SVG.
    setTimeout(() => { if (!ready && valid) markReady(); }, 12000);
  }
  start().catch(fail);
})();
