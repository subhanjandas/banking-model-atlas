# Operational behavior and reconciliation

Application 1.1.0 / model 0.5.0.

## Corrections preserve history

The internal CAD 250 transfer first posts a debit to D1 and a credit to D2. Its later REVERSED event accompanies two new opposite entries, each linked through reverses_entry_id. The original transfer remains visible.

The outbound CAD 75 order progresses to SETTLED, with settlement evidence. Two payment_return installments of 30 and 45 accompany separate deposit credits and journals debiting cash and crediting deposits. PARTIALLY_RETURNED precedes RETURNED. This represents receipt of the full returned money. It does not erase the original payment or settlement.

Checks reject wrong direction, amount, account, earlier booking date, duplicate reversals and reversal-of-reversal. Internal reversed payments must have one reversal per original entry; outbound installments each have one matching credit. Partial returns are now implemented; fees and network messages remain outside scope. Append-only fixtures demonstrate immutability; the analytical database does not prevent privileged historical updates.

## Lifecycle rules

model/lifecycle_transitions.json declares the fictional bank's allowed transitions. Payment histories start RECEIVED, account histories OPEN and card histories ISSUED. For example, a payment may fail before posting; an internal POSTED payment can become REVERSED; a settled outbound payment can become RETURNED. Closed accounts cannot reopen. A blocked card can become active again.

Checks use effective-time order and require unique timestamps per subject. Histories must be complete. These are project-local choices, not universal rules for every bank. The examples include account restriction/reopening and card blocking/unblocking. They do not yet enforce account eligibility at every transaction timestamp or handle late-arriving event corrections.

## Opening to closing

The period begins after the close of 2026-08-31 and ends at the close of 2026-09-30. Only POSTED journal lines strictly after opening and on or before closing contribute. DRAFT journals do not move ledger balances.

| Ledger account | Opening | Movement | Closing |
|---|---:|---:|---:|
| Cash | 1,000 | 160 | 1,160 |
| Card receivables | 0 | 50 | 50 |
| Loan principal | 0 | 900 | 900 |
| Customer deposits | -1,000 | -1,000 | -2,000 |
| Settlement payable | 0 | -100 | -100 |
| Interest income | 0 | -10 | -10 |
| Total | 0 | 0 | 0 |

All figures are CAD, debit-positive and credit-negative. The opening and closing snapshots are independently supplied expectations, not outputs derived from the same journal aggregation. A balanced but incorrect close must still fail the per-account roll-forward check.

Account Ledger Mapping connects each customer account to its control account. Deposit balances are negated for ledger comparison; card and loan amounts owed remain positive. D1 closes at 2,000, D2 at zero, CC1 at 50 and LN1 at 900. Every supplied booked customer entry must have complete, correctly targeted allocations. Cash, clearing and income include bank-side lines without customer-entry mappings.

This is full opening-to-closing reconciliation for the supplied six-account chart and four customer accounts, one currency and one legal entity. It does not establish completeness against an external source, implement close approvals or cover multicurrency consolidation.

## Try and inspect

Run python3 replay.py after installing requirements-demo.txt. Read generated/demo-report.json for each ledger account's opening, movement and closing values. Explore gl_balance_snapshot and account_gl_mapping in the website; their columns, definitions and relationships are generated from the model.
