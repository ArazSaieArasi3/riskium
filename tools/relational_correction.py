"""SQLite v4 assessment correction overlay; no native ontology relation added."""
from functools import lru_cache
from datetime import datetime
import hashlib
import json
from pathlib import Path

import relational_assessment as a
import relational_history as b

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'implementation/relational/0.3.0'
SQL=OUT/'004_correction.sql'
TABLES=b.TABLES+('schema_migration',)+a.NEW_TABLES+('assessment_correction',)


def contract():
    data=json.loads((OUT/'contract.json').read_text())
    for path,digest in data['source_sha256'].items():
        if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=digest:
            raise ValueError('R-CORRECTION-SOURCE: '+path)
    return data


def migration_text():
    contract();return SQL.read_text()


def digest():return hashlib.sha256(migration_text().encode()).hexdigest()


@lru_cache(maxsize=4)
def expected_schema(sha):
    c=a.connect()
    b.execute_script(c,migration_text());result=b.schema_snapshot(c);c.close();return result


def health(c):
    b.require_configuration(c);contract()
    ledger=dict(c.execute('SELECT version,sha256 FROM schema_migration'))
    if set(ledger)!={1,2,3,4} or c.execute('PRAGMA user_version').fetchone()[0]!=4:
        raise ValueError('R-CORRECTION-LEDGER')
    expected={1:hashlib.sha256((b.OUT/'001_tables.sql').read_bytes()).hexdigest(),
      2:hashlib.sha256((b.OUT/'002_guards.sql').read_bytes()).hexdigest(),3:a.migration_hash(),4:digest()}
    if ledger!=expected:raise ValueError('R-CORRECTION-HASH')
    if b.schema_snapshot(c)!=expected_schema(ledger[4]):raise ValueError('R-CORRECTION-SCHEMA')
    if c.execute('PRAGMA foreign_key_check').fetchall():raise ValueError('R-CORRECTION-FK')
    if c.execute('PRAGMA integrity_check').fetchall()!=[('ok',)]:raise ValueError('R-CORRECTION-INTEGRITY')
    b.audit_legacy(c);a.audit_data(c)
    if c.execute('SELECT 1 FROM v_correction_invalid LIMIT 1').fetchone():raise ValueError('R-CORRECTION-DATA')
    if c.execute('''WITH RECURSIVE walk(root,id) AS (
      SELECT corrected_version_id,prior_version_id FROM assessment_correction UNION
      SELECT w.root,c.prior_version_id FROM walk w JOIN assessment_correction c ON c.corrected_version_id=w.id)
      SELECT 1 FROM walk WHERE root=id LIMIT 1''').fetchone():raise ValueError('R-CORRECTION-CYCLE')
    for (value,) in c.execute('SELECT recorded_at FROM assessment_correction'):
        try:
            d=datetime.fromisoformat(value.removesuffix('Z')+'+00:00')
            if len(value)!=20 or d.isoformat(timespec='seconds').replace('+00:00','Z')!=value:raise ValueError()
        except (ValueError,TypeError):raise ValueError('R-CORRECTION-TIME') from None


def snapshot(c):
    return {t:sorted([list(r) for r in c.execute('SELECT * FROM '+t)],key=lambda r:json.dumps(r,ensure_ascii=False)) for t in TABLES}


def migrate(c):
    b.require_configuration(c)
    version=c.execute('PRAGMA user_version').fetchone()[0]
    if version==3:
        with b.transaction(c):
            a.health(c);before=a.snapshot(c);ledger=list(c.execute('SELECT * FROM schema_migration ORDER BY version'))
            sql=migration_text();b.execute_script(c,sql)
            c.execute('INSERT INTO schema_migration VALUES(4,?)',(hashlib.sha256(sql.encode()).hexdigest(),))
            c.execute('PRAGMA user_version=4')
            if a.snapshot(c)!=before or list(c.execute('SELECT * FROM schema_migration WHERE version<4 ORDER BY version'))!=ledger:
                raise ValueError('R-CORRECTION-DATA-LOSS')
            health(c)
    elif version==4:health(c)
    else:raise ValueError('R-CORRECTION-REQUIRES-V3')


def connect(path):
    c=b.connect(path)
    try:migrate(c)
    except BaseException:c.close();raise
    return c


def issue_corrected(c,assessment,results,prior,reason,recorded_at,source):
    health(c)
    if not results:raise ValueError('R-CORRECTION-EMPTY-BUNDLE')
    if any(item.get('reported_value') is not None and not isinstance(item['reported_value'],str) for item in results):
        raise ValueError('R-REPORTED-LEXEME-TYPE')
    with b.transaction(c):
        aid=assessment['assessment_id']
        if not c.execute('SELECT 1 FROM information_artifact WHERE artifact_id=?',(aid,)).fetchone():
            a.add_artifact(c,aid,'RKM-C032','Assessment',assessment['source_record_id'])
        a.stage_version(c,assessment['assessment_version_id'],aid,payload=assessment,source=assessment['source_record_id'])
        a.insert_dict(c,'assessment_snapshot',assessment)
        for item in results:
            row=dict(item,assessment_version_id=assessment['assessment_version_id'])
            if not c.execute('SELECT 1 FROM information_artifact WHERE artifact_id=?',(row['result_id'],)).fetchone():
                a.add_artifact(c,row['result_id'],'RKM-C034','Result',row['source_record_id'])
            a.stage_version(c,row['result_version_id'],row['result_id'],payload=row,source=row['source_record_id'])
            a.insert_dict(c,'result_snapshot',row);a.seal(c,row['result_version_id'],assessment['recorded_at'])
        a.seal(c,assessment['assessment_version_id'],assessment['recorded_at'])
        c.execute('INSERT INTO assessment_correction VALUES(?,?,?,?,?)',(assessment['assessment_version_id'],prior,reason,recorded_at,source))
        health(c)


def family(c,root):
    health(c)
    return dict(independent_corroboration='NOT_ASSESSED',selection='ALL_DECLARED_BRANCHES',
      rows=[list(r) for r in c.execute((OUT/'queries/family.sql').read_text(),dict(root=root))])


def restore_dump(c,text):
    b.require_configuration(c)
    statements=[s for s in b.statements(text) if s.strip().upper() not in ('BEGIN TRANSACTION;','COMMIT;')]
    tables=[s for s in statements if s.lstrip().upper().startswith('CREATE TABLE')]
    inserts=[s for s in statements if s.lstrip().upper().startswith('INSERT INTO')]
    rest=[s for s in statements if s not in tables and s not in inserts]
    with b.transaction(c):
        c.execute('PRAGMA defer_foreign_keys=ON')
        for statement in tables+inserts+rest:c.execute(statement)
        c.execute('PRAGMA user_version=4');health(c)
