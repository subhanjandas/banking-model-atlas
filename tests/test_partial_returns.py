"""Partial totals, repeated observations and valid intermediate lifecycle views."""
import unittest
from test_demo import database
from run_demo import violations
class PartialReturnsTests(unittest.TestCase):
    def test_valid_partial_view(self):
        with database() as db:
            db.execute("DELETE FROM posting_link WHERE account_entry_id='E_RETURN2'")
            db.execute("DELETE FROM account_entry WHERE account_entry_id='E_RETURN2'")
            db.execute("DELETE FROM payment_return WHERE payment_return_id='RET2'")
            db.execute("DELETE FROM payment_event WHERE payment_event_id='PO_OUT_END'")
            results=violations(db)
            for key in ['C16','C20','C21','C22']:self.assertEqual(results[key],[])
    def test_negative_return(self):
        with database() as db:
            db.execute("UPDATE payment_return SET amount=-1 WHERE payment_return_id='RET1'")
            self.assertTrue(violations(db)['C20'])
    def test_return_before_settlement(self):
        with database() as db:
            db.execute("UPDATE payment_return SET returned_on='2026-09-19' WHERE payment_return_id='RET1'")
            self.assertTrue(violations(db)['C20'])
    def test_return_not_marked_in_lifecycle(self):
        with database() as db:
            db.execute("DELETE FROM payment_event WHERE status IN ('RETURNED','PARTIALLY_RETURNED')")
            self.assertTrue(violations(db)['C22'])

    def test_missing_full_return_event(self):
        with database() as db:
            db.execute("DELETE FROM payment_event WHERE payment_event_id='PO_OUT_END'")
            self.assertTrue(violations(db)['C22'])
