"""Build an isolated, additive EvidenceItem dependency candidate; never rewrite production artifacts."""
from pathlib import Path
from copy import deepcopy
from hashlib import sha256
import json,sys
from rdflib import Graph,Namespace,URIRef,Literal
from rdflib.namespace import RDF,RDFS,OWL

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'tools'))
from build_native import build
from build_owl import restriction

VERSION='0.3.2-evidence-use.1'
RISK=Namespace('https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#')
EU=Namespace('https://github.com/ArazSaieArasi3/riskium/candidates/issue93/evidence-use#')
ONTO=URIRef('https://github.com/ArazSaieArasi3/riskium/ontologies/riskium')
FROZEN_SHA='4a052bb0b7321e5209417c69e96644089aa7dba1734cce4a70e5223f2ebbaf59'
def digest(p):return sha256(Path(p).read_bytes()).hexdigest()
def dumps(x):return json.dumps(x,ensure_ascii=False,indent=2)+'\n'

def candidate_model():
 source=ROOT/'ontology/riskium-model.json'
 assert digest(source)==FROZEN_SHA
 base=json.loads(source.read_text()); m=deepcopy(base)
 assert not any(c['id']=='RKM-C075' for c in m['concepts'])
 m['version']=VERSION;m['date_local']='2026-11-08'
 m['publication_profile'].update(source_design_version=VERSION,export_revision='2026-11-08',representation='Isolated EvidenceItem dependency candidate; production baseline and historical receipts unchanged')
 c=deepcopy(next(c for c in m['concepts'] if c['id']=='RKM-C052'))
 c.update(id='RKM-C075',title='EvidenceUseRelator',display_title='Evidence Use Relator',domain='Risk Evidence',domain_id='D09',
  definition='A context-qualified evidential-use relationship connecting a qualified reference and a distinct information artifact used as support, challenge or context in an analysis. Its grounding concerns that use, not the truth of the referenced claim.',
  identity_supplier='RKM-C075',identity_basis='One grounded use episode qualified by its reference, evidence artifact, analysis context and evidential purpose; different descriptions of that same use do not supply new identities.',
  typing_rationale='Relator candidate: a grounded evidential-use relationship, with two distinct mediated documentary participants. The information describing a proposed use is not automatically an instance of this relator.',
  verification_status='ISOLATED_CANDIDATE; scoped source, OWL and explicit-data tests recorded separately')
 m['concepts'].append(c)
 refrole=deepcopy(next(x for x in m['concepts'] if x['id']=='RKM-C066'))
 refrole.update(id='RKM-C076',title='EvidenceReferenceRole',display_title='Evidence Reference Role',definition='A qualified EvidenceReference participating in an actual grounded evidential-use relationship. The reference retains documentary identity when it is only a record of a proposed use.',identity_basis='Inherits InformationArtifact identity through EvidenceReference; role membership depends on grounded evidential use.',typing_rationale='Anti-rigid participation of a documentary reference, distinct from merely recording a proposed use.',verification_status='ISOLATED_CANDIDATE; scoped tests recorded separately')
 m['concepts'].append(refrole)
 gg=deepcopy(m['generalizations'][-1]);gg.update(id='GE-001',specific='RKM-C076',general='RKM-C065',status='ISOLATED_CANDIDATE',first_concept='Evidence Reference Role',first_stereotype='«role»',second_concept='Evidence Reference',second_stereotype='«subkind»');m['generalizations'].append(gg)
 item=next(c for c in m['concepts'] if c['id']=='RKM-C066')
 item['typing_rationale']='Anti-rigid documentary role founded through mandatory mediation by EvidenceUseRelator. The artifact retains InformationArtifact identity when not used as evidence.'
 template=next(r for r in m['associations'] if r['id']=='R-56')
 for rid,predicate,target,target_title,stereotype in [
  ('RE-001','mediatesEvidenceItem','RKM-C066','Evidence Item','mediation'),
  ('RE-002','mediatesEvidenceReference','RKM-C076','Evidence Reference Role','mediation'),
  ('RE-003','groundedInUseRecord','RKM-C014','Information Artifact',None)]:
  r=deepcopy(template)
  r.update(id=rid,source='RKM-C075',source_title='Evidence Use Relator',source_stereotype='«relator»',
   target=target,target_title=target_title,target_stereotype='«role»' if target in {'RKM-C066','RKM-C076'} else ('«subkind»' if target=='RKM-C065' else '«kind»'),
   predicate=predicate,stereotype=stereotype,relation_stereotype='«mediation»' if stereotype else 'None — ordinary association',
   source_end_cardinality='1..*' if stereotype else '0..*',target_end_cardinality='1',
   status='ISOLATED_EVIDENCE_USE_CANDIDATE',basis='Explicitly grounded use; the source pointer RX-021 remains an ordinary documentary relation.',
   rationale='Each use has one named evidence item, one distinct qualified reference and a grounding record. Different uses of the same artifact are permitted.',
   multiplicity_scope='Selected evidence-use candidate profile; incomplete citations remain information/staging, without asserting the role or actual-use relator.')
  m['associations'].append(r)
 m['constraints'].append(dict(id='C-26',title='Grounded evidential use',status='ISOLATED_CANDIDATE_CONSTRAINT',statement='An EvidenceUseRelator mediates a distinct EvidenceItem and EvidenceReferenceRole, has a grounding use record, and is qualified by context and purpose (support, challenge or context). Its reference points to that item and records that context. An ungrounded citation remains information. Use as evidence does not establish claim truth. Duplicate descriptions of one grounded use preserve its identity.'))
 dom=next(d for d in m['domains'] if d['id']=='D09')
 dom['concept_ids'].extend(['RKM-C075','RKM-C076']);dom['concept_titles'].extend(['Evidence Use Relator','Evidence Reference Role'])
 dom['concept_count']+=2;dom['formal_core_count']+=2
 assert len(m['concepts'])==82 and len(m['associations'])==137 and len(m['constraints'])==26
 return base,m

SHAPES='''@prefix risk: <https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#> .
@prefix eu: <https://github.com/ArazSaieArasi3/riskium/candidates/issue93/evidence-use#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

eu:EvidenceItemShape a sh:NodeShape ; sh:targetClass risk:RKM-C066 ;
 sh:property [ sh:path [ sh:inversePath risk:RE-001 ] ; sh:minCount 1 ; sh:class risk:RKM-C075 ; sh:nodeKind sh:IRI ] .
eu:EvidenceReferenceShape a sh:NodeShape ; sh:targetClass risk:RKM-C076 ;
 sh:property [ sh:path [ sh:inversePath risk:RE-002 ] ; sh:minCount 1 ; sh:class risk:RKM-C075 ; sh:nodeKind sh:IRI ] .
eu:EvidenceUseShape a sh:NodeShape ; sh:targetClass risk:RKM-C075 ;
 sh:nodeKind sh:IRI ;
 sh:property [ sh:path risk:RE-001 ; sh:minCount 1 ; sh:maxCount 1 ; sh:class risk:RKM-C066 ; sh:nodeKind sh:IRI ; sh:disjoint risk:RE-002 ] ;
 sh:property [ sh:path risk:RE-002 ; sh:minCount 1 ; sh:maxCount 1 ; sh:class risk:RKM-C076 ; sh:nodeKind sh:IRI ] ;
 sh:property [ sh:path risk:RE-003 ; sh:minCount 1 ; sh:maxCount 1 ; sh:class risk:RKM-C014 ; sh:nodeKind sh:IRI ] ;
 sh:property [ sh:path eu:context ; sh:minCount 1 ; sh:maxCount 1 ; sh:class risk:RKM-C014 ; sh:nodeKind sh:IRI ] ;
 sh:property [ sh:path eu:purpose ; sh:minCount 1 ; sh:maxCount 1 ; sh:datatype xsd:string ; sh:in ( "support" "challenge" "context" ) ] ;
 sh:sparql [ sh:message "The use reference must point to its item and record its analysis context." ; sh:select """
 PREFIX risk: <https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#>
 PREFIX eu: <https://github.com/ArazSaieArasi3/riskium/candidates/issue93/evidence-use#>
 SELECT $this WHERE {
  $this risk:RE-001 ?item ; risk:RE-002 ?ref ; eu:context ?context .
  FILTER (NOT EXISTS { ?ref risk:RX-021 ?item } || NOT EXISTS { ?ref risk:R-68 ?context })
 }""" ] .
'''

SVG='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 480" width="1000" height="480">
<rect width="1000" height="480" fill="white"/><g stroke="#45515b" stroke-width="2" fill="#e6eaf0">
<path d="M260 245H440M560 245H740M500 290V365" fill="none"/>
<rect x="40" y="200" width="220" height="90"/><rect x="740" y="200" width="220" height="90"/>
<rect x="390" y="200" width="220" height="90" fill="#e5eef8"/>
<rect x="390" y="365" width="220" height="80" fill="#eee8f4"/>
<rect x="40" y="30" width="220" height="85" fill="#eee8f4"/>
<path d="M150 200V133" fill="none"/><path d="M150 115l-10 18h20z" fill="white"/>
</g><g font-family="Arial, sans-serif" fill="#18232d" text-anchor="middle">
<g font-size="17"><text x="150" y="60">«kind»</text><text x="150" y="229">«role»</text><text x="500" y="229">«relator»</text><text x="850" y="229">«role»</text><text x="500" y="395">«kind»</text></g>
<g font-size="19" font-weight="bold"><text x="150" y="89">InformationArtifact</text><text x="150" y="258">EvidenceItem</text><text x="500" y="258">EvidenceUseRelator</text><text x="850" y="258" font-size="17">EvidenceReferenceRole</text><text x="500" y="424">InformationArtifact</text></g>
<g font-size="14"><text x="325" y="206">«mediation»</text><text x="675" y="206">«mediation»</text><text x="282" y="237">1</text><text x="366" y="237">1..*</text><text x="637" y="237">1..*</text><text x="720" y="237">1</text><text x="518" y="314">0..*</text><text x="513" y="356">1</text><text x="630" y="340">groundedInUseRecord</text><text x="500" y="165">Two distinct mediated participants; context and purpose qualify each use.</text><text x="500" y="470">Isolated candidate. RX-021 remains an ordinary pointer; evidential use does not establish claim truth.</text></g></g></svg>'''

def render():
 base,m=candidate_model();mp=HERE/'candidate-model.json';mp.write_text(dumps(m))
 native=build(m,digest(mp));np=HERE/'candidate.ontouml.json';np.write_text(dumps(native))
 graph=Graph().parse(ROOT/'ontology/derived/riskium.owl.ttl',format='turtle')
 for pred in [OWL.versionIRI,RDFS.label,RISK.sourceDigest,RISK.nativeDigest,RISK.reviewDigest]:graph.remove((ONTO,pred,None))
 graph.add((ONTO,OWL.versionIRI,URIRef(str(EU).rstrip('#'))));graph.add((ONTO,RDFS.label,Literal('Riskium isolated EvidenceItem dependency candidate '+VERSION)))
 for pred,val in [(RISK.sourceDigest,digest(mp)),(RISK.nativeDigest,digest(np))]:graph.add((ONTO,pred,Literal(val)))
 graph.add((EU.purpose,RDF.type,OWL.DatatypeProperty));graph.add((EU.context,RDF.type,OWL.ObjectProperty))
 c=next(c for c in m['concepts'] if c['id']=='RKM-C075')
 graph.add((RISK[c['id']],RDF.type,OWL.Class));graph.add((RISK[c['id']],RDFS.label,Literal(c['title'])));graph.add((RISK[c['id']],RDFS.comment,Literal(c['definition'])))
 graph.add((RISK[c['id']],RISK.ontoumlStereotype,Literal('relator')))
 c=next(c for c in m['concepts'] if c['id']=='RKM-C076')
 graph.add((RISK[c['id']],RDF.type,OWL.Class));graph.add((RISK[c['id']],RDFS.label,Literal(c['title'])));graph.add((RISK[c['id']],RDFS.comment,Literal(c['definition'])));graph.add((RISK[c['id']],RDFS.subClassOf,RISK['RKM-C065']));graph.add((RISK[c['id']],RISK.ontoumlStereotype,Literal('role')))
 for r in m['associations'][-3:]:
  prop=RISK[r['id']];graph.add((prop,RDF.type,OWL.ObjectProperty));graph.add((prop,RDFS.label,Literal(r['predicate'])));graph.add((prop,RDFS.domain,RISK[r['source']]));graph.add((prop,RDFS.range,RISK[r['target']]))
  for inverse in [False,True]:
   text=restriction('risk:'+r['id'],'risk:'+r['source' if inverse else 'target'],r['source_end_cardinality' if inverse else 'target_end_cardinality'],inverse)
   if text:
    ttl='@prefix risk: <'+str(RISK)+'> . @prefix owl: <'+str(OWL)+'> . @prefix rdfs: <'+str(RDFS)+'> . @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n'
    graph+=Graph().parse(data=ttl+'risk:'+r['target' if inverse else 'source']+' rdfs:subClassOf '+text+' .',format='turtle')
 graph.add((RISK['RE-001'],OWL.propertyDisjointWith,RISK['RE-002']))
 graph.bind('risk',RISK);graph.bind('eu',EU);graph.serialize(HERE/'candidate.owl.ttl',format='turtle')
 (HERE/'evidence-use.shacl.ttl').write_text(SHAPES)
 (HERE/'evidence-use.svg').write_text(SVG)
 return m,native,graph

if __name__=='__main__':
 m,n,g=render();print(dumps({'candidate':VERSION,'concepts':len(m['concepts']),'associations':len(m['associations']),'generalizations':len(m['generalizations']),'constraints':len(m['constraints']),'native_elements':len(n['elements']),'owl_triples':len(g),'production_unchanged':digest(ROOT/'ontology/riskium-model.json')==FROZEN_SHA}))
