"""Generate reviewed SQLite history guards/mapping from fixed source signatures."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'implementation/relational/0.1.0'
RISK='https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'
CLASSES={'RKM-X01':'risk_case','RKM-C014':'information_artifact','RKM-C015':'version_snapshot WHERE is_issued=1',
 'RKM-C022':'register_entry + information_artifact','RKM-C023':'issued version_snapshot with entry_id',
 'RKM-C030':'register artifact kind','RKM-C002':'Context artifact kind','RKM-C035':'Method artifact kind',
 'RKM-C036':'Scale artifact kind','RKM-C072':'Criteria artifact kind'}
RELATIONS={'R-01':('RKM-C022','RKM-X01'),'RX-008':('RKM-C022','RKM-C030'),
 'R-33':('RKM-C023','RKM-C022'),'R-34':('RKM-C023','RKM-C023'),'RX-006':('RKM-C015','RKM-C014')}
SLOTS={'Context':'RKM-C002','Method':'RKM-C035','Scale':'RKM-C036','Criteria':'RKM-C072'}


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def render():
    path=ROOT/'ontology/riskium-model.json';model=json.loads(path.read_text())
    native=json.loads((ROOT/'evaluation/native-review-decisions.json').read_text())
    if model['version']!='0.3.1' or native['source_model_sha256']!=digest(path):raise ValueError('Reviewed native source changed')
    concepts={c['id']:c for c in model['concepts']};rels={r['id']:r for r in model['associations']}
    for cid in CLASSES:
        if concepts[cid]['scope_layer']!='FORMAL_CORE':raise ValueError('Mapped class changed')
    for rid,pair in RELATIONS.items():
        if (rels[rid]['source'],rels[rid]['target'])!=pair or rels[rid]['scope_layer']!='FORMAL_CORE':raise ValueError('Mapped signature changed: '+rid)
    constraints={c['id']:c for c in model['constraints']};source_rows=[]
    for cid in ('C-01','C-03','C-24','C-25'):
        encoded=json.dumps(constraints[cid],sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
        source_rows.append({'id':cid,'statement':constraints[cid]['statement'],'sha256':hashlib.sha256(encoded).hexdigest()})
    sql=['-- Generated history guards; apply with the transactional migration runner.']
    def trigger(name,event,table,when,body):
        sql.append(f'CREATE TRIGGER {name} BEFORE {event} ON {table}'+(' WHEN '+when if when else '')+'\nBEGIN\n'+body+'\nEND;')
    def reject(code):return "SELECT RAISE(ABORT, '"+code+"');"
    for table,key in (('source_record','record_id'),('identity_registry','resource_id'),('risk_case','case_id'),
                      ('information_artifact','artifact_id'),('register_entry','entry_id')):
        trigger(table+'_no_replace','INSERT',table,f'EXISTS(SELECT 1 FROM {table} WHERE {key}=NEW.{key})',reject('R-CATALOG-DUPLICATE'))
        for event in ('UPDATE','DELETE'):trigger(table+'_no_'+event.lower(),event,table,'',reject('R-CATALOG-IMMUTABLE'))
    trigger('snapshot_no_replace','INSERT','version_snapshot','EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.version_id)',reject('R-VERSION-DUPLICATE'))
    trigger('snapshot_insert_unissued','INSERT','version_snapshot','NEW.is_issued<>0',reject('R-ISSUE-VIA-SEAL'))
    trigger('snapshot_immutable_update','UPDATE','version_snapshot','OLD.is_issued=1',reject('R-ISSUED-IMMUTABLE'))
    trigger('snapshot_immutable_delete','DELETE','version_snapshot','OLD.is_issued=1',reject('R-ISSUED-IMMUTABLE'))
    # All predecessor edits, including work-in-progress snapshots, are checked.
    lineage="""SELECT CASE WHEN NEW.previous_version_id IS NOT NULL AND NOT EXISTS(
      SELECT 1 FROM version_snapshot p WHERE p.version_id=NEW.previous_version_id
      AND p.entry_id=NEW.entry_id AND p.is_issued=1) THEN RAISE(ABORT,'R-PREDECESSOR-SAME-ISSUED-ENTRY') END;"""
    cycle="""SELECT CASE WHEN NEW.previous_version_id IS NOT NULL AND EXISTS(
      WITH RECURSIVE prior(id) AS (SELECT NEW.previous_version_id UNION
        SELECT v.previous_version_id FROM version_snapshot v JOIN prior p ON v.version_id=p.id
        WHERE v.previous_version_id IS NOT NULL) SELECT 1 FROM prior WHERE id=NEW.version_id)
      THEN RAISE(ABORT,'R-PREDECESSOR-CYCLE') END;"""
    for event in ('INSERT','UPDATE'):
        trigger('snapshot_lineage_'+event.lower(),event,'version_snapshot','',lineage)
        trigger('snapshot_cycle_'+event.lower(),event,'version_snapshot','',cycle)
    trigger('snapshot_seal','UPDATE','version_snapshot','OLD.is_issued=0 AND NEW.is_issued=1',"""SELECT CASE WHEN NEW.issued_at IS NULL THEN RAISE(ABORT,'R-ISSUE-TIME-REQUIRED') END;
      SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM json_each(NEW.payload_json)) THEN RAISE(ABORT,'R-ISSUE-CONTENT-REQUIRED') END;
      SELECT CASE WHEN EXISTS(SELECT 1 FROM information_artifact a WHERE a.artifact_id=NEW.artifact_id
        AND ((a.kind='RKM-C022' AND (NEW.entry_id IS NULL OR NEW.entry_id<>a.artifact_id))
          OR (a.kind<>'RKM-C022' AND NEW.entry_id IS NOT NULL))) THEN RAISE(ABORT,'R-REVISION-TARGET-KIND') END;""")
    frozen="EXISTS(SELECT 1 FROM version_snapshot WHERE version_id={owner} AND is_issued=1)"
    trigger('dependency_frozen_insert','INSERT','version_dependency',frozen.format(owner='NEW.owner_version_id'),reject('R-DEPENDENCY-FROZEN'))
    trigger('dependency_frozen_update','UPDATE','version_dependency',frozen.format(owner='OLD.owner_version_id')+' OR '+frozen.format(owner='NEW.owner_version_id'),reject('R-DEPENDENCY-FROZEN'))
    trigger('dependency_frozen_delete','DELETE','version_dependency',frozen.format(owner='OLD.owner_version_id'),reject('R-DEPENDENCY-FROZEN'))
    trigger('dependency_no_replace','INSERT','version_dependency','EXISTS(SELECT 1 FROM version_dependency WHERE owner_version_id=NEW.owner_version_id AND slot=NEW.slot)',reject('R-DEPENDENCY-DUPLICATE'))
    target_case='CASE NEW.slot '+' '.join("WHEN '"+k+"' THEN '"+v+"'" for k,v in SLOTS.items())+' END'
    body="""SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM version_snapshot t WHERE t.version_id=NEW.target_version_id AND t.is_issued=1)
       THEN RAISE(ABORT,'R-DEPENDENCY-TARGET-NOT-ISSUED') END;
      SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM version_snapshot t JOIN information_artifact a ON a.artifact_id=t.artifact_id
        WHERE t.version_id=NEW.target_version_id AND a.kind="""+target_case+""") THEN RAISE(ABORT,'R-DEPENDENCY-TARGET-KIND') END;
      SELECT CASE WHEN NEW.direct_artifact_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM version_snapshot t
        WHERE t.version_id=NEW.target_version_id AND t.artifact_id=NEW.direct_artifact_id)
        THEN RAISE(ABORT,'R-DEPENDENCY-DIRECT-TARGET') END;"""
    for event in ('INSERT','UPDATE'):trigger('dependency_target_'+event.lower(),event,'version_dependency','',body)
    sql += ['CREATE INDEX version_by_artifact ON version_snapshot(artifact_id,is_issued);',
        'CREATE INDEX version_by_entry ON version_snapshot(entry_id,is_issued);',
        'CREATE INDEX version_by_predecessor ON version_snapshot(previous_version_id);',
        'CREATE INDEX dependency_by_target ON version_dependency(target_version_id);',
        '''CREATE VIEW v_issued_history AS SELECT v.version_id,v.artifact_id,v.entry_id,e.case_id,e.register_id,
          v.previous_version_id,v.payload_json,v.source_record_id,v.issued_at FROM version_snapshot v
          LEFT JOIN register_entry e ON e.entry_id=v.entry_id WHERE v.is_issued=1;''']
    rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#type'
    facts=[f"SELECT case_id AS subject,'{rdf}' AS predicate,'{RISK}RKM-X01' AS object FROM risk_case",
        f"SELECT artifact_id,'{rdf}','{RISK}'||kind FROM information_artifact",
        f"SELECT artifact_id,'{rdf}','{RISK}RKM-C014' FROM information_artifact",
        f"SELECT version_id,'{rdf}','{RISK}RKM-C015' FROM version_snapshot WHERE is_issued=1",
        f"SELECT version_id,'{rdf}','{RISK}RKM-C023' FROM version_snapshot WHERE is_issued=1 AND entry_id IS NOT NULL",
        f"SELECT entry_id,'{RISK}R-01',case_id FROM register_entry",
        f"SELECT entry_id,'{RISK}RX-008',register_id FROM register_entry",
        f"SELECT version_id,'{RISK}RX-006',artifact_id FROM version_snapshot WHERE is_issued=1",
        f"SELECT version_id,'{RISK}R-33',entry_id FROM version_snapshot WHERE is_issued=1 AND entry_id IS NOT NULL",
        f"SELECT version_id,'{RISK}R-34',previous_version_id FROM version_snapshot WHERE is_issued=1 AND previous_version_id IS NOT NULL"]
    sql.append('CREATE VIEW v_native_facts AS '+'\nUNION\n'.join(facts)+';')
    mapping=dict(schema_version='0.1.0',model_version='0.3.1',source_model_sha256=digest(path),
        native_semantics_changed=False,engine='SQLite >=3.38; foreign_keys=ON, recursive_triggers=ON',
        classes=[{'id':cid,'title':concepts[cid]['title'],'representation':rep} for cid,rep in CLASSES.items()],
        relations=[{'id':rid,'source':s,'target':t,'predicate':rels[rid]['predicate']} for rid,(s,t) in RELATIONS.items()],
        constraints=source_rows,dependency_target_kinds=SLOTS,
        dependency_scope='Supplementary version-owned effective bindings use C-25-style target checks; they are not native assessment usesVersion assertions. Full C-25 subject admission remains separate.',
        content_scope='payload_json is a supplementary serialized semantic snapshot, not a new native InformationContent instance or full RX-007 encoding.',
        lifecycle='working_draft is application staging; only sealed version_snapshot rows represent ArtifactVersion/EntryRevision in the selected native export.',
        identity='Exact governed identifiers, global case/artifact/version families and no label-based keys; aliases/splits/merges require separate explicit identity decisions.',
        schema_policy='Append-only admitted catalog/source identities in this local profile; edits are represented through new records/versions. This does not add universal ontology immutability axioms.',
        limits=['Selected identity/history slice only, not the private 128-table schema or full native admission',
                'No PostgreSQL execution, production security/concurrency/performance or backup disaster-recovery certification',
                'No formula, temporal interval, real-case acceptance or independent/owner semantic judgment',
                'Administrative DDL/PRAGMA disabling can bypass storage guards; supported configured connections and integrity checks are the contract',
                'C-25 dependency role presence and native source-subject admission are not globally established'])
    return '\n\n'.join(sql)+'\n',mapping


def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();sql,mapping=render()
    outputs={OUT/'002_guards.sql':sql,OUT/'mapping.json':json.dumps(mapping,indent=2)+'\n'}
    for path,text in outputs.items():
        if a.check:
            if not path.exists() or path.read_text()!=text:raise ValueError('Generated relational output differs: '+str(path))
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
    print(json.dumps({'classes':len(mapping['classes']),'native_relations':len(mapping['relations']),'profile':'0.1.0'}))


if __name__=='__main__':main()
