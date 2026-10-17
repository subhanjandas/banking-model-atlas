"""Failure, replay, revision and completeness behavior at the input boundary."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from ingest_returns import inputs,process,publish,BatchRejected

class IngestionTests(unittest.TestCase):
    def setUp(self):self.rows,self.manifest=inputs()
    def rejected(self,rows,code,manifest=None):
        with self.assertRaises(BatchRejected) as caught:process(rows,manifest or self.manifest)
        self.assertIn(code,[i['code'] for i in caught.exception.issues])
    def test_valid_batch(self):
        r=process(self.rows,self.manifest)
        self.assertEqual((r['distinct_source_versions'],r['duplicate_deliveries'],r['late_versions']),(3,1,2))
        self.assertEqual((r['revision_control_total'],r['curated_total']),('115.00','75.00'))
    def test_as_of_revision(self):
        before=process(self.rows,self.manifest,'2026-09-29T23:59:59Z')
        after=process(self.rows,self.manifest,'2026-09-30T23:59:59Z')
        self.assertEqual(before['curated_total'],'70.00');self.assertEqual(before['selected_versions']['RET2'],1)
        self.assertEqual(after['curated_total'],'75.00');self.assertEqual(after['selected_versions']['RET2'],2)
    def test_out_of_order_arrival(self):self.assertEqual(process(self.rows,self.manifest),process(list(reversed(self.rows)),self.manifest))
    def test_repeated_delivery_does_not_duplicate_finances(self):
        r=process(self.rows*2,self.manifest);self.assertEqual(r['curated_total'],'75.00');self.assertEqual(r['duplicate_deliveries'],5)
    def test_missing_revision(self):self.rejected([r for r in self.rows if r['version']!=2],'MISSING_SOURCE_RECORDS')
    def test_wrong_control_total(self):
        self.manifest['expected_revision_amount_total']='114.00';self.rejected(self.rows,'SOURCE_CONTROL_TOTAL')
    def test_conflicting_revision(self):
        bad=copy.deepcopy(self.rows[0]);bad['delivery_id']='CONFLICT';bad['payload']['amount']='41.00'
        self.rejected(self.rows+[bad],'REVISION_CONFLICT')
    def test_same_count_wrong_payload(self):
        self.rows[0]['payload']['external_reference']='ALTERED';self.rejected(self.rows,'SOURCE_HASH_MISMATCH')
    def test_unknown_field(self):
        self.rows[0]['payload']['unexpected_column']='x';self.rejected(self.rows,'INVALID_RECORD')
    def test_float_money_rejected(self):
        self.rows[0]['payload']['amount']=40.0;self.rejected(self.rows,'INVALID_RECORD')
    def test_unsupported_contract(self):
        self.rows[0]['contract']='v2';self.rejected(self.rows,'INVALID_RECORD')
    def test_manifest_contract(self):
        self.manifest['contract']='v2';self.rejected(self.rows,'MANIFEST_CONTRACT')
    def test_source_event_after_receipt(self):
        self.rows[0]['event_at']='2026-10-01T12:00:00Z';self.rejected(self.rows,'INVALID_RECORD')
    def test_failed_batch_preserves_last_good_publication(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'curated.json';publish(self.rows,self.manifest,path);before=path.read_bytes()
            with self.assertRaises(BatchRejected):publish(self.rows[:1],self.manifest,path)
            self.assertEqual(path.read_bytes(),before)
            self.assertEqual(len(list(Path(d).iterdir())),1)
    def test_publish_twice_is_byte_identical(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'curated.json';publish(self.rows,self.manifest,p);before=p.read_bytes()
            publish(list(reversed(self.rows)),self.manifest,p);self.assertEqual(p.read_bytes(),before)
    def test_projection_matches_independent_bank_fixture(self):
        fixture=json.loads((Path(__file__).resolve().parents[1]/'fixtures/banking_scenarios.json').read_text())
        self.assertEqual(process(self.rows,self.manifest)['curated_rows'],fixture['tables']['payment_return'])
