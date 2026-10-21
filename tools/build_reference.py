"""Generate an English static reference from the current Riskium model."""
from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/'ontology/riskium-model.json').read_text())
e=lambda value:html.escape(str(value),quote=True)
body=['<h1>Riskium reference</h1>','<p>Conceptual design '+e(m['version'])+'. This generated view refers to the structured design; a native exchange has schema and SDK checks documented in the evaluation record. Complete semantic verification and OWL formalization remain pending.</p>','<nav><a href="../../README.md">Repository guide</a> · <a href="../../ontology/riskium-model.json">Model source</a> · <a href="../../diagrams/selected-view.svg">Selected view</a> · <a href="../../requirements/ontology-requirements.md">Requirements</a> · <a href="../../evaluation/README.md">Evaluation</a></nav>','<p>80 catalog concepts include 77 typed core concepts and three optional boundaries. One imported anchor is recorded separately. HermiT and SHACL execution is planned.</p>','<label>Filter reference <input id="filter" type="search" placeholder="Concept, relation or constraint"></label>']
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
