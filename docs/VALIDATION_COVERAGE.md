# Executable coverage

Nineteen SQL checks cover selected portions of 46 rule specifications. Every query has a bad-data regression test. Eight additional ledger tests cover complete-period reconciliation, missing snapshots, balanced-but-wrong positions, opening trial imbalance, subledger differences, period boundaries duplicate event timestamps and offsetting customer-account errors.

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

**Limit:** Checks booked entry shape, including subsequently corrected payments. Does not validate product eligibility.

## C08 — R27

Outbound settlement agrees with instructions and SETTLED status has evidence.

**Limit:** Full outbound settlement and return only; partial settlement and rail calendars are excluded.

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

## C14 — R39

Reversals preserve the original and negate its exact account movement.

**Limit:** Full reversals only; persistence-level immutability is not enforced by this analytical database.

## C15 — R39

Terminal corrected payments have exactly one reversal per original entry and correct payment kind.

**Limit:** Does not model partial returns, fees, network messages or reversal-of-reversal.

## C16 — R40

payment_event history follows its explicit transition matrix.

**Limit:** Requires complete effective-time histories. Corrections, late arrivals and same-time sequencing are not supported.

## C17 — R40

account_status_event history follows its explicit transition matrix.

**Limit:** Requires complete effective-time histories. Corrections, late arrivals and same-time sequencing are not supported.

## C18 — R40

card_status_event history follows its explicit transition matrix.

**Limit:** Requires complete effective-time histories. Corrections, late arrivals and same-time sequencing are not supported.

## C19 — R42

Every account and entry has complete, correctly targeted ledger mappings.

**Limit:** Completeness is relative to supplied source rows, not an external bank feed.

Full rule enforcement remains incomplete. See OPERATIONS.md for the reconciliation scope and lifecycle assumptions.
