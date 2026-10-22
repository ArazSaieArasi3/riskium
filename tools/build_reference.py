"""Generate an English static reference from the current Riskium model."""
from pathlib import Path
import hashlib,json,html
ROOT=Path(__file__).resolve().parents[1]
model_path=ROOT/'ontology/riskium-model.json'
m=json.loads(model_path.read_text())
coverage=json.loads((ROOT/'evaluation/shacl/coverage-status.json').read_text())
if coverage['source_sha256']!=hashlib.sha256(model_path.read_bytes()).hexdigest() or coverage['baseline']!=359:
    raise SystemExit('SHACL coverage ledger does not match model or fixed denominator')
outcomes=coverage['outcomes']
hermit=json.loads((ROOT/'evaluation/hermit/report.json').read_text())
if hermit['model_version']!=m['version'] or hermit['inputs']['owl_turtle_sha256']!=hashlib.sha256((ROOT/'ontology/derived/riskium.owl.ttl').read_bytes()).hexdigest():
    raise SystemExit('HermiT receipt does not match model version or OWL export')
reasoned=hermit['coverage']
e=lambda value:html.escape(str(value),quote=True)
body=['<h1>Riskium reference</h1>','<p>Conceptual design '+e(m['version'])+'. This generated view refers to the structured design; a native exchange has schema and SDK checks documented in the evaluation record. A bounded typed-core OWL mapping and scoped HermiT run are recorded; complete semantic verification remains open.</p>','<nav><a href="../../README.md">Repository guide</a> · <a href="../../ontology/riskium-model.json">Model source</a> · <a href="../../diagrams/selected-view.svg">Selected view</a> · <a href="../../requirements/ontology-requirements.md">Requirements</a> · <a href="../../evaluation/README.md">Evaluation</a> · <a href="../../evaluation/hermit/report.md">HermiT report</a> · <a href="../../evaluation/shacl/coverage-status.md">SHACL ledger</a> · <a href="../../evaluation/c14-boundary-review.md">C-14 review</a> · <a href="../first-release-profile.md">Release gates</a></nav>','<p>80 catalog concepts include 77 typed core concepts and three optional boundaries. One imported anchor is recorded separately. HermiT passed '+e(sum(x['status']=='PASS' for x in hermit['cases']))+' executed cases covering '+e(reasoned['outcomes']['PASS'])+' of '+e(reasoned['baseline_obligations'])+' reasoner obligations; '+e(reasoned['outcomes']['NOT_RUN'])+' constraint routes remain unexecuted by HermiT. SHACL module coverage: '+e(outcomes.get('PASS',0))+' scoped PASS, '+e(outcomes.get('PARTIAL',0))+' PARTIAL and '+e(outcomes.get('NOT_RUN',0))+' NOT_RUN of '+e(coverage['baseline'])+' obligations. These figures are not complete semantic validation.</p>','<label>Filter reference <input id="filter" type="search" placeholder="Concept, relation or constraint"></label>']
body.append('<h2>Domains</h2><ul>')
for d in m['domains']:body.append('<li><b>'+e(d['title'])+'</b>: '+e(d['definition'])+'</li>')
body.append('</ul><h2>Concepts</h2>')
for c in m['concepts']:
    body.append('<article class="entry" id="'+e(c['id'])+'"><h3>'+e(c['display_title'])+'</h3><p>'+e(c['definition'])+'</p><p class="meta">'+e(c['id'])+' · '+e(c['domain'])+' · '+e(c['scope_layer'])+' · '+e(c['ontouml_stereotype'] or 'untyped boundary')+'</p></article>')
body.append('<h2>Relations</h2><div class="scroll"><table><thead><tr><th>Relation</th><th>Source</th><th>Source-end count</th><th>Target</th><th>Target-end count</th><th>Meaning</th></tr></thead><tbody>')
for r in m['associations']:
    body.append('<tr class="entry"><td>'+e(r['predicate'])+'<br>'+e(r['id'])+'</td><td>'+e(r['source_title'])+'</td><td>'+e(r['source_end_cardinality'])+'</td><td>'+e(r['target_title'])+'</td><td>'+e(r['target_end_cardinality'])+'</td><td>'+e(r['rationale'])+'</td></tr>')
body.append('</tbody></table></div><h2>Generalizations</h2><ul>')
names={c['id']:c['display_title'] for c in m['concepts']+m['imported_types']}
for g in m['generalizations']:body.append('<li class="entry">'+e(names[g['specific']])+' is a '+e(names[g['general']])+'.</li>')
body.append('</ul><h2>Interpretation constraints</h2>')
for c in m['constraints']:body.append('<article class="entry"><h3>'+e(c['title'])+'</h3><p>'+e(c['statement'])+'</p><p class="meta">'+e(c['id'])+'</p></article>')
body.append('<footer>Generated from the version-controlled Riskium design. The source model owns definitions; this reference is a derived view.</footer>')
doc='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Riskium reference</title><style>body{font:16px/1.65 system-ui,sans-serif;color:#203141;max-width:1160px;margin:40px auto;padding:0 24px}h1{font-size:36px}h2{margin-top:42px}a{color:#17658a}nav{margin:22px 0}article{border-bottom:1px solid #dce3e8;padding:8px 0}.meta,footer{color:#536778;font-size:13px}table{border-collapse:collapse;font-size:14px}td,th{border:1px solid #dce3e8;padding:10px;text-align:left;vertical-align:top}th{background:#edf3f6}.scroll{overflow:auto}input{font:inherit;padding:8px}footer{margin-top:40px}</style></head><body>'+''.join(body)+'<script>document.getElementById("filter").addEventListener("input",function(){const q=this.value.toLowerCase();document.querySelectorAll(".entry").forEach(function(el){el.hidden=!el.textContent.toLowerCase().includes(q);});});</script></body></html>'
p=ROOT/'docs/site/index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(doc+'\n')
print(json.dumps({'reference':p.relative_to(ROOT).as_posix(),'concepts':len(m['concepts']),'relations':len(m['associations']),'constraints':len(m['constraints'])}))
