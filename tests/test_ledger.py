"""Independent closing positions must detect balanced but incorrect books."""
import unittest
from test_demo import database
from run_demo import FIXTURE
from reconcile_ledger import reconcile

class LedgerTests(unittest.TestCase):
    def test_complete_period(self):
        with database() as db:
            result=reconcile(db,FIXTURE['period'])
            self.assertEqual(result['ledger_accounts']['G_CASH']['closing'],'1160.00')
            self.assertEqual(result['trial_balance_difference'],'0.00')
    def test_missing_snapshot(self):
        with database() as db:
            db.execute("DELETE FROM gl_balance_snapshot WHERE gl_account_id='G_CASH' AND as_of_date='2026-09-30'")
            with self.assertRaisesRegex(AssertionError,'Missing ledger snapshot'):reconcile(db,FIXTURE['period'])
    def test_balanced_but_wrong_closing(self):
        with database() as db:
            db.execute("UPDATE gl_balance_snapshot SET signed_balance=signed_balance+CASE WHEN gl_account_id='G_CASH' THEN 1 ELSE -1 END WHERE as_of_date='2026-09-30' AND gl_account_id IN ('G_CASH','G_CLEAR')")
            with self.assertRaisesRegex(AssertionError,'roll-forward'):reconcile(db,FIXTURE['period'])
    def test_unbalanced_opening(self):
        with database() as db:
            db.execute("UPDATE gl_balance_snapshot SET signed_balance=999 WHERE gl_account_id='G_CASH' AND as_of_date='2026-08-31'")
            with self.assertRaisesRegex(AssertionError,'Unbalanced trial'):reconcile(db,FIXTURE['period'])
    def test_subledger_difference(self):
        with database() as db:
            db.execute("UPDATE account_balance_snapshot SET balance_amount=2001 WHERE account_id='D1' AND as_of_date='2026-09-30'")
            with self.assertRaisesRegex(AssertionError,'Subledger control mismatch'):reconcile(db,FIXTURE['period'])
    def test_period_excludes_opening_day(self):
        with database() as db:
            db.execute("UPDATE journal SET booked_on='2026-08-31' WHERE journal_id='J_CP'")
            with self.assertRaisesRegex(AssertionError,'roll-forward'):reconcile(db,FIXTURE['period'])
    def test_same_timestamp_rejected(self):
        import duckdb
        with database() as db:
            with self.assertRaises(duckdb.ConstraintException):
                db.execute("INSERT INTO card_status_event VALUES ('DUP','CARD1','ACTIVE','2026-09-01T10:00:00')")

    def test_offsetting_customer_errors(self):
        with database() as db:
            db.execute("UPDATE account_balance_snapshot SET balance_amount=balance_amount+CASE WHEN account_id='D1' THEN 1 ELSE -1 END WHERE account_id IN ('D1','D2') AND as_of_date='2026-09-30'")
            with self.assertRaisesRegex(AssertionError,'Customer account roll-forward'):reconcile(db,FIXTURE['period'])
