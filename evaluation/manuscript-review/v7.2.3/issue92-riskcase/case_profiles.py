"""Caller-selected explicit task checks; never infer universal case admission."""
from copy import deepcopy
from pathlib import Path
import re
from rdflib import Graph,Namespace,URIRef,BNode,Literal,RDF,RDFS,OWL,XSD
from pyshacl import validate
RISK=Namespace('https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#')
APP=Namespace('https://github.com/ArazSaieArasi3/riskium/profiles/riskcase/0.1.0#')
SH=Namespace('http://www.w3.org/ns/shacl#')
TASKS=('analytical-case','operational-register')
RESERVED=tuple(map(str,(RISK,APP,RDF,RDFS,OWL,SH,XSD)))
FORBIDDEN_SCHEMA=(RDFS.subClassOf,RDFS.subPropertyOf,RDFS.domain,RDFS.range,OWL.equivalentClass,OWL.equivalentProperty,OWL.imports)

def compile_request(raw,focus,task):
 if task not in TASKS:raise ValueError('Unsupported externally selected task')
 if not isinstance(focus,(list,tuple)) or not focus or len(set(focus))!=len(focus):raise ValueError('A nonempty distinct external focus is required')
 if any(not isinstance(x,(URIRef,BNode)) for x in focus):raise ValueError('Case focus must be an RDF resource')
 if any(isinstance(x,URIRef) and (not re.fullmatch(r'[A-Za-z][A-Za-z0-9+.-]*:[^\s<>"{}|^`\\]+',str(x)) or str(x).startswith(RESERVED)) for x in focus):raise ValueError('Malformed or reserved case identifier')
 for s,p,o in raw:
  if p in FORBIDDEN_SCHEMA:raise ValueError('Instance input cannot supply schema/import axioms')
  if p in (APP.requestCase,APP.requestedTask) or str(p).startswith(str(APP)+'focus-'):raise ValueError('Input cannot choose its profile or external selectors')
  if p in (OWL.sameAs,OWL.differentFrom) and any(str(x).startswith(RESERVED) for x in (s,o)):raise ValueError('Instance identity cannot rewrite reserved vocabulary')
  if str(s).startswith(str(APP)+'request-'):raise ValueError('Input cannot overwrite trusted request identifiers')
 data=Graph();shapes=Graph()
 for t in raw:data.add(t)
 for pre,ns in [('risk',RISK),('app',APP),('sh',SH)]:shapes.bind(pre,ns)
 def prop(shape,key,path,lo=None,hi=None,cls=None,kind=None):
  p=URIRef(str(shape)+'-'+key);shapes.add((shape,SH.property,p));shapes.add((p,SH.path,path));shapes.add((p,RDF.type,SH.PropertyShape))
  if lo is not None:shapes.add((p,SH.minCount,Literal(lo)))
  if hi is not None:shapes.add((p,SH.maxCount,Literal(hi)))
  if cls:shapes.add((p,SH['class'],cls))
  if kind:shapes.add((p,SH.nodeKind,kind))
  return p
 for i,case in enumerate(focus):
  request=APP['request-'+str(i)];shape=APP['RequestShape-'+str(i)];cs=APP['CaseShape-'+str(i)]
  data.add((request,APP.requestCase,case));data.add((request,APP.requestedTask,Literal(task)))
  shapes.add((shape,RDF.type,SH.NodeShape));shapes.add((shape,SH.targetNode,request))
  p=prop(shape,'case',APP.requestCase,1,1,RISK['RKM-X01'],SH.IRI);shapes.add((p,SH.node,cs));shapes.add((cs,RDF.type,SH.NodeShape))
  prop(cs,'context',RISK['RX-001'],1,cls=RISK['RKM-C002'],kind=SH.IRI)
  prop(cs,'objective',RISK['RX-003'],1,cls=RISK['RKM-X02'],kind=SH.IRI)
  if task=='operational-register':
   ep=prop(cs,'entry',APP.entry,1,1,RISK['RKM-C022'],SH.IRI);es=APP['EntryShape-'+str(i)];shapes.add((es,RDF.type,SH.NodeShape));shapes.add((ep,SH.node,es))
   rp=prop(es,'records-case',RISK['R-01'],1,1,RISK['RKM-X01'],SH.IRI);shapes.add((rp,SH.hasValue,case))
   ap=prop(cs,'approval',APP.approved,1,1);shapes.add((ap,SH.datatype,XSD.boolean));shapes.add((ap,SH.hasValue,Literal(True)))
   prop(cs,'approval-source',APP.approvalSource,1,1,kind=SH.IRI)
 return data,shapes

def evaluate(raw,focus,task):
 data,shapes=compile_request(raw,focus,task)
 conforms,report,_=validate(data,shacl_graph=shapes,inference='none',advanced=False,do_owl_imports=False)
 findings=[]
 for n in report.subjects(RDF.type,SH.ValidationResult):
  findings.append({'focus':str(report.value(n,SH.focusNode)),'shape':str(report.value(n,SH.sourceShape)),'component':str(report.value(n,SH.sourceConstraintComponent)),'message':str(report.value(n,SH.resultMessage))})
 # sh:node wrappers are summary results; inspect the retained detail graph as well.
 components={r['component'] for r in findings};terminal=components-{str(SH.NodeConstraintComponent)}
 missing_approval=task=='operational-register' and any(not list(raw.objects(c,APP.approved)) for c in focus)
 denied=task=='operational-register' and any((c,APP.approved,Literal(False)) in raw for c in focus)
 # hasValue also reports for a missing approval value. Distinguish that from an explicit denial or malformed field.
 if conforms:status='READY_FOR_SELECTED_TASK'
 elif denied:status='NOT_ELIGIBLE_FOR_SELECTED_TASK'
 elif terminal <= {str(SH.MinCountConstraintComponent),str(SH.HasValueConstraintComponent)} and all(x['shape'].endswith('-approval') and missing_approval for x in findings if x['component']==str(SH.HasValueConstraintComponent)):status='INCOMPLETE_FOR_SELECTED_TASK'
 else:status='NOT_ELIGIBLE_FOR_SELECTED_TASK'
 return {'task':task,'conforms':bool(conforms),'status':status,'approval':'UNKNOWN' if missing_approval else ('DENIED' if denied else ('RECORDED' if task=='operational-register' else 'NOT_REQUIRED')),'case_identity_deleted':False,'findings':findings},data,shapes,report
