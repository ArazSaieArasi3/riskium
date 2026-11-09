"""Tests for the explicitly bounded sidecar, not production database acceptance."""
import copy
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from rdflib import Graph, URIRef
from rdflib.namespace import RDF
from rdflib.compare import isomorphic
import relational_use as m


class SidecarUse(unittest.TestCase):
    def setUp(self):
        self.source=m.fixture_source.fresh();m.fixture_source.populate(self.source)
        self.before=m.fixture_source.state_hash(self.source)
        self.db=m.connect();m.initialize(self.source,self.db)
        self.f=json.loads((m.HERE/'fixtures.json').read_text())

    def tearDown(self):
        self.assertEqual(m.fixture_source.state_hash(self.source),self.before)
        m.legacy.health(self.source);self.source.close();self.db.close()

    def prepare(self):
        for g in self.f['groundings']:m.add_grounding(self.db,g)

    def populate(self):
        self.prepare()
        for u in self.f['uses']:m.record_use(self.db,u)

    def reject(self,record):
        before=m.snapshot(self.db)
        with self.assertRaises((ValueError,sqlite3.IntegrityError)):
            m.record_use(self.db,record)
        self.assertEqual(m.snapshot(self.db),before)
        m.health(self.db)

    def test_documentary_import_never_creates_use_or_roles(self):
        self.assertEqual(self.db.execute('SELECT count(*) FROM reference_snapshot').fetchone()[0],4)
        self.assertEqual(m.rows(self.db),[])
        for (version,) in self.db.execute('SELECT version_id FROM reference_snapshot'):
            g=m.information_graph(self.db,version)
            for kind in ['RKM-C075','RKM-C076','RKM-C066']:
                self.assertFalse(list(g.subjects(RDF.type,m.RISK[kind])))

    def test_three_explicit_purposes_and_exact_version_pins(self):
        self.populate();rows=m.rows(self.db)
        self.assertEqual([r[-1] for r in rows],['support','challenge','context'])
        self.assertNotEqual(rows[0][2],rows[1][2]);self.assertNotEqual(rows[0][4],rows[1][4])
        for row in rows:
            graph=m.use_graph(self.db,row[0]);use,ref,_,item,_,ctx,_,ground,_,_=row
            for p,v in [('RE-001',item),('RE-002',ref),('RE-003',ground)]:
                self.assertIn((URIRef(use),m.RISK[p],URIRef(v)),graph)
            self.assertIn((URIRef(use),m.EU.context,URIRef(ctx)),graph)

    def test_information_only_reference_survives_after_other_uses(self):
        self.populate()
        graph=m.information_graph(self.db,'urn:riskium:evidence:ref-c-v1')
        self.assertNotIn((URIRef('urn:riskium:evidence:item-b'),RDF.type,m.RISK['RKM-C066']),graph)
        self.assertNotIn((URIRef('urn:riskium:evidence:ref-c'),RDF.type,m.RISK['RKM-C076']),graph)

    def test_sql_sparql_selected_query_parity(self):
        self.populate();graph=Graph()
        for u in self.f['uses']:graph+=m.use_graph(self.db,u['id'])
        actual=[[str(x) for x in row] for row in graph.query((m.HERE/'query.rq').read_text())]
        self.assertEqual(actual,m.rows(self.db))

    def test_purpose_terms_match_the_pinned_shape_enumeration(self):
        from rdflib.namespace import SH
        from rdflib.collection import Collection
        shapes=Graph().parse(m.HERE.parent/'issue93-integration/combined-managed.shacl.ttl',format='turtle')
        prop=next(p for p in shapes.objects(m.EU.EvidenceUseShape,SH.property) if shapes.value(p,SH.path)==m.EU.purpose)
        choices=set(Collection(shapes,shapes.value(prop,SH['in'])))
        self.populate()
        for u in self.f['uses']:self.assertIn(m.use_graph(self.db,u['id']).value(URIRef(u['id']),m.EU.purpose),choices)

    def test_missing_grounding_and_unknown_reference_rejected(self):
        self.prepare()
        for key in ['grounding_version','reference_version']:
            r=copy.deepcopy(self.f['uses'][0]);r[key]='urn:missing:record';self.reject(r)

    def test_missing_field_and_blank_justification_rejected(self):
        self.prepare();r=copy.deepcopy(self.f['uses'][0]);del r['grounding_version'];self.reject(r)
        r=copy.deepcopy(self.f['uses'][0]);r['justification']=' ';self.reject(r)

    def test_wrong_item_and_unrecorded_context_rejected(self):
        self.prepare()
        for key,value in [('item_version','urn:riskium:evidence:item-a-v2'),('context_version','urn:riskium:knowledge:scenario-b-v1')]:
            r=copy.deepcopy(self.f['uses'][0]);r[key]=value;self.reject(r)

    def test_bad_purpose_and_impossible_date_rejected(self):
        self.prepare()
        for key,value in [('purpose','proves-true'),('recorded_at','2026-02-30T09:00:00Z')]:
            r=copy.deepcopy(self.f['uses'][0]);r[key]=value;self.reject(r)

    def test_duplicate_id_and_exact_episode_tuple_rejected(self):
        self.prepare();m.record_use(self.db,self.f['uses'][0]);self.reject(self.f['uses'][0])
        r=copy.deepcopy(self.f['uses'][0]);r['id']='urn:synthetic:duplicate';self.reject(r)

    def test_declared_direct_alias_rejected(self):
        self.prepare();m.add_alias(self.db,'urn:riskium:evidence:ref-a','urn:riskium:evidence:item-a')
        self.reject(self.f['uses'][0])

    def test_declared_transitive_alias_rejected(self):
        self.prepare();m.add_alias(self.db,'urn:riskium:evidence:ref-a','urn:riskium:evidence:ref-b')
        m.add_alias(self.db,'urn:riskium:evidence:item-a','urn:riskium:evidence:ref-b')
        self.reject(self.f['uses'][0])

    def test_late_alias_cannot_invalidate_recorded_use(self):
        self.populate();before=m.snapshot(self.db)
        with self.assertRaises(sqlite3.IntegrityError):m.add_alias(self.db,'urn:riskium:evidence:ref-a','urn:riskium:evidence:item-a')
        self.assertEqual(m.snapshot(self.db),before)

    def test_sql_layer_rejects_mismatch_without_api(self):
        self.prepare();r=copy.deepcopy(self.f['uses'][0]);r['item_version']='urn:riskium:evidence:item-a-v2'
        with self.assertRaisesRegex(sqlite3.IntegrityError,'R-EU-COHERENCE'):
            self.db.execute('INSERT INTO evidence_use VALUES(?,?,?,?,?,?,?,?)',tuple(r[k] for k in m.USE_FIELDS))
        self.assertEqual(m.rows(self.db),[])

    def test_append_only_records_and_replace_are_rejected(self):
        self.populate();before=m.snapshot(self.db)
        for sql in ['UPDATE evidence_use SET purpose=\'challenge\'','DELETE FROM evidence_use','INSERT OR REPLACE INTO evidence_use SELECT * FROM evidence_use']:
            with self.assertRaises(sqlite3.IntegrityError):self.db.execute(sql)
            self.assertEqual(m.snapshot(self.db),before)

    def test_source_snapshot_and_schema_drift_are_detected(self):
        self.db.execute('DROP TRIGGER reference_snapshot_update')
        with self.assertRaisesRegex(ValueError,'R-EU-SCHEMA'):m.health(self.db)

    def test_configuration_off_is_rejected(self):
        self.db.execute('PRAGMA foreign_keys=OFF')
        with self.assertRaisesRegex(ValueError,'R-EU-CONNECTION'):m.health(self.db)

    def test_backup_reopen_and_dump_restore_preserve_graph(self):
        self.populate();before=m.snapshot(self.db);g=m.use_graph(self.db,self.f['uses'][0]['id'])
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'test.sqlite';target=m.connect(path);self.db.backup(target);target.close()
            target=m.connect(path);m.health(target);self.assertEqual(m.snapshot(target),before)
            self.assertTrue(isomorphic(m.use_graph(target,self.f['uses'][0]['id']),g));target.close()
        target=m.connect();m.restore_dump(target,'\n'.join(self.db.iterdump()));m.health(target)
        self.assertEqual(m.snapshot(target),before);target.close()

    def test_tampered_dump_rolls_back_before_acceptance(self):
        self.populate();text='\n'.join(self.db.iterdump())
        changed=text.replace(",'support','2026-",",'proves-true','2026-")
        self.assertNotEqual(text,changed)
        target=m.connect()
        with self.assertRaises((ValueError,sqlite3.IntegrityError)):m.restore_dump(target,changed)
        self.assertFalse(target.execute("SELECT 1 FROM sqlite_master WHERE type='table'").fetchone())
        target.close()

    def test_nonempty_sidecar_reinitialization_rejected(self):
        before=m.snapshot(self.db)
        with self.assertRaisesRegex(ValueError,'EMPTY-SIDECAR'):m.initialize(self.source,self.db)
        self.assertEqual(m.snapshot(self.db),before)

    def test_changed_proposed_purpose_is_not_required_for_actual_use(self):
        self.prepare();r=copy.deepcopy(self.f['uses'][0]);r['purpose']='challenge';m.record_use(self.db,r)
        self.assertEqual(m.rows(self.db)[0][-1],'challenge')
        self.assertEqual(self.db.execute('SELECT proposed_purpose FROM reference_snapshot WHERE version_id=?',(r['reference_version'],)).fetchone()[0],'support')


if __name__=='__main__':unittest.main()
