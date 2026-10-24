"""Build exact version-owned guards, mapping and readable schema contract for #29."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sqlite3

from build_relational_history import ROOT, RISK
import relational_history as base

OUT = ROOT / 'implementation/relational/0.2.0'
POLICY = OUT / 'policy.json'
NEW_TABLES = ('artifact_typing','scale_snapshot','scale_level','method_scope','assessment_snapshot','result_snapshot')
SP = 'https://github.com/ArazSaieArasi3/riskium/profiles/comparison/0.7.0#'
RDF_TYPE = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_policy():
    policy = json.loads(POLICY.read_text())
    for path, expected in policy['baseline_sha256'].items():
        if sha(ROOT / path) != expected:
            raise ValueError('Assessment baseline changed: ' + path)
    return policy


def render():
    policy = load_policy()
    model = json.loads((ROOT / 'ontology/riskium-model.json').read_text())
    classes = {c['id']: c for c in model['concepts']}
    relations = {r['id']: r for r in model['associations']}
    for cid in policy['inheritance_classes']:
        if classes[cid]['identity_supplier'] != 'RKM-C014':
            raise ValueError('Selected artifact identity changed: ' + cid)
    sql = ['-- Generated guards and selected named-graph projections; no native ontology changes.']
    def trigger(name, event, table, body, when=''):
        sql.append(f'CREATE TRIGGER {name} BEFORE {event} ON {table}' + (' WHEN ' + when if when else '') + '\nBEGIN\n' + body + '\nEND;')
    def check(condition, code):
        return "SELECT CASE WHEN " + condition + " THEN RAISE(ABORT,'" + code + "') END;"
    def kind(value, cid):
        return f"EXISTS(SELECT 1 FROM v_profile_artifact_type WHERE artifact_id={value} AND native_class='{cid}')"
    def issued(value):
        return f'EXISTS(SELECT 1 FROM version_snapshot WHERE version_id={value} AND is_issued=1)'
    def version_role(version, expected, direct=None, required=False):
        prefix = '' if required else version + ' IS NOT NULL AND '
        text = check(prefix + 'NOT ' + issued(version), 'R-ROLE-ISSUED')
        text += check(prefix + f'NOT EXISTS(SELECT 1 FROM version_snapshot v JOIN v_profile_artifact_type t ON t.artifact_id=v.artifact_id WHERE v.version_id={version} AND t.native_class=\'{expected}\')', 'R-ROLE-KIND')
        if direct:
            text += check(version + ' IS NOT NULL AND ' + direct + ' IS NOT NULL AND NOT EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=' + version + ' AND artifact_id=' + direct + ')', 'R-ROLE-TARGET')
            text += check(direct + ' IS NOT NULL AND NOT ' + kind(direct, expected), 'R-ROLE-KIND')
        return text
    sql.append('CREATE VIEW v_profile_artifact_type AS SELECT artifact_id,kind AS native_class FROM information_artifact UNION SELECT artifact_id,native_class FROM artifact_typing;')
    typed = check("NOT EXISTS(SELECT 1 FROM information_artifact WHERE artifact_id=NEW.artifact_id AND kind='RKM-C014')", 'R-TYPE-BASE-KIND')
    typed += check('EXISTS(SELECT 1 FROM version_snapshot WHERE artifact_id=NEW.artifact_id AND is_issued=1)', 'R-TYPE-ALREADY-ISSUED')
    typed += check('EXISTS(SELECT 1 FROM artifact_typing WHERE artifact_id=NEW.artifact_id)', 'R-METADATA-DUPLICATE')
    trigger('a_typing_insert', 'INSERT', 'artifact_typing', typed)
    for event in ('UPDATE','DELETE'):
        trigger('a_typing_' + event.lower(), event, 'artifact_typing', check('1', 'R-CATALOG-IMMUTABLE'))
    specs = {'scale_snapshot': ('scale_version_id', 'scale_version_id'), 'scale_level': ('level_id','scale_version_id'),
        'method_scope': ('method_version_id,scale_id,dimension_id','method_version_id'),
        'assessment_snapshot': ('assessment_version_id','assessment_version_id'), 'result_snapshot': ('result_version_id','result_version_id')}
    for table, (keys, owner) in specs.items():
        match = ' AND '.join(f'{k}=NEW.{k}' for k in keys.split(','))
        for event in ('INSERT','UPDATE','DELETE'):
            body = ''
            if event == 'INSERT':
                body += check('EXISTS(SELECT 1 FROM ' + table + ' WHERE ' + match + ')', 'R-METADATA-DUPLICATE')
            if event != 'INSERT':
                body += check(issued('OLD.' + owner), 'R-ISSUED-METADATA')
            if event != 'DELETE':
                body += check(issued('NEW.' + owner), 'R-ISSUED-METADATA')
            if table == 'result_snapshot':
                if event != 'INSERT':
                    body += check(issued('OLD.assessment_version_id'), 'R-ASSESSMENT-FROZEN')
                if event != 'DELETE':
                    body += check(issued('NEW.assessment_version_id'), 'R-ASSESSMENT-FROZEN')
            if event != 'DELETE':
                if table == 'scale_snapshot':
                    body += check("NOT EXISTS(SELECT 1 FROM version_snapshot v JOIN information_artifact a ON a.artifact_id=v.artifact_id WHERE v.version_id=NEW.scale_version_id AND v.artifact_id=NEW.scale_id AND a.kind='RKM-C036')", 'R-SCALE-VERSION-TARGET')
                    body += check('NOT ' + kind('NEW.dimension_id', 'RKM-C039'), 'R-DIMENSION-KIND')
                elif table == 'scale_level':
                    body += check('NOT ' + kind('NEW.level_id','RKM-C038'), 'R-LEVEL-KIND')
                elif table == 'method_scope':
                    body += check("NOT EXISTS(SELECT 1 FROM version_snapshot v JOIN information_artifact a ON a.artifact_id=v.artifact_id WHERE v.version_id=NEW.method_version_id AND a.kind='RKM-C035')", 'R-METHOD-VERSION-KIND')
                    body += check('NOT ' + kind('NEW.scale_id','RKM-C036') + ' OR NOT ' + kind('NEW.dimension_id','RKM-C039'), 'R-SCOPE-KIND')
                elif table == 'assessment_snapshot':
                    body += check('NOT ' + kind('NEW.assessment_id','RKM-C032') + ' OR NOT ' + kind('NEW.basis_id','RKM-C033'), 'R-ASSESSMENT-KIND')
                    body += check('NOT EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.assessment_version_id AND artifact_id=NEW.assessment_id)', 'R-OWNER-VERSION-TARGET')
                    body += version_role('NEW.context_version_id','RKM-C002','NEW.context_id',True)
                    body += version_role('NEW.method_version_id','RKM-C035','NEW.method_id')
                    body += version_role('NEW.basis_version_id','RKM-C033','NEW.basis_id')
                    for column in ('recorded_at','reference_at','valid_from','valid_to'):
                        value = 'NEW.' + column
                        invalid = f"length({value})<>20 OR {value} NOT GLOB '????-??-??T??:??:??Z' OR substr({value},1,4)<'0001' OR COALESCE(strftime('%Y-%m-%dT%H:%M:%SZ',{value},'+0 seconds'),'')<>{value}"
                        body += check(value + ' IS NOT NULL AND (' + invalid + ')','R-TIME-LEXICAL')
                    body += check('NEW.valid_from IS NOT NULL AND NEW.valid_to IS NOT NULL AND NEW.valid_to<NEW.valid_from','R-TIME-ORDER')
                elif table == 'result_snapshot':
                    body += check('NOT ' + kind('NEW.result_id','RKM-C034'), 'R-RESULT-KIND')
                    body += check('NOT EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.result_version_id AND artifact_id=NEW.result_id)', 'R-OWNER-VERSION-TARGET')
                    # NULL dimension is delegated to the explicit NOT NULL constraint.
                    body += check('NEW.dimension_id IS NOT NULL AND NOT ' + kind('NEW.dimension_id','RKM-C039'), 'R-DIMENSION-KIND')
                    body += version_role('NEW.scale_version_id','RKM-C036','NEW.scale_id')
                    body += check('NEW.dimension_id IS NOT NULL AND NEW.scale_version_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM scale_snapshot WHERE scale_version_id=NEW.scale_version_id AND dimension_id=NEW.dimension_id)', 'R-SCALE-DIMENSION')
                    body += check('NEW.level_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM scale_level WHERE level_id=NEW.level_id AND scale_version_id=NEW.scale_version_id)', 'R-LEVEL-VERSION')
                    body += check('EXISTS(SELECT 1 FROM result_snapshot old JOIN assessment_snapshot a ON a.assessment_version_id=old.assessment_version_id JOIN assessment_snapshot n ON n.assessment_version_id=NEW.assessment_version_id WHERE old.result_id=NEW.result_id AND a.assessment_id<>n.assessment_id)', 'R-RESULT-PARENT-IDENTITY')
                    body += check("NEW.score_kind='COMPUTED'", 'R-COMPUTATION-UNSUPPORTED')
                    body += check("NEW.score_kind NOT IN ('REPORTED','UNKNOWN','COMPUTED')", 'R-SCORE-KIND')
                    body += check("NEW.score_kind='REPORTED' AND (NEW.reported_value IS NULL OR length(trim(NEW.reported_value))=0)", 'R-REPORTED-VALUE')
                    body += check("NEW.score_kind='UNKNOWN' AND NEW.reported_value IS NOT NULL", 'R-UNKNOWN-VALUE')
                    body += check('length(trim(NEW.source_locator))=0 OR length(trim(NEW.interpretation_origin))=0', 'R-SOURCE-QUALIFIER')
            trigger('a_' + table + '_' + event.lower(), event, table, body)
    seal = check("NEW.issued_at IS NOT NULL AND (length(NEW.issued_at)<>20 OR substr(NEW.issued_at,1,4)<'0001' OR NEW.issued_at NOT GLOB '????-??-??T??:??:??Z' OR COALESCE(strftime('%Y-%m-%dT%H:%M:%SZ',NEW.issued_at,'+0 seconds'),'')<>NEW.issued_at)", 'R-TIME-LEXICAL')
    for cid, table, key in (('RKM-C032','assessment_snapshot','assessment_version_id'),('RKM-C034','result_snapshot','result_version_id')):
        seal += check(kind('NEW.artifact_id',cid) + f' AND NOT EXISTS(SELECT 1 FROM {table} WHERE {key}=NEW.version_id)', 'R-ISSUE-METADATA-REQUIRED')
    seal += check('EXISTS(SELECT 1 FROM assessment_snapshot a JOIN result_snapshot r ON r.assessment_version_id=a.assessment_version_id JOIN version_snapshot v ON v.version_id=r.result_version_id WHERE a.assessment_version_id=NEW.version_id AND v.is_issued<>1)', 'R-UNSEALED-RESULT')
    for table, key, artifact in (('assessment_snapshot','assessment_version_id','assessment_id'),('result_snapshot','result_version_id','result_id'),('scale_snapshot','scale_version_id','scale_id')):
        seal += check(f'EXISTS(SELECT 1 FROM {table} WHERE {key}=NEW.version_id AND {artifact}<>NEW.artifact_id)', 'R-OWNER-VERSION-TARGET')
    metadata_columns={
        'assessment_snapshot':('assessment_version_id','assessment_id','basis_id','basis_version_id','context_id','context_version_id','method_id','method_version_id','temporal_context_id','recorded_at','reference_at','valid_from','valid_to','source_record_id'),
        'result_snapshot':('result_version_id','result_id','assessment_version_id','dimension_id','scale_id','scale_version_id','level_id','score_kind','reported_value','source_record_id','source_locator','interpretation_origin')}
    for table, columns in metadata_columns.items():
        differences=' OR '.join(f"json_type(NEW.payload_json,'$.{col}') IS NULL OR json_extract(NEW.payload_json,'$.{col}') IS NOT m.{col}" for col in columns)
        seal+=check(f'EXISTS(SELECT 1 FROM {table} m WHERE m.{columns[0]}=NEW.version_id AND ({differences}))','R-PAYLOAD-METADATA-MISMATCH')
    trigger('a_snapshot_seal','UPDATE','version_snapshot',seal,'OLD.is_issued=0 AND NEW.is_issued=1')
    sql.append("""CREATE VIEW v_assessment_frame AS SELECT r.result_version_id,r.result_id,r.assessment_version_id,a.assessment_id,
      a.context_id,a.context_version_id,a.method_id,a.method_version_id,a.basis_id,a.basis_version_id,a.temporal_context_id,
      a.recorded_at,a.reference_at,a.valid_from,a.valid_to,r.dimension_id,r.scale_id,r.scale_version_id,r.level_id,
      r.score_kind,r.reported_value,r.source_record_id,a.source_record_id AS assessment_source_record_id,r.source_locator,r.interpretation_origin
      FROM result_snapshot r JOIN assessment_snapshot a USING(assessment_version_id)
      JOIN version_snapshot av ON av.version_id=a.assessment_version_id AND av.is_issued=1
      JOIN version_snapshot rv ON rv.version_id=r.result_version_id AND rv.is_issued=1;""")
    # All exported objects are IRIs. Supplied lexical values remain SQL/provenance
    # data; they never become an invented native score predicate.
    quads = []
    def fact(subject, predicate, obj, extra='', condition='1'):
        quads.append(f"SELECT f.assessment_version_id AS graph_id,{subject} AS subject,'{predicate}' AS predicate,{obj} AS object FROM v_assessment_frame f {extra} WHERE {condition} AND {subject} IS NOT NULL AND {obj} IS NOT NULL")
    for column, cid in (('assessment_id','RKM-C032'),('result_id','RKM-C034'),('basis_id','RKM-C033'),('dimension_id','RKM-C039'),('level_id','RKM-C038'),('context_id','RKM-C002'),('method_id','RKM-C035'),('scale_id','RKM-C036')):
        fact('f.'+column,RDF_TYPE,"'"+RISK+cid+"'")
        fact('f.'+column,RDF_TYPE,"'"+RISK+'RKM-C014'+"'")
    for sid,rid,oid in (('assessment_id','R-12','basis_id'),('assessment_id','R-13','result_id'),('assessment_id','R-45','context_id'),('assessment_id','R-46','method_id'),('assessment_id','RX-014','context_version_id'),('assessment_id','RX-015','method_version_id'),('result_id','R-14','scale_id'),('result_id','R-15','level_id'),('result_id','R-48','dimension_id'),('result_id','RX-016','scale_version_id')):
        fact('f.'+sid,RISK+rid,'f.'+oid)
    for column in ('assessment_version_id','result_version_id','context_version_id','method_version_id','basis_version_id','scale_version_id'):
        fact('f.'+column,RDF_TYPE,"'"+RISK+'RKM-C015'+"'")
        fact('f.'+column,RISK+'RX-006','v.artifact_id',f'JOIN version_snapshot v ON v.version_id=f.{column}')
        # Known version-target typing is independent of whether the caller
        # supplied an optional direct artifact edge. Preserve both facts.
        join=f'JOIN version_snapshot v ON v.version_id=f.{column} JOIN v_profile_artifact_type t ON t.artifact_id=v.artifact_id'
        fact('v.artifact_id',RDF_TYPE,"'"+RISK+"'||t.native_class",join)
        fact('v.artifact_id',RDF_TYPE,"'"+RISK+'RKM-C014'+"'",join)
    fact('f.level_id',RISK+'R-16','s.scale_id','JOIN scale_level l ON l.level_id=f.level_id JOIN scale_snapshot s ON s.scale_version_id=l.scale_version_id')
    fact('f.scale_id',RISK+'RK2-019','s.dimension_id','JOIN scale_snapshot s ON s.scale_version_id=f.scale_version_id')
    fact('f.method_id',RISK+'R-49','m.scale_id','JOIN method_scope m ON m.method_version_id=f.method_version_id')
    fact('f.method_id',RISK+'RK2-018','m.dimension_id','JOIN method_scope m ON m.method_version_id=f.method_version_id')
    for sid, prop, oid in (('assessment_id','basisVersion','basis_version_id'),('assessment_id','temporalContext','temporal_context_id'),('assessment_id','source','assessment_source_record_id'),('level_id','levelScaleVersion','scale_version_id')):
        fact('f.'+sid,SP+prop,'f.'+oid)
    sql.append('CREATE VIEW v_assessment_quads AS\n'+'\nUNION\n'.join(quads)+';')
    # Review index necessity from actual FK prefixes; avoid redundant indexes
    # already supplied by an existing PK or UNIQUE key.
    c = base.connect(); base.migrate(c)
    base.execute_script(c,(OUT/'003_assessment_tables.sql').read_text())
    for table, in c.execute("SELECT name FROM sqlite_schema WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name").fetchall():
        indexed = [(tuple(r[2] for r in c.execute('PRAGMA index_info('+row[1]+')')),bool(row[2])) for row in c.execute('PRAGMA index_list('+table+')').fetchall()]
        groups = {}
        for fk in c.execute('PRAGMA foreign_key_list('+table+')'):
            groups.setdefault(fk[0],[]).append((fk[1],fk[3]))
        for values in groups.values():
            cols=tuple(v for _,v in sorted(values))
            # A unique key contained in the FK already limits lookup to one
            # candidate row; another wider index would add write/storage cost.
            if not any(i[:len(cols)]==cols or unique and set(i).issubset(cols) for i,unique in indexed):
                name='a_fk_'+table+'_'+'_'.join(cols)
                sql.append('CREATE INDEX '+name+' ON '+table+'('+','.join(cols)+');')
                indexed.append((cols,False))
    c.close()
    mapped_classes=[dict(id=cid,source_sha256=hashlib.sha256(json.dumps(classes[cid],sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest(),representation='information_artifact identity + artifact_typing exact native membership') for cid in policy['inheritance_classes']]
    mapped_relations=[{k:relations[rid][k] for k in ('id','source','target','predicate','source_end_cardinality','target_end_cardinality')} for rid in policy['native_relation_ids']]
    mapping=dict(schema='riskium-assessment-relational-mapping-v1',profile_version='0.2.0',migration=3,model_version='0.3.1',source_model_sha256=sha(ROOT/'ontology/riskium-model.json'),policy_sha256=sha(POLICY),base_mapping='implementation/relational/0.1.0/mapping.json',new_classes=mapped_classes,new_relations=mapped_relations,
        native_export='v_assessment_quads, one named graph per issued assessment version; base v_native_facts remains available for the original identity/history slice.',
        supplemental_columns=['source_record_id','source_locator','interpretation_origin','recorded_at','reference_at','valid_from','valid_to','temporal_context_id','basis_version_id','score_kind','reported_value','scheme_uri','scheme_edition','local_code'],
        limits=policy['scope_limits'])
    ttl='''@prefix rr: <http://www.w3.org/ns/r2rml#> .
@prefix map: <urn:riskium:assessment-mapping:> .
map:SelectedAssessment a rr:TriplesMap ;
  rr:logicalTable [ rr:tableName "v_assessment_quads" ] ;
  rr:subjectMap [ rr:column "subject" ; rr:termType rr:IRI ;
    rr:graphMap [ rr:column "graph_id" ; rr:termType rr:IRI ] ] ;
  rr:predicateObjectMap [
    rr:predicateMap [ rr:column "predicate" ; rr:termType rr:IRI ] ;
    rr:objectMap [ rr:column "object" ; rr:termType rr:IRI ] ] .
'''
    return {'003_assessment_guards.sql':'\n\n'.join(sql)+'\n','mapping.json':json.dumps(mapping,indent=2)+'\n','mapping.ttl':ttl}


def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
    for name,text in render().items():
        path=OUT/name
        if args.check:
            if not path.exists() or path.read_text()!=text:
                raise ValueError('Generated assessment mapping differs: '+name)
        else:path.write_text(text)
    print(json.dumps(dict(profile='0.2.0',new_tables=6,new_classes=5,new_relations=14,migration=3)))


if __name__=='__main__':main()
