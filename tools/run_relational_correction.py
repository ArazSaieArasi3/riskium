"""Execute the predeclared correction oracles and source-bound SQLite receipts."""
import argparse
import hashlib
import json
import sqlite3
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import patch
from rdflib import URIRef
from rdflib.compare import isomorphic

import relational_correction as c
import relational_assessment as a
import relational_history as b
from run_relational_assessment import graph, expected_graph

OUT=c.ROOT/'evaluation/relational/correction'
TIME='2026-10-26T01:00:00Z'


def fresh():
    db=a.baseline();c.migrate(db);return db


def bundle(suffix='2',value='0.25',source=None):
    assessment=a.default_assessment('a1');assessment.update(assessment_version_id=a.U('a1-v'+suffix),recorded_at='2026-10-26T00:00:00Z')
    result=a.default_result('r1');result.update(result_version_id=a.U('r1-v'+suffix),reported_value=value,
      score_kind='UNKNOWN' if value is None else 'REPORTED',source_record_id=source or a.SOURCE)
    return assessment,result


def issue(db,suffix='2',value='0.25',source=None,**changes):
    assessment,result=bundle(suffix,value,source)
    args=dict(prior=a.U('a1-v1'),reason='Corrected synthetic report',recorded_at=TIME,source=a.SOURCE)
    args.update(changes);c.issue_corrected(db,assessment,[result],**args)


def state(db):
    return dict(rows=c.snapshot(db),schema=b.schema_snapshot(db),version=db.execute('PRAGMA user_version').fetchone()[0])


def complete_family(db):
    issue(db);db.execute('INSERT INTO source_record VALUES(?,?)',(a.U('other-source'),'{"synthetic":"other"}'))
    issue(db,'3',None,a.U('other-source'))


def execute():
    fixture=json.loads((c.OUT/'fixtures.json').read_text());rows=[]
    def add(ident,expected,observed,kind='positive',detail=None):
        matched=expected==observed
        def compact(value):
            if isinstance(value,dict) and set(value)=={'rows','schema','version'}:
                return dict(state_sha256=hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
                  tables=len(value['rows']),user_version=value['version'])
            return value
        rows.append(dict(id=ident,kind=kind,expected=compact(expected),observed=compact(observed),status='PASS' if matched else 'FAIL',detail=detail))
    db=a.baseline();before=a.snapshot(db);ledger=list(db.execute('SELECT * FROM schema_migration'));g=graph(db,a.U('a1-v1'));c.migrate(db)
    add('POPULATED_UPGRADE',True,before==a.snapshot(db) and ledger==list(db.execute('SELECT * FROM schema_migration WHERE version<4')) and isomorphic(g,graph(db,a.U('a1-v1'))))
    old=state(db);c.migrate(db);add('IDEMPOTENT_UPGRADE',old,state(db));db.close()
    db=a.baseline();old=dict(rows=a.snapshot(db),schema=b.schema_snapshot(db),version=3)
    with patch.object(c,'migration_text',return_value=c.migration_text()+'\nINSERT INTO absent_table VALUES(1);\n'):
        try:c.migrate(db);rejected=False
        except sqlite3.OperationalError:rejected=True
    add('FAILED_UPGRADE',True,rejected and old==dict(rows=a.snapshot(db),schema=b.schema_snapshot(db),version=db.execute('PRAGMA user_version').fetchone()[0]),'negative');db.close()
    db=fresh();complete_family(db)
    add('ALL_BRANCH_VALUES',fixture['family'],c.family(db,a.U('a1-v1'))['rows'])
    add('BRANCH_DEPTHS',fixture['lineage'],[list(r) for r in db.execute((c.OUT/'queries/descendants.sql').read_text(),dict(root=a.U('a1-v1')))])
    add('OLD_VALUE',fixture['old_result'],list(db.execute('SELECT score_kind,reported_value FROM result_snapshot WHERE result_version_id=?',(a.U('r1-v1'),)).fetchone()))
    add('NEW_VALUE',fixture['new_result'],list(db.execute('SELECT score_kind,reported_value FROM result_snapshot WHERE result_version_id=?',(a.U('r1-v2'),)).fetchone()))
    add('CORROBORATION_NOT_INFERRED','NOT_ASSESSED',c.family(db,a.U('a1-v1'))['independent_corroboration'])
    add('BOUND_QUERY_INJECTION',[],c.family(db,"'; DROP TABLE result_snapshot; --")['rows'])
    # Independent hand-written source graph from the preceding profile's oracle;
    # only the declared InformationVersion names change, never artifact identity.
    for version in ('1','2','3'):
        expected=expected_graph()
        if version!='1':
            replacement={URIRef(a.U('a1-v1')):URIRef(a.U('a1-v'+version)),URIRef(a.U('r1-v1')):URIRef(a.U('r1-v'+version))}
            from rdflib import Graph
            expected=Graph().parse(data=expected.serialize(format='nt'),format='nt')
            for triple in list(expected):
                mapped=tuple(replacement.get(term,term) for term in triple)
                if mapped!=triple:expected.remove(triple);expected.add(mapped)
        actual=graph(db,a.U('a1-v'+version))
        add('NATIVE_RDF_V'+version,True,isomorphic(expected,actual),detail=dict(expected_nt=sorted(expected.serialize(format='nt').splitlines()),observed_nt=sorted(actual.serialize(format='nt').splitlines())))
    with tempfile.TemporaryDirectory() as temp:
        backup=b.connect(Path(temp)/'backup.sqlite');db.backup(backup);c.health(backup)
        add('BACKUP_REOPEN',state(db),state(backup));backup.close();reopened=c.connect(Path(temp)/'backup.sqlite');add('FILE_REOPEN',c.family(db,a.U('a1-v1')),c.family(reopened,a.U('a1-v1')));reopened.close()
    dump='\n'.join(db.iterdump());restored=b.connect();c.restore_dump(restored,dump);add('DUMP_RESTORE',state(db),state(restored));restored.close()
    # Change only the stored predecessor in the data section, retain valid DDL.
    bad=dump.replace("INSERT INTO \"assessment_correction\" VALUES('"+a.U('a1-v2')+"','"+a.U('a1-v1')+"'", "INSERT INTO \"assessment_correction\" VALUES('"+a.U('a1-v2')+"','"+a.U('a2-v1')+"'")
    assert bad!=dump,'Tamper fixture did not alter the receipt'
    target=b.connect()
    try:c.restore_dump(target,bad);rejected=False
    except ValueError as e:rejected=str(e)=='R-CORRECTION-DATA'
    add('RESTORE_TAMPER',True,rejected and not b.schema_snapshot(target),'negative');target.close();db.close()
    negatives={
      'CROSS_IDENTITY':lambda d:issue(d,prior=a.U('a2-v1')),
      'MISSING_PARENT':lambda d:issue(d,prior=a.U('absent')),
      'SELF_EDGE':lambda d:issue(d,prior=a.U('a1-v2')),
      'EMPTY_REASON':lambda d:issue(d,reason='  '),
      'MISSING_SOURCE':lambda d:issue(d,source='urn:absent'),
      'BAD_CALENDAR':lambda d:issue(d,recorded_at='2026-02-30T01:00:00Z'),
      'EARLY_DECLARATION':lambda d:issue(d,recorded_at='2026-10-25T01:00:00Z')}
    for ident,operation in negatives.items():
        db=fresh();old=state(db)
        try:operation(db);rejected=False;error=None
        except (sqlite3.IntegrityError,ValueError) as e:rejected=True;error=str(e)
        add(ident,True,rejected and state(db)==old,'negative',error);db.close()
    for ident,sql in {
      'DUPLICATE_EDGE':'INSERT INTO assessment_correction SELECT * FROM assessment_correction',
      'REPLACE_EDGE':'INSERT OR REPLACE INTO assessment_correction SELECT * FROM assessment_correction',
      'UPDATE_EDGE':"UPDATE assessment_correction SET reason='changed'",
      'DELETE_EDGE':'DELETE FROM assessment_correction',
      'CYCLE':"INSERT INTO assessment_correction VALUES('"+a.U('a1-v1')+"','"+a.U('a1-v2')+"','cycle','"+TIME+"','"+a.SOURCE+"')"}.items():
        db=fresh();issue(db);old=state(db)
        try:db.execute(sql);rejected=False;error=None
        except sqlite3.IntegrityError as e:rejected=True;error=str(e)
        add(ident,True,rejected and state(db)==old,'negative',error);db.close()
    db=fresh();assessment,result=bundle();a.stage_version(db,a.U('unissued-assessment'),a.U('a1'),payload=dict(assessment,assessment_version_id=a.U('unissued-assessment')))
    a.insert_dict(db,'assessment_snapshot',dict(assessment,assessment_version_id=a.U('unissued-assessment')));old=state(db)
    add('STAGING_NOT_PUBLISHED',[],c.family(db,a.U('unissued-assessment'))['rows'])
    try:issue(db,prior=a.U('unissued-assessment'));rejected=False
    except sqlite3.IntegrityError:rejected=True
    add('UNISSUED_PARENT',True,rejected and state(db)==old,'negative');db.close()
    db=fresh();old=state(db);assessment,good=bundle();bad=a.default_result('bad');bad['score_kind']='COMPUTED'
    try:c.issue_corrected(db,assessment,[good,bad],a.U('a1-v1'),'reason',TIME,a.SOURCE);rejected=False
    except sqlite3.IntegrityError:rejected=True
    add('ATOMIC_BUNDLE_FAILURE',True,rejected and state(db)==old,'negative');db.close()
    for ident,sql in [('CONFIGURATION_OFF','PRAGMA foreign_keys=OFF'),('SCHEMA_DRIFT','DROP TRIGGER correction_update'),('LEDGER_DRIFT',"UPDATE schema_migration SET sha256='changed' WHERE version=4")]:
        db=fresh();db.execute(sql)
        try:c.health(db);error=None
        except ValueError as e:error=str(e)
        expected={'CONFIGURATION_OFF':'R-CONNECTION-POLICY','SCHEMA_DRIFT':'R-CORRECTION-SCHEMA','LEDGER_DRIFT':'R-CORRECTION-HASH'}[ident]
        add(ident,expected,error.split(':')[0] if error else None,'negative');db.close()
    db=fresh();issue(db);db.execute('DROP TRIGGER correction_update');db.execute("UPDATE assessment_correction SET reason='weakened rule admitted change'")
    add('MUTANT_UPDATE_EXPOSED','weakened rule admitted change',db.execute('SELECT reason FROM assessment_correction').fetchone()[0],'mutation');db.close()
    db=fresh();guard=db.execute("SELECT sql FROM sqlite_master WHERE name='correction_insert'").fetchone()[0];db.execute('DROP TRIGGER correction_insert')
    db.execute('INSERT INTO assessment_correction VALUES(?,?,?,?,?)',(a.U('a2-v1'),a.U('a1-v1'),'weakened cross-identity',TIME,a.SOURCE));db.execute(guard)
    try:c.health(db);error=None
    except ValueError as e:error=str(e)
    add('MUTANT_IDENTITY_EXPOSED','R-CORRECTION-DATA',error,'mutation');db.close()
    paths=['implementation/relational/0.3.0/'+p for p in ['contract.json','fixtures.json','004_correction.sql','queries/family.sql','queries/descendants.sql']]+['tools/relational_correction.py','tools/run_relational_correction.py','tools/relational_assessment.py','tools/relational_history.py','tools/run_relational_assessment.py','tools/build_relational_assessment.py',
      'tools/build_relational_history.py','tools/requirements-shacl.txt',
      'implementation/relational/0.1.0/001_tables.sql','implementation/relational/0.1.0/002_guards.sql',
      'implementation/relational/0.1.0/fixtures.json','implementation/relational/0.2.0/policy.json']
    receipts=['evaluation/hermit/report.json','evaluation/shacl/coverage-status.json','evaluation/owner-review/accepted-scope.json']
    preserved={p:hashlib.sha256((c.ROOT/p).read_bytes()).hexdigest() for p in receipts+list(c.contract()['source_sha256'])}
    return dict(schema='riskium-correction-execution-v1',source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=c.ROOT,text=True).strip(),predeclared_contract_commit='753dccdce0865c6cbd3400aa245cea1b2e26d0d6',source_note='Execution checkout plus exact input digests; evaluated worktree bytes may be committed subsequently. Hosted --check replays fixed outcomes without rewriting the receipt.',inputs_sha256={p:hashlib.sha256((c.ROOT/p).read_bytes()).hexdigest() for p in paths},preserved_sources_sha256=preserved,engine=dict(name='SQLite',version=sqlite3.sqlite_version),summary=dict(cases=len(rows),passed=sum(r['status']=='PASS' for r in rows),mutation_controls=sum(r['kind']=='mutation' for r in rows),native_graph_comparisons=3),cases=rows,limits=c.contract()['policy'],independent_acceptance=False,postgresql_executed=False)


def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args();report=execute()
    if any(r['status']!='PASS' for r in report['cases']):
        print(json.dumps([r for r in report['cases'] if r['status']!='PASS'],indent=2));raise SystemExit(1)
    if args.check:
        old=json.loads((OUT/'report.json').read_text())
        for key in ('inputs_sha256','preserved_sources_sha256','summary','cases','limits'):
            if old[key]!=report[key]:raise ValueError('Correction replay differs: '+key)
    else:
        OUT.mkdir(parents=True,exist_ok=True);(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report['summary']))

if __name__=='__main__':main()
