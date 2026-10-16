# Executable check coverage

The 38 business rules are specifications. These 13 queries implement selected checks only. Each query returns violating records; an empty result passes for the loaded fixture. Every check has a negative-data regression test.

## C01 — R34

Posted journals have at least two lines and balance independently.

**Limit:** Does not verify that the chosen ledger accounts are economically correct.

## C02 — R35

Mapped entries and ledger lines agree on direction and currency.

**Limit:** Tests mapped pairs; does not prove that all source entries were supplied.

## C03 — R35

Mapped entry allocations are complete and ledger lines are not overallocated.

**Limit:** Entries without any mapping are outside this check; separate source-completeness reconciliation is required.

## C04 — R13

Statement closing balances reconcile to their listed entries.

**Limit:** Checks listed entries; C05 checks membership and account/date scope.

## C05 — R13

Statement lines use the right account/date and every in-cycle entry is listed.

**Limit:** Does not detect overlapping statement cycles or verify minimum-payment policy.

## C06 — R08

Refund references are valid and cumulative refunds do not exceed purchases.

**Limit:** Network-specific refund exceptions and chargebacks are not modeled.

## C07 — R25, R26

Posted deposit orders have exactly the expected customer-account entries.

**Limit:** Only final POSTED/SETTLED orders are checked; transition matrices, account product eligibility and failed-order reversals need additional checks.

## C08 — R27

Outbound settlement agrees with instructions and SETTLED status has evidence.

**Limit:** Partial settlement, returns and settlement-date calendars are excluded.

## C09 — R31

Scheduled principal totals each contracted loan principal.

**Limit:** Does not generate interest or check all schedule dates.

## C10 — R32

Loan funding has one matching loan debit and deposit credit.

**Limit:** Does not verify borrower eligibility or the destination product kind.

## C11 — R33

Posted loan repayments create only their principal reduction on the loan account.

**Limit:** Does not validate installment allocation, principal overpayment or interest-ledger completeness.

## C12 — R10

Every account entry uses exactly its permitted source reference.

**Limit:** Source linkage alone does not validate the source amount or lifecycle.

## C13 — R09, R34

Posted transaction and journal amounts are strictly positive.

**Limit:** Applies to these four tables only; signed balances and nonnegative schedule amounts follow separate conventions.

## Still outside the executable coverage

Full ownership interval validation, status transition matrices, card replacement cycles, real screening, credit scoring, payment-network behavior, accrual engines, accounting period close and regulatory reporting are not implemented. The fixture uses one currency and one fictional legal entity.
