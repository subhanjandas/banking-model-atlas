import copy
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from engineering.pipeline import ROOT, connect, initialize, apply_batch, snapshot, backfill, reader, migrate
from engineering.evidence import batch, generate
from engineering.contracts import breaking_changes
from scripts.ingest_returns import BatchRejected, fingerprint

class EngineeringTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name)/'state.sqlite'
        self.db = connect(self.path)
        self.payments = json.loads((ROOT/'fixtures/banking_scenarios.json').read_text())['tables']['payment_order']
        initialize(self.db, self.payments)
    def tearDown(self):
        self.db.close(); self.tmp.cleanup()
    def state(self):
        return snapshot(self.db, '2026-09-30T23:59:59Z')
    def initial(self):
        return apply_batch(self.db, *batch('initial'))
    def test_restart_and_correction(self):
        self.initial(); self.db.close(); self.db = connect(self.path)
        result = apply_batch(self.db, *batch('correction'))
        self.assertEqual(result['affected_days'], ['2026-09-28'])
        self.assertEqual(sum(x['return_amount'] for x in self.state()['daily']), 7500)
        self.assertTrue(self.state()['reconciled'])
        self.assertEqual(self.state()['checkpoint'], 2)
    def test_exact_replay_does_not_advance_checkpoint(self):
        self.initial(); original = self.state()
        self.assertEqual(self.initial()['status'], 'replayed')
        self.assertEqual(original, self.state())
    def test_reordered_deliveries_replay(self):
        self.initial(); rows,m = batch('initial')
        self.assertEqual(apply_batch(self.db,list(reversed(rows)),m)['status'],'replayed')
    def test_out_of_order_version_never_downgrades(self):
        apply_batch(self.db, *batch('correction')); self.initial()
        self.assertEqual(self.db.execute("SELECT amount FROM current_returns WHERE key='RET2'").fetchone()[0],4500)
    def test_missing_source_keeps_last_good_projection(self):
        self.initial(); before=self.state()
        with self.assertRaises(BatchRejected): apply_batch(self.db, [], batch('correction')[1])
        after=self.state()
        self.assertEqual(before['daily_sha256'],after['daily_sha256'])
        self.assertEqual(after['latest_attempt'],'rejected')
        self.assertGreater(self.db.execute('SELECT COUNT(*) FROM quarantine').fetchone()[0],0)
    def test_cross_batch_revision_conflict(self):
        self.initial(); rows,m=batch('initial'); rows[0]['payload']['amount']='29.00'
        for v in m['expected_versions']:
            if v['key']==rows[0]['key']: v['sha256']=fingerprint(rows[0])
        m['expected_revision_amount_total']='59.00'; m['batch_id']='CONFLICT'
        with self.assertRaisesRegex(BatchRejected,'REVISION_CONFLICT|DELIVERY_ID_CONFLICT'): apply_batch(self.db,rows,m)
        self.assertEqual(self.state()['checkpoint'],1)
    def test_changed_batch_id_content_rejected(self):
        self.initial(); rows,m=batch('initial'); rows[0]['delivery_id']='NEW'
        with self.assertRaisesRegex(BatchRejected,'BATCH_ID_CONFLICT'): apply_batch(self.db,rows,m)
    def test_over_return_rejected_atomically(self):
        self.initial(); rows,m=batch('correction'); rows[0]['payload']['amount']='46.00'
        m['expected_versions'][0]['sha256']=fingerprint(rows[0]);m['expected_revision_amount_total']='46.00'
        with self.assertRaisesRegex(BatchRejected,'OVER_RETURN'): apply_batch(self.db,rows,m)
        self.assertEqual(self.state()['source_versions'],2)
    def test_exception_rolls_back_projection_and_checkpoint(self):
        self.initial(); before=self.state()
        def fail(): raise RuntimeError('injected')
        with self.assertRaises(RuntimeError): apply_batch(self.db,*batch('correction'),failpoint=fail)
        self.assertEqual(before['daily_sha256'],self.state()['daily_sha256'])
        self.assertEqual(before['checkpoint'],self.state()['checkpoint'])
    def test_abrupt_process_death_rolls_back_and_retry_recovers(self):
        self.initial()
        code='''import os,sys
from engineering.pipeline import connect,apply_batch
from engineering.evidence import batch
db=connect(sys.argv[1])
apply_batch(db,*batch('correction'),failpoint=lambda:os._exit(17))
'''
        result=subprocess.run([sys.executable,'-c',code,str(self.path)],cwd=ROOT)
        self.assertEqual(result.returncode,17)
        self.assertEqual(self.state()['checkpoint'],1)
        self.assertEqual(self.state()['source_versions'],2)
        apply_batch(self.db,*batch('correction'))
        self.assertEqual(self.state()['checkpoint'],2)
    def test_date_correction_rebuilds_old_and_new_partition(self):
        self.initial(); rows,m=batch('correction');r=rows[0]
        r['event_at']='2026-09-27T12:00:00Z'; r['payload']['returned_on']='2026-09-27'
        m['expected_versions'][0]['sha256']=fingerprint(r)
        result=apply_batch(self.db,rows,m)
        self.assertEqual(result['affected_days'],['2026-09-27','2026-09-28'])
        self.assertNotIn('2026-09-28',[x['day'] for x in self.state()['daily']])
    def test_backfill_is_bounded_and_preserves_result(self):
        self.initial(); before=self.state()['daily_sha256']
        backfill(self.db,'2026-09-01','2026-09-30')
        self.assertEqual(before,self.state()['daily_sha256'])
        with self.assertRaises(ValueError):backfill(self.db,'2026-01-01','2026-12-31')
    def test_no_fanout_and_explicit_grain(self):
        self.initial();apply_batch(self.db,*batch('correction'))
        daily=self.state()['daily']
        self.assertEqual(sum(x['payment_amount'] for x in daily),7500)
        self.assertEqual(sum(x['payment_count'] for x in daily),1)
        self.assertEqual(sum(x['return_count'] for x in daily),2)
        self.assertEqual(len({(x['day'],x['channel'],x['currency']) for x in daily}),len(daily))
    def test_stale_clock_and_future_receipt_alert(self):
        self.initial()
        for at in ['2026-10-05T00:00:00Z','2026-09-01T00:00:00Z']:
            self.assertEqual(snapshot(self.db,at)['freshness'],'alert')
    def test_payment_snapshot_cannot_silently_change(self):
        changed=copy.deepcopy(self.payments);changed[1]['amount']='80.00'
        with self.assertRaises(ValueError): initialize(self.db,changed)
    def test_analyst_denied_raw_and_writes(self):
        self.initial();db=reader(self.path,'analyst')
        try:
            self.assertEqual(db.execute('SELECT SUM(payment_amount) FROM daily').fetchone()[0],7500)
            for sql in ['SELECT * FROM versions','SELECT * FROM payments','DELETE FROM daily','PRAGMA user_version',"ATTACH ':memory:' AS other"]:
                with self.assertRaises(sqlite3.DatabaseError):db.execute(sql)
        finally:db.close()
    def test_auditor_readonly_and_unknown_role_denied(self):
        self.initial();db=reader(self.path,'auditor')
        try:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM versions').fetchone()[0],2)
            with self.assertRaises(sqlite3.DatabaseError):db.execute('DELETE FROM versions')
        finally:db.close()
        with self.assertRaises(ValueError):reader(self.path,'admin')
    def test_v1_migration_preserves_data(self):
        self.initial();self.db.execute('ALTER TABLE runs DROP COLUMN operator_note')
        self.db.execute('DROP INDEX current_return_day');self.db.execute('PRAGMA user_version=1')
        before=self.state()['daily_sha256'];migrate(self.db);migrate(self.db)
        self.assertEqual(before,self.state()['daily_sha256'])
        self.assertEqual(self.db.execute('PRAGMA user_version').fetchone()[0],2)
    def test_future_database_version_rejected(self):
        self.db.execute('PRAGMA user_version=999')
        with self.assertRaises(ValueError):migrate(self.db)
        self.assertEqual(self.db.execute('PRAGMA user_version').fetchone()[0],999)
    def test_contract_breaking_and_optional_addition(self):
        old=json.loads((ROOT/'engineering/contract.json').read_text());new=copy.deepcopy(old)
        new['fields']['note']={'type':'STRING','required':False}
        self.assertEqual(breaking_changes(old,new),[])
        new['fields']['note']['required']=True
        new['fields']['payment_amount']['type']='FLOAT';del new['fields']['day']
        self.assertEqual(len(breaking_changes(old,new)),3)
    def test_evidence_is_reproducible(self):
        self.assertEqual(generate(),generate())

if __name__=='__main__':unittest.main()
