"""Run candidate-only SQLite/RDF evidence, with current input-bound receipts."""
import importlib.util
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from rdflib import Graph, Dataset, Literal, URIRef
from rdflib.namespace import OWL, RDF, XSD
from pyshacl import validate
import relational_use as m


def command(args):
    start=time.monotonic();r=subprocess.run([str(x) for x in args],cwd=m.ROOT,capture_output=True,text=True,timeout=120)
    return {'exit_code':r.returncode,'stdout':r.stdout.strip(),'stderr':r.stderr.strip(),'elapsed_ms':round((time.monotonic()-start)*1000)}


def main():
    contract=m.contract();dest=m.HERE/'generated';dest.mkdir(exist_ok=True)
    # B0-4 contract generation is reused, not bypassed or rewritten.
    folder=m.HERE.parent/'issue93-export-contract';sys.path.insert(0,str(folder))
    import export_candidate
    export_candidate.export(json.loads(export_candidate.CONTRACT.read_text()),check=True)
    owl=Graph().parse(folder/'generated/candidate.owl.ttl',format='turtle')
    shapes=Graph().parse(m.HERE.parent/'issue93-integration/combined-managed.shacl.ttl',format='turtle')
    source=m.fixture_source.fresh();m.fixture_source.populate(source);before=m.fixture_source.state_hash(source)
    path=dest/'candidate-use.sqlite'
    if path.exists():path.unlink()  # Only this generated synthetic output.
    db=m.connect(path);m.initialize(source,db)
    fixture=json.loads((m.HERE/'fixtures.json').read_text())
    checks=[]
    def check(name,kind,graph,expected):
        observed,_,_=validate(graph,shacl_graph=shapes,ont_graph=owl,inference='none',advanced=False,do_owl_imports=False)
        checks.append({'id':name,'group':kind,'expected_conforms':expected,'observed_conforms':bool(observed),'pass':bool(observed)==expected})
    for i,record in enumerate(m.fixture_source.fixture()['records'],1):
        version=record['version_id']
        check('old-projection-'+str(i),'legacy-compatibility',m.legacy.native_graph(source,version),False)
        graph=m.information_graph(db,version);graph.serialize(dest/f'information-{i}.ttl',format='turtle')
        check('documentary-projection-'+str(i),'candidate-information',graph,True)
    import_use_count=db.execute('SELECT count(*) FROM evidence_use').fetchone()[0]
    for grounding in fixture['groundings']:m.add_grounding(db,grounding)
    for use in fixture['uses']:m.record_use(db,use)
    all_graph=Graph();dataset=Dataset()
    for i,use in enumerate(fixture['uses'],1):
        graph=m.use_graph(db,use['id']);graph.serialize(dest/f'use-{i}.ttl',format='turtle');all_graph+=graph
        context=dataset.graph(URIRef(use['id']))
        for triple in graph:context.add(triple)
        check('explicit-use-'+str(i),'candidate-use',graph,True)
    base=m.use_graph(db,fixture['uses'][0]['id']);u=URIRef(fixture['uses'][0]['id'])
    for ident in ['missing-grounding','missing-item','missing-reference','invalid-purpose','reversed-mediation','aliased-participants']:
        graph=Graph()+base
        if ident=='invalid-purpose':
            graph.remove((u,m.EU.purpose,None));graph.add((u,m.EU.purpose,Literal('proves-true',datatype=XSD.string)))
        elif ident=='aliased-participants':
            graph.add((graph.value(u,m.RISK['RE-001']),OWL.sameAs,graph.value(u,m.RISK['RE-002'])))
        else:
            pred=m.RISK[{'missing-grounding':'RE-003','missing-item':'RE-001','missing-reference':'RE-002','reversed-mediation':'RE-001'}[ident]]
            value=graph.value(u,pred);graph.remove((u,pred,None))
            if ident=='reversed-mediation':graph.add((value,pred,u))
        check(ident,'negative-export-control',graph,False)
    sql=m.rows(db);sparql=[[str(x) for x in row] for row in all_graph.query((m.HERE/'query.rq').read_text())]
    missing_graph=Graph()
    for use in fixture['uses'][:-1]:missing_graph+=m.use_graph(db,use['id'])
    missing_rows=[[str(x) for x in row] for row in missing_graph.query((m.HERE/'query.rq').read_text())]
    dataset.serialize(dest/'all-explicit-uses.trig',format='trig')
    (dest/'candidate-use.sql').write_text('\n'.join(db.iterdump())+'\n')
    (dest/'query-answers.json').write_text(json.dumps({'sql':sql,'sparql':sparql,'dropped_use_mutant_rows':missing_rows},indent=2)+'\n')
    tests=command([sys.executable,'-m','unittest','discover','-s',m.HERE,'-p','test_relational_use.py','-v'])
    regression={}
    for name in ['test_qualified_evidence.py','test_source_transition.py']:
        r=command([sys.executable,'-m','unittest','discover','-s','tests','-p',name,'-v'])
        count=re.search(r'Ran (\d+) tests?',r['stderr']);r['tests']=int(count[1]) if count else 0;regression[name]=r
    health={'sqlite_version':m.sqlite3.sqlite_version,'integrity':db.execute('PRAGMA integrity_check').fetchone()[0],
            'foreign_key_violations':len(db.execute('PRAGMA foreign_key_check').fetchall()),
            'reference_snapshots':db.execute('SELECT count(*) FROM reference_snapshot').fetchone()[0],
            'imported_version_pins':db.execute('SELECT count(*) FROM artifact_version').fetchone()[0],
            'use_count_immediately_after_import':import_use_count,'explicit_use_records':len(sql)}
    m.health(db);m.legacy.health(source)
    unchanged=before==m.fixture_source.state_hash(source)
    passed={'sidecar_tests':tests['exit_code']==0 and 'Ran 21 tests' in tests['stderr'],
            'all_shacl_outcomes':all(r['pass'] for r in checks),
            'selected_sql_sparql_parity':sql==sparql and len(sql)==3,
            'dropped_use_mutation_detected':missing_rows!=sql,
            'import_never_infers_use':import_use_count==0,
            'legacy_schema_data_unchanged':unchanged,
            'baseline_regressions':all(r['exit_code']==0 and r['tests'] for r in regression.values()),
            'sqlite_integrity':health['integrity']=='ok' and health['foreign_key_violations']==0}
    generated_hashes={p.name:m.digest(p) for p in sorted(dest.iterdir()) if p.is_file()}
    report={'schema':'riskium-explicit-use-sidecar-verification-1','date_tehran':'2026-11-09',
            'candidate_source_commit':'2028c2d21b519940d84b640663b0d0a6cf2499b8',
            'status':'B05_SQLITE_RDF_SLICE_COMPLETE_NOT_PROMOTED' if all(passed.values()) else 'FAIL',
            'checks':passed,'summary':{'sidecar_unit_tests':21,'sidecar_unit_tests_passed':21 if passed['sidecar_tests'] else 0,
             'shacl_outcomes':len(checks),'shacl_matches':sum(r['pass'] for r in checks),
             'new_information_graphs':4,'explicit_use_graphs':3,'negative_export_controls':6,
             'historical_incompatibilities_reconfirmed':4,'selected_query_rows':len(sql),
             'baseline_regression_tests':sum(r['tests'] for r in regression.values()),
             'baseline_regression_passed':sum(r['tests'] for r in regression.values() if r['exit_code']==0),
             'production_promoted':False,'postgresql_tested':False},
            'health':health,'shacl_cases':checks,'tests':tests,'regressions':regression,
            'source_state_hash_before':before,'source_state_hash_after':m.fixture_source.state_hash(source),
            'contract_sha256':m.digest(m.HERE/'contract.json'),'generated_sha256':generated_hashes,
            'boundary':'Synthetic version-pinned sidecar only. Old v7 exports remain historical; the new information/use routes are not an automatic backfill. Factual grounding adequacy, real-data migration, production/PostgreSQL deployment, complete query equivalence and reader/CI promotion remain unestablished.'}
    db.close();source.close()
    (m.HERE/'verification-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'checks':passed,'summary':report['summary'],'health':health},indent=2))
    if not all(passed.values()):raise SystemExit(1)


if __name__=='__main__':main()
