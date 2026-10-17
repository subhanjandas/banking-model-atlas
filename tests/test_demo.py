"""Real SQL execution, including deliberately incorrect financial records."""
import sys
import unittest
from pathlib import Path
import duckdb
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from run_demo import database, report, violations, CHECKS, MODEL, FIXTURE

class DemoTests(unittest.TestCase):
    def test_balances_and_schema(self):
        with database() as db:
            result=report(db)
            self.assertEqual(result['closing_balances'],{'D1':'2000.00','D2':'0.00','CC1':'50.00','LN1':'900.00'})
            self.assertEqual(len(db.execute('SHOW TABLES').fetchall()),81)
    def test_check_metadata(self):
        self.assertEqual(len({c['id'] for c in CHECKS}),27)
        for e in MODEL['entities']:
            self.assertEqual(e['example_coverage']=='sample_records',bool(FIXTURE['tables'].get(e['id'])))
        rules={r['id'] for r in MODEL['rules']}
        for c in CHECKS:
            self.assertTrue(c['coverage_limit'])
            self.assertTrue(set(c['rule_ids'])<=rules)
    def test_foreign_key_is_enforced(self):
        with database() as db:
            with self.assertRaises(duckdb.ConstraintException):
                db.execute("UPDATE posting_link SET account_entry_id='missing'")

MUTATIONS={
'C20':"UPDATE payment_return SET amount=46 WHERE payment_return_id='RET2'",
'C21':"UPDATE account_entry SET amount=44 WHERE account_entry_id='E_RETURN2'",
'C22':"UPDATE payment_event SET status='RETURNED' WHERE payment_event_id='PO_OUT_PARTIAL'",
'C23':"UPDATE fraud_decision SET decided_at='2026-09-01T10:00:00'",
'C24':"UPDATE promise_to_pay SET due_on='2026-10-01'",
'C25':"UPDATE reward_balance_snapshot SET points_balance=61",
'C26':"UPDATE reward_earn SET points=-120",
'C27':"UPDATE complaint_resolution SET resolved_on='2026-09-01'",
'C14':"UPDATE account_entry SET amount=249 WHERE account_entry_id='REV_E_TD'",
'C15':"UPDATE payment_event SET status='REVERSED' WHERE payment_event_id='PO_OUT_END'",
'C16':"UPDATE payment_event SET status='FAILED' WHERE payment_event_id='PO_OUT1'",
'C17':"UPDATE account_status_event SET status='CLOSED' WHERE account_status_event_id='D2_RESTRICTED'",
'C18':"UPDATE card_status_event SET status='CLOSED' WHERE card_status_event_id='CARD_BLOCKED'",
'C19':"DELETE FROM posting_link WHERE posting_link_id='MAP_E_PUR'",
'C01':"UPDATE journal_line SET amount=119 WHERE journal_line_id='J_PUR_1'",
'C02':"UPDATE journal_line SET direction='CREDIT' WHERE journal_line_id='J_PUR_1'",
'C03':"UPDATE posting_link SET allocated_amount=121 WHERE posting_link_id='MAP_E_PUR'",
'C04':"UPDATE statement SET closing_balance=51",
'C05':"UPDATE account_entry SET posted_on='2025-01-01' WHERE account_entry_id='E_PUR'",
'C06':"UPDATE card_transaction SET amount=130 WHERE card_transaction_id='REF1'",
'C07':"UPDATE payment_order SET amount=251 WHERE payment_order_id='PO_INT'",
'C08':"UPDATE payment_settlement SET settled_amount=74 WHERE payment_settlement_id='SET1'",
'C09':"UPDATE loan_schedule_item SET principal_due=99 WHERE loan_schedule_item_id='LS1'",
'C10':"UPDATE account_entry SET amount=999 WHERE account_entry_id='E_LD'",
'C11':"UPDATE account_entry SET amount=99 WHERE account_entry_id='E_LR'",
'C12':"UPDATE account_entry SET kind='ADJUSTMENT' WHERE account_entry_id='E_PUR'",
'C13':"UPDATE account_entry SET amount=-1 WHERE account_entry_id='E_PUR'",
}
def mutation_test(check,sql):
    def test(self):
        with database() as db:
            db.execute(sql)
            self.assertTrue(violations(db)[check],f'{check} failed to detect its bad-data fixture')
    return test
for check,sql in MUTATIONS.items():setattr(DemoTests,'test_reject_'+check,mutation_test(check,sql))
