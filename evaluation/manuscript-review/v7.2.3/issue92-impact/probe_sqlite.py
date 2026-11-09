"""Inspect the frozen identity slice with one disposable synthetic case."""
from pathlib import Path
import json,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'tools'))
import relational_history as history

def probe():
 db=history.connect();history.migrate(db,2);before=history.schema_snapshot(db)
 with history.transaction(db):
  db.execute('INSERT INTO source_record VALUES(?,?)',('urn:riskium:b1:synthetic-source','{"kind":"synthetic-B1-inspection"}'))
  history.add_identity(db,'urn:riskium:b1:case','case')
  db.execute('INSERT INTO risk_case(case_id,label,source_record_id) VALUES(?,?,?)',('urn:riskium:b1:case','Synthetic analytical item without register entry','urn:riskium:b1:synthetic-source'))
 rows=[list(r) for r in db.execute('SELECT subject,predicate,object FROM v_native_facts WHERE subject=?',('urn:riskium:b1:case',))]
 report={'schema':'riskium-riskcase-baseline-sql-inspection-1','fixture':'ONE_SYNTHETIC_CASE_IN_MEMORY','engine':'SQLite '+history.sqlite3.sqlite_version,
  'schema_user_version':db.execute('PRAGMA user_version').fetchone()[0],'case_rows':db.execute('SELECT count(*) FROM risk_case').fetchone()[0],
  'register_entries':db.execute('SELECT count(*) FROM register_entry').fetchone()[0],'case_type_export_rows':rows,
  'foreign_key_violations':len(db.execute('PRAGMA foreign_key_check').fetchall()),'integrity':db.execute('PRAGMA integrity_check').fetchone()[0],
  'schema_unchanged':before==history.schema_snapshot(db),
  'boundary':'Read-only inspection of maintained source plus a disposable synthetic database. The historical identity slice can store/export a case without a register entry. No case/profile migration, real data, PostgreSQL, end-to-end contextual mapping, or new HermiT/SHACL run is established.'}
 db.close()
 assert report['case_rows']==1 and report['register_entries']==0 and len(rows)==1 and report['foreign_key_violations']==0 and report['schema_unchanged'] and report['integrity']=='ok'
 return report
if __name__=='__main__':print(json.dumps(probe(),indent=2)+'\n')
