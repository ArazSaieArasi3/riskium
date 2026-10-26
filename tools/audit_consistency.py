"""Join source-bound research traces without promoting historical acceptance."""
import argparse
from collections import Counter,defaultdict
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'evaluation/consistency'
BASE='caf58628a6b6a02508c644dbcb53d7e298b9b5a7'
REPO='https://github.com/ArazSaieArasi3/riskium'

def read(p):return json.loads((ROOT/p).read_text())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def encode(v):return json.dumps(v,indent=2,ensure_ascii=False)+'\n'
def require(v,m):
    if not v:raise ValueError(m)


def build():
    current_readme=(ROOT/'README.md').read_text()
    require('#33 is next' not in current_readme and 'reference enhancement #33, next SQL slice' not in current_readme,'Stale current navigation')
    require('#41' in current_readme and '#40' in current_readme,'Missing current release/correction route')
    model=read('ontology/riskium-model.json');trace=read('evaluation/traceability/ledger.json')
    formal=read('evaluation/formal-reference/register.json');scope=read('evaluation/owner-review/accepted-scope.json')
    manuscript=read('evaluation/manuscript-review/ledger.json');amend=read('evaluation/manuscript-review/v7.0.8/receipt.json')
    sql=read('evaluation/relational/correction/mapping-accounting.json');cor=read('evaluation/relational/correction/traceability.json')
    h=read('evaluation/hermit/report.json');s=read('evaluation/shacl/coverage-status.json')
    for doc in (trace,formal,cor):
        for p,digest in doc.get('input_sha256',{}).items():require(sha(p)==digest,'Stale trace input: '+p)
    for p,digest in amend['bindings_sha256'].items():require(sha(p)==digest,'Stale approved manuscript binding: '+p)
    require(model['version']==scope['model_version']==amend['model_version']=='0.3.1','Model version differs')
    require(amend['manuscript_version']=='7.0.8' and amend['orsd_revision']=='0.4.3','Manuscript/ORSD revision differs')
    require(h['coverage']['outcomes']=={'PASS':281,'NOT_RUN':14},'Historical HermiT states changed')
    require(s['outcomes']=={'PASS':341,'PARTIAL':1,'NOT_RUN':17},'Historical SHACL states changed')
    require(scope['independent_validation'] is False and scope['full_original_requirement_acceptance'] is False,'Acceptance promoted')
    require(read('evaluation/independent-review/responses.json')['initial_ratings']==[],'Independent review needs separate reviewed ingestion')
    source={r['id']:r for key in ('concepts','imported_types','associations','generalizations','constraints') for r in model[key]}
    require(len(source)==len(sql['rows'])==306,'Native source denominator differs')
    require(len(trace['rows'])==28 and len(manuscript['rows'])==65 and len(amend['changes'])==7 and len(scope['claims'])==12,'Trace/claim denominator differs')
    req_by_model=defaultdict(list)
    for r in trace['rows']:
        for item in r['model_elements']:
            require(item['id'] in source,'Dangling model trace '+item['id']);req_by_model[item['id']].append(r['id'])
    eng=defaultdict(list)
    for engine,receipt,ledger in [('HermiT','evaluation/hermit/report.json',h),('SHACL','evaluation/shacl/coverage-status.json',s)]:
        for item in ledger['obligations']:
            key=item['source_element'].split(':')[0]
            eng[key].append(dict(engine=engine,receipt=receipt,obligation=item['id'],outcome=item['outcome'],case_ids=item.get('case_ids') or ([item['case_id']] if item.get('case_id') else []),scope=item.get('scope','Declared module scope only')))
    clauses={r['id']:r for r in formal['constraints']}
    cor_by_req=defaultdict(list)
    for r in cor['requirements']:
        for ident in r['requirement']['source_requirements']:cor_by_req[ident].append(r['requirement']['id'])
    evidence_paths=set();rows=[]
    def append(family,ident,title,sources,requirements=None,elements=None,constraints=None,implementation=None,oracles=None,evidence=None,outcomes=None,claim=None,limit=None,location=None,issues=None,owner=None):
        for p in sources+(evidence or []):
            if isinstance(p,dict):
                require(all(k in p for k in ('archive','member','sha256')),'Unbound historical archive reference')
                continue  # Retained historical companion, never a fresh public execution.
            require((ROOT/p).is_file(),'Missing source/evidence '+p);evidence_paths.add(p)
        rows.append(dict(row_id=family+':'+ident,family=family,source_id=ident,title=title,
          source_paths=sources,source_bindings_sha256={p:sha(p) for p in sources},requirements=requirements or [],model_elements=elements or [],constraint_ids=constraints or [],
          implementation=implementation or 'No additional implementation claimed',oracle_ids=oracles or [],evidence_paths=evidence or [],
          outcomes=outcomes or [],retained_claim=claim or title,limit=limit or 'Finite/source-bound support; not whole-model correctness.',
          manuscript_location=location or 'No element-specific manuscript assertion inferred',
          guide_locations=['docs/traceability.md','docs/wiki/Traceability.md','docs/current/guide/Traceability.html'],
          current_open_issues=issues or [],owner_scope=owner or 'No new owner/independent rating',independent_acceptance=False))
    for r in trace['rows']:
        owner=scope['trace_dispositions'].get(r['id'],{})
        append('REQUIREMENT',r['id'],r['title'],[r['source_file'],'evaluation/traceability/ledger.json'],[r['id']],
          [x['id'] for x in r['model_elements']],r.get('constraint_ids',[]),
          'Original source trace; correction supplement: '+', '.join(cor_by_req[r['id']]) if cor_by_req[r['id']] else 'Original trace plus separately scoped SQL/application profiles',
          r['query_case_ids']+[x['id'] for x in r['formal_evidence']],sorted({x['receipt'] for x in r['formal_evidence'] if x['receipt']}|({'evaluation/cq/report.json'} if r['query_case_ids'] else set())),
          [dict(historical_acceptance_state=r['acceptance_state'],original_population=r.get('source_population_execution'),bounded_owner_scope=owner.get('proposed_scope'))],
          r['acceptance_criterion'],owner.get('limit',r['remaining_obligation']),issues=[4,5,12,13,23,37],owner=owner.get('owner_disposition','No complete original fulfillment or independent judgment'))
    for r in sql['rows']:
        ident=r['id'];data=source[ident];actual=hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
        require(actual==r['source_sha256'],'Stale native row '+ident)
        f=clauses.get(ident);evidence=[x['receipt'] for x in eng[ident]]+['evaluation/relational/correction/mapping-accounting.json']
        if f:evidence+=f['evidence']
        append('MODEL',ident,r['title'],['ontology/riskium-model.json'],req_by_model[ident],[ident],[ident] if ident in clauses else [],
          r['disposition']+'; correction overlay: '+r['correction_overlay'],[x['obligation'] for x in eng[ident]],sorted(set(evidence)),eng[ident],
          f['accepted_scope']['retained_claim'] if f else data.get('definition') or data.get('rationale') or data.get('statement') or r['title'],
          f['accepted_scope']['unclaimed_or_deferred'] if f else r['reason'],issues=[4,5,12,35,36],owner=f['accepted_scope']['owner_disposition'] if f else None)
    for r in manuscript['rows']:
        require(r['disposition'].startswith('WITHDRAWN') or r['declared_value']==r['checked_value'],'Claim value mismatch '+r['id'])
        append('MANUSCRIPT',r['id'],r['claim'],['evaluation/manuscript-review/ledger.json'],evidence=r['evidence'],
          outcomes=[dict(disposition=r['disposition'],declared=r['declared_value'],checked=r['checked_value'],external_evidence_status='RETAINED_HISTORICAL_NOT_FRESH_REPLAYED' if any(isinstance(p,dict) for p in r['evidence']) else 'PUBLIC_RECEIPT_BINDING')],
          claim='Retained historical claim ledger for 7.0.7, reconciled with unchanged source bindings and explicit 7.0.8 amendments.',
          limit=r['limit'] or 'Source-bound numeric/claim baseline, not a fresh independent scientific judgment.',location=r['location'],issues=[13,23,37])
    for r in amend['changes']:
        append('AMENDMENT',r['id'],r['reason'],['evaluation/manuscript-review/v7.0.8/receipt.json'],
          evidence=['evaluation/consistency/manuscript-readback.json'],outcomes=[dict(paragraph_sha256=r['new_paragraph_sha256'],current_version='7.0.8')],
          claim=r['new_text'],limit='Only this owner-approved paragraph amendment; later SQL/Pages work is not silently added to the article.',
          location='DOCX body paragraph '+str(r['paragraph_index']),owner='Owner-authorized seven-paragraph amendment')
    for r in scope['claims']:
        append('RETAINED_CLAIM',r['id'],r['title'],['evaluation/owner-review/accepted-scope.json'],
          evidence=['evaluation/final-review/report.json'],claim=r['permitted_wording'],limit=r['excluded_wording'],owner=r['owner_disposition'],issues=[4,5,12,13,23,36,37])
    for r in cor['requirements']:
        req=r['requirement'];append('CORRECTION_REQUIREMENT',req['id'],req['accept'],['implementation/relational/0.3.0/contract.json'],req['source_requirements'],constraints=req['clauses'],
          implementation='SQL 0.3.0 / migration 4 / assessment_correction; application metadata only',oracles=r['case_ids'],
          evidence=['evaluation/relational/correction/report.json','implementation/relational/0.3.0/component.json'],outcomes=[dict(status=r['status'])],
          claim=req['accept'],limit=req['reject']+'; general source/scenario/assertion mapping remains open.',issues=[12,35,36])
    require(len(rows)==len({r['row_id'] for r in rows})==423,'Lost/duplicate joined row')
    sources=sorted(evidence_paths|{'tools/audit_consistency.py','evaluation/consistency/findings.json','tools/publication/guide-registry.json','evaluation/formal-reference/register.json','evaluation/relational/correction/traceability.json'})
    register=dict(schema='riskium-cross-document-trace-v1',baseline_commit=BASE,model_version='0.3.1',orsd_revision='0.4.3',manuscript_version='7.0.8',latest_published_distribution='v0.3.2',correction_profile='0.3.0',rows=rows,
      summary=dict(rows=len(rows),families=dict(Counter(r['family'] for r in rows)),historical_hermit=h['coverage']['outcomes'],historical_shacl=s['outcomes'],independent_ratings=0),
      input_sha256={p:sha(p) for p in sources},limits=['Trace completeness is accounting, not original MUST fulfillment or semantic accuracy.','Historical numeric claims retain their original populations; fresh software/replay counts are separate.','No term-specific article or native correction relation is inferred from a general artifact link.','Final audited source and live channels are bound by the completion record; #41 must recheck after final selection.'])
    stream=io.StringIO();writer=csv.writer(stream,lineterminator="\n");writer.writerow(['row_id','source_id','title','source_hashes','requirements','model_elements','constraints','implementation','oracles','evidence','outcomes','retained_claim','limit','manuscript_location','guide_locations','open_issues','owner_scope'])
    for r in rows:writer.writerow([r[k] if isinstance(r[k],str) else json.dumps(r[k],ensure_ascii=False) for k in ['row_id','source_id','title','source_bindings_sha256','requirements','model_elements','constraint_ids','implementation','oracle_ids','evidence_paths','outcomes','retained_claim','limit','manuscript_location','guide_locations','current_open_issues','owner_scope']])
    # Full tracked source inventory, with generated views inventoried separately by
    # their publication registries/readback. No output is hashed into itself.
    allpaths=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard'],cwd=ROOT,text=True).splitlines()
    files=[]
    for p in sorted(set(allpaths)):
        if p.startswith(('evaluation/consistency/','docs/current/','docs/wiki/','docs/releases/','docs/versions/')) or p in ('docs/traceability.md','evaluation/documentation-audit.json'):continue
        if (ROOT/p).is_file():files.append(dict(path=p,sha256=sha(p),bytes=(ROOT/p).stat().st_size))
    sys.path.insert(0,str(ROOT/'tools/publication'))
    from site_registry import check_registry
    registry=check_registry(ROOT,BASE)
    inventory=dict(schema='riskium-consistency-source-inventory-v1',baseline_commit=BASE,source_files=files,generated_outputs='21 shared Wiki/Pages guides and registered frozen outputs are verified separately; HTTP/Wiki readbacks bind actual publication.',frozen_snapshots=len(registry['releases']),external_article='Actual author-facing binaries matched the approved receipt; binaries remain outside this repository.',component_registers=['releases/artifact-matrix.json','releases/development-components.json','releases/distribution-v0.3.2.json','implementation/relational/0.3.0/component.json'])
    md="# Current traceability and document consistency\n\nThis guide joins the existing source-bound ledgers for the audited public Riskium baseline. It contains **423 trace rows**: 28 original requirement/scope/CQ rows, 306 native elements, 65 historical manuscript claims, seven approved manuscript amendments, twelve retained release claims and five correction requirements. A row is an accounting route, not a successful scientific test.\n\n[Full JSON table](../evaluation/consistency/traceability.json) · [CSV table](../evaluation/consistency/traceability.csv) · [Input inventory](../evaluation/consistency/inventory.json) · [Findings and resolutions](../evaluation/consistency/findings.json) · [Actual manuscript readback](../evaluation/consistency/manuscript-readback.json).\n\n## Versions and evidence boundaries\n\nThe ontology remains 0.3.1, ORSD 0.4.3 and approved article 7.0.8. The latest published source distribution is v0.3.2. Later SQL correction 0.3.0/migration 4 and current Pages explanations are separately identified development artifacts; they have not replaced immutable source assets. Next publication #41 must select and freeze its exact component set.\n\nOriginal HermiT outcomes remain 281 PASS / 14 NOT_RUN of 295 obligations. Historical SHACL outcomes remain 341 scoped PASS / one PARTIAL / 17 NOT_RUN of 359. Original CQ populations, three withdrawn article claims and zero independent ratings remain visible. Owner acceptance is bounded and does not complete original MUST requirements. Later correction, comparison and source receipts supplement rather than relabel those populations.\n\n## How to follow a row\n\nStart with a requirement or stable native identifier. The table records the source, linked model elements/constraints, selected implementation or explicit omission, original obligation/query/fixture IDs, actual receipts and outcomes, retained claim and limit, article location, reading routes, owner scope and current follow-up issues. The same row can have a passing structural check and an unimplemented application meaning. Article-wide inventory claims do not imply that every term has its own article paragraph.\n\nThe original [28-row ledger](../evaluation/traceability/README.md), [formal-method guide](formal-method.md), [SQL correction receipt](../evaluation/relational/correction/README.md) and [approved article receipt](../evaluation/manuscript-review/v7.0.8/README.md) retain their full source detail. The current table adds a common reading route without rewriting those checkpoints.\n\n## Requirement and question routes\n\n| ID | Purpose | Model elements | Constraints | Current bounded scope |\n| --- | --- | ---: | --- | --- |\n"
    for r in trace['rows']:
        own=scope['trace_dispositions'].get(r['id'],{})
        md+='| '+r['id']+' | '+r['title']+' | '+str(len(r['model_elements']))+' | '+', '.join(r.get('constraint_ids',[]))+' | '+own.get('proposed_scope','Original query/scope contract; later supplements remain separately bound').replace('_',' ').lower()+' |\n'
    md+='\n## Native and application coverage\n\nAll 306 source elements retain their exact identities and source hashes. The SQL register still records 250 incomplete core mappings and 11 external elements. Correction 0.3.0 adds application history for selected C-03/C-17 subclauses and no new native classes/predicates. All 25 constraint sections in the Formalization guide retain original engine outcomes, bounded claims and exclusions.\n\n| Correction requirement | Original requirements | Constraints | Executed case links |\n| --- | --- | --- | ---: |\n'
    for r in cor['requirements']:
        q=r['requirement'];md+='| '+q['id']+' | '+', '.join(q['source_requirements'])+' | '+', '.join(q['clauses'])+' | '+str(len(r['case_ids']))+' |\n'
    md+='\n## Manuscript reconciliation\n\nThe 65-row 7.0.7 claim baseline is retained with the seven approved 7.0.8 paragraph amendments and twelve bounded release claims. Fresh readback of both author-facing files matched their approved SHA-256 values; all seven amended DOCX paragraphs matched exactly. The unchanged PDF retains its earlier nine-page rendering QA; this audit does not claim a new render, article revision or independent review. New SQL/Pages capabilities are not silently added article claims.\n\n## Publication and next release\n\nThe audit report records source/generated parity separately from actual Wiki/Pages publication. Historical readbacks stay dated. The completion record binds the final corrected source, deployed file bodies and fresh Wiki commit. After any further change, #41 must rerun affected checks before its final stable freeze and independently verify its new assets after publication. Broader source/scenario mapping, formal/application policies, source adequacy, independent review and deployment remain open in the [work plan](work-plan.md).\n\nRun `python tools/audit_consistency.py --check` and the documentation builders to reject missing rows, stale hashes or changed historical denominators. This check executes no new HermiT/SHACL test and produces no ontology correctness percentage.\n'
    return {'evaluation/consistency/traceability.json':encode(register),'evaluation/consistency/traceability.csv':stream.getvalue(),'evaluation/consistency/inventory.json':encode(inventory),'docs/traceability.md':md}


def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
    for name,text in build().items():
        path=ROOT/name
        if args.check:require(path.exists() and path.read_text()==text,'Stale consistency output: '+name)
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
    print(encode(dict(status='SOURCE_DOCUMENT_CONSISTENCY_PASS',trace_rows=423,scientific_engine_runs=0)))

if __name__=='__main__':main()
