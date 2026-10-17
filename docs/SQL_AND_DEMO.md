# Run the banking scenarios

The browser is a metadata explorer. The executable demonstration lives in this repository and runs locally with DuckDB, in memory. No bank connection or credentials are needed.

```bash
python3 -m pip install -r requirements-demo.txt
python3 replay.py
```

`generated/banking.duckdb.sql` creates 56 tables in dependency order. It includes primary keys, unique keys, required columns, enumerated-value checks and non-self foreign keys. Self-referencing links are omitted from the physical constraints and checked by the demo's relationship queries. Run it against a fresh database: it intentionally contains no DROP statements or migration logic.

Money uses DECIMAL(18,2). Fixture amounts are decimal strings. The schema does not magically enforce every rule in the business-rule catalogue. Conditional rules, aggregate balancing and history require separate checks.

## What happens in the example?

Alex Example starts with CAD 1,000 in deposit account D1. D2 starts at zero. A credit-card purchase of 120, refund of 20 and external card repayment of 50 leave 50 owed on CC1. An internal transfer moves 250 from D1 to D2. A loan of 1,000 funds D1 and creates 1,000 of principal owed on LN1. An outbound payment of 75 reduces D2. An externally funded loan repayment brings in 110 cash; 100 reduces principal and 10 is interest. It does not debit D1. The outbound payment is then fully returned and the internal transfer fully reversed, with new entries and journals preserving the originals.

| Account | Opening | Closing | Meaning |
|---|---:|---:|---|
| D1 | 1,000.00 | 2,000.00 | Available deposit book balance; holds are separate. |
| D2 | 0.00 | 0.00 | Deposit balance after both payment corrections. |
| CC1 | 0.00 | 50.00 | Credit-card amount owed. |
| LN1 | 0.00 | 900.00 | Remaining loan principal; interest is separate. |

Ten posted journals balance. Twelve mappings connect selected customer entries to journal lines. Independent opening snapshots include cash +1,000 and deposits -1,000 in debit-positive convention. Closing snapshots cover all six ledger accounts. The replay checks opening and closing trial balances, each account roll-forward and customer-account control totals. This covers the supplied single-entity CAD period, not an external bank feed or a regulatory balance sheet.

The ten supplied loan installments each contain 100 principal and 10 interest. This is an illustrative schedule, not an amortization or APR calculator. Credit decisions and onboarding outcomes are supplied records, not automated decision engines.

## Repeatability and bad data

`fixtures/banking_scenarios.json` supplies 175 records across 49 tables. Seven tables remain unpopulated: having a table definition does not imply its lifecycle was exercised. `scripts/run_demo.py` builds the database, loads the records, checks 95 relationships, executes 19 financial queries, computes balances from entries and compares them with independently declared expected balances and supplied snapshots.

`tests/test_demo.py` includes a separate bad-data mutation for every check. For example, an excessive refund, an unbalanced journal and an incorrect repayment principal must each be detected. These tests establish specific behavior, not exhaustive banking coverage.

After intentional model or fixture changes:

```bash
python3 scripts/export_sql.py
python3 scripts/run_demo.py --write-report
python3 scripts/render_docs.py
python3 replay.py
```

The committed report records the DuckDB version and observed counts. CI checks that generated outputs remain current. Read validation_checks.json for the actual queries and their limits.
