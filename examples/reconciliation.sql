-- Run after loading the synthetic fixture with scripts/run_demo.py's database().
-- Grain: one posted journal. Empty result means each supplied posted journal balances.
SELECT j.journal_id,
       SUM(CASE WHEN l.direction = 'DEBIT' THEN l.amount ELSE -l.amount END) AS difference
FROM journal j
JOIN journal_line l USING (journal_id)
WHERE j.status = 'POSTED'
GROUP BY j.journal_id
HAVING difference <> 0;
