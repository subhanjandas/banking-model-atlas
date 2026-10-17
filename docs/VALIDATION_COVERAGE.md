# Executable coverage

Twenty-seven SQL checks cover selected portions of 47 rule specifications. Each query has a negative-data test. Additional tests cover ledger reconciliation, valid intermediate partial returns and source-ingestion failure/replay behavior. Full banking policy enforcement is not claimed.

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

**Limit:** Original outbound settlement is full; returns can arrive in installments. Rail calendars and fees remain excluded.

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

Full internal reversals have one opposite entry per original; outbound returns use installments.

**Limit:** C20-C22 validate outbound installments separately. Reversal-of-reversal remains unsupported.

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

## C20 — R47

Return installments follow settlement, are positive and never exceed the order amount.

**Limit:** Single-currency full original settlement, with no return fees or FX.

## C21 — R47

Each installment has exactly one equal customer credit on the source account and matching booking date.

**Limit:** Ledger mapping and balances are checked separately; does not prove receipt from a real network.

## C22 — R47

Return status agrees with cumulative returned funds as of every return-state event and latest state.

**Limit:** Return observations use business dates; intraday ordering of same-day installments is not modeled.

## C23 — R43

Fraud case links have a matching card user or account holder, and decisions follow case opening.

**Limit:** Does not perform fraud detection, validate action execution or confirm the assessment is correct.

## C24 — R44

Collections values, promise dates, support intervals and account relationships are structurally coherent.

**Limit:** Days past due and overdue amount are supplied, not calculated. Promise fulfillment and legal eligibility are not implemented.

## C25 — R45

Points snapshots reconcile independently aggregated earnings, fulfilled redemptions and adjustments.

**Limit:** Assumes zero points at enrollment and complete lifetime records. Fulfillment timing is simplified to request date for fulfilled rows.

## C26 — R45

Reward awards use the membership account and valid positive purchase units; corrections stay in membership.

**Limit:** Earning rates, redemption availability and refund clawback policies are supplied, not calculated.

## C27 — R46

Service and complaint events respect intake dates and customer-account relationships.

**Limit:** No regulatory deadlines, delivery confirmation verification or full service workflow transition engine.

See ENGINEERING.md for source completeness relative to a producer manifest and its limitations.
